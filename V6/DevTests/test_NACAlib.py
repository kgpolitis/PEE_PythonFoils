# Use exemple of NACA_LIB
from NACA_LIB import NACA       # Note : If you have python2.7 (check with python -V, then use from NACA_LIB27 instead of NACA_LIB
                                #        switch 
                                #        When used in FreeCAD you have to use the 2.7 version
import matplotlib.pyplot as plt # Note : this import in not required. Displayed as info

# Set a NACA 4 digit foil
foil=NACA(4315)#,TE_closed=True) # default is TE_closed = true

# Display foil parameters
foil.show_parameters()

# Uncomment to plot camber line and thickness
myplot1 = foil.plot_ct()
myplot1.show()

# Uncomment to plot XY coordinates (not necessary to be used with FreeCAD)
myplot2 = foil.plot_XY(show_vecS=True,npoints=20)   # do not hesitate to change plot setting at module FOIL (or FOIL27)
myplot2.show()

