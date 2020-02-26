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


#: Aeolis model state variables
INITIAL_STATE = {
    ('ny', 'nx') : (
        'uw',                               # [m/s] Wind velocity
        'uws',                              # [m/s] Component of wind velocity in x-direction
        'uwn',                              # [m/s] Component of wind velocity in y-direction
        'tau',                              # [N/m^2] Wind shear stress
        'taus',                             # [N/m^2] Component of wind shear stress in x-direction
        'taun',                             # [N/m^2] Component of wind shear stress in y-direction
        'dtaus',                            # [-] Component of the wind shear perturbation in x-direction
        'dtaun',                            # [-] Component of the wind shear perturbation in y-direction
        'udir',                             # [rad] Wind direction
        'zs',                               # [m] Water level above reference
        'Hs',                               # [m] Wave height
        'zne',                         #NEW # [m] Non-erodible layer
    ),
}

MODEL_STATE = {
    ('ny', 'nx') : (
        'x',                                # [m] Real-world x-coordinate of grid cell center
        'y',                                # [m] Real-world y-coordinate of grid cell center
        'ds',                               # [m] Real-world grid cell size in x-direction
        'dn',                               # [m] Real-world grid cell size in y-direction
        'dsdn',                             # [m^2] Real-world grid cell surface area
        'dsdni',                            # [m^-2] Inverse of real-world grid cell surface area
        'alfa',                             # [rad] Real-world grid cell orientation (clockwise)
        'zb',                               # [m] Bed level above reference
        'dzb',                        # NEW # [m] Bed level change per time step
        'S',                                # [-] Level of saturation
        'ustar',                      # NEW # [m/s] Shear velocity by wind
        'ustars',                     # NEW # [m/s] Component of shear velocity in x-direction by wind
        'ustarn',                     # NEW # [m/s] Component of shear velocity in y-direction by wind
        'ustar0',                     # NEW # [m/s] Initial shear velocity
        'zsep',                       # NEW # [m] Z level of polynomial that defines the separation bubble
        'hsep',                       # NEW # [m] Height of separation bubbel = difference between z-level of zsep and of the bed level zb
#        'stall',                      # NEW # [ ] 
#        'bubble',                     # NEW # [ ]
        'dzb_year',                   # NEW # Bed level change averaged over collected time steps 
        'rhoveg',                     # NEW # Vegetation cover
        'drhoveg',                    # NEW # Change in vegetation cover
        'hveg',                       # NEW # [m] height of vegetation
        'dhveg',                      # NEW # [m] Difference in vegetation height per time step
        'dzb_veg',                    # NEW # [m] Bed level change used for calculation of vegetation growth
        'germinate',                  # NEW # 
        'lateral',                    # NEW #
        'dxrhoveg',                   # NEW #
        'vegfac',                     # NEW # [] Vegetation factor 
    ),
    ('ny','nx','nfractions') : (
        'Cu',                               # [kg/m^2] Equilibrium sediment concentration integrated over saltation height
        'Cuf',                              # [kg/m^2] Equilibrium sediment concentration integrated over saltation height, assuming the fluid shear velocity threshold
        'Ct',                               # [kg/m^2] Instantaneous sediment concentration integrated over saltation height
        'q',                                # [kg/m/s] Instantaneous sediment flux
        'qs',                               # [kg/m/s] Instantaneous sediment flux in x-direction
        'qn',                               # [kg/m/s] Instantaneous sediment flux in y-direction
        'pickup',                           # [kg/m^2] Sediment entrainment
        'w',                                # [-] Weights of sediment fractions
        'w_init',                           # [-] Initial guess for ``w''
        'w_air',                            # [-] Weights of sediment fractions based on grain size distribution in the air
        'w_bed',                            # [-] Weights of sediment fractions based on grain size distribution in the bed
        'uth',                              # [m/s] Shear velocity threshold
        'uthf',                             # [m/s] Fluid shear velocity threshold
        'uth0',                             # [m/s] Shear velocity threshold based on grainsize only (aerodynamic entrainment)
        'ug',                               # [m/s] Mean horizontal grain velocity in saturated state
        'ugs',                              # [m/s] Component of the grain velocity in x-direction
        'ugn',                              # [m/s] Component of the grain velocity in y-direction
    ),
    ('ny','nx','nlayers') : (
        'thlyr',                            # [m] Bed composition layer thickness
        'moist',                            # [-] Moisure content
        'salt',                             # [-] Salt content
    ),
    ('ny','nx','nlayers','nfractions') : (
        'mass',                             # [kg/m^2] Sediment mass in bed
    ),
    ('ny','nx','nsavetimes') : (
        'dzb_avg',                     # NEW []    

    )
}


