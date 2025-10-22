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
from parameter import SlitSize
from parameter import undulator as undulator_df
from parameter import energy

from raypyng.postprocessing import PostProcessAnalyzed

p = PostProcessAnalyzed()
mov_av = p.moving_average
##############################################################
# LOAD IN DATA

# Read CSV-File of the Beamline Simulation
BL_file_path = os.path.join('RAYPy_Simulation_coherence_horizontal', 'DetectorAtFocus_RawRaysOutgoing.csv')
BL_df_hor = pd.read_csv(BL_file_path)

BL_file_path = os.path.join('RAYPy_Simulation_coherence_vertical', 'DetectorAtFocus_RawRaysOutgoing.csv')
BL_df_ver = pd.read_csv(BL_file_path)

##############################################################
# PLOTTING AND ANALYSIS
plt.rcParams.update({'font.size': 13})  # Change 14 to any size you prefer
# Create the Main figure
fig, (axs) = plt.subplots(4, 2, figsize=(20, 15))
fig.suptitle('Signature5 - Coherence Imaging, 500 l/mm', size=16)
x_range = [energy[0], energy[-1]]
colors = ['royalblue', 'red', 'green']

# MIRROR REFLECTIVITY
ax1 = axs[0, 0]
# Coatings:
de = 0.01
table = 'Henke'
theta = 0.7
E = np.arange(energy[0], energy[-1], de)

Pt = rm.Material('Pt',  rho=21.45, kind='mirror',table=table)
Pt, _ = get_reflectivity(Pt, E=E, theta=theta)


ax1.plot(E, Pt, 'grey', label='IrCrB4C', linewidth=2)

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

for ind, harm in enumerate(harms):
    ax2.plot(undulator_df[f'Energy{harm}[eV]'],
             undulator_df[f'Photons{harm}'],
             color=colors[ind],
             label=f'Harm. {harm}')
    
ax2.set_title('Cryo IVUE31 Flux curve, Hor Lin polarization')
ax2.set_xlabel('Energy [eV]')
ax2.set_ylabel('Photon flux [ph/s/0.3A/0.1% BW]')
ax2.legend(loc='best')
ax2.set_xlim(x_range)
ax2.set_ylim((1e15, 4e15))

ax2.set_yscale('log')
ax2.minorticks_on()
ax2.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# TRANSMITTED BANDWIDTH
ax3 = axs[1, 0]

window = 1

# vertical
ax3.plot(mov_av(BL_df_ver['PhotonEnergy'], window), 
             mov_av(BL_df_ver['Bandwidth']*1000, window),
             label=f'Vertical',
             color='royalblue', linestyle='solid')
    
# horizontal
ax3.plot(mov_av(BL_df_hor['PhotonEnergy'], window),
             mov_av(BL_df_hor['Bandwidth']*1000, window),
             label=f'Horizontal',
             color=colors[ind], linestyle='dashed')


ax3.set_title(f'Transmitted Bandwidth @{int(SlitSize[0]*1000)} µm ExitSlit')
ax3.set_xlabel('Energy [eV]')
ax3.set_ylabel('Transmitted bandwidth [meV]')
ax3.set_xlim(x_range)
ax3.minorticks_on()
ax3.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')
ax3.legend(loc='lower right', ncol=2)


# BEAMLINE FLUX CURVE
ax4 = axs[1, 1]

