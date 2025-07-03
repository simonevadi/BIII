from raypyng import Simulate
import pandas as pd
import os

from parameter import rml_file_name_bessy3_56m_errors_on_hor_PGM_M3Para as rml_file_name
from parameter import get_vibration
# define the values of the parameters to scan 
from parameter import order, energy_flux as energy, round_flux as rounds    
from parameter import SlitSize, cff, nrays_flux as nrays, ncpu
from parameter import n_sim

this_file_dir=os.path.dirname(os.path.realpath(__file__))
rml_file = os.path.join('rml/'+rml_file_name+'.rml')

sim = Simulate(rml_file, hide=True)

rml=sim.rml
beamline = sim.rml.beamline


# name for simulation folder
sim_name = 'horizontal_PGM_vibration'

# vibrations
amp = 0.03     ## mm 30 micrometer

if amp == 0.0003:
    rot_amp = 0.00005 #in mrad, 50 nrad
elif amp == 0.003:
    rot_amp = 0.0005
elif amp == 0.03:
    rot_amp = 0.005

sim_name = f'horizontal_PGM_vibration_{amp}'


# define a list of dictionaries with the parameters to scan
params = [  
            {beamline.PG.cFactor:cff}, 
            {beamline.ExitSlit.openingWidth:SlitSize},
            {beamline.SU.photonEnergy:energy},
            {beamline.PG.orderDiffraction:order},
            {beamline.SU.numberRays:nrays},
            {beamline.SU.translationXerror:get_vibration(amp, n_sim),
             beamline.SU.translationYerror:get_vibration(amp,n_sim), 
             beamline.M1.translationXerror:get_vibration(amp, n_sim),
             beamline.M1.translationYerror:get_vibration(amp, n_sim),
             beamline.M1.rotationXerror:get_vibration(rot_amp, n_sim),
             beamline.M1.rotationYerror:get_vibration(rot_amp, n_sim),
             beamline.M2.translationXerror:get_vibration(amp, n_sim),
             beamline.M2.translationYerror:get_vibration(amp, n_sim),
             beamline.M2.rotationXerror:get_vibration(rot_amp, n_sim),
             beamline.M2.rotationYerror:get_vibration(rot_amp, n_sim), 
             beamline.PG.translationXerror:get_vibration(amp, n_sim),
             beamline.PG.translationYerror:get_vibration(amp, n_sim),
             beamline.PG.rotationXerror:get_vibration(rot_amp, n_sim),
             beamline.PG.rotationYerror:get_vibration(rot_amp, n_sim), 
             beamline.M3.translationXerror:get_vibration(amp, n_sim),
             beamline.M3.translationYerror:get_vibration(amp, n_sim),
             beamline.M3.rotationXerror:get_vibration(rot_amp, n_sim),
             beamline.M3.rotationYerror:get_vibration(rot_amp, n_sim),
             beamline.M4.translationXerror:get_vibration(amp, n_sim),
             beamline.M4.translationYerror:get_vibration(amp, n_sim),
             beamline.M4.rotationXerror:get_vibration(rot_amp, n_sim),
             beamline.M4.rotationYerror:get_vibration(rot_amp, n_sim),
             beamline.M5.translationXerror:get_vibration(amp, n_sim),
             beamline.M5.translationYerror:get_vibration(amp, n_sim),
             beamline.M5.rotationXerror:get_vibration(rot_amp, n_sim),
             beamline.M5.rotationYerror:get_vibration(rot_amp, n_sim),
         }
        ]

#and then plug them into the Simulation class
sim.params=params

# sim.simulation_folder = '/home/simone/Documents/RAYPYNG/raypyng/test'
sim.simulation_name = sim_name

# turn off reflectivity
sim.reflectivity(True)

# repeat the simulations as many time as needed
sim.repeat = rounds

sim.analyze = False # don't let RAY-UI analyze the results
sim.raypyng_analysis=True # let raypyng analyze the results

undulator_file_path = os.path.join(this_file_dir, 
                                   'undulator_flux_curves','b3_ue42_5_ver_300mA_flux.csv')

undulator = pd.read_csv(undulator_file_path)
sim.undulator_table=undulator

## This must be a list of dictionaries
sim.exports  =  [{beamline.DetectorAtFocus:['RawRaysOutgoing']}]



#uncomment to run the simulations
sim.run(multiprocessing=ncpu, force=False, remove_rawrays=True, remove_round_folders=True)
