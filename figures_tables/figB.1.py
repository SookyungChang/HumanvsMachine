import pickle
import numpy as np
from hVmFigures.plotting import plot_covariance
from hVmFigures.config import DATA_DIR, OUTPUT_DIR, Nspectra, dpi

S_list = ['fps', 'fpdf', 'sm1', 'sm2', 'lyanna']

summaries ={}

for Sn in S_list:
    with open(DATA_DIR / "summaries" / f"S_{Sn}", "rb") as f:
        summaries[Sn] = pickle.load(f)

mock_joint_sv = np.concatenate((summaries['fps'], 
                                np.repeat(summaries['fpdf25'], 11, axis=-1),
                                np.repeat(summaries['pure_sm1'], 28, axis=-1),
                                np.repeat(summaries['pure_sm2'], 7, axis=-1)),axis=1)

positions = [128, 128*3, 128*5, 128*7]
labels = ['FPS', 'FPDF', 'SM1', 'SM2']

def main(name):
    fig = plot_covariance(mock_joint_sv, labels, positions)
    fig.savefig(OUTPUT_DIR / name, dpi=dpi, bbox_inches="tight")
    # print(f"Figure saved to {OUTPUT_DIR / name}")

if __name__ == "__main__":
    main("FigureB.1.png")