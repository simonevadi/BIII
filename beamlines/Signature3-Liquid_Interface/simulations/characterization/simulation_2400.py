import os
import sys
from pathlib import Path

# Load the machine directory
machine_dir = Path(__file__).resolve().parents[4]    # Go four directories up
machine_dir = os.path.join(machine_dir, 'machine')
sys.path.insert(0, str(machine_dir))                 # make root importable for this run

# Now regular absolute import works
from BESSY_III_machine_params import emittance_standard

from raypyng import Simulate

# define the values of the parameters to scan 
from parameter import energy_2400 as energy, cff_2400 as cff
from parameter import SlitSize_2400 as SlitSize
from parameter import nrays, rounds, ncpu
from parameter import undulator
from parameter import efficiency_2400 as efficiency
from parameter import elisa_2400_file_path as rml_file
from parameter import elisa_2400_sim_name as sim_name

sim = Simulate(rml_file, hide=True)

rml=sim.rml
beamline = sim.rml.beamline

# define a list of dictionaries with the parameters to scan
params = [  
            {beamline.ExitSlit.openingHeight:SlitSize},
            {beamline.SU.photonEnergy:energy, 
             beamline.PG.cFactor:cff}, 
            {beamline.SU.numberRays:nrays}, 
        ]

# source parameters (Dips uses sig_x_mm and sig_y_mm, IDs uses sig_x_um and sig_y_um)
params.extend([{beamline.SU.electronSigmaX:emittance_standard['sig_x_um']},
               #{beamline.SU.electronSigmaXs:emittance_standard['sig_xp_urad']},        #for the horizontal PGM would be the opposite (sig_yp_urad)
               {beamline.SU.electronSigmaY:emittance_standard['sig_y_um']},
               {beamline.SU.electronSigmaYs:emittance_standard['sig_yp_urad']},
             ])


#and then plug them into the Simulation class
sim.params=params

# sim.simulation_folder = '/home/simone/Documents/RAYPYNG/raypyng/test'
sim.simulation_name = sim_name

# repeat the simulations as many time as needed
sim.repeat = rounds

sim.analyze = False # let RAY-UI analyze the results
sim.raypyng_analysis = True # let RAY-UI analyze the results

## This must be a list of dictionaries
sim.exports  =  [{beamline.DetectorAtFocus:['RawRaysOutgoing']}]

sim.undulator_table=undulator

sim.efficiency = efficiency

#uncomment to run the simulations
sim.run(multiprocessing=ncpu, force=False, remove_round_folders=True, remove_rawrays=True)