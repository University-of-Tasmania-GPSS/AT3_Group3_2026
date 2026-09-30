"""Fetch and reclassify DEA Level-3 land cover into a land-use pressure layer.

Shared by notebooks 05 (Mole Creek), 07 (statewide), and 09 (temporal
sensitivity) -- same STAC access pattern and reclassification everywhere,
extracted here after the third notebook needed it, to stop it drifting
into three slightly-different copies.
"""

import numpy as np
import odc.stac
import pystac_client
import rioxarray
from rasterio.enums import Resampling

DEA_STAC_URL = "https://explorer.dea.ga.gov.au/stac"
DEA_COLLECTION = "ga_ls_landcover_class_cyear_3"

# Level-3 class -> pressure score (0=None, 1=Low, 3=High).
# Checked against real data before finalising this table, not just AT2's
# partial list: every class observed anywhere over Tasmania (confirmed via
# a full statewide STAC load during Stage 7 development) is covered here --
# 111 Cultivated terrestrial vegetation, 112 Natural terrestrial vegetation,
# 124 Natural aquatic vegetation, 215 Artificial surface, 216 Natural bare
# surface, 220 Water. Class 255 (no data) is left unmapped -> stays 255.
PRESSURE_RECLASS = {111: 3, 112: 1, 124: 1, 215: 3, 216: 1, 220: 0}


def fetch_landuse_pressure(bbox_wgs84, year, template_path, target_crs="EPSG:7855"):
    """Fetch DEA Level-3 land cover for `year`, reclassify to a 0-3 land-use
    pressure scale, and align to the raster grid at `template_path`.

    Parameters
    ----------
    bbox_wgs84 : list[float]
        [west, south, east, north] in WGS84 lon/lat (DEA's STAC search requires
        this, regardless of the target CRS used elsewhere in the project).
    year : int
        Calendar year to fetch (DEA Level-3 land cover covers 1988-2024).
    template_path : str or Path
        Path to a GeoTIFF whose grid (CRS, resolution, extent) the result is
        aligned to -- e.g. a DEM template from Stage 1 or Stage 7.
    target_crs : str
        CRS to load the data in before aligning (should match template_path's
        CRS; EPSG:7855 throughout this project).

    Returns
    -------
    numpy.ndarray
        2D uint8 array aligned to the template grid. 255 = nodata (no DEA
        coverage, or the DEA "no data" class).
    """
    catalog = pystac_client.Client.open(DEA_STAC_URL)
    odc.stac.configure_rio(cloud_defaults=True, aws={"aws_unsigned": True})

    search = catalog.search(
        collections=[DEA_COLLECTION], bbox=bbox_wgs84,
        datetime=f"{year}-01-01/{year}-12-31",
    )
    items = list(search.items())
    if not items:
        raise ValueError(f"No DEA Level-3 land cover items found for {year} over {bbox_wgs84}")

    with rioxarray.open_rasterio(template_path) as dem_template:
        dem_template = dem_template.squeeze()
        # Load at the template's own resolution when it's coarser than DEA's
        # native ~30m (avoids pulling more data than needed statewide); never
        # finer than 30m, since that's not real extra detail, just noise.
        template_res = abs(dem_template.rio.resolution()[0])
        load_res = max(template_res, 30)

        land_cover = odc.stac.load(
            items, bands=["level3"], bbox=bbox_wgs84, crs=target_crs,
            resolution=load_res, groupby="solar_day", resampling="nearest",
        )
        arr = land_cover["level3"]
        if "time" in arr.dims:
            arr = arr.isel(time=0)

        pressure = np.full(arr.shape, 255, dtype="uint8")
        for code_val, score in PRESSURE_RECLASS.items():
            pressure[arr.values == code_val] = score
        pressure_da = arr.copy(data=pressure).rio.write_nodata(255)

        pressure_aligned = pressure_da.rio.reproject_match(dem_template, resampling=Resampling.nearest)

    return pressure_aligned.values
