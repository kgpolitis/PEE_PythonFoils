# Import the library
import FCFoil

# and constants O  : origin
#               ux : unit vector x-axis
#               uy : unit vector y-axis
#               uz : unit vector z-axis
from FCFoil import O,ux,uy,uz

# Add a document (here without a name)
MyFoil=FCFoil.Doc()
n=10
# Create a NACA Foil 
FS1=FCFoil.NACA2("2210",nps=n,npp=n)

# define centre of rotation 
p=ux+3*uz

# translate the foil up to that point
FS1.translate(p)

# rotate it with respect to that point
FS1.rotate(p,uz,45)

# scale it 
FS1.scale(1.5)

# add foil to document 
MyFoil.add(FS1)

# refresh view
Gui.SendMsgToActiveView("ViewFit")