# Creates two interpolating splines
# and two splines defined by translating and rotating 
# the first two and two wire generated from them to a document
# At the fin
import Part
from FreeCAD import Base
from FCFoil import O,ux,uy,uz

# Preliminaries (before starting the actual work)
# Create a document 
FreeCAD.newDocument("Test")
FreeCAD.setActiveDocument("Test")

# Create an alias (here D) for the ActiveDocument
#    
#   D=FreeCAD.ActiveDocument

## Alias for Base.Vector (here Vec)
#Vec=Base.Vector
#
## Vector Constants
#O=Vec(0,0,0)
#ux=Vec(1,0,0)
#uy=Vec(0,1,0)
#uz=Vec(0,0,1)
# Note to avoid rewriting the above commands that
# simply create frequently used vectors, we can 
# just import them from FCFoil as above (see line 7) 

# End of Preliminaries
# Actual work :

## Set of points for spline R (right)
#  Note : We define a single list of points
#         and modify it to obtain SpL and SpR
V=[O,0.01*ux+0.5*uy,uy]

# Construct Spline R
SpR=Part.BSplineCurve()
SpR.interpolate(V,InitialTangent=ux,FinalTangent=-ux+uy)

## Redine point 2 for spline L
#  Note : lists indexing begins at 0,
#         the index of the second point is 1 
V=[uy,-0.01*ux+0.5*uy,O]

# Construct Spline L
SpL=Part.BSplineCurve()
SpL.interpolate(V,InitialTangent=-ux-uy,FinalTangent=ux)

# We create a wire S (for section)
S=Part.Wire([SpL.toShape(),SpR.toShape()])

# Add it to the document 
Part.show(S,"S")

# From this point the two items :
#  
#   S : the variable denoting the wire we work with and 
#  "S": the named wire that we defined by the Part.show 
#       command 
#  
# are independent ! So we modify S and add the modified 
# wire to the document

# S is a "shape". This mean that we can transform it using
# different function provided by the FreeCAD framework.
# These functions can be found by typing :
#                S.
# with the dot. At the FreeCAD console this make a help
# menu appear and we can browse the available commands.
# Here we will use translate and rotate.

p=uy+3*uz
S.translate(p)
S.rotate(p,uz,45)

Part.show(S,"SS")

# Now you can use loft 

