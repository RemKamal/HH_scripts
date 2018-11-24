#!/usr/bin/env python
import time
import subprocess 
import sys, os

date = 'june13'
version = '_inpb'

runTypes = ['DoCuts', 'SaveTrees']

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

trueRun = True
noSleep = False
for typ in typeList:
    print 'regionArgument is ', regionArgument
    #typ = typ if regionArgument is None else regionArgument
    print 'typ is ', typ
    
    hzzCmd="nohup python runSimpleAn_v16_" + regionArgument  + ".py  -i samplesMar21  -j data/samples_" + date + "_tot_hzz.json  -w analysis_" + date + "_tot_hzz_" + typ + '_' + regionArgument + version + " -r " + typ +  " -n 16 -t " + runTyp + " &> log_" + date + "_tot_hzz_" + typ + '_' + regionArgument + version + ".txt&"
    print 'Start analyzing HtoZZ part of the signal MC samples'
    print hzzCmd
    if trueRun:
        p1 = subprocess.Popen(hzzCmd, shell = True)
        if not noSleep:
            time.sleep(150)   
        while p1.poll() is None:
            time.sleep(1)
        print "Hzz process ended, ret code:", p1.returncode


    hwwCmd="nohup python runSimpleAn_v16_" + regionArgument  + ".py  -i samplesMar21  -j data/samples_" + date + "_tot_hww.json  -w analysis_" + date + "_tot_hww_" + typ + '_' + regionArgument + version + " -r " + typ + " -n 16 -t " + runTyp + " &> log_" + date + "_tot_hww_" + typ + '_' + regionArgument + version + ".txt&"
    print 'Start analyzing HtoWW part of the signal MC samples'
    print hwwCmd
    if trueRun:
        p2 = subprocess.Popen(hwwCmd, shell = True)
        if not noSleep:
            time.sleep(200)   
        while p2.poll() is None:
            time.sleep(1)
        print "Hww process ended, ret code:", p2.returncode


    totalCmd="nohup python runSimpleAn_v16_" + regionArgument  + ".py  -i samplesMar21  -j data/samples_" + date + "_total.json  -w analysis_" + date + "_total_" + typ + '_' + regionArgument + version + " -r " + typ + " -n 16 -t " + runTyp + " &> log_" + date + "_total_" + typ + '_' + regionArgument + version + ".txt&"
    print 'Start analyzing all signal, BG, and data samples.'
    print totalCmd
    if trueRun:
        p3 = subprocess.Popen(totalCmd, shell = True)
        if not noSleep:
            time.sleep(7600)   
        while p3.poll() is None:
            time.sleep(10)
        print "total signal process ended, ret code:", p3.returncode
            
    print '=/='*50

print 'all is done!'
