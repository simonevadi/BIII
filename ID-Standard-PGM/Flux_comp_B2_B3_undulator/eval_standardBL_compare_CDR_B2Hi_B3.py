import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import xrt.backends.raycing.materials as rm
import matplotlib.ticker as mticker
 
# try to import PostProcessAnalyzed, ignore if not available (e.g. on Windows)
try:
    from raypyng.postprocessing import PostProcessAnalyzed
except ImportError:
    PostProcessAnalyzed = None

from helper_lib import get_reflectivity
from parameter import SlitSize

##############################################################
# LOAD IN DATA

this_file_dir=os.path.dirname(os.path.realpath(__file__))

# Read Undulator CSV-File BESSY II HiBeta
undulator_B2Hi_table_filename = os.path.join(this_file_dir, 'undulator_flux_curves','b2_HiBeta_UE46_2025_smalerz_300mA_flux.txt')
undulator_B2Hi_df = pd.read_csv(undulator_B2Hi_table_filename, delimiter='\t')

# Read Undulator CSV-File BESSY III
undulator_B3_table_filename = os.path.join(this_file_dir, 'undulator_flux_curves','b3_ue42_5_ver_300mA_flux.csv')
undulator_B3_df = pd.read_csv(undulator_B3_table_filename)


# Read CSV-File of the Beamline Simulation
# BESSY II HiBeta
BL_B2Hi_file_path = os.path.join('RAYPy_Simulation_bessy2hi_37m_PGM_2Perc_coupl_err_on_1_5_degree_1200l_FLUX', 'DetectorAtFocus_RawRaysOutgoing.csv')
BL_B2Hi_df = pd.read_csv(BL_B2Hi_file_path)

# BESSY III
BL_B3_file_path = os.path.join('RAYPy_Simulation_bessy3_56m_PGM_2Perc_coupl_err_on0_75deg_1200l_V3_FLUX', 'DetectorAtFocus_RawRaysOutgoing.csv')
BL_B3_df = pd.read_csv(BL_B3_file_path)


##############################################################
# PLOTTING AND ANALYSIS
# Create the Main figure
fig_main, axs = plt.subplots(2, 1, figsize=(8.27, 11.69), dpi=150, sharex=False)
fig_main.suptitle('Comparison BESSY II Hi Beta vs. III Standard-PGM Beamlines', size=12)
x_range = [50, 2150]

# =====================
# Centralized font size definitions for all plots
# =====================
FONT_SIZES = {
    'title': 12,
    'axis_label': 9,
    'tick_label': 8,
    'legend': 7,
    'bar_label': 9,
    'annotation': 7
}

# Fontsizes, Linesizes:
STitle = FONT_SIZES['title']
SLabes = FONT_SIZES['axis_label']
STickLabels = FONT_SIZES['tick_label']
SLegend = FONT_SIZES['legend']
Linesize = 1.5

harms = [1,3,5] # The Harmonics from the ID. Typically 1,3,5, rather higher. Depends on the FluxSims of the ID.

# Define color for harms
colors = {1: 'darkblue', 3: 'limegreen', 5: 'darkred'}

# BEAMLINE FLUX CURVE
ax1 = axs[0]

# BESSY II HiBeta
for harm in harms:
    Emin_harm = undulator_B2Hi_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_B2Hi_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL_B2Hi_df[(BL_B2Hi_df['PhotonEnergy'] >= Emin_harm) & (BL_B2Hi_df['PhotonEnergy'] <= Emax_harm)]
    ax1.plot(filtered_df['PhotonEnergy'], filtered_df[f'PhotonFlux{harm}'], color=colors[harm], label=f'Harm. {harm} - UE46 @ BESSY II HiBeta (37 m)', linestyle='dotted', linewidth=Linesize)

# BESSY III
for harm in harms:
    Emin_harm = undulator_B3_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_B3_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL_B3_df[(BL_B3_df['PhotonEnergy'] >= Emin_harm) & (BL_B3_df['PhotonEnergy'] <= Emax_harm)]
    ax1.plot(filtered_df['PhotonEnergy'], filtered_df[f'PhotonFlux{harm}'], color=colors[harm], label=f'Harm. {harm} - UE42 @ BESSY III (56 m)', linewidth=Linesize)


