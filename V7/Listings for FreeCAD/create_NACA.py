# Import the library
import FCFoil

# Add a document (here without a name)
M=FCFoil.Doc()

# Create a NACA Foil Wire
#M.NACA("4430")
# or with options
M.NACA("4430",TE_closed=False)

# Set option "foil spacing of points"
#FCFoil.__spacing__=FCFoil.__spacing_cos__

M.n_sections(3)
M.c=FCFoil.linear(1,0.5)

# Add it as a part feature
M.add()
