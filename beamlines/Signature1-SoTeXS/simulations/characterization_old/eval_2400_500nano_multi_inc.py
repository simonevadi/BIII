import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import xrt.backends.raycing.materials as rm
import warnings
warnings.filterwarnings(
    "ignore",
    message="Reading `.npy` or `.npz` file required additional header parsing as it was created on Python 2. Save the file again to speed up loading and avoid this warning."
) 
from helper_lib import get_reflectivity
from parameter import SlitSize_2400 as SlitSize
from parameter import undulator as undulator_df

from raypyng.postprocessing import PostProcessAnalyzed

p = PostProcessAnalyzed()
mov_av = p.moving_average
##############################################################
# LOAD IN DATA

# Read CSV-File of the Beamline Simulation
BL_file_path = os.path.join('RAYPy_Simulation_sotexs_2400_500nano_vary_incidence_angle_mirrors', 'DetectorAtFocus_RawRaysOutgoing.csv')
BL_df = pd.read_csv(BL_file_path)


##############################################################

inc_angles = BL_df['KB_ver.grazingIncAngle'].unique()
print("Unique values in 'KB_ver.grazingIncAngle':")
print(BL_df['KB_ver.grazingIncAngle'].unique())

##############################################################
# PLOTTING AND ANALYSIS
# Extract unique incidence angles from the DataFrame
linestyle_list = ['solid', 'dashed', 'dotted', 'dashdot']
colors = [
    '#1f77b4',  # blue
    '#17becf',  # cyan
    '#2ca02c',  # green
    '#ff7f0e',  # orange
    '#d62728',  # red
    '#9467bd'   # purple
]
# Create the Main figure
plt.rcParams.update({'font.size': 25})  # Change 14 to any size you prefer
fig, (axs) = plt.subplots(2, 2, figsize=(30, 15))
fig.suptitle('SoTeXS, 2400 l/mm, nano focus - M1: 600mm, M3: 500mm, KB_ver: 600mm, KB_hor:400, KB2_ver:500, KB2_hor:400')
x_range = [500, 8000]

# MIRROR REFLECTIVITY
ax1 = axs[0, 0]
# Coatings:
de = 38.9579-30.0000
table = 'Henke'
theta = 0.4
E = np.arange(500, 8001, de)
Ir  = rm.Material('Ir',  rho=22.56, kind='mirror',table=table)
Cr  = rm.Material('Cr',  rho=7.15,  kind='mirror',table=table)
B4C = rm.Material('C',   rho=2.52,  kind='mirror',table=table)
IrCrB4C = rm.Multilayer(tLayer=B4C, tThickness=40, 
                        bLayer=Cr, bThickness=60, 
                        nPairs=1, substrate=Ir)
for ind, theta in enumerate(inc_angles):
    IrCrB4C_r, _ = get_reflectivity(IrCrB4C, E=E, theta=theta)
    ax1.plot(E, IrCrB4C_r,
             color=colors[ind], label=f'theta {theta}°')

ax1.set_title('IrCrB4C Reflectivity at different incidence angles')
ax1.set_xlabel('Energy [eV]')
ax1.set_ylabel('Reflectivity [a.u.]')
ax1.legend()
ax1.set_xlim(x_range)
ax1.minorticks_on()
ax1.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')



# FLUX CURVE UNDULATOR
#Choose the harmonic to plot
ax2 = axs[1, 0]

harms = [1,3,5] # The Harmonics from the ID. Typically 1,3,5, rather higher. Depends on the FluxSims of the ID.

for ind, harm in enumerate(harms):
    ax2.plot(undulator_df[f'Energy{harm}[eV]'], undulator_df[f'Photons{harm}'],
             linestyle=linestyle_list[ind],label=f'Harm. {harm}')
    
ax2.set_title('CPMU21 Flux curve')
ax2.set_xlabel('Energy [eV]')
ax2.set_ylabel('Photon flux [ph/s/300 mA/0.1% BW]')
ax2.legend(loc='best')
ax2.set_xlim(x_range)
ax2.minorticks_on()
ax2.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# TRANSMITTED BANDWIDTH
# ax3 = axs[1, 0]

# window = 1
# for harm in harms:
#     Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
#     Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
#     filtered_df = BL_df[(BL_df['PhotonEnergy'] >= Emin_harm) & (BL_df['PhotonEnergy'] <= Emax_harm)]
#     ax3.plot(mov_av(filtered_df['PhotonEnergy'], window), 
#              mov_av(filtered_df['Bandwidth']*1000, window),
#              label=f'Harm. {harm}')

