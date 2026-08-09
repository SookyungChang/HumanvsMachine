import pickle
import pandas as pd
from itertools import permutations
from hVmFigures.plotting import FoM
from hVmFigures.config import DATA_DIR, OUTPUT_DIR, Nspectra


with open(DATA_DIR / f"ind_chains_Nspectra={Nspectra}.pkl", "rb") as f:
    chains = pickle.load(f)

joint_chains = ['sansa_fps', 'sansa_fpdf', 'sansa_sm', 'fps_fpdf', 'fps_sm', 'fpdf_sm', 'fps_fpdf_sm', 'cur_fps', 'cur_fpdf', 'cur_sm']
for joint_chain in joint_chains:
    chains[joint_chain] = pd.read_parquet(DATA_DIR / f"joint_chains_Nspectra={Nspectra}" / f"{joint_chain}.parquet")



def relative_form(target, reference):
    return FoM(target)/FoM(reference)

def table01():
    reference_chain = chains['sansa']
    results = {"FPS" : relative_form(chains['fps'], reference_chain),
               "FPS+FPDF+SM1" : relative_form(chains['fps_fpdf_sm'], reference_chain),
               "LyαNNA" : relative_form(reference_chain, reference_chain),}
    return pd.DataFrame(
        {
            "S" : results.keys(),
            "FoM/FoM(LyαNNA)" : results.values()
        }
    )

def RCI(St, Sr):
    St_Sr = St + '_' + Sr
    try:
        return (FoM(chains[St_Sr]) - FoM(chains[Sr]))/FoM(chains[St_Sr])
    except KeyError:
        St_Sr = Sr + '_' + St
        return (FoM(chains[St_Sr]) - FoM(chains[Sr]))/FoM(chains[St_Sr])

def table02(S_list):
    rci_fps_fpdf = RCI('fps', 'fpdf')
    print(rci_fps_fpdf)

def tableD1():
    results = {'FPS': RCI('cur', 'fps'),
               'FPDF': RCI('cur', 'fpdf'),
               'SM': RCI('cur', 'sm'),}
    return pd.DataFrame(
            {
                "Sr" : results.keys(),
                "RCI(St=Cur.)" : results.values()
            }
        )
    

if __name__ == "__main__":
    print("-" * 30 + " Table 01 " + "-" * 30)
    print(table01())

    print("-" * 30 + " Table 02 " + "-" * 30)

    S_list = ["fps", "fpdf", "sm", "sansa"]

    rci_matrix = pd.DataFrame(
        index=S_list,
        columns=S_list,
        dtype=float,
    )

    for St, Sr in permutations(S_list, 2):
        rci_matrix.loc[St, Sr] = RCI(St, Sr)

    # diagonal
    for S in S_list:
        rci_matrix.loc[S, S] = 1.0

    print(rci_matrix.to_markdown(floatfmt=".3f"))

    print("-" * 30 + " Table D1 " + "-" * 30)
    print(tableD1())

