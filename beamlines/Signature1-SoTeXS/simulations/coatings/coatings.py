import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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
x_range = [500, 10000]

# MIRROR REFLECTIVITY
ax1 = axs[0]
# Coatings:
table = 'Henke'
theta = 0.4
E = np.arange(500, 10001, 0.01)
Ir  = rm.Material('Ir',  rho=22.56, kind='mirror',table=table)
Cr  = rm.Material('Cr',  rho=7.15,  kind='mirror',table=table)
B4C = rm.Material('C',   rho=2.52,  kind='mirror',table=table)
Ni = rm.Material('Ni',   rho=8.9,  kind='mirror',table=table)


Ir_r, _ = get_reflectivity(Ir, E=E, theta=theta)
Cr_r, _ = get_reflectivity(Cr, E=E, theta=theta)
B4C_r, _ = get_reflectivity(B4C, E=E, theta=theta)
Ni_r, _ = get_reflectivity(Ni, E=E, theta=theta)

ax1.plot(E, Ir_r, 'darkgrey', label='Ir', linewidth=5)
ax1.plot(E, Cr_r, 'crimson', label='Cr', linewidth=5)
ax1.plot(E, B4C_r, 'forestgreen', label='B4C', linewidth=5)
ax1.plot(E, Ni_r, 'violet', label='Ni', linewidth=5)

ax1.set_title('Ir, Cr, B4C single layer reflectivity @ 'f'{theta}° incident angle')
ax1.set_xlabel('Energy [eV]')
ax1.set_ylabel('Reflectivity [a.u.]')
ax1.legend(loc='center right')
ax1.set_xlim(x_range)
ax1.minorticks_on()
ax1.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# some coatings
ax1 = axs[1]

power = 6

# IR B4C
B4C_t = 10
Cr_t = 0
coating = rm.Multilayer(tLayer=B4C, tThickness=B4C_t*10, 
                        bLayer=Cr, bThickness=Cr_t*10, 
                        nPairs=1, substrate=Ir)
coating_r, _ = get_reflectivity(coating, E=E, theta=theta)
ax1.plot(E, coating_r**power, label=f'Ir 30 nm, B4C {B4C_t}nm', linewidth=5)

# Ir_Ni B4C
Ni_t = 10
for B4C_t in np.arange(4, 11, 6):
    coating = rm.Multilayer(tLayer=B4C, tThickness=B4C_t*10, 
                            bLayer=Ni, bThickness=Ni_t*10, 
                            nPairs=1, substrate=Ir)
    coating_r, _ = get_reflectivity(coating, E=E, theta=theta)
    ax1.plot(E, coating_r**power, label=f'Ir 30 nm, Ni {Ni_t} nm, B4C {B4C_t}nm',
             linewidth=5)


ax1.set_title('Different triple coatings')
ax1.set_xlabel('Energy [eV]')
ax1.set_ylabel('Reflectivity [a.u.]')
ax1.legend()
ax1.set_xlim(x_range)
ax1.minorticks_on()
ax1.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')
ax1.minorticks_on()
ax1.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')

# Add more ticks and labels
ax1.xaxis.set_major_locator(ticker.MultipleLocator(500))  # 1 tick per unit
# ax1.yaxis.set_major_locator(ticker.MultipleLocator(0.1))  # 0.1 tick per unit

ax1.xaxis.set_minor_locator(ticker.AutoMinorLocator())
# ax1.yaxis.set_minor_locator(ticker.AutoMinorLocator())

ax1.grid(True)


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


# IR B4C
fig, (axs) = plt.subplots(3, 1, figsize=(20, 25))

# individual coatings
# single coating reflectivity
ax1 = axs[0]

ax1.plot(E, Ir_r, label=f'Ir', alpha=1)
ax1.plot(E, B4C_r, label=f'B4C', alpha=1)

ax1.set_xlabel('Energy [eV]')
ax1.set_ylabel('Reflectivity [a.u.]')
ax1.legend()
ax1.set_xlim(x_range)
ax1.minorticks_on()
ax1.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')
ax1.set_title('Ir, B4C reflectivity  @ 'f'{theta}° incident angle')


# single mirror and six mirror reflectivity
ax1 = axs[1]
ax2 = axs[2]
for B4C_t in np.arange(8, 12, 1):
    Cr_t = 0
    coating = rm.Multilayer(tLayer=B4C, tThickness=B4C_t*10, 
                            bLayer=Cr, bThickness=Cr_t*10, 
                            nPairs=1, substrate=Ir)
    coating_r, _ = get_reflectivity(coating, E=E, theta=theta)
    ax1.plot(E, coating_r, label=f'Ir, B4C {B4C_t}nm', alpha=1)
    ax2.plot(E, coating_r**power, label=f'Ir, B4C {B4C_t}nm', alpha=1)


ax1.set_title('Ir, Cr, B4C single mirror reflectivity @ 'f'{theta}° incident angle')
ax1.set_xlabel('Energy [eV]')
ax1.set_ylabel('Reflectivity [a.u.]')
ax1.legend()
ax1.set_xlim(x_range)
ax1.minorticks_on()
ax1.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


