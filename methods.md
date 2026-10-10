# Methods

*Where could a spill, a fertiliser run-off or a bad land-use decision reach
Tasmania's groundwater fastest? We answer by scoring every map cell on three
questions, multiplying the answers, and adjusting the result for slope.*

## The approach

```{mermaid}
flowchart LR
    A["<b>1. Susceptibility</b><br/>How karstified<br/>is the rock?<br/><i>Karst Atlas</i>"] --> I
    B["<b>2. Connectivity</b><br/>How directly can<br/>surface water get in?<br/><i>Karst Atlas</i>"] --> I
    I(["<b>Intrinsic<br/>vulnerability</b><br/>= S × C"]) --> R
    C["<b>3. Pressure</b><br/>What is happening<br/>on the land?<br/><i>DEA land cover</i>"] --> R
    D["<b>4. Slope</b><br/>Does runoff<br/>concentrate or soak in?<br/><i>DEM</i>"] --> R
    R(["<b>Relative risk</b><br/>= S × C × P × Slope"])
```

**Why multiply?** A score of zero on any ingredient should mean zero risk:
no karst, no route for water, or nothing on the land to cause harm. Adding
would let a high score on one ingredient hide a zero on another. Slope is
the one exception: it is a 0.5-1 multiplier, because flat ground is not
automatically zero-risk the way no karst or no pressure legitimately is.

## Build small, then go big

We built and tuned the method at **Mole Creek**, a well-known karst area in
northern Tasmania, on a 25 m grid. We then froze it and ran it across **all
of Tasmania** at 100 m, without re-tuning, so the two results could be
compared fairly.

Both use one coordinate system (GDA2020 / MGA55, EPSG:7855). The Mole Creek
study area is the Karst Atlas polygons plus a **3 km buffer**. Without
the buffer there is no surrounding land, so connectivity saturates and land
use has nothing outside the karst to measure. The buffer also contains
neighbouring karst (Lorinna, Stockers Plain, Quamby Brook, Golden Valley).
That karst is context only: every Mole Creek result in this book is reported
for the Mole Creek karst itself.

## The four ingredients, mapped at Mole Creek

### 1. Susceptibility: how karstified is the rock?

Each Karst Atlas polygon carries a category from **A** (most intensely
karstified) to **D**, scored 4 to 1, with 0 for no karst.

```{figure} figures/susceptibility.png
:alt: Two maps of Mole Creek: karst intensity from 0 to 4 and exposure type.

Top, karst intensity (Kcategory score 0 to 4, with A highest). Bottom, whether the karst is exposed, covered by other rock, or interstratal.
```

### 2. Connectivity: how directly does water get in?

Connectivity is the highest of three scores:

| Route | Score |
|---|---|
| Exposed karst (open to rainfall) | 3 |
| Proximal catchment (water flows straight onto the karst) | 3 |
| Covered karst (a non-karst cap filters first, after the protective-cover idea in EPIK; Doerfliger et al., 1999) | 2 |
| Distal catchment, or interstratal karst | 1 |
| None of the above | 0 |

```{figure} figures/connectivity.png
:alt: Map of Mole Creek hydrological connectivity.

Connectivity at Mole Creek. Most of the area scores 3 (exposed karst or proximal catchment).
```

:::{dropdown} A second connectivity version (v2)
Version 2 adds three things to the highest-of-three rule (`notebooks/13_connectivity_v2.ipynb`):
- a **mapped-watercourse signal**, a 50 m buffer around natural streams scored by stream size (major stream or river 3, stream-sized tributary 2, minor tributary 1);
- a **slope scaling** on the catchment signals, from 0.5 on flat catchments to 1 at 15° or steeper, so steeper catchments count for more;
- at Mole Creek only, a **D8 flow-routing score**: for each karst polygon, the number of cells that drain to it, classed by Jenks natural breaks. It was computed on a 2 m DEM (`03alt2`) and again on the 25 m DEM (`03alt3`), and the 25 m result is the one used.

Because v2 puts slope inside connectivity, it is compared with the frozen version on equal slope terms. It is not the default. Its effect is in Results.
:::

### 3. Pressure: what is on the land?

Karst aquifers are poor at purifying water: at Mole Creek, surface run-off is
captured quickly by solutional openings and passes through conduits with little
cleaning (Eberhard & Houshold, 2002). What is on the land therefore matters. We
reclassify Digital Earth Australia (DEA) Level 3 land cover (Geoscience
Australia, n.d.) to a pressure score, using annual maps from 1988 to 2024.

| Land-cover class | Score | Reasoning |
|---|---|---|
| Water | 0 | Open water is not a pollutant source on the land. |
| Natural terrestrial vegetation (native forest and grassland; DEA also places lightly grazed pasture and managed plantations here) | 1 | Low-intensity land use. At Mole Creek, mainly forested catchments had low bacterial counts, and lower turbidity (0.2 to 1.3 NTU against 0.2 to 23.4) and nitrate (up to 0.42 mg-N/L against 2.3) than cleared ones; the medians differ significantly (Mann-Whitney, P < 0.05; Eberhard & Houshold, 2002). |
| Natural aquatic vegetation; natural bare surface | 1 | Natural surfaces with no pollutant source on them. |
| Cultivated terrestrial vegetation (crops and actively managed pasture) | 3 | Cleared Mole Creek catchments (mostly dairy, beef, grazing and cropping land) had higher turbidity and nitrate, and more variable, generally higher bacterial counts (Eberhard & Houshold, 2002). Clearance for farmland is a principal impact on Australian karst (Gillieson & Thurgate, 1999). Agricultural nutrient pressure on karst springs is documented in other temperate regions (Fenton et al., 2017; Huebsch et al., 2014). |
| Artificial surface (urban, roads) | 3 | Impervious surfaces shed run-off and contaminants. |

