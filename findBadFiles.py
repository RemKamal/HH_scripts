import subprocess
from ROOT import TFile
#import ROOT
import os
import pprint

try:
    listOfTrees = subprocess.check_output('ls *root', shell=True).split('\n')[:-1]
except subprocess.CalledProcessError as e:
    print e    

allFiles = set(listOfTrees)
badFilesList = []

for fil in listOfTrees:
    if fil:
        print 'working with', fil
        try:
            print 'IN THE TRY'
            root_f = TFile.Open(fil)
            tree=root_f.Get('tree')
            size = os.stat(fil).st_size
            if root_f.IsZombie() or not root_f.IsOpen() or root_f.TestBit(TFile.kRecovered) or size <= 1000 or not tree:
                print 'ZOMBIE file {0}'.format(fil)
                badFilesList.append(fil)
        except Exception as e:
            print 'IN THE EXCEPTION'
            print 'file {0} has size {1}.'.format(fil, size)
            print e
            badFilesList.append(fil)

        print
        print

print '{0} files overall'.format(len(allFiles))
badFiles = set (badFilesList)
goodFiles = allFiles.symmetric_difference(badFiles)
print '{0} goodFiles are:'.format(len(goodFiles)) 
pprint.pprint(goodFiles)


print '{0} badFiles:'.format(len(badFiles))
pprint.pprint(badFiles) 
