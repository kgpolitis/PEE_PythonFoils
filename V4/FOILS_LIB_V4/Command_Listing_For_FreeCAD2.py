# Listing for Foil Generation Example with FreeCAD
from FreeCAD  import Base
import Part
from WAGENINGEN_LIB import WAGENINGEN 

MyFoil=App.newDocument("MyFoil")

foil=WAGENINGEN(Z=4,EAR=1,rR=0.40,tLE_tmax=0,Use_Original=1,s=0)

xpres,ypres=foil.PressureSide_FCAD(npoints=40)
xsuc,ysuc=foil.SuctionSide_FCAD(npoints=40)

vecLE=foil.vecS_LE()
vecTE=foil.vecS_TE()

Vp=[Base.Vector(xpres[i],ypres[i]) for i in range(len(xpres))] 
Vs=[Base.Vector(xsuc[i],ysuc[i]) for i in range(len(xsuc))] 
vLE  = Base.Vector(vecLE[0],vecLE[1])
vTEp = Base.Vector(vecTE[0],vecTE[1])
vTEs = Base.Vector(vecTE[2],vecTE[3])
          
NACABspS=Part.BSplineCurve()
NACABspP=Part.BSplineCurve()

NACABspP.interpolate(Vp,InitialTangent=vTEp,FinalTangent=vLE)
NACABspS.interpolate(Vs,InitialTangent=vLE ,FinalTangent=vTEs)

Foil_Section=Part.Shape([NACABspP,NACABspS])

MyFoil.addObject("Part::Feature","Foil_Section").Shape=Part.Wire(Foil_Section.Edges)

