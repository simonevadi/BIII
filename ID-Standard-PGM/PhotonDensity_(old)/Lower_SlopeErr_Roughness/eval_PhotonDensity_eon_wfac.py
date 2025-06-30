import matplotlib.pyplot as plt
import pandas as pd


# Read CSV-File
# errors normal
simdata_B2lo_eon = pd.read_csv('RAYPy_Simulation_bessy2lo_56m_PGM_2Perc_coupling_errors_on_FLUX/DetectorAtFocus_RawRaysOutgoing.csv')
simdata_B2hi_eon = pd.read_csv('RAYPy_Simulation_bessy2hi_56m_PGM_2Perc_coupling_errors_on_FLUX/DetectorAtFocus_RawRaysOutgoing.csv')
simdata_B3_eon = pd.read_csv('RAYPy_Simulation_bessy3_56m_PGM_2Perc_coupling_errors_on_FLUX/DetectorAtFocus_RawRaysOutgoing.csv')

# errors factor 5 better 
simdata_B2lo_eon_fac5 = pd.read_csv('RAYPy_Simulation_bessy2lo_56m_PGM_2Perc_coupling_errors_on_fac5_FLUX/DetectorAtFocus_RawRaysOutgoing.csv')
simdata_B2hi_eon_fac5 = pd.read_csv('RAYPy_Simulation_bessy2hi_56m_PGM_2Perc_coupling_errors_on_fac5_FLUX/DetectorAtFocus_RawRaysOutgoing.csv')
simdata_B3_eon_fac5 = pd.read_csv('RAYPy_Simulation_bessy3_56m_PGM_2Perc_coupling_errors_on_fac5_FLUX/DetectorAtFocus_RawRaysOutgoing.csv')

# errors factor 10 better 
simdata_B2lo_eon_fac10 = pd.read_csv('RAYPy_Simulation_bessy2lo_56m_PGM_2Perc_coupling_errors_on_fac10_FLUX/DetectorAtFocus_RawRaysOutgoing.csv')
simdata_B2hi_eon_fac10 = pd.read_csv('RAYPy_Simulation_bessy2hi_56m_PGM_2Perc_coupling_errors_on_fac10_FLUX/DetectorAtFocus_RawRaysOutgoing.csv')
simdata_B3_eon_fac10 = pd.read_csv('RAYPy_Simulation_bessy3_56m_PGM_2Perc_coupling_errors_on_fac10_FLUX/DetectorAtFocus_RawRaysOutgoing.csv')

ExitSlitSize = 0.016 
fig, ax = plt.subplots(1, 1,figsize=(12,10))