ax2.set_title('Ir, Cr, B4C six mirror reflectivity @ 'f'{theta}° incident angle')
ax2.set_xlabel('Energy [eV]')
ax2.set_ylabel('Reflectivity [a.u.]')
ax2.legend()
ax2.set_xlim(x_range)
ax2.minorticks_on()
ax2.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


fig.suptitle('Ir-B4C @ 'f'{theta}° incident angle', size=25)

plt.tight_layout()
plt.savefig('plot/SoTeXS_coatings_Ir_B4C.png')



# IR Cr B4C
fig, (axs) = plt.subplots(3, 1, figsize=(20, 25))

# individual coatings
# single coating reflectivity
ax1 = axs[0]

ax1.plot(E, Ir_r, label=f'Ir', alpha=1)
ax1.plot(E, Cr_r, label=f'Ir', alpha=1)
ax1.plot(E, B4C_r, label=f'B4C', alpha=1)

ax1.set_xlabel('Energy [eV]')
ax1.set_ylabel('Reflectivity [a.u.]')
ax1.legend()
ax1.set_xlim(x_range)
ax1.minorticks_on()
ax1.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')
ax1.set_title(f'Ir, B4C reflectivity  @ 'f'{theta}° incident angle')


# single mirror and six mirror reflectivity
ax1 = axs[1]
ax2 = axs[2]
Cr_t = 4
for B4C_t in np.arange(8, 12, 1):
    coating = rm.Multilayer(tLayer=B4C, tThickness=B4C_t*10, 
                            bLayer=Cr, bThickness=Cr_t*10, 
                            nPairs=1, substrate=Ir)
    coating_r, _ = get_reflectivity(coating, E=E, theta=theta)
    ax1.plot(E, coating_r, label=f'Ir, Cr {Cr_t} nm, B4C {B4C_t}nm', alpha=1)
    ax2.plot(E, coating_r**power, label=f'Ir, Cr {Cr_t} nm, B4C {B4C_t}nm', alpha=1)


ax1.set_title('Ir, Cr, B4C single mirror reflectivity @ 'f'{theta}° incident angle')
ax1.set_xlabel('Energy [eV]')
ax1.set_ylabel('Reflectivity [a.u.]')
ax1.legend()
ax1.set_xlim(x_range)
ax1.minorticks_on()
ax1.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


ax2.set_title(f'Ir, Cr, B4C six mirror reflectivity @ 'f'{theta}° incident angle')
ax2.set_xlabel('Energy [eV]')
ax2.set_ylabel('Reflectivity [a.u.]')
ax2.legend()
ax2.set_xlim(x_range)
ax2.minorticks_on()
ax2.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


fig.suptitle('Ir-B4C @ 'f'{theta}° incident angle', size=25)

plt.tight_layout()
plt.savefig('plot/SoTeXS_coatings_Ir_Cr_B4C.png')


# IR Ni B4C
fig, (axs) = plt.subplots(3, 1, figsize=(20, 25))

# individual coatings
# single coating reflectivity
ax1 = axs[0]

ax1.plot(E, Ir_r, label=f'Ir', alpha=1)
ax1.plot(E, Ni_r, label=f'Ir', alpha=1)
ax1.plot(E, B4C_r, label=f'B4C', alpha=1)

ax1.set_xlabel('Energy [eV]')
ax1.set_ylabel('Reflectivity [a.u.]')
ax1.legend()
ax1.set_xlim(x_range)
ax1.minorticks_on()
ax1.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')
ax1.set_title(f'Ir,Ni,  B4C reflectivity  @ 'f'{theta}° incident angle')


# single mirror and six mirror reflectivity
ax1 = axs[1]
ax2 = axs[2]
Ni_t = 10
for B4C_t in np.arange(4, 11, 2):
    coating = rm.Multilayer(tLayer=B4C, tThickness=B4C_t*10, 
                            bLayer=Ni, bThickness=Ni_t*10, 
                            nPairs=1, substrate=Ir)
    coating_r, _ = get_reflectivity(coating, E=E, theta=theta)
    ax1.plot(E, coating_r, label=f'Ir, Cr {Ni_t} nm, B4C {B4C_t}nm', alpha=1)
    ax2.plot(E, coating_r**power, label=f'Ir, Ni {Ni_t} nm, B4C {B4C_t}nm', alpha=1)


ax1.set_title('Ir, Ni, B4C single mirror reflectivity @ 'f'{theta}° incident angle')
ax1.set_xlabel('Energy [eV]')
ax1.set_ylabel('Reflectivity [a.u.]')
ax1.legend()
ax1.set_xlim(x_range)
ax1.minorticks_on()
ax1.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


ax2.set_title(f'Ir, Ni, B4C six mirror reflectivity @ 'f'{theta}° incident angle')
ax2.set_xlabel('Energy [eV]')
ax2.set_ylabel('Reflectivity [a.u.]')
ax2.legend()
ax2.set_xlim(x_range)
ax2.minorticks_on()
ax2.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


fig.suptitle('Ir-Ni-B4C @ 'f'{theta}° incident angle', size=25)

plt.tight_layout()
plt.savefig('plot/SoTeXS_coatings_Ir_Ni_B4C.png')


plt.close()
