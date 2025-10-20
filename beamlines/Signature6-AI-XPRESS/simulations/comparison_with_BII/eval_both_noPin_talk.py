import os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd
import numpy as np
import xrt.backends.raycing.materials as rm
import warnings
warnings.filterwarnings(
    "ignore",
    message="Reading `.npy` or `.npz` file required additional header parsing as it was created on Python 2. Save the file again to speed up loading and avoid this warning."
)
from helper_lib import get_reflectivity

from raypyng.postprocessing import PostProcessAnalyzed

p = PostProcessAnalyzed()
mov_av = p.moving_average
##############################################################
# LOAD IN DATA

current_factor = 3
mrad_scale = 200
# Read CSV-File of the Beamline Simulation
BL_file_path = os.path.join('..','characterization','RAYPy_Simulation_AI-XPRESS_Si111', 'DetectorAtFocus_RawRaysOutgoing.csv')
BL_df_si111 = pd.read_csv(BL_file_path)
BL_df_si111[f'SourcePhotonFlux'] = BL_df_si111[f'SourcePhotonFlux']*current_factor # for 300 mA
BL_df_si111[f'PhotonFlux'] = BL_df_si111[f'PhotonFlux']*current_factor # for 300 mA

myspot_Si111_path = os.path.join('RAYPy_Simulation_MySpot_Si111_noM2_no_pinhole', 'DetectorAtFocus_RawRaysOutgoing.csv')
myspot_Si111 = pd.read_csv(myspot_Si111_path)
myspot_Si111[f'SourcePhotonFlux'] = myspot_Si111[f'SourcePhotonFlux']*current_factor/mrad_scale # for 300 mA
myspot_Si111[f'PhotonFlux'] = myspot_Si111[f'PhotonFlux']*current_factor # for 300 mA

##############################################################
# PLOTTING AND ANALYSIS
plt.rcParams.update({'font.size': 13})  # Change 14 to any size you prefer
# Create the Main figure
fig, (axs) = plt.subplots(1, 2, figsize=(20, 7))
fig.suptitle('Signature6: AI-XPRESS, Comparison at BII: MySpot', size=16)
x_range = [2500, 40000]
colors = ['blue', 'red', 'green', 'orange', 'purple', 'violet']

# MIRROR REFLECTIVITY
ax1 = axs[0]
# Coatings:
de = 0.1
table = 'Chantler'
theta = 0.1
E = np.arange(500, x_range[-1], de)
Ir  = rm.Material('Ir',  rho=22.56, kind='mirror',table=table)
Rh  = rm.Material('Rh',  rho=12.423,  kind='mirror',table=table)
IrRh = rm.Multilayer(tLayer=Rh, tThickness=40, 
                        bLayer=Rh, bThickness=0, 
                        nPairs=1, substrate=Ir)

Ir, _ = get_reflectivity(Ir, E=E, theta=theta)
Rh, _ = get_reflectivity(Rh, E=E, theta=theta)
IrRh, _ = get_reflectivity(IrRh, E=E, theta=theta)

ax1.plot(E, Ir, 'grey', label='Ir', alpha=0.5, linewidth=1.5)
ax1.plot(E, Rh, 'blue', label='Rh', alpha=0.5, linewidth=1.5)
ax1.plot(E, IrRh, 'black', label='IrRh', linewidth=2)

ax1.set_title('Mirror Coating Reflectivity @ 'f'{theta}° incident angle')
ax1.set_xlabel('Energy [eV]')
ax1.set_ylabel('Reflectivity [a.u.]')
ax1.legend()
ax1.set_xlim(x_range)
ax1.minorticks_on()
ax1.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# FLUX CURVE DIPOLE
#Choose the harmonic to plot
ax2 = axs[1]


ax2.plot(BL_df_si111[f'PhotonEnergy'],
            BL_df_si111[f'SourcePhotonFlux'],
            label='BIII SB 4T')

ax2.plot(myspot_Si111[f'PhotonEnergy'],
            myspot_Si111[f'SourcePhotonFlux'],
            label='BII WS 7T')


    
ax2.set_title('Source, Superbend 4T BIII vs Wavelength Shifter 7T BII')
ax2.set_xlabel('Energy [eV]')
ax2.set_ylabel('Photon flux [ph/s/300 mA/0.1% BW]')
ax2.legend(loc='best')
ax2.set_xlim(x_range)
ax2.set_yscale('log')
ax2.minorticks_on()
ax2.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')

##############################################################
# SAVING
# Ensure the "plot" folder exists
plot_folder = 'plot'
if not os.path.exists(plot_folder):
    os.makedirs(plot_folder)

# Save the the figure
plt.tight_layout()
plt.savefig('plot/talk/AI_XPRESS_MySpot_comparison_noPinhole_1.png')
# plt.show()
plt.close()

fig, (axs) = plt.subplots(1, 2, figsize=(20, 7))
fig.suptitle('Signature6: AI-XPRESS, Comparison at BII: MySpot', size=16)
# TRANSMITTED BANDWIDTH
ax3 = axs[0]

window = 2

# Si111 BIII
ax3.plot(mov_av(BL_df_si111['PhotonEnergy'], window), 
            mov_av(BL_df_si111['Bandwidth'], window),
            label=f'BIII Si111')    
# Si111 BII
ax3.plot(mov_av(myspot_Si111['PhotonEnergy'], window), 
            mov_av(myspot_Si111['Bandwidth'], window),
            label=f'BII Si111')    
 

ax3.set_title(f'Transmitted Bandwidth')
ax3.set_xlabel('Energy [eV]')
ax3.set_ylabel('Transmitted bandwidth [eV]')
ax3.set_xlim(x_range)
ax3.minorticks_on()
# ax3.set_yscale('log')
ax3.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')
ax3.legend(loc='lower right', ncol=2)


