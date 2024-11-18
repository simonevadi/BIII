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
from parameter import rml_file_name_bessy3_standard_PGM_100Perc_coupling as rml_file_name
from parameter import colors, grating
SlitSize = SlitSize*1000

# file/folder/ml index definition
flux_simulation_folder = 'RAYPy_Simulation_'+rml_file_name+'_FLUX'
rp_simulation_folder = 'RAYPy_Simulation_'+rml_file_name+'_RP'



varying_var = SlitSize
varying_var_n = 'Exit Slit'
varying_var_unit = 'um'

# load Flux simulations results
folder_name  = flux_simulation_folder
oe           = 'DetectorAtFocus'
flux_path    = os.path.join(flux_simulation_folder, oe+'_RawRaysOutgoing.dat')
flux         = pd.read_csv(flux_path, sep='\t')
en_flux_path = os.path.join(flux_simulation_folder, 'input_param_SU_photonEnergy.dat')
energy_flux  = np.loadtxt(en_flux_path)

# load RP simulations results
folder_name  = rp_simulation_folder
oe           = 'DetectorAtFocus'
rp_path      = os.path.join(rp_simulation_folder, oe+'_RawRaysOutgoing.dat')
rp           = pd.read_csv(rp_path, sep='\t')
en_rp_path   = os.path.join(rp_simulation_folder, 'input_param_SU_photonEnergy.dat')
energy_rp    = np.loadtxt(en_rp_path)




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



# BEAMLINE TRANSMISSION
ax = axs[0,1]

ss = energy_flux.shape[0]
ind=0
for ind, es in enumerate(varying_var):
    ax.plot(energy_flux,flux['PercentageRaysSurvived'][ss*ind:ss*(ind+1)], colors[ind], label=f'{varying_var_n} {es} {varying_var_unit}' )

ax.set_xlabel(r'Energy [eV]')
ax.set_ylabel('Transmission [%]')
ax.set_title('Available Flux [in transmitted bandwidth]')
ax.grid(which='both', axis='both')
ax.legend()



# BANDWIDTH
ax = axs[1,0]
ss = energy_rp.shape[0]

for ind, es in enumerate(varying_var):
    ax.plot(energy_rp,1000*rp['Bandwidth'][ss*ind:ss*(ind+1)],colors[ind])#,label=f'{varying_var_n} {es} {varying_var_unit}')


ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Transmitted Bandwidth [meV]')
ax.set_title('Transmitted Bandwidth (tbw)')
ax.grid(which='both', axis='both')
# ax.set_yscale('log')
ax.legend()


# RESOLVING POWER
ax = axs[1,1]

# plot and deal with bandwidth=0 case.
for ind, es in enumerate(varying_var):
    try:
        res_p = energy_rp / rp['Bandwidth'][ss * ind:ss * (ind + 1)]
    except ZeroDivisionError:
        res_p = 0
    inf_indices = np.where(np.isinf(rp))[0]
    if len(inf_indices)>0:
        print(f"For {varying_var_n} size {ss}, you have zero bandwidth starting at E={energy_rp[inf_indices[0]]} eV.")
    ax.plot(energy_rp, res_p, colors[ind], label=f'{varying_var_n} {es} {varying_var_unit}')

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('RP [a.u.]')
ax.set_title('Resolving Power')
ax.grid(which='both', axis='both')
ax.legend()

# HORIZONTAL FOCUS
ax = axs[2,0]
for ind, es in enumerate(varying_var):
    ax.plot(energy_rp,1000*rp['HorizontalFocusFWHM'][ss*ind:ss*(ind+1)],colors[ind],label=f'{varying_var_n} {es} {varying_var_unit}')

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Focus Size [um]')
ax.set_title('Horizontal Focus')
ax.legend()

# # VERTICAL FOCUS
ax = axs[2,1]
for ind, es in enumerate(varying_var):
    ax.plot(energy_rp,1000*rp['VerticalFocusFWHM'][ss*ind:ss*(ind+1)],colors[ind],label=f'{varying_var_n} {es} {varying_var_unit}')

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Focus Size [um]')
ax.set_title('Vertical Focus')

plt.tight_layout()
#plt.savefig('plot/FluxRpFocus'+rml_file_name+'.png')
plt.savefig('plot/FluxRpFocus'+rml_file_name+'.pdf')

# plt.show()


# # PERMIL BANDWIDTH
# ax = axs[0]
# for ind, es_size in enumerate(SlitSize):
#     filtered_rp = rp[rp['ExitSlit.totalHeight'] == es_size]
#     energy = filtered_rp['Dipole.photonEnergy']
#     bw = filtered_rp['Bandwidth']
#     ax.plot(energy/1000,energy/(1000*bw) )
# 
# ax.set_xlabel('Energy [keV]')
# ax.set_ylabel('Energy/1000/bandwidth [a.u.]')
# ax.set_title('PerMil Transmission')
# ax.grid(which='both', axis='both')
# 
# 
# # PERMIL FLUX 
# ax = axs[1]
# for ind, es_size in enumerate(SlitSize):
#     filtered_flux = flux[flux['ExitSlit.totalHeight'] == es_size]
#     energy = filtered_flux['Dipole.photonEnergy']
#     abs_flux = filtered_flux['PhotonFlux']
#     filtered_rp = rp[rp['ExitSlit.totalHeight'] == es_size]
#     bw = filtered_rp['Bandwidth']
#     ax.plot(energy,(energy/1000/bw)*abs_flux)
# 
# ax.set_xlabel(r'Energy [eV]')
# ax.set_ylabel('Flux [ph/s/tbw]')
# ax.set_title('Transmission / Per MIl bandwidth')
# ax.grid(which='both', axis='both')
# 
# plt.suptitle('PGM-Dipole, 2400 l/mm blazed grating + ML')
# plt.tight_layout()
# plt.savefig('plot/PGM-2400-ML-Dipole-PerMil.pdf')