import matplotlib.pyplot as plt
import pandas as pd


# Read CSV-File
simdata_B2lo_eoff = pd.read_csv('RAYPy_Simulation_bessy2lo_56m_PGM_2Perc_coupling_errors_off_FLUX/DetectorAtFocus_RawRaysOutgoing.csv')
simdata_B2hi_eoff = pd.read_csv('RAYPy_Simulation_bessy2hi_56m_PGM_2Perc_coupling_errors_off_FLUX/DetectorAtFocus_RawRaysOutgoing.csv')
simdata_B3_eoff = pd.read_csv('RAYPy_Simulation_bessy3_56m_PGM_2Perc_coupling_errors_off_FLUX/DetectorAtFocus_RawRaysOutgoing.csv')

fig, (ax) = plt.subplots(1, 1,figsize=(15,10))


ExitSlit_list = simdata_B2lo_eoff['ExitSlit.openingHeight'].unique()
for ExitSlit in ExitSlit_list:
    if ExitSlit != 0.024:
        continue
    reduced_simdata_B2lo_eoff = simdata_B2lo_eoff[simdata_B2lo_eoff['ExitSlit.openingHeight']==ExitSlit]
    energy_B2lo_eoff = reduced_simdata_B2lo_eoff['SU.photonEnergy']
    N_rays_B2lo_eoff = reduced_simdata_B2lo_eoff['PercentageRaysSurvived']
    vf_B2lo_eoff = reduced_simdata_B2lo_eoff['VerticalFocusFWHM']
    hf_B2lo_eoff = reduced_simdata_B2lo_eoff['HorizontalFocusFWHM']
    PhotonDensity_B2lo_eoff = N_rays_B2lo_eoff/((vf_B2lo_eoff*hf_B2lo_eoff)*1000)       # divided by 1000 to get [nm]; number of ph divided by an area

    reduced_simdata_B2hi_eoff = simdata_B2hi_eoff[simdata_B2hi_eoff['ExitSlit.openingHeight']==ExitSlit]
    energy_B2hi_eoff = reduced_simdata_B2hi_eoff['SU.photonEnergy']
    N_rays_B2hi_eoff = reduced_simdata_B2hi_eoff['PercentageRaysSurvived']
    vf_B2hi_eoff = reduced_simdata_B2hi_eoff['VerticalFocusFWHM']
    hf_B2hi_eoff = reduced_simdata_B2hi_eoff['HorizontalFocusFWHM']
    PhotonDensity_B2hi_eoff = N_rays_B2hi_eoff/((vf_B2hi_eoff*hf_B2hi_eoff)*1000)

    reduced_simdata_B3_eoff = simdata_B3_eoff[simdata_B3_eoff['ExitSlit.openingHeight']==ExitSlit]
    energy_B3_eoff = reduced_simdata_B3_eoff['SU.photonEnergy']
    N_rays_B3_eoff = reduced_simdata_B3_eoff['PercentageRaysSurvived']
    vf_B3_eoff = reduced_simdata_B3_eoff['VerticalFocusFWHM']
    hf_B3_eoff = reduced_simdata_B3_eoff['HorizontalFocusFWHM']
    PhotonDensity_B3_eoff = N_rays_B3_eoff/((vf_B3_eoff*hf_B3_eoff)*1000)

    # Density Plot
    # lines, = ax.plot(energy_B2hi, PhotonDensity_B2hi,  label = f'B2 high beta ExitSlit {int(ExitSlit*1000)}'+' µm')
    # used_colors = lines.get_color()
    # ax.plot(energy_B2lo, PhotonDensity_B2lo,color = used_colors, label = f'B2 low beta ExitSlit {int(ExitSlit*1000)}'+' µm', marker='s')

    # ax.plot(energy_B3, PhotonDensity_B3, color = used_colors, label = f'B3 ExitSlit {int(ExitSlit*1000)}'+' µm', linestyle='dashed')

    ax.plot(energy_B2hi_eoff, PhotonDensity_B2hi_eoff, label = f'B2 (high beta) ExitSlit {int(ExitSlit*1000)}'+' µm', marker='s', color='blue')
    ax.plot(energy_B2lo_eoff, PhotonDensity_B2lo_eoff, label = f'B2 (low beta) ExitSlit {int(ExitSlit*1000)}'+' µm', marker='s', color='lightblue') 
    ax.plot(energy_B3_eoff, PhotonDensity_B3_eoff, label = f'B3 ExitSlit {int(ExitSlit*1000)}'+' µm', marker='s', color='green')

ax.minorticks_on()
ax.grid(linestyle='dotted', color='grey')
ax.tick_params(axis='both', labelsize=14)
ax.set_ylabel ('Photon density [%/µm²]', fontsize=14)
# ax.set_ylabel(r'$\frac{N}{\mathrm{[µm^2]}} \, @ \, 0.1\% \, \mathrm{bandwidth}$' + ' in [%]', fontsize=16)
ax.set_xlabel('Energy [eV]', fontsize= 16)
ax.set_title('BESSY II vs. BESSY III @ 56 m standard PGM-BL PhotonDensity (errors off)', fontsize= 18)
# ax.set_title('BESSY III @ 56 m standard PGM-BL bandwidth normalized transmission', fontsize= 18)
ax.legend(fontsize=16, loc='best')
plt.tight_layout()
plt.savefig('plot/Photon Density B2_B3 erros_off at 24 mu.png')
plt.savefig('plot/Photon Density B2_B3 erros_off at 24 mu.pdf')
# plt.show()
