import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path
import xrt.backends.raycing.materials as rm
 
from raypyng.postprocessing import PostProcessAnalyzed
from helper_lib import get_reflectivity

from parameter import HRRIXS_SlitSize as SlitSize
from parameter import HRRIXS_undulator as undulator_df

##############################################################
# LOAD IN DATA

# HR-RIXS V1:
BL_file_path = os.path.join('RAYPy_Simulation_HRRIXS_91m_1', 'DetectorAtFocus_RawRaysOutgoing.csv')
BL_df = pd.read_csv(BL_file_path)


# HR-RIXS V2:
BL1_file_path = os.path.join('RAYPy_Simulation_HRRIXS_91m_2', 'DetectorAtFocus_RawRaysOutgoing.csv')
BL1_df = pd.read_csv(BL1_file_path)

# HR-RIXS V2:
BL2_file_path = os.path.join('RAYPy_Simulation_HRRIXS_91m_3', 'DetectorAtFocus_RawRaysOutgoing.csv')
BL2_df = pd.read_csv(BL2_file_path)


##############################################################
# PLOTTING AND ANALYSIS
# Create the Main figure
fig, (axs) = plt.subplots(4, 2, figsize=(20, 15))
fig.suptitle('Comparison HR-RIXS 91 m dev. versions', size=14)
x_range = [100, 2150]

# Smoothing the data
window = 10
step = 1

BL_df_smoothed  = BL_df.rolling(window=window, step=step).mean()   
BL1_df_smoothed = BL1_df.rolling(window=window, step=step).mean()
BL2_df_smoothed = BL2_df.rolling(window=window, step=step).mean()
# BL3_df_smoothed = BL3_df.rolling(window=window, step=step).mean()


# Define color for harms
colors = {1: 'blue', 3: 'red', 5: 'green', 7: 'orange', 9: 'purple', 11: 'brown', 13: 'pink', 15: 'cyan'}


# Define Linestyles for vert., hor_M1_Para, and hor_M1M3_Para
vert            = 'solid'
hor_M1_Para     = 'dotted'
hor_M1M3_Para   = 'dashed'

# MIRROR REFLECTIVITY
ax1 = axs[0, 0]
# Coatings:
de = 38.9579-30.0000
table = 'Henke'
theta = 0.75
E = np.arange(50, 2150, de)
Au  = rm.Material('Au',  rho=19.32, kind='mirror',table=table)
Pt  = rm.Material('Pt',  rho=21.45, kind='mirror',table=table)
Rh  = rm.Material('Rh',  rho=12.41, kind='mirror',table=table)
Ru  = rm.Material('Ru',  rho=12.37, kind='mirror',table=table)  
Cr  = rm.Material('Cr',  rho=7.15,  kind='mirror',table=table) 
Ir  = rm.Material('Ir',  rho=22.56, kind='mirror',table=table)  
Pd  = rm.Material('Pd',  rho=12.02, kind='mirror',table=table)

B4C = rm.Material('C', rho=2.52,  kind='mirror',  table=table)

IrCrB4C = rm.Multilayer(tLayer=B4C, tThickness=40,
                        bLayer=Cr, bThickness=60, 
                        nPairs=1, substrate=Ir)

Au, _ = get_reflectivity(Au, E=E, theta=theta)
Pt, _ = get_reflectivity(Pt, E=E, theta=theta)
Ru, _ = get_reflectivity(Ru, E=E, theta=theta)
Rh, _ = get_reflectivity(Rh, E=E, theta=theta)
B4C, _ = get_reflectivity(B4C, E=E, theta=theta)
IrCrB4C, _ = get_reflectivity(IrCrB4C, E=E, theta=theta)
Cr, _ = get_reflectivity(Cr, E=E, theta=theta)
Ir, _ = get_reflectivity(Ir, E=E, theta=theta)
Pd, _ = get_reflectivity(Pd, E=E, theta=theta)

ax1.plot(E, Au, 'b', label='Au')
ax1.plot(E, Pt, 'r', label='Pt')
ax1.plot(E, IrCrB4C, 'y', label='IrCrB4C')
ax1.plot(E, Ru, 'g', label='Ru')
ax1.plot(E, Rh, 'c', label='Rh')
ax1.plot(E, Cr, 'm', label='Cr')
ax1.plot(E, Ir, 'k', label='Ir')
ax1.plot(E, Pd, 'orange', label='Pd')
ax1.plot(E, B4C, 'purple', label='B4C')


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

