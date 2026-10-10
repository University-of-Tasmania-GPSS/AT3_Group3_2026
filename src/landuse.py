"""Fetch and reclassify DEA Level-3 land cover into a land-use pressure layer.

Shared by notebooks 05 (Mole Creek), 07 (statewide), and 09 (temporal
sensitivity) -- same STAC access pattern and reclassification everywhere,
extracted here after the third notebook needed it, to stop it drifting
into three slightly-different copies.
"""

import time
from pathlib import Path

import numpy as np
import odc.stac
import pystac_client
import rioxarray
from rasterio.enums import Resampling

DEA_STAC_URL = "https://explorer.dea.ga.gov.au/stac"
DEA_COLLECTION = "ga_ls_landcover_class_cyear_3"


def _with_retry(fn, tries=6, wait_s=20):
    """The DEA STAC service intermittently answers 503; retry with a growing pause."""
    for attempt in range(tries):
        try:
            return fn()
        except pystac_client.exceptions.APIError:
            if attempt == tries - 1:
                raise
            time.sleep(wait_s * (attempt + 1))

# Level-3 class -> pressure score (0=None, 1=Low, 3=High). Covers every
# class observed anywhere over Tasmania: 111 Cultivated terrestrial
# vegetation, 112 Natural terrestrial vegetation, 124 Natural aquatic
# vegetation, 215 Artificial surface, 216 Natural bare surface, 220 Water.
# Class 255 (no data) is left unmapped -> stays 255.
PRESSURE_RECLASS = {111: 3, 112: 1, 124: 1, 215: 3, 216: 1, 220: 0}


def fetch_landuse_pressure(bbox_wgs84, year, template_path, target_crs="EPSG:7855", reclass=None, cache_dir=None):
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
    reclass : dict, optional
        Level-3 class code -> pressure score. Defaults to `PRESSURE_RECLASS`; pass
        another mapping to test an alternative scoring scheme (Stage 9).
    cache_dir : str or Path, optional
        If given, the raw (unreclassified) Level-3 class raster for this
        template+year is cached under `cache_dir` (
        download once, keep the raw file, reuse it for every later run and
        reclass variant). A cache hit needs no network access at all. The
        cache key is `{template filename stem}_{year}_level3.tif`, since in
        practice every call site always pairs the same template with the
        same geographic extent (Mole Creek vs. statewide).

    Returns
    -------
    numpy.ndarray
        2D uint8 array aligned to the template grid. 255 = nodata (no DEA
        coverage, or the DEA "no data" class).
    """
    cache_path = None
    if cache_dir is not None:
        cache_dir = Path(cache_dir)
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_path = cache_dir / f"{Path(template_path).stem}_{year}_level3.tif"

    with rioxarray.open_rasterio(template_path) as dem_template:
        dem_template = dem_template.squeeze()

        if cache_path is not None and cache_path.exists():
            with rioxarray.open_rasterio(cache_path) as cached:
                arr = cached.squeeze().load()
        else:
            catalog = _with_retry(lambda: pystac_client.Client.open(DEA_STAC_URL))
            # Pin the AWS region/endpoint explicitly: GDAL's default region
            # discovery hits the generic (non-bucket-qualified) s3.amazonaws.com
            # endpoint first, which some network environments block even when
            # the bucket-qualified regional endpoint is reachable.
            odc.stac.configure_rio(
                cloud_defaults=True,
                aws={
                    "aws_unsigned": True,
                    "region_name": "ap-southeast-2",
                    "endpoint_url": "s3.ap-southeast-2.amazonaws.com",
                },
            )

            search = catalog.search(
                collections=[DEA_COLLECTION], bbox=bbox_wgs84,
                datetime=f"{year}-01-01/{year}-12-31",
            )
            items = _with_retry(lambda: list(search.items()))
            if not items:
                raise ValueError(f"No DEA Level-3 land cover items found for {year} over {bbox_wgs84}")

            # Load at the template's own resolution when it's coarser than DEA's
            # native ~30m (avoids pulling more data than needed statewide); never
            # finer than 30m, since that's not real extra detail, just noise.
            template_res = abs(dem_template.rio.resolution()[0])
            load_res = max(template_res, 30)

            # Downsampling categorical data (e.g. statewide: 30m native -> 100m)
            # needs majority/mode resampling, not nearest -- nearest just keeps
            # one native pixel in ~11 and throws the other ten away, which can
            # pick a non-dominant class. Only matters when actually downsampling;
            # nearest is correct for Mole Creek's slight 30m->25m upsample.
            load_resampling = "mode" if load_res > 30 else "nearest"

            land_cover = odc.stac.load(
                items, bands=["level3"], bbox=bbox_wgs84, crs=target_crs,
                resolution=load_res, groupby="solar_day", resampling=load_resampling,
            )
            arr = land_cover["level3"]
            if "time" in arr.dims:
                arr = arr.isel(time=0)

            if cache_path is not None:
                arr.rio.write_nodata(255).rio.to_raster(cache_path, compress="LZW", dtype="uint8")

        pressure = np.full(arr.shape, 255, dtype="uint8")
        for code_val, score in (PRESSURE_RECLASS if reclass is None else reclass).items():
            pressure[arr.values == code_val] = score
        pressure_da = arr.copy(data=pressure).rio.write_nodata(255)

        pressure_aligned = pressure_da.rio.reproject_match(dem_template, resampling=Resampling.nearest)

    return pressure_aligned.values
