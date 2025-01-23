import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

# path to xrt:
import os, sys; sys.path.append(os.path.join('..', '..', '..'))  # analysis:ignore
import xrt.backends.raycing.materials as rm

# helper lib
from helper_lib import get_reflectivity
from helper_lib import scale_undulator_flux

# andrey ML
from multilayer_helper import ML_eff

# file/folder/ml index definition
from params import hb_1200_sim_name_flux, lb_400_sim_name_flux,  ml_sim_name_flux
from params import hb_1200_sim_name_rp, lb_400_sim_name_rp, ml_sim_name_rp

from params import ml_table, ml_index
from raypyng.postprocessing import PostProcessAnalyzed

beamline_name = 'BESSYIII_Dipole'
p = PostProcessAnalyzed()
window = 50
# Set global font sizes
suptitle_size = 18
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['font.size'] = 12  # Adjust font size globally
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['legend.fontsize'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12

# loading the data
oe = 'DetectorAtFocus' + '_RawRaysOutgoing.csv'

# 1200 l/mm
flux1200 = pd.read_csv(os.path.join(f'RAYPy_Simulation_{hb_1200_sim_name_flux}', oe))
rp1200 = pd.read_csv(os.path.join(f'RAYPy_Simulation_{hb_1200_sim_name_rp}', oe))
energy_1200 = flux1200['PhotonEnergy'].unique()
source_flux1200 = flux1200['SourcePhotonFlux']
# 400 l/mm
flux400 = pd.read_csv(os.path.join(f'RAYPy_Simulation_{lb_400_sim_name_flux}', oe))
rp400 = pd.read_csv(os.path.join(f'RAYPy_Simulation_{lb_400_sim_name_rp}', oe))
energy_400 = flux400['PhotonEnergy'].unique()
source_flux400 = flux400['SourcePhotonFlux']
# ml 
fluxml = pd.read_csv(os.path.join(f'RAYPy_Simulation_{ml_sim_name_flux}', oe))
rpml = pd.read_csv(os.path.join(f'RAYPy_Simulation_{ml_sim_name_flux}', oe))
energy_ml = fluxml['PhotonEnergy'].unique()
source_fluxml = fluxml['SourcePhotonFlux']


# plotting Flux and RP
fig, (axs) = plt.subplots(3, 2,figsize=(10,10))
log = False
# MIRROR COATING
ax=axs[0,0]

de = 38.9579-30.0000
table = 'Henke'
theta = 0.8
E = np.arange(50, 5001, de)
# triple coating
Ir  = rm.Material('Ir',  rho=22.56, kind='mirror',table=table)
Cr  = rm.Material('Cr',  rho=7.15,  kind='mirror',table=table)
B4C = rm.Material('C', rho=2.52,  kind='mirror',  table=table)
IrCrB4C = rm.Multilayer( tLayer=B4C, tThickness=40, 
                        bLayer=Cr, bThickness=60, 
                        nPairs=1, substrate=Ir)
IrCrB4C, _ = get_reflectivity(IrCrB4C, E=E, theta=theta)


ax.plot(E, IrCrB4C, 'blue', label='IrCrB4C')

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Reflectivity [a.u.]')
ax.set_title(f'Mirror Coating Reflectivity at {theta}° ')
ax.legend()

# CPMU20

ax = axs[0,1]
ax.plot(energy_ml, source_fluxml)

ax.set_title('CPMU20 Flux')
ax.grid(which='both', axis='both')

ax.set_ylabel('Flux [ph/s/0.1A/0.1%bw]')




color_list = [('blue','orange'), ('cyan', 'red')]
labels_list = ['M1 out', 'M1 in']




# AVAILABLE FLUX IN PERCENTAGE
ax = axs[1,0]

ax.plot(flux400['Dipole.photonEnergy'],
        flux400['PercentageRaysSurvived'], 
        label=f'400 l/mm' )
ax.plot(flux1200['Dipole.photonEnergy'],
        flux1200['PercentageRaysSurvived'], 
        label=f'1200 l/mm' )
# ax.plot(fluxml['Dipole.photonEnergy'],
#         fluxml['PercentageRaysSurvived'], 
#         label=f'2400 l/mm' )
ax.set_xlabel(r'Energy [eV]')
ax.set_ylabel('Transmission [%]')
ax.set_title('Available Flux (in transmitted bandwidth)')
ax.grid(which='both', axis='both')
# ax.set_yscale('log')

# Define a custom formatter function to display labels as floats with two decimal places
def custom_formatter(x, pos):
    return f"{x:.2}%"

# Apply the custom formatter to the y-axis
ax.yaxis.set_major_formatter(ticker.FuncFormatter(custom_formatter))

# AVAILABLE FLUX ABSOLUTE
ax = axs[1,1]
abs_flux_1200 = flux1200['PhotonFlux']
abs_flux_400 = flux400['PhotonFlux']

perc_flux_ml = fluxml['PhotonFlux']
abs_flux_ml = ML_eff(perc_flux_ml, 
                ind=ml_index, 
                energy=energy_ml,
                grating_eff_file=ml_table)


ax.plot(energy_400, abs_flux_400, label='400 l/mm')
ax.plot(energy_1200, abs_flux_1200, label='1200 l/mm')
ax.plot(energy_ml, abs_flux_ml, label='2400 l/mm + ML')
if log:
    ax.set_yscale('log')
ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Flux [ph/s/0.1A/tbw]')
ax.grid(which='both', axis='both')
ax.set_title('Available Flux (absolute)')
ax.legend()


# BANDWIDTH
ax = axs[2,0]
bw_400 = rp400['Bandwidth']
bw_1200 = rp1200['Bandwidth']
bw_ml = rpml['Bandwidth']

ax.plot(energy_400,bw_400)
ax.plot(energy_1200,bw_1200)
ax.plot(p.moving_average(energy_ml, window), 
        p.moving_average(bw_ml, window))
# Calculate the line as 6000 divided by the energy values
energy_threshold = np.arange(energy_1200[0], energy_ml[-1])
threshold_transmission = energy_threshold/6000
ax.plot(energy_threshold, threshold_transmission, linestyle='dashed', color='black')
# Plot this calculated line on the same axes
# ax.plot(energy_ml, inv_energy_line, label='6000/Energy', linestyle='--', color='red')

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Transmitted Bandwidth [eV]')
ax.set_title('Transmitted bandwidth (tbw)')
ax.grid(which='both', axis='both')


# RESOLVING POWER
ax = axs[2,1]

ax.plot(energy_400,energy_400/bw_400)
ax.plot(energy_1200,energy_1200/bw_1200)
ax.plot(p.moving_average(energy_ml, window),
        p.moving_average(energy_ml/bw_ml, window))

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('RP [a.u.]')
ax.set_title('Resolving Power')
ax.grid(which='both', axis='both')
ax.axhline(y=6000, color='k', linestyle='--', label='RP 6000')
ax.legend()

plt.suptitle('SoTeXs', fontsize=suptitle_size)
plt.tight_layout()
plt.savefig('plot/Dipole-PGM.png')

# plotting Flux and RP
fig, (axs) = plt.subplots(2, 1,figsize=(10,10))
   

# HORIZONTAL FOCUS
ax = axs[0]
focx_400 = rp400['HorizontalFocusFWHM']
focx_1200 = rp1200['HorizontalFocusFWHM']
focx_ml = rpml['HorizontalFocusFWHM']

ax.plot(p.moving_average(energy_400,window),
        p.moving_average(focx_400*1000,window), 
        label='400 l/mm')
ax.plot(p.moving_average(energy_1200,window),
        p.moving_average(focx_1200*1000,window), 
        label='1200 l/mm')
ax.plot(p.moving_average(energy_ml,window),
        p.moving_average(focx_ml*1000,window), 
        label='2400 l/mm')

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Focus Size [um]')
ax.set_title('Horizontal focus')
ax.legend()
# VERTICAL FOCUS
ax = axs[1]
focy_400 = rp400['VerticalFocusFWHM']
focy_1200 = rp1200['VerticalFocusFWHM']
focy_ml = rpml['VerticalFocusFWHM']

ax.plot(p.moving_average(energy_400, window),
        p.moving_average(focy_400*1000,window))
ax.plot(p.moving_average(energy_1200, window),
        p.moving_average(focy_1200*1000,window))
ax.plot(p.moving_average(energy_ml,window),
        p.moving_average(focy_ml*1000,window))

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Focus Size [um]')
ax.set_title('Vertical focus')

plt.suptitle('SoTeXs Focus Size', fontsize=suptitle_size)
plt.tight_layout()
plt.savefig('plot/Dipole-PGM-Focus.png')


fig, (axs) = plt.subplots(2, 1,figsize=(10,10))


# PERMIL BANDWIDTH
ax = axs[0]
permil_bw_400 = flux400['EnergyPerMilPerBw']
permil_bw_1200 = flux1200['EnergyPerMilPerBw']
permil_bw_ml = fluxml['EnergyPerMilPerBw']

ax.plot(p.moving_average(energy_400/1000,window),
    p.moving_average(permil_bw_400,window))
ax.plot(p.moving_average(energy_1200/1000,window),
    p.moving_average(permil_bw_1200,window))
ax.plot(p.moving_average(energy_ml/1000,window),
    p.moving_average(permil_bw_ml,window))

ax.set_xlabel('Energy [keV]')
ax.set_ylabel('Energy/1000/bandwidth [a.u.]')
ax.set_title('PerMil Transmission')
ax.grid(which='both', axis='both')
ax.legend()


# PERMIL FLUX 
ax = axs[1]
permil_flux_400 = flux400['FluxPerMilPerBwPerc']
permil_flux_1200 = flux1200['FluxPerMilPerBwPerc']
permil_flux_ml = fluxml['FluxPerMilPerBwPerc']

ax.plot(p.moving_average(energy_1200,10),
        p.moving_average(permil_flux_1200,10),
        label='400 l/mm')
ax.plot(p.moving_average(energy_400,10),
        p.moving_average(permil_flux_400,10),
        label='1200 l/mm')
ax.plot(p.moving_average(energy_ml,10),
        p.moving_average(permil_flux_ml,10),
        label='2400 l/mm')

ax.set_xlabel(r'Energy [eV]')
ax.set_ylabel('Flux [ph/s/0.1A/tbw]')
ax.set_title('Transmission / Per Mil bandwidth')
ax.grid(which='both', axis='both')
ax.set_yscale('log')
ax.legend()

plt.suptitle('SoTeXs PerMil', fontsize=suptitle_size)
plt.tight_layout()
plt.savefig('plot/Dipole-PGM-PerMil.png')
plt.show()

