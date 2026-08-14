import numpy as np
import pandas as pd
import pickle
from hVmFigures.prepro import summary_prepro, reshape_2d_data
from hVmFigures.config import Nspectra, DATA_DIR
from hVmFigures.plotting import sampler_plot
from hVmFigures.infer import MCMC

def inference(S_name_list, niter=6000):
    Slist = []
    for S_name in S_name_list:
        with open(DATA_DIR / f"summaries/S_{S_name}.pkl", "rb") as f:
            Sn = pickle.load(f)
        Slist.append(Sn)

    Smock_j = np.concatenate([Sn['Smock'] for Sn in Slist], axis=1)
    Smodel_j_mean = np.concatenate([Sn['Smodel_mean'] for Sn in Slist], axis=1)

    mcmc = MCMC(Smock_j, Smodel_j_mean)
    sampler = mcmc.mcmc(niter=niter)
    sampler_plot(sampler)
    chain = mcmc.reduced_chain(sampler,thin=1)
    return chain