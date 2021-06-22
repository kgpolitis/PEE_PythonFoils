# Use exemple of NACA_LIB
from WAGENINGEN_LIB import WAGENINGEN       # Note : If you have python2.7 (check with python -V, then use from NACA_LIB27 instead of NACA_LIB
                                #        switch 
                                #        When used in FreeCAD you have to use the 2.7 version
import matplotlib.pyplot as plt # Note : this import in not required. Displayed as info

# Set a WAGENINGEN foil - no smoothing at the Leading Edge
#foil=WAGENINGEN(Z=4,EAR=1,rR=0.2,tLE_tmax=0.2)#,TE_closed=True) # default is TE_closed = true

# Set a WAGENINGEN foil - with smoothing
foil=WAGENINGEN(Z=4,EAR=1,rR=0.2,tLE_tmax=0.2,Smooth_LE=1,x0s=0.1,x0p=0.1,ks=0.5,kp=0.5)#,TE_closed=True) # default is TE_closed = true

# Display foil parameters
foil.show_parameters()

# Uncomment to plot camber line and thickness
#myplot1 = foil.plot_cR()
#myplot1.show()

#myplot2 = foil.plot_xtmax()
#myplot2.show()

#myplot3 = foil.plot_tmax()
#myplot3.show()

myplot4 = foil.plot_V2()
myplot4.show()

#With linear spacing 
myplot5 = foil.plot_XY(spacing='linear')
#With cosine spacing 
#myplot5 = foil.plot_XY(spacing='cos')
myplot5.show()

#With linear spacing 
foil.write4Xfoil(npoints=60,spacing='linear')
#With cosine spacing 
#foil.write4Xfoil(npoints=60,spacing='cos')
