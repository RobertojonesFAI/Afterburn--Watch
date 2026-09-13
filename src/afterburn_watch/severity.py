"""Burn-severity computation: NBR, differenced NBR (dNBR), and BAER classification.

These are the core spectral formulas from the project's technical spec
(see docs/technical-spec.md). They are intentionally dependency-light
(pure NumPy) so they can be unit tested without a full raster stack.

References
----------
- BAER breaks: standard Burned Area Emergency Response 4-class scheme.
- Regional/ecoregion break alternatives (e.g. EPA Level 2 Western Cordillera)
  are an open research question -- see docs/technical-spec.md, section 4.
"""

from __future__ import annotations

import numpy as np

# Standard BAER burn-severity breaks (on dNBR * 1000 scale)
BAER_BREAKS = {
    "unburned_low": (-np.inf, 100),
    "low": (100, 270),
    "moderate": (270, 660),
    "high": (660, np.inf),
}


def compute_nbr(nir: np.ndarray, swir2: np.ndarray) -> np.ndarray:
    """Compute the Normalized Burn Ratio (NBR).

    NBR = (NIR - SWIR2) / (NIR + SWIR2)

    For Sentinel-2, NIR is Band 8 (842 nm) and SWIR2 is Band 12 (2190 nm).

    Parameters
    ----------
    nir, swir2 : np.ndarray
        Reflectance arrays for the NIR and SWIR2 bands (same shape).

    Returns
    -------
    np.ndarray
        NBR values in [-1, 1].
    """
    nir = nir.astype("float32")
    swir2 = swir2.astype("float32")
    denom = nir + swir2
    with np.errstate(divide="ignore", invalid="ignore"):
        nbr = np.where(denom != 0, (nir - swir2) / denom, np.nan)
    return nbr


def compute_dnbr(nbr_pre: np.ndarray, nbr_post: np.ndarray) -> np.ndarray:
    """Compute the differenced NBR (dNBR) between pre- and post-fire scenes.

    dNBR = (NBR_pre - NBR_post) * 1000

    Higher positive values indicate greater vegetation/soil disturbance.
    """
    return (nbr_pre - nbr_post) * 1000.0


def classify_baer(dnbr: np.ndarray) -> np.ndarray:
    """Classify a dNBR raster into standard BAER severity classes.

    Returns an integer array: 0=unburned/low, 1=low, 2=moderate, 3=high.
    NaN inputs are preserved as -1 (no data).
    """
    out = np.full(dnbr.shape, -1, dtype="int8")
    valid = ~np.isnan(dnbr)
    out[valid & (dnbr < 100)] = 0
    out[valid & (dnbr >= 100) & (dnbr < 270)] = 1
    out[valid & (dnbr >= 270) & (dnbr < 660)] = 2
    out[valid & (dnbr >= 660)] = 3
    return out
