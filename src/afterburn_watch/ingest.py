"""Sentinel-2 scene discovery via the AWS Earth Search STAC API.

FALLBACK / RESEARCH PATH -- not the primary one. Per Keith Weber's Sept 11
call recommendation (docs/technical-spec.md section 8, PROGRESS.md), our
primary data source is a pre-built NASA RECOVER package (see recover.py),
which already contains dNBR. This module stays useful for a fire RECOVER
doesn't cover yet, or to validate RECOVER's own dNBR against a fresh
Sentinel-2 computation -- but it is not time-critical anymore.

This is a starting point, not a finished pipeline -- the open research
questions from docs/technical-spec.md still need to be resolved here:

  * L1C (top-of-atmosphere) vs. L2A (surface reflectance) -- which product
    gives more stable dNBR results for our fire perimeters?
  * Cloud/smoke masking using the Scene Classification Layer (SCL) band
    that ships with L2A.

Earth Search (Element84) is a public, no-auth-required STAC catalog over
the Sentinel-2 Cloud-Optimized GeoTIFFs on AWS Open Data.
"""

from __future__ import annotations

from datetime import date
from typing import Iterable

from pystac_client import Client

EARTH_SEARCH_URL = "https://earth-search.aws.element84.com/v1"

# TODO (research): confirm sentinel-2-l2a vs sentinel-2-l1c per the
# trade-off above before this becomes the default.
DEFAULT_COLLECTION = "sentinel-2-l2a"


def find_scenes(
    bbox: Iterable[float],
    start: date,
    end: date,
    max_cloud_cover: float = 20.0,
    collection: str = DEFAULT_COLLECTION,
    limit: int = 20,
):
    """Query Earth Search for Sentinel-2 scenes over a bounding box and date range.

    Parameters
    ----------
    bbox : (min_lon, min_lat, max_lon, max_lat)
        Bounding box of the fire perimeter (e.g. the 2024 Wapiti Fire).
    start, end : date
        Date range to search (e.g. a pre-fire window or a post-fire window).
    max_cloud_cover : float
        Maximum scene-level cloud cover percentage to accept.
    collection : str
        STAC collection id ("sentinel-2-l2a" or "sentinel-2-l1c").
    limit : int
        Max number of items to return.

    Returns
    -------
    list[pystac.Item]
        Matching scenes, most recent first.
    """
    catalog = Client.open(EARTH_SEARCH_URL)
    search = catalog.search(
        collections=[collection],
        bbox=list(bbox),
        datetime=f"{start.isoformat()}/{end.isoformat()}",
        query={"eo:cloud_cover": {"lt": max_cloud_cover}},
        limit=limit,
    )
    return list(search.items())
