import numpy as np
from pathlib import Path
import pickle
from itertools import combinations
from hVmFigures.config import DATA_DIR, Niter
from hVmFigures.plotting import sampler_plot
from hVmFigures.infer import MCMC


def inference(S_name_list, niter, plot=True, Npool=False):
    Slist = []
    for S_name in S_name_list:
        with open(DATA_DIR / f"summaries/S_{S_name}.pkl", "rb") as f:
            Sn = pickle.load(f)
        Slist.append(Sn)

    Smock_j = np.concatenate([Sn['Smock'] for Sn in Slist], axis=1)
    Smodel_j_mean = np.concatenate([Sn['Smodel_mean'] for Sn in Slist], axis=1)

    mcmc = MCMC(Smock_j, Smodel_j_mean, Npool=Npool)
    sampler = mcmc.mcmc(niter=niter)
    if plot is True:
        sampler_plot(sampler)
    chain = mcmc.reduced_chain(sampler,thin=1)
    return chain

if __name__ == "__main__":
    S_list = ['fps', 'fpdf', 'sm1', 'sm2', 'lyanna', 'curvature']
    for n in [2,3,4,5]:
        for Sn in combinations(S_list, n):
            file_name = f"{'_'.join(Sn)}.parquet"
            file_path = Path(DATA_DIR / "joint_chains" / file_name)
            if file_path.exists():
                pass
            else:
                print(f"Inferring... {file_name}")
                chain = inference([*Sn], niter=Niter)
                chain.to_parquet(DATA_DIR / "joint_chains" / file_name)

    
