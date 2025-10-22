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
colors = ['red', 'blue', 'green']
color_B2 = ['salmon', 'royalblue', 'lime']

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

ax1.plot(E, Ir, 'orange', label='Ir', alpha=0.5)
ax1.plot(E, Cr, 'blue', label='Cr', alpha=0.5)
ax1.plot(E, B4C, 'red', label='B4C', alpha=0.5)
ax1.plot(E, IrCrB4C, 'black', label='IrCrB4C', linewidth=3)

ax1.set_title('Mirror Coating Reflectivity @ 'f'{theta}° incident angle')
ax1.set_xlabel('Energy [eV]')
ax1.set_ylabel('Reflectivity [a.u.]')
ax1.legend()
ax1.set_xlim(x_range)
ax1.minorticks_on()
ax1.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')



ax3 = axs[0]

window = 20



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
    
ax3.set_yscale('log')
ax3.set_ylim((1e11,4e15))
ax3.set_xlim(x_range)
ax3.set_xlabel('Energy [eV]')
ax3.set_ylabel('Ph/s/0.3A/0.1%BW')
ax3.set_title('IVU28 @ BESSY III vs CPMU20 @ BESSY II')

custom_lines = [
    Line2D([0], [0], color=colors[0], linestyle='solid', lw=2),
    Line2D([0], [0], color=color_B2[0], linestyle='dashed', lw=2),
]

ax3.legend(custom_lines, ['B3 - solid lines', 'B2 - dashed lines'], loc='best')

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


ax3.plot(mov_av(BL_df['PhotonEnergy'], window), 
             mov_av(BL_df['Bandwidth']*1000, window),
             linestyle='solid',
             label=f'B3 - nano focus',
             color='blue',
             linewidth=3,)

ax3.plot(mov_av(BL_df_micro['PhotonEnergy'], window), 
             mov_av(BL_df_micro['Bandwidth']*1000, window),
             linestyle='solid',
             label=f'B3 - micro focus', 
             color='orange',
             linewidth=3,)

ax3.plot(mov_av(BL_df_2['PhotonEnergy'], window), 
             mov_av(BL_df_2['Bandwidth']*1000, window),
             linestyle='solid',
             label=f'B2', 
             color='lime')



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
ls = ['solid', 'dashed', 'dotted']
for ind,harm in enumerate(harms):
    Emin_harm = undulator_3[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_3[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df[(BL_df['PhotonEnergy'] >= Emin_harm) & (BL_df['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(mov_av(filtered_df['PhotonEnergy'], window), 
             mov_av(filtered_df[f'PhotonFlux{harm}'], window),
             color='blue', linestyle=ls[ind], linewidth=3,
             label=f'B3-nano')

for ind,harm in enumerate(harms):
    Emin_harm = undulator_3[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_3[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df_micro[(BL_df_micro['PhotonEnergy'] >= Emin_harm) & (BL_df_micro['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(mov_av(filtered_df['PhotonEnergy'], window), 
             mov_av(filtered_df[f'PhotonFlux{harm}'], window),
             color='orange', linestyle=ls[ind], linewidth=3,
             label=f'B3-micro')
    
for ind,harm in enumerate(harms):    
    Emin_harm = undulator_2[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_2[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df_2[(BL_df_2['PhotonEnergy'] >= Emin_harm) & (BL_df_2['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(mov_av(filtered_df['PhotonEnergy'], window), 
                mov_av(filtered_df[f'PhotonFlux{harm}'], window),
                color='lime', linestyle=ls[ind],
                label=f'B2-Harm. {harm}')
    

ax4.set_title('Flux at Focus')
ax4.set_xlabel('Energy [eV]')
ax4.set_ylabel('Photon flux [ph/s/300 mA/TBW]')

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


###################################################
fig, (axs) = plt.subplots(1, 2, figsize=(20, 7))
fig.suptitle('Comparison SoTeXS @ BESSY II and BESSY III, 2400 l/mm')


# Resolving Power
ax3 = axs[0]

window = 10


ax3.plot(mov_av(BL_df['PhotonEnergy'], window), 
             mov_av(BL_df['PhotonEnergy']/BL_df['Bandwidth'], window),
             linestyle='solid',
             label=f'B3 - nano focus',
             color='blue',
             linewidth=3,)

ax3.plot(mov_av(BL_df_micro['PhotonEnergy'], window), 
             mov_av(BL_df_micro['PhotonEnergy']/BL_df_micro['Bandwidth'], window),
             linestyle='solid',
             label=f'B3 - micro focus', 
             color='orange',
             linewidth=3,)

window=50
ax3.plot(mov_av(BL_df_2['PhotonEnergy'], window), 
             mov_av(BL_df_2['PhotonEnergy']/BL_df_2['Bandwidth'], window),
             linestyle='solid',
             label=f'B2', 
             color='lime')



ax3.set_title(f'Resolving Power @{int(SlitSize[0]*1000)} µm ExitSlit')
ax3.set_xlabel('Energy [eV]')
ax3.set_ylabel('Resolving Power [a.u.]')
ax3.legend(loc='best')
ax3.set_xlim(x_range)
ax3.set_ylim(5000, 20000)
ax3.minorticks_on()
ax3.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# BEAMLINE FLUX CURVE
ax4 = axs[1]
window = 1
ls = ['solid', 'dashed', 'dotted']
for ind,harm in enumerate(harms):
    Emin_harm = undulator_3[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_3[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df[(BL_df['PhotonEnergy'] >= Emin_harm) & (BL_df['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(mov_av(filtered_df['PhotonEnergy'], window), 
             mov_av(filtered_df[f'PhotonFlux{harm}'], window),
             color='blue', linestyle=ls[ind], linewidth=3,
             label=f'B3-nano')

for ind,harm in enumerate(harms):
    Emin_harm = undulator_3[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_3[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df_micro[(BL_df_micro['PhotonEnergy'] >= Emin_harm) & (BL_df_micro['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(mov_av(filtered_df['PhotonEnergy'], window), 
             mov_av(filtered_df[f'PhotonFlux{harm}'], window),
             color='orange', linestyle=ls[ind], linewidth=3,
             label=f'B3-micro')
    
for ind,harm in enumerate(harms):    
    Emin_harm = undulator_2[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_2[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df_2[(BL_df_2['PhotonEnergy'] >= Emin_harm) & (BL_df_2['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(mov_av(filtered_df['PhotonEnergy'], window), 
                mov_av(filtered_df[f'PhotonFlux{harm}'], window),
                color='lime', linestyle=ls[ind],
                label=f'B2-Harm. {harm}')
    

ax4.set_title('Flux at Focus')
ax4.set_xlabel('Energy [eV]')
ax4.set_ylabel('Photon flux [ph/s/300 mA/TBW]')

ax4.set_xlim(x_range)
ax4.minorticks_on()
ax4.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')
ax4.set_ylim((10e9,1e15))
ax4.set_yscale('log')

# Save the the figure
plt.tight_layout()
plt.savefig('plot/talk/SoTeXS_2400_comparison_3.png')
# plt.show()
plt.close()