ax1.set_title('Flux curves', fontsize=STitle)
ax1.set_xlabel('Energy [eV]', fontsize=SLabes)
ax1.set_ylabel('Photon flux [ph/s/300 mA/0.1 % BW]', fontsize=SLabes)
ax1.set_yscale('log')
legend = ax1.legend(loc='best', fontsize=SLegend)
legend.get_frame().set_facecolor('white')
legend.get_frame().set_alpha(1.0)
ax1.set_xlim(x_range)
ax1.minorticks_on()
ax1.tick_params(labelsize=STickLabels)
# ax1.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# Flux Density
ax2 = axs[1]

# BESSY II HiBeta
for harm in harms:
    Emin_harm = undulator_B2Hi_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_B2Hi_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL_B2Hi_df[(BL_B2Hi_df['PhotonEnergy'] >= Emin_harm) & (BL_B2Hi_df['PhotonEnergy'] <= Emax_harm)]
    foc_area = (filtered_df['VerticalFocusFWHM']*filtered_df['HorizontalFocusFWHM'])*1000  # in µm²
    ax2.plot(filtered_df['PhotonEnergy'],filtered_df[f'PhotonFlux{harm}']/foc_area, color=colors[harm], label=f'Harm. {harm} - UE46 @ BESSY II HiBeta (37 m)', linestyle='dotted', linewidth=Linesize)

# BESSY III
for harm in harms:
    Emin_harm = undulator_B3_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_B3_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL_B3_df[(BL_B3_df['PhotonEnergy'] >= Emin_harm) & (BL_B3_df['PhotonEnergy'] <= Emax_harm)]
    foc_area = (filtered_df['VerticalFocusFWHM']*filtered_df['HorizontalFocusFWHM'])*1000  # in µm²
    ax2.plot(filtered_df['PhotonEnergy'],filtered_df[f'PhotonFlux{harm}']/foc_area, color=colors[harm], label=f'Harm. {harm} - UE42 @ BESSY III (56 m)', linewidth=Linesize)


ax2.set_title('Flux Density', fontsize=STitle)
ax2.set_xlabel('Energy [eV]', fontsize=SLabes)
ax2.set_ylabel('Photons flux per µm²', fontsize=SLabes)
ax2.set_yscale('log')
# ax2.legend(loc='best', fontsize=SLegend)
ax2.set_xlim(x_range)
ax2.minorticks_on()
ax2.tick_params(labelsize=STickLabels)
# ax2.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')

##############################################################

# Insert label for interesting points
x_lines = {
    'C': 282.1,
    'O': 543.1,
    'Si': 1839,
    'S': 2472,
    'Fe': 844.6,
    'Co': 925.1,
    'Ni': 1008.6,
    'Cu': 1096.7,
    'Ga': 1299,
    'Ce': 1436
}

# Individuelle y-Offsets für bessere Lesbarkeit
label_offsets = {
    'C': 0.02,
    'O': 0.1,
    'Si': 1.3,
    'S': 0.4,
    'Fe': 0.01,
    'Co': 0.1,
    'Ni': 0.01,
    'Cu': 0.2,
    'Ga': 0.1,
    'Ce': 2.8
}

for label, x_val in x_lines.items():
    ax2.axvline(x=x_val, color='lightgrey', linestyle='--', linewidth=0.8)
    y1_vals = []
    y2_vals = []
    for harm in harms:
        y1_h = np.interp(x_val, BL_B2Hi_df['PhotonEnergy'], BL_B2Hi_df[f'PhotonFlux{harm}']/((BL_B2Hi_df['VerticalFocusFWHM']*BL_B2Hi_df['HorizontalFocusFWHM'])*1000))
        y2_h = np.interp(x_val, BL_B3_df['PhotonEnergy'], BL_B3_df[f'PhotonFlux{harm}']/((BL_B3_df['VerticalFocusFWHM']*BL_B3_df['HorizontalFocusFWHM'])*1000))
        y1_vals.append(y1_h)
        y2_vals.append(y2_h)
    y1_max = max(y1_vals)
    y2_max = max(y2_vals)
    offset = label_offsets.get(label, 1.0)
    if y1_max != 0:
        factor = y2_max / y1_max
        factor_str = f'x{factor:.1f}'
    else:
        factor_str = 'n/a'
    # Nur Element und Faktor fett, Energie normal
    label_text = f'$\\bf{{{label}}}$\n$\\bf{{{factor_str}}}$\n{x_val:.1f} eV'
    ax2.text(
        x_val,
        min(y1_max, y2_max)*offset,
        label_text,
        rotation=0,
        va='top',
        ha='center',
        fontsize=6,
        color='black',
        bbox=dict(facecolor='white', edgecolor='grey', boxstyle='round,pad=0.2', linewidth=0.8)
    )

