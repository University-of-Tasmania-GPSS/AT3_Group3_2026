# Results

*Which choices change the map?*

This chapter shows the map it produces, then how far each choice we tested moves it, and how well it holds up against independent data. 

## 1. Intrinsic vulnerability at Mole Creek

Intrinsic vulnerability is susceptibility (how karstified and how exposed the rock is) multiplied by connectivity (how much water drains in). It describes the karst itself, before land use or slope is applied.

```{figure} figures/intrinsic_vulnerability_mole_creek.png
:alt: Map of the Mole Creek karst in five blue classes from very low to very high intrinsic vulnerability. Most of the karst is High, with Very high patches in the north and Very low patches in the east.
:width: 100%

Intrinsic vulnerability at Mole Creek (25 m): susceptibility × connectivity. Most of the karst is High (56%), with small Very high areas (5%) where exposed, strongly karstified karst sits low in a large catchment.
```

More than half of the Mole Creek karst (56%) has High intrinsic vulnerability, mostly across the west and centre, where the rock is strongly karstified. The highest class (Very high, 5%) is a small area in the north-west and north-centre where that rock is open to the surface and lies low in a large catchment. The eastern block is Moderate (25%), and the lowest classes are a narrow strip on the south-east edge (Low, 6%) and small patches of karst between other rock layers in the centre and east (Very low, 8%).

Covered and interstratal karst scores lower than exposed karst of the same category.

## 2. Relative risk at Mole Creek

Relative risk multiplies intrinsic vulnerability by land-use pressure and the slope multiplier. It uses LIST land use for 2021, with the scoring set out in the Methods.

```{figure} figures/risk_mole_creek.png
:alt: Map of the Mole Creek karst in five classes of relative risk, from Very Low to Very High.
:width: 100%

Relative karst risk at Mole Creek (25 m).
```

Risk is highest in the west. About four in five of the High (13%) and Very High (15%) cells lie in the western third of the study area, mostly on exposed karst and steeper ground. The centre is mostly Moderate (38%), and the east is mostly Low (26%) or Very Low (8%), where the karst is flat and covered by other rock. Land-use pressure is averaged over each named system, so inside the main Mole Creek system the pattern comes from the ground itself, while the small Chudleigh Hill system, which has higher pressure, is almost all Very High.

Most karst falls in the lower classes. This comes from the arithmetic: the score is the product of numbers below one, so it bunches towards zero, and a place has to score high on every ingredient to score high overall. The classes are therefore narrow (0.025 wide), and the colours show *relative* risk: which places stand out from the rest of Tasmania's karst.

## 3. Across Tasmania

The same model runs across the state at 100 m. The map below shows both results for Tasmania. 

:::{embed} #risk-map-compact
:::

*Interactive map of Tasmania: relative karst risk (low to high, ranked among the karst cells) and intrinsic vulnerability (five blue classes). Choose a layer in the layers menu, use the Mole Creek button to zoom in, click a karst system for its category, exposure, connectivity class, mean slope and mean risk, and switch on the springs. Grey land is outside the mapped karst.*

Across the state, the shares of the karst cells in the intrinsic vulnerability classes are Very low 18%, Low 4%, Moderate 22%, High 47% and Very high 9%. The shares in the relative risk classes are below, with Mole Creek for comparison.

| Class | Score up to | Mole Creek (25 m) | Tasmania (100 m) |
|---|---|---|---|
| Very Low | 0.025 | 8.1% | 37.7% |
| Low | 0.05 | 26.0% | 24.8% |
| Moderate | 0.075 | 37.6% | 24.5% |
| High | 0.10 | 13.0% | 8.3% |
| Very High | above 0.10 | 15.2% | 4.7% |

*Share of the karst cells in each class.*

## 4. Which systems rank highest

Statewide, mean risk per named karst system (100 m). Only the 260 systems with at least 20 cells are ranked, because the top of an unfiltered list is a few systems of 2 to 11 cells.

| Rank | System | Atlas category | Mean risk | Cells |
|---|---|---|---|---|
| 1 | Flowery Gully | A | 0.168 | 120 |
| 2 | Doctors Rocks | B | 0.164 | 71 |
| 3 | Savage River Mine | B | 0.153 | 26 |
| 4 | Gunns Plains | A | 0.146 | 2,998 |
| 5 | Nabageena | B | 0.136 | 103 |
| 6 | Wynyard | C | 0.135 | 173 |
| 7 | Port Hills | B | 0.133 | 57 |
| 8 | Irishtown - Sedgy Creek (2) | B | 0.131 | 106 |
| 9 | Lorinna | B | 0.114 | 169 |
| 10 | Puncheon | B | 0.114 | 132 |
| 33 | Mole Creek | A and B | 0.074 | 24,260 |
| 52 | Meander - Western Creek | D | 0.055 | 1,507 |

Mole Creek (Chudleigh Hill) has only 13 cells at 100 m, so it is left out of the ranking. 132 karst polygons were too small for a single 100 m cell, have no connectivity score and are left out.

