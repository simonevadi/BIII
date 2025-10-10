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
from parameter import SlitSize_2400 as SlitSize
from parameter import undulator as undulator_df
from parameter import efficiency_2400

from raypyng.postprocessing import PostProcessAnalyzed

p = PostProcessAnalyzed()
mov_av = p.moving_average
##############################################################
# LOAD IN DATA

# Read CSV-File of the Beamline Simulation
BL_file_path = os.path.join('RAYPy_Simulation_sotexs_2400', 'DetectorAtFocus_RawRaysOutgoing.csv')
BL_df = pd.read_csv(BL_file_path)

BL_file_path = os.path.join('RAYPy_Simulation_sotexs_1200', 'DetectorAtFocus_RawRaysOutgoing.csv')
BL_df_1200 = pd.read_csv(BL_file_path)
# BL_df_1200 = BL_df_1200_all[BL_df_1200_all['PG.cFactor']==2.25]  

##############################################################
# PLOTTING AND ANALYSIS
plt.rcParams.update({'font.size': 13})  # Change 14 to any size you prefer
# Create the Main figure
fig, (axs) = plt.subplots(4, 2, figsize=(20, 15))
fig.suptitle('Signature2 - Liquid Interface, 2400 l/mm - Nano Focus', size=16)
x_range = [0, 10000]
colors = ['blue', 'red', 'green', 'orange', 'purple', 'violet']

# MIRROR REFLECTIVITY
ax1 = axs[0, 0]
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


# FLUX CURVE UNDULATOR
#Choose the harmonic to plot
ax2 = axs[0, 1]

harms = [1,3,5,7] # The Harmonics from the ID. Typically 1,3,5, rather higher. Depends on the FluxSims of the ID.

for ind, harm in enumerate(harms):
    ax2.plot(undulator_df[f'Energy{harm}[eV]'],
             undulator_df[f'Photons{harm}'],
             color=colors[ind],
             label=f'Harm. {harm}')
    
ax2.set_title('IVU28 Flux curve')
ax2.set_xlabel('Energy [eV]')
ax2.set_ylabel('Photon flux [ph/s/300 mA/0.1% BW]')
ax2.legend(loc='best')
ax2.set_xlim(x_range)
ax2.set_yscale('log')
ax2.minorticks_on()
ax2.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# TRANSMITTED BANDWIDTH
ax3 = axs[1, 0]

window = 5

# 1200
for ind, harm in enumerate(harms):
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df_1200[(BL_df_1200['PhotonEnergy'] >= Emin_harm) & (BL_df_1200['PhotonEnergy'] <= Emax_harm)]
    ax3.plot(mov_av(filtered_df['PhotonEnergy'], window), 
             mov_av(filtered_df['Bandwidth']*1000, window),
             label=f'Harm.{harm}, 1200l/mm',
             color=colors[ind], linestyle='solid')
    
# 2400
for ind, harm in enumerate(harms):
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df[(BL_df['PhotonEnergy'] >= Emin_harm) & (BL_df['PhotonEnergy'] <= Emax_harm)]
    ax3.plot(mov_av(filtered_df['PhotonEnergy'], window),
             mov_av(filtered_df['Bandwidth']*1000, window),
             label=f'Harm.{harm}, 2400l/mm',
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
    filtered_df = BL_df_1200[(BL_df_1200['PhotonEnergy'] >= Emin_harm) & (BL_df_1200['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(filtered_df['PhotonEnergy'],
             filtered_df[f'PhotonFlux{harm}'],
             label=f'Harm. {harm}',
             color=colors[ind], linestyle='solid')
    
# 2400
for ind, harm in enumerate(harms):
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df[(BL_df['PhotonEnergy'] >= Emin_harm) & (BL_df['PhotonEnergy'] <= Emax_harm)]
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

# RESOLVING POWER
ax5 = axs[2, 0]
window = 20

# 1200
ax5.plot(mov_av(BL_df_1200['PhotonEnergy'], window),
         mov_av(BL_df_1200[f'PhotonEnergy']/BL_df_1200[f'Bandwidth'], window),
         linestyle='solid', label='All Harmonics, 1200l/mm')

# 2400
ax5.plot(mov_av(BL_df['PhotonEnergy'], window),
         mov_av(BL_df[f'PhotonEnergy']/BL_df[f'Bandwidth'], window),
         linestyle='dashed', label='All Harmonics, 2400l/mm')

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
    filtered_df = BL_df_1200[(BL_df_1200['PhotonEnergy'] >= Emin_harm) & (BL_df_1200['PhotonEnergy'] <= Emax_harm)]
    foc_area = (filtered_df['VerticalFocusFWHM']*filtered_df['HorizontalFocusFWHM'])*1000  # in µm²
    ax6.plot(filtered_df['PhotonEnergy'],
             filtered_df[f'PhotonFlux{harm}']/foc_area,
             label=f'Harm. {harm}', 
             color=colors[ind], linestyle='solid')
    
# 2400
for ind, harm in enumerate(harms):
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df[(BL_df['PhotonEnergy'] >= Emin_harm) & (BL_df['PhotonEnergy'] <= Emax_harm)]
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

# Focus
ax7 = axs[3, 0]
focus_path = os.path.join('plot', 'DetectorAtFocus-RawRaysOutgoing.csv')
focus = pd.read_csv(
    focus_path,
    sep='\t',        # columns separated by tabs
    decimal='.',     # use comma as decimal separator
    skiprows=1       # skip the first line (the 'sep=' line)
)

hb = ax7.hexbin(
    focus['DetectorAtFocus_OX']*1e6,
    focus['DetectorAtFocus_OY']*1e6,
    gridsize=60, cmap='viridis'
)
ax7.set_xlabel('nm')
ax7.set_ylabel('nm')
hor_foc = np.mean(BL_df['HorizontalFocusFWHM']*1e6)
ver_foc = np.mean(BL_df['VerticalFocusFWHM']*1e6)
ax7.set_title(f'Focus at Sample Position: (HxV) {hor_foc:.0f} x {ver_foc:.0f} nm²')


# multilayer efficiency
ax8 = axs[3, 1]

ax8.plot(efficiency_2400['Energy[eV]'],
         efficiency_2400['Efficiency']*100)

ax8.set_title('Monochromator optics coated with Ni-B4C multilayer, 40 bilayers')
ax8.set_xlabel('Energy [eV]')
ax8.set_ylabel('Monochromator Efficiency [%]')
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
plt.savefig('plot/sotexs_nanoFocus.png')
# plt.show()
plt.close()