No land-cover class scores 2, so cells take only 0, 1 or 3.

**How firm are these scores?** Their direction (cultivated above natural) has
local support, although even there catchment lithology controlled most of the water
chemistry and only turbidity (and more weakly nitrate) tracked disturbance
(Eberhard & Houshold, 2002). Their values have no support: we found no study giving numeric weights
across land-use classes. Published karst risk frameworks keep land-use hazard
separate from intrinsic vulnerability (Zwahlen, 2004) and set hazard weights by
expert judgement (Ravbar & Goldscheider, 2007). Our scores are in the same
position, so we treat them as ordinal assumptions and test them in the
sensitivity analysis.

```{figure} figures/pressure.png
:alt: Two maps of Mole Creek land-use pressure, 2010 and 2020.

Land-use pressure at Mole Creek, 2010 (top) and 2020 (bottom). The darkest areas are cultivated or built-up land.
```

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

:::{dropdown} A second pressure version (LIST land-use, v2)
DEA Level 3 cannot separate managed plantation from natural vegetation and
counts lightly grazed pasture as natural. The second version scores the finer
LIST land-use layer (121 classes) on a 0-10 scale instead
(`notebooks/05b_landuse_pressure_list.ipynb`). Classes are scored by the LIST
primary-group hierarchy, from conservation land (1) up to intensive uses
such as feedlots, effluent ponds and waste (10), with plantation forestry
and modified pasture at 6. These values are expert judgement, like the DEA
scores. It is not the default. Its effect is in Results.
:::

### 4. Slope: does runoff concentrate or soak in?

Slope comes from the DEM (25 m at Mole Creek, 100 m statewide). It enters as a **multiplier from 0.5 to 1**: 0.5 on flat ground, rising in a straight line to 1.0 at 30° or steeper. Steeper ground is scored as more vulnerable, on the reasoning that runoff concentrates and runs towards sinkholes instead of soaking in where it falls. Published karst indices disagree on the sign (see the Introduction), so this direction is a judgement, and we tested the opposite direction.

The floor of 0.5 is deliberate. Flat ground is not automatically safe the way "no karst" or "no pressure" is, so slope may lower risk but never zero it. Most karst is gentle, so most cells sit near 0.5 (Results shows what that does to the risk scale). Slope is taken from each run's own DEM, so the 100 m statewide run sees smoother, gentler slopes than the 25 m local run.

```{figure} figures/slope_factor_mole_creek.png
:alt: Map of the slope multiplier on the Mole Creek karst, from 0.5 on flat ground to 1.0 on steep ground. Most of the karst is close to 0.5.

The slope multiplier on the Mole Creek karst. Most of the karst is gentle, so most cells sit near 0.5, and only the steep margins reach 1.0.
```

## Putting it together

Susceptibility (0 to 4) and connectivity (0 to 3) are each divided by their
maximum so that neither dominates because of its scale, then multiplied to give
**intrinsic vulnerability**. Multiplying by pressure and then by the slope
multiplier gives **relative risk**. Risk runs from 0 to 1 and is sorted into fixed
classes of width 0.2: *Very Low*, *Low*, *Moderate*, *High* and *Very High*,
with 0 shown as *None*. The edges are absolute, so a label means the same
score at Mole Creek and statewide, and a class stays empty if no cell reaches it.

## Scaling up to Tasmania

The same code (`src/karst.py`, `src/landuse.py`, `src/hydro.py`) runs statewide at 100 m, with the same fixed classes and 0 to 1 scale. To see what the coarser grid costs, we resample the statewide result onto the Mole Creek grid and compare the two surfaces over the Mole Creek karst.

## How we tested it

- **Scale.** Does the 100 m statewide run reproduce the 25 m local pattern?
- **Sensitivity.** What if we change the weights, use a different year, change how pressure is aggregated, or swap the land-use or connectivity inputs?
- **Structure.** What if the ingredients were added with weights instead of multiplied?
- **Independent data.** Do mapped springs and conservation values line up with the scores? Neither dataset is ever an input to the model.

## Reproducibility

The pipeline is 15 notebooks, run in numbered order, sharing code in `src/`
(`05b` and `09b` run alongside `05` and `09` as their v2 counterparts; there
is no Stage 11 or Stage 12). Two further notebooks, `03alt2` (2 m DEM) and
`03alt3` (25 m DEM), run the D8 flow-routing on the `connectivity-hydlines`
branch. They are not part of the numbered run: the 2 m run is too large to
repeat, so its outputs are shared, and Stage 13 reads the 25 m output and
checks it against the 2 m one. Raw data stays in a shared folder, every other
output is regenerated by the notebooks, and `environment.yml` pins the conda
environment.

The steps, in order:

1. Study areas and setup (00–01)
2. Susceptibility, connectivity and intrinsic vulnerability (02–04)
3. Land-use pressure and relative risk, v1 (DEA) and v2 (LIST) (05, 05b, 06)
4. Statewide run and scale comparison (07–08)
5. Sensitivity and validation (09, 10)
6. Connectivity v2 (slope, watercourses, D8 routing) and the
   connectivity-x-land-use comparison (13, 09b)
7. Alternative risk structures: weighted sum and a clean EPIK replication (14)
