import numpy as np
from scipy.interpolate import UnivariateSpline
import matplotlib.pyplot as plt
# path to xrt:
import os, sys; sys.path.append(os.path.join('..', '..', '..'))  # analysis:ignore
import xrt.backends.raycing.materials as rm

crystal = rm.CrystalSi(hkl=(1, 1, 1))
reflectivity_1_list = []
reflectivity_2_list = []
energy_list = np.arange(2500, 40000, 1000)
for energy in energy_list:
    dtheta = np.linspace(-250, 500, 10000)
    dt = dtheta[1] - dtheta[0]
    theta = crystal.get_Bragg_angle(energy) + dtheta*1e-6
    refl = np.abs(crystal.get_amplitude(energy, np.sin(theta))[0])**2  # s-polarization
    spline = UnivariateSpline(dtheta, refl-refl.max()/2, s=0)
    r11, r12 = spline.roots()  # find the roots

    rc = np.convolve(refl, refl, 'same') / (refl.sum()*dt) * dt
    spline = UnivariateSpline(dtheta, rc-rc.max()/2, s=0)
    r21, r22 = spline.roots()  # find the roots
    reflectivity_1_list.append(np.max(refl))
    reflectivity_2_list.append(np.max(rc))
    plt.plot(dtheta, refl, 'r', label=u'one crystal\nFWHM = {0:.1f} µrad'.format(
        crystal.get_Darwin_width(energy)*1e6))
    plt.axvspan(r11, r12, facecolor='r', alpha=0.05)
    plt.plot(dtheta, rc, 'b', label=u'two crystal (conv)'
            u'\nFWHM = {0:.1f} µrad'.format(r22-r21))
    plt.gca().set_xlabel(u'$\\theta - \\theta_{B}$ (µrad)')
    plt.gca().set_ylabel(r'reflectivity')
    plt.axvspan(r21, r22, facecolor='b', alpha=0.05)
    plt.legend(loc='upper right', fontsize=12)
    plt.gca().set_xlim(dtheta[0], dtheta[-1])

    text = u'Rocking curve of {0}{1[0]}{1[1]}{1[2]} at energy={2:.0f} eV'.format(
        crystal.name, crystal.hkl, energy)
    plt.text(0.5, 1.02, text, transform=plt.gca().transAxes, size=15, ha='center')
    plt.savefig(f'plot/crystal/Si111/individual/crystal_{energy}.png')
    plt.close()

plt.figure()
plt.plot(energy_list, reflectivity_1_list, label='one crystal')
plt.plot(energy_list, reflectivity_2_list, label='two crystal (conv)')
plt.xlabel('Energy [eV]')
plt.ylabel('Reflectivity [a.u.]')
plt.title('Si111')
plt.legend()
plt.savefig('plot/crystal/Si111/Si111.png')
plt.close()


##################
crystal = rm.CrystalSi(hkl=(3, 1, 1))
reflectivity_1_list = []
reflectivity_2_list = []
energy_list = np.arange(4000, 40000, 1000)
for energy in energy_list:
    dtheta = np.linspace(-250, 500, 10000)
    dt = dtheta[1] - dtheta[0]
    theta = crystal.get_Bragg_angle(energy) + dtheta*1e-6
    refl = np.abs(crystal.get_amplitude(energy, np.sin(theta))[0])**2  # s-polarization
    spline = UnivariateSpline(dtheta, refl-refl.max()/2, s=0)
    r11, r12 = spline.roots()  # find the roots

    rc = np.convolve(refl, refl, 'same') / (refl.sum()*dt) * dt
    spline = UnivariateSpline(dtheta, rc-rc.max()/2, s=0)
    r21, r22 = spline.roots()  # find the roots
    reflectivity_1_list.append(np.max(refl))
    reflectivity_2_list.append(np.max(rc))
    plt.plot(dtheta, refl, 'r', label=u'one crystal\nFWHM = {0:.1f} µrad'.format(
        crystal.get_Darwin_width(energy)*1e6))
    plt.axvspan(r11, r12, facecolor='r', alpha=0.05)
    plt.plot(dtheta, rc, 'b', label=u'two crystal (conv)'
            u'\nFWHM = {0:.1f} µrad'.format(r22-r21))
    plt.gca().set_xlabel(u'$\\theta - \\theta_{B}$ (µrad)')
    plt.gca().set_ylabel(r'reflectivity')
    plt.axvspan(r21, r22, facecolor='b', alpha=0.05)
    plt.legend(loc='upper right', fontsize=12)
    plt.gca().set_xlim(dtheta[0], dtheta[-1])

    text = u'Rocking curve of {0}{1[0]}{1[1]}{1[2]} at energy={2:.0f} eV'.format(
        crystal.name, crystal.hkl, energy)
    plt.text(0.5, 1.02, text, transform=plt.gca().transAxes, size=15, ha='center')
    plt.savefig(f'plot/crystal/Si311/individual/crystal_{energy}.png')
    plt.close()

plt.figure()
plt.plot(energy_list, reflectivity_1_list, label='one crystal')
plt.plot(energy_list, reflectivity_2_list, label='two crystal (conv)')
plt.xlabel('Energy [eV]')
plt.ylabel('Reflectivity [a.u.]')
plt.title('Si311')
plt.legend()
plt.savefig('plot/crystal/Si311/Si311.png')
plt.close()