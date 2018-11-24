#!/usr/bin/env python
import time
import subprocess 
import sys, os

date = 'sept22'
version = '_inpb'
jsons = ['toMakeDataCard_samples_1pb_bbZZ_muons.json', 'toMakeDataCard_samples_1pb_bbZZ_electrons.json']
runTypes = ['DoCuts', 'SaveTrees']

#json = 'toMakeDataCard_samples_1pb_total_onlyVV.json'
json = jsons[0]
print json 

typeList = [
    'SR',
    #'CRDY',
    # 'CRTT',
    # 'CRDY_0b',
    #'CRDY_1b'
    #
    ]

runTyp =  runTypes[1]

if len(sys.argv) > 1:
    regionArgument = sys.argv[1] 
    if regionArgument != 'minitrees':
        print 'Are you sure about region?'
        sys.exit(1)
else:
    regionArgument = None
if not regionArgument:
    print 'please specify "regionArgument", exiting...'
    sys.exit(1)

trueRun = True
noSleep = True

for typ in typeList:
    print 'regionArgument is ', regionArgument
    #typ = typ if regionArgument is None else regionArgument
    print 'typ is ', typ
    
    # hzzCmd="nohup python runSimpleAn_v16_" + regionArgument  + ".py  -i samplesMar21  -j data/samples_" + date + "_tot_hzz.json  -w analysis_" + date + "_tot_hzz_" + typ + '_' + regionArgument + version + " -r " + typ +  " -n 16 -t " + runTyp + " &> log_" + date + "_tot_hzz_" + typ + '_' + regionArgument + version + ".txt&"
    # print
    # print 'Start analyzing HtoZZ part of the signal MC samples'
    # print hzzCmd
    # if trueRun:
    #     p1 = subprocess.Popen(hzzCmd, shell = True)
    #     if not noSleep:
    #         time.sleep(150)   
    #     while p1.poll() is None:
    #         time.sleep(1)
    #     print "Hzz process ended, ret code:", p1.returncode


    # hwwCmd="nohup python runSimpleAn_v16_" + regionArgument  + ".py  -i samplesMar21  -j data/samples_" + date + "_tot_hww.json  -w analysis_" + date + "_tot_hww_" + typ + '_' + regionArgument + version + " -r " + typ + " -n 16 -t " + runTyp + " &> log_" + date + "_tot_hww_" + typ + '_' + regionArgument + version + ".txt&"
    # print
    # print 'Start analyzing HtoWW part of the signal MC samples'
    # print hwwCmd
    # if trueRun:
    #     p2 = subprocess.Popen(hwwCmd, shell = True)
    #     if not noSleep:
    #         time.sleep(200)   
    #     while p2.poll() is None:
    #         time.sleep(1)
    #     print "Hww process ended, ret code:", p2.returncode


    #totalCmd="echo 20000 | dc -e '?[q]sQ[d1=Qd1-lFx*]dsFxp'"
    totalCmd = "nohup python runSimpleAn_v16_" + regionArgument  + ".py  -i samplesSept21  -j data/" + json + " -w analysis_" + date + "_total_" + typ + '_' + regionArgument + version + " -r " + typ + " -n 16 -t " + runTyp + " &> log_" + date + "_total_" + typ + '_' + regionArgument + version + ".txt&"
    print
    print 'Start analyzing all signal, BG, and data samples.'
    print totalCmd
    if trueRun:
        p3 = subprocess.Popen(totalCmd, shell = True)
        if not noSleep:
            time.sleep(7600)   
        while p3.poll() is None:
            time.sleep(10)
        print "total signal process ended, ret code:", p3.returncode
        print 'job number of the CHILD process in bash is ', p3.pid
    print '=/='*50

print 'all is done!'
