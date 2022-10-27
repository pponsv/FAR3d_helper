import os
import sys
import subprocess
import numpy as np

JOULE_TO_KEV   = 1.60218E-16 #
ION_MASS       = 1.672621898E-27 # kg
B_ZERO         = 0.95 # T
CONST_MU_0     = 4*np.pi*1e-7

def calc_cvfp(efast, dens):
    """Calcula cvfp a partir de la energía del ión y la densidad"""
    v_fast = np.sqrt(efast * JOULE_TO_KEV / ION_MASS) # m/s (falta un factor 1/2? )
    v_alf  = B_ZERO / np.sqrt(CONST_MU_0 * ION_MASS * dens)
    # print(v_fast, v_alf)
    return v_fast/v_alf

source_folder      =  os.path.abspath("./00_main_input")

source_input_model = f"{source_folder}/Input_Model"
source_input_eq    = f"{source_folder}/Eq_NBI"
source_input_profs = f"{source_folder}/TJII_NBIx.txt"
source_exec        = f"{source_folder}/xfar3d"
source_run         = f"{source_folder}/test.sh"

cwd                = os.getcwd()

dens   = 1.15E19 # 1e20 m^-3
# Parameters to scan
betas  = np.linspace(0.01, 0.03, 2) # beta_fast
e_fast = np.linspace(5, 30, 2) # in KeV

for tbeta in betas:
    for te_fast in e_fast:
        tfoldername     = f"beta_{tbeta:.3f}_efast_{te_fast:.3f}"
        out_input_model = os.path.abspath(f"./{tfoldername}/Input_Model")
        ## Make folder, copy Input_Model
        subprocess.run(["mkdir", "-p", tfoldername])
        subprocess.run(["cp", source_input_model, out_input_model])
        ## Linking other files
        subprocess.run(["ln", "-sf", source_input_eq,    f"{tfoldername}/Eq_NBI"])
        subprocess.run(["ln", "-sf", source_input_profs, f"{tfoldername}/TJII_NBIx.txt"])
        subprocess.run(["ln", "-sf", source_exec,        f"{tfoldername}/xfar3d"])
        subprocess.run(["ln", "-sf", source_run,         f"{tfoldername}/test.sh"])
        ## Change executable
        with open(out_input_model, 'r') as tfile:
            ndata    = tfile.readlines()
        ## Change beta
        tline        = [idx for idx,line in enumerate(ndata) if 'bet0_f: ' in line][0] + 1
        ndata[tline] = f"{tbeta:.5f}\n"
        ## Change cvfp
        cvfp         = calc_cvfp(te_fast, dens)
        tline        = [idx for idx,line in enumerate(ndata) if 'cvfp: ' in line][0] + 1
        ndata[tline] = f"{cvfp:.5f}, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0\n"
        with open(out_input_model, 'w') as nfile:
            nfile.writelines(ndata)
        ## Run bash file
        os.chdir(tfoldername)
        subprocess.Popen("./TJII.sh")
        os.chdir(cwd)
# print(ndata)
