import pandas as pd
import numpy as np
import os, sys, subprocess

source_folder      =  os.path.abspath("./00_main_input")
folderfile        =   os.path.abspath("./tfolders.txt")

with open(folderfile, 'r') as tfile:
    foldernames = tfile.readlines()

results = pd.DataFrame(columns=['beta', 'efast', 'n', 'grwth', 'omega'])
k = 0
for folder in foldernames:
    folder, beta, tfast = folder.split()
    farprt = f"{folder}/temp_grwth_omega"
    try:
        with open(farprt, 'r') as tfile:
            ndata = tfile.readlines()
        for i in range(0, len(ndata), 4):
            n, grwth, omega = ndata[i].split()
            results.loc[k] = [beta, tfast, n, grwth, omega]
            k += 1
    except Exception as e:
        print(e)

results.to_excel('results.xlsx')
