import numpy as np
import scipy
from scipy.fft import fft, fftfreq, rfft, irfft
from scipy.interpolate import splrep, BSpline

def discard_large_k_modes_and_smooth(flux, k, cutoff_k_idx = 257, R_FWHM = 10820.21):
    # smoothing and removing smaller scale than k corresponding to cutoff_k_idx
    """
    R_FWHM : spectral resolution # 60000/2.35482**2 the reference of this number
    c : speed of light (km/s)
    The convolution of the flux and a Gaussian fuctnion with sigma = c/(R_FWHM*np.sqrt(8*np.log(2)))
    * https://mathworld.wolfram.com/FourierTransformGaussian.html
    Remove the k-modes larger than 0.182 s/km.
    """
    fft_skewers = rfft(flux) 
    v_sigma     = 2.998E5 / R_FWHM / 2.35482 # 2.998E5 / R_FWHM * 2.35482??
    kernel      = np.exp(-v_sigma**2 * k**2 / 2.)
    fft_skewers*= kernel
    fft_skewers[:, cutoff_k_idx:] = 0j
    irfft_skewers                 = irfft(fft_skewers)
    return irfft_skewers

def tocontrast(flux): # contrast flux \delta_F(v)    
    return flux/np.mean(flux,axis=1)[:,np.newaxis] - 1

def get_fps(flux, hvel):
    """
    flux : transmitted flux of quasar absorption spectrum in hubble velocity (v) unit
    delta v = 17.245 km/s

    Convert these flux into contrast form F/Fmean - 1 : delta_F(v)
    Compute the discrete Fourier transform of flux, using a fast Fourier Transform (FFT)
    Wave vector k = 2*np.pi/v (s/km) : hat_delta_F(k)

    Power spectrum is written as the ensemble average over flux realization of hat_delta_F(k)
    """                                            
    Nx = flux.shape[-1]                                    # the length of each spectrum data, # hvel: hubble velocity list
    delx = abs(hvel[0]-hvel[1])                            # the length of the minimum interval of hvel 
    klist = np.fft.rfftfreq(int(Nx), d=delx) * 2 * np.pi   # mode list
    alpha = delx/Nx                                        # Normalization
    
    if flux.ndim == 2:                                                   # for mock data
        contrasted_flux = flux / np.mean(flux, axis=1)[:,np.newaxis] - 1 # contrast form : flux/mean_flux - 1
        hat_contrasted_flux = np.fft.rfft(contrasted_flux, axis=1)       # Fourier transform
        fps = alpha * np.absolute(hat_contrasted_flux)**2                # power spectrum ~ |F(flux)|^2
        return klist, fps

    else:                                                                # for model data
        contrasted_flux = flux / np.mean(flux, axis=2)[:,:,np.newaxis] - 1
        hat_contrasted_flux = np.fft.rfft(contrasted_flux, axis=2)
        fps = alpha * np.absolute(hat_contrasted_flux)**2
        return klist, fps
    

def get_fpdf(flux, num_bins):
    bins = np.linspace(0, 1, num_bins+1)                       # list of bins
    x = (bins[1:] + bins[:-1])/2                               # x-axis of PDF
    x = x[:-1]                                                 # remove the last bin due to its redundancy
    
    fpdf = np.zeros((flux.shape[0],num_bins))                  # FPDF mock shape (num of spectra, num of bins)
    for i in range(flux.shape[0]):
        hist = np.histogram(flux[i], bins=bins, density=True)  # density=True:probability density function
        fpdf[i,:] = hist[0]                                    # compute PDF of transmitted flux of mock data
    return fpdf[:,:-1]                                         # remove the last bin due to its redundancy

    
class Curvature: # Curvature statistic
    def __init__(self, flux):
        self.rebinned_hvel = np.load('/project/ls-gruen/users/sookyung.chang/smooth/rebinned_hvel.npy')
        self.flux = flux
    def flux_to_fuc(self, s=0):
        tck = splrep(self.rebinned_hvel, self.flux , s=s)
        return BSpline(*tck)
    def kappa(self):
        x = self.rebinned_hvel
        flux_fuc = self.flux_to_fuc()
        dx = x[1]-x[0]
        d2F = scipy.misc.derivative(flux_fuc, x, dx=dx, n=2)
        dF = scipy.misc.derivative(flux_fuc, x, dx=dx, n=1)
        kap = d2F/((1 + dF**2)**(3/2))
        return abs(kap)