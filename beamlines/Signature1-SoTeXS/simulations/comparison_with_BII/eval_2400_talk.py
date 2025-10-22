import os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import xrt.backends.raycing.materials as rm
import warnings
warnings.filterwarnings(
    "ignore",
    message="Reading `.npy` or `.npz` file required additional header parsing as it was created on Python 2. Save the file again to speed up loading and avoid this warning."
)
from helper_lib import get_reflectivity

import pandas as pd

from parameter3 import SlitSize_2400 as SlitSize
from parameter3 import undulator as undulator_3

from params import undulator as undulator_2
from raypyng.postprocessing import PostProcessAnalyzed

p = PostProcessAnalyzed()
mov_av = p.moving_average
##############################################################
# LOAD IN DATA

# Read CSV-File of the Beamline Simulation
BL_file_path = os.path.join('../characterization/RAYPy_Simulation_sotexs_2400', 'DetectorAtFocus_RawRaysOutgoing.csv')
BL_df = pd.read_csv(BL_file_path)

# Read CSV-File of the Beamline Simulation
BL_file_path = os.path.join('../characterization/RAYPy_Simulation_sotexs_2400', 'IntermediateFocus_RawRaysIncoming.csv')
BL_df_micro = pd.read_csv(BL_file_path)

# Read CSV-File of the Beamline Simulation
BL_file_path = os.path.join('RAYPy_Simulation_2400', 'DetectorAtFocus_RawRaysOutgoing.csv')
BL_df_2 = pd.read_csv(BL_file_path)

harms=[1,3,5]
##############################################################
# PLOTTING AND ANALYSIS
plt.rcParams.update({'font.size': 15})  # Change 14 to any size you prefer
# Create the Main figure
fig, (axs) = plt.subplots(1, 2, figsize=(20, 7))
fig.suptitle('Comparison SoTeXS @ BESSY II and BESSY III, 2400 l/mm')
x_range = [500, 8000]

# MIRROR REFLECTIVITY
ax1 = axs[0]
# Coatings:
de = 38.9579-30.0000
table = 'Henke'
theta = 0.4
E = np.arange(500, x_range[-1], de)
Ir  = rm.Material('Ir',  rho=22.56, kind='mirror',table=table)
Cr  = rm.Material('Cr',  rho=7.15,  kind='mirror',table=table)
B4C = rm.Material('C',   rho=2.52,  kind='mirror',table=table)
IrCrB4C = rm.Multilayer(tLayer=B4C, tThickness=40, 
                        bLayer=Cr, bThickness=60, 
                        nPairs=1, substrate=Ir)

Ir, _ = get_reflectivity(Ir, E=E, theta=theta)
Cr, _ = get_reflectivity(Cr, E=E, theta=theta)
B4C, _ = get_reflectivity(B4C, E=E, theta=theta)
IrCrB4C, _ = get_reflectivity(IrCrB4C, E=E, theta=theta)

ax1.plot(E, Ir, 'gold', label='Ir', alpha=0.5)
ax1.plot(E, Cr, 'blue', label='Cr', alpha=0.5)
ax1.plot(E, B4C, 'red', label='B4C', alpha=0.5)
ax1.plot(E, IrCrB4C, 'black', label='IrCrB4C', linewidth=2)

ax1.set_title('Mirror Coating Reflectivity @ 'f'{theta}° incident angle')
ax1.set_xlabel('Energy [eV]')
ax1.set_ylabel('Reflectivity [a.u.]')
ax1.legend()
ax1.set_xlim(x_range)
ax1.minorticks_on()
ax1.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')



ax3 = axs[0]

window = 20
colors = ['red', 'blue', 'green']
color_B2 = ['salmon', 'skyblue', 'lightgreen']


ax3 = axs[1]
for ind,harm in enumerate(harms):
    ax3.plot(undulator_3[f'Energy{harm}[eV]'], 
             undulator_3[f'Photons{harm}'],
             color=colors[ind], linestyle='solid',
             linewidth=3,
             label=f'B3-Harm. {harm}')
for ind,harm in enumerate(harms):
    ax3.plot(undulator_2[f'Energy{harm}[eV]'], 
             undulator_2[f'Photons{harm}'],
             color=color_B2[ind], linestyle='dashed',
             label=f'B2-Harm. {harm}')
    
