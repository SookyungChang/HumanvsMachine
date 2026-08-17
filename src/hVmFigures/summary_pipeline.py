import numpy as np
from kymatio.numpy import Scattering1D
from itertools import combinations
from hVmFigures.summaries import get_fps, get_fpdf, tocontrast
from hVmFigures.summaries import discard_large_k_modes_and_smooth
from hVmFigures.config import DATA_DIR, num_bins, J, Q, T, hvel, flux, klist

def smooth_and_rebin(flux, klist):
    smoothed_flux = discard_large_k_modes_and_smooth(flux, klist) # smoothing mock spectra
    smoothed_rebinned_flux = np.mean(smoothed_flux.reshape(-1, 512, 8), axis = -1) # rebinning mock spectra
    rebinned_hvel = np.mean(hvel.reshape(512, 8), axis = -1)
    return smoothed_rebinned_flux, rebinned_hvel

def get_summaries(flux, hvel):
    # Flux power spectrum
    _, S_fps = get_fps(flux, hvel)

    # Flux probability density function
    S_fpdf = get_fpdf(flux, num_bins)

    # Scattering Moments
    flux_contrast = tocontrast(flux) 

    ##################################### The principle to obtain pure sm1 and sm2 #####################################
    # scattering = Scattering1D(J, flux_contrast.shape[-1], Q, 2**T, max_order=1)
    # first_order_wst = scattering(flux_contrast) # compute the first and second order scattering coefficients
    # first_order_wst = first_order_wst[:,1:,:]   # Remove the low pass part (doesn't have information)

    # second_order_wst = np.zeros((9, first_order_wst.shape[0], first_order_wst.shape[1], first_order_wst.shape[-1]))
    # for i in range(9):
    #     second_order_wst[i] = scattering(first_order_wst[:,i,:])[:,1:,:] # compute the first and second order scattering moments(coefficients)

    # # Average Pooling
    # pure_sm1 = np.mean(first_order_wst, axis=-1)
    # second_order_scattering_moments = np.mean(second_order_wst, axis=-1)

    # # Remove the first-order moments information from the second-order moments
    # pure_sm2 = np.zeros((9, first_order_wst.shape[0], 9))
    # for i in range(9):
    #     pure_sm2[i] = second_order_scattering_moments[i]/pure_sm1[:,i][:,np.newaxis]

    scattering = Scattering1D(J, flux_contrast.shape[-1], Q, 2**T)
    scattering_moments = np.mean(scattering(flux_contrast), axis=-1)

    # To make a list for the pairs from the second layer of scattering transform
    numbers = list(range(0, J+1)) # e.g. 0,1,2,3,4,5,6,7,8 when J=8
    combination_list_total = list(combinations(numbers, 2))  
    # wavelets at the second order = [0,0,0,1,2,3,4,5,6]
    combination_list_total.remove((0,1))
    combination_list_total.remove((0,2))
    combination_list_total.remove((1,2)) # remove (0,1), (0,2), (1,2) kymatio default
                                        # (should find the way to change this default)

    # Let's separate "scattering moments" array into "first and second order scattering moments" array
    first_moments = scattering_moments[:,:9]
    second_moments = scattering_moments[:,9:]

    # Delete redundant information that is already present in the first scattering moments
    pure_second_moments = np.zeros((scattering_moments.shape[0], 33))
    for i, pair in enumerate(combination_list_total):
        pure_second_moments[:,i] = second_moments[:,i]/first_moments[:,pair[0]]
    # divide each element in the second moments by the corresponding amplitude in the first moments.

    return S_fps, S_fpdf, first_moments, pure_second_moments # FPS, FPDF, SM1, SM2

if __name__ == "__main__":
    # The number of samples is 3.
    smoothed_rebinned_flux, rebinned_hvel = smooth_and_rebin(flux, klist)
    S_fps, S_fpdf, first_moments, pure_second_moments = get_summaries(smoothed_rebinned_flux, rebinned_hvel)
    print(f"FPS: {S_fps.shape} | FPDF: {S_fpdf.shape} | SM1: {first_moments.shape} | SM2: {pure_second_moments.shape}")


