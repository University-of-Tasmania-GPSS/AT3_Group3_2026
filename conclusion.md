# Conclusion

:::{div}
:class: tagline
Same karst, different users, different questions.
:::

```{figure} figures/connectivity_landuse_2x2_mole_creek.png
:alt: Four maps of the Mole Creek karst. The main map, a 100 m DEM, DEA land cover and a six-input weighted sum, each split into fifths of its own cells. The 100 m map is blockier, DEA is almost identical to the main map, and the weighted sum looks like a different map.
:width: 90%
:align: center

The main map and one change on each axis. Titles give the rank correlation with the main map (1 = same ordering).
```

## What we found

We built a Karst Intrinsic Vulnerability Index (KIVI) at Mole Creek (25 m), applied it across Tasmania (100 m), and combined it with LIST land use and slope into a relative karst risk map, using the same code and fixed classes at both scales.

**A KIVI for Tasmania.** Susceptibility (Atlas category × exposure) times connectivity (D8 flow routing) runs at 25 m and 100 m with the same five classes. Across the state, 47% of karst cells are High and 9% Very high. Exposure is part of the score because it lifts the springs check from about the 96th to the 99th percentile.

**KIVI with land use.** Multiplying KIVI by LIST 2021 pressure and the slope multiplier gives the risk map. Risk is highest in the west of Mole Creek, and Flowery Gully, Doctors Rocks and Gunns Plains lead the statewide ranking of larger systems. Over the DEA series from 1988 to 2024 the level of risk follows land use and the pattern stays fixed.

**KIVI with conservation value.** Combining KIVI with CFEV Integrated Conservation Value gives a four-class priority map. The top class covers 13% of the karst, mostly in the south-west mountains and at Mole Creek (Results, section 7).

## What the tests showed

- **Method matters most.** The six-input weighted sum gives a very different Mole Creek map (0.55), and adding the four ingredients changes the state's ordering (0.70).
- **Scale matters less.** A 2 m elevation model gives the same map as 25 m (0.99), and the 100 m grid changes it a little (0.89).
- **Data matters least at Mole Creek.** Tasmanian land use and national land cover give the same Mole Creek ranking (0.98) and differ more across the state (0.84), because the Tasmanian layer separates plantations and irrigated pasture.

## What we would do next

- **Add ground truth.** Water-quality or dye-tracing records would let us test the map against measured contamination.
- **Route pressure along the flow paths.** Pressure is a mean over each named system. Routing land use along the flow paths into each karst polygon describes what reaches the karst more closely.
- **Run each LIST snapshot.** LIST has six snapshots (2002, 2009–10, 2013, 2015, 2019 and 2021), and running the model on each shows how risk moves with land use.
- **Keep the sinks.** Flow routing that retains sinks (Whitebox, RichDEM) may suit karst, where sinks can be real sinkholes.
- **Fill the missing inputs.** Soil cover, depth to groundwater and sinkhole density would allow a literature-style index for Tasmania.
- **Flag the small systems.** A confidence mark based on each system's cell count shows where the 100 m map is least reliable.

## Limitations

**Ground truth**
- Nothing measures contamination, so there is no way to say which map is right. The only check is where springs are, and springs mark where water leaves the karst.
- The springs check rests on 12 to 28 systems. The spring locations were probably mapped using the same karst knowledge that feeds our scores, and well-studied karst is more likely to have mapped springs.
- Checking that the most karstified systems rank highest is partly circular, because susceptibility comes from the same Atlas category used to name and rank them.

**Data**
- The national land-cover product cannot see plantations or irrigated pasture. The Tasmanian land-use layer can, and it has six snapshots (2002 to 2021), fewer than DEA's annual series. The main map uses the latest (2021), so change over time is only partly covered.
- The 2 m elevation model was run only at Mole Creek, where it matches the 25 m map (0.99). Whether it matches in karst with steeper or more complex terrain is untested.
- The 100 m statewide run smooths slope and misses small systems. 132 karst areas were too small for a single cell, so they have no connectivity score and are left out of the statewide map.
- Karst susceptibility is only four Atlas categories, and the files we had do not define categories B and C.
- Rainfall from the Atlas is one value per polygon and barely varies at Mole Creek, so we left it out.

**Method**
- Land-use scores, slope direction and class edges are judgement. Published methods disagree on the sign of slope, and our map follows one choice.
- Connectivity is routed over the surface DEM. It cannot see underground drainage or sinkholes, and catchments are cut off at the edge of the 3 km buffer, so polygons near the edge may be slightly under-counted.
- Pressure is averaged over each named system, so every cell in a system gets the same value and the map is patchy by system. This was the choice that changed the Mole Creek map most.
- Scores are relative, and the risk classes are 0.025 wide because the product of four terms rarely exceeds 0.1. The colours show rank within Tasmania's karst.
- Very small systems dominate an unfiltered ranking, so we only rank systems of at least 20 cells.
- We built and froze the method at Mole Creek, so some choices began as judgement calls, and the tests checked them afterwards.
