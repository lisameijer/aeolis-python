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

import logging
import numpy as np
import matplotlib.pyplot as plt

# package modules
from aeolis.utils import *


# initialize logger
logger = logging.getLogger(__name__)

def grainspeed(s, p):
    '''Compute grain speed according to Duran 2007 (p. 42)

    Parameters
    ----------
    s : dict
        Spatial grids
    p : dict
        Model configuration parameters

    Returns
    -------
    dict
        Spatial grids
        '''
    
    # Create each grain fraction
    
    nf = p['nfractions']
    d = p['grain_size']
    
    z = s['zb'].copy()
    x = s['x']
    y = s['y']
    
    uth = s['uth']  
    uth0 = s['uth0']    
    ustar = s['ustar']
    ustars = s['ustars']
    ustarn = s['ustarn']
    
    rhog = p['rhog']
    rhoa = p['rhoa']
    s = rhog/rhoa
    
    A = 0.95
    B = 5.12        
    
    g = np.repeat(p['g'], nf, axis = 0)
    v = np.repeat(p['v'], nf, axis = 0)
    
    kappa = p['kappa']
        
    # Drag coefficient (Duran, 2007 -> Jimenez and Madsen, 2003)
    
    r       = 1. # Duran 2007, p. 33
    c       = 14./(1.+1.4*r)
    
    tv      = (v/g**2)**(1/3) # +- 5.38 ms                                      # Andreotti, 2004
    
    lv      = (v**2/(p['Aa']**2*g*(s-1)))**(1/3)

    zm      = c * uth * tv  # characteristic height of the saltation layer +- 20 mm
    z0      = d/20.  # grain based roughness layer +- 10 mu m - Duran 2007 p.32
    z1      = 35. * lv # reference height +- 35 mm
  
    alpha   = 0.17 * d / lv
