import pickle
from hVsFigures.plotting import plot_posterior
from hVsFigures.config import DATA_DIR, OUTPUT_DIR, Nspectra, dpi

with open(DATA_DIR / f"ind_chains_Nspectra={Nspectra}.pkl", "rb") as f:
    chains = pickle.load(f)

chain_info = [
    ("sm1", "SM1"),
    ("sm2", "SM2"),
    ("sm", "SM (SM1+SM2)"),
]

color_list = ['#17becf','#1f77b4','#CC7722']

def main(name):
    fig, _ = plot_posterior(chains, chain_info, color_list)
    fig.savefig(OUTPUT_DIR / name, dpi=dpi, bbox_inches="tight")
    print(f"Figure saved to {OUTPUT_DIR / name}")

if __name__ == "__main__":
    main("Figure3.png")
    