## 5. How much do the choices matter?

Each choice was changed one at a time and the result compared with the main map. The measure is the **rank correlation over the mapped karst cells**. 

:::{embed} #choices-chart
:::

| Group | Choice | Mole Creek (25 m) | Tasmania (100 m) |
|---|---|---|---|
| Scale | 2 m DEM | 0.99 | – |
| Scale | 100 m DEM | 0.89 | – |
| Data | DEA land cover | 0.98 | 0.84 |
| Method | Four ingredients added | 0.98 | 0.70 |
| Method | Six ingredients added | 0.55 | 0.82 |
| Method | Slope, flatter = higher | 0.83 | 0.96 |
| Method | Slope, 10 degree ceiling | 0.99 | 0.99 |
| Method | Exposure removed | 0.91 | 0.96 |

```{figure} figures/connectivity_landuse_2x2_mole_creek.png
:alt: Four maps of the Mole Creek karst. The main map, a 100 m DEM, DEA land cover and a six-input weighted sum, each split into fifths of its own cells. The 100 m map is blockier, the DEA map is almost identical to the main map, and the weighted sum looks like a different map.
:width: 100%

The main map and one change on each axis. Each map is split into fifths of its own karst cells, so the colours show each cell's rank.
```

**Scale.** Routing water on a 2 m elevation model gives almost the same map as 25 m (0.99; 88% of polygons fall in the same connectivity class). The 100 m grid changes it more (0.89), mainly because small polygons are covered by only a few cells. 

**Data.** Replacing the Tasmanian land-use layer with the national DEA land-cover layer has little effect on the Mole Creek ranking (similarity = 0.98) but produces greater differences across the state (0.84). These differences reflect contrasting land-cover classifications: LIST distinguishes plantation forestry and irrigated pasture from other land uses, whereas DEA groups these areas within broader natural or cultivated cover classes. DEA also uses a coarser classification scheme (three levels compared with LIST’s 0–10 scale), resulting in higher mean risk scores at Mole Creek (0.095 versus 0.062).

**Method.** 
- Adding the four ingredients instead of multiplying keeps the Mole Creek ordering (0.98) and changes the state's (0.70). It also puts every cell in the top class, because a sum scores about 0.4 to 0.5 where the product scores about 0.06, so a sum needs its own class edges.
- A six-input weighted sum, closer to a literature-style index, gives a very different Mole Creek map (0.55). Indices like this need inputs such as soil cover, depth to groundwater and sinkhole density, which Tasmania has no statewide data for, so catchment flags, watercourses and rainfall stood in. 
- Slope direction matters at Mole Creek (0.83) and hardly at all statewide (0.96). Most Mole Creek karst is gentle, so flipping the rule (flatter = more vulnerable, as in one published method) lifts nearly all of it at once. Lowering the slope ceiling from 30° to 10° barely changes the ordering (0.99).
- Removing exposure changes the map by about as much as moving to a 100 m grid (0.91 at Mole Creek, 0.96 statewide).

### Land-use change moves the level of risk and leaves the pattern in place

```{figure} figures/landuse_trend.png
:alt: Two line charts from 1988 to 2024. High-pressure land on karst swings between about 22% and 65% at Mole Creek and stays between 10% and 19% statewide. Mean risk follows the same shape.
:width: 100%

High-pressure land and mean risk on karst, 1988 to 2024, using DEA land cover (the only source with an annual series).
```

At Mole Creek the share of high-pressure land on the karst swings from 65% (1988) to 22% (2011) and back to 64% (2024), while the pattern of risk stays almost fixed (a correlation of at least 0.9998 between years). Statewide the share is lower, between 10% and 19%. So one year of land use is enough to say *where* risk concentrates, but not *how much* there is, and the map should be updated as land use changes. The LIST layer is a single year (2021), which is a limit.

## 6. Checks against independent data

The one independent check is **mapped springs** (CFEV groundwater-dependent ecosystems), as there is no contamination record to test against. Each spring within a set distance of mapped karst takes the intrinsic score of its nearest karst polygon. The average score for the systems that hold springs is then compared with random draws of karst, weighted by area.

| Distance limit | Systems with springs | Their average score | Karst average | Percentile of the random draws |
|---|---|---|---|---|
| Within 0 m | 17 | 0.50 | 0.34 | 99.9 |
| Within 250 m | 22 | 0.45 | 0.34 | 99.5 |
| Within 500 m | 24 | 0.44 | 0.34 | 99.3 |
| Within 1000 m | 28 | 0.44 | 0.34 | 99.6 |

Springs sit in karst that scores well above the average, at about the 99th percentile, and the result holds when warm and mound springs are removed. Adding exposure raised this from about the 96th percentile. Three caveats keep it a weak check. Springs mark where water *leaves* the karst, which says little about where it enters. The test rests on 12 to 28 systems. And springs are probably mapped using the same karst knowledge that feeds our scores, and more often where karst is exposed, so some of the match is built in.

% TODO: the CFEV comparison goes here, as a new subsection "7. CFEV".
