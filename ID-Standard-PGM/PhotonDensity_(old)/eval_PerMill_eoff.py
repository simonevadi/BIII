import matplotlib.pyplot as plt
import pandas as pd


# Read CSV-File
simdata_B2lo_eoff = pd.read_csv('RAYPy_Simulation_bessy2lo_56m_PGM_2Perc_coupling_errors_off_FLUX/DetectorAtFocus_RawRaysOutgoing.csv')
simdata_B2hi_eoff = pd.read_csv('RAYPy_Simulation_bessy2hi_56m_PGM_2Perc_coupling_errors_off_FLUX/DetectorAtFocus_RawRaysOutgoing.csv')
simdata_B3_eoff = pd.read_csv('RAYPy_Simulation_bessy3_56m_PGM_2Perc_coupling_errors_off_FLUX/DetectorAtFocus_RawRaysOutgoing.csv')

ExitSlitSize = 0.024

fig, ax = plt.subplots(2, 1,figsize=(12,10))

# PerMil Energy
ExitSlit_list = simdata_B2lo_eoff['ExitSlit.openingHeight'].unique()
for ExitSlit in ExitSlit_list:
    if ExitSlit != ExitSlitSize:
        continue

    # BESSY II LoBeta
    reduced_simdata_B2lo_eoff = simdata_B2lo_eoff[simdata_B2lo_eoff['ExitSlit.openingHeight']==ExitSlit]
    energy_B2lo_eoff = reduced_simdata_B2lo_eoff['SU.photonEnergy']
    PerMilEnergy_B2lo_eoff = reduced_simdata_B2lo_eoff['EnergyPerMilPerBw']
    
    # BESSY II HiBeta
    reduced_simdata_B2hi_eoff = simdata_B2hi_eoff[simdata_B2hi_eoff['ExitSlit.openingHeight']==ExitSlit]
    energy_B2hi_eoff = reduced_simdata_B2hi_eoff['SU.photonEnergy']
    PerMilEnergy_B2hi_eoff = reduced_simdata_B2hi_eoff['EnergyPerMilPerBw']

    # BESSY III
    reduced_simdata_B3_eoff = simdata_B3_eoff[simdata_B3_eoff['ExitSlit.openingHeight']==ExitSlit]
    energy_B3_eoff = reduced_simdata_B3_eoff['SU.photonEnergy']
    PerMilEnergy_B3_eoff = reduced_simdata_B3_eoff['EnergyPerMilPerBw']
    
    ax[0].plot(energy_B2hi_eoff, PerMilEnergy_B2hi_eoff, label = f'B2 (high beta) ExitSlit {int(ExitSlit*1000)}'+' µm', marker='s', color='blue')
    ax[0].plot(energy_B2lo_eoff, PerMilEnergy_B2lo_eoff, label = f'B2 (low beta) ExitSlit {int(ExitSlit*1000)}'+' µm', marker='s', color='lightblue') 
    ax[0].plot(energy_B3_eoff, PerMilEnergy_B3_eoff, label = f'B3 ExitSlit {int(ExitSlit*1000)}'+' µm', marker='s', color='green')

ax[0].minorticks_on()
ax[0].grid(linestyle='dotted', color='grey')
ax[0].tick_params(axis='both', labelsize=14)
ax[0].set_ylabel ('Energy/1000/bw [a.u.]', fontsize=14)
# ax.set_ylabel(r'$\frac{N}{\mathrm{[µm^2]}} \, @ \, 0.1\% \, \mathrm{bandwidth}$' + ' in [%]', fontsize=16)
ax[0].set_xlabel('Energy [eV]', fontsize= 16)
ax[0].set_title('BESSY II vs. BESSY III @ 56 m standard PGM-BL PerMil bandwidth (errors off)', fontsize= 18)
# ax.set_title('BESSY III @ 56 m standard PGM-BL bandwidth normalized transmission', fontsize= 18)
ax[0].legend(fontsize=16, loc='best')



# PerMil Flux
ExitSlit_list = simdata_B2lo_eoff['ExitSlit.openingHeight'].unique()
for ExitSlit in ExitSlit_list:
    if ExitSlit != ExitSlitSize:
        continue

    # BESSY II LoBeta
    reduced_simdata_B2lo_eoff = simdata_B2lo_eoff[simdata_B2lo_eoff['ExitSlit.openingHeight']==ExitSlit]
    energy_B2lo_eoff = reduced_simdata_B2lo_eoff['SU.photonEnergy']
    PerMilFlux_B2lo_eoff = reduced_simdata_B2lo_eoff['FluxPerMilPerBwPerc']
    
    # BESSY II HiBeta
    reduced_simdata_B2hi_eoff = simdata_B2hi_eoff[simdata_B2hi_eoff['ExitSlit.openingHeight']==ExitSlit]
    energy_B2hi_eoff = reduced_simdata_B2hi_eoff['SU.photonEnergy']
    PerMilFlux_B2hi_eoff = reduced_simdata_B2hi_eoff['FluxPerMilPerBwPerc']
   
    # BESSY III
    reduced_simdata_B3_eoff = simdata_B3_eoff[simdata_B3_eoff['ExitSlit.openingHeight']==ExitSlit]
    energy_B3_eoff = reduced_simdata_B3_eoff['SU.photonEnergy']
    PerMilFlux_B3_eoff = reduced_simdata_B3_eoff['FluxPerMilPerBwPerc']
    
    ax[1].plot(energy_B2hi_eoff, PerMilFlux_B2hi_eoff, label = f'B2 (high beta) ExitSlit {int(ExitSlit*1000)}'+' µm', marker='s', color='blue')
    ax[1].plot(energy_B2lo_eoff, PerMilFlux_B2lo_eoff, label = f'B2 (low beta) ExitSlit {int(ExitSlit*1000)}'+' µm', marker='s', color='lightblue') 
    ax[1].plot(energy_B3_eoff, PerMilFlux_B3_eoff, label = f'B3 ExitSlit {int(ExitSlit*1000)}'+' µm', marker='s', color='green')


ax[1].minorticks_on()
ax[1].grid(linestyle='dotted', color='grey')
ax[1].tick_params(axis='both', labelsize=14)
ax[1].set_ylabel ('Flux [ph/s/tbw]', fontsize=14)
# ax.set_ylabel(r'$\frac{N}{\mathrm{[µm^2]}} \, @ \, 0.1\% \, \mathrm{bandwidth}$' + ' in [%]', fontsize=16)
ax[1].set_xlabel('Energy [eV]', fontsize= 16)
ax[1].set_title('BESSY II vs. BESSY III @ 56 m standard PGM-BL PerMil flux (errors off)', fontsize= 18)
# ax.set_title('BESSY III @ 56 m standard PGM-BL bandwidth normalized transmission', fontsize= 18)
# ax[1].legend(fontsize=16, loc='best')





plt.tight_layout()
plt.savefig('plot_PerMill/Photon Density B2_B3 erros_off at ' f'{int(ExitSlitSize*1000)} mu.png')
plt.savefig('plot_PerMill/Photon Density B2_B3 erros_off at ' f'{int(ExitSlitSize*1000)} mu.pdf')
# plt.show()