ax3.legend()
ax3.set_yscale('log')
ax3.set_ylim((1e11,2e15))
ax3.set_xlabel('Energy [eV]')
ax3.set_ylabel('Ph/s/0.3A/0.1%BW')
ax3.set_title('IVU28 @ BESSY III vs CPMU21 @ BESSY II')

# SAVING
# Ensure the "plot" folder exists
plot_folder = 'plot'
if not os.path.exists(plot_folder):
    os.makedirs(plot_folder)

# Save the the figure
plt.tight_layout()
plt.savefig('plot/talk/SoTeXS_2400_comparison_1.png')
# plt.show()
plt.close()





###################################################
fig, (axs) = plt.subplots(1, 2, figsize=(20, 7))
fig.suptitle('Comparison SoTeXS @ BESSY II and BESSY III, 2400 l/mm')


# TRANSMITTED BANDWIDTH
ax3 = axs[0]

window = 20
colors = ['red', 'blue', 'green']
color_B2 = ['salmon', 'skyblue', 'lightgreen']

ax3.plot(mov_av(BL_df['PhotonEnergy'], window), 
             mov_av(BL_df['Bandwidth']*1000, window),
             linestyle='solid',
             label=f'B3 - nano focus',
             color='blue')
ax3.plot(mov_av(BL_df_micro['PhotonEnergy'], window), 
             mov_av(BL_df_micro['Bandwidth']*1000, window),
             linestyle='solid',
             label=f'B3 - micro focus', 
             color='orange')

ax3.plot(mov_av(BL_df_2['PhotonEnergy'], window), 
             mov_av(BL_df_2['Bandwidth']*1000, window),
             linestyle='solid',
             label=f'B2', 
             color='green')



