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

What the index shows. KIVI separates karst by how karstified and exposed it is and how much water drains into it. At Mole Creek this puts most of the karst in the High class, with the highest values where exposed, strongly karstified rock sits low in a large catchment. Statewide, most karst falls in the lower risk classes, and the top-ranked systems are mostly small (Flowery Gully, Doctors Rocks, Savage River Mine), with Gunns Plains the largest system in the top five. Mole Creek ranks 33rd on mean risk, so the test area is not the highest-risk karst in the state. It is a good test area because of its feature density, land-use variety and accessibility, but it is not a typical high-risk case. Because Mole Creek is mostly Atlas category A and B karst, how the index behaves in weakly karstified systems (such as Meander – Western Creek, category D) has been tested less.
How much the choices matter. The sensitivity tests show that the main map is robust to some choices and sensitive to others. Routing water on a 2 m DEM gave almost the same ranking as 25 m (0.99), so the coarser grid is an acceptable substitute for this input at Mole Creek. The 100 m grid changed the map more (0.89), mainly because small polygons are covered by few cells, and 132 polygons were too small to receive any score. The statewide map therefore under-represents small karst systems, which also dominate the top of the unfiltered ranking. The largest effects came from method choices. Replacing the product with a six-input weighted sum gave a very different map (0.55), and reversing the slope rule changed the Mole Creek ranking (0.83) but hardly changed the statewide one (0.96). The six-input comparison is limited by data: the inputs such a method needs (soil cover, depth to groundwater, sinkhole density) have no statewide Tasmanian coverage, so proxies were substituted. The difference in outcome partly reflects those weaker proxies and not only the method.
Land-use change. Land-use change altered the level of risk and left its pattern almost fixed (correlation of at least 0.9998 between years). This is largely a consequence of the design. KIVI and slope do not change between dates, and land-use pressure is averaged over each named system, so most of the spatial pattern comes from the intrinsic layers. The result shows that the pattern is driven by the ground, but it does not show that land-use change is unimportant. The change in level is the more informative result, and the swing at Mole Creek from 65% to 22% and back to 64% high-pressure land is large enough that it should be checked against the DEA classification before it is read as real land-use change. The DEA series is also the only annual one, and it cannot separate plantation forestry from native forest, which is the distinction that matters most for pressure.
Independent checks. Springs fall in karst that scores at about the 99th percentile of random draws, and the result holds across distance thresholds. The check is weak for the reasons already noted: springs mark discharge, not contamination pathways, the test rests on 12 to 28 systems, and spring mapping may draw on the same karst knowledge that feeds the scores. Exposure was added partly because it improved this result (from about the 96th percentile), so the check is no longer fully independent of model development. No contamination record was available to test against, so KIVI should be read as a relative ranking of places for attention and not as a prediction of contamination.
Conservation value. Higher-KIVI cells are more often Very High ICV (48% against 6%). This agreement should not be read as two independent measures converging, because CFEV’s assessment drew on the Karst Atlas V3, and the Atlas category feeds KIVI. The priority map is most useful as a way of identifying where high vulnerability and high conservation value coincide (Mole Creek, Junee–Florentine, Mt Anne–Upper Weld). Its class boundaries are provisional, and it ranks places without measuring risk.
Limitations and further work. KIVI addresses groundwater contamination only, and does not capture physical karst damage such as subsidence or damage to cave features. Karst network development (K in EPIK) has no independent measure and is carried only implicitly through the Atlas category, and there is no precipitation term, which matters across Tasmania’s west–east rainfall gradient. Connectivity captures upstream contributing area but not swallow-hole proximity or catchment slope and vegetation. Scores are products of fractions, so they bunch near zero and are meaningful only in relative terms. The Atlas dates from 2003 and its boundaries and categories may have changed. Priorities for further work are ground-truthing at Mole Creek, a rainfall term, bore and cave records as additional checks, a land-use layer that separates plantation from native forest with an annual series, and testing in weakly karstified systems.
________________________________________
Check before submitting
•	Interpretive claims: the explanation for the land-use pattern (static KIVI plus system-averaged pressure) and the circularity points are my reading of your results. Confirm they match how you built the model.
•	Definition mismatch: the introduction defines vulnerability as covering “physical karst damage”, while the discussion says KIVI is contamination only. One of the two needs changing.
•	Length: if there’s a word limit, the limitations paragraph can be shortened to a list of one-line caveats.
