import os
import subprocess
import re
fileLocation = ['/store/user/arizzi/VHBBHeppyV25/', '/store/user/tboccali/Ntuples_v25/', '/store/group/phys_higgs/hbb/ntuples/V25' ]


"""
Prepare a list of BG MCsamples from the location defined above.

Args:
    None

Usage:
    python prepareSamples.py > logOfSamples.txt

Returns:
    A list of samples to use with 'chooseBestSamples.py'

"""


skipList = [] #'WJet', 'Wjet', 'DYJet', 'NuNu', '1L1Nu', '2Nu','LNu', "WH", 'Wplus', 'Wminus' , 'Bulk', 'GluHTo' ,'VBFHToBB', 'ZHiggs0', 'bbHToBB', 'ToQQ']
prefixPisa = 'xrdfs stormgf1.pi.infn.it ls '
prefixCern = 'xrdfs 188.184.38.46 ls '
for site in fileLocation:
    prefix = prefixCern if 'group' in site else prefixPisa
    files = str(subprocess.check_output(prefix+site, shell=True) )
    for l1 in files.split('\n'):
        filesL1 = str(subprocess.check_output(prefix + l1, shell=True) )
        for l2 in filesL1.split('\n'):
            if site in l2:
                filesL2 = str(subprocess.check_output(prefix + l2, shell=True) )
                for l3 in filesL2.split('\n'):
                    #keep only MC samples 
                    if site in l3 and 'Summer16MAv2' in l3:
                        filesL3 = str(subprocess.check_output(prefix + l3, shell=True) )
                        l = len(filesL3.split('\n'))-1
                        myStr = l3 + "/:"
                        for count, l4 in enumerate (filesL3.split('\n'), start = 1) :
                            if count ==1: 
                                myStr += l4[-4:]
                            if count >1 and count<=l:
                                myStr +=','+ l4[-4:]
                        # remove unwanted samples
                        if any(word in myStr for word in skipList):
                            continue
                        else:
                            print myStr
