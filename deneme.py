# C:\Users\emre\AppData\Local\Programs\Python\Python310\Lib\site-packages\colour

# # Plotting the *CIE 1931 Chromaticity Diagram*.
# # The argument *standalone=False* is passed so that the plot doesn't get displayed
# # and can be used as a basis for other plots.
# chromaticity_diagram_plot_CIE1931(standalone=True)

##############################
# import colour
# colour.plotting.temperature.plot_planckian_locus_in_chromaticity_diagram(['D65'], bounding_box=[0.4, 0.6, 0, 1])

##############################
#Or if you want to do it via Matplotlib, you will need to use the standalone keyword as we are rendering/showing the figure by default:

import numpy as np
import colour
# import matplotlib.pyplot as plt
# # colour.plotting.temperature.plot_planckian_locus_in_chromaticity_diagram(['D65'], standalone=False)
# # colour.plotting.plot_chromaticity_diagram_CIE1931(standalone=False)
# # colour.plotting.plot_RGB_chromaticities_in_chromaticity_diagram_CIE1931(standalone=False)
# colour.plotting.plot_chromaticity_diagram()
# # plt.xlim([0.4, 0.6])
# plt.show()

# from colour.plotting import *
# RGB = np.random.random((32, 32, 3))
# # print(RGB)
# plot_RGB_chromaticities_in_chromaticity_diagram_CIE1931(RGB, colourspaces=['ACEScg', 'S-Gamut', 'Pointer Gamut'])

from colour.models import RGB_COLOURSPACE_sRGB, RGB_COLOURSPACE_BT2020, RGB_COLOURSPACE_NTSC1953
print(RGB_COLOURSPACE_NTSC1953.primaries)
# prng = np.random.RandomState(2)
# colour.RGB_colourspace_pointer_gamut_coverage_MonteCarlo(RGB_COLOURSPACE_sRGB, 10e3, random_state=prng)

# 3 boyutlu çizdiriyor
# plot_RGB_colourspaces_gamuts(['ITU-R BT.709', 'ACEScg', 'S-Gamut'])
