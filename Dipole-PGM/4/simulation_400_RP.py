from raypyng import Simulate

# define the values of the parameters to scan 
from params import lb_400_order as order,  lb_400_energy_rp as energy
from params import lb_400_SlitSize as SlitSize, lb_400_grating as grating 
from params import lb_400_cff as cff
from params import lb_400_nrays_rp as nrays, lb_400_rounds_rp as rounds
from params import lb_400_ncpu_rp as ncpu, lb_400_sim_name_rp as sim_name
from params import lb_400_file_path
from params import b3_params
from params_B3 import b3_array

sim = Simulate(lb_400_file_path, hide=True)

rml=sim.rml
beamline = sim.rml.beamline


params = [  
            {beamline.ExitSlit.totalHeight:SlitSize},
            {beamline.Dipole.photonEnergy:energy},
            {beamline.PG.cFactor:cff}, 
            {beamline.PG.orderDiffraction:order},
            {beamline.Dipole.numberRays:nrays}, 
            {beamline.Dipole.sourceWidth:b3_array['sig_x']/1000, 
             beamline.Dipole.sourceHeight:b3_array['sig_y']/1000, 
             beamline.Dipole.verEbeamDiv:b3_array['sig_x_prime'], 
             }
        ]

#and then plug them into the Simulation class
sim.params=params

# sim.simulation_folder = '/home/simone/Documents/RAYPYNG/raypyng/test'
sim.simulation_name = sim_name

# turn off reflectivity
sim.reflectivity(reflectivity=False)

# repeat the simulations as many time as needed
sim.repeat = rounds

sim.analyze = False # let RAY-UI analyze the results
sim.raypyng_analysis = True # let RAY-UI analyze the results

## This must be a list of dictionaries
sim.exports  =  [
    {beamline.DetectorAtFocus:['RawRaysOutgoing']}
    ]


# create the rml files
#sim.rml_list()

#uncomment to run the simulations
sim.run(multiprocessing=ncpu, force=False)
