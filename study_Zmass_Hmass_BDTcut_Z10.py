import subprocess
import time, os
import numpy as np
import glob, re, io
import pickle, itertools

trueRun = True

dirs = [
    '1pb_noBDTcut_inCRs_Zm10p10_Hm20p20',
    '1pb_noBDTcut_inCRs_Zm10p10_Hm30p25',
    # '1pb_noBDTcut_inCRs_Zm15p15_Hm25p20', '1pb_noBDTcut_inCRs_Zm15p15_Hm35p25',
    '1pb_noBDTcut_inCRs_Zm10p10_Hm25p20', '1pb_noBDTcut_inCRs_Zm10p10_Hm35p25',
    # '1pb_noBDTcut_inCRs_Zm15p15_Hm25p25',
    '1pb_noBDTcut_inCRs_Zm10p10_Hm25p25',
    # '1pb_noBDTcut_inCRs_Zm15p15_Hm20p20', '1pb_noBDTcut_inCRs_Zm15p15_Hm30p25'
    ]

curDir = os.getcwd()
for d in dirs:
    
    os.chdir(d)
    cp_command = 'cp ../createBDTvsLimitPlot.py .' 
    print_commad = 'pwd'

    run_command = 'python createBDTvsLimitPlot.py ' + d
    if trueRun:
        time.sleep(1)
        subprocess.call(cp_command, shell=True)
        subprocess.call(print_commad, shell=True)
        subprocess.call(run_command, shell=True)
    os.chdir(curDir)
