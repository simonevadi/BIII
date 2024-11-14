from raypyng import Simulate
import numpy as np
import os

from helper_lib import delete_round_folders
from parameter import rml_file_name_bessy3_long_PGM_2Perc_coupling as rml_file_name

this_file_dir=os.path.dirname(os.path.realpath(__file__))
rml_file = os.path.join('rml/'+rml_file_name+'.rml')

sim = Simulate(rml_file, hide=True)
#sim.batch_size = 2

rml=sim.rml
beamline = sim.rml.beamline


# cpu
from parameter import ncpu

# name for simulation folder
sim_name = rml_file_name+'_RP'

# define the values of the parameters to scan 
from parameter import order, energy_rp as energy
from parameter import SlitSize, cff, nrays_rp as nrays
from parameter import round_rp as rounds
from parameter import grating


# define a list of dictionaries with the parameters to scan
params = [  
            {beamline.PG.cFactor:cff}, 
            {beamline.ExitSlit.openingHeight:SlitSize},
            {beamline.PG.lineDensity:grating},          
            {beamline.PG.orderDiffraction:order},
            {beamline.SU.numberRays:nrays},
            {beamline.SU.photonEnergy:energy}         
        ]

#and then plug them into the Simulation class
sim.params=params

# sim.simulation_folder = '/home/simone/Documents/RAYPYNG/raypyng/test'
sim.simulation_name = sim_name

# turn off reflectivity
sim.reflectivity(reflectivity=False)

# repeat the simulations as many time as needed
sim.repeat = rounds

sim.analyze = False # don't let RAY-UI analyze the results
sim.raypyng_analysis=True # let raypyng analyze the results

## This must be a list of dictionaries
sim.exports  =  [
    {beamline.DetectorAtFocus:['RawRaysOutgoing']}
    ]


# create the rml files
#sim.rml_list()

#uncomment to run the simulations
sim.run(multiprocessing=ncpu, force=False)

#delete_round_folders('RAYPy_Simulation_'+sim_name)