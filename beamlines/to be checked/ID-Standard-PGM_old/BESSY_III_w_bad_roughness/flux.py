import numpy as np
def retrieve_flux_beamline(folder_name,source,oe,nsimulations,rounds=1,current=0.3):
        """Extract the flux from object ScalarBeamProperties and from source ScalarElementProperties.

        This function takes as arguments the name of the 
        simulation folder, the exported objet in RAY-UI and there
        number of simulations and returns the flux at the optical element in 
        percentage and in number of photons, and the flux produced
        by the dipole.
        It requires ScalarBeamProperties to be exported for the desired optical element,
        if the source is a dipole it requires ScalarElementProperties to be exported for the Dipole

        Args:
            folder_name (str): the path to the folder where the simulations are
            source (str): the source name
            oe (str): the optical element name
            nsimulations (int): the number of simulations
            rounds (int): the number of rounds of simulations
            current (float, optional): the ring current in Ampere. Defaults to 0.3.

        Returns:
            if the source is a Dipole:
                photon_flux (np.array) : the photon flux at the optical element
                flux_percent (np.array) : the photon flux in percentage relative to the source
                source_Photon_flux (np.array) : the photon flux of the source
            else:
                flux_percent (np.array) : the photon flux in percentage relative to the source
        """        
        scale_factor = current/0.1
        flux_percent = np.zeros(nsimulations)
        if source == 'Dipole':
            flux         = np.zeros(nsimulations)
            flux_dipole  = np.zeros(nsimulations)
        for n in range(nsimulations):
            try:
                for r in range(rounds):
                    temp = np.loadtxt(folder_name+'/round_'+str(r)+'/'+str(n)+'_'+oe+'-ScalarBeamProperties.csv',skiprows = 2)
                    flux_percent[n] += temp[25]/rounds
                    if source == 'Dipole':
                        dipole_abs_flux = np.loadtxt(folder_name+'/round_'+str(r)+'/'+str(n)+'_Dipole-ScalarElementProperties.csv',skiprows = 2)
                        #flux[n]         += (dipole_abs_flux[12]*temp[25]/100)/rounds
                        #flux_dipole[n]  += dipole_abs_flux[12]/rounds                        
                        # now apparently dipole_abs_flux is only one number....
                        flux[n]         += (dipole_abs_flux*temp[25]/100)/rounds
                        flux_dipole[n]  += dipole_abs_flux/rounds
                
            except OSError:
                print('######################')
                print(n, 'NOT FOUND:\n'+folder_name+'/round_'+str(r)+'/'+str(n)+'_'+oe+'-ScalarBeamProperties.csv')
                continue
        flux_percent = np.array(flux_percent)
        if source == 'Dipole':
            flux = np.array(flux)
            flux_dipole = np.array(flux_dipole)
            return flux*scale_factor, flux_percent, flux_dipole*scale_factor
        return flux_percent*scale_factor
