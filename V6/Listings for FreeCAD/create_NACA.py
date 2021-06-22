# Import the library
import FCFoil

# Add a document (here without a name)
MyFoil=FCFoil.Doc()
n=20
# Create a NACA Foil Wire
FS=FCFoil.NACA2("4430",nps=n,npp=n)

# Add it as a part feature
MyFoil.add(FS)