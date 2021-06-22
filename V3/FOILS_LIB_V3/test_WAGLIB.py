# Use exemple of NACA_LIB
from WAGENINGEN_LIB import WAGENINGEN       # Note : If you have python2.7 (check with python -V, then use from NACA_LIB27 instead of NACA_LIB
                                #        switch 
                                #        When used in FreeCAD you have to use the 2.7 version
import matplotlib.pyplot as plt # Note : this import in not required. Displayed as info

# Set a NACA 4 digit foil
foil=WAGENINGEN()#,TE_closed=True) # default is TE_closed = true

# Display foil parameters
foil.show_parameters()

# Uncomment to plot camber line and thickness
myplot1 = foil.plot_chord()
myplot1.show()

