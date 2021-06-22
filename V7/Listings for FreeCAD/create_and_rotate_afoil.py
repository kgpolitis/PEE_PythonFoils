# Import the library
import FCFoil

# and constants O  : origin
#               ux : unit vector x-axis
#               uy : unit vector y-axis
#               uz : unit vector z-axis
from FCFoil import O,ux,uy,uz

# Add a document (here without a name)
MyFoil=FCFoil.Doc()

# Create a NACA Foil 
FS1=FCFoil.NACA2("4430")

# define centre of rotation 
p=ux+3*uz

# translate the foil up to that point
FS1.translate(p)

# rotate it with respect to that point
FS1.rotate(p,uz,45)

# add foil to document 
MyFoil.add(FS1)

# refresh view
Gui.SendMsgToActiveView("ViewFit")