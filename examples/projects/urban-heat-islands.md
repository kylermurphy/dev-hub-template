---
id: HEAT
title: Urban heat islands from satellite land-surface temperature
status: active
started: 2026-09
horizon: 2027-06
repos: []
updated: 2026-09-29
---

# HEAT — Urban heat islands from satellite land-surface temperature

> **Example only.** A made-up project, a few weeks in. In a real hub it lives at
> `projects/urban-heat-islands.md`. It has no code repo yet, so `repos` is `[]` and every
> **Links** cell is `—`. Once code work starts, the repo is tracked and its task and feature IDs
> go in those cells.

## Summary

How much hotter are city centres than the land around them on summer days, and has that grown
over the last decade? Mapping it from satellite land-surface temperature (LST) for 20 cities
gives one consistent, comparable picture. Success is validated intensity maps, with
uncertainties, and a trend for each city.

## Background

A surface urban heat island is the gap between a city's surface temperature and that of a rural
ring around it. Satellite LST measures it everywhere at once, where weather stations only see a
few points [1]. Earlier maps mix sensors, seasons and rural rings, so cities can't be compared
fairly, and few give uncertainties or trends [2]. The data are public: daily LST at 1 km from
2015 on, and hourly air temperatures from station networks for validation. The analysis starts
in notebooks; there's no code repo yet.

## Science goals

- **G1** — Measure how strong summer surface heat islands are in large cities, and how much
  that varies between cities.
- **G2** — Find out whether they grew between 2015 and 2025.

## Objectives and work packages

### O1 — Map summer heat-island intensity for 20 cities, 2015–2025

**Serves:** G1 · **Success criteria:** intensity maps with uncertainty for all 20 cities, validated against station data

| WP | Status | Work package | Output | Links |
| --- | --- | --- | --- | --- |
| WP1.1 | 🟠 WIP | Download and cloud-mask the LST scenes | clean dataset | — |
| WP1.2 | ⏩ Todo | Build the intensity pipeline | maps + uncertainty | — |
| WP1.3 | ⏩ Todo | Validate against weather stations | validation figure | — |

### O2 — Estimate each city's 2015–2025 trend in intensity

**Serves:** G2 · **Success criteria:** a trend with a confidence interval for every city, stable under a stricter cloud mask

| WP | Status | Work package | Output | Links |
| --- | --- | --- | --- | --- |
| WP2.1 | ⏩ Todo | Choose a trend method and test it on three cities | method note | — |
| WP2.2 | ⏩ Todo | Trends for all 20 cities | trend table + draft paper section | — |

## Plans

### 2026-09-22 — Plan for WP1.1

**Goal:** a cloud-free stack of summer daytime LST for each of the 20 cities.

- [x] List the cities and a bounding box for each
- [ ] Download June–August daytime LST, 2015–2025
- [ ] Apply the quality flags; drop scenes that are more than half cloud
- [ ] Count the scenes left per city and month

**Data and methods:** daily 1 km LST; the product's own quality flags for the cloud mask.
**Risks:** some cities may have too few clear scenes; if so, use 8-day composites.
**Code work:** none yet. If the pipeline outgrows notebooks, track a repo and add tasks.

## Next actions

- [ ] Decide how wide the rural reference ring should be (added 2026-09-24)
- [ ] Find a station network with open hourly data for all 20 cities (added 2026-09-29)
- [ ] Track a code repo (`add-repo`) once the pipeline outgrows notebooks (added 2026-09-29)

## References

1. Example, A. (2019). *Measuring surface heat islands from space.* Example Journal of Remote
   Sensing (made up). [doi:10.0000/example.1](https://doi.org/10.0000/example.1) — the
   standard definition of intensity.
2. Sample, B. and Case, C. (2022). *Comparing heat islands across cities.* Example Letters (made
   up). [doi:10.0000/example.2](https://doi.org/10.0000/example.2) — shows how the choice of
   rural ring changes the answer.

## Decisions

| Date | Decision | Why |
| --- | --- | --- |
| 2026-09-24 | Use daily 1 km LST, not a finer sensor that revisits every 16 days | Summer means need many clear days more than they need resolution |

## Research log

- **2026-09-29** — The cloud mask removes about 40% of July scenes. That still leaves enough
  for monthly means in 18 of the 20 cities.
- **2026-09-22** — Project started; WP1.1 planned.
