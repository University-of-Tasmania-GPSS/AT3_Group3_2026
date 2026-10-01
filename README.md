# Karst Groundwater Vulnerability in Tasmania

KGG375 GIS Project (AT3) — Group 3, University of Tasmania

## Project Objectives

This project builds a relative karst vulnerability/risk model for
Tasmania by combining three genuinely distinct layers — **karst
susceptibility**, **hydrological connectivity**, and **land-use
pressure** — rather than one large weighted index over every available
dataset. The method is prototyped and frozen at a local case-study area
(**Mole Creek**) before being scaled up statewide, then the statewide
and local results are compared to evaluate how scale/resolution affects
the vulnerability pattern.

Study extent: **Mole Creek** (local, high-resolution — used to develop
and test the method first) and **statewide Tasmania** (coarse — the
tested method applied at scale).

**Mole Creek boundary note:** the Mole Creek study area is the union of
the relevant Karst Atlas polygons, **buffered by 3 km**
(`notebooks/00_bounding_boxes.ipynb`). The unbuffered union covers
essentially 100% of its own area with karst/catchment features, leaving
no surrounding land — found during Stage 3 development, when the
hydrological connectivity layer came out saturated (every polygon
scoring maximum) because there was no background left to score lower.
The same problem would have broken Stage 5 (land-use pressure): the
whole project asks whether *surrounding* land use pressures the karst,
which needs land outside the karst polygons to carry that signal. A 3 km
buffer is a pragmatic, documented choice, not a true watershed
delineation — worth stating as a limitation in `methods.md` rather than
presenting as a rigorously derived catchment boundary.

Objectives:
1. Prototype the vulnerability model at Mole Creek: karst susceptibility
   (Karst Atlas `Kcategory` + exposure type) → hydrological connectivity
   (`Kproxcatch` + DEM-derived drainage) → land-use pressure (DEA land
   cover) → combined relative vulnerability/risk.
2. Freeze the method once it produces a geographically sensible result,
   then apply the same workflow statewide at coarser resolution.
3. Compare the statewide-coarse and Mole-Creek-detailed outputs for the
   Mole Creek area to evaluate how scale/resolution affects
   classification (this doubles as informal validation).
4. **Done — Stage 9** (`notebooks/09_sensitivity_analysis.ipynb`):
   alternative weight emphases, a rainfall experiment (`KAVRAIN`), and
   the multi-year land-use trend (full 37-year annual series at Mole
   Creek, 1988–2024, ~1s/year; 5-year steps statewide). Consistent
   finding across all three: the broad risk pattern is robust
   (r > 0.97 against baseline in every case), but the **top-ranked
   named area is not** — it flips under pressure-emphasis and under the
   rainfall experiment. The land-use trend is genuinely non-monotonic
   (a U-shape, 1988→~2010 low→2024), not the steady increase the
   earlier 2010-vs-2020 snapshot implied — and the same U-shape shows
   up independently statewide, which is itself flagged as possibly a
   DEA product artefact rather than confirmed as a real land-management
   signal, worth checking before leaning on it.
5. Use independent datasets (CFEV GDE springs, CFEV conservation value)
   to validate and contextualise — not to construct — the vulnerability
   score, then combine risk × conservation value into a management
   priority matrix.
6. Communicate the workflow and findings via a reproducible MyST/Jupyter
   Book.

**Explicitly out of scope / optional-only:** borehole data (useful only
if it turns out clean and well-covered at Mole Creek — not a
fundamental model input, since depth/flow/position-accuracy filtering
could become a project of its own); AHP (a small number of transparent,
literature-justified weights are used instead, given only 3–4
criteria); TGD/Karst Index Database cross-checks (time-permitting only).

