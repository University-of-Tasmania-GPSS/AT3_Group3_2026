"""Karst susceptibility and hydrological connectivity scoring, pressure aggregation and risk
classification, shared by the notebooks so the frozen method stays identical across them.

All reclassification choices here are ordinal, not ratio, scores: a value
of 4 means "more" than 2, not "twice as much".
"""

import geopandas as gpd
import numpy as np
from rasterio.features import rasterize

# --- Stage 2: karst intensity -----------------------------------------------

# KCATEGORY, per the Karst Atlas v3 Data Dictionary (Sharples 2003): A =
# intensely karstified ... D = possibly partially karstified, 0 = not karst.
CATEGORY_SCORE = {"A": 4, "B": 3, "C": 2, "D": 1, "0": 0}


def classify_exposure_type(karst_gdf):
    """Return exposed/covered/interstratal/non-karst per polygon, from
    whichever of KEXPOSED/KCOVERED/KINTERSTR is non-zero (mutually
    exclusive in the data)."""
    def _row_type(row):
        if row["KEXPOSED"] != "0":
            return "exposed"
        if row["KCOVERED"] != "0":
            return "covered"
        if row["KINTERSTR"] != "0":
            return "interstratal"
        return "non-karst"
    return karst_gdf.apply(_row_type, axis=1)


EXPOSURE_CODE = {"non-karst": 0, "interstratal": 1, "covered": 2, "exposed": 3}


def add_karst_susceptibility(karst_gdf):
    """Add `karst_intensity`, `exposure_type`, and `exposure_code` (numeric
    encoding of exposure_type, for rasterising/plotting) columns in place,
    return the same GeoDataFrame for chaining."""
    karst_gdf["karst_intensity"] = karst_gdf["KCATEGORY"].map(CATEGORY_SCORE)
    karst_gdf["exposure_type"] = classify_exposure_type(karst_gdf)
    karst_gdf["exposure_code"] = karst_gdf["exposure_type"].map(EXPOSURE_CODE)
    return karst_gdf


# --- Stage 3: hydrological connectivity -------------------------------------

# Covered karst has a protective non-karst cap between the surface and the
# karst itself; EPIK's Protective Cover (P) factor treats that cover as
# *reducing* vulnerability, not neutral. So: exposed keeps the maximum score
# (no buffering); covered is still autogenic (it gets its own rainfall, per
# the Data Dictionary) but scored lower for the buffering; interstratal is
# lower again since, per the Data Dictionary, it is not autogenic at all --
# its recharge depends on an external catchment (KPROXCATCH), not direct
# rainfall.
AUTOGENIC_SCORE = {"exposed": 3, "covered": 2, "interstratal": 1, "non-karst": 0}


def add_connectivity(karst_gdf):
    """Add `autogenic_score`, `proximal_score`, `distal_score`, and the
    combined `connectivity` (max of the three) columns in place."""
    karst_gdf["autogenic_score"] = karst_gdf["exposure_type"].map(AUTOGENIC_SCORE)
    # KPROXCATCH holds letters (A-D) or "0", so it always reads as text. KDISTCATCH
    # holds only 0/1/2, so a re-export could read it as numbers; the str cast keeps
    # the comparison with "0" valid either way.
    karst_gdf["proximal_score"] = np.where(karst_gdf["KPROXCATCH"] != "0", 3, 0)
    karst_gdf["distal_score"] = np.where(karst_gdf["KDISTCATCH"].astype(str) != "0", 1, 0)
    karst_gdf["connectivity"] = karst_gdf[
        ["autogenic_score", "proximal_score", "distal_score"]
    ].max(axis=1)
    return karst_gdf


# Class edges for the main D8 connectivity score: powers of ten of the ratio of upstream cells to polygon
# cells (class 1: up to 1, 2: 1-10, 3: 10-100, 4: over 100). Fixed, so a class means the same ratio at every scale.
D8_DECADE_EDGES = (1, 10, 100)
# Edges of an earlier five-class scheme, kept for the archived notebooks.
D8_LOG_EDGES = (1, 3, 10, 30)


