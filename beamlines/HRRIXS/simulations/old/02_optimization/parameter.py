import numpy as np
# these must match the name of the rml files in the rml folder that you want to simulate

rml_file_name_bessy3_HRRIXS_myV2   = 'bessy3_93_HRRIXS_V2'              #my approach of the HR-RIXS BL
rml_file_name_bessy3_HRRIXS_myV3   = 'bessy3_93_HRRIXS_V3_const'        #constrains of B3 - Radiaton protection
rml_file_name_bessy3_HRRIXS_myV4   = 'bessy3_93_HRRIXS_V4'
rml_file_name_bessy3_HRRIXS_myV5   = 'bessy3_93_HRRIXS_V5'
rml_file_name_bessy3_HRRIXS_JV     = 'bessy3_High_end_BL_SU_V2'         #Jens BL

order       = 1
SlitSize    = np.array([.012, .010, .008, .006, .002])
grating     = np.array([2400])
cff         = np.array([2.50])

energy_flux = np.arange(100, 2001,50)
energy_rp   = np.arange(100, 2001,50)

nrays_flux  = 1e5
nrays_rp    = 1e5

round_flux = 4
round_rp   = 4

ncpu       = 10

### plotting colors
import matplotlib
import matplotlib.pyplot as plt
# Generate 20 colors from the 'hsv' colormap which resembles a rainbow
colors_rainbow = plt.cm.tab20(np.linspace(0, 2, int(max(1,2))))
# Convert the colors to hex format for easy usage
colors = [matplotlib.colors.rgb2hex(color) for color in colors_rainbow]
colors = ["Red", "Orange", "Green", "Blue", "Indigo", "Violet"]
