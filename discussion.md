# Discussion

### What the index shows

KIVI separates karst by how karstified and exposed it is and how much water drains into it. At Mole Creek this puts most of the karst in the High class, with the highest values where exposed, strongly karstified rock sits low in a large catchment. Statewide, most karst falls in the lower risk classes, and the top-ranked systems are mostly small (Flowery Gully, Doctors Rocks, Savage River Mine), with Gunns Plains the largest system in the top five. Mole Creek ranks 33rd on mean risk, so the test area is not the highest-risk karst in the state. It is a good test area because of its feature density, land-use variety and accessibility, but it is not a typical high-risk case. Because Mole Creek is mostly Atlas category A and B karst, how the index behaves in weakly karstified systems (such as Meander – Western Creek, category D) has been tested less.

### Which scale to use

We built the method at 25 m and applied it statewide at 100 m.

- **Finer routing changes little.** Routing on a 2 m DEM gave almost the same ranking as 25 m, because the connectivity classes are wide enough that most polygons keep their class.
- **The 100 m grid loses small systems.** Small polygons are covered by few cells, and some were too small to receive a score, so the statewide map under-represents small karst systems. They also dominate the top of an unfiltered ranking.
- **Resolution affects connectivity most.** It is the only ingredient that depends on the DEM.
- **Part of the Mole Creek difference comes from the routing area.** The 25 m DEM stops at the 3 km buffer and the 100 m DEM covers all of Tasmania, so the 100 m routing counts upstream land beyond the buffer and some polygons move up a connectivity class. This is part of why the statewide map shows more of Mole Creek in the higher KIVI classes than the 25 m map.

The 100 m map suits screening the state, and finer data is worth using where a decision depends on one site. This is the trade-off between local detail and statewide coverage described in the literature (Moreno-Gómez et al., 2019; Iván & Mádl-Szőnyi, 2017).

### Which method to choose

We kept the product. A place has to be high on every ingredient to score high, which suits a question about where pressure meets vulnerable karst. EPIK and COP also multiply their factors (Doerfliger et al., 1999; Vías et al., 2006), and methods applied to the same karst give different maps (Ravbar & Goldscheider, 2009), so the structure is a choice that matters.