for harm in harms:
    ax2.plot(undulator_df[f'Energy{harm}[eV]'], undulator_df[f'Photons{harm}'], label=f'Harm. {harm}', color=colors[harm])
    
ax2.set_title('UE42.5 Flux curve')
ax2.set_xlabel('Energy [eV]')
ax2.set_ylabel('Photon flux [ph/s/300 mA/0.1% BW]')
ax2.legend(fontsize=12, loc='best')
ax2.set_xlim(x_range)
ax2.minorticks_on()
ax2.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# TRANSMITTED BANDWIDTH
ax3 = axs[1, 0]

for harm in harms:
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df_smoothed[(BL_df_smoothed['PhotonEnergy'] >= Emin_harm) & (BL_df_smoothed['PhotonEnergy'] <= Emax_harm)]
    ax3.plot(filtered_df['PhotonEnergy'], filtered_df['Bandwidth']*1000, label=f'Harm. {harm}', color=colors[harm], linestyle=vert)

for harm in harms:
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL1_df_smoothed[(BL1_df_smoothed['PhotonEnergy'] >= Emin_harm) & (BL1_df_smoothed['PhotonEnergy'] <= Emax_harm)]
    ax3.plot(filtered_df['PhotonEnergy'], filtered_df['Bandwidth']*1000, label=f'Harm. {harm}', color=colors[harm], linestyle=hor_M1_Para)

for harm in harms:
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL2_df_smoothed[(BL2_df_smoothed['PhotonEnergy'] >= Emin_harm) & (BL2_df_smoothed['PhotonEnergy'] <= Emax_harm)]
    ax3.plot(filtered_df['PhotonEnergy'], filtered_df['Bandwidth']*1000, label=f'Harm. {harm}', color=colors[harm], linestyle=hor_M1M3_Para)

# for harm in harms:
#     Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
#     Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
#     filtered_df = BL3_df_smoothed[(BL3_df_smoothed['PhotonEnergy'] >= Emin_harm) & (BL3_df_smoothed['PhotonEnergy'] <= Emax_harm)]
#     ax3.plot(filtered_df['PhotonEnergy'], filtered_df['Bandwidth']*1000, label=f'Harm. {harm}', color=colors[harm], linestyle='dashdot')

ax3.set_title(f'Transmitted Bandwidth @ {int(SlitSize[0]*1000)} µm ExitSlit')
ax3.set_xlabel('Energy [eV]')
ax3.set_ylabel('Transmitted bandwidth [meV]')
# ax3.legend(loc='best', fontsize=12)
ax3.set_xlim(x_range)
ax3.minorticks_on()
ax3.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# BEAMLINE FLUX CURVE
ax4 = axs[1, 1]

