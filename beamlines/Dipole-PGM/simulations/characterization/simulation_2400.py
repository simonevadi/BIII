from raypyng import Simulate

# define the values of the parameters to scan 
from params import ml_energy as energy
from params import ml_SlitSize as SlitSize
from params import ml_nrays as nrays, ml_rounds as rounds
from params import ml_ncpu as ncpu, ml_sim_name as sim_name
from params import ml_rml_file_path, ml_cff as cff
from params import efficiency

sim = Simulate(ml_rml_file_path, hide=True)

rml=sim.rml
beamline = sim.rml.beamline

# define a list of dictionaries with the parameters to scan
params = [  
            # set two parameters: "alpha" and "beta" in a dependent way. 
            {beamline.ExitSlit.totalHeight:SlitSize},
            
            {beamline.Dipole.photonEnergy:energy, 
            beamline.PG.cFactor:cff}, 
            
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
sim.exports  =  [{beamline.DetectorAtFocus:['RawRaysOutgoing']}]

sim.efficiency = efficiency

# create the rml files
#sim.rml_list()

#uncomment to run the simulations
sim.run(multiprocessing=ncpu, force=False, remove_round_folders=False, remove_rawrays=True)
