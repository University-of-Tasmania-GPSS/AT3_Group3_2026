"""Karst susceptibility and hydrological connectivity scoring, shared by
notebooks 02, 03, and 07 -- extracted after review found the same logic had
been copy-pasted into all three (making "frozen method" not actually true:
a change made in one place wouldn't reach the others).

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
    whichever of KEXPOSED/KCOVERED/KINTERSTR is non-zero (confirmed mutually
    exclusive in the real data during Stage 2 development)."""
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

# Revised after review flagged exposed==covered==3 as an unjustified choice:
# covered karst has a protective non-karst cap between the surface and the
# karst itself. EPIK's Protective cover (P) factor -- discussed in this
# project's own Framework section when EPIK/COP were compared and set aside
# -- treats that cover as *reducing* vulnerability, not being neutral to it.
# So: exposed keeps the maximum score (no buffering at all); covered is
# still autogenic (it gets its own rainfall -- Data Dictionary confirms this)
# but scored lower to reflect the buffering; interstratal is lower again,
# since per the Data Dictionary it is NOT autogenic at all (its recharge
# depends on an external catchment, i.e. KPROXCATCH, not direct rainfall).
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


# --- Shared: overlap-safe rasterisation -------------------------------------

def rasterize_max(gdf, value_column, out_shape, transform, fill=0, dtype="uint8"):
    """Rasterise `value_column`, with overlapping polygons resolved by
    MAX rather than draw-order (`rasterio.features.rasterize` burns shapes
    in the order given -- last one wins on overlap, which silently produces
    wrong results if a low-value polygon happens to be drawn after a
    high-value one it overlaps). Checked during review: no polygons with
    *different* values genuinely overlap in area in the current Mole Creek
    or statewide data, so this hasn't caused a wrong result yet -- but it's
    one line to fix properly rather than rely on that continuing to hold.
    """
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
    catchment-only polygons have karst_intensity=0, so their intrinsic
    vulnerability -- and therefore their contribution to risk -- is always 0,
    however much high-pressure land they contain. Checked during review:
    26.8% of high-pressure cells at Mole Creek sat in zero-intensity
    (catchment-only) polygons and were contributing nothing. This function
    lets a catchment's land use reach the karst it actually drains into,
    rather than only the pixel directly on top of the karst mattering.

    Two problems found in a second review pass of the first version, both
    fixed here:
    - `KNAME` is blank/null for 454 of 2601 statewide features (5 at Mole
      Creek). A plain `groupby("KNAME")` silently drops NaN groups, so those
      polygons got no aggregation at all rather than an explicit fallback.
      Fixed: blank-name polygons are each treated as their own single-feature
      system (no cross-polygon pooling for them, but explicit, not silent).
    - Some `KNAME` values are shared by genuinely unrelated, widely-separated
      polygons -- "Several" (3 polygons up to 233km apart) and "Various" (2
      polygons 104km apart) are placeholder labels, not real system names;
      even a real name like "Trowutta-Sumac" turned out to have a few
      polygons several km from the main cluster. Pooling pressure across
      polygons that don't actually share a catchment would be wrong. Fixed:
      within each `KNAME` group, only polygons within `max_gap_m` of each
      other (chained transitively) are pooled together. Checked before
      picking 1000m: "Mole Creek" (73 polygons spanning 37km) stays one
      connected system even at 500m, because it's a genuinely contiguous
      chain; "Several"/"Various" split into singletons at any threshold
      tested, because they're never actually close together.

    Still uses a MEAN over each system, not the pixel's own value -- a
    simple, transparent aggregation, not a flow-routed or distance-weighted
    one (which would need more time than this project has). One real
    consequence worth stating in `discussion.md`, not just this docstring:
    every karst cell in a system now gets the *same* pressure value, so
    within-system spatial variation in land use is gone -- the resulting
    risk maps are patchier by system than by the underlying land use.
    """
    effective = pressure_array.copy()
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

# Ordered vocabulary to draw labels from. Reserved for review-fixed reuse
# across Stages 4, 6, and 7 -- previously each notebook hand-typed its own
# label list, which produced an outright duplicate ("Very Low" twice) in
# Stage 7, used "None" vs "Very Low" inconsistently for the same 0.0 value
# between stages, and would silently mis-assign or drop values if the set of
# distinct scores changed upstream (exactly what happened to Stage 4 when
# Stage 3's connectivity scoring was revised: cells with the new 0.5/0.667
# scores fell through a hardcoded 4-value dict and were wrongly left as
# nodata).
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


RISK_EDGES = (0.2, 0.4, 0.6, 0.8)
RISK_LABELS = ["None", "Very Low", "Low", "Moderate", "High", "Very High"]


def classify_fixed(score_array, valid_mask, edges=RISK_EDGES, labels=RISK_LABELS):
    """Classify a 0-1 score into fixed, equal-width classes, with exact 0 kept as
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
