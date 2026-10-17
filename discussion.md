# Discussion

% Rough points to cover. Order and headings to be decided when drafting.

- Method choice moved the map most. Multiplying needs every ingredient to be high, adding lets one ingredient carry a cell, and the six-input sum differed mainly because of its extra inputs.
- Scale and data moved it less. Connectivity is the only ingredient tied to DEM resolution and it is classed in powers of ten, so most polygons keep their class from 2 m to 100 m. The 100 m run scores Mole Creek higher partly because its routing sees land beyond the 3 km buffer.
- DEA and LIST agree at Mole Creek (mostly natural land and pasture) and split statewide where plantations and irrigated pasture appear.
- Mole Creek reacts more than the state to each choice, because it is small and one or two systems set the order.
- Land use changes how much risk there is, and the ground sets where it sits. Averaging pressure over each named system was the biggest single change at Mole Creek, and routing pressure along flow paths would improve it.
- Higher-KIVI karst is more often Very High conservation value, so the two layers point at many of the same places. The priority classes use provisional bands.
- Springs sit at about the 99th percentile of KIVI. The check is thin: 12 to 28 systems, discharge points, and spring mapping that probably shares sources with the Atlas.
- No contamination data, so no way to say which structure or map is right.
- EPIK and COP also disagree with each other (Ravbar and Goldscheider, 2009). Our index is simpler because Tasmania has no statewide soil cover, depth to groundwater or sinkhole density. Leads into the British Columbia paragraph below.
- The map suits screening the state and choosing where finer data is worth collecting. Different users want different maps.
- The shared functions, fixed classes and one rank-correlation measure made each test quick to run.


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


---

Moved from intro
 ## Not just about water
Most of the karst vulnerability index methods in the literature concentrate on groundwater and not physical karst but the Canadian province of British Columbia has developed a comprehensive set of standards and procedures for assessing karst vulnerability which includes geomorphology, hydrology and also ecosystems (The Province of British Columbia, 2003) and is a potential reference for developing a more comprehensive karst assessment approach in Tasmania. https://www2.gov.bc.ca/assets/gov/environment/natural-resource-stewardship/nr-laws-policy/risc/karst_risc.pdf