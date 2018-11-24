import os, sys
import subprocess
import re


"""
Hadd samples into one.

Args:
    None

Usage:
    python haddSamples.py

Returns:
    A big root file made out of several skimmed ones.

"""
curDir = os.getcwd()
cmd = 'hadd -f '
#Radion_80r2as_2016_MAv2_v0v1.root skim*root'


for dirName, folders, files in os.walk("."):
    if dirName == ".":
        for folder in folders:
            #nameRe
            niceName = re.compile(r'([A-Za-z0-9_-]*)__Run([A-Za-z0-9_-]*)').search(folder).group(1)
#            matchObj = nameRe
 #           niceName = matchObj
            cmdhadd=cmd + niceName + '.root ' + folder + '/skim*root'
            
            output = str(subprocess.check_output( 'echo ' + cmdhadd, shell=True))
            print 'Before executing: ', output
            try:
                retcode = subprocess.check_output( cmdhadd, shell=True)
                if retcode < 0:
                    print >>sys.stderr, "Child was terminated by signal", -retcode
                    print '\n'
                else:
                    print >>sys.stderr, "Child returned:", retcode
                    print '\n'
            except OSError as e:
                print >>sys.stderr, "Execution failed:", e



