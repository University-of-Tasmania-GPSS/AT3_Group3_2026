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

## Take-home points

We set out to test how scale, data and method choices change a karst risk map, and to build one model that runs from Mole Creek to the whole of Tasmania.

- **Method matters most.** Adding the ingredients instead of multiplying them, or using a six-input weighted sum, changes the map more than a finer elevation model or a different land-use layer. The six-input sum gave a very different Mole Creek map (0.55), and adding the four ingredients changed the state's ordering (0.70).
- **Data and scale matter less.** A 2 m elevation model gives the same map as 25 m (0.99), and the 100 m grid changes it only a little (0.89). Tasmanian land use against national land cover barely moves Mole Creek (0.98) and moves the state more (0.84), because the Tasmanian layer can see plantations and irrigated pasture.
- **One model scales from a cave system to the state.** The same code and fixed classes run at 25 m locally and 100 m statewide. The coarse map is good for screening the state, and finer data is worth using where a decision depends on it.
- **Exposure belongs in the model.** Scoring how exposed the karst is changes the map a little (0.91 at Mole Creek) and strengthens the springs check: springs sit at about the 99th percentile of the karst score, up from about the 96th.
- **The map is relative.** It ranks places against each other, and the right map depends on who is asking and what they need to decide.

## What we would do next

- **Add ground truth.** Water-quality or dye-tracing records would let us test the map against something other than where springs are.
- **Route pressure along the flow paths.** Pressure is a simple mean over each named system. Routing land use along the flow paths into each karst polygon would be a better description of what reaches the karst.
- **Keep the sinks.** Standard flow routing fills sinks, which in karst can be real sinkholes. Methods that retain sinks (in Whitebox and RichDEM) may work better, and we did not have time to test them.
- **Fill the missing inputs.** Soil cover, depth to groundwater and sinkhole density would make a literature-style index possible for Tasmania.
- **Track land-use change.** LIST has six snapshots (2002, 2009–10, 2013, 2015, 2019 and 2021). Running the model on each would show how risk moves as land use changes.
- **Flag the small systems.** A confidence mark based on how many grid cells each system has would show where the 100 m map is least reliable.

:::{dropdown} Limitations

**Ground truth**
- Nothing measures contamination, so there is no way to say which map is right. The only check is where springs are, and springs mark where water leaves the karst.
- The springs check rests on 12 to 28 systems. The spring locations were probably mapped using the same karst knowledge that feeds our scores, and well-studied karst is more likely to have mapped springs.
- Checking that the most karstified systems rank highest is partly circular, because susceptibility comes from the same Atlas category used to name and rank them.

**Data**
- The national land-cover product cannot see plantations or irrigated pasture. The Tasmanian land-use layer can, and it has six snapshots (2002 to 2021), fewer than DEA's annual series. The main map uses the latest (2021), so change over time is only partly covered.
- We ran the 2 m elevation model only at Mole Creek, as a check. It matched the 25 m map, so finer data did not look worth pursuing.
- The 100 m statewide run smooths slope and misses small systems. 132 karst areas were too small for a single cell, so they have no connectivity score and are left out of the statewide map.
- Karst susceptibility is only four Atlas categories, and the files we had do not define categories B and C.
- Rainfall from the Atlas is one value per polygon and barely varies at Mole Creek, so we left it out.

**Method**
- Land-use scores, slope direction and class edges are judgement. Published methods disagree on the sign of slope, and our map follows one choice.
- Connectivity is routed over the surface DEM. It cannot see underground drainage or sinkholes, and catchments are cut off at the edge of the 3 km buffer, so polygons near the edge may be slightly under-counted.
- Pressure is averaged over each named system, so every cell in a system gets the same value and the map is patchy by system. This was the choice that changed the Mole Creek map most.
- Scores are relative, and the risk classes were re-set to 0.025 steps when the land-use layer and exposure lowered the scores. The colours show rank within Tasmania's karst.
- Very small systems dominate an unfiltered ranking, so we only rank systems of at least 20 cells.
- We built and froze the method at Mole Creek, so some choices began as judgement calls, and the tests checked them afterwards.
:::
