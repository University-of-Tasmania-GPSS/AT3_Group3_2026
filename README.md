# Karst Groundwater Vulnerability in Tasmania

KGG375 GIS Project (AT3) — Group 3, University of Tasmania

**Book title:** *Hidden Landscapes, Unseen Risks* — developing a karst vulnerability index to assess land-use pressure and potential water-quality risk in Tasmania.

**Published book:** https://university-of-tasmania-gpss.github.io/AT3_Group3_2026/
(built from the `main` branch by `.github/workflows/deploy.yml`).

## Project aim

Test how **scale**, **data** and **method** choices change a relative karst risk map, then use the best-supported combination to build an index that scales from one cave system (Mole Creek) to the whole state. There is no contamination ground truth, so the result is a *relative* map and the focus is on how much each choice moves it.

The model multiplies four terms, each scaled 0 to 1:

| Term | What it is |
|---|---|
| **Susceptibility** | Karst Atlas category (A–D, scored 4–1) × exposure type (exposed 3, covered 2, interstratal 1) |
| **Connectivity** | D8 flow routing: upstream cells draining to each karst polygon, per polygon cell, in four powers-of-ten classes |
| **Pressure** | LIST Tasmania land-use matrix for 2021 (0–10), averaged over each named karst system; DEA land cover is the tested alternative |
| **Slope** | Multiplier from 0.5 (flat) to 1 (30° or steeper) |

*Intrinsic vulnerability* = susceptibility × connectivity. *Relative risk* = intrinsic vulnerability × pressure × slope. See `methods.md` for the method and `results.md` for the findings.

The method is built and tuned at **Mole Creek** (25 m grid), then applied across **Tasmania at 100 m** and compared. The Mole Creek study area is the Karst Atlas polygons plus a 3 km buffer (`notebooks/00_bounding_boxes.ipynb`), because pressure and routing need the land around the karst. Results are reported for the Mole Creek karst only.

## Main findings

- **Method moves the map most.** Adding the four ingredients instead of multiplying them keeps the Mole Creek order (rank correlation 0.98) and changes the state's (0.70). A six-input weighted sum gives a very different Mole Creek map (0.55). Slope direction changes Mole Creek (0.83) but barely the state (0.96).
- **Scale and data matter less.** A 2 m DEM gives the same map as 25 m (0.99); the 100 m grid changes it more (0.89). Tasmanian land use against DEA land cover barely moves Mole Creek (0.98) and moves the state more (0.84).
- **Exposure** shifts the map a little (0.91 at Mole Creek, 0.96 statewide) and improves the independent springs check (springs sit at about the 99th percentile of the karst score).
- **No single ideal map.** Which map suits depends on the user and the question; the book states the choices and how far each one moves the result.

The "rank correlation" is the Spearman correlation with the main map over the mapped karst cells (1 = same ordering).

**Out of scope:** borehole data, AHP weighting, TGD/Karst Index Database cross-checks, and CFEV karst conservation value (tried as context in Stage 10, then dropped).

**Known limitations:** no contamination data; scores are partly judgement; 132 karst polygons are too small for a 100 m cell and are left without a connectivity score; LIST land use has six snapshots (2002 to 2021), so change over time is only partly covered, and the main map uses 2021. These are set out in the Conclusion.

## Group members