def log1p_classes(ratio, n_classes=4):
    """Classes 1..n_classes for D8 ratios, from equal-width intervals in log1p space.

    The range runs from the lowest to the highest finite ratio, so each run's breaks follow its own data
    (`log1p` keeps a zero ratio). Returns (classes, ratio_edges): NaN class where the ratio is not finite,
    and the n_classes + 1 interval edges converted back to ratio units.
    """
    ratio = np.asarray(ratio, float)
    ok = np.isfinite(ratio)
    log_values = np.log1p(ratio[ok])
    log_edges = np.linspace(log_values.min(), log_values.max(), n_classes + 1)
    classes = np.full(ratio.shape, np.nan)
    classes[ok] = np.clip(np.digitize(log_values, log_edges[1:-1]) + 1, 1, n_classes)
    return classes, np.expm1(log_edges)


def add_connectivity_d8(karst_gdf, counts_csv, scheme="decades", n_classes=4, edges=None, unrouted="atlas"):
    """Replace the Atlas connectivity with D8 flow-routing connectivity (`add_connectivity` must have run first).

    The D8 signal is `upstream_cells_per_target_cell` from the routing notebooks (03alt3 at 25 m, 03-100m at
    100 m): how many DEM cells drain into each karst polygon, per cell of the polygon. It is classed and
    rescaled to the same 0-3 scale as the Atlas score, so later stages can keep reading `connectivity`. The
    scores are fractional (e.g. 3 * 2/4), so rasterise them with a float dtype, not `rasterize_max`'s default.

    scheme: "decades" (main) classes the ratio at fixed powers of ten (`D8_DECADE_EDGES`: up to 1, 1-10,
        10-100, over 100); "log1p" splits log1p(ratio) into `n_classes` equal-width intervals between the lowest
        and highest ratio of the routed polygons (edges follow each run's data; see `log1p_classes`); "log"
        uses the older five-class edges `D8_LOG_EDGES`. Pass `edges` to override the edges of "decades" or "log".
    unrouted: polygons with no raster cell at this resolution (small polygons at 100 m) have no ratio.
        "atlas" keeps their Atlas score, "zero" sets 0.

    Columns added: `connectivity_atlas` (the Atlas score, kept as the fallback and for checks), `d8_ratio`,
    `d8_class` (1..n, NaN if unrouted) and `connectivity_source` ("d8", "atlas" or "none"); `connectivity` is
    overwritten, and the ratio edges are stored in `karst_gdf.attrs["d8_ratio_edges"]`. Returns the same GeoDataFrame.
    """
    import pandas as pd

    d8 = pd.read_csv(counts_csv)[["target_objectid", "upstream_cells_per_target_cell", "target_raster_cells"]]
    d8 = d8.drop_duplicates("target_objectid").rename(
        columns={"target_objectid": "OBJECTID", "upstream_cells_per_target_cell": "ratio_in",
                 "target_raster_cells": "cells_in"})
    merged = karst_gdf[["OBJECTID"]].merge(d8, on="OBJECTID", how="left")
    ratio = merged["ratio_in"].to_numpy(float)
    routed = np.isfinite(ratio) & (merged["cells_in"].fillna(0).to_numpy() > 0)

    if scheme in ("decades", "log"):
        use = edges if edges is not None else (D8_DECADE_EDGES if scheme == "decades" else D8_LOG_EDGES)
        classes = np.digitize(ratio, use, right=True) + 1
        n, ratio_edges = len(use) + 1, np.asarray(use, float)
    elif scheme == "log1p":
        classes, ratio_edges = log1p_classes(np.where(routed, ratio, np.nan), n_classes)
        n = n_classes
    else:
        raise ValueError(f"scheme must be 'decades', 'log1p' or 'log', not {scheme!r}")

    d8_class = np.where(routed, classes, np.nan)
    atlas = karst_gdf["connectivity"].to_numpy(float)
    karst_gdf["connectivity_atlas"] = atlas
    karst_gdf["d8_ratio"] = np.where(routed, ratio, np.nan)
    karst_gdf["d8_class"] = d8_class
    fallback = atlas if unrouted == "atlas" else 0.0
    karst_gdf["connectivity"] = np.where(routed, 3.0 * d8_class / n, fallback)
    karst_gdf["connectivity_source"] = np.where(routed, "d8", "atlas" if unrouted == "atlas" else "none")
    karst_gdf.attrs["d8_ratio_edges"] = ratio_edges
    return karst_gdf


