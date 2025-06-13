import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 

# path to xrt:
import os, sys; sys.path.append(os.path.join('..', '..', '..'))  # analysis:ignore
import xrt.backends.raycing.materials as rm

# raypyng 
from raypyng.postprocessing import PostProcessAnalyzed

# from helper library
from helper_lib import get_reflectivity


from params import ml_sim_name, hb_1200_sim_name, hb_400_sim_name

ppa = PostProcessAnalyzed()
mov_av = ppa.moving_average


flux_simulation_folder_2400 = 'RAYPy_Simulation_' + ml_sim_name
flux_simulation_folder_1200 = 'RAYPy_Simulation_' + hb_1200_sim_name
flux_simulation_folder_400 = 'RAYPy_Simulation_' + hb_400_sim_name





# loading the data
oe = 'DetectorAtFocus' + '_RawRaysOutgoing.csv'
flux_2400 = pd.read_csv(os.path.join(flux_simulation_folder_2400, oe))
flux_1200 = pd.read_csv(os.path.join(flux_simulation_folder_1200, oe))
flux_400 = pd.read_csv(os.path.join(flux_simulation_folder_400, oe))

# define energy regions
flux_2400 = flux_2400[(flux_2400['Dipole.photonEnergy'] >= 50) & (flux_2400['Dipole.photonEnergy'] <= 4500)]
flux_1200 = flux_1200[(flux_1200['Dipole.photonEnergy'] >= 50) & (flux_1200['Dipole.photonEnergy'] <= 1800)]
flux_400 = flux_400[(flux_400['Dipole.photonEnergy'] >= 50) & (flux_400['Dipole.photonEnergy'] <= 1800)]
# source flux
source_flux = flux_2400.drop_duplicates(subset='Dipole.photonEnergy')[['Dipole.photonEnergy', 'SourcePhotonFlux']]


# plotting Flux and RP
fig, (axs) = plt.subplots(4, 2,figsize=(24,24))



# MIRROR COATING
table = 'Henke'
E = np.arange(source_flux['Dipole.photonEnergy'].iloc[0],
              source_flux['Dipole.photonEnergy'].iloc[-1],
              0.005)
Ir  = rm.Material('Ir',  rho=22.56, kind='mirror',table=table)
Cr  = rm.Material('Cr',  rho=7.15,  kind='mirror',table=table)
B4C = rm.Material('C', rho=2.52,  kind='mirror',  table=table)
IrCrB4C = rm.Multilayer( tLayer=B4C, tThickness=40, 
                        bLayer=Cr, bThickness=60, 
                        nPairs=1, substrate=Ir)
IrCrB4C, _ = get_reflectivity(IrCrB4C, E=E, theta=1.0)

ax=axs[0,0]
ax.plot(E, IrCrB4C, label='IrCrB4C@1.0°')

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Reflectivity [a.u.]')
ax.set_title('Mirror Coating Reflectivity at 1.0° ')
ax.legend()

# Dipole Flux
ax = axs[0,1]
ax.set_title('Dipole Flux')
ax.grid(which='both', axis='both')
ax.plot(source_flux['Dipole.photonEnergy'],
        source_flux['SourcePhotonFlux'],
        label='Dipole Flux')
ax.set_ylabel('Flux [ph/s/0.1%bw]')

ax.legend(loc=6)


# AVAILABLE FLUX 
ax = axs[1,0]

# 2400 l/mm
energy = flux_2400['Dipole.photonEnergy']
abs_flux = flux_2400['PhotonFlux']
ax.plot(energy, abs_flux, label='2400 l/mm')
# 1200 l/mm
energy = flux_1200['Dipole.photonEnergy']
abs_flux = flux_1200['PhotonFlux']
ax.plot(energy, abs_flux, label='1200 l/mm')
# 400 l/mm
energy = flux_400['Dipole.photonEnergy']
abs_flux = flux_400['PhotonFlux']
ax.plot(energy, abs_flux, label='400 l/mm')

ax.set_xlabel(r'Energy [eV]')
ax.set_ylabel('Flux [ph/s/tbw]')
ax.legend()

# FLUX DENSITY
ax = axs[1,1]
window=20

