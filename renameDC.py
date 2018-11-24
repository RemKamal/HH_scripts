import sys
import fileinput
import shutil
import os
import logging
import re
import pprint

logging.basicConfig(level=logging.INFO)

#if possible - put logger inside the function
logger = logging.getLogger(__name__)

inFile = 'datacard.txt'

dict_substitutions = {
    "QCDscale_Higgs_HH" : "QCDscale_Higgs",
    "CMS_eff_b_light"   : "CMS_btag_light",
    "CMS_eff_b_heavy"   : "CMS_btag_heavy",
    "QCDscale_TT"       : "QCDscale_ttbar",
    "WW"                : "hww",
    "ZZ"                : "hzz",
       #"QCDscale_ST"       : "",
    }

lineToRemove = "QCDscale_ST"


logger.info("before copy")
if os.path.exists(inFile):# or os.path.getsize(inFile) < 100:
    shutil.copy("dataCard_SR.txt", inFile)

logger.info("before for loop")
with open ("dataCard_SR.txt", "r") as fIn, open (inFile, "w") as fOut:
    for line in fIn:
        if line.startswith('\n') or line.startswith('#'):
            pass
        elif lineToRemove in line:
            continue
        else:
            listik = re.split(r'(\s+)', line)
            print listik
            for (k, v) in dict_substitutions.items():#word in listik:
                line = line.replace(k, v)
            listik_new = re.split(r'(\s+)', line)
            print listik_new
            for idx, (el1, el2) in enumerate(zip(listik, listik_new)):
                if el1 != el2:
                    print '-'*100
                    print len(listik_new[idx+1])
                    print len(el1)
                    print len(el2) 
                    newSeparation = (len(listik_new[idx+1]) + (len(el1) - len(el2)))
                    listik_new[idx+1] = ' ' * newSeparation
                    print len(listik_new[idx+1])

            line = ''.join(listik_new)    
        fOut.write(line)


with open (inFile, 'r') as fileCheck:
    pprint.pprint (fileCheck.readlines())


