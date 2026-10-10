"""Land-use pressure from the LIST Tasmania land-use polygons (experimental).

Alternative to the DEA land-cover reclass in landuse.py. Scores are expert
judgement on a 0-10 scale, anchored to the LIST primary-group hierarchy
(1 conservation ... 5 intensive uses) with adjustments within each group.
"""
import geopandas as gpd
from rasterio.warp import transform_bounds

from karst import rasterize_max

LIST_NATIVE_CRS = "EPSG:28355"

# Longest matching code prefix wins ("5.7.1" before "5.7" before "5").
MATRIX = {
    "1": 1,
    "2.1": 4, "2.2": 3,
    "3.1": 6, "3.2": 6, "3.2.1": 5, "3.3": 7, "3.4": 6, "3.5": 6, "3.6": 5,
    "4.1": 6, "4.2": 8, "4.3": 9, "4.4": 7, "4.5": 9, "4.6": 6,
    "5.1": 7, "5.2": 10, "5.2.5": 0, "5.3": 8, "5.4": 7, "5.4.3": 6,
    "5.5": 5, "5.6": 3, "5.7": 6, "5.7.1": 7, "5.7.4": 7, "5.8": 7, "5.9": 10,
    "6": 0,
}


def code_string(lu_coden):
    """113 -> '1.1.3' (works for every LIST year, which all carry LU_CODEN)."""
    return ".".join(str(int(lu_coden)).zfill(3))


def lookup_score(code, mapping):
    parts = code.split(".")
    for n in range(len(parts), 0, -1):
        key = ".".join(parts[:n])
        if key in mapping:
            return mapping[key]
    raise KeyError(f"No score for land-use code {code}")


def load_list_landuse(shp_path, target_crs, bounds_target=None):
    """Read the LIST layer (optionally only inside `bounds_target`, given in
    `target_crs`), reproject, and add a dotted `lu_code` column."""
    bbox = None
    if bounds_target is not None:
        bbox = tuple(transform_bounds(target_crs, LIST_NATIVE_CRS, *bounds_target))
    gdf = gpd.read_file(shp_path, bbox=bbox).to_crs(target_crs)
    gdf = gdf[gdf.geom_type.isin(["Polygon", "MultiPolygon"])].copy()
    gdf["lu_code"] = gdf["LU_CODEN"].map(code_string)
    return gdf


def pressure_raster(gdf, mapping, shape, transform):
    """Score raster on the template grid. -1 = no LIST polygon (nodata)."""
    gdf = gdf.copy()
    gdf["score"] = gdf["lu_code"].map(lambda c: lookup_score(c, mapping)).astype("float32")
    return rasterize_max(gdf, "score", shape, transform, fill=-1, dtype="float32")
