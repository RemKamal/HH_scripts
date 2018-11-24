import os, sys
import subprocess
import re
import time
import random

"""
Hadd samples into one.

Args:
    None

Usage:
    python haddSamples.py

Returns:
    A big root file made out of several skimmed ones.

"""

skipList = ['QCD', '10to50', 'HT', 'DiLept', 'TT_TuneCUETP8M2T4down', 'TT']
dryRun = False
curDir = os.getcwd()
cmd = 'hadd -f -n 0 '
#Radion_80r2as_2016_MAv2_v0v1.root skim*root'


for dirName, folders, files in os.walk("."):
    if dirName == ".":
        #print folders
        for folder in folders:
            #print folder
            #nameRe
            #niceName = re.compile(r'([A-Za-z0-9_-]*)__Run([A-Za-z0-9_-]*)').search(folder).group(1)
#            matchObj = nameRe
 #           niceName = matchObj
            #cmdhadd=cmd + niceName + '.root ' + folder + '/skim*root'
                      
            if any(dir in folder for dir in skipList): continue

            cmdhadd=cmd + folder + '.root ' + folder + '/skim*root' 
            
            output = str(subprocess.check_output( 'echo ' + cmdhadd, shell=True))
            #print 'Before executing: ', output
            rint = str(random.randint(1, 1000) )
            #checkFileCmd = 'ar_skim' + rint + '=( $(find ./' + folder + '/' + ' -maxdepth 1 -name "skim*" -size +0 ) )' 
            checkFileCmd = 'ar_skim=( $(find ./' + folder + '/' + ' -maxdepth 1 -name "skim*" -size +0 ) )' 
            print 'command to execute: ', checkFileCmd

            try:
                print 'Checking ... ', folder
                ret = subprocess.check_output( checkFileCmd, shell=True)
                time.sleep(2)
                #retur = subprocess.check_output( 'export filesLength=${#ar_skim'+rint+'[@]}' , shell=True)
                retur = subprocess.check_output( 'export filesLength=${#ar_skim[@]}' , shell=True)
                if ret < 0 or retur < 0:
                    print >>sys.stderr, "Child was terminated by signal", -\
retcode
                    print '\n'
                else:
                    print >>sys.stderr, "Child returned:", ret
                    print >>sys.stderr, "Child returned:", retur
                    print '\n'
            except OSError as e:
                print >>sys.stderr, "Execution failed:", e

            try:
                fLength = int(os.environ['filesLength'])
                print 'fLength is ', fLength
                print 'random int is ', rint
            except KeyError: 
                print "Please set the environment variable, see the code."
                sys.exit(1)
                
            if fLength <= 0:
                print folder, ' has no skim* files'
                continue
#            elif fLength < 0:
 #               exit(1)
            elif fLength > 50:
                print 'more than 50 skim files...'
                subprocess.check_output( 'mkdir ' + folder + '_hadd_part2', shell=True)
                time.sleep(2)
                subprocess.check_output( 'ls ' + folder + '/skim*  | head -50 | xargs -I{} mv {} ' +folder + '_hadd_part2', shell=True)
                time.sleep(5)
            else:
                #print 'fLength is ', fLength
                print 'Smth is wrong, check the code!'
                exit(1)
                
            if not dryRun:
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

                if fLength > 50:
                    cmdhadd2=cmd + folder + '_hadd_part2.root ' + folder + '_hadd_part2/skim*root' 
                    try:
                        retcode2 = subprocess.check_output( cmdhadd2, shell=True)
                        if retcode2 < 0:
                            print >>sys.stderr, "Child was terminated by signal", -retcode2
                            print '\n'
                        else:
                            print >>sys.stderr, "Child returned:", retcode2
                            print '\n'
                    except OSError as er:
                        print >>sys.stderr, "Execution failed:", er
                        