for label, x_val in x_lines.items():
    ax1.axvline(x=x_val, color='lightgrey', linestyle='--', linewidth=0.8)
    y1_vals = []
    y2_vals = []
    for harm in harms:
        y1_h = np.interp(x_val, BL_B2Hi_df['PhotonEnergy'], BL_B2Hi_df[f'PhotonFlux{harm}'])
        y2_h = np.interp(x_val, BL_B3_df['PhotonEnergy'], BL_B3_df[f'PhotonFlux{harm}'])
        y1_vals.append(y1_h)
        y2_vals.append(y2_h)
    y1_max = max(y1_vals)
    y2_max = max(y2_vals)
    offset = label_offsets.get(label, 1.0)
    if y1_max != 0:
        factor = y2_max / y1_max
        factor_str = f'x{factor:.2f}'
    else:
        factor_str = 'n/a'
    label_text = f'$\\bf{{{label}}}$\n$\\bf{{{factor_str}}}$\n{x_val:.1f} eV'
    ax1.text(
        x_val,
        min(y1_max, y2_max)*offset,
        label_text,
        rotation=0,
        va='top',
        ha='center',
        fontsize=6,
        color='black',
        bbox=dict(facecolor='white', edgecolor='grey', boxstyle='round,pad=0.2', linewidth=0.8)
    )

# =====================
# Parameters for histogram appearance and binning
# =====================
hist_bar_color = 'green'    # Change this to any valid matplotlib color
hist_bin_width = 250        # Change this to adjust the bin width (e.g. 100, 500, etc.)
hist_x_start = 250          # Start of histogram x range
hist_x_stop = 2150          # End of histogram x range (inclusive)

# =====================
# Histogram of gain (factor) every hist_bin_width eV (Flux Density)
# =====================
x_hist = np.arange(hist_x_start, hist_x_stop + 1, hist_bin_width)
factors_density = []
for x_val in x_hist:
    y1_vals = [np.interp(x_val, BL_B2Hi_df['PhotonEnergy'], BL_B2Hi_df[f'PhotonFlux{harm}']/((BL_B2Hi_df['VerticalFocusFWHM']*BL_B2Hi_df['HorizontalFocusFWHM'])*1000)) for harm in harms]
    y2_vals = [np.interp(x_val, BL_B3_df['PhotonEnergy'], BL_B3_df[f'PhotonFlux{harm}']/((BL_B3_df['VerticalFocusFWHM']*BL_B3_df['HorizontalFocusFWHM'])*1000)) for harm in harms]
    y1_max = max(y1_vals)
    y2_max = max(y2_vals)
    if y1_max != 0:
        factor = y2_max / y1_max
    else:
        factor = np.nan
    factors_density.append(factor)

# =====================
# Histogram of gain (factor) every hist_bin_width eV (Flux)
# =====================
factors_flux = []
for x_val in x_hist:
    y1_vals = [np.interp(x_val, BL_B2Hi_df['PhotonEnergy'], BL_B2Hi_df[f'PhotonFlux{harm}']) for harm in harms]
    y2_vals = [np.interp(x_val, BL_B3_df['PhotonEnergy'], BL_B3_df[f'PhotonFlux{harm}']) for harm in harms]
    y1_max = max(y1_vals)
    y2_max = max(y2_vals)
    if y1_max != 0:
        factor = y2_max / y1_max
    else:
        factor = np.nan
    factors_flux.append(factor)

