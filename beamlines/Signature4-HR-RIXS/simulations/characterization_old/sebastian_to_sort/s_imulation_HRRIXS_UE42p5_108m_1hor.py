import os
import sys
from pathlib import Path

# Load the machine directory
machine_dir = Path(__file__).resolve().parents[4]    # Go four directories up
machine_dir = os.path.join(machine_dir, 'machine')
sys.path.insert(0, str(machine_dir))                 # make root importable for this run

from raypyng import Simulate

# Load the machine directory from the machine file
from BESSY_III_machine_params import emittance_standard

# Define the values of the parameters to scan 
from parameter import ncpu, nrays, rounds
from parameter import HRRIXS_energy       as energy
# from parameter import HRRIXS_SlitSize     as SlitSize
from parameter import HRRIXS_cff          as cff
from parameter import HRRIXS_grating      as grating
from parameter import HRRIXS_order        as order
from parameter import HRRIXS_undulator    as undulator
from parameter import HRRIXS_108m_1hor_file_path as rml_file
from parameter import HRRIXS_108m_1hor_sim_name  as sim_name

sim = Simulate(rml_file, hide=True)

rml=sim.rml
beamline = sim.rml.beamline

# define a list of dictionaries with the parameters to scan
params = [  
            {beamline.PG.orderDiffraction:order},
            {beamline.PG.cFactor:cff},
            {beamline.PG.lineDensity:grating},
            # {beamline.ExitSlit.openingHeight:SlitSize},
            {beamline.SU.numberRays:nrays},
            {beamline.SU.photonEnergy:energy}
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

# Who will analyze ttheeh data
sim.analyze = False # don't let RAY-UI analyze the results
sim.raypyng_analysis=True # let raypyng analyze the results

# Load the undulator table
sim.undulator_table=undulator

## This must be a list of dictionaries
sim.exports  =  [{beamline.DetectorAtFocus:['RawRaysOutgoing']}]

#uncomment to run the simulations
sim.run(multiprocessing=ncpu, force=False, remove_rawrays=True, remove_round_folders=True)
