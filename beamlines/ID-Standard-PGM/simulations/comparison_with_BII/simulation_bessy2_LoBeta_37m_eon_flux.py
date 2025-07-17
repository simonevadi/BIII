from raypyng import Simulate
from pathlib import Path
import pandas as pd
import os
import sys
import importlib.util

from parameter import rml_file_name_bessy2_LoBeta_37m as rml_file_name

# Load the machine directory
machine_dir = Path(__file__).resolve().parents[4]    # Go four directories up
machine_dir = os.path.join(machine_dir, 'machine')
sys.path.insert(0, str(machine_dir))                 # make root importable for this run

# Load the machine parameter file
machine_file = "BESSY_II_LoBeta_machine_params"  # File name of the machine parameters module
machine_params_path = os.path.join(machine_dir, machine_file + ".py")
spec = importlib.util.spec_from_file_location("emittance_module", machine_params_path)
emittance_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(emittance_module)
emittance_standard = emittance_module.emittance_standard

# Load the RML file
this_file_dir=os.path.dirname(os.path.realpath(__file__))
rml_file = os.path.join('rml_b2/'+rml_file_name+'.rml')

sim = Simulate(rml_file, hide=True)

rml=sim.rml
beamline = sim.rml.beamline

# cpu
from parameter import ncpu

# name for simulation folder
sim_name = rml_file_name+'_FLUX'

# define the values of the parameters to scan 
from parameter import order, energy_flux as energy, round_flux as rounds    
from parameter import SlitSize, cff, nrays_flux as nrays

# define a list of dictionaries with the parameters to scan
params = [  
            {beamline.PG.cFactor:cff}, 
            {beamline.ExitSlit.openingHeight:SlitSize},
            {beamline.SU.photonEnergy:energy},
            {beamline.PG.orderDiffraction:order},
            {beamline.SU.numberRays:nrays}
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

# turn on/off reflectivity (on=True / off=False)
sim.reflectivity(True)

# repeat the simulations as many time as needed
sim.repeat = rounds

sim.analyze = False # don't let RAY-UI analyze the results
sim.raypyng_analysis = True # let raypyng analyze the results


undulator_file_path = os.path.abspath(
    os.path.join(this_file_dir, '..', '..', '..', '..', 'undulators',
                 'UndulatorFiles_BESSY_II',
                 'undulator_flux_curves_SPECTRA',
                 'UE46_b2_LoBeta_2PercCoupl_2025_smalerz_300mA.txt')
)

undulator = pd.read_csv(undulator_file_path, delimiter='\t')
sim.undulator_table=undulator

## This must be a list of dictionaries
sim.exports  =  [{beamline.SU:['RawRaysOutgoing']},
                 {beamline.DetectorAtFocus:['RawRaysOutgoing']}]

#uncomment to run the simulations
sim.run(multiprocessing=ncpu, force=False, remove_rawrays=True, remove_round_folders=True)
