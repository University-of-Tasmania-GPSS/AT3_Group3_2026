# Hydrological connectivity map alignment report

## Study boundary and common map frame

- Study boundary: `C:\Users\innoc\OneDrive - University of Tasmania\AT3_initial_datasets\Output_data\mole_creek_bounding_box_EPSG7855.gpkg` (existing Mole Creek Karst Atlas geometry buffered by 3 km in Stage 0).
- Boundary CRS: `EPSG:7855`; boundary bounds: `(427095.733, 5370570.652, 481521.97, 5410510.649)`.
- Map CRS: `EPSG:7855`. All maps use the same limits: `(425095.733, 5368570.652, 483521.97, 5412510.649)`.
- The frame uses the existing mapping helper's 2 km cartographic margin around the saved 3 km study boundary; no new analysis buffer was created.
- Figure dimensions: 10 x 5.6 inches. Basemap: Esri World Topographic Map, zoom 11, via the existing mapping helper. All maps use the same axis formatter, grid, north arrow, scale bar, and attribution.
- The original Stage 7.1 display used target-polygon bounds plus the helper's margin. Its new exported map uses the common 3 km study frame so it can be compared spatially with the raster stages. The pre-existing susceptibility PNG was not overwritten.

## Raster alignment

All displayed raster layers were checked against `dem_mc_EPSG7855.tif`. No reprojection, crop, manual shift, or resampling was applied.

| Layer | Input file | CRS | Width x height | Pixel size (m) | Bounds | NoData | Matches DEM grid | Plot extent matches bounds |
|---|---|---|---:|---|---|---:|---|---|
| DEM reference | `dem_mc_EPSG7855.tif` | EPSG:7855 | 2178 x 1599 | 25.000000062 x 25.000000062 m | (427075.387, 5370551.486, 481525.387, 5410526.486) | -9999.0 | True | None |
| Filled DEM | `dem_mc_25m_filled_EPSG7855_alt3.tif` | EPSG:7855 | 2178 x 1599 | 25.000000062 x 25.000000062 m | (427075.387, 5370551.486, 481525.387, 5410526.486) | -9999.0 | True | True |
| Flow accumulation | `flow_accum_mc_25m_EPSG7855_alt3.tif` | EPSG:7855 | 2178 x 1599 | 25.000000062 x 25.000000062 m | (427075.387, 5370551.486, 481525.387, 5410526.486) | -32768.0 | True | True |
| D8 pointer | `d8_pointer_mc_25m_EPSG7855_alt3.tif` | EPSG:7855 | 2178 x 1599 | 25.000000062 x 25.000000062 m | (427075.387, 5370551.486, 481525.387, 5410526.486) | -32768.0 | True | True |
| Drainage | `drainage_network_mc_25m_EPSG7855_alt3.tif` | EPSG:7855 | 2178 x 1599 | 25.000000062 x 25.000000062 m | (427075.387, 5370551.486, 481525.387, 5410526.486) | 255.0 | True | True |

## Display choices

- Raster stages: black outlines show the 66 Mole Creek target polygons selected by the Stage 7.1 count table from `karst_mc_susceptibility_EPSG7855.gpkg`.

- Filled DEM: terrain colour ramp; elevation range 156.9 to 1440.0 m; NoData is transparent.
- Flow accumulation: logarithmic colour normalization; valid-cell min/median/90th/99th/max = 1/5/52/4,003/599,326 upstream cells. Raster values remain unchanged.
- D8 pointer: categorical Whitebox-native codes `[0, 1, 2, 4, 8, 16, 32, 64, 128]`; 0 means no downstream pointer; positive codes are compass directions as described in the map legend.
- Drainage: binary values `[0, 1]` with NoData transparent; only value 1 is drawn over the basemap.
- Susceptibility: the existing Stage 7.1 log-scale target classes and the shared `02_karst_susceptibility` magma palette are retained; only the map frame is standardized.

## Flow accumulation distribution

- Valid cells: 1,848,410; min 1; median 5; 90th percentile 52; 99th percentile 4,003; max 599,326 upstream cells.

No analytical raster or vulnerability/connectivity methodology was changed.
