import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import xrt.backends.raycing.materials as rm

from raypyng.postprocessing import PostProcessAnalyzed
from helper_lib import get_reflectivity
from parameter import SlitSize

##############################################################
# LOAD IN DATA

this_file_dir=os.path.dirname(os.path.realpath(__file__))

# Read CSV-File of the Beamline Simulation
# BL#1
BL1_file_path = os.path.join('RAYPy_Simulation_HRRIXS_91m_no_err_no_refl_FLUX', 'DetectorAtFocus_RawRaysOutgoing.csv')
BL1_df = pd.read_csv(BL1_file_path)
label_1 = 'HR-RIXS 93m'

# BL#2
BL2_file_path = os.path.join('RAYPy_Simulation_HRRIXS_93m_no_err_no_refl_FLUX', 'DetectorAtFocus_RawRaysOutgoing.csv')
BL2_df = pd.read_csv(BL2_file_path)
label_2 = 'HR-RIXS 91m'

##############################################################
# PLOTTING AND ANALYSIS
# Create the Main figure
fig, (axs) = plt.subplots(4, 2, figsize=(20, 15))
fig.suptitle('BESSY III HR-RIXS Beamline (91 vs. 93 m; with SU)', size=16)
x_range = [50, 3100]

# MIRROR REFLECTIVITY
ax1 = axs[0, 0]
# Coatings:
de = 38.9579-30.0000
table = 'Henke'
theta = 0.75
E = np.arange(50, 5001, de)

Au  = rm.Material('Au',  rho=19.32, kind='mirror',table=table)
B4C = rm.Material('C',   rho=2.52,  kind='mirror',table=table)
Cr  = rm.Material('Cr',  rho=7.14,  kind='mirror',table=table)
Ir  = rm.Material('Ir',  rho=22.56, kind='mirror',table=table)
IrCrB4C = rm.Multilayer( tLayer=B4C, tThickness=40, 
                        bLayer=Cr, bThickness=60, 
                        nPairs=1, substrate=Ir)
# Pt  = rm.Material('Pt',  rho=21.45, kind='mirror',table=table)

Au, _ = get_reflectivity(Au, E=E, theta=theta)
B4C, _ = get_reflectivity(B4C, E=E, theta=theta)
Cr, _ = get_reflectivity(Cr, E=E, theta=theta)
Ir, _ = get_reflectivity(Ir, E=E, theta=theta)
IrCrB4C, _ = get_reflectivity(IrCrB4C, E=E, theta=theta)
# Pt, _ = get_reflectivity(Pt, E=E, theta=theta)

ax1.plot(E, Au, 'gold', label='Au')
ax1.plot(E, B4C, 'black', label=r'B$_4$C')
ax1.plot(E, Cr, 'grey', label='Cr')
ax1.plot(E, Ir, 'silver', label='Ir')
ax1.plot(E, IrCrB4C, 'green', label=r'IrCrB$_4$C')
# ax1.plot(E, Pt, 'r', label='Pt')


ax1.set_title('Mirror Coating Reflectivity @ 'f'{theta}° incident angle')
ax1.set_xlabel('Energy [eV]')
ax1.set_ylabel('Reflectivity [a.u.]')
ax1.legend()
ax1.set_xlim(x_range)
ax1.minorticks_on()
ax1.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')



# FLUX CURVE UNDULATOR
#Choose the harmonic to plot
ax2 = axs[0, 1]

harms = [1,3,5] # The Harmonics from the ID. Typically 1,3,5, rather higher. Depends on the FluxSims of the ID.


# ax2.plot(BL_df['PhotonEnergy'], BL_df['PercentageRaysSurvived'])    
# ax2.set_title('SU Flux curve')
# ax2.set_xlabel('Energy [eV]')
# ax2.set_ylabel('Photon flux [% @c0.1% BW]')
# ax2.legend(fontsize=12, loc='best')
# ax2.set_xlim(x_range)
# ax2.minorticks_on()
# ax2.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# TRANSMITTED BANDWIDTH
ax3 = axs[1, 0]

ax3.plot(BL1_df['PhotonEnergy'], BL1_df['Bandwidth']*1000, label=label_1)
ax3.plot(BL2_df['PhotonEnergy'], BL2_df['Bandwidth']*1000, label=label_2)
ax3.set_title(f'Transmitted Bandwidth @{float(SlitSize*1000)} µm ExitSlit')
ax3.set_xlabel('Energy [eV]')
ax3.set_ylabel('Transmitted bandwidth [meV]')
ax3.legend(loc='best', fontsize=12)
ax3.set_xlim(x_range)
ax3.minorticks_on()
ax3.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# BEAMLINE FLUX CURVE
ax4 = axs[1, 1]