# =====================
# Both gain histograms (Flux and Flux Density) on the same DIN A4 page, Flux first, NO secondary y-axis
# =====================
fig_hist, (ax_gain_flux, ax_gain_density) = plt.subplots(2, 1, figsize=(8.27, 11.69), dpi=150, sharex=False)

# Calculate y-axis max for better label placement
hist_ymax_flux = max(factors_flux) * 1.25
hist_ymax_density = max(factors_density) * 1.25

# Flux Gain Histogram (now first)
bar1 = ax_gain_flux.bar(x_hist, factors_flux, width=hist_bin_width - 10, color=hist_bar_color, edgecolor='grey', alpha=0.6)
for i, (x_val, factor) in enumerate(zip(x_hist, factors_flux)):
    if not np.isnan(factor):
        ax_gain_flux.text(x_val, factor + 0.03*hist_ymax_flux, f'x{factor:.1f}',
                          ha='center', va='bottom', fontsize=9, fontweight='bold')
    else:
        ax_gain_flux.text(x_val, 0.03*hist_ymax_flux, 'n/a', ha='center', va='bottom', fontsize=9, fontweight='bold')
ax_gain_flux.set_xlabel('Energy [eV]', fontsize=FONT_SIZES['axis_label'])
ax_gain_flux.set_ylabel('Gain [factor]', fontsize=FONT_SIZES['axis_label'])
ax_gain_flux.set_title(f'Flux Gain (BESSY III / II, max over harmonics) every {hist_bin_width} eV', fontsize=FONT_SIZES['title'])
ax_gain_flux.xaxis.set_major_locator(mticker.MultipleLocator(hist_bin_width))
ax_gain_flux.tick_params(labelsize=FONT_SIZES['tick_label'])
ax_gain_flux.grid(axis='y', linestyle='--', linewidth=0.5, color='lightgrey')
ax_gain_flux.set_ylim(0, hist_ymax_flux)

# Flux Density Gain Histogram (now second)
bar2 = ax_gain_density.bar(x_hist, factors_density, width=hist_bin_width - 10, color=hist_bar_color, edgecolor='grey', alpha=0.6)
for i, (x_val, factor) in enumerate(zip(x_hist, factors_density)):
    if not np.isnan(factor):
        ax_gain_density.text(x_val, factor + 0.03*hist_ymax_density, f'x{factor:.1f}',
                            ha='center', va='bottom', fontsize=9, fontweight='bold')
    else:
        ax_gain_density.text(x_val, 0.03*hist_ymax_density, 'n/a', ha='center', va='bottom', fontsize=9, fontweight='bold')
ax_gain_density.set_xlabel('Energy [eV]', fontsize=FONT_SIZES['axis_label'])
ax_gain_density.set_ylabel('Gain [factor]', fontsize=FONT_SIZES['axis_label'])
ax_gain_density.set_title(f'Flux Density Gain (BESSY III / II, max over harmonics) every {hist_bin_width} eV', fontsize=FONT_SIZES['title'])
ax_gain_density.xaxis.set_major_locator(mticker.MultipleLocator(hist_bin_width))
ax_gain_density.tick_params(labelsize=FONT_SIZES['tick_label'])
ax_gain_density.grid(axis='y', linestyle='--', linewidth=0.5, color='lightgrey')
ax_gain_density.set_ylim(0, hist_ymax_density)

plt.tight_layout()
# =====================
# End of combined gain histogram plot
# =====================

###############################################################
# SAVING
# Ensure the "plot" folder exists
plot_folder = 'plot'
if not os.path.exists(plot_folder):
    os.makedirs(plot_folder)

plt.tight_layout()

# Save the combined gain histogram figure
fig_hist.savefig(os.path.join(plot_folder, 'CDR-Plots/Gain_Histograms_Flux_and_FluxDensity.pdf'))

# Save the main comparison figure (axs)
fig_main.savefig(os.path.join(plot_folder, 'CDR-Plots/Main_Comparison_Flux_and_FluxDensity.pdf'))

plt.show()