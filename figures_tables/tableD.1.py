import pickle
import pandas as pd
from itertools import combinations
from hVmFigures.config import DATA_DIR
from hVmFigures.information import INFO


# DATA LOAD
with open(DATA_DIR / f"ind_chains.pkl", "rb") as f:
    ind_chains = pickle.load(f)

ind_chains['sm1_sm2'] = pd.read_parquet(DATA_DIR / "joint_chains" / "sm1_sm2.parquet")

S_list = ['fps', 'fpdf', 'sm1_sm2']

joint_chains = {}
St = 'curvature'
for Sr in S_list:
    file_name = f"{Sr}_{St}.parquet"
    try:
        joint_chains[f"{Sr}_{St}"] = pd.read_parquet(DATA_DIR / "joint_chains" / file_name)
    except FileNotFoundError:
        pass

info = INFO(ind_chains, joint_chains)

def tableD1():
    results = {f"{Sr.upper()}" : info.RCI(St, Sr) for Sr in S_list}
    return pd.DataFrame(
        {
            "Sr" : results.keys(),
            "RCI(St=Cur.)" : results.values()
        }
    ).round(3)

if __name__ == "__main__":
    print("-" * 30 + " Table D.1 " + "-" * 30)
    print(tableD1())
