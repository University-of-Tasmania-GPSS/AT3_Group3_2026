# Karst Groundwater Vulnerability in Tasmania

KGG375 GIS Project (AT3) — Group 3, University of Tasmania

## Project Objectives

A relative karst vulnerability/risk model for Tasmania built from three
layers — **karst susceptibility**, **hydrological connectivity** and
**land-use pressure** — rather than one large weighted index. The method
is developed and frozen at **Mole Creek** (local, 25 m), applied
statewide at 100 m without re-tuning, and the two scales are compared.
See `methods.md` for the method.

The Mole Creek study area is the relevant Karst Atlas polygons buffered
by 3 km (`notebooks/00_bounding_boxes.ipynb`). Without the buffer there is
no surrounding land: connectivity saturates and land-use pressure has
nothing outside the karst to measure. The buffer is a pragmatic choice,
not a watershed delineation.

Objectives:
1. Prototype the model at Mole Creek: susceptibility (`Kcategory` +
   exposure type) → connectivity (`Kproxcatch` + DEM drainage) →
   land-use pressure (DEA land cover) → relative risk.
2. Freeze the method, then apply it statewide.
3. Compare statewide-coarse and Mole-Creek-detailed outputs over Mole
   Creek (Stage 8).
4. **Stage 9 — sensitivity** (`notebooks/09_sensitivity_analysis.ipynb`):
   weights, rainfall, the 1988–2024 land-use trend, and the
   catchment-aggregation choice. Aggregation is the largest sensitivity
   (r≈0.10 vs. the frozen method; r>0.94 for every weight/rainfall
   variant). Weights and rainfall shift the top-ranked area. The land-use
   trend is a U-shape at both scales, possibly a shared DEA product
   artefact.
5. **Stage 10 — validation** (`notebooks/10_validation_context.ipynb`):
   CFEV GDE springs check, never build, the model, tested per named
   system (112 points fall in ~25 systems) against a karst-only null.
   Statewide, GDE systems sit at or below typical karst (~0.1st
   percentile). Mole Creek's 37 points all fall in one system, so no
   p-value is reported. A risk × conservation-value matrix gives 51
   high-risk, high/VH-value systems; the gradient is nearly flat (mean
   risk 0.218/0.239/0.277 for M/H/VH), so it is a ranking tool.
6. Communicate the workflow via a reproducible MyST/Jupyter Book.

**Out of scope:** borehole data (depth/flow/accuracy filtering is a
project of its own), AHP (3–4 literature-justified weights are used
instead), and TGD/Karst Index Database cross-checks (not built).

**Known limitation:** the method is tuned at Mole Creek, so statewide
results may reflect its geology/land-use mix.

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
├── environment.yml     # conda environment
├── myst.yml            # MyST/Jupyter Book config
├── index.md, introduction.md, methods.md, results.md,
│   discussion.md, conclusion.md, reference.md   # Book pages
├── notebooks/          # Stages 00–10, run in numbered order
├── src/                # shared code: karst.py, landuse.py
├── meeting_minutes/
└── .github/workflows/deploy.yml   # builds & publishes the Book
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

Datasets live in a University of Tasmania OneDrive shared library
("AT3_initial_datasets"), not in the repository: `Input_data/` (raw
sources) and `Output_data/` (everything the notebooks generate).
Notebooks read and write via `AT3_DATA_DIR`.

Sources (`Input_data/`):
- **Karst Atlas v3.1** (2003) — mapped karst extent and carbonate
  features; via Mineral Resources Tasmania / group access.
- **LIST CFEV Karst** (LISTdata, DPIPWE) — conservation value polygons.
  Used in Stage 10 (field `KT_ICV`: M/H/VH). Boundaries differ from the
  Karst Atlas ("Mole Creek" splits into "Mole Creek 1-4"), so it is joined
  by spatial overlay, not by name.
- **LIST CFEV Groundwater Dependent Ecosystems / springs** (LISTdata,
  DPIPWE) — validation only. 115 points statewide, 37 within Mole Creek.
- **LIST Groundwater Boreholes** — optional, unused.
- **DEM** — LIST 25 m statewide, per-municipality tiles (all 29 downloaded).
- **Geology** — Mineral Resources Tasmania at 1:25,000, 1:250,000 and
  1:500,000 (`geopackage/`, `geology25k/`).
- **Geoconservation site data** (`geosite_report_4_22-Sep-2026/`) —
  sourced, unused.
- **Tasmania state boundary** (`STE_2021_AUST_SHP_GDA2020/`, ABS ASGS).
- **Land use** — DEA Level-3 Land Cover (`ga_ls_landcover_class_cyear_3`),
  fetched on demand via the DEA STAC catalogue
  (`https://explorer.dea.ga.gov.au/stac`) with `pystac_client` +
  `odc.stac`; no authentication needed, no local raw files. AT3 disallows
  PyQGIS, so resampling uses `rioxarray`/`xarray` and reclassification
  uses `numpy`.

## Design Decisions

- Build at Mole Creek first, freeze, then apply statewide.
- Keep vector layers as vectors until something needs rasterising.
- Geology refines the susceptibility layer; it does not add its own
  weighted score (no double-counting).
- CFEV springs and conservation value are validation/context only, never
  inputs to the score.
- A few justified weights, not AHP.
- Shared code: `src/landuse.py` (`fetch_landuse_pressure()`, Stages 5, 7,
  9) and `src/karst.py` (susceptibility, connectivity, classification,
  pressure aggregation; Stages 2, 3, 7).

## Method Corrections (Stages 2–8)

- **Pressure reaching karst:** catchment-only polygons have zero karst
  intensity, so their pressure never reached the risk product (26.8% of
  high-pressure cells at Mole Creek). Karst cells now use the mean
  pressure across their named system (`aggregate_pressure_by_system()`),
  a simple mean, not flow-routed.
- **Resampling:** statewide land cover uses `mode`, not nearest-neighbour,
  when downsampling 30 m to 100 m.
- **Scoring:** covered karst now scores below exposed (EPIK protective
  cover); the Stage 2 carbonate match no longer matches "non-carbonate".
- **Rasterising:** `rasterize_max()` makes overlaps resolve to the max,
  not draw order.
- **Statistics:** Stages 6 and 8 both use pooled-pixel means. Stage 8
  headlines the cells where either surface is nonzero (r=0.91 over all
  cells is inflated by ~77% zero-zero cells).
- **Outputs and code:** each stage writes its own file; labels come from
  `classify_scores()`/`classify_fixed()`; Stage 7 imports the shared
  modules; dead `d8_pointer` call removed.
- **Not independent checks:** Stage 6's "named areas rank sensibly"
  (risk derives partly from `KCATEGORY`, which names and ranks the areas)
  and Stage 7's Mole Creek cross-check (a subset of the same computation)
  confirm the arithmetic, not the model.