#    s['alpha'] = alpha

    Sstar   = d/(4*v)*np.sqrt(g*d*(s-1.))
    Cd      = (4/3)*(A+np.sqrt(2*alpha)*B/Sstar)**2
    
    uf = np.sqrt(4/(3*Cd)*(s-1.)*g*d)                                            # Grain settling velocity - Jimnez and Madsen, 2003
   
    # Initiate arrays
    
    ets = np.zeros(uth.shape)
    etn = np.zeros(uth.shape)

    ueff = np.zeros(uth.shape)
    ueff0 = np.zeros(uth.shape)
    
    ustar = np.repeat(ustar[:,:,np.newaxis], nf, axis=2)
    ustars = np.repeat(ustars[:,:,np.newaxis], nf, axis=2)
    ustarn = np.repeat(ustarn[:,:,np.newaxis], nf, axis=2)
    
    # Efficient wind velocity (Duran, 2006 - Partelli, 2013)
    ueff = (uth0 / kappa) * (np.log(z1 / z0))
    ueff0 = (uth0 / kappa) * (np.log(z1 / z0)) 

    for i in range(nf):  
        # determine ueff for different grainsizes
        
        ix = (ustar[:,:,i] >= uth[:,:,i])*(ustar[:,:,i] > 0.)
        ueff[ix,i] = (uth[ix,i] / kappa) * (np.log(z1[i] / z0[i]) + 2*(np.sqrt(1+z1[i]/zm[ix,i]*(ustar[ix,i]**2/uth[ix,i]**2-1))-1))
        
        # PLOT effective wind velocity per grain fraction ---------------
        # plt.pcolormesh(x, y, ueff[:, :, i])  
        # plt.xlabel('x [m]')
        # plt.ylabel('y [m]')
        # plt.title('Effective wind velocity [m/s]')
        # plt.colorbar()
        # plt.show()
        # ---------------------------------------------------------------
    
    # Wind direction
    
    ix = (ustar >= uth)*(ustar > 0.)
    
    ets[:] = 1.
    etn[:] = 0.

    ets[ix] = ustars[ix] / ustar[ix]
    etn[ix] = ustarn[ix] / ustar[ix]
    
    # Surface gradient
    dzs = np.zeros(z.shape)
    dzn = np.zeros(z.shape)
    
    dzs[:,1:-1] = (z[:,2:]-z[:,:-2])/(x[:,2:]-x[:,:-2])
    dzn[1:-1,:] = (z[:-2,:]-z[2:,:])/(y[:-2,:]-y[2:,:])
    
    # Boundaries
    
    dzs[:,0] = dzs[:,1]
    dzn[0,:] = dzn[1,:]    
    dzs[:,-1] = dzs[:,-2]
    dzn[-1,:] = dzn[-2,:]
    
    dhs = np.repeat(dzs[:,:,np.newaxis], nf, axis = 2)
    dhn = np.repeat(dzn[:,:,np.newaxis], nf, axis = 2)
    
    Axs = ets + 2*alpha*dhs
    Axn = etn + 2*alpha*dhn
    Ax = np.hypot(Axs, Axn)

    # Compute grain speed
    # print ('alpha:', type(alpha), alpha.shape)
    # print ('ueff:', type(ueff), ueff.shape)
    # print ('uf:', type(uf), uf.shape)
    # print ('Ax:', type(Ax), Ax.shape)
    # print ('ets:', type(ets), ets.shape)
    # print ('dhs:', type(dhs), dhs.shape)
    
    ug0 = np.zeros(uth.shape)
    ugs = np.zeros(uth.shape)
    ugn = np.zeros(uth.shape)
    ug = np.zeros(uth.shape)

    for i in range(nf):  
        # loop over fractions
        ug0[:,:,i] = (ueff0[:,:,i] - uf[i] / (np.sqrt(2 * alpha[i])))
        ugs[:,:,i] = (ueff[:,:,i] - uf[i] / (np.sqrt(2. * alpha[i]) * Ax[:,:,i])) * ets[:,:,i] - (np.sqrt(2*alpha[i]) * uf[i] / Ax[:,:,i]) * dhs[:,:,i] 
        ugn[:,:,i] = (ueff[:,:,i] - uf[i] / (np.sqrt(2. * alpha[i]) * Ax[:,:,i])) * etn[:,:,i] - (np.sqrt(2*alpha[i]) * uf[i] / Ax[:,:,i]) * dhn[:,:,i]
        
        ug[:,:,i] = np.hypot(ugs[:,:,i], ugn[:,:,i])
        
        # set the grain velocity to zero inside the separation bubble
        
        ix = (ustar[:,:,i] == 0.)
        
        ug0[ix,i] = 0.
        ugs[ix,i] = 0.
        ugn[ix,i] = 0.
        ug[ix,i] = 0.
        
        # plt.pcolormesh(x, y, ug[:, :, i])
        # bar = plt.colorbar()
        # bar.set_label('ug [m/s]')
        # plt.xlabel('x [m]')
        # plt.ylabel('y [m]')
        # plt.title('Horizontal grain velocity (incl. sep bubble)')
        # plt.show()

        
    return ug0, ugs, ugn, ug


def equilibrium(s, p):
    '''Compute equilibrium sediment concentration following Bagnold (1937)

    Parameters
    ----------
    s : dict
        Spatial grids
    p : dict
        Model configuration parameters

    Returns
    -------
    dict
        Spatial grids

    '''

    if p['process_transport']:
        
        ug0, ugs, ugn, ug = grainspeed(s,p)
        
        s['ug0'] = ug0
        s['ugs'] = ugs
        s['ugn'] = ugn    
        s['ug']  = ug
        
        nf     = p['nfractions']
        alpha  = p['alpha']
        ustar  = s['ustar'][:,:,np.newaxis].repeat(nf, axis=2)
        ustar0 = s['ustar0'][:,:,np.newaxis].repeat(nf, axis=2)
        uth    = s['uth']
        uthf   = s['uthf']
        uth0   = s['uth0']
        
        ix = (ustar != 0.)*(ug != 0.)
        
        s['Cu']  = np.zeros(ug.shape)
        s['Cuf'] = np.zeros(ug.shape)      

        s['Cu'][ix] = _equilibrium(ustar[ix], uth[ix], ug[ix],
                                   Cb=p['Cb'], alpha=p['alpha'], rhoa=p['rhoa'], g=p['g'], method=p['method_transport'])
        s['Cuf'][ix] = _equilibrium(ustar[ix], uthf[ix], ug[ix],
                                    Cb=p['Cb'], alpha=p['alpha'], rhoa=p['rhoa'], g=p['g'], method=p['method_transport'])