#: AeoLiS model default configuration
DEFAULT_CONFIG = {
    'process_wind'                  : True,               # Enable the process of wind
    'process_shear'                 : True,               # Enable the process of wind shear
    'process_tide'                  : True,               # Enable the process of tides
    'process_wave'                  : True,               # Enable the process of waves
    'process_runup'                 : True,               # Enable the process of wave runup
    'process_moist'                 : True,               # Enable the process of moist
    'process_mixtoplayer'           : True,               # Enable the process of mixing
    'process_threshold'             : True,               # Enable the process of threshold
    'process_transport'             : True,               # Enable the process of transport
    'process_bedupdate'             : True,               # Enable the process of bed updating
    'process_meteo'                 : False,              # Enable the process of meteo
    'process_salt'                  : False,              # Enable the process of salt
    'process_humidity'              : False,              # Enable the process of humidity
    'process_avalanche'             : True,         # NEW # Enable the process of avalanching
    'process_inertia'               : False,        # NEW 
    'process_separation'            : False,         # NEW # Enable the including of separation bubble
    'process_vegetation'            : False,        # NEW # Enable the including of vegetation
    'th_grainsize'                  : True,               # Enable wind velocity threshold based on grainsize
    'th_bedslope'                   : False,              # Enable wind velocity threshold based on bedslope
    'th_moisture'                   : True,               # Enable wind velocity threshold based on moisture
    'th_humidity'                   : False,              # Enable wind velocity threshold based on humidity
    'th_salt'                       : False,              # Enable wind velocity threshold based on salt
    'th_roughness'                  : True,               # Enable wind velocity threshold based on roughness
    'th_nelayer'                    : True,         # NEW # Enable wind velocity threshold based on a non-erodible layer
    'xgrid_file'                    : None,               # Filename of ASCII file with x-coordinates of grid cells
    'ygrid_file'                    : None,               # Filename of ASCII file with y-coordinates of grid cells
    'bed_file'                      : None,               # Filename of ASCII file with bed level heights of grid cells
    'wind_file'                     : None,               # Filename of ASCII file with time series of wind velocity and direction
    'tide_file'                     : None,               # Filename of ASCII file with time series of water levels
    'wave_file'                     : None,               # Filename of ASCII file with time series of wave heights
    'meteo_file'                    : None,               # Filename of ASCII file with time series of meteorlogical conditions
    'bedcomp_file'                  : None,               # Filename of ASCII file with initial bed composition
    'threshold_file'                : None,               # Filename of ASCII file with shear velocity threshold
    'ne_file'                       : None,         # NEW # Filename of ASCII file with non-erodible layer
    'veg_file'                      : None,         # NEW # Filename of ASCII file with initial vegetation density
    'wave_mask'                     : None,               # Filename of ASCII file with mask for wave height
    'tide_mask'                     : None,               # Filename of ASCII file with mask for tidal elevation
    'threshold_mask'                : None,               # Filename of ASCII file with mask for the shear velocity threshold
    'nx'                            : 0,                  # [-] Number of grid cells in x-dimension
    'ny'                            : 0,                  # [-] Number of grid cells in y-dimension
    'dt'                            : 60.,                # [s] Time step size
    'CFL'                           : 1.,                 # [-] CFL number to determine time step in explicit scheme
    'accfac'                        : 1.,                 # [-] Numerical acceleration factor
    'tstart'                        : 0.,                 # [s] Start time of simulation
    'tstop'                         : 3600.,              # [s] End time of simulation
    'restart'                       : None,               # [s] Interval for which to write restart files
    'dzb_interval'                  : 604800,       # NEW # [s] Interval used for calcuation of vegetation growth
    'output_times'                  : 60.,                # [s] Output interval in seconds of simulation time
    'output_file'                   : None,               # Filename of netCDF4 output file
    'output_vars'                   : ['zb', 'zs',
                                       'zsep', 'hsep',
                                       'Ct', 'Cu',
                                       'uw', 'udir', 
                                       'uth', 'mass'
                                       'pickup', 'w'],    # Names of spatial grids to be included in output
    'output_types'                  : [],                 # Names of statistical parameters to be included in output (avg, sum, var, min or max)
    'grain_size'                    : [225e-6],           # [m] Average grain size of each sediment fraction
    'grain_dist'                    : [1.],               # [-] Initial distribution of sediment fractions
    'nfractions'                    : 1,                  # [-] Number of sediment fractions
    'nlayers'                       : 3,                  # [-] Number of bed layers
    'layer_thickness'               : .01,                # [m] Thickness of bed layers
    'g'                             : 9.81,               # [m/s^2] Gravitational constant
    'v'                             : 0.000015,             # [m^2/s] Air viscosity  
    'rhoa'                          : 1.225,              # [kg/m^3] Air density
    'rhog'                          : 2650.,              # [kg/m^3] Grain density
    'rhow'                          : 1025.,              # [kg/m^3] Water density
    'porosity'                      : .4,                 # [-] Sediment porosity
    'Aa'                            : .085,               # [-] Constant in formulation for wind velocity threshold based on grain size
    'z'                             : 10.,                # [m] Measurement height of wind velocity
    'h'                             : None,               # [m] Representative height of saltation layer
    'k'                             : 0.001,              # [m] Bed roughness
    'Cb'                            : 1.5,                # [-] Constant in formulation for equilibrium sediment concentration
    'm'                             : 0.5,                # [-] Factor to account for difference between average and maximum shear stress
    'alpha'                         : 0.4,                # [-] Relation of vertical component of ejection velocity and horizontal velocity difference between impact and ejection 
    'kappa'                         : 0.41,               # [-] Von Kármán constant
    'sigma'                         : 4.2,                # [-] Ratio between basal area and frontal area of roughness elements
    'beta'                          : 130.,               # [-] Ratio between drag coefficient of roughness elements and bare surface
    'bi'                            : 1.,                 # [-] Bed interaction factor
    'T'                             : 1,                  # [s] Adaptation time scale in advection equation
    'Tdry'                          : 3600.*1.5,          # [s] Adaptation time scale for soil drying
    'Tsalt'                         : 3600.*24.*30.,      # [s] Adaptation time scale for salinitation
    'eps'                           : 1e-3,               # [m] Minimum water depth to consider a cell "flooded"
    'gamma'                         : .5,                 # [-] Maximum wave height over depth ratio
    'xi'                            : .3,                 # [-] Surf similarity parameter
    'facDOD'                        : .1,                 # [-] Ratio between depth of disturbance and local wave height
    'csalt'                         : 35e-3,              # [-] Maximum salt concentration in bed surface layer
    'cpair'                         : 1.0035e-3,          # [MJ/kg/oC] Specific heat capacity air
    'theta_dyn'                     : 33.,          # NEW # [degrees] Dynamic angle of repose, critical dynamic slope for avalanching 
    'theta_stat'                    : 34.,          # NEW # [degrees] Static angle of repose, critical static slope for avalanching
    'hveg_max'                      : 1.,           # NEW # [m] Max height of vegetation 
    'V_ver'                         : 0.,           # NEW # [1/year]
    'V_lat'                         : 0.,           # NEW # [m/year]
    'germinate'                     : 0.,           # NEW # [1/year] Possibility of germination per year
    'lateral'                       : 0.,           # NEW # -/year
    'veg_gamma'                     : 1.,
    'scheme'                        : 'euler_backward',   # Name of numerical scheme (euler_forward, euler_backward or crank_nicolson)
    'boundary_lateral'              : 'circular',         # Name of lateral boundary conditions (circular, noflux)
    'boundary_offshore'             : 'noflux',           # Name of offshore boundary conditions (gradient, noflux, constant, uniform)
    'boundary_offshore_flux'        : 0.,                 # Constant offshore boundary flux
    'boundary_onshore'              : 'gradient',         # Name of onshore boundary conditions (gradient, noflux, constant, uniform)
    'boundary_onshore_flux'         : 0.,                 # Constant onshore boundary flux
    'method_moist'                  : 'belly_johnson',    # Name of method to compute wind velocity threshold based on soil moisture content
    'method_transport'              : 'bagnold',          # Name of method to compute equilibrium sediment transport rate
    'max_error'                     : 1e-6,               # [-] Maximum error at which to quit iterative solution in implicit numerical schemes
    'max_iter'                      : 1000,               # [-] Maximum number of iterations at which to quit iterative solution in implicit numerical schemes
    'max_iter_ava'                  : 1000,               # [-] Maximum number of iterations at which to quit iterative solution in avalanching calculation
    'refdate'                       : '2020-01-01 00:00', # [-] Reference datetime in netCDF output
    'callback'                      : None,               # Reference to callback function (e.g. example/callback.py':callback)
    'wind_convention'               : 'nautical',        # Convention used for the wind direction in the input files
}


#: Required model configuration parameters
REQUIRED_CONFIG = ['nx', 'ny']

#: Merge initial and model state
MODEL_STATE.update({
    (k, MODEL_STATE[k] + INITIAL_STATE[k])
    for k in set(MODEL_STATE).intersection(INITIAL_STATE)
})
