# SPEX-PRISM_lib.py
# Library of functions for reading in the SPEX-PRISM library

# Imports

import numpy as np
import scipy.interpolate
import astropy.io.fits as FITS
import pickle

### FUNCTIONS ###

## Data manipulation routines ##
def interpolate_xy(x, y, x_new, fill_value='extrapolate'):
    ''' Interpolate y values to new grid of x values.

        Parameters
        ----------
        x : 1-D numpy array 
            Current x values
        y : 1-D numpy array 
            Current y values
        x_new : 1-D numpy array 
            New x values to interpolate onto

        Returns
        -------
        y_new : 1-D numpy array 
            Interpolated y values
    '''
    quadinterp = scipy.interpolate.interp1d(x, y, kind='slinear', bounds_error=False, fill_value=fill_value)
    return quadinterp(x_new)


## SPEX-PRISM library routines

def read_spectrum(filename):
    ''' Reads a spectrum from the SpeX Prism library.

        Parameters
        ----------
        filename: string
            Filename of spectrum to be read

        Returns
        -------
        wav: 1D numpy array
            Array of spectral wavelengths
        flux: 1D numpy array
            Array of spectral fluxes
        err: 1D numpy array
            Array of spectral errors
    '''
    spex_dir = 'SPEX-PRISM'
    hdul = FITS.open(spex_dir+'/'+filename)
    shape_data = np.shape(hdul[0].data)
    if len(shape_data) == 3:
        wav, flux, err = hdul[0].data[0][0], hdul[0].data[0][1], hdul[0].data[0][2]
    else:
        wav, flux, err = hdul[0].data[0], hdul[0].data[1], hdul[0].data[2]
    
    with open(spex_dir+'/spectral_data.pkl', 'rb') as fp:
        SpT_data_dict = pickle.load(fp)
    for key in SpT_data_dict.keys():
        if filename in SpT_data_dict[key]:
            SpT = key
            break
    return wav, flux, err, SpT

def list_all_available_SpT():
    ''' Prints all spectral types available in the SpeX Prism library.

        Parameters
        ----------
        None

        Returns
        -------
        SpTs: list
            List of strings corresponding to all available spectral types in library
    '''
    spex_dir = 'SPEX-PRISM'
    with open(spex_dir+'/spectral_data.pkl', 'rb') as fp:
        SpT_data_dict = pickle.load(fp)

    return list(SpT_data_dict.keys())

def list_SpT_filenames(SpT):
    ''' Prints all the filenames of a given spectral type available in the SpeX Prism library.

        Parameters
        ----------
        SpT: string
            String corresponding to spectral type of interest

        Returns
        -------
        filwnames: list
            List of strings corresponding to all filenames of the input spectral type
    '''
    spex_dir = 'SPEX-PRISM'

    with open(spex_dir+'/spectral_data.pkl', 'rb') as fp:
        SpT_data_dict = pickle.load(fp)

    filenames = SpT_data_dict[SpT]
    return filenames

def get_all_SpT(SpT):
    ''' Returns all spectra corresponding to the input spectral type.

        Parameters
        ----------
        SpT: string
            String corresponding to the spectral type of interest

        Returns
        -------
        wavs: 2D numpy array
            Array of wavelengths for all spectra in library corresponding to input spectral type
        fluxes: 2D numpy array
            Array of spectral fluxes for all spectra in library corresponding to input spectral type
        errs: 2D numpy array
            Array of spectral errors for all spectra in library corresponding to input spectral type
    '''
    filenames = list_SpT_filenames(SpT)
    wavs, fluxes, errs = [], [], []

    for filename in filenames:
        wav, flux, err, _ = read_spectrum(filename)
        wavs.append(wav)
        fluxes.append(flux)
        errs.append(err)

    return wavs, fluxes, errs