**Known limitation to state explicitly in the Discussion:** since the
method is developed and tuned at Mole Creek before being frozen and
applied statewide without re-tuning, results elsewhere in the state may
reflect Mole Creek's specific geology/land-use mix rather than a
truly general model.

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
│   ├── 00_bounding_boxes.ipynb   # Tasmania + Mole Creek study area boundaries (EPSG:7855)
│   └── 01_setup_mole_creek.ipynb # Mole Creek karst/geology clip + statewide DEM build
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
   conda activate KGG375_AT3
   ```
3. Request access to the shared OneDrive data folder (see "Data Access"
   below), copy `.env.example` to `.env`, and set `AT3_DATA_DIR` to your
   local path to that folder.
4. Run the notebooks in `notebooks/` in numbered order.
5. Build the book locally:
   ```bash
   jupyter-book build --html
   ```

## Data Access

Datasets are shared via a University of Tasmania OneDrive shared library
folder ("AT3_initial_datasets"), not committed to this repository. It's
split into `Input_data/` (raw source datasets, below) and `Output_data/`
(everything the notebooks generate — reprojected/clipped layers, rasters,
final outputs). Notebooks read raw data via `AT3_DATA_DIR/Input_data/...`
and write generated files to `AT3_DATA_DIR/Output_data/...`.

Current `Input_data/` contents:

- **Karst Atlas v3.1** — shapefile + geodatabase of mapped karst extent
  and carbonate features, with metadata/data dictionary (2003)
- **LIST CFEV Karst (statewide)** — karst zone polygons with conservation
  value and management priority ratings (published 2015; geometry from
  Karst Atlas v3, 2003; conservation assessment from 2005)
- **LIST CFEV Groundwater Dependent Ecosystems / springs (statewide)** —
  sourced; needed for the Stage 10 validation step (used to check the
  model, not to build it — see limitations note above on avoiding
  circularity)
- **LIST Groundwater Boreholes (statewide)** — borehole locations and
  attributes from the Groundwater Information Access Portal
- **DEM** — LIST 25m statewide DEM, per-municipality tiles, **all 29
  municipalities downloaded (complete)**
- **Geology** — Mineral Resources Tasmania geopackages (`geopackage/`) at
  1:25,000, 1:250,000, and 1:500,000 scale, plus a raw shapefile version
  (`geology25k/`) and QGIS symbology files
- **Geoconservation site data** (`geosite_report_4_22-Sep-2026/`) —
  sourced; candidate for the Stage 10 TGD/optional cross-check
- **Tasmania state boundary** (`STE_2021_AUST_SHP_GDA2020/`) — ABS ASGS
  boundary, used for the statewide study extent
- **Land use** — complete for both Mole Creek (`notebooks/05_landuse_pressure.ipynb`)
  and statewide (`notebooks/07_statewide_application.ipynb`), from Digital
  Earth Australia (DEA) Level-3 Land Cover (`ga_ls_landcover_class_cyear_3`),
  fetched on demand via STAC (not a static download — no local raw files
  to list here)
- **Mole Creek study area boundary** — complete (`notebooks/00_bounding_boxes.ipynb`)

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
- Borehole groundwater data — Groundwater Information Access Portal / LISTdata Open Data (optional input, see Objectives)
- CFEV Groundwater Dependent Ecosystems (springs) — LISTdata Open Data, DPIPWE Water and Marine Resources Division (validation only)

## Workflow / Methodology Reference

The full staged workflow (karst susceptibility → hydrological
connectivity → land-use pressure → combined risk, developed at Mole
Creek then scaled statewide, with sensitivity analysis and
validation/context stages) is documented in detail in the group's
"Revised workflow" notes. Key methodological decisions to remember:

- Build/test at **Mole Creek first**, freeze the method, then apply
  statewide — not the other way around.
- Keep vector layers as vectors until something genuinely needs
  rasterising.
- Don't double-count: geology refines/checks the karst susceptibility
  layer rather than contributing its own independent weighted score.
- CFEV GDE springs and CFEV conservation value are validation/context
  only — never inputs to the vulnerability score (avoids circularity).
- Use a small number of transparent, justified weights rather than a
  full AHP exercise.
- DEA land-use fetch/reclassify logic lives in `src/landuse.py`
  (`fetch_landuse_pressure()`), shared by Stages 5, 7, and 9 — not
  copy-pasted per notebook.
- The multi-year land-use trend is a real annual time series (1988–2024
  at Mole Creek, ~5-year steps statewide), not a two-point comparison —
  confirmed feasible before committing to it, not assumed.
- Karst scoring logic (Stages 2/3/7) lives in `src/karst.py`
  (`add_karst_susceptibility()`, `add_connectivity()`), same reason as
  the land-use module — was copy-pasted into three notebooks.

## Fixes from an internal review (30 Sep)

A structured review of Stages 2–8 found several issues worth recording
here rather than letting them sit silently in commit history. Each was
verified against the actual code and data before fixing (a few claims
in the review didn't hold up, or were already fixed by an earlier
commit — noted below too):

**Real bugs, fixed:**
- **Land-use pressure couldn't reach the karst it should affect.**
  Risk = intrinsic vulnerability × pressure is a per-cell product;
  catchment-only polygons have `karst_intensity`=0, so their
  contribution to risk was always 0 however much high-pressure land
  they contained. Measured: 26.8% of high-pressure cells at Mole Creek
  were affected. Fixed with `aggregate_pressure_by_system()` in
  `src/karst.py` — karst cells now use the mean pressure across their
  whole named system (karst + its own catchment), not just the pixel's
  own value. A simple mean, not flow-routed — stated as a limitation.
- **`rasterize()` overlap order.** Overlapping polygons burn in draw
  order (last wins), which can silently produce a wrong value.
  Checked: no polygons with *different* values genuinely overlap in
  area in the current data, so this wasn't live-broken — fixed anyway
  (`rasterize_max()`, sorts ascending so the max value wins) since it's
  a one-line fix for a real footgun.
- **Statewide DEA land cover used nearest-neighbour when downsampling**
  30m native data to 100m, keeping one pixel in ~11 rather than the
  dominant class. Fixed: `mode` resampling when actually downsampling.
- **Exposed and covered karst scored identically** (both "autogenic").
  Revised: covered scores lower (EPIK's Protective Cover logic — a
  non-karst cap reduces vulnerability, not neutral to it).
- **Stage 6 and Stage 8 used different aggregation methods**
  (mean-of-polygon-means vs. pooled-pixel-mean) for what was presented
  as the same per-area statistic, and gave different numbers for the
  same named area as a result. Standardised on pooled everywhere.
- **Stage 8's r=0.91 / 95.6% agreement was computed over all cells**,
  ~77% of which are 0 in both surfaces — agreeing on "nothing here"
  inflates the headline. Now reports both, with the cells-where-
  either-surface-is-nonzero version as the honest headline.
- **02/03 overwrote the same Stage 1 output file in place** — each
  stage now writes its own file (`karst_mc_susceptibility_EPSG7855.gpkg`,
  `karst_mc_connectivity_EPSG7855.gpkg`), so re-running one stage can't
  silently drop another's columns.
- **02's carbonate string match** would also match a hypothetical
  "non-carbonate" description (doesn't occur in the current data, fixed
  anyway).
- **Stage 7's `LABELS` list had "Very Low" twice**, hand-typed with an
  assertion that only checked length, not correctness — replaced with
  `classify_scores()`/`classify_continuous()` in `src/karst.py`, which
  generate labels from whatever values actually occur.
- **Karst scoring was copy-pasted into Stage 7**, not actually shared
  from `src/karst.py` despite Stage 5's land-use fetch already being
  properly shared — fixed, Stage 7 now imports both.
- **Stage 3's `d8_pointer` call was dead code** — computed and never
  used; `d8_flow_accumulation` reads the filled DEM directly. Removed.

**Claims softened, not fixed as bugs (they were accurate about the
model, just overstated as validation):**
- Stage 6's "named areas rank sensibly" check is not independent —
  risk is partly derived from `KCATEGORY`, the same field used to name
  and rank the areas. It confirms the combination arithmetic behaves as
  intended, not that the model is externally validated.
- Stage 7's "cross-check" against Mole Creek isn't independent either —
  Mole Creek is a subset of the same statewide computation with the
  same data and formula, so agreement is partly expected by
  construction, not a genuine replication.

**Checked and found not to hold, or already fixed:**
- The review's claim that Stage 7 doesn't import `fetch_landuse_pressure`
  was against an earlier version — the refactor already fixed this
  before the review.
