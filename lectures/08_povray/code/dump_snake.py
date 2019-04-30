#!/usr/bin/env python3
""" Dumps the snake as a sphere sweep given data points and radii """

__author__ = "Tejaswin Parthasarathy"
__license__ = "GPL"

import numpy as np


def dump_snake_to_povray(t_step, t_pos, t_radius=0.01, t_prefix=""):
    """ Dumps the rod for visualization in povray. Assumes that the
    rod is of unit length almost on the XY plane (normal Z) and translates
    starting from the origin to the positive X axes. If not, you can
    suitably transform your data (as a post-processing step) to fit
    given constraints.

    Parameters
    ----------
    t_step : int
        The current time-step. Useful for sequential/ordered numbering
        of rendered files.
    t_pos : np.array
        The nodal positions of the rod at given t_step, as a (3, *) or
        (*,3) shaped array.
    t_radius: float
        The radius of the snake, as a constant (ignoring the small
        dilation effects)
    t_prefix: str
        Prefix for the file name (can also be a path)

    Returns
    -------
    None

    """

    # 0. Define helper function for pythonic text conversion
    def vectorize(arr, rad):
        """ transforms [a, b, c] into string "<a, b, c>"" """
        n = arr.shape[0]
        temp = [None] * n
        for i in range(n):
            temp[i] = (
                "<%s>" % ",".join([str(e)
                                   for e in arr[i]]) + ",{}".format(rad))
        return ",\n".join(temp)

    # 1. Piece together different parts of the string

    # Arrange data conveniently
    povray_arr = t_pos if t_pos.shape[1] == 3 else t_pos.T
    # Data in z always negative to keep with povray conventions
    povray_arr[:, 2] = -np.abs(povray_arr[:, 2])

    # Define the head string
    HEAD_STR = r"""
#include "scenepovray.inc"

sphere_sweep
    {
        b_spline
        %s,
    """ % "{}".format(povray_arr.shape[0])

    # Define the body string after manipulations

    BODY_STR = vectorize(povray_arr, t_radius)

    # Define the tail string
    TAIL_STR = r"""
        texture
        {
        pigment{ color rgbt<0.45,0.39,1,0.0> }
        finish { phong 1 }
        }
        scale<1,1,1>
        rotate<0,0,0>
        translate<0,0,0>
    }
    """

    # 2. Write to file
    file_name = t_prefix + "snake_{:07d}.pov".format(t_step)

    with open(file_name, "w") as text_file:
        print(HEAD_STR + BODY_STR + TAIL_STR, file=text_file)


def test_dump():
    """ Test object for the dump function"""
    x_vals = np.linspace(0., 1., 50)
    y_vals = 0.1 * np.sin(5 * np.pi * x_vals)
    radius = 0.05
    z_vals = 0.0 * x_vals - radius
    prefix = "./data/"
    data_arr = np.vstack((x_vals, y_vals, z_vals))
    dump_snake_to_povray(0, data_arr, radius, prefix)

    y_vals = 0.1 * np.cos(5 * np.pi * x_vals)
    data_arr = np.vstack((x_vals, y_vals, z_vals))
    dump_snake_to_povray(1000, data_arr, radius, prefix)


if __name__ == "__main__":
    test_dump()
