# Methods

## The approach

```{mermaid}
flowchart LR
    A["<b>1. Susceptibility</b><br/>How karstified<br/> times how covered<br> is the rock?<br/>"] --> I
    B["<b>2. Connectivity</b><br/>How much water<br/>drains in?<br/>"] --> I
    I(["<b>Intrinsic<br/>vulnerability</b><br/>= S × C"]) --> R
    C["<b>3. Pressure</b><br/>What is happening<br/>on the land?<br/>"] --> R
    D["<b>4. Slope</b><br/>Does runoff<br/>concentrate or soak in?<br/>"] --> R
    R(["<b>Relative risk</b><br/>= S × C × P × Slope<br/>"])
```

## Build small, then go big

We built and tuned the method at Mole Creek, a well-known karst area in
northern Tasmania, on a 25 m grid, and then froze it and ran it across all
of Tasmania at 100 m. Both use one coordinate system (GDA2020 / MGA55, EPSG:7855). The Mole Creek
study area is the Karst Atlas polygons plus a 3 km buffer. 

The logic of the project is to test how scale, data and method choices change the map and then use the most defensible combination. In practice we built and froze the method at Mole Creek first, so some choices (the equation, the scores) began as judgement calls, and the tests then checked them.

## The four ingredients, mapped at Mole Creek

### 1. Susceptibility: how karstified is the rock and how much cover does the karst have?

Each Karst Atlas polygon carries a category from **A** (most intensely
karstified) to **D**, scored 4 to 1, with 0 for no karst. It also carries an exposure type. Exposed karst is open to the surface and scores 3. Covered karst has a protective cap of other rock and scores 2. Interstratal karst sits between other rock layers, gets little rain of its own, and scores 1. Susceptibility is the two multiplied together, each divided by its maximum, so covered and interstratal karst score below exposed karst of the same category.

```{figure} figures/susceptibility.png
:alt: Two maps of Mole Creek: karst intensity from 0 to 4 and exposure type.

Top, karst intensity (Kcategory score 0 to 4, with A highest). Bottom, whether the karst is exposed, covered by other rock, or interstratal.
```

### 2. Connectivity: how much water potentially reaches each polygon? 

We used the D8 direction map created during the flow accumulation calculation to trace up the hill from each karst polygon and count how many cells could potentially contribute their water to the polygon **D8 flow routing** (WhiteboxTools). All cells on the way to the top of the catchment were counted including the polygon's own cells, except for interstratal karst as it is not considered to receive the rain falling on it itself. 

```{figure} figures/steps_to_find_connectivity_susceptibility_classes.gif
:alt: Two maps of Mole Creek: karst intensity from 0 to 4 and exposure type.
Stages of caculating the hydrological connectivity susceptibility. The gif starts with the DEM.
```

Doing a standard flow accumulation often doesn’t work very well for karst because it fills in the sink which in karst can be actual sink holes, but catchment area, which it effectively measures, can be used as an input. There are other flow accumulation methods that retain the sinks and work better for highly porous karst from Whitebox and RichDEM but we had a time limitation. 

