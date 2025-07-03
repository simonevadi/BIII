import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import xrt.backends.raycing.materials as rm
 
from raypyng.postprocessing import PostProcessAnalyzed
from helper_lib import get_reflectivity
from parameter_ml import SlitSize

##############################################################
# LOAD IN DATA

this_file_dir=os.path.dirname(os.path.realpath(__file__))

# Read Undulator CSV-File BESSY III
undulator_table_filename = os.path.join(this_file_dir, 'undulator_flux_curves','IVUE28_b3_2025_smalerz_300mA_2PercCoupl.txt')
undulator_df = pd.read_csv(undulator_table_filename, sep='\t')

# Read CSV-File of the Beamline Simulation
BL_file_path = os.path.join('RAYPy_Simulation_bessy3_56m_PGM_2Perc_coupl_err_on0_75deg_2400l_V3_FLUX', 'DetectorAtFocus_RawRaysOutgoing.csv')
BL_df = pd.read_csv(BL_file_path)


##############################################################
# PLOTTING AND ANALYSIS
# Create the Main figure
fig, (axs) = plt.subplots(4, 2, figsize=(20, 15))
fig.suptitle('IVUE28 BESSY III Standard PGM Beamline (56 m) with ML', size=16)
x_range = [500, 6000]

# MIRROR REFLECTIVITY
ax1 = axs[0, 0]
# Coatings:
de = 38.9579-30.0000
table = 'Henke'
theta = 0.75
E = np.arange(50, 6001, de)
Au  = rm.Material('Au',  rho=19.32, kind='mirror',table=table)
Pt  = rm.Material('Pt',  rho=21.45, kind='mirror',table=table)
Ir  = rm.Material('Ir',  rho=22.56, kind='mirror',table=table)
Cr  = rm.Material('Cr',  rho=7.15,  kind='mirror',table=table)
B4C = rm.Material('C',   rho=2.52,  kind='mirror',table=table)
IrCrB4C = rm.Multilayer(tLayer=B4C, tThickness=40, 
                        bLayer=Cr, bThickness=60, 
                        nPairs=1, substrate=Ir)

Au, _ = get_reflectivity(Au, E=E, theta=theta)
Pt, _ = get_reflectivity(Pt, E=E, theta=theta)
Ir, _ = get_reflectivity(Ir, E=E, theta=theta)
Cr, _ = get_reflectivity(Cr, E=E, theta=theta)
B4C, _ = get_reflectivity(B4C, E=E, theta=theta)
IrCrB4C, _ = get_reflectivity(IrCrB4C, E=E, theta=theta)

ax1.plot(E, Au, 'gold', label='Au', alpha=0.5)
ax1.plot(E, Pt, 'dimgrey', label='Pt', alpha=0.5)
ax1.plot(E, Ir, 'darkgrey', label='Ir', alpha=0.5)
# ax1.plot(E, Cr, 'c', label='Cr')
# ax1.plot(E, B4C, 'm', label='B4C')
ax1.plot(E, IrCrB4C, 'darkmagenta', label='IrCrB4C')

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

harms = [1,3,5,7,9] # The Harmonics from the ID. Typically 1,3,5, rather higher. Depends on the FluxSims of the ID.

for harm in harms:
    ax2.plot(undulator_df[f'Energy{harm}[eV]'], undulator_df[f'Photons{harm}'], label=f'Harm. {harm}')
    
ax2.set_title('IVUE28 Flux curve')
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
    filtered_df = BL_df[(BL_df['PhotonEnergy'] >= Emin_harm) & (BL_df['PhotonEnergy'] <= Emax_harm)]
    ax3.plot(filtered_df['PhotonEnergy'], filtered_df['Bandwidth']*1000, label=f'Harm. {harm}')

ax3.set_title(f'Transmitted Bandwidth @{int(SlitSize[0]*1000)} µm ExitSlit')
ax3.set_xlabel('Energy [eV]')
ax3.set_ylabel('Transmitted bandwidth [meV]')
ax3.legend(loc='best', fontsize=12)
ax3.set_xlim(x_range)
ax3.minorticks_on()
ax3.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# BEAMLINE FLUX CURVE
ax4 = axs[1, 1]

for harm in harms:
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df[(BL_df['PhotonEnergy'] >= Emin_harm) & (BL_df['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(filtered_df['PhotonEnergy'], filtered_df[f'PhotonFlux{harm}'], label=f'Harm. {harm}')

ax4.set_title('Flux curve 56 m PGM-Beamline with ML')
ax4.set_xlabel('Energy [eV]')
ax4.set_ylabel('Photon flux [ph/s/300 mA/0.1% BW]')
ax4.legend(loc='best', fontsize=12)
ax4.set_xlim(x_range)
ax4.minorticks_on()
ax4.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# RESOLVING POWER
ax5 = axs[2, 0]

for harm in harms:
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df[(BL_df['PhotonEnergy'] >= Emin_harm) & (BL_df['PhotonEnergy'] <= Emax_harm)]
    ax5.plot(filtered_df['PhotonEnergy'], (filtered_df[f'PhotonEnergy']/filtered_df[f'Bandwidth']), label=f'Harm. {harm}')

ax5.set_title(f'Resolving Power @ {int(SlitSize[0]*1000)} µm ExitSlit')
ax5.set_xlabel('Energy [eV]')
ax5.set_ylabel(r'$\frac{E}{\Delta E}$ [a.u.]')
ax5.legend(loc='best', fontsize=12)
ax5.set_xlim(x_range)
ax5.minorticks_on()
ax5.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# Flux Density
ax6 = axs[2, 1]
for harm in harms:
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df[(BL_df['PhotonEnergy'] >= Emin_harm) & (BL_df['PhotonEnergy'] <= Emax_harm)]
    foc_area = (filtered_df['VerticalFocusFWHM']*filtered_df['HorizontalFocusFWHM'])*1000  # in µm²
    ax6.plot(filtered_df['PhotonEnergy'],filtered_df[f'PhotonFlux{harm}']/foc_area, label=f'Harm. {harm}')

ax6.set_title('Flux Density')
ax6.set_xlabel('Energy [eV]')
ax6.set_ylabel('Photons flux per µm²')
ax6.legend(loc='best', fontsize=12)
ax6.set_xlim(x_range)
ax6.minorticks_on()
ax6.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')

# Horizontal Focus Size
ax7 = axs[3, 0]

ax7.plot(BL_df['PhotonEnergy'], BL_df['HorizontalFocusFWHM']*1000, label='Horizontal Focus Size', color='red')

ax7.set_title('Horizontal Focus Size')
ax7.set_xlabel('Energy [eV]')
ax7.set_ylabel('[µm]')
ax7.set_xlim(x_range)
ax7.minorticks_on()
ax7.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')

# Vertical Focus Size
ax8 = axs[3, 1]

ax8.plot(BL_df['PhotonEnergy'], BL_df['VerticalFocusFWHM']*1000, label='Vertical Focus Size', color='limegreen')

ax8.set_title('Vertical Focus Size')
ax8.set_xlabel('Energy [eV]')
ax8.set_ylabel('[µm]')
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
plt.savefig('plot/Flux_curves IVUE28 @ BESSY III with ML_err_on.pdf')
plt.show()
