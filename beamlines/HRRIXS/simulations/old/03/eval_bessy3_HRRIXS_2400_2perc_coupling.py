import numpy as np
# import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

# path to xrt:
import os, sys; sys.path.append(os.path.join('..', '..', '..'))  # analysis:ignore
import xrt.backends.raycing.materials as rm

# raypyng 
from raypyng.postprocessing import PostProcessAnalyzed

# from helper library
from helper_lib import get_reflectivity
from helper_lib import scale_undulator_flux, order

# import simulation parameters
from parameter import energy_rp, energy_flux
from parameter import SlitSize
from parameter import rml_file_name_bessy3_HRRIXS_2Perc_coupling as rml_file_name
from parameter import colors, grating


# file/folder/ml index definition
flux_simulation_folder = 'RAYPy_Simulation_'+rml_file_name+'_FLUX'
rp_simulation_folder = 'RAYPy_Simulation_'+rml_file_name+'_RP'



varying_var = SlitSize
varying_var_n = 'Exit Slit'
varying_var_unit = 'um'

# loading the data
oe = 'DetectorAtFocus' + '_RawRaysOutgoing.csv'
flux = pd.read_csv(os.path.join(flux_simulation_folder, oe))
rp = pd.read_csv(os.path.join(rp_simulation_folder, oe))
source_flux = flux.drop_duplicates(subset='SU.photonEnergy')[['SU.photonEnergy', 'SourcePhotonFlux']]
print(flux.columns)


########################################
# plotting Flux and RP

fig, (axs) = plt.subplots(3, 2,figsize=(10,10))
fig.suptitle(f"{rml_file_name}, {grating[0]} l/mm grating")


# MIRROR COATING
# de = 38.9579-30.0000
# table = 'Henke'
# theta = 
# E = np.arange(50, 5001, de)
# Ir  = rm.Material('Ir',  rho=22.56, kind='mirror',table=table)
# Cr  = rm.Material('Cr',  rho=7.15,  kind='mirror',table=table)
# B4C = rm.Material('C', rho=2.52,  kind='mirror',  table=table)
# IrCrB4C = rm.Multilayer( tLayer=B4C, tThickness=40, 
#                         bLayer=Cr, bThickness=60, 
#                         nPairs=1, substrate=Ir)

# IrCrB4C, _ = get_reflectivity(IrCrB4C, E=E, theta=theta)

# ax2=axs[0,0]
# ax2.set_xlabel('Energy [eV]')
# ax2.set_ylabel('Reflectivity [a.u.]')
# ax2.set_title('Mirror Coating Reflectivity')
# ax2.plot(E, IrCrB4C, 'b', label='IrCrB4C')
# ax2.legend()



# BEAMLINE TRANSMISSION / AVAIABLE FLUX
ax = axs[0,1]

for ind, es_size in enumerate(SlitSize):
    filtered_flux = flux[flux['ExitSlit.openingHeight'] == es_size]
    #filtered_flux = flux[flux['PG.lineDensity'] == grating[0]]
    energy = filtered_flux['SU.photonEnergy']
    perc_flux = filtered_flux['PercentageRaysSurvived']
    ax.plot(energy,perc_flux, label=f'ExitSlit {int(es_size*1000)} um')

ax.set_xlabel(r'Energy [eV]')
ax.set_ylabel('Transmission [%]')
ax.set_title('Available Flux [in transmitted bandwidth]')
ax.grid(which='both', axis='both')
ax.legend()



# BANDWIDTH
ax = axs[1,0]

for ind, es_size in enumerate(SlitSize):
    filtered_rp = rp[rp['ExitSlit.openingHeight'] == es_size]
    energy = filtered_rp['SU.photonEnergy']
    bw = filtered_rp['Bandwidth']
    ax.plot(energy,bw, label=f'ExitSlit {int(es_size*1000)} um' )
ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Transmitted Bandwidth [eV]')
ax.set_title('Transmitted bandwidth (tbw)')
ax.grid(which='both', axis='both')



# RESOLVING POWER

