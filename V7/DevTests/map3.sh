#!/bin/bash
# 
# Create a mapping between version 27 and the 
# foil libraries found in this directory
# 
# To use this file type at a terminal : 
#     ./map27.sh
# 
# But do not forget to set the execution
# priviledges :
#     chmod +x map27.sh
# 
# 
ln -sf ../ForPython3/FOIL.py
ln -sf ../ForPython3/NACA_LIB.py
ln -sf ../ForPython3/WAGENINGEN_LIB.py