# 2400
for ind, harm in enumerate(harms):
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df_ver[(BL_df_ver['PhotonEnergy'] >= Emin_harm) & (BL_df_ver['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(filtered_df['PhotonEnergy'],
             filtered_df[f'PhotonFlux{harm}'],
             label=f'Harm. {harm}',
             color=colors[ind], linestyle='solid')
    
# 2400
for ind, harm in enumerate(harms):
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df_hor[(BL_df_hor['PhotonEnergy'] >= Emin_harm) & (BL_df_hor['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(filtered_df['PhotonEnergy'],
             filtered_df[f'PhotonFlux{harm}'],
             label=f'Harm. {harm}',
             color=colors[ind], linestyle='dashed')

ax4.set_title('Flux at Focus')
ax4.set_xlabel('Energy [eV]')
ax4.set_ylabel('Photon flux [ph/s/300 mA/TBW]')
ax4.set_xlim(x_range)
ax4.minorticks_on()
ax4.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')
ax4.set_yscale('log')


custom_lines = [
    Line2D([0], [0], color='royalblue', linestyle='solid', lw=2),
    Line2D([0], [0], color='royalblue', linestyle='dashed', lw=2),
]

ax4.legend(custom_lines, ['Vertical - solid lines', 'Horizontal - dashed lines'], loc='best')
# RESOLVING POWER
ax5 = axs[2, 0]
window = 1

# Vertical
ax5.plot(mov_av(BL_df_ver['PhotonEnergy'], window),
         mov_av(BL_df_ver[f'PhotonEnergy']/BL_df_ver[f'Bandwidth'], window),
         color = 'royalblue', linestyle='solid',
         label='Vertical')

# Horizontal
ax5.plot(mov_av(BL_df_hor['PhotonEnergy'], window),
         mov_av(BL_df_hor[f'PhotonEnergy']/BL_df_hor[f'Bandwidth'], window),
         color = 'green', linestyle='dashed',
         label='Horizontal')

ax5.set_title(f'Resolving Power @ {int(SlitSize[0]*1000)} µm ExitSlit')
ax5.set_xlabel('Energy [eV]')
ax5.set_ylabel(r'$\frac{E}{\Delta E}$ [a.u.]')
ax5.set_xlim(x_range)
ax5.legend(loc='lower right')
ax5.minorticks_on()
ax5.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# Flux Density
ax6 = axs[2, 1]

# 1200
for ind, harm in enumerate(harms):
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df_ver[(BL_df_ver['PhotonEnergy'] >= Emin_harm) & (BL_df_ver['PhotonEnergy'] <= Emax_harm)]
    foc_area = (filtered_df['VerticalFocusFWHM']*filtered_df['HorizontalFocusFWHM'])*1000  # in µm²
    ax6.plot(filtered_df['PhotonEnergy'],
             filtered_df[f'PhotonFlux{harm}']/foc_area,
             label=f'Harm. {harm}', 
             color=colors[ind], linestyle='solid')
    
# 2400
for ind, harm in enumerate(harms):
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df_hor[(BL_df_hor['PhotonEnergy'] >= Emin_harm) & (BL_df_hor['PhotonEnergy'] <= Emax_harm)]
    foc_area = (filtered_df['VerticalFocusFWHM']*filtered_df['HorizontalFocusFWHM'])*1000  # in µm²
    ax6.plot(filtered_df['PhotonEnergy'],
             filtered_df[f'PhotonFlux{harm}']/foc_area,
             label=f'Harm. {harm}', 
             color=colors[ind], linestyle='dashed')

ax6.set_title('Flux Density')
ax6.set_xlabel('Energy [eV]')
ax6.set_ylabel('Photons flux per µm²')
ax6.set_xlim(x_range)
ax6.set_yscale('log')
ax6.minorticks_on()
ax6.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')

custom_lines = [
    Line2D([0], [0], color='royalblue', linestyle='solid', lw=2),
    Line2D([0], [0], color='royalblue', linestyle='dashed', lw=2),
]

ax6.legend(custom_lines, ['Vertical - solid lines', 'Horizontal - dashed lines'], loc='best')

# Focus Horizontal
ax7 = axs[3, 0]
focus_path = os.path.join('plot', 'horizontal_focus.csv')
focus = pd.read_csv(
    focus_path,
    sep='\t',        # columns separated by tabs
    decimal='.',     # use comma as decimal separator
    skiprows=1       # skip the first line (the 'sep=' line)
)
x = focus['DetectorAtFocus_OX'] * 1e3
y = focus['DetectorAtFocus_OY'] * 1e3

x_lim=(-5,5)#
y_lim=(-5,5)
size = 0.05

ax7.scatter(x,y, s=size, color='yellow', alpha=1)

ax7.set_facecolor('#002147')

ax7.set_xlim(x_lim)
ax7.set_ylim(y_lim)

ax7.set_xlabel('µm')
ax7.set_ylabel('µm')
# hor_foc = np.mean(BL_df_hor['HorizontalFocusFWHM']*1e3)
# ver_foc = np.mean(BL_df_hor['VerticalFocusFWHM']*1e3)
ax7.set_title(f'Horizontal Monochromator, Focus FWHM(HxV) {2.0:.1f} x {1.5:.1f} µm²')

# Focus Vertical
ax7 = axs[3, 1]
focus_path = os.path.join('plot', 'vertical_focus.csv')
focus = pd.read_csv(
    focus_path,
    sep='\t',        # columns separated by tabs
    decimal='.',     # use comma as decimal separator
    skiprows=1       # skip the first line (the 'sep=' line)
)
x = focus['DetectorAtFocus_OX'] * 1e3
y = focus['DetectorAtFocus_OY'] * 1e3


ax7.scatter(x,y, s=size, color='yellow', alpha=1)

ax7.set_facecolor('#002147')

ax7.set_xlim(x_lim)
ax7.set_ylim(y_lim)

ax7.set_xlabel('µm')
ax7.set_ylabel('µm')
hor_foc = np.mean(BL_df_hor['HorizontalFocusFWHM']*1e3)
ver_foc = np.mean(BL_df_hor['VerticalFocusFWHM']*1e3)
ax7.set_title(f'Vertical Monochromator, Focus FWHM(HxV) {2.2:.1f} x {2.0:.1f} µm²')

##############################################################
# SAVING
# Ensure the "plot" folder exists
plot_folder = 'plot'
if not os.path.exists(plot_folder):
    os.makedirs(plot_folder)

# Save the the figure
plt.tight_layout()
plt.savefig('plot/coherence.png')
# plt.show()
plt.close()


