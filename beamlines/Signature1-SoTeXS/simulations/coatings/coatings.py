import os
import matplotlib.pyplot as plt
import numpy as np
import xrt.backends.raycing.materials as rm
import warnings
warnings.filterwarnings(
    "ignore",
    message="Reading `.npy` or `.npz` file required additional header parsing as it was created on Python 2. Save the file again to speed up loading and avoid this warning."
)
from helper_lib import get_reflectivity

##############################################################
# PLOTTING AND ANALYSIS
plt.rcParams.update({'font.size': 20})  # Change 14 to any size you prefer
# Create the Main figure
fig, (axs) = plt.subplots(2, 1, figsize=(20, 15))
x_range = [500, 8000]

# MIRROR REFLECTIVITY
ax1 = axs[0]
# Coatings:
table = 'Henke'
theta = 0.4
E = np.arange(500, 8001, 0.01)
Ir  = rm.Material('Ir',  rho=22.56, kind='mirror',table=table)
Cr  = rm.Material('Cr',  rho=7.15,  kind='mirror',table=table)
B4C = rm.Material('C',   rho=2.52,  kind='mirror',table=table)


Ir_r, _ = get_reflectivity(Ir, E=E, theta=theta)
Cr_r, _ = get_reflectivity(Cr, E=E, theta=theta)
B4C_r, _ = get_reflectivity(B4C, E=E, theta=theta)

ax1.plot(E, Ir_r, 'darkgrey', label='Ir', alpha=1)
ax1.plot(E, Cr_r, 'crimson', label='Cr', alpha=1)
ax1.plot(E, B4C_r, 'forestgreen', label='B4C', alpha=1)

ax1.set_title('Ir, Cr, B4C single layer reflectivity @ 'f'{theta}° incident angle')
ax1.set_xlabel('Energy [eV]')
ax1.set_ylabel('Reflectivity [a.u.]')
ax1.legend()
ax1.set_xlim(x_range)
ax1.minorticks_on()
ax1.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')

ax1 = axs[1]


B4C_t = 4
Cr_t = 6
IrCrB4C = rm.Multilayer(tLayer=B4C, tThickness=B4C_t*10, 
                        bLayer=Cr, bThickness=Cr_t*10, 
                        nPairs=1, substrate=Ir)
IrCrB4C_r, _ = get_reflectivity(IrCrB4C, E=E, theta=theta)
ax1.plot(E, IrCrB4C_r, label=f'Ir, Cr {Cr_t}nm, B4C {B4C_t}nm', alpha=1)


B4C_t = 4
Cr_t = 0
IrCrB4C = rm.Multilayer(tLayer=B4C, tThickness=B4C_t*10, 
                        bLayer=Cr, bThickness=Cr_t*10, 
                        nPairs=1, substrate=Ir)
IrCrB4C_r, _ = get_reflectivity(IrCrB4C, E=E, theta=theta)
ax1.plot(E, IrCrB4C_r, label=f'Ir, Cr {Cr_t}nm, B4C {B4C_t}nm', alpha=1)

B4C_t = 10
Cr_t = 0
IrCrB4C = rm.Multilayer(tLayer=B4C, tThickness=B4C_t*10, 
                        bLayer=Cr, bThickness=Cr_t*10, 
                        nPairs=1, substrate=Ir)
IrCrB4C_r, _ = get_reflectivity(IrCrB4C, E=E, theta=theta)
ax1.plot(E, IrCrB4C_r, label=f'Ir, Cr {Cr_t}nm, B4C {B4C_t}nm', alpha=1)

B4C_t = 15
Cr_t = 2
IrCrB4C = rm.Multilayer(tLayer=B4C, tThickness=B4C_t*10, 
                        bLayer=Cr, bThickness=Cr_t*10, 
                        nPairs=1, substrate=Ir)
IrCrB4C_r, _ = get_reflectivity(IrCrB4C, E=E, theta=theta)
ax1.plot(E, IrCrB4C_r, label=f'Ir, Cr {Cr_t}nm, B4C {B4C_t}nm', alpha=1)


ax1.legend()

fig.suptitle('Mirror Coating Reflectivity @ 'f'{theta}° incident angle', size=25)

##############################################################
# SAVING
# Ensure the "plot" folder exists
plot_folder = 'plot'
if not os.path.exists(plot_folder):
    os.makedirs(plot_folder)

# Save the the figure
plt.tight_layout()
plt.savefig('plot/SoTeXS_coatings.png')
# plt.show()
plt.close()
