__doc__ = """Python script for finding the optimal of a simple function"""

import numpy as np
from scipy.optimize import minimize

WEIGHTS = np.array([4, -2, 7, 5, 11, 1])


def cost_fun(arg_x):
    """ Cost function to minimize"""
    cost = np.inner(WEIGHTS, arg_x)
    return -cost


init_guess = np.zeros((6, ))
bnds = [(-4, 4) for x in range(6)]
bnds = tuple(bnds)
res = minimize(cost_fun, init_guess, method='SLSQP', bounds=bnds)
print(res.x)
