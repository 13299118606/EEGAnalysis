"""
phase analysis

author: Yizhan Miao
email: yzmiao@protonmail.com
last update: Oct 1 2018
"""

import numpy as np


def dwt_itpc(dwtresult, itpcz=False, weights=None):
    """Calculate the inter-trial phase clustering from the dwt result

    Syntax: ITPC = dwt_itpc(dwtresult, zscore, weights)

    Keyword arguments:
    dwtresult -- (numpy.ndarray, dtype="complex") 3D complex array from dwt function
    itpcz     -- (bool) flag for ITPCz analysis [default: False]
    weights   -- (numpy.ndarray) weights for wITPCz analysis [default: None] #TODO

    Return:
    ITPC -- (numpy.ndarray) iter-trial pahse clustering result
    """
    unit = dwtresult / np.abs(dwtresult)
    ITPC = np.abs(np.sum(unit, 1) / np.size(dwtresult, 1))
    
    if itpcz == True:
        result = ITPC**2 * np.size(dwtresult, 1)
    else:
        result = ITPC
    
    return result
