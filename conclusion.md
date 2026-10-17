# Conclusion

## What we found

We built a Karst Intrinsic Vulnerability Index (KIVI) at Mole Creek (25 m), applied it across Tasmania (100 m), and combined it with LIST land use, slope and CFEV conservation value, using the same code and fixed classes at both scales.

**A KIVI for Tasmania.** Susceptibility (Atlas category × exposure) times connectivity (D8 flow routing) runs at 25 m and 100 m with the same five classes. Across the state, 47% of karst cells are High and 9% Very high. Exposure is part of the score because it lifts the springs check from about the 96th to the 99th percentile.

**Scale.** A 2 m elevation model gives the same map as 25 m (0.99), and the 100 m grid changes it a little (0.89). The 100 m run scores Mole Creek higher, partly because its routing includes land beyond the 25 m buffer.

**Sensitivity.** Method choices move the map most. The six-input weighted sum gives a very different Mole Creek map (0.55), and adding the four ingredients changes the state's ordering (0.70). Tasmanian land use and national land cover give the same Mole Creek ranking (0.98) and differ more across the state (0.84), because the Tasmanian layer separates plantations and irrigated pasture.

**KIVI with land use.** Multiplying KIVI by LIST 2021 pressure and the slope multiplier gives the risk map. Risk is highest in the west of Mole Creek, and Flowery Gully, Doctors Rocks and Gunns Plains lead the statewide ranking of larger systems. Over the DEA series from 1988 to 2024 the level of risk follows land use and the pattern stays fixed.

**KIVI with conservation value.** Combining KIVI with CFEV Integrated Conservation Value gives a four-class priority map. The top class covers 13% of the karst, mostly in the south-west mountains and at Mole Creek (Results, section 7).

## What we would do next

- **Add ground truth.** Water-quality or dye-tracing records would let us test the map against measured contamination.
- **Route pressure along the flow paths.** Pressure is a mean over each named system. Routing land use along the flow paths into each karst polygon describes what reaches the karst more closely.
- **Run each LIST snapshot.** LIST has six snapshots (2002, 2009–10, 2013, 2015, 2019 and 2021), and running the model on each shows how risk moves with land use.
- **Keep the sinks.** Flow routing that retains sinks (Whitebox, RichDEM) may suit karst, where sinks can be real sinkholes.
- **Fill the missing inputs.** Soil cover, depth to groundwater and sinkhole density would allow a literature-style index for Tasmania.
- **Flag the small systems.** A confidence mark based on each system's cell count shows where the 100 m map is least reliable.
