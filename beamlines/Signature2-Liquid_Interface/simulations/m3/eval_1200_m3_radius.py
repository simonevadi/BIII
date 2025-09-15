import os
import matplotlib.pyplot as plt
import pandas as pd

from parameter import cff_1200

from raypyng.postprocessing import PostProcessAnalyzed

p = PostProcessAnalyzed()
mov_av = p.moving_average
##############################################################
# LOAD IN DATA

# Read CSV-File of the Beamline Simulation
BL_file_path = os.path.join('RAYPy_Simulation_elisa_1200_m3_radius', 'ExitSlit_RawRaysOutgoing.csv')
BL_df_all = pd.read_csv(BL_file_path)

##############################################################
# PLOTTING AND ANALYSIS
# Create the Main figure
fig, (axs) = plt.subplots(1, 1, figsize=(20, 15))
fig.suptitle('elisa, 1200 l/mm, M3 radius and focus Size at Exit Slit', size=16)

# Vertical Focus Size
for cff in cff_1200:
    BL_df = BL_df_all[BL_df_all['PG.cFactor'] == cff]
    axs.plot(BL_df['M3.radius'],
            BL_df['VerticalFocusFWHM'],
            label=f'{cff}')

axs.set_title('Vertical Focus Size')
axs.set_xlabel('Radius [mm]')
axs.set_ylabel('[µm]')
axs.legend()
axs.minorticks_on()
axs.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


##############################################################
# SAVING
# Ensure the "plot" folder exists
plot_folder = 'plot'
if not os.path.exists(plot_folder):
    os.makedirs(plot_folder)

# Save the the figure
plt.tight_layout()
plt.savefig('plot/elisa_1200_m3_radius.png')
# plt.show()
