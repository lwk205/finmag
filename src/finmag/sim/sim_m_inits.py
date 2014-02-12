import finmag
from finmag.util import helpers

import logging
import math
import numpy as np

log = logging.getLogger("finmag")

def initialise_skyrmion_centre_2D(sim, skyrmionRadius):
    """
    Initialise the magnetisation to a pattern resembling a skyrmion in the
    centre of the mesh which should be relaxed to obtain the most natural
    skyrmion possible.

    *Assumptions*: It is assumed that the mesh is a 2D mesh. If it is not, the
                   skyrmion will be projected in higher dimensions.

    *Arguments*:

    skyrmionRadius
        The radius of the skyrmion in mesh co-ordinates

    This function returns nothing.
    """

    # Build the function
    def m_skyrmion(pos):
        """This function returns a vector corresponding to a skyrmion at the
        origin."""

        # Convert position vector into cylindrical form; "r" being the distance
        # of the point from the origin and "t" being the argument.
        r = pow(pow(pos[0], 2) + pow(pos[1], 2), 0.5)

        if abs(pos[0]) < 1e-6:
            if abs(pos[1]) < 1e-6:
                t = 0
            elif pos[1] > 0:
                t = np.pi / 2.
            else:
                t = -np.pi / 2.
        else:
            t = np.arctan2(pos[1], pos[0])

        # Define vector components outside of the skyrmion:
        if r >= skyrmionRadius:
            mz = 1
            mt = 0

        # Define vector components inside the skyrmion:
        else:
            mz = -np.cos(np.pi * r / skyrmionRadius)
            mt = np.sin(np.pi * r / skyrmionRadius)

        # Convert to cartesian form and normalize.
        mx = -np.sin(t) * mt
        my = np.cos(t) * mt
        out = np.array([mx, my, mz], dtype="float64")
        return out / np.linalg.norm(out)

    # Use the above function to initialise the magnetisation.
    sim.set_m(m_skyrmion)


