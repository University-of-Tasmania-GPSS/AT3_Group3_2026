"""Watercourse and slope inputs shared by the notebooks: `slope_risk_multiplier` (Stages 6 and 7) and the
watercourse helpers (the weighted-sum test).

Watercourses come from the LIST hydrolines (one folder per council). Only natural watercourses are used:
the layer also holds shorelines, connectors through water bodies, drains and dams, which are unrelated to
streams reaching karst.
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


def slope_degrees(dem, nodata, cell_size):
    """Slope in degrees from a DEM array, via a simple finite-difference gradient."""
    z = np.where(dem == nodata, np.nan, dem.astype(float))
    dzdy, dzdx = np.gradient(z, cell_size)
    return np.degrees(np.arctan(np.hypot(dzdx, dzdy)))


def slope_risk_multiplier(slope_deg, ref_deg=30.0, min_factor=0.5):
    """Slope multiplier on the risk: 0.5 on flat ground, rising to 1 at `ref_deg` degrees or steeper.
    Steeper ground is scored as more vulnerable; the literature does not settle the sign (see the Methods).

    A `ref_deg` of 30 degrees reaches the full factor of 1, and only a small share of mapped karst is this
    steep. The factor has a floor of `min_factor` instead of 0, because flat ground can still carry risk, so
    slope lowers a score without zeroing it.

    Cells next to DEM nodata (coastline, mosaic edges) have an undefined gradient, so `slope_degrees`
    returns NaN there. Those cells take the neutral factor 1.0, which leaves an otherwise valid risk cell intact.
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
