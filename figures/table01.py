import pickle
import pandas as pd
from itertools import combinations
from hVmFigures.config import DATA_DIR
from hVmFigures.information import INFO


# DATA LOAD
with open(DATA_DIR / f"ind_chains.pkl", "rb") as f:
    ind_chains = pickle.load(f)

S_list = ['fps', 'fpdf', 'sm1', 'sm2', 'lyanna']
joint_chains = {}
for n in [2, 3, 4]:
    for Sn in combinations(S_list, n):
        file_name = f"{'_'.join(Sn)}.parquet"
        try:
            joint_chains[f"{'_'.join(Sn)}"] = pd.read_parquet(DATA_DIR / "joint_chains" / file_name)
        except FileNotFoundError:
            pass

info = INFO(ind_chains, joint_chains)

def table01():
    results = {"FPS" : info.relative_form('fps'),
               "FPDF" : info.relative_form('fpdf'),
               "SM1" : info.relative_form('sm1'),
               "SM2" : info.relative_form('sm2'),
               "SM" : info.relative_form('sm1_sm2'),
               "FPS+FPDF" : info.relative_form('fps_fpdf'),
               "FPS+FPDF+SM" : info.relative_form('fps_fpdf_sm1_sm2'),
               "LyαNNA" : info.relative_form('lyanna'),}
    return pd.DataFrame(
        {
            "S" : results.keys(),
            "FoM/FoM(LyαNNA)" : results.values()
        }
    ).round(3)

if __name__ == "__main__":
    print("-" * 30 + " Table 01 " + "-" * 30)
    print(table01())