ExitSlit_list = simdata_B2lo_eon['ExitSlit.openingHeight'].unique()
for ExitSlit in ExitSlit_list:
    if ExitSlit != ExitSlitSize:
        continue

    # BESSY II LoBeta normal
    reduced_simdata_B2lo_eon = simdata_B2lo_eon[simdata_B2lo_eon['ExitSlit.openingHeight']==ExitSlit]
    energy_B2lo_eon = reduced_simdata_B2lo_eon['SU.photonEnergy']
    N_rays_B2lo_eon = reduced_simdata_B2lo_eon['PercentageRaysSurvived']
    vf_B2lo_eon = reduced_simdata_B2lo_eon['VerticalFocusFWHM']
    hf_B2lo_eon = reduced_simdata_B2lo_eon['HorizontalFocusFWHM']
    PhotonDensity_B2lo_eon = N_rays_B2lo_eon/((vf_B2lo_eon*hf_B2lo_eon)*1000)       # divided by 1000 to get [nm]; number of ph divided by an area

    # BESSY II HiBeta normal
    reduced_simdata_B2hi_eon = simdata_B2hi_eon[simdata_B2hi_eon['ExitSlit.openingHeight']==ExitSlit]
    energy_B2hi_eon = reduced_simdata_B2hi_eon['SU.photonEnergy']
    N_rays_B2hi_eon = reduced_simdata_B2hi_eon['PercentageRaysSurvived']
    vf_B2hi_eon = reduced_simdata_B2hi_eon['VerticalFocusFWHM']
    hf_B2hi_eon = reduced_simdata_B2hi_eon['HorizontalFocusFWHM']
    PhotonDensity_B2hi_eon = N_rays_B2hi_eon/((vf_B2hi_eon*hf_B2hi_eon)*1000)

    # BESSY III normal 
    reduced_simdata_B3_eon = simdata_B3_eon[simdata_B3_eon['ExitSlit.openingHeight']==ExitSlit]
    energy_B3_eon = reduced_simdata_B3_eon['SU.photonEnergy']
    N_rays_B3_eon = reduced_simdata_B3_eon['PercentageRaysSurvived']
    vf_B3_eon = reduced_simdata_B3_eon['VerticalFocusFWHM']
    hf_B3_eon = reduced_simdata_B3_eon['HorizontalFocusFWHM']
    PhotonDensity_B3_eon = N_rays_B3_eon/((vf_B3_eon*hf_B3_eon)*1000)



    # BESSY II LoBeta errors factor 5 better
    reduced_simdata_B2lo_eon_fac5 = simdata_B2lo_eon_fac5[simdata_B2lo_eon_fac5['ExitSlit.openingHeight']==ExitSlit]
    energy_B2lo_eon_fac5 = reduced_simdata_B2lo_eon_fac5['SU.photonEnergy']
    N_rays_B2lo_eon_fac5 = reduced_simdata_B2lo_eon_fac5['PercentageRaysSurvived']
    vf_B2lo_eon_fac5 = reduced_simdata_B2lo_eon_fac5['VerticalFocusFWHM']
    hf_B2lo_eon_fac5 = reduced_simdata_B2lo_eon_fac5['HorizontalFocusFWHM']
    PhotonDensity_B2lo_eon_fac5 = N_rays_B2lo_eon_fac5/((vf_B2lo_eon_fac5*hf_B2lo_eon_fac5)*1000)       # divided by 1000 to get [nm]; number of ph divided by an area

    # BESSY II HiBeta errors factor 5 better
    reduced_simdata_B2hi_eon_fac5 = simdata_B2hi_eon_fac5[simdata_B2hi_eon_fac5['ExitSlit.openingHeight']==ExitSlit]
    energy_B2hi_eon_fac5 = reduced_simdata_B2hi_eon_fac5['SU.photonEnergy']
    N_rays_B2hi_eon_fac5 = reduced_simdata_B2hi_eon_fac5['PercentageRaysSurvived']
    vf_B2hi_eon_fac5 = reduced_simdata_B2hi_eon_fac5['VerticalFocusFWHM']
    hf_B2hi_eon_fac5 = reduced_simdata_B2hi_eon_fac5['HorizontalFocusFWHM']
    PhotonDensity_B2hi_eon_fac5 = N_rays_B2hi_eon_fac5/((vf_B2hi_eon_fac5*hf_B2hi_eon_fac5)*1000)

    # BESSY III errors factor 5 better
    reduced_simdata_B3_eon_fac5 = simdata_B3_eon_fac5[simdata_B3_eon_fac5['ExitSlit.openingHeight']==ExitSlit]
    energy_B3_eon_fac5 = reduced_simdata_B3_eon_fac5['SU.photonEnergy']
    N_rays_B3_eon_fac5 = reduced_simdata_B3_eon_fac5['PercentageRaysSurvived']
    vf_B3_eon_fac5 = reduced_simdata_B3_eon_fac5['VerticalFocusFWHM']
    hf_B3_eon_fac5 = reduced_simdata_B3_eon_fac5['HorizontalFocusFWHM']
    PhotonDensity_B3_eon_fac5 = N_rays_B3_eon_fac5/((vf_B3_eon_fac5*hf_B3_eon_fac5)*1000)



    # BESSY II LoBeta errors factor 10 better
    reduced_simdata_B2lo_eon_fac10 = simdata_B2lo_eon_fac10[simdata_B2lo_eon_fac10['ExitSlit.openingHeight']==ExitSlit]
    energy_B2lo_eon_fac10 = reduced_simdata_B2lo_eon_fac10['SU.photonEnergy']
    N_rays_B2lo_eon_fac10 = reduced_simdata_B2lo_eon_fac10['PercentageRaysSurvived']
    vf_B2lo_eon_fac10 = reduced_simdata_B2lo_eon_fac10['VerticalFocusFWHM']
    hf_B2lo_eon_fac10 = reduced_simdata_B2lo_eon_fac10['HorizontalFocusFWHM']
    PhotonDensity_B2lo_eon_fac10 = N_rays_B2lo_eon_fac10/((vf_B2lo_eon_fac10*hf_B2lo_eon_fac10)*1000)       # divided by 1000 to get [nm]; number of ph divided by an area

    # BESSY II HiBeta errors factor 10 better
    reduced_simdata_B2hi_eon_fac10 = simdata_B2hi_eon_fac10[simdata_B2hi_eon_fac10['ExitSlit.openingHeight']==ExitSlit]
    energy_B2hi_eon_fac10 = reduced_simdata_B2hi_eon_fac10['SU.photonEnergy']
    N_rays_B2hi_eon_fac10 = reduced_simdata_B2hi_eon_fac10['PercentageRaysSurvived']
    vf_B2hi_eon_fac10 = reduced_simdata_B2hi_eon_fac10['VerticalFocusFWHM']
    hf_B2hi_eon_fac10 = reduced_simdata_B2hi_eon_fac10['HorizontalFocusFWHM']
    PhotonDensity_B2hi_eon_fac10 = N_rays_B2hi_eon_fac10/((vf_B2hi_eon_fac10*hf_B2hi_eon_fac10)*1000)

    # BESSY III errors factor 10 better
    reduced_simdata_B3_eon_fac10 = simdata_B3_eon_fac10[simdata_B3_eon_fac10['ExitSlit.openingHeight']==ExitSlit]
    energy_B3_eon_fac10 = reduced_simdata_B3_eon_fac10['SU.photonEnergy']
    N_rays_B3_eon_fac10 = reduced_simdata_B3_eon_fac10['PercentageRaysSurvived']
    vf_B3_eon_fac10 = reduced_simdata_B3_eon_fac10['VerticalFocusFWHM']
    hf_B3_eon_fac10 = reduced_simdata_B3_eon_fac10['HorizontalFocusFWHM']
    PhotonDensity_B3_eon_fac10 = N_rays_B3_eon_fac10/((vf_B3_eon_fac10*hf_B3_eon_fac10)*1000)


    ax.plot(energy_B3_eon, PhotonDensity_B3_eon, label = 'B3 normal errors', marker='s', color='green')
    ax.plot(energy_B3_eon_fac5, PhotonDensity_B3_eon_fac5, label = '5 times better', linestyle= 'dashed', marker='s', color='darkseagreen')
       
    ax.plot(energy_B2hi_eon, PhotonDensity_B2hi_eon, label = 'B2_hibeta normal errors', marker='s', color='blue')
    ax.plot(energy_B2hi_eon_fac5, PhotonDensity_B2hi_eon_fac5, label = '5 times better', linestyle= 'dashed', marker='s', color='deepskyblue')
    
    # ax.plot(energy_B3_eon_fac10, PhotonDensity_B3_eon_fac10, label = '10 times better', marker='s', color='lightgreen')




ax.minorticks_on()
ax.grid(linestyle='dotted', color='grey')
ax.tick_params(axis='both', labelsize=14)
ax.set_ylabel ('Photon density [%/µm²]', fontsize=14)
# ax.set_ylabel(r'$\frac{N}{\mathrm{[µm^2]}} \, @ \, 0.1\% \, \mathrm{bandwidth}$' + ' in [%]', fontsize=16)
ax.set_xlabel('Energy [eV]', fontsize= 16)
ax.set_title('BESSY II vs. III @ 56 m standard PGM-BL PhotonDensity (errors on) @ 16 µm ES', fontsize= 18)
# ax.set_title('BESSY III @ 56 m standard PGM-BL bandwidth normalized transmission', fontsize= 18)
ax.legend(fontsize=16, loc='best')
plt.tight_layout()
plt.savefig('plot/Photon Density B2_B3 errors_on at 'f'{int(ExitSlitSize*1000)} mu.png')
plt.savefig('plot/Photon Density B2_B3 errors_on at 'f'{int(ExitSlitSize*1000)} mu.pdf')
plt.show()