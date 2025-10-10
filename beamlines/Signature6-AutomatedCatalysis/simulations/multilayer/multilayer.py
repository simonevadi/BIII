import numpy as np
import matplotlib.pyplot as plt
import os

# path to xrt:
import os, sys; sys.path.append(os.path.join('..', '..', '..'))  # analysis:ignore
import xrt.backends.raycing.materials as rm
from helper_lib import get_reflectivity


os.makedirs('plot/multilayer', exist_ok=True)


# plotting Flux and RP
fig, (ax) = plt.subplots(1, 1,figsize=(10,10))



# MIRROR COATING
C = rm.Material('C', rho=2.2)
W = rm.Material('W', rho=19.3)
Si = rm.Material('Si', rho=2.65)

mL = rm.Multilayer(tLayer=C, tThickness=10, 
                        bLayer=W, bThickness=8, 
                        nPairs=100, substrate=Si)
energy = 8000
theta = np.linspace(0, 1.7, 10001)  # degrees
rs, rp = mL.get_amplitude(energy, np.sin(np.deg2rad(theta)))[0:2]

ax.plot(theta, abs(rs)**2, 'r')
ax.plot(theta, abs(rp)**2, 'b')

ax.set_xlabel('Theta [eV]')
ax.set_ylabel('Reflectivity [a.u.]')
ax.set_title(f'Multilayer Reflectivity at {energy} eV')
ax.legend()



plt.suptitle('Multilayer reflectivity')
plt.tight_layout()
plt.savefig(f'plot/multilayer/multilayer_reflectivity_{energy}eV.png')


