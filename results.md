# Results

*Which choices change the map, and by how much?*

## The map

:::{embed} #risk-map-compact
:::

*Relative karst risk across Tasmania, with land cover for 2020. Click a karst system for its score, and use the buttons to jump to Mole Creek. Grey land has no karst mapped.*

## Which choices move it

:::{embed} #choices-chart
:::

*How far each choice moves the map: 1 = same ordering of the karst, lower = bigger change. Hover for the values.*

| Choice | Test | Mole Creek (25 m) | Tasmania (100 m) |
|---|---|---|---|
| No catchment averaging of pressure | Other | 0.30 | 0.83 |
| Six-input weighted sum | Method | 0.38 | 0.51 |
| COP slope direction (flatter = higher) | Method | 0.61 | 0.87 |
| 100 m grid instead of 25 m | Scale | 0.83 | – |
| LIST land use | Data | 0.99 | 0.85 |
| All four ingredients summed | Method | 0.94 | 0.89 |
| Slope ceiling of 10 degrees | Method | 0.98 | 0.97 |
| Connectivity weighted double | Other | 0.97 | 0.97 |
| Routing on a 2 m DEM | Scale | 0.99 | – |

- **Scale.** A 2 m DEM gives almost the same map as 25 m (0.99). The coarser 100 m grid moves it more (0.83).
- **Data.** LIST land use barely moves Mole Creek (0.99) and moves the state more (0.85).
- **Method.** Adding the ingredients keeps most of the ordering (0.89 to 0.94) but puts every cell in the top class. The six-input weighted sum changes it most (0.38 and 0.51), and COP's slope direction moves Mole Creek more than the state (0.61 and 0.87).
- **Judgement calls.** Averaging pressure over a system matters most (0.30 at Mole Creek).
- **Springs.** Mapped springs sit in higher-scoring karst (about the 96th percentile), a weak check because springs mark where water leaves.

:::{dropdown} Scale: 2 m, 25 m and 100 m
…
:::

:::{dropdown} Data: DEA and LIST land use
…
:::

:::{dropdown} Method: multiply or add, and the slope rule
…
:::

:::{dropdown} Other judgement calls
…
:::

:::{dropdown} Springs check
…
:::