ax = axs[1,1]
for ind, es_size in enumerate(SlitSize):
    filtered_rp = rp[rp['ExitSlit.openingHeight'] == es_size]
    energy = filtered_rp['SU.photonEnergy']
    bw = filtered_rp['Bandwidth']
    ax.plot(energy,energy/bw, label=f'ExitSlit {int(es_size*1000)} um' )

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('RP [a.u.]')
ax.set_title('Resolving Power')
ax.grid(which='both', axis='both')
ax.legend()



# HORIZONTAL FOCUS

ax = axs[2,0]

for ind, es_size in enumerate(SlitSize):
    filtered_rp = rp[rp['ExitSlit.openingHeight'] == es_size]
    energy = filtered_rp['SU.photonEnergy']
    focx = filtered_rp['HorizontalFocusFWHM']
    ax.plot(energy,focx*1000, label=f'ExitSlit {int(es_size*1000)} um' )

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Focus Size [um]')
ax.set_title('Horizontal focus')

plt.suptitle('PGM, 2400 l/mm grating (unkonwn)')
plt.tight_layout()
plt.savefig('plot/FluxRpFocus'+rml_file_name+'.pdf')
# plt.show()


## Initialize an empty list to accumulate 'HorizontalFocusFWHM' data
#focx = []
#
## Loop through each slit size in the 'SlitSize' list
#for ind, es_size in enumerate(SlitSize):
#    # Filter the DataFrame for the current slit size
#    filtered_rp = rp[rp['ExitSlit.openingHeight'] == es_size]
#    
#    energy = filtered_rp['SU.photonEnergy']
#    
#    # Sum up 'HorizontalFocusFWHM' for each slit size
#    focx.append(filtered_rp['HorizontalFocusFWHM'])
#
## Convert 'focx_plot' to a numpy array for element-wise operations
#focx = np.array(focx)
#focx = np.mean(focx, axis=0)
#
#ax.plot(energy,focx*1000, label=f'ExitSlit {int(es_size*1000)} um' )
#
#ax.set_xlabel('Energy [eV]')
#ax.set_ylabel('Focus Size [um]')
#ax.set_title('Horizontal focus')
#ax.legend()



# VERTICAL FOCUS

ax = axs[2,1]
for ind, es_size in enumerate(SlitSize):
    filtered_rp = rp[rp['ExitSlit.openingHeight'] == es_size]
    energy = filtered_rp['SU.photonEnergy']
    focy = filtered_rp['VerticalFocusFWHM']
    ax.plot(energy,focy*1000, label=f'ExitSlit {int(es_size*1000)} um' )

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Focus Size [um]')
ax.set_title('Vertical focus')

plt.suptitle('PGM, 2400 l/mm grating (unkonwn)')
plt.tight_layout()
plt.savefig('plot/FluxRpFocus'+rml_file_name+'.pdf')
# plt.show()


fig, (axs) = plt.subplots(2, 1,figsize=(10,10))



 # PERMIL BANDWIDTH
ax = axs[0]
for ind, es_size in enumerate(SlitSize):
     filtered_rp = rp[rp['ExitSlit.openingHeight'] == es_size]
     energy = filtered_rp['SU.photonEnergy']
     bw = filtered_rp['Bandwidth']
     ax.plot(energy/1000,energy/(1000*bw) )
 
ax.set_xlabel('Energy [keV]')
ax.set_ylabel('Energy/1000/bandwidth [a.u.]')
ax.set_title('PerMil Transmission')
ax.grid(which='both', axis='both')

 
## PERMIL FLUX 
#ax = axs[1]
#for ind, es_size in enumerate(SlitSize):
#     filtered_flux = flux[flux['ExitSlit.openingHeight'] == es_size]
#     energy = filtered_flux['SU.photonEnergy']
#     abs_flux = filtered_flux['PhotonFlux']
#     filtered_rp = rp[rp['ExitSlit.openingHeight'] == es_size]
#     bw = filtered_rp['Bandwidth']
#     ax.plot(energy,(energy/1000/bw)abs_flux)
# 
#ax.set_xlabel(r'Energy [eV]')
#ax.set_ylabel('Flux [ph/s/tbw]')
#ax.set_title('Transmission / Per MIl bandwidth')
#ax.grid(which='both', axis='both')
# 
plt.suptitle('PGM-Dipole, 2400 l/mm grating (unkonwn)')
plt.tight_layout()
plt.savefig('plot/HRRIXS-2400-PGM-PerMil.pdf')