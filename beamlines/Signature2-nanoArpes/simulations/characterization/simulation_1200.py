from pathlib import Path
import os
import sys

# Load the machine directory
machine_dir = Path(__file__).resolve().parents[4]    # Go four directories up
machine_dir = os.path.join(machine_dir, 'machine')
sys.path.insert(0, str(machine_dir))                 # make root importable for this run

# Now regular absolute import works
from BESSY_III_machine_params import emittance_standard

from raypyng import Simulate

from parameter import nanoARPES_300_file_path as rml_file
from parameter import nanoARPES_300_sim_name as sim_name
from parameter import undulator
from parameter import energy_300, rounds, ncpu   
from parameter import SlitSize_300, cff_300, nrays


sim = Simulate(rml_file, hide=True)

rml=sim.rml
beamline = sim.rml.beamline


# define a list of dictionaries with the parameters to scan
params = [  
            {beamline.PG.cFactor:cff_300}, 
            {beamline.ExitSlit.openingHeight:SlitSize_300},
            {beamline.UE65.photonEnergy:energy_300},
            {beamline.UE65.numberRays:nrays}
        ]

# source parameters (Dips uses sig_x_mm and sig_y_mm, IDs uses sig_x_um and sig_y_um)
params.extend([{beamline.UE65.electronSigmaX:emittance_standard['sig_x_um']},
               {beamline.UE65.electronSigmaY:emittance_standard['sig_y_um']},
               {beamline.UE65.electronSigmaYs:emittance_standard['sig_yp_urad']},
             ])

#and then plug them into the Simulation class
sim.params=params

# sim.simulation_folder = '/home/simone/Documents/RAYPYNG/raypyng/test'
sim.simulation_name = sim_name

# repeat the simulations as many time as needed
sim.repeat = rounds

sim.analyze = False # don't let RAY-UI analyze the results
sim.raypyng_analysis=True # let raypyng analyze the results


sim.undulator_table=undulator

## This must be a list of dictionaries
sim.exports  =  [
                 {beamline.DetectorAtFocus:['RawRaysOutgoing']}]


#uncomment to run the simulations
sim.run(multiprocessing=ncpu, force=False, remove_rawrays=True, remove_round_folders=True)
