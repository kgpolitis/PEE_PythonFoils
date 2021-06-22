# Import the library
import FCFoil

# Add a document (here without a name)
MyFoil=FCFoil.Doc()

# Create a Wageningen Foil 
FS1=FCFoil.WAGEN(Z=4,EAR=1,rR=0.4)

# Add it as a part using a name different from the default
MyFoil.add(FS1,'My Wageningen Section')

# Create a NACA Foil 
FS2=FCFoil.NACA(4430)

# Add it as a part using a name different from the default
MyFoil.add(FS2,'My NACA Section')