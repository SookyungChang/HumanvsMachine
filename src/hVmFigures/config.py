from pathlib import Path
import numpy as np

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Directories
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

# settings
Nspectra = 500

# Plot settings
alpha_list = [0.05, 0.1, 0.15, 0.3, 0.4]
sigmas = [0,1,2]
dpi = 300
r = 0.9
fontsize = 12

# Inference settings
tem_gam = np.load(DATA_DIR / "tem_gam.npy") # thermal parameter list (T0, gamma) of 100 simulations
Niter = 30000

# Summary settings
num_bins = 25
J = 8 # J determines the number of wavelet filters, e.g. j=0,1,2,3,4,5,6,7,8 
Q = 1 # Increasing the Number of Filters by a Factor of Q
T = 0 # the size of the low pass filter (isn't used here)

hvel = np.load(DATA_DIR /'v_h_skewer_redshift_2.2_cosmo_grid_1.npy') # Hubble velocity [km/s]
flux = np.load(DATA_DIR /'F_array_3_skewers_redshift_2.2_cosmo_grid_1.npy') # Transmitted Flux samples
klist = np.load(DATA_DIR / 'klist.npy')