Karst lower in a large catchment receives more water than karst on a divide. The ratio is classed in **powers of ten**: class 1 is a ratio of up to 1 (little more than the polygon's own ground drains in), class 2 is 1 to 10, class 3 is 10 to 100, and class 4 is over 100 (hundreds of times its own area, as for karst low in a big catchment). The four classes are rescaled to 0 to 3. Each step is ten times the last, which suits a ratio that runs from 0 to over 100,000. The edges are the same at every resolution, so a class means the same ratio at 2 m, 25 m and 100 m, and no single large catchment sets the scale.

Routing depends on the DEM, so connectivity is where resolution enters the project:

| Run | DEM | Covers | Used for |
|---|---|---|---|
| Fine | 2 m | Mole Creek | Checking the 25 m run |
| Local | 25 m | Mole Creek | The Mole Creek map |
| Statewide | 100 m | All of Tasmania | The Tasmania map |

The 2 m run is too large to repeat for the state, so it is compared with the 25 m run at Mole Creek, and the 100 m run is compared with both on the polygons they share (`notebooks/13_connectivity_resolution.ipynb`). The Karst Atlas flags were our first connectivity score (the highest of exposure type, proximal catchment and distal catchment). They are archived (`notebooks/archive/`) and kept only as a check on the routing.

**Polygons with no routed score.** At 100 m, 132 of the 1,677 karst polygons (about 0.02% of karst area) are too small to hold a single grid cell, so the routing cannot score them. We leave them out: they have no connectivity score and do not appear on the statewide map or in the rankings. Giving them a substitute score, from the Atlas flags or by leaving connectivity out of the product, would score them on a different basis from every other polygon, and would inflate them. At Mole Creek's 25 m, all 66 polygons are routed. The neighbouring karst inside the 3 km buffer is not routed and is context only.

```{figure} figures/scale_resolution_mole_creek.png
:alt: Three maps of a 5.5 by 4 km part of the Mole Creek karst showing the D8 connectivity class of each polygon when water is routed on a 2 m, 25 m and 100 m DEM. Most polygons keep the same class at all three resolutions.

The same ground at three resolutions: the D8 connectivity class of each karst polygon when water is routed on a 2 m, 25 m and 100 m DEM.
```

### 3. Pressure: what is on the land? 

Karst aquifers are poor at purifying water: at Mole Creek, surface run-off is
captured quickly by solutional openings and passes through conduits with little
cleaning (Eberhard & Houshold, 2002). What is on the land therefore matters, and there is more than one source of land-use data, so two layers are scored and compared:

| | **DEA land cover** | **LIST land use** |
|---|---|---|
| Source | Digital Earth Australia Level 3 land cover (Geoscience Australia, n.d.), annual maps 1988 to 2024, 30 m | LIST Tasmania land-use polygons (2021), 121 classes |
| Classes scored | Six: water, natural vegetation, aquatic vegetation, bare surface, cultivated, artificial | The LIST hierarchy, from conservation land to intensive uses |
| Scale | 0, 1 or 3 | 0 to 10 |
| Sees | Cultivated against natural cover, for any year | Plantation forestry, irrigated pasture, intensive animal production, mining and waste |
| Misses | Cannot separate managed plantation from native forest, and counts lightly grazed pasture as natural | A single year, and a heavier Tasmania-only dataset |

The main map uses **LIST land use**: it is Tasmania's own source and records what the land is used for, not only what covers it. DEA is kept as a tested alternative.

:::{embed} #pressure-slider
:::

*Land-use pressure at Mole Creek in 2021. Natural land is left clear, and each layer darkens from there up to its own maximum score, so darker means higher pressure within that layer.*

:::{dropdown} Why average pressure across a whole catchment?
Pressure on the sinkhole cell itself says little, because the water arriving
there comes from the whole catchment upslope. Catchment-only polygons also
have zero susceptibility, so a per-cell product would ignore their land use
entirely: 26.8% of high-pressure cells at Mole Creek were being missed this
way. Each karst cell now takes the mean pressure across its named system. We
cluster polygons that sit close together, so placeholder names like "Several"
do not merge unrelated systems.
:::

:::{dropdown} Why is bare ground scored low?
It is a natural surface with no pollutant source on it. Fast runoff is already
captured by connectivity, so scoring it again here would count it twice.
:::


### 4. Slope: does runoff concentrate or soak in?

Slope comes from the DEM (25 m at Mole Creek, 100 m statewide). It enters as a **multiplier from 0.5 to 1**: 0.5 on flat ground, rising in a straight line to 1.0 at 30 degrees or steeper. Steeper ground is scored as more vulnerable, on the reasoning that runoff concentrates and runs towards sinkholes instead of soaking in where it falls. The floor of 0.5 is deliberate. Flat ground is not automatically safe the way "no karst" or "no pressure" is, so slope may lower risk but never zero it. Slope is taken from each run's own DEM, so the 100 m statewide run sees smoother, gentler slopes than the 25 m local run. The sign and the ceiling are judgements, tested as part of the method test below.

```{figure} figures/slope_factor_mole_creek.png
:alt: Map of the slope multiplier on the Mole Creek karst, from 0.5 on flat ground to 1.0 on steep ground. Most of the karst is close to 0.5.

The slope multiplier on the Mole Creek karst.
```

## Putting it together 

Susceptibility (0 to 4) and connectivity (0 to 3) are each divided by their
maximum so that neither dominates because of its scale, then multiplied to give
**intrinsic vulnerability**. Multiplying by pressure and then by the slope
multiplier gives **relative risk**. Risk is a product of four terms that are each
below 1, so it rarely exceeds 0.5 (a strong cell scores about 0.1 with LIST pressure and exposure). It is sorted into fixed
classes at 0.025, 0.05, 0.075 and 0.10: *Very Low* (up to 0.025), *Low*, *Moderate*, *High* and
*Very High* (above 0.10), with 0 shown as *None*. The edges are absolute, so a label means the same
score at Mole Creek and statewide, and a class stays empty if no cell reaches it.

### The scores in one place

Every ingredient is scaled to 0 to 1 before it enters the equation:

| Ingredient | Raw score | Scaled by |
|---|---|---|
| Susceptibility (S) | Karst Atlas category A to D scored 4 to 1, times exposure (exposed 3, covered 2, interstratal 1), 0 for no karst | each divided by its maximum, then multiplied |
| Connectivity (C) | Four D8 log classes, scaled to 0 to 3 | divided by 3 |
| Pressure (P) | LIST land-use matrix, 0 to 10: conservation and natural land 1, plantation forestry 6, intensive uses up to 10 | divided by 10 |
| Slope | Multiplier from 0.5 (flat) to 1 (30 degrees or steeper) | used as it is |

The land-use scores are expert judgement in both versions (DEA classes in `05`, the LIST matrix in `src/landuse_list.py`).

### How the ingredients combine 

Both EPIK and COP multiply their factors, while methods such as DRASTIC add weighted scores, so we run the alternatives
(`notebooks/14_weighted_sum_prototype.ipynb`):

| Structure | How the ingredients combine | Inputs |
|---|---|---|
| **Product (main)** | S × C × P × slope | The four ingredients above |
| Same inputs, all summed | A weighted sum of S, C, P and slope, zero off the karst; equal weights and 3:3:2:1 | The same four |
| Six-input weighted sum | Equal weights over susceptibility, exposure, catchment flags, watercourse, slope and rainfall, then × P | Six inputs, closer to a literature-style index |
| EPIK and COP replications | EPIK's 3:1:3:2 weights over its four analogues; COP's O × C × P product | Each method's own factors |

Keeping the inputs the same in the first two rows separates the effect of structure from the effect of data.

:::{embed} #structure-slider
:::

*The main product (left) against the four ingredients added with equal weights (right), Mole Creek. The two are on different scales (the sum scores 0.4 to 0.5, the product mostly under 0.1), so each map is split into fifths of its own karst cells: the colours show where each map ranks a cell, not how large its score is.*

#### How slope enters

Slope is part of the method too. Published rules differ, and COP (Vías et al., 2006) gives slope two signs, so we run our rule against COP's and against lower ceilings (`notebooks/09_sensitivity_analysis.ipynb`, section 9.7):

| Rule | Direction | Form |
|---|---|---|
| Ours (main) | Steeper = higher | Continuous, 0.5 to 1 at 30 degrees |
| Lower ceilings | Steeper = higher | Continuous, reaching 1 at 20, 15 or 10 degrees |
| COP Scenario 1 (water draining to a swallow hole) | Steeper = higher | Four classes at 8%, 31% and 76% slope (4.6, 17.2 and 37.2 degrees) |
| COP Scenario 2 (diffuse recharge on the karst itself) | Flatter = higher, because runoff on steep ground leaves the karst | The same four classes, reversed |

COP's vegetation split is dropped because pressure already scores land cover.

## Scaling up to Tasmania

The same code (`src/karst.py`, `src/landuse.py`, `src/hydro.py`) runs statewide at 100 m, with the same fixed classes, the same connectivity breaks and the same 0 to 1 scale. To see what the coarser grid costs, we resample the statewide result onto the Mole Creek grid and compare the two surfaces over the Mole Creek karst.

## How we tested it

- **Scale.** Does the 100 m statewide run reproduce the 25 m local pattern, and does routing on a 2 m DEM change the Mole Creek map?
- **Data.** Does swapping LIST land use for DEA land cover change the map?
- **Method.** Does adding weighted scores instead of multiplying them, or a different slope rule, change the map, and does it change how well springs line up with the scores?
- **Independent data.** Do mapped springs line up with the scores? The springs data is never an input to the model.

## Sensitivity

The three tests above vary the choices the Introduction names. The model also rests on smaller judgement calls, and each is run once against the main map (`notebooks/09_sensitivity_analysis.ipynb`):

| Judgement | Main choice | What we varied |
|---|---|---|
| Catchment averaging of pressure | Mean over each named system, polygons within 1 km chained | No averaging; other distance thresholds |
| Weights | Equal (each ingredient to the power 1) | Each ingredient doubled in turn |
| Pressure scores | LIST matrix, 0 to 10 | For the DEA version: natural land at 0; a milder 1:2 contrast |
| Rainfall | Not used | A 0.5 to 1 modifier from the Atlas rainfall field |

Every test, and these judgement calls, is scored on one measure in `notebooks/16_which_choices_matter.ipynb`: the rank correlation with the main map over the mapped karst. The land-cover year is not a sensitivity. It is a change to track, and the final map uses 2021 land use.

## Reproducibility

The pipeline is 17 notebooks, run in numbered order, sharing code in `src/`
(`05b` builds the LIST pressure layer that Stage 6 uses, and `05` is the DEA alternative; there is no Stage 11 or
Stage 12, and the retired Atlas connectivity comparisons are in `notebooks/archive/`). Three further notebooks run the D8
flow-routing that feeds the connectivity score: `03alt3` (25 m DEM) for
Mole Creek, `03-100m-hydrological-connectivity` (100 m DEM) for all of
Tasmania, and `03alt2` (2 m DEM, Mole Creek) for the scale check. They sit
before Stages 3 and 7 and are not part of the numbered run: the routing is
slow and the 2 m run is too large to repeat, so their count tables are shared
outputs that Stages 3, 7 and 13 read. Raw data and those tables stay in a
shared folder, every other output is regenerated by the notebooks, and
`environment.yml` pins the conda environment.

The steps, in order:

1. Study areas and setup (00–01)
2. Susceptibility, connectivity and intrinsic vulnerability (02–04, with exposure in 04 v2)
3. Land-use pressure, DEA (05) and LIST (05b), and relative risk (06)
4. Statewide run and scale comparison (07–08)
5. Sensitivity and validation (09, 10)
6. Connectivity across resolution, springs test and the Atlas check (13)
7. The method test: product against weighted sum, with EPIK and COP replications (14)
8. The interactive risk map on the Results page (15)
9. Which choices move the map: one comparison of every test on a single measure (16)
