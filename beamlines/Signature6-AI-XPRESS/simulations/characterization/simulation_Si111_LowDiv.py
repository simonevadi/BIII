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

from parameter import si111_low_file_path as rml_file
from parameter import si111_low_sim_name as sim_name
from parameter import energy_si111 as energy, rounds, ncpu, nrays


sim = Simulate(rml_file, hide=True)

rml=sim.rml
beamline = sim.rml.beamline


# define a list of dictionaries with the parameters to scan
params = [  
            {beamline.Dipole.photonEnergy:energy},
            {beamline.Dipole.numberRays:nrays}
        ]

# source parameters (Dips uses sig_x_mm and sig_y_mm, IDs uses sig_x_um and sig_y_um)
params.extend([{beamline.Dipole.sourceWidth:emittance_standard['sig_x_mm']},
               {beamline.Dipole.sourceHeight:emittance_standard['sig_y_mm']},
               {beamline.Dipole.verEbeamDiv:emittance_standard['sig_yp_urad']},
             ])

#and then plug them into the Simulation class
sim.params=params

# sim.simulation_folder = '/home/simone/Documents/RAYPYNG/raypyng/test'
sim.simulation_name = sim_name

# repeat the simulations as many time as needed
sim.repeat = rounds

sim.analyze = False # don't let RAY-UI analyze the results
sim.raypyng_analysis=True # let raypyng analyze the results


## This must be a list of dictionaries
sim.exports  =  [{beamline.DetectorAtFocus:['RawRaysOutgoing']}]


#uncomment to run the simulations
sim.run(multiprocessing=ncpu, force=False, remove_rawrays=True, remove_round_folders=True)
