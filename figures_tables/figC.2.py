import pickle
import pandas as pd
from chainconsumer import Chain
import matplotlib.pyplot as plt
from hVmFigures.plotting import chain_plot_with_label
from hVmFigures.config import DATA_DIR, OUTPUT_DIR, Nspectra, dpi, r, fontsize

with open(DATA_DIR / f"ind_chains_Nspectra={Nspectra}.pkl", "rb") as f:
    chains = pickle.load(f)

joint_chains = ['fps_fpdf', 'fps_sm', 'fpdf_sm', 'fps_fpdf_sm']
for joint_chain in joint_chains:
    chains[joint_chain] = pd.read_parquet(DATA_DIR / f"joint_chains_Nspectra={Nspectra}" / f"{joint_chain}.parquet")

chain_info = {
    'fps_fpdf': 'FPS+FPDF',
    'fps_sm': 'FPS+SM',
    'fpdf_sm': 'FPDF+SM',
    'sm': 'SM (SM1+SM2)',
    'fps': 'FPS',
    'fpdf': 'FPDF',
}

def get_chain_list(*chain_keys):
    color_list = ['#1f77b4', '#1b9e77', '#9467bd']
    return [Chain(samples=chains[key], name=chain_info[key], color=color_list[i], shade_alpha=0.1 + 0.1*i) for i, key in enumerate(chain_keys)]

def plot_posterior_comparison():
    nrows = 3
    ncols = 1
    fig = plt.figure(dpi=dpi, figsize=(5*r,10*r))
    gs = fig.add_gridspec(nrows, ncols, hspace=0.02)
    axes = gs.subplots(sharey=True, sharex=True)

    chain_plot_with_label(axes[0], get_chain_list('fpdf', 'fps', 'fps_fpdf'), 'upper right')
    chain_plot_with_label(axes[1], get_chain_list('fpdf', 'sm', 'fpdf_sm'), 'upper right')
    chain_plot_with_label(axes[2], get_chain_list('fps', 'sm', 'fps_sm'), 'upper right')
    for i in range(3):
        axes[i].set_ylim(1.49, 1.66)
        axes[i].set_xlim(7200, 14300)

    for i in range(3):
        axes[i].set_ylabel('γ', fontsize=fontsize)
    axes[2].set_xlabel('$T_0$ [K]', fontsize=fontsize)
    return fig, axes

def main(name):
    fig, _ = plot_posterior_comparison()
    fig.savefig(OUTPUT_DIR / name, dpi=dpi, bbox_inches="tight")
    # print(f"Figure saved to {OUTPUT_DIR / name}")

if __name__ == "__main__":
    main("FigureC.2.png")