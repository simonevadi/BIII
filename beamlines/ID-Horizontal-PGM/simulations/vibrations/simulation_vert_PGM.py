from raypyng import Simulate
import pandas as pd
import numpy as np
import os

from parameter import rml_file_name_bessy3_56m_errors_on as rml_file_name
from parameter import order, energy_flux as energy, round_flux as rounds    
from parameter import SlitSize, cff, nrays_flux as nrays, ncpu

this_file_dir=os.path.dirname(os.path.realpath(__file__))
rml_file = os.path.join('rml/'+rml_file_name+'.rml')

sim = Simulate(rml_file, hide=True)

rml=sim.rml
beamline = sim.rml.beamline

# name for simulation folder
sim_name = 'vertical_PGM'

# define a list of dictionaries with the parameters to scan
params = [  
            {beamline.PG.cFactor:cff}, 
            {beamline.ExitSlit.openingHeight:SlitSize},
            {beamline.SU.photonEnergy:np.arange(100, 2101, 200)},
            {beamline.PG.orderDiffraction:order},
            {beamline.SU.numberRays:nrays},
            ]

#and then plug them into the Simulation class
sim.params=params

# sim.simulation_folder = '/home/simone/Documents/RAYPYNG/raypyng/test'
sim.simulation_name = sim_name

# turn off reflectivity
sim.reflectivity(True)

# repeat the simulations as many time as needed
sim.repeat = 5

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
