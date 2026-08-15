import numpy as np
import pandas as pd
import pickle
from itertools import permutations
from hVmFigures.prepro import summary_prepro, reshape_2d_data
from hVmFigures.config import Nspectra, DATA_DIR, Niter
from hVmFigures.plotting import sampler_plot
from hVmFigures.infer import MCMC


def inference(S_name_list, niter=6000, plot=True, Npool=False):
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
    S_list = ['fps', 'fpdf', 'sm1', 'sm2', 'lyanna']
    for S1, S2 in permutations(S_list, 2):
        chain = inference([S1, S2], niter=Niter)
        with open(DATA_DIR / "joint_chains" / f"{S1}_{S2}.pkl", "wb") as f:
            pickle.dump(chain, f)

    
