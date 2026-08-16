import pickle
import pandas as pd
from hVmFigures.plotting import plot_posteriors
from hVmFigures.config import DATA_DIR, OUTPUT_DIR, dpi

with open(DATA_DIR / f"ind_chains.pkl", "rb") as f:
    chains = pickle.load(f)
chains["fps_fpdf_sm"] = pd.read_parquet(DATA_DIR / f"joint_chains"/ "fps_fpdf_sm1_sm2.parquet")
chains["fps_fpdf"] = pd.read_parquet(DATA_DIR / f"joint_chains"/ "fps_fpdf.parquet")

chain_info = [
    ("fps", "FPS"),
    ("fps_fpdf", "FPS+FPDF"),
    ("fps_fpdf_sm", "FPS+FPDF+SM"),
    ("lyanna", "LyαNNA"),
]
color_list = ['#9467bd', "#949d2f", '#1b9e77', '#d62728']
alpha_list = [0.3, 0.3, 0.3, 0.3]

def main(name):
    fig, _ = plot_posteriors(chains, chain_info, color_list, alpha_list=alpha_list)
    fig.savefig(OUTPUT_DIR / name, dpi=dpi, bbox_inches="tight")
    # print(f"Figure saved to {OUTPUT_DIR / name}")

if __name__ == "__main__":
    main("Figure4.png")