ax3.set_title(f'Transmitted Bandwidth @{int(SlitSize[0]*1000)} µm ExitSlit')
ax3.set_xlabel('Energy [eV]')
ax3.set_ylabel('Transmitted bandwidth [meV]')
ax3.legend(loc='best')
ax3.set_xlim(x_range)
ax3.minorticks_on()
ax3.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# BEAMLINE FLUX CURVE
ax4 = axs[1]
window = 1
for ind,harm in enumerate(harms):
    Emin_harm = undulator_3[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_3[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df[(BL_df['PhotonEnergy'] >= Emin_harm) & (BL_df['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(mov_av(filtered_df['PhotonEnergy'], window), 
             mov_av(filtered_df[f'PhotonFlux{harm}'], window),
             color='blue', linestyle='solid',
             label=f'B3-nano')

for ind,harm in enumerate(harms):
    Emin_harm = undulator_3[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_3[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df_micro[(BL_df_micro['PhotonEnergy'] >= Emin_harm) & (BL_df_micro['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(mov_av(filtered_df['PhotonEnergy'], window), 
             mov_av(filtered_df[f'PhotonFlux{harm}'], window),
             color='orange', linestyle='solid',
             label=f'B3-micro')
    
for ind,harm in enumerate(harms):    
    Emin_harm = undulator_2[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_2[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df_2[(BL_df_2['PhotonEnergy'] >= Emin_harm) & (BL_df_2['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(mov_av(filtered_df['PhotonEnergy'], window), 
                mov_av(filtered_df[f'PhotonFlux{harm}'], window),
                color='green', linestyle='dashed',
                label=f'B2-Harm. {harm}')
    

ax4.set_title('Flux at Focus')
ax4.set_xlabel('Energy [eV]')
ax4.set_ylabel('Photon flux [ph/s/300 mA/TBW]')
custom_lines = [
    Line2D([0], [0], color='blue', linestyle='solid', lw=2),
    Line2D([0], [0], color='orange', linestyle='solid', lw=2),
    Line2D([0], [0], color='green', linestyle='solid', lw=2)
]

ax4.legend(custom_lines, ['B3-nano', 'B3-micro', 'B2'], loc='best')
ax4.set_xlim(x_range)
ax4.minorticks_on()
ax4.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')
ax4.set_ylim((10e9,1e15))
ax4.set_yscale('log')

# Save the the figure
plt.tight_layout()
plt.savefig('plot/talk/SoTeXS_2400_comparison_2.png')
# plt.show()
plt.close()

# # TRANSMITTED BANDWIDTH
# ax3 = axs[0, 0]

# window = 20
# colors = ['red', 'blue', 'green']
# color_B2 = ['salmon', 'skyblue', 'lightgreen']
# for ind,harm in enumerate(harms):
#     Emin_harm = undulator_3[f'Energy{harm}[eV]'].min()
#     Emax_harm = undulator_3[f'Energy{harm}[eV]'].max()
#     filtered_df = BL_df[(BL_df['PhotonEnergy'] >= Emin_harm) & (BL_df['PhotonEnergy'] <= Emax_harm)]
#     ax3.plot(mov_av(filtered_df['PhotonEnergy'], window), 
#              mov_av(filtered_df['Bandwidth']*1000, window),
#              color=colors[ind], linestyle='solid',
#              label=f'B3-Harm. {harm}')
#     Emin_harm = undulator_2[f'Energy{harm}[eV]'].min()
#     Emax_harm = undulator_2[f'Energy{harm}[eV]'].max()
#     filtered_df = BL_df_2[(BL_df_2['PhotonEnergy'] >= Emin_harm) & (BL_df_2['PhotonEnergy'] <= Emax_harm)]
#     ax3.plot(mov_av(filtered_df['PhotonEnergy'], window), 
#                 mov_av(filtered_df['Bandwidth']*1000, window),
#                 color=color_B2[ind], linestyle='dashed',
#                 label=f'B2-Harm. {harm}')


# ax3.set_title(f'Transmitted Bandwidth @{int(SlitSize[0]*1000)} µm ExitSlit')
# ax3.set_xlabel('Energy [eV]')
# ax3.set_ylabel('Transmitted bandwidth [meV]')
# ax3.legend(loc='best')
# ax3.set_xlim(x_range)
# ax3.minorticks_on()
# ax3.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# # BEAMLINE FLUX CURVE
# ax4 = axs[0, 1]
# window = 1
# for ind,harm in enumerate(harms):
#     Emin_harm = undulator_3[f'Energy{harm}[eV]'].min()
#     Emax_harm = undulator_3[f'Energy{harm}[eV]'].max()
#     filtered_df = BL_df[(BL_df['PhotonEnergy'] >= Emin_harm) & (BL_df['PhotonEnergy'] <= Emax_harm)]
#     ax4.plot(mov_av(filtered_df['PhotonEnergy'], window), 
#              mov_av(filtered_df[f'PhotonFlux{harm}'], window),
#              color=colors[ind], linestyle='solid',
#              label=f'B3-Harm. {harm}')
#     Emin_harm = undulator_2[f'Energy{harm}[eV]'].min()
#     Emax_harm = undulator_2[f'Energy{harm}[eV]'].max()
#     filtered_df = BL_df_2[(BL_df_2['PhotonEnergy'] >= Emin_harm) & (BL_df_2['PhotonEnergy'] <= Emax_harm)]
#     ax4.plot(mov_av(filtered_df['PhotonEnergy'], window), 
#                 mov_av(filtered_df[f'PhotonFlux{harm}'], window),
#                 color=color_B2[ind], linestyle='dashed',
#                 label=f'B2-Harm. {harm}')
    

# ax4.set_title('Flux with CPMU21')
# ax4.set_xlabel('Energy [eV]')
# ax4.set_ylabel('Photon flux [ph/s/300 mA/TBW]')
# ax4.legend(loc='best')
# ax4.set_xlim(x_range)
# ax4.minorticks_on()
# ax4.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')
# ax4.set_yscale('log')

# # RESOLVING POWER
# ax5 = axs[1, 0]
# window = 20
# for ind,harm in enumerate(harms):
#     Emin_harm = undulator_3[f'Energy{harm}[eV]'].min()
#     Emax_harm = undulator_3[f'Energy{harm}[eV]'].max()
#     filtered_df = BL_df[(BL_df['PhotonEnergy'] >= Emin_harm) & (BL_df['PhotonEnergy'] <= Emax_harm)]
#     ax5.plot(mov_av(filtered_df['PhotonEnergy'], window),
#              mov_av(filtered_df[f'PhotonEnergy']/filtered_df[f'Bandwidth'], window),
#              color=colors[ind], linestyle='solid',
#              label=f'B3-Harm. {harm}')
#     Emin_harm = undulator_2[f'Energy{harm}[eV]'].min()
#     Emax_harm = undulator_2[f'Energy{harm}[eV]'].max()
#     filtered_df = BL_df_2[(BL_df_2['PhotonEnergy'] >= Emin_harm) & (BL_df_2['PhotonEnergy'] <= Emax_harm)]
#     ax5.plot(mov_av(filtered_df['PhotonEnergy'], window),
#              mov_av(filtered_df[f'PhotonEnergy']/filtered_df[f'Bandwidth'], window),
#                 color=color_B2[ind], linestyle='dashed',
#                 label=f'B2-Harm. {harm}')

# ax5.set_title(f'Resolving Power @ {int(SlitSize[0]*1000)} µm ExitSlit')
# ax5.set_xlabel('Energy [eV]')
# ax5.set_ylabel(r'$\frac{E}{\Delta E}$ [a.u.]')
# ax5.legend(loc='best')
# ax5.set_xlim(x_range)
# ax5.minorticks_on()
# ax5.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# # Flux Density
# ax6 = axs[1, 1]

# for ind,harm in enumerate(harms):
#     Emin_harm = undulator_3[f'Energy{harm}[eV]'].min()
#     Emax_harm = undulator_3[f'Energy{harm}[eV]'].max()
#     filtered_df = BL_df[(BL_df['PhotonEnergy'] >= Emin_harm) & (BL_df['PhotonEnergy'] <= Emax_harm)]
#     foc_area = (filtered_df['VerticalFocusFWHM']*filtered_df['HorizontalFocusFWHM'])*1000
#     ax6.plot(filtered_df['PhotonEnergy'],
#              filtered_df[f'PhotonFlux{harm}']/foc_area,
#              color=colors[ind], linestyle='solid',
#              label=f'B3-Harm. {harm}')
#     Emin_harm = undulator_2[f'Energy{harm}[eV]'].min()
#     Emax_harm = undulator_2[f'Energy{harm}[eV]'].max()
#     filtered_df = BL_df_2[(BL_df_2['PhotonEnergy'] >= Emin_harm) & (BL_df_2['PhotonEnergy'] <= Emax_harm)]
#     foc_area = (filtered_df['VerticalFocusFWHM']*filtered_df['HorizontalFocusFWHM'])*1000
#     ax6.plot(filtered_df['PhotonEnergy'],
#              filtered_df[f'PhotonFlux{harm}']/foc_area,
#                 color=color_B2[ind], linestyle='dashed',
#                 label=f'B2-Harm. {harm}')
    
# ax6.set_title('Flux Density')
# ax6.set_xlabel('Energy [eV]')
# ax6.set_ylabel('Photons flux per µm²')
# ax6.legend(loc='best')
# ax6.set_xlim(x_range)
# ax6.minorticks_on()
# ax6.set_yscale('log')
# ax6.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')

# # Horizontal Focus Size
# ax7 = axs[2, 0]
# ax7.plot(mov_av(BL_df['PhotonEnergy'], window),
#          mov_av(BL_df['HorizontalFocusFWHM']*1000, window),
#          label='B3', color='purple', linestyle='solid')

# ax7.plot(mov_av(BL_df_2['PhotonEnergy'], window),
#          mov_av(BL_df_2['HorizontalFocusFWHM']*1000, window),
#          label='B2', color='violet', linestyle='dashed')

# ax7.set_title('Horizontal Focus Size')
# ax7.set_xlabel('Energy [eV]')
# ax7.set_ylabel('[µm]')
# ax7.set_ylim(0.01, 10.5)
# ax7.set_yscale('log')
# ax7.set_xlim(x_range)
# ax7.minorticks_on()
# ax7.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')
# ax7.yaxis.set_major_formatter(ScalarFormatter())
# ax7.ticklabel_format(style='plain', axis='y')
# ax7.legend(loc='best')
# # Vertical Focus Size
# ax8 = axs[2, 1]

# ax8.plot(mov_av(BL_df['PhotonEnergy'], window),
#          mov_av(BL_df['VerticalFocusFWHM']*1000, window),
#          label='B3', color='brown', linestyle='solid')

# ax8.plot(mov_av(BL_df_2['PhotonEnergy'], window),
#          mov_av(BL_df_2['VerticalFocusFWHM']*1000, window),
#          label='B2', color='peru', linestyle='dashed')

# ax8.set_title('Vertical Focus Size')
# ax8.set_xlabel('Energy [eV]')
# ax8.set_ylabel('[µm]')
# ax8.set_xlim(x_range)
# ax8.set_ylim(0.01, 10.5)
# ax8.set_yscale('log')
# ax8.minorticks_on()
# ax8.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')
# ax8.yaxis.set_major_formatter(ScalarFormatter())
# ax8.ticklabel_format(style='plain', axis='y')
# ax8.legend(loc='best')




