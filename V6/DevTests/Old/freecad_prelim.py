from FreeCAD import Base
import Part,PartGui
from NACA_LIB27 import NACA

doc=FreeCAD.newDocument("NACA_test")

foil=NACA(4315)

