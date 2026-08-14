import pickle
import pandas as pd
from hVmFigures.plotting import plot_posteriors
from hVmFigures.config import DATA_DIR, OUTPUT_DIR, Nspectra, dpi

with open(DATA_DIR / f"ind_chains_Nspectra={Nspectra}.pkl", "rb") as f:
    chains = pickle.load(f)
fps_fpdf_sm = pd.read_parquet(DATA_DIR / f"joint_chains_Nspectra={Nspectra}"/ "fps_fpdf_sm.parquet")
chains["fps_fpdf_sm"] = fps_fpdf_sm

chain_info = [
    ("fps", "FPS"),
    ("fps_fpdf_sm", "FPS+FPDF+SM"),
    ("sansa", "LyαNNA"),
]
color_list = ['#9467bd', '#1b9e77', '#d62728']
alpha_list = [0.3, 0.3, 0.3]

def main(name):
    fig, _ = plot_posteriors(chains, chain_info, color_list, alpha_list=alpha_list)
    fig.savefig(OUTPUT_DIR / name, dpi=dpi, bbox_inches="tight")
    print(f"Figure saved to {OUTPUT_DIR / name}")

if __name__ == "__main__":
    main("Figure4.png")