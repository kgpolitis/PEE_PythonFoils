# Creates two interpolating splines
# and two splines defined by translating and rotating 
# the first two and two wire generated from them to a document
# At the fin
import Part
from FreeCAD import Base
from FCFoil import O,ux,uy,uz
from numpy import sqrt, linspace

# Preliminaries (before starting the actual work)
# Create a document

rev=True
if (rev):
    FreeCAD.newDocument("Test_revT")
    FreeCAD.setActiveDocument("Test_revF")
else:
    FreeCAD.newDocument("Test_revF")
    FreeCAD.setActiveDocument("Test_revF")
    
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
n=4
t=linspace(0,1,n)
V=[ux*t[i]+uy*t[i]*(1-t[i]) for i in range(len(t))]

# Construct Spline R
SpR=Part.BSplineCurve()
SpR.interpolate(V,InitialTangent=ux+uy,FinalTangent=ux-uy)

## Redine point 2 for spline L
#  Note : lists indexing begins at 0,
#         the index of the second point is 1 
if (rev) : 
    t=linspace(1,0,n)

V=[ux*t[i]-uy*t[i]*(1-t[i]) for i in range(len(t))]

# Construct Spline L
SpL=Part.BSplineCurve()
if (not rev):
    SpL.interpolate(V,InitialTangent=ux-uy,FinalTangent=ux+uy)
else    :
    SpL.interpolate(V,InitialTangent=-ux-uy,FinalTangent=-ux+uy)

# We create a wire S (for section)
S=Part.Wire([SpR.toShape(),SpL.toShape()])

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

t=linspace(0,1,n)
V=[ux*t[i]+0.5*uy*t[i]*(1-t[i]) for i in range(len(t))]

# Construct Spline R
SpR=Part.BSplineCurve()
SpR.interpolate(V,InitialTangent=ux+0.5*uy,FinalTangent=ux-0.5*uy,Parameters=t)

## Redine point 2 for spline L
#  Note : lists indexing begins at 0,
#         the index of the second point is 1 
if (rev):
    t=linspace(1,0,n)

V=[ux*t[i]-0.2*uy*t[i]*(1-t[i]) for i in range(len(t))]

# Construct Spline L
SpL=Part.BSplineCurve()
if (not rev):
    SpL.interpolate(V,InitialTangent=ux-0.2*uy,FinalTangent=ux+0.2*uy,Parameters=t)
else    :
    SpL.interpolate(V,InitialTangent=-ux-0.2*uy,FinalTangent=-ux+0.2*uy,Parameters=1-t)

# We create a wire S (for section)
SS=Part.Wire([SpR.toShape(),SpL.toShape()])

p=uy+3*uz
SS.scale(1.5)
SS.translate(p)
SS.rotate(p,uz,45)

Part.show(SS,"SS")

# Now you can use loft 
Part.show(Part.makeLoft([S,SS]))
