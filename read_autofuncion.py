import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

folderfile = os.path.abspath("./tfolders.txt")

with open(folderfile, 'r') as tfile:
    foldernames = tfile.readlines()

for folder in foldernames:
    foldername, beta, tfast = folder.split()
    print(foldername)
    phifile = f"./{foldername}/phi_0000"
    try:
        fig, ax = plt.subplots(1,1)
        tmp = pd.read_csv(phifile, sep='\t')
        tmp.plot(x="r", y=tmp.columns[1:], ax=ax)
        fig.savefig(f"./{foldername}/phi.pdf")
    except Exception as e:
        print(f"{foldername}: error")
        print(e)
    

plt.show()
