import sys
import glob
from shutil import copyfile
import os

for name in glob.glob("Glu*RunIISummer*root"):
    print 'name', name
    
    newName = name[:name.find("_RunIISummer")] + "minitree.root"
    print 'newName', newName
    if not os.path.exists(newName):
        copyfile(name, newName)
