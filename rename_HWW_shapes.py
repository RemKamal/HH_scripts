import sys
import glob
from shutil import copyfile
import os

trueRun = True

for name in glob.glob("*/*/Glu*HWW*root"):
    if True:#'450' in name and 'nominal' in name and 'low_SR_0.925' in name:
        pass
    else:
        continue

    print 'name', name
        
    newName = name.replace('_HWW', '')
    #[:name.find("_RunIISummer")] + "minitree.root"
    print 'newName', newName
    if not trueRun: continue
    if not os.path.exists(newName):
        copyfile(name, newName)

