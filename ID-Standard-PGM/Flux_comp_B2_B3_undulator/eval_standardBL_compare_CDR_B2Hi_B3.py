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
    'annotation': 6
}

# Fontsizes, Linesizes:
STitle = FONT_SIZES['title']
SLabes = FONT_SIZES['axis_label']
STickLabels = FONT_SIZES['tick_label']
SLegend = FONT_SIZES['legend']
SAnnotation = FONT_SIZES['annotation']
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
legend = ax1.legend(loc='lower left', fontsize=SLegend)
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
    'C-K'   : 284.2,
    'O-K'   : 543.1,
    'Si-K'  : 1839.0,
    'Si-L'  : 99.8,
    'S-K'   : 2472,
    'Fe-L'  : 707.0,
    'Co-L'  : 793.0,
    'Mn-L'  : 649.9, 
    'Ni-L'  : 870.0,
    'Cu-L'  : 952.1,
    'Eu-M'  : 1614,
    'Ga-L'  : 1143,
    'Gd-M'  : 1688,
    'Ho-M'  : 1923,
    'Ce-M'  : 1274
}

# Individuelle y-Offsets für bessere Lesbarkeit
label_offsets = {
    'C-K'   : 0.02,
    'O-K'   : 0.1,
    'Si-K'  : 1.3,
    'Si-L'  : 0.3,
    'S-K'   : 0.4,
    'Fe-L'  : 0.01,
    'Co-L'  : 0.1,
    'Mn-L'  : 0.4,
    'Ni-L'  : 0.01,
    'Cu-L'  : 0.2,
    'Eu-M'  : 0.1,
    'Ga-L'  : 0.1,
    'Gd-M'  : 0.05,
    'Ho-M'  : 0.01,
    'Ce-M'  : 2.4
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
    # Only element and factor in bold, no energy in the box
    label_text = f'$\\bf{{{label}}}$\n$\\bf{{{factor_str}}}$'
    ax2.text(
        x_val,
        min(y1_max, y2_max)*offset,
        label_text,
        rotation=0,
        va='top',
        ha='center',
        fontsize=SAnnotation,
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
    label_text = f'$\\bf{{{label}}}$\n$\\bf{{{factor_str}}}$'
    ax1.text(
        x_val,
        min(y1_max, y2_max)*offset,
        label_text,
        rotation=0,
        va='top',
        ha='center',
        fontsize=SAnnotation,
        color='black',
        bbox=dict(facecolor='white', edgecolor='grey', boxstyle='round,pad=0.2', linewidth=0.8)
    )

# =====================
# Parameters for histogram appearance and binning
# =====================
hist_bar_color = 'green'    # Change this to any valid matplotlib color
hist_bin_width = 100        # Change this to adjust the bin width (e.g. 100, 500, etc.)
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

# Flux Gain Histogram
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

# Flux Density Gain Histogram
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

# --- Kurvendiagramm für die Histogramm-Daten (Flux und Flux Density) ---

fig_curve_hist, ax_curve_hist = plt.subplots(figsize=(8.27, 5), dpi=150)

# Plot Flux Gain (Kurve)
ax_curve_hist.plot(x_hist, factors_flux, marker='o', linestyle='-', color='green', linewidth=1.5, markersize=6, label='Flux Gain (BESSY III / II)')

# Plot Flux Density Gain (Kurve) - jetzt blau statt orange
ax_curve_hist.plot(x_hist, factors_density, marker='s', linestyle='-', color='blue', linewidth=1.5, markersize=6, label='Flux Density Gain (BESSY III / II)')

ax_curve_hist.set_xlim(hist_x_start, hist_x_stop)
ax_curve_hist.set_ylim(0, max(max(factors_flux), max(factors_density))*1.25)
ax_curve_hist.set_xlabel('Energy [eV]', fontsize=FONT_SIZES['axis_label'])
ax_curve_hist.set_ylabel('Flux gain [factor]', fontsize=FONT_SIZES['axis_label'])
ax_curve_hist.set_title('Flux gain (Curve diagram from Gain Histogramm', fontsize=FONT_SIZES['title'])
ax_curve_hist.grid(axis='y', linestyle='--', linewidth=0.5, color='lightgrey')
ax_curve_hist.tick_params(labelsize=FONT_SIZES['tick_label'])
ax_curve_hist.minorticks_on()
ax_curve_hist.legend(fontsize=FONT_SIZES['legend'])

plt.tight_layout()

# =====================
# Histogram of element edges with 0.1% bandwidth, y-value is gain factor
# =====================
import matplotlib.patches as mpatches

# Prepare data for histogram
element_names = list(x_lines.keys())
element_energies = np.array(list(x_lines.values()))
bandwidths = 0.001 * element_energies  # 0.1% of each edge energy

# Calculate gain factor for each element edge (max over harmonics)
gain_factors = []
for name, energy in zip(element_names, element_energies):
    y1_vals = [np.interp(energy, BL_B2Hi_df['PhotonEnergy'], BL_B2Hi_df[f'PhotonFlux{harm}']) for harm in harms]
    y2_vals = [np.interp(energy, BL_B3_df['PhotonEnergy'], BL_B3_df[f'PhotonFlux{harm}']) for harm in harms]
    y1_max = max(y1_vals)
    y2_max = max(y2_vals)
    if y1_max != 0:
        gain = y2_max / y1_max
    else:
        gain = np.nan
    gain_factors.append(gain)

fig_edges, ax_edges = plt.subplots(figsize=(8.27, 11.69), dpi=150)

# Draw each element as a rectangle (bandwidth window), height = gain factor
for i, (name, energy, bw, gain) in enumerate(zip(element_names, element_energies, bandwidths, gain_factors)):
    left = energy - bw/2
    rect = mpatches.Rectangle((left, 0), bw, gain, color='royalblue', alpha=0.7, edgecolor='black')
    ax_edges.add_patch(rect)
    # Alternate label position above/below bar to avoid overlap
    if i % 2 == 0:
        y_label = gain + 0.04 * max(gain_factors)
        va = 'bottom'
    else:
        y_label = gain - 0.04 * max(gain_factors)
        va = 'top'
    ax_edges.text(
        energy, y_label, name,
        ha='center', va=va, fontsize=FONT_SIZES['bar_label'], fontweight='bold', rotation=0, color='black',
        bbox=dict(facecolor='white', edgecolor='grey', boxstyle='round,pad=0.2', linewidth=0.8)
    )

# Set axis limits and labels (use same energy range as other plots)
ax_edges.set_xlim(x_range)
ax_edges.set_ylim(0, max(gain_factors)*1.25)
ax_edges.set_yticks(np.round(np.linspace(0, max(gain_factors)*1.1, 5), 1))  # Show 5 ticks, rounded to 1 decimal
ax_edges.set_xlabel('Energy [eV]', fontsize=FONT_SIZES['axis_label'])
ax_edges.set_ylabel('Gain [factor]', fontsize=FONT_SIZES['axis_label'])
ax_edges.set_title('Element edges (0.1% bandwidth, height = flux gain factor compared to BESSY II)', fontsize=FONT_SIZES['title'])
ax_edges.grid(axis='y', linestyle='--', linewidth=0.5, color='lightgrey')
ax_edges.tick_params(labelsize=FONT_SIZES['tick_label'])
ax_edges.tick_params(axis='y', which='minor', left=False, right=False)  # Remove y-minorticks
ax_edges.minorticks_on()  # keep minorticks on x

plt.tight_layout()


###############################################################
# SAVING
###############################################################
# Ensure the "plot" folder exists
plot_folder = 'plot'
if not os.path.exists(plot_folder):
    os.makedirs(plot_folder)

# Save the main comparison figure (axs)
fig_main.savefig(os.path.join(plot_folder, 'CDR-Plots/Main_Comparison_Flux_and_FluxDensity.pdf'))

# Save the combined gain histogram figure
fig_hist.savefig(os.path.join(plot_folder, 'CDR-Plots/Gain_Histograms_Flux_and_FluxDensity.pdf'))

# Save the curve histogram figure
fig_curve_hist.savefig(os.path.join(plot_folder, 'CDR-Plots/Gain_Curve_Flux_and_FluxDensity.pdf'))

# Save the element edge gain histogram
fig_edges.savefig(os.path.join(plot_folder, 'CDR-Plots/Element_Edges_Gain_Bandwidth_Histogram.pdf'))

plt.show()
