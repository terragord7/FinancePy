##############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane
##############################################################################

import numpy as np
from math import exp

from ...finutils.FinGlobalVariables import gSmall
from ...finutils.FinFrequency import FinFrequency, FinFrequencyTypes
from ...finutils.FinHelperFunctions import inputTime
from ...finutils.FinHelperFunctions import labelToString
from ...finutils.FinError import FinError
from ...market.curves.FinDiscountCurve import FinDiscountCurve

###############################################################################


class FinDiscountCurveNSS(FinDiscountCurve):
    ''' Implementation of Nelson-Siegel-Svensson parametrisation of the
    zero rate curve '''

    def __init__(self, beta1, beta2, beta3, beta4, tau1, tau2):

        if tau1 <= 0:
            raise FinError("Tau1 must be positive")

        if tau2 <= 0:
            raise FinError("Tau2 must be positive")

        self._beta1 = beta1
        self._beta2 = beta2
        self._beta3 = beta3
        self._beta4 = beta4
        self._tau1 = tau1
        self._tau2 = tau2

###############################################################################

    def zero(self, t):
        ''' Calculation of zero rates. This function can return a vector
        of zero rates given a vector of times. '''

        if np.any(t < 0.0):
            raise FinError("All times must be positive")

        t = t + gSmall  # To avoid overflows when t=0.0
        theta1 = t / self._tau1
        theta2 = t / self._tau2
        expTerm1 = np.exp(-theta1)
        expTerm2 = np.exp(-theta2)
        zeroRate = self._beta1
        zeroRate += self._beta2 * (1.0 - expTerm1) / theta1
        zeroRate += self._beta3 * ((1.0 - expTerm1) / theta1 - expTerm1)
        zeroRate += self._beta4 * ((1.0 - expTerm2) / theta2 - expTerm2)
        return zeroRate

###############################################################################

    def fwd(self, t):
        ''' Calculation of forward rates. This function uses Numpy so returns
        a vector of forward rates given a Numpy array vector of times. '''

        theta1 = t / self._tau1
        theta2 = t / self._tau2
        expTerm1 = np.exp(-theta1)
        expTerm2 = np.exp(-theta2)
        fwdRate = self._beta1
        fwdRate += self._beta2 * expTerm1
        fwdRate += self._beta3 * theta1 * expTerm1
        fwdRate += self._beta4 * theta2 * expTerm2
        return fwdRate

###############################################################################

    def df(self, t):
        ''' Discount factor for Nelson-Siegel-Svensson curve
        parametrisation. '''
        r = self.zero(t)
        return exp(-r * t)

###############################################################################
