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
BL_file_path = os.path.join('../characterization/RAYPy_Simulation_elisa_2400', 'DetectorAtFocus_RawRaysOutgoing.csv')
BL_df = pd.read_csv(BL_file_path)

# Read CSV-File of the Beamline Simulation
BL_file_path = os.path.join('../characterization/RAYPy_Simulation_elisa_1200', 'DetectorAtFocus_RawRaysOutgoing.csv')
BL_df_1200 = pd.read_csv(BL_file_path)
BL_df_1200_5 = BL_df_1200[BL_df_1200['PG.cFactor'] == 5]
BL_df_1200 = BL_df_1200[BL_df_1200['PG.cFactor'] == 2.25]

# Read CSV-File of the Beamline Simulation
BL_file_path = os.path.join('RAYPy_Simulation_2400', 'DetectorAtFocus_RawRaysOutgoing.csv')
BL_df_2 = pd.read_csv(BL_file_path)
BL_df_2 = BL_df_2[BL_df_2['PhotonEnergy'] <= 5800]
# Read CSV-File of the Beamline Simulation
BL_file_path = os.path.join('RAYPy_Simulation_1200_Pt', 'DetectorAtFocus_RawRaysOutgoing.csv')
BL_df_2_1200 = pd.read_csv(BL_file_path)
BL_df_2_1200 = BL_df_2_1200[BL_df_2_1200['PhotonEnergy'] <= 2000]

harms=[1,3,5]
x_range = [200, 6200]

##############################################################
# PLOTTING AND ANALYSIS
plt.rcParams.update({'font.size': 15})  # Change 14 to any size you prefer
# Create the Main figure
fig, (axs) = plt.subplots(1, 2, figsize=(20, 7))
fig.suptitle('Comparison Liquid Interface @ BESSY III and SoTeXS @ BESSY II')

# MIRROR REFLECTIVITY
ax1 = axs[0]
# Coatings:
de = 0.01
table = 'Henke'
theta = 0.4
E = np.arange(x_range[0], x_range[-1], de)
Ir  = rm.Material('Ir',  rho=22.56, kind='mirror',table=table)
Cr  = rm.Material('Cr',  rho=7.15,  kind='mirror',table=table)
B4C = rm.Material('C',   rho=2.52,  kind='mirror',table=table)
IrCrB4C = rm.Multilayer(tLayer=B4C, tThickness=40, 
                        bLayer=Cr, bThickness=60, 
                        nPairs=1, substrate=Ir)
Pt = rm.Material('Pt', rho=21.45, kind='mirror',table=table)

Ir, _ = get_reflectivity(Ir, E=E, theta=theta)
Cr, _ = get_reflectivity(Cr, E=E, theta=theta)
B4C, _ = get_reflectivity(B4C, E=E, theta=theta)
IrCrB4C, _ = get_reflectivity(IrCrB4C, E=E, theta=theta)
Pt, _ = get_reflectivity(Pt, E=E, theta=theta)

ax1.plot(E, Ir, 'gold', label='Ir', alpha=0.5)
ax1.plot(E, Cr, 'blue', label='Cr', alpha=0.5)
ax1.plot(E, B4C, 'red', label='B4C', alpha=0.5)
ax1.plot(E, IrCrB4C, 'black', label='IrCrB4C', linewidth=2)
ax1.plot(E, Pt, 'grey', label='Pt', alpha=1, linewidth=2)

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
             label=f'B3-Harm. {harm}')
for ind,harm in enumerate(harms):
    ax3.plot(undulator_2[f'Energy{harm}[eV]'], 
             undulator_2[f'Photons{harm}'],
             color=colors[ind], linestyle='solid',
             label=f'B2-Harm. {harm}')
    
ax3.legend()
ax3.set_yscale('log')
ax3.set_xlabel('Energy [eV]')
ax3.set_ylabel('Ph/s/0.3A/0.1%BW')
ax3.set_xlim(x_range)
ax3.set_ylim(9e7, 5e15)
ax3.set_title('IVUE42 @ BESSY III vs CPMU21 @ BESSY II')

# SAVING
# Ensure the "plot" folder exists
plot_folder = 'plot'
if not os.path.exists(plot_folder):
    os.makedirs(plot_folder)

# Save the the figure
plt.tight_layout()
plt.savefig('plot/talk/LiquidInterface_2400_comparison_1.png')
# plt.show()
plt.close()





