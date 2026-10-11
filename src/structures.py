"""Inputs and weighted sums for the structure comparison (Stage 14) and the choices chart (Stage 16).

The six-input weighted sum adds exposure, catchment flags, watercourse and rainfall to susceptibility
and slope. Every input is scaled 0-1 and is zero off the mapped karst.
"""
import numpy as np

from hydro import watercourse_raster
from karst import rasterize_max

NAMES = ["Susceptibility", "Exposure", "Catchment", "Watercourse", "Slope", "Rainfall"]
W_EQUAL = dict.fromkeys(NAMES, 1.0)
# A rough analogue of EPIK's 3:1:3:2 (epikarst ~ susceptibility, protective cover ~ exposure,
# infiltration ~ catchment, karst network ~ watercourse), with slope and rainfall at 1.
W_EXPERT = {"Susceptibility": 3, "Exposure": 1, "Catchment": 3, "Watercourse": 2, "Slope": 1, "Rainfall": 1}
SLOPE_REF_DEG = 15.0


def weighted_sum(X, w):
    return sum(w[k] * X[k] for k in NAMES) / sum(w.values())


def build_inputs(karst, shape, transform, wc, slope, rain_range):
    """The six 0-1 input rasters. `karst` needs add_karst_susceptibility and add_connectivity run."""
    k = karst.copy()
    k["catchment_score"] = np.maximum(k["proximal_score"], k["distal_score"])
    rmin, rmax = rain_range
    k["rain_norm"] = np.where(k["karst_intensity"] > 0, ((k["KAVRAIN"] - rmin) / (rmax - rmin)).clip(0, 1), 0.0)
    rz = lambda col, dt="uint8": rasterize_max(k, col, shape, transform, fill=0, dtype=dt).astype(float)
    return {
        "Susceptibility": rz("karst_intensity") / 4.0,
        "Exposure": rz("autogenic_score") / 3.0,
        "Catchment": rz("catchment_score") / 3.0,
        "Watercourse": watercourse_raster(wc, shape, transform).astype(float) / 3.0,
        "Slope": np.clip(np.nan_to_num(slope, nan=0.0) / SLOPE_REF_DEG, 0, 1),
        "Rainfall": rz("rain_norm", "float32"),
    }
