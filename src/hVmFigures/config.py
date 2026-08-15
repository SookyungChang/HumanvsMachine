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