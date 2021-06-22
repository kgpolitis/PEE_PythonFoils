# Define Thickness distributions
import numpy as np

# Constants for 4 digit thickness
A0 = 0.2969       # multiplies sqrt
A1 =-0.126        # multiplies x
A2 =-0.3516       # multiplies x^2
A3 = 0.2843       # multiplies x^3
A4c =-0.1036       # multiplies x^4 (closed trailing edge)
A4o =-0.1015       # multiplies x^4 (open trailing edge)

def NACA4_closed(x):
    if (x==0 or x==1):
        yt=0
    else:
        yt=A0*np.sqrt(x)+A1*x+A2*x**2+A3*x**3+A4c*x**4
    return yt

def NACA4_open(x):
    if (x==0):
        yt=0
    else:
        yt=A0*np.sqrt(x)+A1*x+A2*x**2+A3*x**3+A4o*x**4
    return yt