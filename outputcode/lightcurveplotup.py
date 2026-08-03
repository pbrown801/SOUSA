import matplotlib.pyplot as plt
import numpy as np
import os
import glob

def process_light_curve(filename, output_dir='SOUSA light curve plots'):
    """
    Process a single light curve file and create a plot.
    
    Parameters:
    -----------
    filename : str
        Path to the .dat file
    output_dir : str
        Directory to save the output plots
    """
    
    # Extract the supernova name from the filename
    basename = os.path.basename(filename)
    snname = basename.replace('.dat', '').replace('_uvotB15.1', '')
    
    print(f"Processing {snname}...")
    
    try:
        # Read the data
        data = open(filename, 'r')
        
        # Initialize lists for each filter - now including limits
        uvw2mjd, uvw2mag, uvw2magerr = [], [], []
        uvw2sat_mjd, uvw2sat_val = [], []  # saturation limits
        uvw2sig_mjd, uvw2sig_val = [], []  # 3-sigma upper limits
        
        uvm2mjd, uvm2mag, uvm2magerr = [], [], []
        uvm2sat_mjd, uvm2sat_val = [], []
        uvm2sig_mjd, uvm2sig_val = [], []
        
        uvw1mjd, uvw1mag, uvw1magerr = [], [], []
        uvw1sat_mjd, uvw1sat_val = [], []
        uvw1sig_mjd, uvw1sig_val = [], []
        
        umjd, umag, umagerr = [], [], []
        usat_mjd, usat_val = [], []
        usig_mjd, usig_val = [], []
        
        bmjd, bmag, bmagerr = [], [], []
        bsat_mjd, bsat_val = [], []
        bsig_mjd, bsig_val = [], []
        
        vmjd, vmag, vmagerr = [], [], []
        vsat_mjd, vsat_val = [], []
        vsig_mjd, vsig_val = [], []
        
        # Read the data from the file
        lines = np.genfromtxt(data, dtype=[('filter', 'S5'), ('mjd', float), ('mag', float), ('maggerr', float), 
                                            ('siglim', float), ('satlim', float), ('rate', float), ('rateerr', float)], 
                              usecols=(0, 1, 2, 3, 4, 5, 6, 7), unpack=True, autostrip=True, comments='#')
        
        # Handle single data point case - numpy returns scalars instead of arrays
        if lines[0].ndim == 0:  # Single data point
            # Convert scalars to single-element arrays
            filters = np.array([lines[0]])
            mjd = np.array([lines[1]])
            mag = np.array([lines[2]])
            magerr = np.array([lines[3]])
            siglim = np.array([lines[4]])
            satlim = np.array([lines[5]])
            rate = np.array([lines[6]])
            rateerr = np.array([lines[7]])
        else:  # Multiple data points
            filters = lines[0]
            mjd = lines[1]
            mag = lines[2]
            magerr = lines[3]
            siglim = lines[4]
            satlim = lines[5]
            rate = lines[6]
            rateerr = lines[7]
        
        # Filter out NULL values and populate filter-specific lists
        for i in range(len(filters)):
            # Convert filter name to string if it's in bytes format
            if isinstance(filters[i], bytes):
                filter_name = filters[i].decode('utf-8')
            else:
                filter_name = filters[i]
            
            mag_is_null = np.isnan(mag[i])
            rate_is_null = np.isnan(rate[i])
            
            # Determine what to plot based on the rules:
            # 1. If mag and rate are both NULL → plot saturation limit (upward triangle)
            # 2. If mag is NULL and rate is finite → plot 3-sigma upper limit (downward triangle)
            # 3. If mag is finite → plot normal data point with error bars
            
            if filter_name == 'UVW2':
                if mag_is_null and rate_is_null:
                    # Saturation limit
                    uvw2sat_mjd.append(mjd[i])
                    uvw2sat_val.append(satlim[i])
                elif mag_is_null and not rate_is_null:
                    # 3-sigma upper limit
                    uvw2sig_mjd.append(mjd[i])
                    uvw2sig_val.append(siglim[i])
                else:
                    # Normal data point
                    uvw2mjd.append(mjd[i])
                    uvw2mag.append(mag[i])
                    uvw2magerr.append(magerr[i])
                    
            elif filter_name == 'UVM2':
                if mag_is_null and rate_is_null:
                    uvm2sat_mjd.append(mjd[i])
                    uvm2sat_val.append(satlim[i])
                elif mag_is_null and not rate_is_null:
                    uvm2sig_mjd.append(mjd[i])
                    uvm2sig_val.append(siglim[i])
                else:
                    uvm2mjd.append(mjd[i])
                    uvm2mag.append(mag[i])
                    uvm2magerr.append(magerr[i])
                    
            elif filter_name == 'UVW1':
                if mag_is_null and rate_is_null:
                    uvw1sat_mjd.append(mjd[i])
                    uvw1sat_val.append(satlim[i])
                elif mag_is_null and not rate_is_null:
                    uvw1sig_mjd.append(mjd[i])
                    uvw1sig_val.append(siglim[i])
                else:
                    uvw1mjd.append(mjd[i])
                    uvw1mag.append(mag[i])
                    uvw1magerr.append(magerr[i])
                    
            elif filter_name == 'U':
                if mag_is_null and rate_is_null:
                    usat_mjd.append(mjd[i])
                    usat_val.append(satlim[i])
                elif mag_is_null and not rate_is_null:
                    usig_mjd.append(mjd[i])
                    usig_val.append(siglim[i])
                else:
                    umjd.append(mjd[i])
                    umag.append(mag[i])
                    umagerr.append(magerr[i])
                    
            elif filter_name == 'B':
                if mag_is_null and rate_is_null:
                    bsat_mjd.append(mjd[i])
                    bsat_val.append(satlim[i])
                elif mag_is_null and not rate_is_null:
                    bsig_mjd.append(mjd[i])
                    bsig_val.append(siglim[i])
                else:
                    bmjd.append(mjd[i])
                    bmag.append(mag[i])
                    bmagerr.append(magerr[i])
                    
            elif filter_name == 'V':
                if mag_is_null and rate_is_null:
                    vsat_mjd.append(mjd[i])
                    vsat_val.append(satlim[i])
                elif mag_is_null and not rate_is_null:
                    vsig_mjd.append(mjd[i])
                    vsig_val.append(siglim[i])
                else:
                    vmjd.append(mjd[i])
                    vmag.append(mag[i])
                    vmagerr.append(magerr[i])
        
        # Create the plot
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot data for each filter (only if data exists)
        #UVW2
        if uvw2mjd:
            ax.errorbar(uvw2mjd, uvw2mag, yerr=uvw2magerr, linestyle='-', marker='o', 
                       label='UVW2', color='black', markersize=6, capsize=3)
        if uvw2sat_mjd and not uvw2mjd:  # Only label if no regular data
            ax.scatter(uvw2sat_mjd, uvw2sat_val, marker='^', color='black', s=80, 
                      facecolors='none', edgecolors='black', linewidths=1.5, label='UVW2')
        elif uvw2sat_mjd:  # Has regular data, don't label
            ax.scatter(uvw2sat_mjd, uvw2sat_val, marker='^', color='black', s=80, 
                      facecolors='none', edgecolors='black', linewidths=1.5)
        if uvw2sig_mjd and not uvw2mjd:  # Only label if no regular data
            ax.scatter(uvw2sig_mjd, uvw2sig_val, marker='v', color='black', s=80,
                      facecolors='none', edgecolors='black', linewidths=1.5, label='UVW2')
        elif uvw2sig_mjd:  # Has regular data, don't label
            ax.scatter(uvw2sig_mjd, uvw2sig_val, marker='v', color='black', s=80,
                      facecolors='none', edgecolors='black', linewidths=1.5)
        
        # UVW1 filter
        if uvw1mjd:
            ax.errorbar(uvw1mjd, uvw1mag, yerr=uvw1magerr, linestyle='-', marker='o', 
                       label='UVW1', color='red', markersize=6, capsize=3)
        if uvw1sat_mjd and not uvw1mjd:
            ax.scatter(uvw1sat_mjd, uvw1sat_val, marker='^', color='red', s=80,
                      facecolors='none', edgecolors='red', linewidths=1.5, label='UVW1')
        elif uvw1sat_mjd:
            ax.scatter(uvw1sat_mjd, uvw1sat_val, marker='^', color='red', s=80,
                      facecolors='none', edgecolors='red', linewidths=1.5)
        if uvw1sig_mjd and not uvw1mjd:
            ax.scatter(uvw1sig_mjd, uvw1sig_val, marker='v', color='red', s=80,
                      facecolors='none', edgecolors='red', linewidths=1.5, label='UVW1')
        elif uvw1sig_mjd:
            ax.scatter(uvw1sig_mjd, uvw1sig_val, marker='v', color='red', s=80,
                      facecolors='none', edgecolors='red', linewidths=1.5)
        
        # UVM2 filter
        if uvm2mjd:
            ax.errorbar(uvm2mjd, uvm2mag, yerr=uvm2magerr, linestyle='-', marker='*', 
                       label='UVM2', color='maroon', markersize=8, capsize=3)
        if uvm2sat_mjd and not uvm2mjd:
            ax.scatter(uvm2sat_mjd, uvm2sat_val, marker='^', color='maroon', s=80,
                      facecolors='none', edgecolors='maroon', linewidths=1.5, label='UVM2')
        elif uvm2sat_mjd:
            ax.scatter(uvm2sat_mjd, uvm2sat_val, marker='^', color='maroon', s=80,
                      facecolors='none', edgecolors='maroon', linewidths=1.5)
        if uvm2sig_mjd and not uvm2mjd:
            ax.scatter(uvm2sig_mjd, uvm2sig_val, marker='v', color='maroon', s=80,
                      facecolors='none', edgecolors='maroon', linewidths=1.5, label='UVM2')
        elif uvm2sig_mjd:
            ax.scatter(uvm2sig_mjd, uvm2sig_val, marker='v', color='maroon', s=80,
                      facecolors='none', edgecolors='maroon', linewidths=1.5)
        
        # U filter
        if umjd:
            ax.errorbar(umjd, umag, yerr=umagerr, linestyle='-', marker='D', 
                       label='U', color='violet', markersize=6, capsize=3)
        if usat_mjd and not umjd:
            ax.scatter(usat_mjd, usat_val, marker='^', color='violet', s=80,
                      facecolors='none', edgecolors='violet', linewidths=1.5, label='U')
        elif usat_mjd:
            ax.scatter(usat_mjd, usat_val, marker='^', color='violet', s=80,
                      facecolors='none', edgecolors='violet', linewidths=1.5)
        if usig_mjd and not umjd:
            ax.scatter(usig_mjd, usig_val, marker='v', color='violet', s=80,
                      facecolors='none', edgecolors='violet', linewidths=1.5, label='U')
        elif usig_mjd:
            ax.scatter(usig_mjd, usig_val, marker='v', color='violet', s=80,
                      facecolors='none', edgecolors='violet', linewidths=1.5)
        
        # B filter
        if bmjd:
            ax.errorbar(bmjd, bmag, yerr=bmagerr, linestyle='-', marker='s', 
                       label='B', color='blue', markersize=6, capsize=3)
        if bsat_mjd and not bmjd:
            ax.scatter(bsat_mjd, bsat_val, marker='^', color='blue', s=80,
                      facecolors='none', edgecolors='blue', linewidths=1.5, label='B')
        elif bsat_mjd:
            ax.scatter(bsat_mjd, bsat_val, marker='^', color='blue', s=80,
                      facecolors='none', edgecolors='blue', linewidths=1.5)
        if bsig_mjd and not bmjd:
            ax.scatter(bsig_mjd, bsig_val, marker='v', color='blue', s=80,
                      facecolors='none', edgecolors='blue', linewidths=1.5, label='B')
        elif bsig_mjd:
            ax.scatter(bsig_mjd, bsig_val, marker='v', color='blue', s=80,
                      facecolors='none', edgecolors='blue', linewidths=1.5)
        
        # V filter
        if vmjd:
            ax.errorbar(vmjd, vmag, yerr=vmagerr, linestyle='-', marker='^', 
                       label='V', color='green', markersize=6, capsize=3)
        if vsat_mjd and not vmjd:
            ax.scatter(vsat_mjd, vsat_val, marker='^', color='green', s=80,
                      facecolors='none', edgecolors='green', linewidths=1.5, label='V')
        elif vsat_mjd:
            ax.scatter(vsat_mjd, vsat_val, marker='^', color='green', s=80,
                      facecolors='none', edgecolors='green', linewidths=1.5)
        if vsig_mjd and not vmjd:
            ax.scatter(vsig_mjd, vsig_val, marker='v', color='green', s=80,
                      facecolors='none', edgecolors='green', linewidths=1.5, label='V')
        elif vsig_mjd:
            ax.scatter(vsig_mjd, vsig_val, marker='v', color='green', s=80,
                      facecolors='none', edgecolors='green', linewidths=1.5)
        
        # Set plot properties
        ax.set_title(f'{snname} Light Curve', fontsize=14, fontweight='bold')
        ax.set_xlabel('Modified Julian Date', fontsize=12)
        ax.set_ylabel('Magnitude', fontsize=12)
        ax.invert_yaxis()  # Lower magnitude = brighter object
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        # Save the figure
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        savename = os.path.join(output_dir, f'{snname}_lightcurve.jpg')
        plt.savefig(savename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"  ✓ Saved plot to {savename}")
        return True
        
    except Exception as e:
        print(f"  ✗ Error processing {snname}: {str(e)}")
        return False


def main():
    """
    Main function to process all light curve files in the SOUSA folder.
    """
    # Path to SOUSA folder (adjust if needed)
    sousa_path = r'/Users/supernova/Desktop/SN/github/SOUSA/data'
    
    # Find all .dat files
    dat_files = glob.glob(os.path.join(sousa_path, '*.dat'))
    
    if not dat_files:
        print(f"No .dat files found in {sousa_path}")
        print("Please check that the SOUSA folder path is correct.")
        return
    
    print(f"Found {len(dat_files)} light curve files to process.\n")
    
    # Process each file
    successful = 0
    failed = 0
    failed_files = [] # track which files failed

    for filename in dat_files:
        if process_light_curve(filename):
            successful += 1
        else:
            failed += 1
            failed_files.append(os.path.basename(filename))  # Store just the filename

    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Processing complete!")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"{'='*50}")

    if failed_files:
        print(f"\nFailed files:")
        for failed_file in failed_files:
            print(f"  - {failed_file}")


if __name__ == "__main__":
    main()