# BEAMLINE FLUX CURVE
ax4 = axs[1]

# BIII Si111
ax4.plot(mov_av(BL_df_si111['PhotonEnergy'], window), 
            mov_av(BL_df_si111['PhotonFlux'], window),
            label=f'BIII Si111')    
# BII Si111
ax4.plot(mov_av(myspot_Si111['PhotonEnergy'], window), 
            mov_av(myspot_Si111['PhotonFlux'], window),
            label=f'BII Si111')   

ax4.set_title('Flux at Focus')
ax4.set_xlabel('Energy [eV]')
ax4.set_ylabel('Photon flux [ph/s/300 mA/TBW]')
ax4.set_xlim(x_range)
ax4.minorticks_on()
ax4.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')
ax4.set_yscale('log')

# Save the the figure
plt.tight_layout()
plt.savefig('plot/talk/AI_XPRESS_MySpot_comparison_noPinhole_2.png')
# plt.show()
plt.close()

fig, (axs) = plt.subplots(1, 2, figsize=(20, 7))
fig.suptitle('Signature6: AI-XPRESS, Comparison at BII: MySpot', size=16)

# # RESOLVING POWER
# ax5 = axs[2, 0]
# window = 1

# # BIII Si111
# ax5.plot(mov_av(BL_df_si111['PhotonEnergy'], window),
#          mov_av(BL_df_si111[f'PhotonEnergy']/BL_df_si111[f'Bandwidth'], window),
#          linestyle='solid', label='BIII Si111')

# # BII Si111
# ax5.plot(mov_av(myspot_Si111['PhotonEnergy'], window),
#          mov_av(myspot_Si111[f'PhotonEnergy']/myspot_Si111[f'Bandwidth'], window),
#          linestyle='solid', label='BII Si111')



# ax5.set_title(f'Resolving Power')
# ax5.set_xlabel('Energy [eV]')
# ax5.set_ylabel(r'$\frac{E}{\Delta E}$ [a.u.]')
# ax5.set_xlim(x_range)
# ax5.legend(loc='best')
# ax5.minorticks_on()
# ax5.set_ylim(0, 20000)
# ax5.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# # Flux Density
# ax6 = axs[2, 1]


# # BIII Si111
# foc_area = (BL_df_si111['VerticalFocusFWHM']*BL_df_si111['HorizontalFocusFWHM'])*1000  # in µm²

# ax6.plot(BL_df_si111['PhotonEnergy'],
#              BL_df_si111[f'PhotonFlux']/foc_area,
#              label=f'BIII Si111')
    
# # BIII Si111
# foc_area = (myspot_Si111['VerticalFocusFWHM']*myspot_Si111['HorizontalFocusFWHM'])*1000  # in µm²

# ax6.plot(myspot_Si111['PhotonEnergy'],
#              myspot_Si111[f'PhotonFlux']/foc_area,
#              label=f'BII Si111')


# ax6.set_title('Flux Density')
# ax6.set_xlabel('Energy [eV]')
# ax6.set_ylabel('Photons flux per µm²')
# ax6.set_xlim(x_range)
# ax6.set_yscale('log')
# ax6.minorticks_on()
# ax6.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')

# ####################################################
# # Focus at BIII
# ax7 = axs[3,0]
# x_lim =(-450,450)
# y_lim =(-450,450)
# focus_path = os.path.join('plot', 'AI-XPRESS_DetectorAtFocus-RawRaysOutgoing.csv')
# focus = pd.read_csv(
#     focus_path,
#     sep='\t',        # columns separated by tabs
#     decimal='.',     # use comma as decimal separator
#     skiprows=1       # skip the first line (the 'sep=' line)
# )
# x = focus['DetectorAtFocus_OX'] * 1e3
# y = focus['DetectorAtFocus_OY'] * 1e3


# ax7.scatter(x,y, s=4, color='yellow', alpha=1)

# ax7.set_facecolor('#002147')


# ax7.set_xlim(x_lim)
# ax7.set_ylim(y_lim)

# ax7.set_xlabel('µm')
# ax7.set_ylabel('µm')
# hor_foc = np.mean(BL_df_si111['HorizontalFocusFWHM']*1e3)
# ver_foc = np.mean(BL_df_si111['VerticalFocusFWHM']*1e3)
# ax7.set_title(f'AI-XPRESS Focus, FWHM(HxV) {50:.0f} x {50:.0f} µm²')

# ####################################################
# # Focus at BII
# ax8 = axs[3,1]

# focus_path = os.path.join('plot', 'MySpot_noPinhole_DetectorAtFocus-RawRaysOutgoing.csv')
# focus = pd.read_csv(
#     focus_path,
#     sep='\t',        # columns separated by tabs
#     decimal='.',     # use comma as decimal separator
#     skiprows=1       # skip the first line (the 'sep=' line)
# )
# x = focus['DetectorAtFocus_OX'] * 1e3
# y = focus['DetectorAtFocus_OY'] * 1e3

# ax8.scatter(x,y, s=4, color='yellow', alpha=1)

# ax8.set_facecolor('#002147')


# ax8.set_xlim(x_lim)
# ax8.set_ylim(y_lim)

# ax8.set_xlabel('µm')
# ax8.set_ylabel('µm')
# hor_foc = np.mean(BL_df_si111['HorizontalFocusFWHM']*1e3)
# ver_foc = np.mean(BL_df_si111['VerticalFocusFWHM']*1e3)
# ax8.set_title(f'MySpot Focus, FWHM(HxV) {270:.0f} x {150:.0f} µm²')




