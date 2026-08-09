import pickle
import pandas as pd
from hVmFigures.plotting import plot_FoM_bar
from hVmFigures.config import DATA_DIR, OUTPUT_DIR, Nspectra, dpi

with open(DATA_DIR / f"ind_chains_Nspectra={Nspectra}.pkl", "rb") as f:
    chains = pickle.load(f)

joint_chains = ['fps_fpdf', 'fps_sm', 'fpdf_sm', 'fps_fpdf_sm']
for joint_chain in joint_chains:
    chains[joint_chain] = pd.read_parquet(DATA_DIR / f"joint_chains_Nspectra={Nspectra}" / f"{joint_chain}.parquet")

chain_info = [
    ("fps_fpdf_sm", "FPS+FPDF+SM"),
    ('fps_fpdf', 'FPS+FPDF'),
    ("fps_sm", "FPS+SM"),
    ("fpdf_sm", "FPDF+SM"),
    ("sm", "SM (SM1+SM2)"),
    ("fps", "FPS"),
    ("sm1", "SM1"),
    ("sm2", "SM2"),
    ("fpdf", "FPDF"),
]

def main(name):
    fig, _ = plot_FoM_bar(chains, chain_info)
    fig.savefig(OUTPUT_DIR / name, dpi=dpi, bbox_inches="tight")
    print(f"Figure saved to {OUTPUT_DIR / name}")

if __name__ == "__main__":
    main("FigureC.1.png")