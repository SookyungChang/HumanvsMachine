import pickle
import pandas as pd
from hVmFigures.plotting import plot_FoM_bar
from hVmFigures.config import DATA_DIR, OUTPUT_DIR, Nspectra, dpi

with open(DATA_DIR / f"ind_chains.pkl", "rb") as f:
    chains = pickle.load(f)

joint_chains = ['fps_fpdf', 'sm1_sm2', 'fps_sm1_sm2', 'fpdf_sm1_sm2', 'fps_fpdf_sm1_sm2']
for joint_chain in joint_chains:
    chains[joint_chain] = pd.read_parquet(DATA_DIR / f"joint_chains" / f"{joint_chain}.parquet")

chain_info = [
    ("fps_fpdf_sm1_sm2", "FPS+FPDF+SM"),
    ('fps_fpdf', 'FPS+FPDF'),
    ("fps_sm1_sm2", "FPS+SM"),
    ("fpdf_sm1_sm2", "FPDF+SM"),
    ("sm1_sm2", "SM (SM1+SM2)"),
    ("fps", "FPS"),
    ("sm1", "SM1"),
    ("sm2", "SM2"),
    ("fpdf", "FPDF"),
]

def main(name):
    fig, _ = plot_FoM_bar(chains, chain_info)
    fig.savefig(OUTPUT_DIR / name, dpi=dpi, bbox_inches="tight")
    # print(f"Figure saved to {OUTPUT_DIR / name}")

if __name__ == "__main__":
    main("FigureC.1.png")