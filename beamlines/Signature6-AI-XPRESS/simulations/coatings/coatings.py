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
theta = 0.11
power = 2
x_range = [500, 40000]

# MIRROR REFLECTIVITY
ax1 = axs[0]
# Coatings:
table = 'Chantler'

E = np.arange(1000, 40001, 1)
Ir  = rm.Material('Ir',  rho=22.56, kind='mirror',table=table)
Rh  = rm.Material('Rh',  rho=12.423,  kind='mirror',table=table)



Ir_r, _ = get_reflectivity(Ir, E=E, theta=theta)
Rh_r, _ = get_reflectivity(Rh, E=E, theta=theta)

ax1.plot(E, Ir_r, 'darkgrey', label='Ir', linewidth=5)
ax1.plot(E, Rh_r, 'crimson', label='Rh', linewidth=5)


ax1.set_title('Ir, Rh single layer')
ax1.set_xlabel('Energy [eV]')
ax1.set_ylabel('Reflectivity [a.u.]')
ax1.legend(loc='center right')
ax1.set_xlim(x_range)
ax1.minorticks_on()
ax1.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')
# Add more ticks and labels
ax1.xaxis.set_major_locator(ticker.MultipleLocator(5000))  # 1 tick per unit
# ax1.yaxis.set_major_locator(ticker.MultipleLocator(0.1))  # 0.1 tick per unit
ax1.xaxis.set_minor_locator(ticker.AutoMinorLocator())
# ax1.yaxis.set_minor_locator(ticker.AutoMinorLocator())
ax1.grid(True)


########################################################
# double coating vs Rh thichkness
ax1 = axs[1]
for Rh_t in range(2,5,1):
    coating = rm.Multilayer(tLayer=Rh, tThickness=Rh_t*10, 
                            bLayer=Rh, bThickness=0, 
                            nPairs=1, substrate=Ir)
    coating_r, _ = get_reflectivity(coating, E=E, theta=theta)
    ax1.plot(E, coating_r**power,
             label=f'Ir 30nm, Rh {Rh_t}nm',
             linewidth=3,
             linestyle='--' )

ax1.set_title('Ir, Rh, two mirrors')
ax1.set_xlabel('Energy [eV]')
ax1.set_ylabel('Reflectivity [a.u.]')
ax1.legend(loc='center right')
ax1.set_xlim(x_range)
ax1.minorticks_on()
ax1.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')
# Add more ticks and labels
ax1.xaxis.set_major_locator(ticker.MultipleLocator(5000))  # 1 tick per unit
# ax1.yaxis.set_major_locator(ticker.MultipleLocator(0.1))  # 0.1 tick per unit
ax1.xaxis.set_minor_locator(ticker.AutoMinorLocator())
# ax1.yaxis.set_minor_locator(ticker.AutoMinorLocator())
ax1.grid(True)


##############################################
fig.suptitle(f'Mirror Coating Reflectivity @ 'f'{theta}° incident angle, table: {table}', size=25)

##############################################################
# SAVING
# Ensure the "plot" folder exists
plot_folder = 'plot'
if not os.path.exists(plot_folder):
    os.makedirs(plot_folder)

# Save the the figure
plt.tight_layout()
plt.savefig('plot/AI-XPRESS_coatings.png')
plt.show()

plt.close()
