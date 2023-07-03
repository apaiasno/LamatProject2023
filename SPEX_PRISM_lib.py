# SPEX-PRISM_lib.py
# Library of functions for reading in the SPEX-PRISM library

# Imports

import numpy as np
import astropy.io.fits as FITS
import pickle

# Functions

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
    spex_dir = 'SPEX-PRISM'

    with open(spex_dir+'/spectral_data.pkl', 'rb') as fp:
        SpT_data_dict = pickle.load(fp)

    filenames = SpT_data_dict[SpT]
    
    wavs, fluxes, errs = [], [], []

    for filename in filenames:
        wav, flux, err, _ = read_spectrum(filename)
        wavs.append(wav)
        fluxes.append(flux)
        errs.append(err)

    return wavs, fluxes, errs