# --- Shared: overlap-safe rasterisation -------------------------------------

def rasterize_max(gdf, value_column, out_shape, transform, fill=0, dtype="uint8"):
    """Rasterise `value_column`, with overlapping polygons resolved by MAX
    rather than draw order (`rasterio.features.rasterize` burns shapes in
    the order given, so the last one wins on overlap)."""
    ordered = gdf.sort_values(value_column)  # ascending: highest value drawn last, wins
    return rasterize(
        [(geom, val) for geom, val in zip(ordered.geometry, ordered[value_column])],
        out_shape=out_shape, transform=transform, fill=fill, dtype=dtype,
    )


def load_karst_atlas(shapefile_path, target_crs):
    """Load the Karst Atlas, reproject, and drop degenerate line/point
    geometries that gpd.clip() can leave behind at a study-area boundary."""
    karst = gpd.read_file(shapefile_path).to_crs(target_crs)
    return karst[karst.geom_type.isin(["Polygon", "MultiPolygon"])].copy()


# --- Stage 6/7: catchment-aggregated pressure -------------------------------

def _spatial_clusters(geometries, max_gap_m):
    """Split `geometries` into spatially-connected clusters -- two geometries
    are in the same cluster if they're within `max_gap_m` of each other
    (touching/overlapping counts). Returns an int array of cluster labels,
    same length as `geometries`.
    """
    n = len(geometries)
    if n <= 1:
        return np.zeros(n, dtype=int)
    from scipy.sparse import lil_matrix
    from scipy.sparse.csgraph import connected_components
    adj = lil_matrix((n, n), dtype=bool)
    for i in range(n):
        for j in range(i + 1, n):
            if geometries[i].distance(geometries[j]) <= max_gap_m:
                adj[i, j] = True
    _, labels = connected_components(adj, directed=False)
    return labels