# ax3.set_title(f'Transmitted Bandwidth @{int(SlitSize[0]*1000)} µm ExitSlit')
# ax3.set_xlabel('Energy [eV]')
# ax3.set_ylabel('Transmitted bandwidth [meV]')
# # ax3.legend(loc='best', fontsize=12)
# ax3.set_xlim(x_range)
# ax3.minorticks_on()
# ax3.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# BEAMLINE FLUX CURVE
ax4 = axs[0, 1]
for ind, inc_angle in enumerate(inc_angles):
    filtered_df = BL_df[BL_df['KB_ver.grazingIncAngle'] == inc_angle]
    for ind2, harm in enumerate(harms):
        Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
        Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
        ax4.plot(filtered_df['PhotonEnergy'], filtered_df[f'PhotonFlux{harm}'],
                 color=colors[ind], linestyle=linestyle_list[ind2],
                 label=f'Inc. Angle {inc_angle}' if harm==1 else None)

ax4.set_title('Flux with CPMU21')
ax4.set_xlabel('Energy [eV]')
ax4.set_ylabel('Photon flux [ph/s/300 mA/TBW]')
ax4.legend(loc='best')
ax4.set_xlim(x_range)
ax4.minorticks_on()
ax4.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')
ax4.set_yscale('log')

# # RESOLVING POWER
# ax5 = axs[2, 0]
# for inc_angle in inc_angles:
#     filtered_df = BL_df[BL_df['KB_ver.grazingIncAngle'] == inc_angle]
#     for harm in harms:
#         Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
#         Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
#         # filtered_df = filtered_df[(filtered_df['PhotonEnergy'] >= Emin_harm) & (filtered_df['PhotonEnergy'] <= Emax_harm)]
#         ax5.plot(mov_av(filtered_df['PhotonEnergy'], window),
#                 mov_av(filtered_df[f'PhotonEnergy']/filtered_df[f'Bandwidth'], window),
#                 label=f'Harm. {harm}')

# ax5.set_title(f'Resolving Power @ {int(SlitSize[0]*1000)} µm ExitSlit')
# ax5.set_xlabel('Energy [eV]')
# ax5.set_ylabel(r'$\frac{E}{\Delta E}$ [a.u.]')
# # ax5.legend(loc='best', fontsize=12)
# ax5.set_xlim(x_range)
# ax5.minorticks_on()
# ax5.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# Flux Density
ax6 = axs[1, 1]
for ind, inc_angle in enumerate(inc_angles):
    filtered_df = BL_df[BL_df['KB_ver.grazingIncAngle'] == inc_angle]
    for ind2, harm in enumerate(harms):
        Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
        Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
        # filtered_df = BL_df[(BL_df['PhotonEnergy'] >= Emin_harm) & (BL_df['PhotonEnergy'] <= Emax_harm)]
        foc_area = (filtered_df['VerticalFocusFWHM']*filtered_df['HorizontalFocusFWHM'])*1000  # in µm²
        ax6.plot(filtered_df['PhotonEnergy'],filtered_df[f'PhotonFlux{harm}']/foc_area,
                color=colors[ind], linestyle=linestyle_list[ind2],
                label=f'Inc. Angle {inc_angle}' if harm==1 else None)

ax6.set_title('Flux Density')
ax6.set_xlabel('Energy [eV]')
ax6.set_ylabel('Photons flux per µm²')
# ax6.legend(loc='best')
ax6.set_xlim(x_range)
ax6.minorticks_on()
ax6.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')

# # Horizontal Focus Size
# ax7 = axs[3, 0]
# ax7.plot(mov_av(BL_df['PhotonEnergy'], window),
#          mov_av(BL_df['HorizontalFocusFWHM']*1000, window),
#          label='Horizontal Focus Size', color='red')

# ax7.set_title('Horizontal Focus Size')
# ax7.set_xlabel('Energy [eV]')
# ax7.set_ylabel('[µm]')
# ax7.set_xlim(x_range)
# ax7.minorticks_on()
# ax7.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')

# Vertical Focus Size
# ax8 = axs[3, 1]

# ax8.plot(mov_av(BL_df['PhotonEnergy'], window),
#          mov_av(BL_df['VerticalFocusFWHM']*1000, window),
#          label='Vertical Focus Size', color='limegreen')

# ax8.set_title('Vertical Focus Size')
# ax8.set_xlabel('Energy [eV]')
# ax8.set_ylabel('[µm]')
# ax8.set_xlim(x_range)
# ax8.minorticks_on()
# ax8.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


##############################################################
# SAVING
# Ensure the "plot" folder exists
plot_folder = 'plot'
if not os.path.exists(plot_folder):
    os.makedirs(plot_folder)

# Save the the figure
plt.tight_layout()
plt.savefig('plot/SoTeXS_2400_500nano_multi_inc.png')
# plt.show()