# 2400 l/mm
energy = mov_av(flux_2400['Dipole.photonEnergy'], window)
abs_flux = flux_2400['PhotonFlux']
focx = flux_2400['HorizontalFocusFWHM']*1000  # convert to um
focy = flux_2400['VerticalFocusFWHM']*1000  # convert to um
flux_density = mov_av(abs_flux / (focx * focy), window)
ax.plot(energy, flux_density, label='2400 l/mm')
# 1200 l/mm
energy = mov_av(flux_1200['Dipole.photonEnergy'], window)
abs_flux = flux_1200['PhotonFlux']
focx = flux_1200['HorizontalFocusFWHM']*1000  # convert to um
focy = flux_1200['VerticalFocusFWHM']*1000  # convert to um
flux_density = mov_av(abs_flux / (focx * focy), window)
ax.plot(energy, flux_density, label='1200 l/mm')
# 400 l/mm
energy = mov_av(flux_400['Dipole.photonEnergy'], window)
abs_flux = flux_400['PhotonFlux']
focx = flux_400['HorizontalFocusFWHM']*1000  # convert to um
focy = flux_400['VerticalFocusFWHM']*1000  # convert to um
flux_density = mov_av(abs_flux / (focx * focy), window)
ax.plot(energy, flux_density, label='400 l/mm')

ax.set_xlabel(r'Energy [eV]')
ax.set_ylabel('Flux [ph/s/tbw/µm²]')
ax.set_title('Flux Density')
ax.legend()

# BANDWIDTH
ax = axs[2,0]
window = 20

# 2400 l/mm
energy = mov_av(flux_2400['Dipole.photonEnergy'], window)
bw = mov_av(flux_2400['Bandwidth'], window)
ax.plot(energy,bw, label=f'2400 l/mm' )
# 1200 l/mm
energy = mov_av(flux_1200['Dipole.photonEnergy'], window)
bw = mov_av(flux_1200['Bandwidth'], window)
ax.plot(energy,bw, label=f'1200 l/mm' )
# 400 l/mm
energy = mov_av(flux_400['Dipole.photonEnergy'], window)
bw = mov_av(flux_400['Bandwidth'], window)
ax.plot(energy,bw, label=f'400 l/mm' )


ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Transmitted Bandwidth [eV]')
ax.set_title('Transmitted bandwidth (tbw)')
ax.grid(which='both', axis='both')
# ax.legend()


# RESOLVING POWER
ax = axs[2,1]
window = 20

# 2400 l/mm
energy = mov_av(flux_2400['Dipole.photonEnergy'], window)
bw = mov_av(flux_2400['Bandwidth'], window)
ax.plot(energy,energy/bw, label=f'2400 l/mm')
# 1200 l/mm
energy = mov_av(flux_1200['Dipole.photonEnergy'], window)
bw = mov_av(flux_1200['Bandwidth'], window)
ax.plot(energy,energy/bw, label=f'1200 l/mm')
# 400 l/mm
energy = mov_av(flux_400['Dipole.photonEnergy'], window)
bw = mov_av(flux_400['Bandwidth'], window)
ax.plot(energy,energy/bw, label=f'400 l/mm')

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('RP [a.u.]')
ax.set_title('Resolving Power')
ax.grid(which='both', axis='both')

# HORIZONTAL FOCUS
ax = axs[3,0]
window = 20


# 2400 l/mm
energy = mov_av(flux_2400['Dipole.photonEnergy'], window)
focx = mov_av(flux_2400['HorizontalFocusFWHM'], window)
ax.plot(energy,focx*1000, label=f'2400 l/mm' )
# 1200 l/mm
energy = mov_av(flux_1200['Dipole.photonEnergy'], window)
focx = mov_av(flux_1200['HorizontalFocusFWHM'], window)
ax.plot(energy,focx*1000, label=f'1200 l/mm' )
# 400 l/mm
energy = mov_av(flux_400['Dipole.photonEnergy'], window)
focx = mov_av(flux_400['HorizontalFocusFWHM'], window)
ax.plot(energy,focx*1000, label=f'400 l/mm' )

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Focus Size [um]')
ax.set_title('Horizontal focus')

# VERTICAL FOCUS
ax = axs[3,1]
window = 20 

# 2400 l/mm
energy = mov_av(flux_2400['Dipole.photonEnergy'], window)
focy = mov_av(flux_2400['VerticalFocusFWHM'], window)
ax.plot(energy,focy*1000, label=f'2400 l/mm')
# 1200 l/mm
energy = mov_av(flux_1200['Dipole.photonEnergy'], window)
focy = mov_av(flux_1200['VerticalFocusFWHM'], window)
ax.plot(energy,focy*1000, label=f'1200 l/mm')
# 400 l/mm
energy = mov_av(flux_400['Dipole.photonEnergy'], window)
focy = mov_av(flux_400['VerticalFocusFWHM'], window)
ax.plot(energy,focy*1000, label=f'400 l/mm')

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Focus Size [um]')
ax.set_title('Vertical focus')

# plt.suptitle(f'Dipole-PGM @ BIII, Slit Size {100} um, cff 2.25')
plt.tight_layout()
plt.savefig('plot/Dipole-PGM.png')
plt.show()