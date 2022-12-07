import pandas as pd
import numpy as np
import os, sys, subprocess

source_folder      =  os.path.abspath("./00_main_input")
folderfile        =   os.path.abspath("./tfolders.txt")

with open(folderfile, 'r') as tfile:
    foldernames = tfile.readlines()

# results = pd.DataFrame(columns=['beta', 'efast', 'n', 'grwth', 'omega'])
for folder in foldernames:
    folder, beta, tfast = folder.split()
    farprt = f"{folder}/temp_grwth_omega"
    out_input_model = f"{folder}/Input_Model"
    try:
        with open(farprt, 'r') as tfile:
            ndata = tfile.readlines()
        n, grwth, omega = ndata[0].split() # If FAR3D_NEW // Modificar índice según el modo que se quiera
        # grwth, omega = ndata[i].split() # If FAR3D_OLD // Modificar índice según el modo que se quiera
        omega = np.float64(omega)
        # Rewrite input model
        with open(out_input_model, 'r') as nfile:
            ndata = nfile.readlines()
        tline = [idx for idx,line in enumerate(ndata) if 'epflr_on: ' in line][0] + 1
        ndata[tline] = "1\n"
        tline = [idx for idx,line in enumerate(ndata) if 'omegar: ' in line][0] + 1
        ndata[tline] = f"{omega:.5f}\n"
        with open(out_input_model, 'w') as nfile:
            ndata = nfile.writelines(ndata)
    except Exception as e:
        print(e)

# results.to_excel('results.xlsx')
