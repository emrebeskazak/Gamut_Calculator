# import numpy as np
# import colour
from colour.plotting import ( 
    plot_RGB_colourspaces_in_chromaticity_diagram_CIE1931, 
    plot_RGB_colourspaces_in_chromaticity_diagram_CIE1976UCS
)

# from colour.models import (
#     RGB_COLOURSPACE_sRGB, 
#     RGB_COLOURSPACE_BT2020, 
#     RGB_COLOURSPACE_NTSC1953
# )

import sample

plot_RGB_colourspaces_in_chromaticity_diagram_CIE1931(['ITU-R BT.2020', sample.RGB_COLOURSPACE_SAMPLE])