- Maggie Meng Li — UTas ID: 142410 — GitHub: [mags612](https://github.com/mags612) — yume0612@gmail.com
- Rachel Elisabeth Roberts — UTas ID: 855396 — GitHub: [RachelElisabethR](https://github.com/RachelElisabethR)

KGG375, University of Tasmania

## AI usage acknowledgement

Generative AI tools were used in this project: Claude (Anthropic, used through Claude Code) and ChatGPT. They were used to:

- **Assist with code development and debugging:** writing and fixing shared functions in `src/` (for example the susceptibility score, the D8 connectivity classing, overlap-safe rasterising and the colour helpers), editing and re-running the notebooks in order, tracking down errors, and checking outputs against each other.
- **Explain methods and compare options:** discussing alternatives such as multiplying against adding ingredients, class breaks, slope rules and the sensitivity tests, and explaining what published indices (EPIK, COP, DRASTIC) need.
- **Improve written content:** drafting and tightening wording in the book pages, notebook notes and the presentation script, and keeping numbers in the text consistent with the saved outputs.
- **Build figures and the interactive map:** the interactive Leaflet map, the Plotly sensitivity chart, map and figure layouts, and the introduction diagrams (the diagram captions say where an AI helped draw them).
- **Support repository setup:** environment, build configuration and file organisation.

The group chose the research question, the model design and scoring, which tests to run, and how to interpret the results. All AI-assisted code and text was reviewed, run and checked by the group against the saved outputs before inclusion, consistent with the unit's Academic Integrity guidance. AI did not supply any data.

## Repository structure

```
├── environment.yml     # conda environment
├── myst.yml            # MyST / Jupyter Book config (custom.css styles the pages)
├── index.md, introduction.md, methods.md, results.md,
│   discussion.md, conclusion.md, reference.md    # book pages
├── notebooks/          # Stages 00–16, run in numbered order (see below)
├── src/                # shared code (see below)
├── figures/            # figures used by the book, and the interactive map
├── meeting_minutes/
└── .github/workflows/deploy.yml   # builds and publishes the book
```

**Notebooks** (`notebooks/`): `00` bounding boxes, `01` Mole Creek set-up, `02` karst susceptibility, `03` connectivity, `04` and `04_v2` intrinsic vulnerability (without and with exposure), `05` and `05b` land-use pressure (DEA and LIST), `06` relative risk at Mole Creek, `07` statewide run, `08` compare scales, `09` sensitivity, `10` springs check, `13` connectivity across resolution, `14` weighted-sum prototype, `15` interactive map, `16` which choices move the map. `notebooks/archive/` holds retired comparisons.

**D8 routing notebooks** (`03alt3` for 25 m at Mole Creek, `03-100m-hydrological-connectivity` for the state, `03alt2` for 2 m at Mole Creek) run WhiteboxTools and write the count tables that Stages 3, 7 and 13 read. They are slow and are not part of the numbered run; their outputs are shared.

**Shared code** (`src/`): `karst.py` (susceptibility, connectivity, classes, pressure aggregation), `landuse.py` (DEA land cover), `landuse_list.py` (LIST land-use matrix), `hydro.py` (slope, watercourses), `structures.py` (weighted-sum inputs), `d8_routing.py` (upstream counts check), `mapping.py` (map helpers and colours).

Raw and processed datasets are **not stored in this repository**. They are kept in a shared OneDrive folder (University of Tasmania Shared Libraries) so both group members can use them without bloating the git history. See "Data access" below.

## Reproduction instructions

1. Clone this repository.
2. Create the conda environment:
   ```bash
   conda env create -f environment.yml
   conda activate KGG375_AT3
   ```
3. Request access to the shared OneDrive data folder (see "Data access") and set the environment variable `AT3_DATA_DIR` to your local path to it *before* starting Jupyter, for example `export AT3_DATA_DIR="/path/to/AT3_initial_datasets"`. The notebooks read it with `os.environ`.
4. Run the notebooks in `notebooks/` in numbered order. The routing tables from the D8 notebooks are read from the shared `Output_data/` folder.
5. Build the book locally:
   ```bash
   jupyter-book build --html
   ```
   The build does not re-run the notebooks; it uses their saved outputs.

## Data access

Datasets live in a University of Tasmania OneDrive shared library ("AT3_initial_datasets"), not in the repository: `Input_data/` (raw sources) and `Output_data/` (everything the notebooks generate). Notebooks read and write through `AT3_DATA_DIR`.

Sources (`Input_data/`):
- **Karst Atlas v3.1** (2003) — mapped karst extent, category, exposure and catchment flags; via Mineral Resources Tasmania / group access.
- **LIST land use** (LISTdata, DPIPWE) — land-use polygons for 2002, 2009–10, 2013, 2015, 2019 and 2021, scored with the matrix in `src/landuse_list.py`. The 2021 layer is the main pressure layer.
- **DEA Level-3 Land Cover** (`ga_ls_landcover_class_cyear_3`) — the alternative pressure layer, fetched on demand through the DEA STAC catalogue (`https://explorer.dea.ga.gov.au/stac`) with `pystac_client` and `odc.stac`; no authentication needed.
- **LIST CFEV Groundwater Dependent Ecosystems / springs** — independent check only. 115 points statewide.
- **DEM** — LIST 25 m statewide (built per municipality), with a 2 m DEM for Mole Creek used as a check.
- **LIST hydrolines** — watercourses (used in the six-input weighted-sum test).
- **Geology** — Mineral Resources Tasmania at 1:25,000, 1:250,000 and 1:500,000, kept for context.
- **Tasmania state boundary** — ABS ASGS (`STE_2021_AUST_SHP_GDA2020/`).

The unit disallows PyQGIS, so resampling uses `rioxarray` and `xarray`, and flow routing uses WhiteboxTools.

## Design decisions

- Build at Mole Creek first, then apply the same method statewide.
- Keep vector layers as vectors until something needs rasterising.
- Multiply the ingredients, so a place must be high on all of them to score high. The alternatives are tested.
- Exposure is part of susceptibility (karst intensity times exposure), so covered karst scores below exposed karst.
- Connectivity classes use fixed powers of ten, so a class means the same ratio at every resolution.
- Springs are an independent check and never an input to the score.
- Polygons with no routed connectivity score (too small for a 100 m cell) are left out.
- Risk classes are fixed (0.025, 0.05, 0.075, 0.10), so a label means the same score at Mole Creek and statewide; the interactive map colours cells by rank.

## Method notes

- **Pressure reaching karst:** each karst cell takes the mean pressure across its named system, including its catchment polygons (`aggregate_pressure_by_system()`). Only polygons within 1 km of each other under one name are pooled.
- **Overlaps:** `rasterize_max()` resolves overlapping polygons to the maximum and skips polygons with no score.
- **Statistics:** Stages 6 and 8 use pooled-pixel means; rank correlation is the common measure across tests (Stage 16).
- **Not independent checks:** Stage 6's "named areas rank sensibly" is partly circular (risk derives partly from the Atlas category that names and ranks the areas), and the springs check is only independent-ish (the spring and karst data share sources).