#        if p['method_transport'].lower() == 'bagnold' or 'cdm':
#            s['Cu0'] = np.zeros(ug.shape)
            
#            s['Cu0'] = _equilibrium(ustar0, uth0, ug0,
#                                   Cb=p['Cb'], alpha=p['alpha'], rhoa=p['rhoa'], g=p['g'], method=p['method_transport'])

    s['Cu']  *= p['accfac']
    s['Cuf'] *= p['accfac']
    
    return s


def _equilibrium(ustar, uth, ug, Cb, alpha, rhoa, g, method):
    if method.lower() == 'bagnold':
        Cu = np.maximum(0., Cb * rhoa / g * (ustar - uth)**3 / ug)
    elif method.lower() == 'kawamura':
        Cu = np.maximum(0., Cb * rhoa / g * (ustar + uth)**2 * (ustar - uth) / ug)
    elif method.lower() == 'lettau':
        Cu = np.maximum(0., Cb * rhoa / g * (ustar - uth) * ustar**2 / ug)
    elif method.lower() == 'cdm':
        Cu = np.maximum(0.,  2 * alpha * rhoa / g * (ustar**2 - uth**2))    
    else:
        logger.log_and_raise('Unknown transport formulation [%s]' % method, exc=ValueError)

    return Cu


def compute_weights(s, p):
    '''Compute weights for sediment fractions

    Multi-fraction sediment transport needs to weigh the transport of
    each sediment fraction to prevent the sediment transport to
    increase with an increasing number of sediment fractions. The
    weighing is not uniform over all sediment fractions, but depends
    on the sediment availibility in the air and the bed and the bed
    interaction parameter ``bi``.

    Parameters
    ----------
    s : dict
        Spatial grids
    p : dict
        Model configuration parameters

    Returns
    -------
    numpy.ndarray
        Array with weights for each sediment fraction

    '''

    w_air = normalize(s['Ct'], s['Cu'])
    w_bed = normalize(s['mass'][:,:,0,:], axis=2)

    w = (1. - p['bi']) * w_air \
        + (1. - np.minimum(1., (1. - p['bi']) * np.sum(w_air, axis=2, keepdims=True))) * w_bed
    w = normalize(w, axis=2)
    
    return w, w_air, w_bed


def renormalize_weights(w, ix):
    '''Renormalizes weights for sediment fractions

    Renormalizes weights for sediment fractions such that the sum of
    all weights is unity. To ensure that the erosion of specific
    fractions does not exceed the sediment availibility in the bed,
    the normalization only modifies the weights with index equal or
    larger than ``ix``.

    Parameters
    ----------
    w : numpy.ndarray
        Array with weights for each sediment fraction
    ix : int
        Minimum index to be modified

    Returns
    -------
    numpy.ndarray
        Array with weights for each sediment fraction

    '''
    
    f = np.sum(w[:,:,:ix], axis=2, keepdims=True)
    w[:,:,ix:] = normalize(w[:,:,ix:], axis=2) * (1. - f)

    # normalize in case of supply-limitation
    # use uniform distribution in case of no supply
    w = normalize(w, axis=2, fill=1./w.shape[2])

    return w
