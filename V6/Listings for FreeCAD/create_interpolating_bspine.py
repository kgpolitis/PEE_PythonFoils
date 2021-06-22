import Part
from FreeCAD import Base

# Alias for Base.Vector (here Vec)
Vec=Base.Vector

# Vector Constants
O=Vec(0,0,0)
ux=Vec(1,0,0)
uy=Vec(0,1,0)
uz=Vec(0,0,1)

## Set of points for spline R (right)
VR=[O,ux+uy,2*uy]

# Construct Spline R
SpR=Part.BSplineCurve()
SpR.interpolate(VR)

## Set of point for spline L (left)
VL=[O,-0.5*ux+uy,2*uy]

# Construct Spline 2
SpL=Part.BSplineCurve()
SpL.interpolate(VL)

# At this point we have constructed the "geometry".
# We have to relate the geometry to a document 
# in order to visualise it.

# Create a document 
FreeCAD.newDocument("Test")
FreeCAD.setActiveDocument("Test")

# Create an alias (here D) for the ActiveDocument
D=FreeCAD.ActiveDocument

# Add the splines directly to the document 
D.addObject("Part::Feature","R").Shape=SpR.toShape()
D.addObject("Part::Feature","L").Shape=SpL.toShape()

# Notes :
#    There is no need to define two lists of points (VR and VL).
#    As long as we use the list we don't need it anymore.
#    In a similar manner we dont need to define two Splines.
#    A single spline tool suffices as long as we create the 
#    shape and add it as an object to our document directly.