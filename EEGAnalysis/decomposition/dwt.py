"""
decomposition analysis with wavelet transform.

author: Yizhan Miao
email: yzmiao@protonmail.com
last update: Oct 3 2018
"""

import numpy as np

## wavelet
def morlet(F, fs):
    """Morlet wavelet"""
    wtime = np.linspace(-1, 1, 2*fs)
    s = 6 / (2 * np.pi * F)
    wavelet = np.exp(2*1j*np.pi*wtime*F) * np.exp(-wtime**2/(2*s**2))
    return wavelet


## wavelet tranform
def dwt(data, fs, frange, wavelet=morlet, reflection=False):
    """wavelet tranform decomposition.

    Syntax: Dwt = dwt(data, fs, frange, wavelet, reflection)

    Keyword arguments:
    data       -- (numpy.ndarray) 1D or 2D array. for 2D array, columns as
                  observations, rows as raw data.
    fs         -- (int) sampling rate
    frange     -- (numpy.ndarray) target frequencies
    wavelet    -- (function) wavelet function [default: morlet]
    reflection -- (bool) perform data reflection, to compensate the edge effect
                  [default: False]

    Return:
    Dwt        -- (numpy.ndarray, dtype="complex") wavelet decomposition result

    """

    if np.ndim(data) == 1:
        data = np.reshape(data, (1, len(data)))

    if reflection:
        data_flip = np.fliplr(data)
        data_fft = np.hstack((data_flip, data, data_flip))
    else:
        data_fft = data

    nConv = np.size(data_fft, -1) + int(2*fs)
    fft_data = np.fft.fft(data_fft, nConv)

    Dwt = np.zeros((np.size(frange), np.size(data, 0), np.size(data, 1)), dtype="complex")

    for idx, F in enumerate(frange):
        fft_wavelet = np.fft.fft(wavelet(F, fs), nConv)
        conv_wave = np.fft.ifft(fft_wavelet * fft_data, nConv)
        conv_wave = conv_wave[:, fs:-fs]

        if reflection:
            Dwt[idx, :, :] = conv_wave[:, np.size(data, 1):-np.size(data, 1)]
        else:
            Dwt[idx, :, :] = conv_wave

    return Dwt
