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
#myplot1 = foil.plot_ct()
#myplot1.show()

# Uncomment to plot XY coordinates (not necessary to be used with FreeCAD)
myplot2 = foil.plot_XY(show_vecS=True,npoints=20)   # do not hesitate to change plot setting at module FOIL (or FOIL27)
myplot2.show()

# Obtain coordinates for pressure side (here you can also set npoints are an optional argument)
xpres,ypres=foil.PressureSide_FCAD()

# Exemple with optional : xpres,ypres=foil.PressureSide_FCAD(npoints=100)

# Obtain coordinates for suction side (here you can also set npoints are an optional argument)
xsuc,ysuc=foil.SuctionSide_FCAD()

# Obtain tangent vector for LE (returns one vector to be used for both pressure and suction side) 
vecLE=foil.vecS_LE()

# Obtain tangent vectors for TE (returns two vectors, one for pressure and one for suction side) 
vecTE=foil.vecS_TE()


# NOTE : Trads
# LE = Leading  Edge = Bord d'attaque
# TE = Trealing Edge = Bord de fuite
# Pressure side      = Intrados
# Suction  side      = Extrados
# Camber line        = (Ligne de) cambrure
# Thickness          = Eppaiseur 
# Chord              = Corde
# 
# Les quatre chiffres MPTT de NACA Serie 4 indiquent les suivants :
#      M  : Cambrure max en % de la corde                  , e.g. si  M=4 , donc cambrure  max       : m       = 0.04 c  
#      P  : Placement de la cambrure max en 10% de la corde, e.g. si  P=2 , donc cambrure  max est a : p = x/c = 0.2  
#      TT : Eppaiseur max en % de la corde                 , e.g. si TT=15, donc eppaiseur max       : t       = 0.15 c (toujours a x/c=0.3)
# 
########################
#  USAGE WITH FREECAD  #
########################
# 
# 
# 1. Open FreeCAD, the Python Console of FreeCAD and set path
#    a. To open the console : Affichage > Vues > Console Python
#    b. Type : import sys
#              for path in sys.path:
#                  print(path)
#       N'oubliez pas les quatres espaces avant print (et les deux points après sys.path)  
#    c. Choisir n'importe quel répertoire vous souhaitez et copier-coller dedans les fichiers NACA_LIB27.py, FOIL27.py
#    d. Redemarer le logiciel 
# 
# 2. Import modules: 
# 
#    from FreeCAD  import Base
#    import Part
#    from NACA_LIB27 import NACA
#    
#    Create a document :
#    
#              MyFoil=App.newDocument("MyFoil")
#    
# 3. Use as explained above (copier-coller les commandes) to obtain : (see also command listing)
#           a. x,y coordinates of the pressure and suction side of the foil
#           b. tangents at the trailing edge and leading edge
#      de votre MPTT Series 4 NACA foil préféré
# 
# 4. Generate base vectors of FreeCAD 
#       a. for points    
#        >of pressure side
#          Vp=[Base.Vector(xpres[i],ypres[i]) for i in range(len(xpres))] 
#       
#        >of suction side
#          Vs=[Base.Vector(xsuc[i],ysuc[i]) for i in range(len(xsuc))] 
# 
#       b. for tangents :
#        
#        >one (the same vector) at the LE for the pressure side and the suction side 
#          vLE  = Base.Vector(vecLE[0],vecLE[1])
#        
#        >two (different vectors) at the TE for the pressure side and the suction side 
#          vTEp = Base.Vector(vecTE[0],vecTE[1])
#          vTEs = Base.Vector(vecTE[2],vecTE[3])
#          
# 5. Create Bsplines and interpolate points (Bspline ??? ça veut dire ??)
#      
#           NACABspS=Part.BSplineCurve()
#           NACABspP=Part.BSplineCurve()
#           
#           NACABspP.interpolate(Vp,InitialTangent=vTEp,FinalTangent=vLE)
#           NACABspS.interpolate(Vs,InitialTangent=vLE ,FinalTangent=vTEs)
#           
# 6. Create Shape and add to document
# 
#           Foil_Section=Part.Shape([NACABspP,NACABspS])
#           MyFoil.addObject("Part::Feature","Foil_Section").Shape=Foil_Section
#           
#           

