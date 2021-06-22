# Creates two interpolating BSplineCurves
# and adds them to a document
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

# Construct Spline L
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

# Create a Wire that contains both splines
D.addObject("Part::Feature","LR").Shape=Part.Wire([SpL.toShape(),SpR.toShape()])

# Test if the objects are closed
# Note that the objected are referenced by "name" provided at the addObject command
# For Spline L
D.L.Shape.isClosed()
# For Spline R
D.R.Shape.isClosed()
# For the Wire
D.LR.Shape.isClosed()

# Notes :
#   1. There is no need to define two lists of points (VR and VL).
#      As long as we use the list of point we don't need it anymore
#      and we may replace the points in a single list.
#      In a similar manner we dont need to define two Splines.
#      A single spline tool suffices as long as we create the 
#      shape and add it as an object to our document directly.
#   2. Here the commands at lines 41,42 work in the same manner 
#      as the command Part.show so they can be replaced by 
#      Part.show(SpR.toShape(),"R")
#      Part.show(SpL.toShape(),"L")