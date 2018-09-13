ROLL = 'ROLL' # deg 0.01 99999
PITCH = 'PIT' # deg 0.01 99999
YAW = 'YAW' # deg 0.01 99999
ANGLEOFATTACK = 'AOA'
MACHNUMBER = 'MACH'
EW_HORZ_WINDSPEED = 'U'
NS_HORZ_WINDSPEED = 'V'
VERT_WINDSPEED = 'W'
NS_HORZ_GROUNDSPEED = 'Ydot'
EW_HORZ_GROUNDSPEED = 'Xdot'
VERT_SPEED = 'Zdot'
VERTICALACCEL = 'Zdotdot'

COLS_FOR_SIM = [MACHNUMBER, ROLL, PITCH, YAW]

# Static Pressure (Psta) mb 0.1 99999
# Static Temperature * (Tsta) K 0.01 99999
# True Air Speed * (TAS) m/s 0.01 99999
# E-W Horizontal Wind Speed * (U) m/s 0.01 999999
# N-S Horizontal Wind Speed * (V) m/s 0.01 999999
# Vertical Wind Speed *@ (W) m/s 0.001 999999
# LOG10 Turbulent Dissipation Rate (TEDR) Kw/Kg 0.01 99999
# LOG10 Reynolds Number per Length (REYN) /m 0.01 9999
# Latitude +N (LAT) deg 0.001 999999
# Longitude +E (LONG) deg 0.001 9999999
# Pressure Altitude (PALT) m 0.1 999999
# Potential Temperature * (POT) K 0.01 99999
# Roll Angle +right wing down (ROLL) deg 0.01 99999
# Heading Angle (HDG) deg 0.01 99999
# Pitch Angle (PITCH) deg 0.01 99999
# N-S Ground Speed +N (Ydot) m/s 0.01 999999
# E-W Ground Speed +E (Xdot) m/s 0.01 999999
# Vertical Speed +U @ (Zdot) m/s 0.001 999999
# Q (Compressible Dynamic Pressure) (q) mb 0.01 999999
# Yaw Angle (sideslip angle) (YAW) deg 0.01 99999
# Angle of Attack (AOA) deg 0.01 99999
# Mach Number (MACH) 0.0001 999999
# Vertical Acceleration +U (Zdotdot) m/ss 0.001 999999
# Yaw delta P (Ydp) mb 0.001 999999
# AOA delta P (Adp) mb 0.001 999999
