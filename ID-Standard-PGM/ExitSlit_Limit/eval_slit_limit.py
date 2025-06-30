import os
import matplotlib.pyplot as plt
import pandas as pd


# import simulation parameters

from parameter import rml_file_name_bessy3_long_52 as rml_file_name_b2
from parameter import rml_file_name_bessy2_LoBeta_long_52 as rml_file_name_b3


# file/folder/ml index definition
rp_simulation_folder_b2 = 'RAYPy_Simulation_'+rml_file_name_b2+'_RP'
rp_simulation_folder_b3 = 'RAYPy_Simulation_'+rml_file_name_b3+'_RP'


# loading the data B2
oe = 'DetectorAtFocus' + '_RawRaysOutgoing.csv'
rp_b2 = pd.read_csv(os.path.join(rp_simulation_folder_b2, oe))

# loading the data B3
oe = 'DetectorAtFocus' + '_RawRaysOutgoing.csv'
rp_b3 = pd.read_csv(os.path.join(rp_simulation_folder_b3, oe))

# Bandwidth normalized Transmission
fig, (ax) = plt.subplots(2, 1,figsize=(15,10))

for energy in rp_b2['PhotonEnergy'].unique():
    
    # BESSY 2:
    filtered_rp_b2 = rp_b2[rp_b2['PhotonEnergy'] == energy]
    es_size_b2 = filtered_rp_b2['ExitSlit.openingHeight']  
    energy_b2 = filtered_rp_b2['PhotonEnergy']  
    bandwidth_b2 = filtered_rp_b2['Bandwidth']  
    
    
    # # BESSY 3:
    filtered_rp_b3 = rp_b3[rp_b3['PhotonEnergy'] == energy]
    es_size_b3 = filtered_rp_b3['ExitSlit.openingHeight']  
    energy_b3 = filtered_rp_b3['PhotonEnergy']  
    bandwidth_b3 = filtered_rp_b3['Bandwidth']  

    # Plot: 
    
    ax[0].plot(es_size_b2, energy_b2/bandwidth_b2, marker='o', label = f'{energy} eV')
    ax[1].plot(es_size_b3, energy_b3/bandwidth_b3, marker='o', label = f'{energy} eV')
    


# ax.legend(fontsize=16)
ax[0].minorticks_on()
ax[0].tick_params(axis='both', labelsize=14)
ax[0].grid(linestyle='dotted')
ax[0].set_xlabel('ExitSlit [µm]', fontsize=14)
ax[0].invert_xaxis()
ax[0].set_ylabel('Resolving Power', fontsize=14)
ax[0].set_ylim(20000, 70000)
ax[0].set_title('BESSY II')
ax[0].legend()

ax[1].minorticks_on()
ax[1].tick_params(axis='both', labelsize=14)
ax[1].grid(linestyle='dotted')
ax[1].set_xlabel('ExitSlit [µm]', fontsize=14)
ax[1].invert_xaxis()
ylimits = ax[0].get_ylim()
ax[1].set_ylim(ylimits)
ax[1].set_ylabel('Resolving Power', fontsize=14)
ax[1].set_title('BESSY III')
ax[1].legend()

plt.suptitle('ResolvingPower BESSY II vs. BESSY III @ Standard 56 m PGM BL', fontsize=18)
plt.tight_layout()
plt.savefig('plot/SlitLimit BESSY II vs BESSY III with standard PGM BL @ dif µm ExitSlit.png')
plt.show()