- **A sum needs more decisions.** Added scores sit at a different level from the product, so they need their own class edges, and each input needs a weight that no data can set.
- **The springs check favours the product, and the weights decide a sum.** Springs sit much higher in the product's scores than in the six-input sum's, and random weight sets scatter widely around the equal-weight result.
- **The slope rule matters at Mole Creek and hardly at all statewide.** Published rules differ on the sign of slope (Vías et al., 2006). Most Mole Creek karst is gentle, so reversing the rule lifts nearly all of it at once.
- **The six-input comparison is limited by data.** The inputs such a method needs (soil cover, depth to groundwater, sinkhole density) have no statewide Tasmanian coverage (Moreno-Gómez et al., 2024), so proxies were substituted, and the difference partly reflects those weaker proxies.
- **Connectivity uses D8 routing over a filled DEM.** It is simple and works across all karst types, and catchment area is a reasonable stand-in for the water a polygon receives. Filling can hide real sinkholes, so a sink-retaining method might suit karst better and is untested here (O'Callaghan & Mark, 1984; Jenson & Domingue, 1988).
- **A product is easier to explain.** It has no weights to defend, and the effect of each ingredient is easy to describe to different users.

The springs check is weak, and a weighted sum with well-chosen inputs and weights could do as well. The choice rests on the evidence we have and on how easily the map can be explained.

### Which land-use data to use

We used LIST for the main map and DEA as the tested alternative. LIST is a Tasmanian product that separates plantations and irrigated pasture, which matter for pressure (Gillieson & Thurgate, 1999; Vilhar et al., 2022). DEA has the longer annual record (Geoscience Australia, n.d.).

- **The two agree at Mole Creek.** The karst there is mostly natural land and pasture, so both layers score it alike. They differ statewide, where plantations and irrigated pasture appear.
- **The layers differ in what they can see.** LIST distinguishes plantation forestry and irrigated pasture from other land uses, and DEA groups them within broader natural or cultivated classes. DEA's coarser three-level scheme also gives a higher mean risk at Mole Creek.
- **The score scale moves the level and leaves the pattern.** Pressure scores are judgement, and different schemes change how much risk there is while the ranking holds.
- **Land use changes the level of risk, and the ground sets the pattern.** KIVI and slope do not change between dates, and pressure is averaged over each named system, so most of the spatial pattern comes from the intrinsic layers. This shows that the pattern is driven by the ground and leaves the importance of land-use change open.
- **One year of land use shows where risk concentrates.** The amount of risk follows the land-use year, so the map should be updated as land use changes.
- **The change in level is the informative part.** The swing at Mole Creek is large enough that it should be checked against the DEA classification before it is read as real land-use change, and DEA cannot separate plantation forestry from native forest, which is the distinction that matters most for pressure (Ollivier et al., 2019).

DEA suits tracking change over time, and LIST suits a map of where pressure comes from. Running the model on each LIST snapshot is the next step, and it would show change over time with the better layer.

### Independent checks
- According to the metadata for the CFEV Groundwater Dependent Ecosystems (GDEs)layer, many of the springs mapped as point data are cave entrances making them a potential tool for checking the KIVI scores.

- Springs and subsurface streams from the dataset were used as an independent hydrological plausibility check on the KIVI model, checking karst areas only to see whether the GDE's were more concentrated in higher vulnerability karst. 

- The check found that at the 500m proximity threshold the 24 named karst systems with nearby GDE points had a mean KIVI score of 0.438, compared with an area-weighted karst baseline of 0.343 supporting the model’s capturing factors relevant to karst hydrology but it is a limited check. The springs are limited to a selection of known springs which may not be independent of the Karst Atlas data and only a small number of distinct systems is represented. The spatial information for each spring was generalised, but using the 500m proximity threshold would have helped even that out.

- There is a more comprehensive list of known GDE’s, GDE points.shp, done by Rolan Eberhard (2004) that would potentially provide a stronger check.

### Conservation priority matrix and map 
- The method produced a statewide conservation priority map at a 100m resolution that included vulnerability as well as a priority matrix combining showing the combinations that informed our final classes. The analysis identified 4,094km2 where the CFEV and intrinsic vulnerability overlapped with only 6.3km2 unmatched. The largest provisional priority class was Priority 3 — Moderate, covering 47.30% of eligible area. Priority 1 — Highest covered 12.79%, and Priority 1 and 2 together accounted for 32.12%. The priority classes are provisional, with the vulnerability bands and priority rules being agreed values/rules.  

- Higher vulnerability scores were more often spatially associated with very high conservation values in this dataset at 48% in the higher vulnerability band compared with 19.1% across the lower and moderate band. This may show some lack of independence between the two measures – the distinctiveness and representativeness parameters forming part of the ICV may overlap with Kcategory and Exposure in the Karst Atlas which form a major part of the KIVI. This could be tested by just using the naturalness score from the ICV to check whether the same skew occurs.  

- Due to the provisional nature of the scores, the priority map is most useful as a way of identifying where high vulnerability and high conservation value coincide, notably Mole Creek, Junee-Florentine and Mt Anne-Upper Weld. 

## Limitations

- KIVI is focused on groundwater vulnerability and does not include physical damage such as subsidence or damage to karst features other than through groundwater contamination. Land use risk can address this to a point by scoring categories like mining and production forest high.

### Input data quality and currency
- The Karst Atlas V3.1 data is from 2003 and its accompanying metadata says it has significant discrepancies in its polygon boundaries, while some more recently discovered karst areas are not included. The original Atlas was mapped at 1:100,000 and not all the polygons have been upgraded to 1:25,000.  

- Resampling to 100m loses detail from the finer resolution layers so local variation is smoothed and parameter scores may change, particularly for small polygons. 132 small polygons could not receive a D8 connectivity score.  

### Method and structure of index
- Parameters chosen to contribute to the KIVI were chosen by judgement based on which available datasets seemed to fit with the literature best. Weights and score bands were also set by judgement, including land use data from the LIST used for the risk map. The ranking depends on these choices and would need substantial testing and validation before being relied on.  
- Connectivity only captures upstream contributing area– it doesn’t represent underground drainage or sinkhole drainage, and one method would not be suitable in all karst areas.  

### Validation and independence
There was no testing against contamination or damage records so no validation of the index.

### Scope and transferability
The KIVI is specific for Tasmania as many of its inputs are state specific such as the Karst Atlas and the LIST inputs.
The statewide index, risk map and conservation priority maps are potentially useful screening tools to look at before investigating an area in depth but should not be relied on for small scale accuracy.

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
