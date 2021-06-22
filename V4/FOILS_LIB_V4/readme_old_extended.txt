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

