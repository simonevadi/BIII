from raypyng import Simulate
import pandas as pd
import os

from parameter import rml_file_name_bessy2_LoBeta_37m as rml_file_name

this_file_dir=os.path.dirname(os.path.realpath(__file__))
rml_file = os.path.join('rml_b2/'+rml_file_name+'.rml')

sim = Simulate(rml_file, hide=True)

rml=sim.rml
beamline = sim.rml.beamline

# cpu
from parameter import ncpu

# name for simulation folder
sim_name = rml_file_name+'_FLUX'

# define the values of the parameters to scan 
from parameter import order, energy_flux as energy, round_flux as rounds    
from parameter import SlitSize, cff, nrays_flux as nrays

# define a list of dictionaries with the parameters to scan
params = [  
            {beamline.PG.cFactor:cff}, 
            {beamline.ExitSlit.openingHeight:SlitSize},
            {beamline.SU.photonEnergy:energy},
            {beamline.PG.orderDiffraction:order},
            {beamline.SU.numberRays:nrays}
        ]

#and then plug them into the Simulation class
sim.params=params

# sim.simulation_folder = '/home/simone/Documents/RAYPYNG/raypyng/test'
sim.simulation_name = sim_name

# turn on/off reflectivity (on=True / off=False)
sim.reflectivity(True)

# repeat the simulations as many time as needed
sim.repeat = rounds

sim.analyze = False # don't let RAY-UI analyze the results
sim.raypyng_analysis = True # let raypyng analyze the results


undulator_file_path = os.path.abspath(
    os.path.join(this_file_dir, '..', '..', '..', '..', 'undulators',
                 'UndulatorFiles_BESSY_II',
                 'undulator_flux_curves_SPECTRA',
                 'UE46_b2_LoBeta_2PercCoupl_2025_smalerz_300mA.txt')
)

undulator = pd.read_csv(undulator_file_path, delimiter='\t')
sim.undulator_table=undulator

## This must be a list of dictionaries
sim.exports  =  [{beamline.SU:['RawRaysOutgoing']},
                 {beamline.DetectorAtFocus:['RawRaysOutgoing']}]

#uncomment to run the simulations
sim.run(multiprocessing=ncpu, force=False, remove_rawrays=True, remove_round_folders=True)
