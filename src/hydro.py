"""Watercourse and slope inputs, shared by the frozen method (slope_risk_multiplier, Stages 6-7)
and connectivity v2 (experimental: watercourses, D8 routing, the polygon-level slope factor).

Watercourses come from the LIST hydrolines (one folder per council). Only natural
watercourses are used: the layer also holds shorelines, connectors through water bodies,
drains and dams, which say nothing about streams reaching karst.
"""
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from affine import Affine
from rasterio.features import rasterize
from rasterio.warp import transform_bounds

LIST_NATIVE_CRS = "EPSG:28355"

# Stream size -> how strongly a stream reaching karst delivers water (same 0-3 scale as the other signals).
STREAM_CLASS_SCORE = {
    "Major River": 3, "River": 3, "Minor River": 3, "Major Stream": 3, "Stream": 3,
    "Minor Stream": 2, "Tributary": 2,
    "Minor Tributary": 1,
}


def load_watercourses(hydline_root, bounds_target, target_crs="EPSG:7855"):
    """Natural watercourses inside `bounds_target` (given in `target_crs`); add scores with `score_watercourses`."""
    bbox = tuple(transform_bounds(target_crs, LIST_NATIVE_CRS, *bounds_target))
    parts = []
    for shp in sorted(Path(hydline_root).glob("LIST_HYDLINE_*/list_hydline_*.shp")):
        g = gpd.read_file(shp, bbox=bbox, where="HYDLNTY1 = 'Watercourse'")
        if len(g):
            parts.append(g[["HYD_CLASS", "geometry"]])
    return gpd.GeoDataFrame(pd.concat(parts, ignore_index=True), crs=LIST_NATIVE_CRS).to_crs(target_crs)


def score_watercourses(wc):
    """Add the 0-3 stream-size `score` column from HYD_CLASS."""
    wc = wc.copy()
    wc["score"] = wc["HYD_CLASS"].map(STREAM_CLASS_SCORE).fillna(1).astype(int)
    return wc


def watercourse_raster(watercourses, shape, transform, buffer_m=50):
    """Score raster (0-3): each watercourse is buffered by `buffer_m` (Atlas polygons are coarse,
    and a stream reaching karst loses water along its margin) and burned with its stream-size
    score, the highest score winning where buffers overlap. 0 = no mapped watercourse nearby."""
    from karst import rasterize_max
    wc = watercourses.copy()
    wc["geometry"] = wc.geometry.buffer(buffer_m)
    return rasterize_max(wc, "score", shape, transform, fill=0, dtype="uint8")


def add_d8_connectivity(karst_gdf, d8_csv_path, score_col="hydrological_connectivity_vulnerability_score",
                         max_class=5, out_col="d8_score"):
    """Join Rachel's D8 upstream-routing connectivity score (from the `connectivity-hydlines`
    branch: WhiteboxTools D8 flow-routing from every source cell to each karst target polygon,
    classified into 1-5 Jenks natural-breaks classes on upstream_cells_per_target_cell) onto
    `karst_gdf` by `OBJECTID`, rescaled from Rachel's 1-`max_class` Jenks classes to the same
    0-3 scale `add_connectivity`/`add_connectivity_v2` use for the other signals, so it can be
    combined with them via `max()`.

    Scope limit: Rachel's routing covers only the 66 "core" target polygons in the Mole Creek
    focus (exactly `in_mole_creek_focus()`'s selection), not the statewide karst. Polygons
    outside that set get NaN here, not 0 -- 0 would wrongly imply "checked, no connectivity"
    rather than "not yet routed". Any combination must handle that NaN explicitly (e.g.
    `np.fmax`, which already ignores it) rather than treating an unrouted polygon as worst case.

    This D8 score is empirically uncorrelated with the polygon mean-slope factor used in
    `add_connectivity_v2` (Spearman rho approx -0.02 to -0.18, n=66, not significant) -- it
    measures catchment extent/routing topology, not terrain steepness, so combining the two is
    not expected to double-count the same information.

    Returns the same GeoDataFrame with `d8_score` (0-3, NaN outside the routed set) added in place.
    """
    d8 = pd.read_csv(d8_csv_path)[["target_objectid", score_col]].rename(
        columns={"target_objectid": "OBJECTID", score_col: "_jenks_class"})
    karst_gdf = karst_gdf.merge(d8, on="OBJECTID", how="left")
    karst_gdf[out_col] = (karst_gdf["_jenks_class"] - 1) / (max_class - 1) * 3.0
    return karst_gdf.drop(columns="_jenks_class")


def slope_degrees(dem, nodata, cell_size):
    """Slope in degrees from a DEM array, via a simple finite-difference gradient."""
    z = np.where(dem == nodata, np.nan, dem.astype(float))
    dzdy, dzdx = np.gradient(z, cell_size)
    return np.degrees(np.arctan(np.hypot(dzdx, dzdy)))


def slope_risk_multiplier(slope_deg, ref_deg=30.0, min_factor=0.5):
    """0.5-1 multiplier on the frozen risk from slope, steeper = more vulnerable (the direction
    connectivity v2's own internal slope scaling already assumes, kept for consistency; the
    literature does not settle the sign -- see discussion.md).

    Scaled by `ref_deg` (30 degrees reaches the full factor of 1; only a small share of mapped
    karst is this steep) and floored at `min_factor` rather than 0: flat ground is not
    automatically zero-risk the way zero susceptibility, connectivity or pressure legitimately
    is, so slope must not be able to zero out an otherwise highly vulnerable, well-connected,
    highly-pressured cell just because it happens to be flat.

    A handful of cells next to DEM nodata (coastline, mosaic edges) get a NaN slope from
    `slope_degrees`' finite-difference gradient, not because the terrain is unusual but
    because the gradient itself is undefined there. Those cells get the neutral factor (1.0,
    no attenuation) rather than NaN, so a missing slope estimate cannot silently zero out an
    otherwise valid risk cell the way propagating NaN through the product would.
    """
    s = np.clip(slope_deg / ref_deg, 0, 1)
    factor = min_factor + (1 - min_factor) * s
    return np.where(np.isnan(slope_deg), 1.0, factor)


def mean_slope_by_polygon(gdf, slope_deg, transform):
    """Mean of `slope_deg` over each polygon's cells (NaN where a polygon has no valid cell)."""
    inv = ~transform
    out = np.full(len(gdf), np.nan)
    for k, geom in enumerate(gdf.geometry):
        minx, miny, maxx, maxy = geom.bounds
        c0, r1 = inv * (minx, miny)
        c1, r0 = inv * (maxx, maxy)
        r0, r1 = max(int(np.floor(r0)), 0), min(int(np.ceil(r1)), slope_deg.shape[0])
        c0, c1 = max(int(np.floor(c0)), 0), min(int(np.ceil(c1)), slope_deg.shape[1])
        if r1 <= r0 or c1 <= c0:
            continue
        win = transform * Affine.translation(c0, r0)
        for touched in (False, True):
            m = rasterize([(geom, 1)], out_shape=(r1 - r0, c1 - c0), transform=win,
                          fill=0, dtype="uint8", all_touched=touched).astype(bool)
            vals = slope_deg[r0:r1, c0:c1][m]
            vals = vals[~np.isnan(vals)]
            if len(vals):
                out[k] = vals.mean()
                break
    return out
