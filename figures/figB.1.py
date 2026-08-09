import pickle
import numpy as np
from hVmFigures.plotting import plot_covariance
from hVmFigures.config import DATA_DIR, OUTPUT_DIR, Nspectra, dpi

with open(DATA_DIR / f"summaries_for_cov_Nspectra={Nspectra}.pkl", "rb") as f:
    summaries_for_cov = pickle.load(f)

mock_joint_sv = np.concatenate((summaries_for_cov['fps'], 
                                np.repeat(summaries_for_cov['fpdf25'], 11, axis=-1),
                                np.repeat(summaries_for_cov['pure_sm1'], 28, axis=-1),
                                np.repeat(summaries_for_cov['pure_sm2'], 7, axis=-1)),axis=1)

positions = [128, 128*3, 128*5, 128*7]
labels = ['FPS', 'FPDF', 'SM1', 'SM2']

def main(name):
    fig = plot_covariance(mock_joint_sv, labels, positions)
    fig.savefig(OUTPUT_DIR / name, dpi=dpi, bbox_inches="tight")
    print(f"Figure saved to {OUTPUT_DIR / name}")

if __name__ == "__main__":
    main("FigureB.1.png")