def aggregate_pressure_by_system(karst_gdf, pressure_array, transform, pressure_nodata, max_gap_m=1000):
    """Return a copy of `pressure_array` where every KARST cell (not
    catchment-only cells) has been replaced with the MEAN pressure across its
    whole named system -- the karst polygon(s) AND whichever catchment
    polygons share the same `KNAME` *and are spatially connected* to it.

    Why: risk = intrinsic_vulnerability x pressure is a per-cell product, and
    catchment-only polygons have karst_intensity=0, so their contribution to
    risk is always 0, however much high-pressure land they contain -- 26.8%
    of high-pressure cells at Mole Creek were lost this way. This function
    lets a catchment's land use reach the karst it actually drains into,
    rather than only the pixel directly on top of the karst mattering.

    Two `KNAME` issues are handled explicitly:
    - It is blank/null for 454 of 2601 statewide features (5 at Mole Creek);
      a plain `groupby("KNAME")` would silently drop these. Each blank-name
      polygon is instead treated as its own single-feature system.
    - Some names are shared by unrelated, widely-separated polygons --
      "Several" (3 polygons up to 233 km apart) and "Various" (2 polygons
      104 km apart) are placeholder labels, not real system names; even a
      real name like "Trowutta-Sumac" has outlying polygons several km from
      its main cluster. So within each `KNAME` group, only polygons within
      `max_gap_m` of each other (chained transitively) are pooled. At
      `max_gap_m=1000`, "Mole Creek" (73 polygons spanning 37 km) stays one
      connected system, while "Several"/"Various" split into singletons, as
      they should.

    Uses a MEAN over each system, not the pixel's own value -- simple and
    transparent, not flow-routed or distance-weighted. Consequence: every
    karst cell in a system gets the *same* pressure value, so within-system
    spatial variation in land use is gone (see `discussion.md`).
    """
    effective = pressure_array.astype(float)  # float: a uint8 input would truncate the system mean
    shape = pressure_array.shape

    # Blank/null KNAME -> each polygon is its own system (explicit, not a
    # silent groupby-drop). Real names get spatial-cluster splitting below.
    karst_gdf = karst_gdf.copy()
    blank = karst_gdf["KNAME"].isna() | (karst_gdf["KNAME"].astype(str).str.strip() == "")
    karst_gdf.loc[blank, "_group_key"] = [f"__unnamed_{i}" for i in karst_gdf.index[blank]]
    karst_gdf.loc[~blank, "_group_key"] = karst_gdf.loc[~blank, "KNAME"]

    systems = []  # list of (geometries, karst_only_subframe)
    for _, name_group in karst_gdf.groupby("_group_key"):
        if len(name_group) <= 1:
            systems.append(name_group)
            continue
        labels = _spatial_clusters(list(name_group.geometry), max_gap_m)
        for cluster_id in np.unique(labels):
            systems.append(name_group.iloc[labels == cluster_id])

    for group in systems:
        karst_only = group[group["karst_intensity"] > 0]
        if len(karst_only) == 0:
            continue  # this system has no actual karst cells to assign to

        # Rasterize each system's own footprint to index pressure directly,
        # rather than re-opening a file per system (hundreds of times statewide).
        group_pixels_mask = rasterize(
            [(g, 1) for g in group.geometry], out_shape=shape, transform=transform, fill=0, dtype="uint8"
        )
        group_vals = pressure_array[group_pixels_mask == 1]
        group_vals = group_vals[group_vals != pressure_nodata]
        if len(group_vals) == 0:
            continue
        group_mean_pressure = group_vals.mean()

        karst_cells_mask = rasterize(
            [(g, 1) for g in karst_only.geometry], out_shape=shape, transform=transform, fill=0, dtype="uint8"
        )
        effective[karst_cells_mask == 1] = group_mean_pressure

    return effective


# --- Shared: classify a combined score onto whatever distinct values occur -

# Ordered vocabulary to draw labels from, shared across Stages 4, 6 and 7 so
# a given score always gets the same label and new distinct values upstream
# can't silently fall through a hardcoded label list.
_CANONICAL_LABELS = [
    "None", "Very Low", "Low", "Low-Moderate", "Moderate",
    "Moderate-High", "High", "Very High", "Severe", "Extreme",
]


def classify_scores(score_array, valid_mask):
    """Classify `score_array` directly on whatever distinct values actually
    occur within `valid_mask` (not arbitrary quantile breaks -- these scores
    are products of a handful of discrete ordinal inputs, so there are only
    ever a few real combinations, and classifying on the actual values is
    more meaningful than imposing bins on them).

    Returns (class_array, present_values, labels): `class_array` is a uint8
    raster where value i corresponds to present_values[i] and labels[i]
    (255 = outside valid_mask); `present_values` is sorted ascending.
    """
    present = sorted(np.unique(score_array[valid_mask]))
    n = len(present)

    if n > len(_CANONICAL_LABELS):
        labels = [f"Class {i} ({v:.3f})" for i, v in enumerate(present)]
    else:
        # Evenly spread across the vocabulary, always fixing "None" to the
        # lowest value when it's exactly 0 (every stage's score is a product
        # of factors that can be 0, so this always occurs in practice).
        start = 1 if present[0] == 0 else 0
        pool = _CANONICAL_LABELS[start:]
        remaining = n - (1 if start == 1 else 0)
        idxs, used = [], set()
        for k in range(remaining):
            target = round(k * (len(pool) - 1) / max(remaining - 1, 1))
            while target in used and target < len(pool) - 1:
                target += 1
            used.add(target)
            idxs.append(target)
        labels = (["None"] if start == 1 else []) + [pool[i] for i in idxs]

    class_array = np.full(score_array.shape, 255, dtype="uint8")
    for i, val in enumerate(present):
        class_array[valid_mask & np.isclose(score_array, val)] = i
    return class_array, present, labels