def initialise_skyrmion_hexlattice_2D(sim, meshX, meshY, tileScaleX=1,
                                      skyrmionRadiusScale=0.2):
    """
    Initialise the magnetisation to a pattern resembling a hexagonal
    lattice of 2D skyrmions which should be relaxed to obtain the most
    natural lattice possible. The most stable of lattices will exist on
    meshes whose horizontal dimension is equal to the vertical tile
    dimension / sqrt(3); if the mesh does not (approximately) conform to
    these dimensions, a warning will be raised (because this will result in
    elliptical skyrmions being created).

    *Assumptions*: It is assumed that the mesh is a rectangular 2D mesh. If
                   it is not, the 2D hexagonal lattice will be projected in
                   higher dimensions.

    *Arguments*:

    meshX
        The length of the rectangular mesh in the first dimension (the 'X'
        direction).

    meshY
        As above, but for the second dimension (the 'Y' direction).

    tileScaleX=1
        The fraction of the size of the tile in the first dimension (the
        'X' direction) to the size of the mesh. For example, if this
        quantity is equal to 0.5, there will be two tiles in the first
        dimension.

    skyrmionRadiusScale=0.3
        The radius of the skyrmion defined as a fraction of the tile in the
        first dimension ('X' direction).

    This function returns nothing.
    """

    # Ensure the mesh is of the dimensions stated above, and raise a
    # warning if it isn't.
    if abs(meshX / float(meshY) - np.sqrt(3)) > 0.05 and \
       abs(meshY / float(meshX) - np.sqrt(3)) > 0.05:
        log.warning("Mesh dimensions do not accurately support hexagonal" +
                    " lattice formation! (One should be a factor of sqrt" +
                    "(3) greater than the other.)")

    # Calculate lengths of tiles and the skyrmion radius in mesh
    # co-ordinates.
    tileLengthX = meshX * tileScaleX
    tileLengthY = meshY * tileScaleX
    skyrmionRadius = tileLengthX * skyrmionRadiusScale

    # Build the function.
    def m_skyrmion_hexlattice(pos):
        """
        Function that takes a position vector of a point in a vector field
        and returns a vector such that the vector field forms a hexagonal
        lattice of skyrmions of the field is toroidal. This only works for
        rectangular meshes whos horizontal tile dimension is equal to the
        vertical tile dimension / sqrt(3)."""

        # Convert position into tiled co-ordinates.
        cx = pos[0] % tileLengthX - tileLengthX / 2.
        cy = pos[1] % tileLengthY - tileLengthY / 2.

        # ==== Define first skyrmion quart ====#
        # Define temporary cartesian co-ordinates (tcx, tcy) that can be
        # used to define a polar co-ordinate system.
        tcx = cx - tileLengthX / 2.
        tcy = cy

        r = pow(pow(tcx, 2) + pow(tcy, 2), 0.5)
        t = np.arctan2(tcy, tcx)

        tcx_flip = cx + tileLengthX / 2.
        r_flip = pow(pow(tcx_flip, 2) + pow(tcy, 2), 0.5)
        t_flip = np.arctan2(tcy, tcx_flip)

        # Populate vector field:
        mz = -1 + 2 * r / skyrmionRadius
        mz_flip = -1 + 2 * r_flip / skyrmionRadius

        # Replicate to other half-plane of the vector field and convert to
        # cartesian form.
        if(mz <= 1):
            mt = np.sin(np.pi * r / skyrmionRadius)
            mx_1 = -np.sin(t) * mt
            my_1 = np.cos(t) * mt
            mz_1 = mz

        elif(mz_flip < 1):
            mt = -np.sin(np.pi * r_flip / skyrmionRadius)
            mz_1 = mz_flip
            mx_1 = np.sin(t_flip) * mt
            my_1 = -np.cos(t_flip) * mt

        elif(mz > 1):
            mx_1 = 0
            my_1 = 0
            mz_1 = 1

        # ==== Define second skyrmion quart ====#
        # Define temporary cartesian co-ordinates (tcx, tcy) that can be
        # used to define polar co-ordinate system.
        tcx = cx
        tcy = cy - tileLengthY / 2.

        r = pow(pow(tcx, 2) + pow(tcy, 2), 0.5)
        t = np.arctan2(tcy, tcx)

        tcy_flip = cy + tileLengthY / 2.
        r_flip = pow(pow(tcx, 2) + pow(tcy_flip, 2), 0.5)
        t_flip = np.arctan2(tcy_flip, tcx)

        # Populate vector field:
        mz = -1 + 2 * r / skyrmionRadius
        mz_flip = -1 + 2 * r_flip / skyrmionRadius

        # Replicate to other half-plane of the vector field and convert to
        # cartesian form.
        if(mz <= 1):
            mt = np.sin(np.pi * r / skyrmionRadius)
            mx_2 = -np.sin(t) * mt
            my_2 = np.cos(t) * mt
            mz_2 = mz

        elif(mz_flip < 1):
            mt = -np.sin(np.pi * r_flip / skyrmionRadius)
            mz_2 = mz_flip
            mx_2 = np.sin(t_flip) * mt
            my_2 = -np.cos(t_flip) * mt

        elif(mz > 1):
            mx_2 = 0
            my_2 = 0
            mz_2 = 1

        #==== Combine and normalize. ====#
        mx = mx_1 + mx_2
        my = my_1 + my_2
        mz = mz_1 + mz_2 - 1

        out = np.array([mx, my, mz], dtype="float64")

        return out / np.linalg.norm(out)

    # Use the above function to initialise the magnetisation.
    sim.set_m(m_skyrmion_hexlattice)


def initialise_vortex(sim, type, center=None, **kwargs):
    """
    Initialise the magnetisation to a pattern that resembles a vortex state.
    This can be used as an initial guess for the magnetisation, which should
    then be relaxed to actually obtain the true vortex pattern (in case it is
    energetically stable).

    If `center` is None, the vortex core centre is placed at the sample centre
    (which is the point where each coordinate lies exactly in the middle between
    the minimum and maximum coordinate for each component). The vortex lies in
    the x/y-plane (i.e. the magnetisation is constant in z-direction). The
    magnetisation pattern is such that m_z=1 in the vortex core centre, and it
    falls off in a radially symmetric way.

    The exact vortex profile depends on the argument `type`. Currently the
    following types are supported:

       'simple':

           m_z falls off in a radially symmetric way until m_z=0 at
           distance `r` from the centre.

       'feldtkeller':

           m_z follows the profile m_z = exp(-2*r^2/beta^2), where `beta`
           is a user-specified parameter.

    All provided keyword arguments are passed on to the helper functions which
    implement the vortex profiles (e.g., finmag.util.helpers.vortex_simple or
    finmag.util.helpers.vortex_feldtkeller). See their documentation for details
    and other allowed arguments.

    """
    coords = np.array(sim.mesh.coordinates())
    if center == None:
        center = 0.5 * (coords.min(axis=0) + coords.max(axis=0))

    vortex_funcs = {
        'simple': helpers.vortex_simple,
        'feldtkeller': helpers.vortex_feldtkeller,
        }

    kwargs['center'] = center

    try:
        fun_m_init = vortex_funcs[type](**kwargs)
        log.debug("Initialising vortex of type '{}' with arguments: {}".format(type, kwargs))
    except KeyError:
        raise ValueError("Vortex type must be one of {}. Got: {}".format(vortex_funcs.keys(), type))

    sim.set_m(fun_m_init)
