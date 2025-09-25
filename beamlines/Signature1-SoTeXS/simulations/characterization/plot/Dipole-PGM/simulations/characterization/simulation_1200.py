from pathlib import Path
import sys
import os

# Go four directories up
machine_dir = Path(__file__).resolve().parents[4]
machine_dir = os.path.join(machine_dir, 'machine')
sys.path.insert(0, str(machine_dir))        # make root importable for this run

# Now regular absolute import works
from machine_params import emittance_standard

from raypyng import Simulate

# define the values of the parameters to scan 
from params import hb_1200_energy as energy
from params import hb_1200_SlitSize as SlitSize
from params import hb_1200_cff as cff
from params import hb_1200_nrays as nrays, hb_1200_rounds as rounds
from params import hb_1200_ncpu as ncpu, hb_1200_sim_name as sim_name
from params import hb_1200_file_path

sim = Simulate(hb_1200_file_path, hide=True)

rml=sim.rml
beamline = sim.rml.beamline



# define a list of dictionaries with the parameters to scan
params = [  
            {beamline.ExitSlit.totalHeight:SlitSize},            
            {beamline.Dipole.photonEnergy:energy},
            {beamline.PG.cFactor:cff},             
            {beamline.Dipole.numberRays:nrays}
        ]

# source parameters
params.extend([{beamline.Dipole.sourceWidth:emittance_standard['sig_x_mm']},
               {beamline.Dipole.sourceHeight:emittance_standard['sig_y_mm']},
               {beamline.Dipole.verEbeamDiv:emittance_standard['sig_yp_urad']},
             ])

#and then plug them into the Simulation class
sim.params=params

# sim.simulation_folder = '/home/simone/Documents/RAYPYNG/raypyng/test'
sim.simulation_name = sim_name

# turn off reflectivity
# sim.reflectivity(reflectivity=True)

# repeat the simulations as many time as needed
sim.repeat = rounds

sim.analyze = False # let RAY-UI analyze the results
sim.raypyng_analysis = True # let RAY-UI analyze the results
## This must be a list of dictionaries
sim.exports  =  [{beamline.DetectorAtFocus:['RawRaysOutgoing']}]

#uncomment to run the simulations
sim.run(multiprocessing=ncpu, force=False,
        remove_round_folders=False, remove_rawrays=True)
