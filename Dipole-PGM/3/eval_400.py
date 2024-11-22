import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# path to xrt:
import os, sys; sys.path.append(os.path.join('..', '..', '..'))  # analysis:ignore
import xrt.backends.raycing.materials as rm
from helper_lib import get_reflectivity


# file/folder/ml index definition
from params import lb_400_SlitSize as SlitSize
from params import lb_400_cff as cff
from params import lb_400_sim_name_rp, lb_400_sim_name_flux


flux_simulation_folder_400 = 'RAYPy_Simulation_' + lb_400_sim_name_flux
rp_simulation_folder_400   = 'RAYPy_Simulation_' + lb_400_sim_name_rp



# loading the data
oe = 'DetectorAtFocus' + '_RawRaysOutgoing.csv'
flux = pd.read_csv(os.path.join(flux_simulation_folder, oe))
rp = pd.read_csv(os.path.join(rp_simulation_folder, oe))
source_flux = flux.drop_duplicates(subset='Dipole.photonEnergy')[['Dipole.photonEnergy', 'SourcePhotonFlux']]



# plotting Flux and RP
fig, (axs) = plt.subplots(4, 2,figsize=(10,10))

ax = axs[0,1]
ax.axis("off")

# text
ax = axs[1,0]
ax.set_title('Dipole Flux')
ax.grid(which='both', axis='both')
ax.plot(source_flux['Dipole.photonEnergy'],
        source_flux['SourcePhotonFlux'],
        label='Dipole Flux')
ax.set_ylabel('Flux [ph/s/0.1%bw]')

ax.legend(loc=6)

# MIRROR COATING
de = 38.9579-30.0000
table = 'Henke'
theta = 1.0
E = np.arange(50, 5001, de)

Pt = rm.Material('Pt', rho=21.45,  kind='mirror',  table=table)
Pt1, _ = get_reflectivity(Pt, E=E, theta=theta)

ax2=axs[0,0]
ax2.set_xlabel('Energy [eV]')
ax2.set_ylabel('Reflectivity [a.u.]')
ax2.set_title(f'Mirror Coating Reflectivity at {theta}° ')
ax2.plot(E, Pt1, label='Pt°')
ax2.legend()



# AVAILABLE FLUX 
ax = axs[1,1]
for ind, es_size in enumerate(SlitSize):
    filtered_flux = flux[flux['ExitSlit.totalHeight'] == es_size]
    energy = filtered_flux['Dipole.photonEnergy']
    perc_flux = filtered_flux['PercentageRaysSurvived']
    ax.plot(energy,perc_flux, label=f'ExitSlit {int(es_size*1000)} um' )

ax.set_xlabel(r'Energy [eV]')
ax.set_ylabel('Transmission [%]')
ax.set_title('Available Flux (in transmitted bandwidth)')
ax.grid(which='both', axis='both')
ax.legend()


ax2 = ax.twinx()
energy = filtered_flux['Dipole.photonEnergy']
abs_flux = filtered_flux['PhotonFlux']
ax2.set_xlabel(r'Energy [eV]')
line = ax2.plot(energy, abs_flux)
line[0].remove()
ax2.set_ylabel('Flux [ph/s/tbw]')


# BANDWIDTH
ax = axs[2,0]
for ind, es_size in enumerate(SlitSize):
    filtered_rp = rp[rp['ExitSlit.totalHeight'] == es_size]
    energy = filtered_rp['Dipole.photonEnergy']
    bw = filtered_rp['Bandwidth']
    ax.plot(energy,bw, label=f'ExitSlit {int(es_size*1000)} um' )
ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Transmitted Bandwidth [eV]')
ax.set_title('Transmitted bandwidth (tbw)')
ax.grid(which='both', axis='both')
# ax.legend()


# RESOLVING POWER
ax = axs[2,1]
for ind, es_size in enumerate(SlitSize):
    filtered_rp = rp[rp['ExitSlit.totalHeight'] == es_size]
    energy = filtered_rp['Dipole.photonEnergy']
    bw = filtered_rp['Bandwidth']
    ax.plot(energy,energy/bw, label=f'ExitSlit {int(es_size*1000)} um' )

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('RP [a.u.]')
ax.set_title('Resolving Power')
ax.grid(which='both', axis='both')
ax.legend()

# HORIZONTAL FOCUS
ax = axs[3,0]
# Initialize an empty list to accumulate 'HorizontalFocusFWHM' data
focx = []

# Loop through each slit size in the 'SlitSize' list
for ind, es_size in enumerate(SlitSize):
    # Filter the DataFrame for the current slit size
    filtered_rp = rp[rp['ExitSlit.totalHeight'] == es_size]
    
    energy = filtered_rp['Dipole.photonEnergy']
    
    # Sum up 'HorizontalFocusFWHM' for each slit size
    focx.append(filtered_rp['HorizontalFocusFWHM'])

# Convert 'focx_plot' to a numpy array for element-wise operations
focx = np.array(focx)
focx = np.mean(focx, axis=0)

ax.plot(energy,focx*1000, label=f'ExitSlit {int(es_size*1000)} um' )

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Focus Size [um]')
ax.set_title('Horizontal focus')
ax.legend()

# VERTICAL FOCUS
ax = axs[3,1]
for ind, es_size in enumerate(SlitSize):
    filtered_rp = rp[rp['ExitSlit.totalHeight'] == es_size]
    energy = filtered_rp['Dipole.photonEnergy']
    focy = filtered_rp['VerticalFocusFWHM']
    ax.plot(energy,focy*1000, label=f'ExitSlit {int(es_size*1000)} um' )

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Focus Size [um]')
ax.set_title('Vertical focus')

plt.suptitle('PGM-Dipole, 400 l/mm laminar grating')
plt.tight_layout()
plt.savefig('plot/PGM-400-Dipole.png')
# plt.show()


fig, (axs) = plt.subplots(2, 1,figsize=(10,10))


# PERMIL BANDWIDTH
ax = axs[0]
for ind, es_size in enumerate(SlitSize):
    filtered_rp = rp[rp['ExitSlit.totalHeight'] == es_size]
    energy = filtered_rp['Dipole.photonEnergy']
    bw = filtered_rp['Bandwidth']
    ax.plot(energy/1000,energy/(1000*bw) )

ax.set_xlabel('Energy [keV]')
ax.set_ylabel('Energy/1000/bandwidth [a.u.]')
ax.set_title('PerMil Transmission')
ax.grid(which='both', axis='both')


# PERMIL FLUX 
ax = axs[1]
for ind, es_size in enumerate(SlitSize):
    filtered_flux = flux[flux['ExitSlit.totalHeight'] == es_size]
    energy = filtered_flux['Dipole.photonEnergy']
    abs_flux = filtered_flux['PhotonFlux']
    filtered_rp = rp[rp['ExitSlit.totalHeight'] == es_size]
    bw = filtered_rp['Bandwidth']
    ax.plot(energy,(energy/1000/bw)*abs_flux)

ax.set_xlabel(r'Energy [eV]')
ax.set_ylabel('Flux [ph/s/tbw]')
ax.set_title('Transmission / Per MIl bandwidth')
ax.grid(which='both', axis='both')

plt.suptitle('PGM-Dipole, 400 l/mm laminar grating')
plt.tight_layout()
plt.savefig('plot/PGM-400-Dipole-PerMil.png')


