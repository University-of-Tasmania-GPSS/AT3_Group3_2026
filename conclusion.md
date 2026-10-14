jup# Conclusion

:::{div}
:class: tagline
Same karst, different users, different questions.
:::

```{figure} figures/connectivity_landuse_2x2_mole_creek.png
:alt: Four maps of the Mole Creek karst. The main map, a 100 m grid, DEA land cover and a six-input weighted sum, each split into fifths of its own cells. The 100 m grid is blockier, DEA is almost identical to the main map, and the weighted sum looks like a different map.
:width: 90%
:align: center

The main map and one change on each axis. Titles give the rank correlation with the main map (1 = same ordering).
```

:::{dropdown} What we found

- **Top three areas.** The highest relative risk in Tasmania is at Flowery Gully (0.17), Doctors Rocks (0.16) and Savage River Mine (0.15), among systems of at least 20 cells.
- **Method moves the map most.** Adding the four ingredients keeps the Mole Creek order (0.98) but not the state's (0.70), and a six-input literature-style index gives a very different Mole Creek map (0.55). Slope direction changes Mole Creek (0.83) but barely the state (0.96).
- **Scale and data matter less.** A 2 m elevation model gives the same map as 25 m (0.99), and the 100 m grid changes it a little more (0.89). Tasmanian land use against national land cover barely moves Mole Creek (0.98) and moves the state more (0.84).
- **Exposure.** Scoring how exposed the karst is changes the map a little (0.91 at Mole Creek, 0.96 statewide), and it strengthens the springs check (springs sit at about the 99th percentile of the karst score, up from the 96th).

:::

:::{dropdown} Limitations

**Ground truth**
- Nothing measures contamination, so there is no way to say which map is right. The only check is where springs are, and springs mark where water leaves the karst.
- The springs check rests on 12 to 28 systems. The spring locations were probably mapped using the same karst knowledge that feeds our scores, and well-studied karst is more likely to have mapped springs.
- Checking that the most karstified systems rank highest is partly circular, because susceptibility comes from the same Atlas category used to name and rank them.

**Data**
- The national land-cover product cannot see plantations or irrigated pasture. The Tasmanian land-use layer can, but it is a single year (2021), so we cannot track change in land use.
- We ran the 2 m elevation model only at Mole Creek, as a check. It matched the 25 m map, so finer data did not look worth pursuing.
- The 100 m statewide run smooths slope and misses small systems. 132 karst areas were too small for a single cell and keep their Atlas connectivity score.
- Karst susceptibility is only four Atlas categories, and the files we had do not define categories B and C.
- Rainfall from the Atlas is one value per polygon and barely varies at Mole Creek, so we left it out.

**Method**
- Land-use scores, slope direction and class edges are judgement. Published methods disagree on the sign of slope, and our map follows one choice.
- Connectivity is routed over the surface DEM. It cannot see underground drainage or sinkholes.
- Pressure is averaged over each named system, so every cell in a system gets the same value and the map is patchy by system. This was the choice that changed the Mole Creek map most.
- Scores are relative, not absolute, and the risk classes were re-set from 0.05 to 0.03 steps when the land-use layer changed. The colours show rank within Tasmania's karst, not a chance of contamination.
- Very small systems dominate an unfiltered ranking, so we only rank systems of at least 20 cells.
- We built and froze the method at Mole Creek, so some choices began as judgement calls, and the tests checked them afterwards.
:::
