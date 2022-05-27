import numpy as np
from colour.models.rgb import RGB_Colourspace

# ELLE GİRİLEN DENEME DEĞERLER ################################################
#
PRIMARIES_SAMPLE = np.array(
    [
        [0.6717, 0.3147],   #R
        [0.2912, 0.6625],   #G
        [0.1573, 0.0560],   #B
    ]
)
"""*SAMPLE* colourspace primaries."""

WHITEPOINT_NAME_SAMPLE: str = "SAMPLE"
"""*SAMPLE* colourspace whitepoint name."""

CCS_WHITEPOINT_SAMPLE = np.array([0.3102, 0.3056])
"""*SAMPLE* colourspace whitepoint chromaticity coordinates."""

RGB_COLOURSPACE_SAMPLE = RGB_Colourspace(
    "Sample",
    PRIMARIES_SAMPLE,
    CCS_WHITEPOINT_SAMPLE,
    WHITEPOINT_NAME_SAMPLE
)
#
# ELLE GİRİLEN DENEME DEĞERLER #################################################