ax4.plot(BL1_df['PhotonEnergy'], BL1_df['PercentageRaysSurvived'], label=label_1)
ax4.plot(BL2_df['PhotonEnergy'], BL2_df['PercentageRaysSurvived'], label=label_2)   
ax4.set_title(f'Flux curve @{float(SlitSize*1000)} µm ExitSlit')
ax4.set_xlabel('Energy [eV]')
ax4.set_ylabel('Photon flux [%]')
# ax4.legend(loc='best', fontsize=12)
ax4.set_xlim(x_range)
ax4.minorticks_on()
ax4.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# RESOLVING POWER
ax5 = axs[2, 0]

ax5.plot(BL1_df['PhotonEnergy'], (BL1_df[f'PhotonEnergy']/BL1_df[f'Bandwidth']), label=label_1)
ax5.plot(BL2_df['PhotonEnergy'], (BL2_df[f'PhotonEnergy']/BL2_df[f'Bandwidth']), label=label_2)
ax5.set_title(f'Resolving Power @ {float(SlitSize*1000)} µm ExitSlit')
ax5.set_xlabel('Energy [eV]')
ax5.set_ylabel(r'$\frac{E}{\Delta E}$ [a.u.]')
# ax5.legend(loc='best', fontsize=12)
ax5.set_xlim(x_range)
ax5.minorticks_on()
ax5.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')

# Flux Density
ax6 = axs[2, 1]
# for harm in harms:
#     Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
#     Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
#     filtered_df = BL_df[(BL_df['PhotonEnergy'] >= Emin_harm) & (BL_df['PhotonEnergy'] <= Emax_harm)]
#     foc_area = (filtered_df['VerticalFocusFWHM']*filtered_df['HorizontalFocusFWHM'])*1000  # in µm²
#     ax6.plot(filtered_df['PhotonEnergy'],filtered_df[f'PhotonFlux{harm}']/foc_area, label=f'Harm. {harm}')

# Footprint BL1
FWHM_BL1_vf = BL1_df['VerticalFocusFWHM']*1000  # in µm
FWHM_BL2_hf = BL1_df['HorizontalFocusFWHM']*1000  # in µm
foc_area_BL1 = (FWHM_BL1_vf*FWHM_BL2_hf)  # in µm²

# Footprint BL2
FWHM_BL2_vf = BL2_df['VerticalFocusFWHM']*1000  # in µm
FWHM_BL2_hf = BL2_df['HorizontalFocusFWHM']*1000  # in µm
foc_area_BL2 = (FWHM_BL2_vf*FWHM_BL2_hf)  # in µm²

ax6.plot(BL1_df['PhotonEnergy'], (BL1_df['PercentageRaysSurvived']/foc_area_BL1), label=label_1)
ax6.plot(BL2_df['PhotonEnergy'], (BL2_df['PercentageRaysSurvived']/foc_area_BL2), label=label_2)
ax6.set_title('Flux Density')
ax6.set_xlabel('Energy [eV]')
ax6.set_ylabel('Photons per µm² [%]')
# ax6.legend(loc='best', fontsize=12)
ax6.set_xlim(x_range)
ax6.minorticks_on()
ax6.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')

# Horizontal Focus Size
ax7 = axs[3, 0]

ax7.plot(BL1_df['PhotonEnergy'], BL1_df['HorizontalFocusFWHM']*1000, label=label_1, color='red')
ax7.plot(BL2_df['PhotonEnergy'], BL2_df['HorizontalFocusFWHM']*1000, label=label_2, color='darkred')    

ax7.set_title('Horizontal Focus Size')
ax7.set_xlabel('Energy [eV]')
ax7.set_ylabel('[µm]')
ax7.legend(loc='best', fontsize=12)
ax7.set_xlim(x_range)
ax7.minorticks_on()
ax7.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')

# Vertical Focus Size
ax8 = axs[3, 1]

ax8.plot(BL1_df['PhotonEnergy'], BL1_df['VerticalFocusFWHM']*1000, label=label_1, color='green')
ax8.plot(BL2_df['PhotonEnergy'], BL2_df['VerticalFocusFWHM']*1000, label=label_2, color='darkgreen')

ax8.set_title('Vertical Focus Size')
ax8.set_xlabel('Energy [eV]')
ax8.set_ylabel('[µm]')
ax8.legend(loc='best', fontsize=12)
ax8.set_xlim(x_range)
ax8.minorticks_on()
ax8.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


##############################################################
# SAVING
# Ensure the "plot" folder exists
plot_folder = 'plot'
if not os.path.exists(plot_folder):
    os.makedirs(plot_folder)

# Save the the figure
plt.tight_layout()
# plt.savefig('plot/Photon Density B2_B3 errors_on at 24 mu.png')
plt.savefig('plot/BESSY III HR-RIXS comparison 91 vs 93 m.pdf')
plt.tight_layout()
plt.show()
