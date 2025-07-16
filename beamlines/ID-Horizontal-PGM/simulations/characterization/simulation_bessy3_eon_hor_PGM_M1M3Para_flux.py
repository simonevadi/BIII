from raypyng import Simulate
from pathlib import Path
import pandas as pd
import os
import sys

from parameter import rml_file_name_bessy3_56m_hor_PGM_M1M3Para as rml_file_name

# Load the machine directory
machine_dir = Path(__file__).resolve().parents[4]      # Go four directories up
machine_dir = os.path.join(machine_dir, 'machine')
sys.path.insert(0, str(machine_dir))        # make root importable for this run

from machine_params import emittance_standard

# Load the RML file
this_file_dir=os.path.dirname(os.path.abspath(__file__))
rml_file = os.path.join('..','..','rml/'+rml_file_name+'.rml')

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
            {beamline.ExitSlit.openingWidth:SlitSize},
            {beamline.SU.photonEnergy:energy},
            {beamline.PG.orderDiffraction:order},
            {beamline.SU.numberRays:nrays}
        ]

# source parameters
params.extend([{beamline.SU.electronSigmaX:emittance_standard['sig_x_mm']},
               {beamline.SU.electronSigmaXs:emittance_standard['sig_xp_urad']},        #for the vertical PGM would be the opposite (sig_xp_urad)
               {beamline.SU.electronSigmaY:emittance_standard['sig_y_mm']},
               # {beamline.SU.electronSigmaYs:emittance_standard['sig_yp_urad']},
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
sim.raypyng_analysis=True # let raypyng analyze the results

undulator_file_path = os.path.abspath(
    os.path.join(this_file_dir, '..', '..', '..', '..', 'undulators',
                 'UndulatorFiles_BESSY_III',
                 'undulator_flux_curves_SPECTRA',
                 'UE42p5_b3_2PercCoupl_2025_smalerz_ver_300mA.csv')
)

undulator = pd.read_csv(undulator_file_path)
sim.undulator_table=undulator

## This must be a list of dictionaries
sim.exports  =  [{beamline.DetectorAtFocus:['RawRaysOutgoing']}]



#uncomment to run the simulations
sim.run(multiprocessing=ncpu, force=False, remove_rawrays=True, remove_round_folders=True)
