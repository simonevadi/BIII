import matplotlib.pyplot as plt
import pandas as pd


# Read CSV-File
simdata_B2hi_eoff_focus = pd.read_csv('CSV_RayUI/bessy2hi_56m_PGM_2Perc_coupling_errors_off/loop_accumulated_DetectorAtFocus-ScalarBeamProperties.csv', sep='\t')
simdata_B2hi_eoff_source = pd.read_csv('CSV_RayUI/bessy2hi_56m_PGM_2Perc_coupling_errors_off/loop_accumulated_SU-ScalarBeamProperties.csv', sep='\t')

simdata_B2hi_eon_focus = pd.read_csv('CSV_RayUI/bessy2hi_56m_PGM_2Perc_coupling_errors_on/loop_accumulated_DetectorAtFocus-ScalarBeamProperties.csv', sep='\t')
simdata_B2hi_eon_source = pd.read_csv('CSV_RayUI/bessy2hi_56m_PGM_2Perc_coupling_errors_on/loop_accumulated_SU-ScalarBeamProperties.csv', sep='\t')

simdata_B3_eoff_focus = pd.read_csv('CSV_RayUI/bessy3_56m_PGM_2Perc_coupling_errors_off/loop_accumulated_DetectorAtFocus-ScalarBeamProperties.csv', sep='\t')
simdata_B3_eoff_source = pd.read_csv('CSV_RayUI/bessy3_56m_PGM_2Perc_coupling_errors_off/loop_accumulated_SU-ScalarBeamProperties.csv', sep='\t')

simdata_B3_eon_focus = pd.read_csv('CSV_RayUI/bessy3_56m_PGM_2Perc_coupling_errors_on/loop_accumulated_DetectorAtFocus-ScalarBeamProperties.csv', sep='\t')
simdata_B3_eon_source = pd.read_csv('CSV_RayUI/bessy3_56m_PGM_2Perc_coupling_errors_on/loop_accumulated_SU-ScalarBeamProperties.csv', sep='\t')


fig, ax = plt.subplots(1, 1,figsize=(20,10))


# BESSY II HiBeta eoff
Energy_B2hi_eoff = simdata_B2hi_eoff_source['SU_photonEnergy']
PsiSource_B2hi_eoff = simdata_B2hi_eoff_source['SU_psi_width']
PhiSource_B2hi_eoff = simdata_B2hi_eoff_source['SU_phi_width']
PsiFocus_B2hi_eoff = simdata_B2hi_eoff_focus['DetectorAtFocus_psi_width']
PhiFocus_B2hi_eoff = simdata_B2hi_eoff_focus['DetectorAtFocus_phi_width']

## SolidAngel eoff
SASource_B2hi_eoff = PsiSource_B2hi_eoff*PhiSource_B2hi_eoff
SASFocus_B2hi_eoff = PsiFocus_B2hi_eoff*PhiFocus_B2hi_eoff

## Area and Foci of Source eoff
hf_Source_B2hi_eoff = simdata_B2hi_eoff_source['SU_intensityH_width_X']
vf_Source_B2hi_eoff = simdata_B2hi_eoff_source['SU_intensityH_width_Y']
ASource_B2hi_eoff = vf_Source_B2hi_eoff*hf_Source_B2hi_eoff

## Area and Foci of Focus eoff
hf_Focus_B2hi_eoff = simdata_B2hi_eoff_focus['DetectorAtFocus_intensityH_width_X']
vf_Focus_B2hi_eoff = simdata_B2hi_eoff_focus['DetectorAtFocus_intensityH_width_Y']
AFocus_B2hi_eoff = vf_Focus_B2hi_eoff*hf_Focus_B2hi_eoff




# BESSY II HiBeta eon
Energy_B2hi_eon = simdata_B2hi_eon_source['SU_photonEnergy']
PsiSource_B2hi_eon = simdata_B2hi_eon_source['SU_psi_width']
PhiSource_B2hi_eon = simdata_B2hi_eon_source['SU_phi_width']
PsiFocus_B2hi_eon = simdata_B2hi_eon_focus['DetectorAtFocus_psi_width']
PhiFocus_B2hi_eon = simdata_B2hi_eon_focus['DetectorAtFocus_phi_width']

## SolidAngel eon
SASource_B2hi_eon = PsiSource_B2hi_eon*PhiSource_B2hi_eon
SASFocus_B2hi_eon = PsiFocus_B2hi_eon*PhiFocus_B2hi_eon

## Area and Foci of Source eon
hf_Source_B2hi_eon = simdata_B2hi_eon_source['SU_intensityH_width_X']
vf_Source_B2hi_eon = simdata_B2hi_eon_source['SU_intensityH_width_Y']
ASource_B2hi_eon = vf_Source_B2hi_eon*hf_Source_B2hi_eon

