# Afterburn Watch -- Technical Spec (condensed)

Source: adapted from `Team_Afterburn_Watch_burn_severity_monitoring_prototype_overview-v3.docx`
(kept here as the living reference now that we're on GitHub).

## 1. Mission

Post-wildfire debris flows are an acute hydro-geomorphic threat across the
Western United States, capable of causing catastrophic damage to critical
infrastructure, water resources, and residential communities within minutes
of intense rainfall.

Afterburn Watch builds an automated, open-source Python workflow that
ingests public Sentinel-2 satellite imagery (AWS Open Data), computes
differenced Normalized Burn Ratio (dNBR) rasters, classifies soil/vegetation
burn severity, and prepares data handoffs for the downstream USGS
post-fire debris-flow likelihood and rainfall-threshold models (`pfdf`).
An interactive decision-support map lets emergency managers evaluate
post-fire risk in **hours rather than weeks**.

## 2. Hackathon Context

- **Event:** R-CON 2026 Innovation Village, Boise Centre, Boise, Idaho.
- **Live Showcase:** October 13, 2026.
- **Challenge:** Challenge 01 (Wildfire Resilience), Problem Statement 2 --
  equipping emergency managers, utilities, and recovery teams with rapid,
  accurate post-fire intelligence.
- **Benchmark fire:** 2024 Wapiti Fire, central Idaho (Custer/Boise
  counties), extensible to a multi-fire dropdown of historical USGS PFDF
  assessment perimeters.
- **Deliverable:** Interactive web map (Streamlit/Folium) overlaying
  Sentinel-2 dNBR burn-severity rasters, catchment boundaries, and
  predicted rainfall-intensity thresholds.

## 3. Team & Roles

| Member | Role | Focus |
|---|---|---|
| Roberto Jones | Researcher + Builder | L1C vs. L2A, cloud/smoke masking (SCL), BAER vs. regional thresholds, `pfdf` integration, and shares pipeline-building work equally with Troy. |
| Troy Jenks | Builder | Core Python pipeline, STAC queries, dNBR computation, interactive map. |
| Ashraf Md | Strategist | Business feasibility, stakeholder fit (BLM, USACE, NWS). |
| Storyteller / PM (shared) | -- | Whitepaper and pitch deck. |

## 4. Pipeline Architecture

1. **Automated data ingestion** -- query the AWS Sentinel-2 STAC API (Earth
   Search / Element84) for pre-fire and post-fire imagery over the fire's
   bounding box (default: 2024 Wapiti Fire). See `src/afterburn_watch/ingest.py`.
2. **Data product / cloud-masking trade-off** -- decide between Level-1C
   (top-of-atmosphere) and Level-2A (surface reflectance), and use the
   Scene Classification Layer (SCL) band to remove cloud/shadow/smoke.
   **Open research question -- owned by Roberto.**
3. **Spectral processing** -- compute NBR per scene, then dNBR between the
   pre- and post-fire pair. See `src/afterburn_watch/severity.py`.
4. **Burn-severity classification** -- start from standard BAER breaks
   (Unburned/Low <100, Low 100-270, Moderate 270-660, High >=660), while
   evaluating regional ecoregion thresholds (e.g. EPA Level 2 Western
   Cordillera) for shrub vs. tree-dominated canopy differences.
5. **Raster export** -- export cloud-masked, reclassified dNBR GeoTIFFs
   formatted as inputs for `pfdf`.
6. **Decision-support map** -- interactive Streamlit/Folium app with fire
   selection, dNBR overlay, and catchment-scale summaries. See
   `src/afterburn_watch/app.py`.

## 5. Domain / Scientific Rationale

- **USGS M1 / M\* likelihood model:** debris-flow likelihood `p` as a
  logistic function of terrain steepness (T), burn severity (F = dNBR/1000),
  and soil erodibility (S). The 2026 regional update (Graber et al., 2026)
  replaces raw rainfall with a 1-year 15-minute rainfall ratio (R\*) to
  account for regional hydroclimate variation across EPA Ecoregions.
- **`pfdf` integration:** our classified dNBR rasters populate the burn
  severity term (F) and the moderate/high-severity terrain proportion (T)
  that `pfdf` (King, 2023 -- USGS) expects.
- **Multi-year recovery context:** annually updated dNBR captures multi-year
  vegetation recovery, reducing false-positive warnings (Graber et al.,
  2026, Geosphere).

## 6. Formula Reference

| Parameter | Formula / Thresholds | Notes |
|---|---|---|
| NBR | `NBR = (B08 - B12) / (B08 + B12)` | Sentinel-2 NIR (Band 8, 842 nm) and SWIR-2 (Band 12, 2190 nm). |
| dNBR | `dNBR = (NBR_pre - NBR_post) * 1000` | Higher positive values = more canopy loss / soil burn. |
| BAER breaks | Unburned/Low <100, Low 100-270, Moderate 270-660, High >=660 | Standard 4-class BAER scheme. |
| USGS M1/M\* link function | `x = β + C1*(T)*R* + C2*(F)*R*`, `p = e^x / (1 + e^x)` | T = steep-terrain proportion (>=23°); F = dNBR/1000; R\* = 1-yr 15-min rainfall ratio. |

## 7. Roadmap (Sept 7 -- Oct 13, 2026)

| Sprint | Builder (Troy / Roberto) | Strategist (Ashraf) | Research (Roberto) | Storyteller / PM |
|---|---|---|---|---|
| Sept 7 (Sprint 1) | Assess SentinelHub & AWS STAC APIs; outline script architecture. | Define target market & user personas (BLM/USACE). | Review USGS M1/M\* papers; establish dNBR formula specs. | Define prototype vision; start whitepaper draft. |
| Sept 14 (Sprint 2) | Ingest Wapiti Fire Sentinel-2 scenes; script dNBR calculation. | Draft cost-benefit / operational-efficiency section. | Evaluate L1C vs. L2A & SCL cloud masking; compile BAER break tables. | Finalize whitepaper submission; outline pitch deck. |
| Sept 21 (Sprint 3) | Build Streamlit/Folium map; overlay dNBR GeoTIFFs. | Marketing collateral & agency deployment strategy. | Validate Wapiti dNBR outputs against USGS assessment perimeters. | Integrate whitepaper into presentation draft; demo. |
| Sept 28 (Sprint 4) | Package prototype; multi-fire dropdown selector. | Finalize market-viability slides. | Review model assumptions & counterpoints. | Package full deck; internal review. |
| Oct 5-13 (Final) | Bug fixes; lock demo environment. | Polish pitch delivery & Q&A prep. | Finalize technical summary tables. | Live dry runs; present Oct 13. |

## Data source strategy (decided Sept 11 kickoff)

We are **not** generating a new DNBR product from scratch as our primary
path -- with a two-week build window, that competes directly with building
the actual pipeline. Instead we lean on already-authoritative sources
(NASA RECOVER data packages: dNBR, fire perimeters, roads, soils) and put
our engineering time into ingestion, `pfdf` coupling, and the
decision-support map -- the part that actually turns "weeks" into "hours."
Sentinel-2's ~5-day revisit (vs. Landsat's 16-day revisit, which RECOVER's
own dNBR protocol is built on) is our potential edge if we do need to
compute dNBR ourselves for a very recent fire not yet covered by an
authoritative product.
