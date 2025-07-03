import os
import pandas as pd

from raypyng import Simulate

# define the values of the parameters to scan 
from parameter_ml import order, energy
from parameter_ml import SlitSize
from parameter_ml import nrays, rounds
from parameter_ml import ncpu
from parameter_ml import cff
from parameter_ml import efficiency
from parameter_ml import rml_file_name_bessy3_long_56m_errors_on_ml as rml_file_name

sim = Simulate('rml/'+rml_file_name+'.rml', hide=True)
rml=sim.rml
beamline = sim.rml.beamline

# define a list of dictionaries with the parameters to scan
params = [  
            {beamline.ExitSlit.openingHeight:SlitSize},
            {beamline.SU.photonEnergy:energy, 
             beamline.PG.cFactor:cff}, 
            {beamline.PG.orderDiffraction:order},
            {beamline.SU.numberRays:nrays}, 
        ]

#and then plug them into the Simulation class
sim.params=params

# sim.simulation_folder = '/home/simone/Documents/RAYPYNG/raypyng/test'
sim.simulation_name = rml_file_name+'_FLUX'

# turn off reflectivity
# sim.reflectivity(reflectivity=True)

# repeat the simulations as many time as needed
sim.repeat = rounds

sim.analyze = False # let RAY-UI analyze the results
sim.raypyng_analysis = True # let RAY-UI analyze the results

## This must be a list of dictionaries
sim.exports  =  [{beamline.DetectorAtFocus:['RawRaysOutgoing']}]

this_file_dir=os.path.dirname(os.path.realpath(__file__))
undulator_file_path = os.path.join(this_file_dir,
                                   'undulator_flux_curves',
                                   'IVUE28_b3_2025_smalerz_300mA_2PercCoupl.txt')

undulator = pd.read_csv(undulator_file_path, sep='\t')
sim.undulator_table=undulator


sim.efficiency = efficiency

# create the rml files
#sim.rml_list()

#uncomment to run the simulations
sim.run(multiprocessing=ncpu, force=False, remove_round_folders=True, remove_rawrays=True)