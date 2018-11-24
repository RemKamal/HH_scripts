#!/usr/bin/env python
import time
import subprocess 
import sys, os

date = 'june5'
version = '_v1'
trueRun = True
noSleep = False

typeList = [
    #'SR',
    'minitrees'
    #'CRDY',
    #'CRTT',
    #'CRDY_0b',
    #'CRDY_1b'
    
    ]

if len(sys.argv) > 1:
    saveHistsOrTrees = sys.argv[1]
    if len(sys.argv) > 2:
        regionArgument = sys.argv[2] 
        if regionArgument not in {'SR', 'CRDY', 'CRTT'}:
            print 'unknown "regionArgument", please use SR or CRxy, or CRDY_zz'
            sys.exit(1)
    else:
        regionArgument = 'SR'
else:
    print 'choose "DoCuts or SaveTrees" as input arguments' 
    print 'syntax: python produceMiniTrees.py "DoCuts or SaveTrees" "regionArgument"'
    sys.exit(1)


for typ in typeList:
    #typ = typ if regionArgument is None else regionArgument
    print 'typ is ', typ
    
    hzzCmd="nohup python runSimpleAn_v15_" + typ + ".py  -i samplesMar21  -j data/samples_" + date + "_tot_hzz.json  -w analysis_" + date + "_tot_hzz_" + typ + version + " -r " + regionArgument +  " -n 16 -t " + saveHistsOrTrees + " &> log_" + saveHistsOrTrees + "_" +  date + "_tot_hzz_" + typ + version + ".txt&"

    print hzzCmd
    if trueRun:
        print 'Start analyzing HtoZZ part of the signal MC samples'
        
        p1 = subprocess.Popen(hzzCmd, shell = True)
        if not noSleep:
            time.sleep(150)   
        while p1.poll() is None:
            time.sleep(1)
        print "Hzz process ended, ret code:", p1.returncode


    hwwCmd="nohup python runSimpleAn_v15_" + typ + ".py  -i samplesMar21  -j data/samples_" + date + "_tot_hww.json  -w analysis_" + date + "_tot_hww_" + typ + version + " -r " + typ + " -n 16 -t " + saveHistsOrTrees + " &> log_" + saveHistsOrTrees + "_" + date + "_tot_hww_" + typ + version + ".txt&"

    print hwwCmd
    if trueRun:
        print 'Start analyzing HtoWW part of the signal MC samples'
    
        p2 = subprocess.Popen(hwwCmd, shell = True)
        if not noSleep:
            time.sleep(200)   
        while p2.poll() is None:
            time.sleep(1)
        print "Hww process ended, ret code:", p2.returncode


    totalCmd="nohup python runSimpleAn_v15_" + typ + ".py  -i samplesMar21  -j data/samples_" + date + "_total.json  -w analysis_" + date + "_total_" + typ + version + " -r " + typ + " -n 16 -t " + saveHistsOrTrees + " &> log_" + saveHistsOrTrees + "_" + date + "_total_" + typ + version + ".txt&"
    
    print totalCmd
    if trueRun:

        print 'Start analyzing all signal, BG, and data samples.'
        p3 = subprocess.Popen(totalCmd, shell = True)
        # if not noSleep:
        #     time.sleep(7600)   
        # while p3.poll() is None:
        #     time.sleep(10)
        print "total signal process ended, ret code:", p3.returncode
            
    print '=/='*50
    if regionArgument:
        break

print 'all is done!'
