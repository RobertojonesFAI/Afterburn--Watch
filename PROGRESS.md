# Progress Log

Purpose: track builder/research steps for Afterburn Watch. Migrated here
from the team's shared `Afterburn_Watch_Progress.xlsx` (Sept 2026) now that
we have a repo -- keep updating this file with PRs instead of the
spreadsheet going forward.

## Environment & tooling

- [x] Environment setup
- [x] Ran `pfdf`'s local test suite -- 8 local tests failed.
  - Failures appear related to NumPy type issues in dependencies, not to
    `pfdf` logic itself. Considered safe to ignore (we're not testing
    third-party libraries).
  - Reference: [pfdf work items](https://code.usgs.gov/ghsc/lhp/pfdf/-/work_items),
    [Jonathan King, USGS](https://www.usgs.gov/staff-profiles/jonathan-m-king#publications)
    (lead author of `pfdf`).

## `pfdf` tutorial walkthrough (official Jupyter tutorials, `pfdf-main/tutorials/`)

- [x] 01 -- Start Here
- [x] 02 -- Raster Intro (2D raster library)
- [x] 03 -- Download Data (data sources)
- [x] 04 -- Preprocessing (bounding box, min/max dataset)
- [ ] 05 -- Hazard Assessment (end-to-end flow -- **next up**)
- [ ] 06 -- Raster Properties
- [ ] 07 -- Raster Factories
- [ ] 08 -- Spatial Metadata
- [ ] 09 -- RasterMetadata Class
- [ ] 10 -- Parallel Basins
- [ ] 11 -- Parameter Sweep

## Repo scaffolding (this commit)

- [x] `pyproject.toml` with `pfdf` + pipeline dependencies
- [x] `src/afterburn_watch/severity.py` -- NBR / dNBR / BAER classification (unit tested)
- [x] `src/afterburn_watch/ingest.py` -- Earth Search STAC query stub
- [x] `src/afterburn_watch/app.py` -- Streamlit entry point (scaffold only)
- [x] `docs/technical-spec.md` -- condensed technical spec for reference

## Notes / open ideas

- For local 3D visualization, may need Blender (via
  [BlenderGIS](https://github.com/domlysz/BlenderGIS/)) to import raster
  outputs. Overlay rendering would lean on image masking and OpenStreetMap
  basemaps.

## Not started yet

- [ ] Real Sentinel-2 ingestion run against the 2024 Wapiti Fire
- [ ] L1C vs. L2A decision + SCL cloud/smoke masking implementation
- [ ] BAER vs. regional-ecoregion threshold comparison
- [ ] Wiring `severity.py` output into `pfdf`'s hazard-assessment functions
- [ ] Folium map overlay in `app.py`