for harm in harms:
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df_smoothed[(BL_df_smoothed['PhotonEnergy'] >= Emin_harm) & (BL_df_smoothed['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(filtered_df['PhotonEnergy'], filtered_df[f'PhotonFlux{harm}']/250, label=f'Harm. {harm}', color=colors[harm], linestyle=vert)

for harm in harms:
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL1_df_smoothed[(BL1_df_smoothed['PhotonEnergy'] >= Emin_harm) & (BL1_df_smoothed['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(filtered_df['PhotonEnergy'], filtered_df[f'PhotonFlux{harm}']/250, label=f'Harm. {harm}', color=colors[harm], linestyle=hor_M1_Para)

for harm in harms:
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL2_df_smoothed[(BL2_df_smoothed['PhotonEnergy'] >= Emin_harm) & (BL2_df_smoothed['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(filtered_df['PhotonEnergy'], filtered_df[f'PhotonFlux{harm}']/250, label=f'Harm. {harm}', color=colors[harm], linestyle=hor_M1M3_Para)

# for harm in harms:
#     Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
#     Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
#     filtered_df = BL3_df_smoothed[(BL3_df_smoothed['PhotonEnergy'] >= Emin_harm) & (BL3_df_smoothed['PhotonEnergy'] <= Emax_harm)]
#     ax4.plot(filtered_df['PhotonEnergy'], filtered_df[f'PhotonFlux{harm}'], label=f'Harm. {harm}', color=colors[harm], linestyle='dashdot')

ax4.set_title('Flux curve')
ax4.set_xlabel('Energy [eV]')
ax4.set_ylabel('Photon flux [ph/s/300 mA/0.1% BW]')
# ax4.legend(loc='best', fontsize=12)
ax4.set_xlim(x_range)
ax4.minorticks_on()
ax4.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# RESOLVING POWER
ax5 = axs[2, 0]

for harm in harms:
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df_smoothed[(BL_df_smoothed['PhotonEnergy'] >= Emin_harm) & (BL_df_smoothed['PhotonEnergy'] <= Emax_harm)]
    ax5.plot(filtered_df['PhotonEnergy'], (filtered_df[f'PhotonEnergy']/filtered_df[f'Bandwidth']), label=f'Harm. {harm}', color=colors[harm], linestyle=vert)

for harm in harms:
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL1_df_smoothed[(BL1_df_smoothed['PhotonEnergy'] >= Emin_harm) & (BL1_df_smoothed['PhotonEnergy'] <= Emax_harm)]
    ax5.plot(filtered_df['PhotonEnergy'], (filtered_df[f'PhotonEnergy']/filtered_df[f'Bandwidth']), label=f'Harm. {harm}', color=colors[harm], linestyle=hor_M1_Para)

for harm in harms:
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL2_df_smoothed[(BL2_df_smoothed['PhotonEnergy'] >= Emin_harm) & (BL2_df_smoothed['PhotonEnergy'] <= Emax_harm)]
    ax5.plot(filtered_df['PhotonEnergy'], (filtered_df[f'PhotonEnergy']/filtered_df[f'Bandwidth']), label=f'Harm. {harm}', color=colors[harm], linestyle=hor_M1M3_Para)

# for harm in harms:
#     Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
#     Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
#     filtered_df = BL3_df_smoothed[(BL3_df_smoothed['PhotonEnergy'] >= Emin_harm) & (BL3_df_smoothed['PhotonEnergy'] <= Emax_harm)]
#     ax5.plot(filtered_df['PhotonEnergy'], (filtered_df[f'PhotonEnergy']/filtered_df[f'Bandwidth']), label=f'Harm. {harm}', color=colors[harm], linestyle='dashdot')

ax5.set_title(f'Resolving Power @ {int(SlitSize[0]*1000)} µm ExitSlit')
ax5.set_xlabel('Energy [eV]')
ax5.set_ylabel(r'$\frac{E}{\Delta E}$ [a.u.]')
# ax5.legend(loc='best', fontsize=12)
ax5.set_xlim(x_range)
ax5.minorticks_on()
ax5.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# Flux Density
ax6 = axs[2, 1]
for harm in harms:
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df_smoothed[(BL_df_smoothed['PhotonEnergy'] >= Emin_harm) & (BL_df_smoothed['PhotonEnergy'] <= Emax_harm)]
    foc_area = (filtered_df['VerticalFocusFWHM']*filtered_df['HorizontalFocusFWHM'])*1000  # in µm²
    ax6.plot(filtered_df['PhotonEnergy'],(filtered_df[f'PhotonFlux{harm}']/250)/foc_area, label=f'Harm. {harm}', color=colors[harm], linestyle=vert)

for harm in harms:
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL1_df_smoothed[(BL1_df_smoothed['PhotonEnergy'] >= Emin_harm) & (BL1_df_smoothed['PhotonEnergy'] <= Emax_harm)]
    foc_area = (filtered_df['VerticalFocusFWHM']*filtered_df['HorizontalFocusFWHM'])*1000  # in µm²
    ax6.plot(filtered_df['PhotonEnergy'],(filtered_df[f'PhotonFlux{harm}']/250)/foc_area, label=f'Harm. {harm}', color=colors[harm], linestyle=hor_M1_Para)

for harm in harms:
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL2_df_smoothed[(BL2_df_smoothed['PhotonEnergy'] >= Emin_harm) & (BL2_df_smoothed['PhotonEnergy'] <= Emax_harm)]
    foc_area = (filtered_df['VerticalFocusFWHM']*filtered_df['HorizontalFocusFWHM'])*1000  # in µm²
    ax6.plot(filtered_df['PhotonEnergy'],(filtered_df[f'PhotonFlux{harm}']/250)/foc_area, label=f'Harm. {harm}', color=colors[harm], linestyle=hor_M1M3_Para)

# for harm in harms:
#     Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
#     Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
#     filtered_df = BL3_df_smoothed[(BL3_df_smoothed['PhotonEnergy'] >= Emin_harm) & (BL3_df_smoothed['PhotonEnergy'] <= Emax_harm)]
#     foc_area = (filtered_df['VerticalFocusFWHM']*filtered_df['HorizontalFocusFWHM'])*1000  # in µm²
#     ax6.plot(filtered_df['PhotonEnergy'],filtered_df[f'PhotonFlux{harm}']/foc_area, label=f'Harm. {harm}', color=colors[harm], linestyle='dashdot')

ax6.set_title('Flux Density')
ax6.set_xlabel('Energy [eV]')
ax6.set_ylabel('Photons flux per µm²')
# ax6.legend(loc='best', fontsize=12)
ax6.set_xlim(x_range)
ax6.minorticks_on()
ax6.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# Horizontal Focus Size
ax7 = axs[3, 0]

ax7.plot(BL_df_smoothed['PhotonEnergy'], BL_df_smoothed['HorizontalFocusFWHM']*1000, label='Horizontal Focus Size', color='red', linestyle=vert)
ax7.plot(BL1_df_smoothed['PhotonEnergy'], BL1_df_smoothed['HorizontalFocusFWHM']*1000, label='Horizontal Focus Size', color='orangered', linestyle=hor_M1_Para)
ax7.plot(BL2_df_smoothed['PhotonEnergy'], BL2_df_smoothed['HorizontalFocusFWHM']*1000, label='Horizontal Focus Size', color='darkred', linestyle=hor_M1M3_Para)
# ax7.plot(BL3_df_smoothed['PhotonEnergy'], BL3_df_smoothed['HorizontalFocusFWHM']*1000, label='Horizontal Focus Size', color='firebrick', linestyle='dashdot')

ax7.set_title('Horizontal Focus Size')
ax7.set_xlabel('Energy [eV]')
ax7.set_ylabel('[µm]')
ax7.set_xlim(x_range)
ax7.minorticks_on()
ax7.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')

# Vertical Focus Size
ax8 = axs[3, 1]

ax8.plot(BL_df_smoothed['PhotonEnergy'], BL_df_smoothed['VerticalFocusFWHM']*1000, label='Vertical Focus Size', color='green', linestyle=vert)
ax8.plot(BL1_df_smoothed['PhotonEnergy'], BL1_df_smoothed['VerticalFocusFWHM']*1000, label='Vertical Focus Size', color='lightgreen', linestyle=hor_M1_Para)
ax8.plot(BL2_df_smoothed['PhotonEnergy'], BL2_df_smoothed['VerticalFocusFWHM']*1000, label='Vertical Focus Size', color='darkgreen', linestyle=hor_M1M3_Para)
# ax8.plot(BL3_df_smoothed['PhotonEnergy'], BL3_df_smoothed['VerticalFocusFWHM']*1000, label='Vertical Focus Size', color='limegreen', linestyle='dashdot')

ax8.set_title('Vertical Focus Size')
ax8.set_xlabel('Energy [eV]')
ax8.set_ylabel('[µm]')
ax8.set_xlim(x_range)
ax8.minorticks_on()
ax8.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')

# Replace the legend with a textbox
fig.text(
    0.19, 0.7,
    'HR-RIXS V1 (solid lines)\n'
    'HR-RIXS V2 (dotted lines)\n'
    'HR-RIXS V3 (dashed lines)',
    fontsize=9, ha='right', va='top',
    bbox=dict(facecolor='white', alpha=0.8, edgecolor='grey')
)

##############################################################
# SAVING
# Ensure the "plot" folder exists
plot_folder = 'plot'
if not os.path.exists(plot_folder):
    os.makedirs(plot_folder)

# Save the the figure
plt.tight_layout()
# plt.savefig('plot/Comparison HR-RIXS versions with UE42p5.pdf')
plt.show()