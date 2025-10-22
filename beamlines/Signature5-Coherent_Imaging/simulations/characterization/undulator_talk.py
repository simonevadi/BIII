from pathlib import Path
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

fig, (ax) = plt.subplots(1, 1, figsize=(10, 7))
harms = [1,3,5]
#######
undulator_file_path = os.path.abspath(
    os.path.join(Path(__file__).resolve().parents[4], 
                 'undulators',
                 'UndulatorFiles_BESSY_III',
                 'IVUE31',
                 'CohIm-Cryo-IVUE31-C-1.csv')
)
undulator_C = pd.read_csv(undulator_file_path)

#######
undulator_file_path = os.path.abspath(
    os.path.join(Path(__file__).resolve().parents[4], 
                 'undulators',
                 'UndulatorFiles_BESSY_III',
                 'IVUE31',
                 'CohIm-Cryo-IVUE31-HL-1.csv')
)
undulator_HL = pd.read_csv(undulator_file_path)

#######
undulator_file_path = os.path.abspath(
    os.path.join(Path(__file__).resolve().parents[4], 
                 'undulators',
                 'UndulatorFiles_BESSY_III',
                 'IVUE31',
                 'CohIm-Cryo-IVUE31-IN-1.csv')
)
undulator_IN = pd.read_csv(undulator_file_path)

#######
undulator_file_path = os.path.abspath(
    os.path.join(Path(__file__).resolve().parents[4], 
                 'undulators',
                 'UndulatorFiles_BESSY_III',
                 'IVUE31',
                 'CohIm-Cryo-IVUE31-VL-1.csv')
)
undulator_VL = pd.read_csv(undulator_file_path)

for ind,harm in enumerate(harms):
    ax.plot(undulator_C[f'Energy{harm}[eV]'], 
             undulator_C[f'Photons{harm}'],
             color='red', linestyle='solid',
             linewidth=5)
    ax.plot(undulator_HL[f'Energy{harm}[eV]'], 
             undulator_HL[f'Photons{harm}']*1,
             color='royalblue', linestyle='dashed',
             linewidth=4)
    ax.plot(undulator_IN[f'Energy{harm}[eV]'], 
             undulator_IN[f'Photons{harm}']*1,
             color='forestgreen', linestyle='dotted',
             linewidth=3)
    ax.plot(undulator_VL[f'Energy{harm}[eV]'], 
             undulator_VL[f'Photons{harm}']*1,
             color='orange', linestyle='dotted',
             linewidth=2)

def get_energy_range(df, harm):
    col = f'Energy{harm}[eV]'
    photon_col = f'Photons{harm}'
    if col in df.columns and df[photon_col].max() > 0:
        return f"{int(np.min(df[col]))} – {int(np.max(df[col]))}"
    else:
        return ""

# Create table data dynamically with safety for missing harmonics
table_data = [
    ['Circular',
     get_energy_range(undulator_C, 1),
     get_energy_range(undulator_C, 3),
     get_energy_range(undulator_C, 5),
     get_energy_range(undulator_C, 7)],

    ['Horizontal Linear',
     get_energy_range(undulator_HL, 1),
     get_energy_range(undulator_HL, 3),
     get_energy_range(undulator_HL, 5),
     get_energy_range(undulator_HL, 7)],

    ['Inclined',
     get_energy_range(undulator_IN, 1),
     get_energy_range(undulator_IN, 3),
     get_energy_range(undulator_IN, 5),
     get_energy_range(undulator_IN, 7)],

    ['Vertical Linear',
     get_energy_range(undulator_VL, 1),
     get_energy_range(undulator_VL, 3),
     get_energy_range(undulator_VL, 5),
     get_energy_range(undulator_VL, 7)]
]

# Add the table to the plot
table = ax.table(
    cellText=table_data,
    colLabels=['Polarization', 'Harm.1 [eV]', 'Harm.3 [eV]', 'Harm.5 [eV]', 'Harm.7 [eV]'],
    loc='lower left',
    cellLoc='center',
    colLoc='center'
)

# Optional styling
table.scale(0.8, 1.2)
table.auto_set_font_size(False)
table.set_fontsize(10)



custom_lines = [
    Line2D([0], [0], color='red', linestyle='solid', lw=2),
    Line2D([0], [0], color='royalblue', linestyle='solid', lw=2),
    Line2D([0], [0], color='forestgreen', linestyle='solid', lw=2),
    Line2D([0], [0], color='orange', linestyle='solid', lw=2)
]

ax.legend(custom_lines, ['Circular', 'Hor-Lin', 'Inclined', 'Ver Lin'], loc='best')

ax.set_yscale('log')
# ax.set_xscale('log')
ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Ph/s/0.3A/0.1%BW')
# ax.set_xlim(x_range)
ax.set_ylim(1e10, 1e16)
ax.set_title('Cryo IVUE31')
# Save the the figure
plt.tight_layout()
plt.savefig('plot/talk/coherence_undulator.png')
# plt.show()
plt.close()