###################################################
fig, (axs) = plt.subplots(1, 2, figsize=(20, 7))
fig.suptitle('Comparison SoTeXS @ BESSY II and BESSY III, 2400 l/mm')


# TRANSMITTED BANDWIDTH
ax3 = axs[0]

window = 30

ax3.plot(mov_av(BL_df['PhotonEnergy'], window), 
             mov_av(BL_df['Bandwidth']*1000, window),
             linestyle='solid',
             label=f'B3 - 2400 l/mm',
             color='royalblue')

ax3.plot(mov_av(BL_df_1200['PhotonEnergy'], window), 
             mov_av(BL_df_1200['Bandwidth']*1000, window),
             linestyle='solid',
             label=f'B3 - 1200 l/mm - cff=2.25',
             color='cyan')

ax3.plot(mov_av(BL_df_2['PhotonEnergy'], window), 
             mov_av(BL_df_2['Bandwidth']*1000, window),
             linestyle='solid',
             label=f'B2 - 2400l/mm', 
             color='green')

ax3.plot(mov_av(BL_df_2_1200['PhotonEnergy'], window), 
             mov_av(BL_df_2_1200['Bandwidth']*1000, window),
             linestyle='solid',
             label=f'B2 - 1200l/mm - cff=2.25', 
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
for ind,harm in enumerate(harms):
    Emin_harm = undulator_3[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_3[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df[(BL_df['PhotonEnergy'] >= Emin_harm) & (BL_df['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(mov_av(filtered_df['PhotonEnergy'], window), 
             mov_av(filtered_df[f'PhotonFlux{harm}'], window),
             color='royalblue', linestyle='solid',
             label=f'B3 2400 l/mm')

for ind,harm in enumerate([1]):
    Emin_harm = undulator_3[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_3[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df_1200[(BL_df_1200['PhotonEnergy'] >= Emin_harm) & (BL_df_1200['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(mov_av(filtered_df['PhotonEnergy'], window), 
             mov_av(filtered_df[f'PhotonFlux{harm}'], window),
             color='cyan', linestyle='solid',
             label=f'B3 1200 l/mm')
    
    
for ind,harm in enumerate(harms):    
    Emin_harm = undulator_2[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_2[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df_2[(BL_df_2['PhotonEnergy'] >= Emin_harm) & (BL_df_2['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(mov_av(filtered_df['PhotonEnergy'], window), 
                mov_av(filtered_df[f'PhotonFlux{harm}'], window),
                color='green', linestyle='solid',
                label=f'B2-Harm. {harm}')

for ind,harm in enumerate([1]):
    Emin_harm = undulator_2[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_2[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df_2_1200[(BL_df_2_1200['PhotonEnergy'] >= Emin_harm) & (BL_df_2_1200['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(mov_av(filtered_df['PhotonEnergy'], window), 
             mov_av(filtered_df[f'PhotonFlux{harm}'], window),
             color='lime', linestyle='solid',
             label=f'B2 1200 l/mm')    

ax4.set_title('Flux at Focus')
ax4.set_xlabel('Energy [eV]')
ax4.set_ylabel('Photon flux [ph/s/300 mA/TBW]')
custom_lines = [
    Line2D([0], [0], color='royalblue', linestyle='solid', lw=2),
    Line2D([0], [0], color='cyan', linestyle='solid', lw=2),
    Line2D([0], [0], color='green', linestyle='solid', lw=2),
    Line2D([0], [0], color='lime', linestyle='solid', lw=2)
]

ax4.legend(custom_lines, ['B3 - 2400 l/mm', 'B3 - 1200 l/mm', 'B2 - 2400 l/mm', 'B2 - 1200 l/mm'], loc='best')
ax4.set_xlim(x_range)
ax4.minorticks_on()
ax4.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')
ax4.set_ylim((1e7,1e14))
ax4.set_yscale('log')

# Save the the figure
plt.tight_layout()
plt.savefig('plot/talk/LiquidInterface_2400_comparison_2.png')
# plt.show()
plt.close()




###################################################
fig, (axs) = plt.subplots(1, 2, figsize=(20, 7))
fig.suptitle('Comparison SoTeXS @ BESSY II and BESSY III, 2400 l/mm')


# TRANSMITTED BANDWIDTH
ax3 = axs[0]

window = 30


ax3.plot(mov_av(BL_df['PhotonEnergy'], window), 
             mov_av(BL_df['PhotonEnergy']/BL_df['Bandwidth'], window),
             linestyle='solid',
             label=f'B3 - 2400 l/mm',
             color='royalblue')

ax3.plot(mov_av(BL_df_1200['PhotonEnergy'], window), 
             mov_av(BL_df_1200['PhotonEnergy']/BL_df_1200['Bandwidth'], window),
             linestyle='solid',
             label=f'B3 - 1200 l/mm - cff=2.25',
             color='cyan')

ax3.plot(mov_av(BL_df_1200_5['PhotonEnergy'], window), 
             mov_av(BL_df_1200_5['PhotonEnergy']/BL_df_1200_5['Bandwidth'], window),
             linestyle='solid',
             label=f'B3 - 1200 l/mm - cff=5',
             color='navy')

ax3.plot(mov_av(BL_df_2['PhotonEnergy'], window), 
             mov_av(BL_df_2['PhotonEnergy']/BL_df_2['Bandwidth'], window),
             linestyle='solid',
             label=f'B2 - 2400l/mm', 
             color='green')

ax3.plot(mov_av(BL_df_2_1200['PhotonEnergy'], window), 
             mov_av(BL_df_2_1200['PhotonEnergy']/BL_df_2_1200['Bandwidth'], window),
             linestyle='solid',
             label=f'B2 - 1200l/mm - cff=2.25', 
             color='lime')


ax3.set_title(f'Resolving Power @{int(SlitSize[0]*1000)} µm ExitSlit')
ax3.set_xlabel('Energy [eV]')
ax3.set_ylabel('Resolving Power [a.u.]')
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
             color='royalblue', linestyle='solid',
             label=f'B3 2400 l/mm')

for ind,harm in enumerate([1]):
    Emin_harm = undulator_3[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_3[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df_1200[(BL_df_1200['PhotonEnergy'] >= Emin_harm) & (BL_df_1200['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(mov_av(filtered_df['PhotonEnergy'], window), 
             mov_av(filtered_df[f'PhotonFlux{harm}'], window),
             color='cyan', linestyle='solid',
             label=f'B3 1200 l/mm cff 2.25')
    
for ind,harm in enumerate([1]):
    Emin_harm = undulator_3[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_3[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df_1200_5[(BL_df_1200_5['PhotonEnergy'] >= Emin_harm) & (BL_df_1200_5['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(mov_av(filtered_df['PhotonEnergy'], window), 
             mov_av(filtered_df[f'PhotonFlux{harm}'], window),
             color='navy', linestyle='solid',
             label=f'B3 1200 l/mm - cff 5')
    
    
for ind,harm in enumerate(harms):    
    Emin_harm = undulator_2[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_2[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df_2[(BL_df_2['PhotonEnergy'] >= Emin_harm) & (BL_df_2['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(mov_av(filtered_df['PhotonEnergy'], window), 
                mov_av(filtered_df[f'PhotonFlux{harm}'], window),
                color='green', linestyle='solid',
                label=f'B2-Harm. {harm}')

for ind,harm in enumerate([1]):
    Emin_harm = undulator_2[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_2[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df_2_1200[(BL_df_2_1200['PhotonEnergy'] >= Emin_harm) & (BL_df_2_1200['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(mov_av(filtered_df['PhotonEnergy'], window), 
             mov_av(filtered_df[f'PhotonFlux{harm}'], window),
             color='lime', linestyle='solid',
             label=f'B2 1200 l/mm')    

ax4.set_title('Flux at Focus')
ax4.set_xlabel('Energy [eV]')
ax4.set_ylabel('Photon flux [ph/s/300 mA/TBW]')
custom_lines = [
    Line2D([0], [0], color='royalblue', linestyle='solid', lw=2),
    Line2D([0], [0], color='cyan', linestyle='solid', lw=2),
    Line2D([0], [0], color='green', linestyle='solid', lw=2),
    Line2D([0], [0], color='lime', linestyle='solid', lw=2)
]

ax4.legend(custom_lines, ['B3 - 2400 l/mm', 'B3 - 1200 l/mm', 'B2 - 2400 l/mm', 'B2 - 1200 l/mm'], loc='best')
ax4.set_xlim(x_range)
ax4.minorticks_on()
ax4.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')
ax4.set_ylim((1e7,1e14))
ax4.set_yscale('log')

# Save the the figure
plt.tight_layout()
plt.savefig('plot/talk/LiquidInterface_2400_comparison_3.png')
# plt.show()
plt.close()




############# undulator
from pathlib import Path

fig, (ax) = plt.subplots(1, 1, figsize=(10, 7))

#######
undulator_file_path = os.path.abspath(
    os.path.join(Path(__file__).resolve().parents[4], 
                 'undulators',
                 'UndulatorFiles_BESSY_III',
                 'IVUE42-C.csv')
)
undulator_C = pd.read_csv(undulator_file_path)

#######
undulator_file_path = os.path.abspath(
    os.path.join(Path(__file__).resolve().parents[4], 
                 'undulators',
                 'UndulatorFiles_BESSY_III',
                 'IVUE42-HL.csv')
)
undulator_HL = pd.read_csv(undulator_file_path)

#######
undulator_file_path = os.path.abspath(
    os.path.join(Path(__file__).resolve().parents[4], 
                 'undulators',
                 'UndulatorFiles_BESSY_III',
                 'IVUE42-IN.csv')
)
undulator_IN = pd.read_csv(undulator_file_path)

#######
undulator_file_path = os.path.abspath(
    os.path.join(Path(__file__).resolve().parents[4], 
                 'undulators',
                 'UndulatorFiles_BESSY_III',
                 'IVUE42-VL.csv')
)
undulator_VL = pd.read_csv(undulator_file_path)

for ind,harm in enumerate(harms):
    ax.plot(undulator_C[f'Energy{harm}[eV]'], 
             undulator_C[f'Photons{harm}'],
             color='red', linestyle='solid',
             linewidth=5)
    ax.plot(undulator_HL[f'Energy{harm}[eV]'], 
             undulator_HL[f'Photons{harm}']*1,
             color='royalblue', linestyle='dashed',
             linewidth=4)
    ax.plot(undulator_IN[f'Energy{harm}[eV]'], 
             undulator_IN[f'Photons{harm}']*1,
             color='forestgreen', linestyle='dotted',
             linewidth=3)
    ax.plot(undulator_VL[f'Energy{harm}[eV]'], 
             undulator_VL[f'Photons{harm}']*1,
             color='orange', linestyle='dotted',
             linewidth=2)

def get_energy_range(df, harm):
    col = f'Energy{harm}[eV]'
    photon_col = f'Photons{harm}'
    if col in df.columns and df[photon_col].max() > 0:
        return f"{int(np.min(df[col]))} – {int(np.max(df[col]))}"
    else:
        return ""

# Create table data dynamically with safety for missing harmonics
table_data = [
    ['Circular',
     get_energy_range(undulator_C, 1),
     get_energy_range(undulator_C, 3),
     get_energy_range(undulator_C, 5),
     get_energy_range(undulator_C, 7)],

    ['Horizontal Linear',
     get_energy_range(undulator_HL, 1),
     get_energy_range(undulator_HL, 3),
     get_energy_range(undulator_HL, 5),
     get_energy_range(undulator_HL, 7)],

    ['Inclined',
     get_energy_range(undulator_IN, 1),
     get_energy_range(undulator_IN, 3),
     get_energy_range(undulator_IN, 5),
     get_energy_range(undulator_IN, 7)],

    ['Vertical Linear',
     get_energy_range(undulator_VL, 1),
     get_energy_range(undulator_VL, 3),
     get_energy_range(undulator_VL, 5),
     get_energy_range(undulator_VL, 7)]
]

# Add the table to the plot
table = ax.table(
    cellText=table_data,
    colLabels=['Polarization', 'Harm.1 [eV]', 'Harm.3 [eV]', 'Harm.5 [eV]', 'Harm.7 [eV]'],
    loc='lower left',
    cellLoc='center',
    colLoc='center'
)

# Optional styling
table.scale(0.8, 1.2)
table.auto_set_font_size(False)
table.set_fontsize(10)



custom_lines = [
    Line2D([0], [0], color='red', linestyle='solid', lw=2),
    Line2D([0], [0], color='royalblue', linestyle='solid', lw=2),
    Line2D([0], [0], color='forestgreen', linestyle='solid', lw=2),
    Line2D([0], [0], color='orange', linestyle='solid', lw=2)
]

ax.legend(custom_lines, ['Circular', 'Hor-Lin', 'Inclined', 'Ver Lin'], loc='best')

ax.set_yscale('log')
# ax.set_xscale('log')
ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Ph/s/0.3A/0.1%BW')
# ax.set_xlim(x_range)
ax.set_ylim(1e10, 1e16)
ax.set_title('IVUE42')
# Save the the figure
plt.tight_layout()
plt.savefig('plot/talk/LiquidInterface_undulator.png')
# plt.show()
plt.close()


