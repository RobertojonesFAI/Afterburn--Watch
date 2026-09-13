# Afterburn Watch

**Afterburn Watch empowers emergency managers to evaluate post-fire risks within hours rather than weeks.**

Built for the R-CON 2026 Innovation Village hackathon (Boise, Idaho) --
Challenge 01: Wildfire Resilience, Problem Statement 2 (rapid post-fire intelligence
for emergency managers, utilities, and recovery teams). Live Showcase: **October 13, 2026**.

## The problem

Post-wildfire debris flows can devastate infrastructure, water resources, and
communities within minutes of an intense rainstorm on a burned watershed.
Existing USGS post-fire hazard assessments are scientifically solid, but
producing one for a new fire is slow -- delays that cost fire managers and
the National Weather Service the response time they need.

## What this does

Afterburn Watch is an automated Python pipeline that:

1. Pulls Sentinel-2 imagery from AWS Open Data (no auth required) for a
   given fire perimeter.
2. Computes the differenced Normalized Burn Ratio (dNBR) and classifies
   burn severity (BAER breaks, with regional thresholds under evaluation).
3. Formats the result as input for [`pfdf`](https://code.usgs.gov/ghsc/lhp/pfdf),
   USGS's official post-fire debris-flow hazard-assessment library
   (Cannon et al. 2010, Gartner et al. 2014, Staley et al. 2017 models).
4. Renders an interactive map (Streamlit + Folium) so a fire manager can
   see burn severity, catchment boundaries, and hazard estimates without
   waiting on a manual, weeks-long turnaround.

Benchmark case: the **2024 Wapiti Fire** (central Idaho).

See [`docs/technical-spec.md`](docs/technical-spec.md) for the full
architecture, formulas, and roadmap, and [`PROGRESS.md`](PROGRESS.md) for
where things currently stand.

## Repo structure

```
src/afterburn_watch/
  severity.py   # NBR / dNBR / BAER classification (unit tested)
  ingest.py     # Sentinel-2 scene discovery via the Earth Search STAC API
  app.py        # Streamlit decision-support map (entry point)
docs/
  technical-spec.md
tests/
  test_severity.py
notebooks/      # exploratory / tutorial notebooks
data/           # local data (gitignored -- raw/interim/processed)
```

## Getting started

```bash
python -m venv .venv && source .venv/bin/activate

# pfdf is NOT on PyPI -- it's published on USGS's own GitLab package
# registry, so you need the extra index below or the install will fail
# with "No matching distribution found for pfdf".
pip install -e ".[dev,tutorials]" \
  --extra-index-url https://code.usgs.gov/api/v4/groups/859/-/packages/pypi/simple

# run tests
pytest

# run the app scaffold
streamlit run src/afterburn_watch/app.py
```

`pfdf` requires Python >=3.11. If the install above still fails, see
`pfdf`'s own [fallback instructions](https://ghsc.code-pages.usgs.gov/lhp/pfdf/resources/installation)
(clone + `poetry install`) -- and note this to the team, since it likely
means something else about the environment needs attention too.

## Team (Afterburn Watch)

| Name | Role |
|---|---|
| Roberto Jones | Researcher & Builder |
| Troy Jenks | Builder |
| Ashraf Md | Strategist |

Advisors: Keith Weber (GIS TReC, Idaho State University), Ashley Bosa
(Resilience Institute, Boise State University).

## Key references

- Cannon, S.H. et al., 2010. *Predicting the probability and volume of
  postwildfire debris flows in the intermountain western United States.*
  GSA Bulletin, 122(1-2), 127-144.
- Gartner, J.E. et al., 2014. *Empirical models for predicting volumes of
  sediment deposited by debris flows...* Engineering Geology, 176, 45-56.
- Staley, D.M. et al., 2017. *Prediction of spatially explicit rainfall
  intensity-duration thresholds for post-fire debris-flow generation...*
  Geomorphology, 278, 149-162.
- Graber, A. et al., 2026. *Regional Models for Postfire Debris-Flow
  Likelihood and Rainfall Thresholds.* Earth Surface Processes and
  Landforms.

## Acknowledgments

- [`pfdf`](https://code.usgs.gov/ghsc/lhp/pfdf) -- USGS post-fire
  debris-flow hazard assessment library (King, J. et al.), licensed under
  GPL-3.0. This project depends on it but does not redistribute its source.
- [NASA RECOVER](https://giscenter.isu.edu/research/Techpg/nasa_RECOVER2/index.htm) --
  post-fire decision-support data packages (dNBR, fire perimeters, roads,
  soils), maintained by the ISU GIS Center.

## License

TBD -- to be decided before any public release. Note that `pfdf` (a core
dependency) is GPL-3.0; confirm license compatibility before distributing
this project publicly.
