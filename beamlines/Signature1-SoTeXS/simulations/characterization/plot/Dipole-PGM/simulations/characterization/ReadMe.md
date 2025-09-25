# Dipole PGM
- In the folder `frontend` there is the design of the frontend. The first one is the ID, then we have Dipole 2 and then Dipole 4. 

## Design
- The current design is done for **Dipole 2**. Total space for the beamline and endstation should be around 58 meters. Currently the beamline is 56 meters long
- **Dipole parameters**:
    - Source width/height: 11µm/3.3µm
    - Vertical E-beam divergency: 0.6 µrad
    - Horizontal divergence: 1.5 mrad (chosen such that M1 is not overillumnated)
    - electron energy 2.5 GeV
    - **Magnetic Field Strength 1.3 T**
    - Critical energy 5.4 keV
    - Bending Radius 6.4 m
- **M1** and the **PGM** are **inside the radiation protection wall**: this allows to maximize the M3-ExitSlit and ExitSlit-KBs distances, increasing energy resolution and focus size.
- M1 is placed 10 meters from the source
- The PGM is placed 13m from the source
- The refocusing is done with KB optics: the first one is focusing vertically and the second one horizontally (As we have much larger beam horizontally)
- The distance between the second KB and the focus is 1 meter.
- In the simulations cff is 2.25 and the ExitSlit opening is 100 µm. 

## ToDo
- Make sure the placement of M1 and and the PGM inside the radiation protection wall is fine.
- Clarify properties of the Dipole. Can we decide the Magnetic Field or is it fixed?