## Area and Foci of Focus eon
hf_Focus_B2hi_eon = simdata_B2hi_eon_focus['DetectorAtFocus_intensityH_width_X']
vf_Focus_B2hi_eon = simdata_B2hi_eon_focus['DetectorAtFocus_intensityH_width_Y']
AFocus_B2hi_eon = vf_Focus_B2hi_eon*hf_Focus_B2hi_eon



# BESSY III eoff
Energy_B3_eoff = simdata_B3_eoff_source['SU_photonEnergy']
PsiSource_B3_eoff = simdata_B3_eoff_source['SU_psi_width']
PhiSource_B3_eoff = simdata_B3_eoff_source['SU_phi_width']
PsiFocus_B3_eoff = simdata_B3_eoff_focus['DetectorAtFocus_psi_width']
PhiFocus_B3_eoff = simdata_B3_eoff_focus['DetectorAtFocus_phi_width']

## SolidAngel eoff
SASource_B3_eoff = PsiSource_B3_eoff*PhiSource_B3_eoff
SASFocus_B3_eoff = PsiFocus_B3_eoff*PhiFocus_B3_eoff

## Area and Foci of Source eoff
hf_Source_B3_eoff = simdata_B3_eoff_source['SU_intensityH_width_X']
vf_Source_B3_eoff = simdata_B3_eoff_source['SU_intensityH_width_Y']
ASource_B3_eoff = vf_Source_B3_eoff*hf_Source_B3_eoff

## Area and Foci of Focus eoff
hf_Focus_B3_eoff = simdata_B3_eoff_focus['DetectorAtFocus_intensityH_width_X']
vf_Focus_B3_eoff = simdata_B3_eoff_focus['DetectorAtFocus_intensityH_width_Y']
AFocus_B3_eoff = vf_Focus_B3_eoff*hf_Focus_B3_eoff



# BESSY III eon
Energy_B3_eon = simdata_B3_eon_source['SU_photonEnergy']
PsiSource_B3_eon = simdata_B3_eon_source['SU_psi_width']
PhiSource_B3_eon = simdata_B3_eon_source['SU_phi_width']
PsiFocus_B3_eon = simdata_B3_eon_focus['DetectorAtFocus_psi_width']
PhiFocus_B3_eon = simdata_B3_eon_focus['DetectorAtFocus_phi_width']

## SolidAngel eon
SASource_B3_eon = PsiSource_B3_eon*PhiSource_B3_eon
SASFocus_B3_eon = PsiFocus_B3_eon*PhiFocus_B3_eon

## Area and Foci of Source eon
hf_Source_B3_eon = simdata_B3_eon_source['SU_intensityH_width_X']
vf_Source_B3_eon = simdata_B3_eon_source['SU_intensityH_width_Y']
ASource_B3_eon = vf_Source_B3_eon*hf_Source_B3_eon

## Area and Foci of Focus eon
hf_Focus_B3_eon = simdata_B3_eon_focus['DetectorAtFocus_intensityH_width_X']
vf_Focus_B3_eon = simdata_B3_eon_focus['DetectorAtFocus_intensityH_width_Y']
AFocus_B3_eon = vf_Focus_B3_eon*hf_Focus_B3_eon


ax.plot(Energy_B2hi_eoff, (ASource_B2hi_eoff*SASource_B2hi_eoff)/(AFocus_B2hi_eoff*SASFocus_B2hi_eoff), label = 'B2 (high beta) errors off, ES 130 µm', marker='s', color='blue') 
ax.plot(Energy_B2hi_eon, (ASource_B2hi_eon*SASource_B2hi_eon)/(AFocus_B2hi_eon*SASFocus_B2hi_eon), label = 'B2 (high beta) errors on, ES 30 µm', marker='s', color='deepskyblue') 
ax.plot(Energy_B3_eoff, (ASource_B3_eoff*SASource_B3_eoff)/(AFocus_B3_eoff*SASFocus_B3_eoff), label = 'B3 errors off, ES 16 µm', marker='s', color='green') 
ax.plot(Energy_B3_eon, (ASource_B3_eon*SASource_B3_eon)/(AFocus_B3_eon*SASFocus_B3_eon), label = 'B3 errors on, ES 16 µm', marker='s', color='darkseagreen') 


ax.minorticks_on()
ax.grid(linestyle='dotted', color='grey')
ax.tick_params(axis='both', labelsize=14)
ax.set_ylabel (r'$\eta$ of brilliance [%]' , fontsize=14)
ax.set_xlabel('Energy [eV]', fontsize= 16)
# ax.set_title('BESSY II vs. BESSY III @ 56 m standard PGM-BL PhotonDensity (errors on)', fontsize= 18)
# ax.set_title('BESSY III @ 56 m standard PGM-BL bandwidth normalized transmission', fontsize= 18)
ax.legend(fontsize=16, loc='best')
plt.tight_layout()
plt.savefig('plot/Brilliance B2_B3 errors_on at 16 mu.png')
plt.savefig('plot/Brilliance B2_B3 errors_on at 16 mu.pdf')
#plt.show()