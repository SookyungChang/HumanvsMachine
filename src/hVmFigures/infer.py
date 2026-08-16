import os
import numpy as np
import scipy
import emcee
import pandas as pd
from scipy.linalg import cho_factor, cho_solve
from hVmFigures.prepro import summary_prepro, reshape_2d_data
from hVmFigures.config import Nspectra, tem_gam # thermal parameter list (T0, gamma) of 100 simulations
from hVmFigures.plotting import sampler_plot
import multiprocessing as mp



class MCMC:
    """
    Utilize the emcee package to perform MCMC-based inference.
    Nspectra : The variable Nspectra is used to rescale the posterior distribution.
    """
    def __init__(self, Smock, Smodel_mean, Npool):
        
        self.minT0, self.maxT0 = 6000.0, 15000.0
        self.mingam, self.maxgam = 1.3, 1.66
        self.Npool = Npool
        self.Length = Smock.shape[-1]
        self.Smock_mean = np.mean(Smock, axis=0)
        if self.Length == 1:                             # This case involves curvature statistic
            self.Smock_sigma = np.std(Smock, axis=0)/np.sqrt(Nspectra)
        else:                                                  
            self.Smock_cov = np.cov(Smock.T)/Nspectra

        self.c, self.low = cho_factor(self.Smock_cov) # Compute the Cholesky decomposition of the covariance to compute likelihood faster 

        self.Smodel_mean = Smodel_mean
        self.summary_emulation_functions = [self.summary_emulation(i) for i in range(self.Length)]
        
    def summary_emulation(self, i):                           # emulation for i-rd element of summary vectors
        T0, gam, summary = reshape_2d_data(tem_gam[:,0], tem_gam[:,1], self.Smodel_mean[:,i])
        emulated_summary_f = scipy.interpolate.RectBivariateSpline(T0, gam, summary) # cubic spline interpolation
        return emulated_summary_f
    
    def loglikelihood(self):
        """
            Compute Log of the likelihood.
            Since we have data for only 100 points, 
            it can be used to interpolate the values of the likelihood for the rest of the points.
        """
        delta = self.Smodel_mean - self.Smock_mean
        if self.Length == 1:                             # This case involves curvature statistic
            return sum(- 0.5 * delta**2/self.Smock_sigma**2)
        else: 
            z = cho_solve((self.c, self.low), delta)
            return - 0.5 * np.dot(delta, z)
        
    def summary_emulated_loglikelihood_function(self, theta): 
    # During each iteration of MCMC, compute the elements of the summary vectors corresponding to each pair of thermal parameters. 
    # The emulation functon created by model data was used for this computation.
        T0, gam = theta                                     
        summary_chain = np.zeros(self.Length)
        for i in range(self.Length):
            summary_chain[i] = self.summary_emulation_functions[i](T0, gam)[0][0]
        delta = summary_chain - self.Smock_mean
        z = cho_solve((self.c, self.low), delta)
        return - 0.5 * np.dot(delta, z)
    
    def loglikelihood_emulated_function(self, theta):
        T0, gam = theta
        return self.loglikeli_emulation(T0, gam)
    
    def prior_range(self, theta):
        T0, gam = theta
        if self.minT0 < T0 < self.maxT0 and self.mingam < gam < self.maxgam:
            return 0.0
        return -np.inf
    
    def posterior(self, theta):
        # print("PID:", os.getpid(), flush=True)
        lp = self.prior_range(theta)                          # log-prior
        return lp + self.summary_emulated_loglikelihood_function(theta)

        # the number of iteration: niter
        # the number of walkers: nwalkers
        # the initial point is determined by maximum likelihood estimation
    def mcmc(self, niter=6000, nwalkers=50, initial=np.array([10090.90909091, 1.57636364])):
        ndim = len(initial)
        # The initial positions of each walker are close to the 'initial'
        p0 = [np.array(initial) * (1 + 1e-2 * (np.random.randn(ndim)) ) for i in range(nwalkers)]
        # print("CPU count:", mp.cpu_count()) 
        if self.Npool is False:
            sampler = emcee.EnsembleSampler(nwalkers, ndim, self.posterior)
            sampler.run_mcmc(p0, niter, progress=True)
        else:
            with mp.Pool(16) as pool:
                print("Pool created")
                
                sampler = emcee.EnsembleSampler(
                    nwalkers,
                    ndim,
                    self.posterior,
                    pool=pool
                )
                sampler.run_mcmc(p0, niter, progress=True)
        return sampler
        
    def reduced_chain(self, sampler, thin=1):
        tau = sampler.get_autocorr_time()
        # remove burn-in phase to remove the information from the initial point
        reduced_chain = sampler.get_chain(discard = int(np.mean(tau * 3)), thin = thin, flat=True)
        reduced_chain = pd.DataFrame(reduced_chain)
        reduced_chain.columns = ['$T_0$ [K]', 'γ']
        return reduced_chain
    