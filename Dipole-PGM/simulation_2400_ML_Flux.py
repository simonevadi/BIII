from raypyng import Simulate
import numpy as np
import os
from multilayer_helper import AndreyML

# define the values of the parameters to scan 
from params import ml_order as order,  ml_energy_flux as energy
from params import ml_SlitSize as SlitSize, ml_grating as grating 
from params import ml_index as index, ml_table
from params import ml_nrays_flux as nrays, ml_rounds_flux as rounds
from params import ml_ncpu_flux as ncpu, ml_sim_name_flux as sim_name
from params import ml_rml_file_path

sim = Simulate(ml_rml_file_path, hide=True)

rml=sim.rml
beamline = sim.rml.beamline

# Andrey ML
aml = AndreyML(excel_file_name=ml_table)
cff = aml.get_cff_for_ML(ind=index, order=order, energy=energy)

# define a list of dictionaries with the parameters to scan
params = [  
            # set two parameters: "alpha" and "beta" in a dependent way. 
            {beamline.ExitSlit.totalHeight:SlitSize},
            
            {beamline.Dipole.photonEnergy:energy, 
            beamline.PG.cFactor:cff}, 
            
            {beamline.PG.orderDiffraction:order},

            {beamline.Dipole.numberRays:nrays}
        ]

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
sim.exports  =  [{beamline.Dipole:['RawRaysOutgoing']},
                 {beamline.DetectorAtFocus:['RawRaysOutgoing']}]


# create the rml files
#sim.rml_list()

#uncomment to run the simulations
sim.run(multiprocessing=ncpu, force=False)