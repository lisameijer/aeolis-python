'''This file is part of AeoLiS.
   
AeoLiS is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
   
AeoLiS is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
   
You should have received a copy of the GNU General Public License
along with AeoLiS.  If not, see <http://www.gnu.org/licenses/>.
   
AeoLiS  Copyright (C) 2015 Bas Hoonhout

bas.hoonhout@deltares.nl         b.m.hoonhout@tudelft.nl
Deltares                         Delft University of Technology
Unit of Hydraulic Engineering    Faculty of Civil Engineering and Geosciences
Boussinesqweg 1                  Stevinweg 1
2629 HVDelft                     2628CN Delft
The Netherlands                  The Netherlands

'''


from __future__ import absolute_import, division

import numpy as np
import logging
import operator
import matplotlib.pyplot as plt


# package modules
import aeolis.shear
from aeolis.utils import *


# initialize logger
logger = logging.getLogger(__name__)


def initialize(s, p):
    '''Initialize wind model

    '''

    # apply wind direction convention
    if isarray(p['wind_file']):
        if p['wind_convention'] == 'cartesian':
            pass
        elif p['wind_convention'] == 'nautical':
            p['wind_file'][:,2] = 270.0 - p['wind_file'][:,2]
        else:
            logger.log_and_raise('Unknown convention: %s' 
                                 % p['wind_convention'], exc=ValueError)

    # initialize wind shear model
    if p['process_shear']:
        s['shear'] = aeolis.shear.WindShear(s['x'], s['y'], s['zb'],
                                            L=100., l=10., z0=.001, 
                                            buffer_width=10.)                   
        
    return s


def interpolate(s, p, t):
    '''Interpolate wind velocity and direction to current time step

    Interpolates the wind time series for velocity and direction to
    the current time step. The cosine and sine of the direction angle
    are interpolated separately to prevent zero-crossing errors. The
    wind velocity is decomposed in two grid components based on the
    orientation of each individual grid cell. In case of a
    one-dimensional model only a single positive component is used.

    Parameters
    ----------
    s : dict
        Spatial grids
    p : dict
        Model configuration parameters
    t : float
        Current time

    Returns
    -------
    dict
        Spatial grids

    '''
        
    if p['process_wind'] and p['wind_file'] is not None:

        uw_t = p['wind_file'][:,0]
        uw_s = p['wind_file'][:,1]
        uw_d = p['wind_file'][:,2] / 180. * np.pi

        s['uw'][:,:] = interp_circular(t, uw_t, uw_s)
        s['udir'][:,:] = np.arctan2(interp_circular(t, uw_t, np.sin(uw_d)),
                                    interp_circular(t, uw_t, np.cos(uw_d))) * 180. / np.pi

    s['uws'] = s['uw'] * np.cos(s['alfa'] + s['udir'] / 180. * np.pi)           # alfa is real world grid cell orientation
    s['uwn'] = s['uw'] * np.sin(s['alfa'] + s['udir'] / 180. * np.pi)

    if p['ny'] == 0:
        s['uwn'][:,:] = 0.
        
    s['uw'] = np.abs(s['uw'])
    
    # Compute wind shear at height z
    kappa = 0.41
    z = p['z']
    z0 = p['k']                                                                 # dependent on grain size?                                             
    
    s['tau'] = s['uw'] * kappa / np.log(z/z0)
    s['taus'] = s['uws'] * kappa / np.log(z/z0)
    s['taun'] = s['uwn'] * kappa / np.log(z/z0)
    
    # Compute wind velocity (at height z1)
    if p['h'] is not None:
        z1 = p['h']
    
        s['uw'] = s['tau'] / kappa * np.log(z1/z0)
        s['uws'] = s['taus'] / kappa * np.log(z1/z0)
        s['uwn'] = s['taun'] / kappa * np.log(z1/z0)
    
    # Shear stress to shear velocity                                            # waar wordt dit voor gebruikt?
    s['ustar'] = np.sqrt(s['tau'] / p['rhoa'])
    s['ustars'] = s['ustar'] * s['taus'] / s['tau']
    s['ustarn'] = s['ustar'] * s['taun'] / s['tau']
        
    ix = s['tau'] == 0.
    s['ustar'][ix] = 0.
    s['ustars'][ix] = 0.
    s['ustarn'][ix] = 0.
                
    s['ustar0'] = s['ustar']
    s['tau0'] = s['tau']
    s['taus0'] = s['taus'].copy()
    s['taun0'] = s['taun'].copy()
    
    return s

def shear(s,p):
    
    # Compute shear velocity field (including separation)
    if 'shear' in s.keys() and p['process_shear']:
        
        s['shear'].set_topo(s['zb'].copy())
        
        s['shear'](u0=s['uw'][0,0],
                   udir=s['udir'][0,0],
                   process_separation = p['process_separation'])
        
        s['dtaus'], s['dtaun'] = s['shear'].get_shear()
        s['taus'], s['taun'] = s['shear'].add_shear(s['taus'], s['taun'])
        s['tau'] = np.hypot(s['taus'], s['taun'])
        
#        print (s['tau'])
        
#        plt.figure()
#        plt.pcolormesh(s['x'], s['y'], s['ustar'])
#        # plt.pcolormesh(s['x'], s['y'], (np.sqrt(2 * alfa) * uf / Ax[:,:,0]) * dhs[:,:,0])
#        plt.colorbar()
#        plt.show()
                               
        # Returns separation surface     
        if p['process_separation']:
            s['hsep'] = s['shear'].get_separation()
            s['zsep'] = s['hsep'] + s['zb']

    return s


# def filter_low(s, p, par, direction, Cut):                                    # No references to this filter function..?
                                                                                 
#    return s