# Fixed class edges for the 0-1 risk score. The score is a product of four terms that are each below 1,
# so it rarely exceeds 0.5 (even a strong cell scores about 0.2), and equal 0.05-wide classes spread it
# over the range it actually reaches; 0.2-wide classes put almost every cell in the first.
RISK_EDGES = (0.05, 0.10, 0.15, 0.20)
RISK_LABELS = ["None", "Very Low", "Low", "Moderate", "High", "Very High"]


def classify_fixed(score_array, valid_mask, edges=RISK_EDGES, labels=RISK_LABELS):
    """Classify a 0-1 score into fixed classes at `edges`, with exact 0 kept as
    its own "None" class. Because the edges are absolute, the same label means the
    same score range wherever it is used (Mole Creek and statewide), and a class
    stays empty if no cell reaches it.

    Returns (class_array, edges, labels); class 0 is "None", 255 is outside `valid_mask`.
    """
    class_array = np.full(score_array.shape, 255, dtype="uint8")
    class_array[valid_mask & (score_array == 0)] = 0
    nonzero = valid_mask & (score_array > 0)
    class_array[nonzero] = np.digitize(score_array[nonzero], edges, right=True) + 1
    return class_array, list(edges), list(labels)


# --- Mole Creek focus --------------------------------------------------------

def in_mole_creek_focus(karst_gdf):
    """True for polygons that belong to the Mole Creek systems (the same selection
    Stage 0 buffers). The 3 km buffer also contains neighbouring systems such as
    Lorinna and Stockers Plain, which are context only."""
    names = karst_gdf["KNAME"].fillna("").astype(str)
    return names.str.contains("Mole Creek") | (names == "Meander - Western Creek")


def mole_creek_focus_mask(karst_gdf, shape, transform):
    """Boolean raster of the Mole Creek karst itself (karst_intensity > 0 polygons in
    the Mole Creek systems), on the grid given by `shape` and `transform`."""
    sel = karst_gdf[in_mole_creek_focus(karst_gdf) & (karst_gdf["karst_intensity"] > 0)]
    burned = rasterize([(g, 1) for g in sel.geometry], out_shape=shape, transform=transform,
                       fill=0, dtype="uint8")
    return burned == 1


# --- Connectivity v2 (experimental) ------------------------------------------

def add_connectivity_v2(karst_gdf, mean_slope_deg, slope_ref_deg=15.0, min_factor=0.5):
    """Polygon-level connectivity with slope folded in (`add_connectivity` must have run first).

    A slope factor in [min_factor, 1] scales the catchment-derived signals (proximal and
    distal) by the polygon's mean slope, because steeper catchments deliver runoff more
    readily. The autogenic signal (exposed / covered / interstratal) is not slope-scaled.
    A polygon with no slope value is left unscaled. The watercourse signal is cell-level and
    is combined with this at raster stage (see `hydro.watercourse_raster`).
    """
    s = np.clip(np.asarray(mean_slope_deg, float) / slope_ref_deg, 0, 1)
    factor = np.where(np.isnan(s), 1.0, min_factor + (1 - min_factor) * np.nan_to_num(s))
    karst_gdf["mean_slope_deg"] = mean_slope_deg
    karst_gdf["slope_factor"] = factor
    karst_gdf["proximal_score_v2"] = karst_gdf["proximal_score"] * factor
    karst_gdf["distal_score_v2"] = karst_gdf["distal_score"] * factor
    karst_gdf["connectivity_v2"] = karst_gdf[
        ["autogenic_score", "proximal_score_v2", "distal_score_v2"]
    ].max(axis=1)
    return karst_gdf
