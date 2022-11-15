import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import os
from cycler import cycler

plt.rc('axes', prop_cycle=(cycler('linestyle', ['-', '--', ':', '-.'])) * 
        cycler('color', mpl.colormaps['tab10'](np.linspace(0, 1, 7) )))

folderfile = os.path.abspath("./tfolders.txt")

with open(folderfile, 'r') as tfile:
    foldernames = tfile.readlines()

for folder in foldernames:
    foldername, beta, tfast = folder.split()
    print(foldername)
    phifile = f"./{foldername}/phi_0000"
    try:
        tmp = pd.read_csv(phifile, sep='\t')
        fig, ax = plt.subplots(1,1, figsize=[7,5])
        tmp.plot(x="r", y=tmp.columns[1:], ax=ax)
        ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        fig.savefig(f"./{foldername}/phi.pdf")
    except Exception as e:
        print(f"{foldername}: error")
        print(e)
    

plt.show()
