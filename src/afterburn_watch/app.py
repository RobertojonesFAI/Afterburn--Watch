"""Streamlit decision-support map -- entry point (placeholder).

Run with:  streamlit run src/afterburn_watch/app.py

Target UX (from docs/technical-spec.md, section 4):
  * Fire perimeter selector, defaulting to the 2024 Wapiti Fire, extensible
    to a dropdown of historical USGS PFDF assessment perimeters.
  * dNBR / burn-severity raster overlay.
  * Catchment-scale vulnerability summary panel.

Per Keith Weber's Sept 11 call recommendation (docs/technical-spec.md
section 8, PROGRESS.md), the primary data path is a pre-built NASA RECOVER
package (recover.py), not our own Sentinel-2 ingestion (ingest.py /
severity.py, kept as a fallback/research track).
"""

from __future__ import annotations

import streamlit as st

st.set_page_config(page_title="Afterburn Watch", layout="wide")

st.title("Afterburn Watch")
st.caption(
    "Post-fire burn-severity decision support -- evaluate debris-flow risk "
    "in hours, not weeks."
)

st.info(
    "This is a scaffold. Next up: fire selector (default: 2024 Wapiti Fire), "
    "loading a NASA RECOVER data package (see recover.py) for its dNBR / "
    "fire perimeter, feeding that into pfdf's likelihood and volume models, "
    "and a Folium map overlay. (Our own Sentinel-2 ingestion in ingest.py / "
    "severity.py is now a fallback/research path -- see docs/technical-spec.md "
    "section 8.)"
)

# TODO: fire perimeter selector (st.selectbox), default to Wapiti 2024
# TODO: load the RECOVER package via recover.load_recover_package() /
#       find_dnbr_raster() for the selected fire (primary path)
# TODO: wire the RECOVER dNBR / perimeter into pfdf's likelihood (Staley/M1)
#       and volume (Gartner) hazard-assessment functions
# TODO: render the classified raster + catchment summary on a Folium map
# TODO (fallback/research, lower priority): ingest.find_scenes() +
#       severity.compute_nbr/compute_dnbr/classify_baer for fires RECOVER
#       doesn't cover, or to cross-check RECOVER's own dNBR
