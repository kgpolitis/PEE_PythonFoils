# Import the library
import FCFoil

# Add a document
MyFoil=FCFoil.Doc("My Foil")

# Create a Wageningen Foil 
FS1=FCFoil.WAGEN(Z=4,EAR=1,rR=0.4)

# Add it as a part 
MyFoil.add(FS1)

# Create a Symmetric NACA Foil 
FS2=FCFoil.NACA("0015")

# Add it as a part 
MyFoil.add(FS2)