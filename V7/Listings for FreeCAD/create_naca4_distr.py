import FCFoil
M=FCFoil.Doc()
M.NACA("4430")
M.n_sections(3)
M.c=FCFoil.linear(1.5,1)
M.t=FCFoil.linear(20,0)
M.L=2
M.add()