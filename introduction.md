---
title: Introduction
---

# The ground that swallows rain

**If a contaminant spilled on Tasmanian karst today, which areas would be most vulnerable and how could we tell?**

```{figure} figures/Croesus.jpg
:alt: Inside a limestone cave at Mole Creek, Tasmania.
:width: 100%

Rachel inside a cave at Mole Creek.
```

## Rock that rain dissolves

Most landscapes filter water as it moves through soil and rock. Karst can do the opposite. Rain dissolves limestone, gradually opening cracks into sinkholes, caves and underground streams.

Water entering through a sinkhole can bypass much of the filtration and attenuation that occurs in soil and porous material before reaching a cave, spring or aquifer. At Mole Creek, surface run-off is captured quickly by openings in the rock and passes through conduits with little cleaning (Eberhard & Houshold, 2002). Whatever the water picks up on the way goes with it.

```{figure} figures/intro_cross_section.svg
:alt: Cross-section of karst. Rain falls on forest and a cleared paddock, runs into a sinkhole, travels through a cave passage below the water table and emerges at a spring. Three numbered labels mark the rock, how directly water gets in, and what is on the land.
:width: 100%

Water enters at a sinkhole and leaves at a spring. Anything it picks up on the way (red dots) travels with it. The three numbers are the three questions our index asks of every map cell. *Diagram drawn by Claude (Anthropic, generative AI) from the authors' description and checked by the authors.*
```

## Small, scattered, easy to overlook

Mapped karst covers 6% of Tasmania, about 4,100 km², in patches from the north-west to the south. It is a small share of the land, but it carries the springs and wet ecosystems that depend on it.

We start at Mole Creek in the north: well studied, full of caves, and actively farmed. What is on the land above matters here.

```{figure} figures/tasmania_karst_locator.png
:alt: Map of Tasmania showing scattered mapped karst and the Mole Creek study area highlighted.
:width: 420px
:align: center

Mapped karst is scattered across just 6% of Tasmania. Mole Creek, an actively farmed karst area in the north, is this project's study site.
```

## Why nobody agrees on the answer

**Method:** A systematic review of karst vulnerability methods highlights scale and parameter transferability as key dimensions separating them (Iván & Mádl-Szőnyi, 2017). Tested against real tracer data, EPIK and COP disagree, and EPIK tends to overestimate vulnerability (Ravbar & Goldscheider, 2009).

**Scale:** Parameters tuned at one karst system do not automatically transfer to another (Moreno-Gómez et al., 2019). Fine hydrological detail, such as 2 m flow-routing, only works at a small site, which forces a trade-off with statewide coverage.

**Data:** Data scarcity is itself a core limitation of karst vulnerability mapping (Ollivier et al., 2019). Free statewide land cover (DEA) cannot tell a pine plantation from native forest. Tasmania's own LIST layer can, but it is a heavier, Tasmania-only dataset.

So the useful question is not "which index is right?" but **which choices change the answer, and by how much?**

## What we set out to do

**Build a karst vulnerability index that can scale from one cave system to the whole state, then test how different inputs and combination methods change the result.**

```{figure} figures/intro_aims_path.svg
:alt: A winding stream passes four stops: build at Mole Creek, freeze and scale to Tasmania, swap the land-use data between DEA and LIST, then test and report.
:width: 100%

The project in four steps. *Diagram drawn by Claude (Anthropic, generative AI) from the authors' description and checked by the authors.*
```
