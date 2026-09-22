# Karst Groundwater Vulnerability in Tasmania

KGG375 GIS Project (AT3) — Group 3, University of Tasmania

## Project Objectives

This project develops a statewide screening model of karst groundwater
vulnerability to agricultural land-use pressure across the whole of
Tasmania's mapped karst areas, then validates the coarse statewide model
against a locally detailed model for a selected verification area
(TBC). The workflow combines a literature-justified weighted linear
combination (WLC) vulnerability index with borehole-derived groundwater
depth data, and evaluates how model resolution and scale affect
vulnerability classification.

Study extent: statewide (Tasmania) for the coarse screening model; one
selected local area, to be decided, for the high-resolution verification
model.

Objectives:
1. Build a statewide WLC-based karst vulnerability index at coarse
   resolution using publicly available Tasmanian geospatial data.
2. Build a high-resolution local model for the selected verification
   area, incorporating additional borehole/groundwater depth data.
3. Compare the two models to evaluate how scale/resolution affects
   vulnerability classification (serving as both sensitivity analysis
   and informal validation).
4. Communicate the workflow and findings via a reproducible MyST/Jupyter
   Book.

## Group Members

- Maggie Meng Li — UTas ID: 142410 — GitHub: [mags612](https://github.com/mags612) — yume0612@gmail.com
- Rachel Elisabeth Roberts — UTas ID: 855396 — GitHub: [RachelElisabethR](https://github.com/RachelElisabethR)

KGG375, University of Tasmania

## AI Usage Acknowledgement

Generative AI tools (Claude, ChatGPT) were used during this project for
brainstorming project scope, discussing methodological options, and
assisting with code development, debugging, and repository setup. All
AI-assisted content was reviewed, tested, and understood by the group
before inclusion, consistent with the unit's Academic Integrity
guidance. This section will be expanded with specific examples as the
project progresses (e.g. which notebooks/functions had AI assistance).

## Published Jupyter Book

Deploys automatically to GitHub Pages on every push to `main` (see
`.github/workflows/deploy.yml`). Once Pages is enabled in the repo
settings, it will be published at:
https://university-of-tasmania-gpss.github.io/AT3_Group3_2026/

## Repository Structure

```
├── README.md
├── environment.yml     # conda environment with all required packages
├── myst.yml            # MyST/Jupyter Book project + table of contents config
├── index.md            # book landing page
├── introduction.md     # motivation / background / objectives (the "hook")
├── methods.md          # study area, data sources, spatial analysis workflow
├── results.md          # key findings, maps, figures
├── discussion.md       # hurdles, limitations, alternative approaches
├── conclusion.md       # take-home point(s)
├── reference.md         # references (APA 7th)
├── notebooks/            # analysis notebooks, run in numbered order
├── src/                  # reusable Python functions (reclassification, WLC, interpolation, etc.)
├── meeting_minutes/       # weekly meeting minutes
└── .github/workflows/deploy.yml   # auto-builds & publishes the book to GitHub Pages
```

Note: raw/processed datasets are **not stored in this repository** — they
are kept in a shared OneDrive folder (University of Tasmania Shared
Libraries) so both group members can access and sync them without
bloating the git history. See "Data Access" below.

## Reproduction Instructions

1. Clone this repository.
2. Create the conda environment:
   ```bash
   conda env create -f environment.yml
   conda activate karst-vulnerability
   ```
3. Request access to the shared OneDrive data folder (see "Data Access"
   below) and update the data path at the top of `notebooks/01_data_prep.ipynb`
   to point to your local copy.
4. Run the notebooks in `notebooks/` in numbered order.
5. Build the book locally:
   ```bash
   jupyter-book build --html
   ```

## Data Access

Datasets are shared via a University of Tasmania OneDrive shared library
folder ("AT3_initial_datasets"), not committed to this repository.
Current contents:

- **Karst Atlas v3.1** — shapefile + geodatabase of mapped karst extent
  and carbonate features, with metadata/data dictionary (2003)
- **LIST CFEV Karst (statewide)** — karst zone polygons with conservation
  value and management priority ratings (published 2015; geometry from
  Karst Atlas v3, 2003; conservation assessment from 2005)
- **LIST Groundwater Boreholes (statewide)** — borehole locations and
  attributes from the Groundwater Information Access Portal
- **DEM** — LIST 25m statewide DEM, per-municipality tiles, **all 29
  municipalities downloaded (complete)**
- **Geology** — Mineral Resources Tasmania geopackages at 1:25,000,
  1:250,000, and 1:500,000 scale, with QGIS symbology files
- **Land use** — not yet downloaded; will be sourced from Digital Earth
  Australia (DEA) Level-3 Land Cover (`ga_ls_landcover_class_cyear_3`),
  using the same STAC-based access pattern as AT2 (see Data Sources
  below for the pipeline)

## Data Sources

- Tasmanian Karst Atlas v3.1 — sourced via Mineral Resources Tasmania / group access (not on public LISTdata Open Data)
- CFEV Karst layer — LISTdata Open Data, DPIPWE Water and Marine Resources Division
- Geology (1:25,000 / 1:250,000 / 1:500,000) — Mineral Resources Tasmania
- LiDAR/25m DEM — LISTdata Open Data (per-municipality tiles, statewide)
- Land use — Digital Earth Australia (DEA) Level-3 Land Cover
  (`ga_ls_landcover_class_cyear_3`), accessed via the DEA STAC catalogue
  (`https://explorer.dea.ga.gov.au/stac`) with `pystac_client` + `odc.stac`,
  no authentication required (anonymous S3 access). Same access method as
  used in AT2. **Note:** AT2's resampling/reclassification steps used
  PyQGIS (`processing.run("gdal:warpreproject", ...)`), which the AT3
  brief explicitly disallows ("modern geospatial stack, i.e. not
  PyQGIS") — for this project, reproject/resample with
  `rioxarray`/`xarray` (`.rio.reproject`, nearest-neighbour for
  categorical data) and reclassify with `numpy`/`xarray` mapping instead.
- Borehole groundwater data — Groundwater Information Access Portal / LISTdata Open Data
