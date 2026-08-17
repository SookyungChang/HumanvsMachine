import pickle
import pandas as pd
from itertools import combinations, permutations
from hVmFigures.config import DATA_DIR
from hVmFigures.information import INFO

# DATA LOAD
with open(DATA_DIR / f"ind_chains.pkl", "rb") as f:
    ind_chains = pickle.load(f)

ind_chains['sm1_sm2'] = pd.read_parquet(DATA_DIR / "joint_chains" / "sm1_sm2.parquet")

S_list = ['fps', 'fpdf', 'sm1_sm2', 'lyanna']

joint_chains = {}

for Sn in combinations(S_list, 2):
    file_name = f"{'_'.join(Sn)}.parquet"
    try:
        joint_chains[f"{'_'.join(Sn)}"] = pd.read_parquet(DATA_DIR / "joint_chains" / file_name)
    except FileNotFoundError:
        pass

print(joint_chains.keys())

info = INFO(ind_chains, joint_chains)

def table02():
    rci_matrix = pd.DataFrame(
        index=S_list,
        columns=S_list,
        dtype=float,
    )
    for St, Sr in permutations(S_list, 2):
        rci_matrix.loc[St, Sr] = info.RCI(St, Sr)

    # diagonal
    for S in S_list:
        rci_matrix.loc[S, S] = 1.0

    return rci_matrix.to_markdown(floatfmt=".3f")

if __name__ == "__main__":
    print("-" * 30 + " Table 02 " + "-" * 30)
    print(table02())
    