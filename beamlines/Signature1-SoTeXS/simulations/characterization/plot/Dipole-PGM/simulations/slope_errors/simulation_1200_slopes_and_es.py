from pathlib import Path
import sys
import os

# Go four directories up
machine_dir = Path(__file__).resolve().parents[4]
machine_dir = os.path.join(machine_dir, 'machine')
sys.path.insert(0, str(machine_dir))        # make root importable for this run

# Now regular absolute import works
from machine_params import emittance_standard

import pandas as pd
import numpy as np
from raypyng import Simulate

# define the values of the parameters to scan 
from params import hb_1200_cff
from params import ncpu
from params import hb_1200_file_path
from slopes_helper import make_slopes_params

sim = Simulate(hb_1200_file_path, hide=True)

rml=sim.rml
beamline = sim.rml.beamline

energy = np.arange(50, 2551, 250)    
rounds = 1
nrays  = 2e5

slopes = {
    beamline.M1.slopeErrorMer:  (np.array([0.2, 0.5, 0.7, 2]), 0.5),
    beamline.M1.slopeErrorSag: (np.array([1.0, 1.5, 2.0, 5]), 1.5),
    beamline.PremirrorM2.slopeErrorMer: (np.array([0.03, 0.05, 0.07, 1.5]), 0.05),
    beamline.PremirrorM2.slopeErrorSag: (np.array([0.3, 0.5, 0.7, 2]), 0.5),
    beamline.PG.slopeErrorMer: (np.array([0.03, 0.05, 0.07, 1.5]), 0.05),
    beamline.PG.slopeErrorSag: (np.array([0.3, 0.5, 0.7, 2]), 0.5),
    beamline.M3.slopeErrorSag: (np.array([0.5, 1.0, 1.5, 4]), 1.0),
    beamline.M3.slopeErrorMer: (np.array([0.1, 0.3, 0.5, 4]), 0.3),
    beamline.KB_ver.slopeErrorMer: (np.array([0.03, 0.05, 0.07, 0.2]), 0.05),
    beamline.KB_ver.slopeErrorSag: (np.array([0.05, 0.1, 0.15, 0.5]), 0.1),
    beamline.KB_hor.slopeErrorMer: (np.array([0.03, 0.05,0.07]), 0.05),
    beamline.KB_hor.slopeErrorSag: (np.array([0.05, 0.1, 0.15, 0.5]), 0.1)
}
slopes_dict = make_slopes_params(slopes)
# define a list of dictionaries with the parameters to scan
params = [  
            {beamline.ExitSlit.openingHeight:[0.02,0.01, 0.005]},
            {beamline.Dipole.photonEnergy:energy},
            {beamline.PG.cFactor:hb_1200_cff}, 
            {beamline.Dipole.numberRays:nrays}, 
        ]

# source parameters
params.extend([{beamline.Dipole.sourceWidth:emittance_standard['sig_x_mm']},
               {beamline.Dipole.sourceHeight:emittance_standard['sig_y_mm']},
               {beamline.Dipole.verEbeamDiv:emittance_standard['sig_yp_urad']},
             ])

params.append(slopes_dict)  # append the slopes dictionary to the list of parameters

# import the parameters into the simulation
#and then plug them into the Simulation class
sim.params=params

# sim.simulation_folder = '/home/simone/Documents/RAYPYNG/raypyng/test'
sim.simulation_name = '1200_slopes_and_exit_slit'

# turn off reflectivity
sim.reflectivity(False)

# repeat the simulations as many time as needed
sim.repeat = rounds

sim.analyze = False # let RAY-UI analyze the results
sim.raypyng_analysis = True # let RAY-UI analyze the results

## This must be a list of dictionaries
sim.exports  =  [{beamline.DetectorAtFocus:['RawRaysOutgoing']}]

#uncomment to run the simulations
sim.run(multiprocessing=ncpu, force=False, remove_round_folders=True, remove_rawrays=True)