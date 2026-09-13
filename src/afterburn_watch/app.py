"""Streamlit decision-support map -- entry point (placeholder).

Run with:  streamlit run src/afterburn_watch/app.py

Target UX (from docs/technical-spec.md, section 4.6):
  * Fire perimeter selector, defaulting to the 2024 Wapiti Fire, extensible
    to a dropdown of historical USGS PFDF assessment perimeters.
  * dNBR / burn-severity raster overlay.
  * Catchment-scale vulnerability summary panel.
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
    "Sentinel-2 ingestion (see ingest.py), dNBR computation and BAER "
    "classification (see severity.py), and a Folium map overlay."
)

# TODO: fire perimeter selector (st.selectbox), default to Wapiti 2024
# TODO: run ingest.find_scenes() for pre/post windows around the selected fire
# TODO: compute dNBR via severity.compute_nbr / compute_dnbr / classify_baer
# TODO: render the classified raster + catchment summary on a Folium map
