#!/usr/bin/env python
import time
import subprocess 
import sys, os

#os.system(cmd)
#chmod +x runSimpleAn_v10_test.py
date = 'mar25'
version = '_v3'

# typeSR = '_sr'
# typeCRtt = '_crTT'
# typeCRdy = '_crDY'
#    typ = typeSR

typeList = [ '_crDY']


for typ in typeList:


    hzzCmd="nohup python  runSimpleAn_v12" + typ  + ".py  -i samplesMar21  -j data/samples_" + date + "_tot_hzz.json  -w analysis_" + date + "_tot_hzz" + typ + version + " -n 16 &> log_" + date + "_tot_hzz" + typ + version + ".txt&"
    print 'Start analyzing HtoZZ part of the signal MC samples'
    print hzzCmd
    p1 = subprocess.Popen(hzzCmd, shell = True)
    time.sleep(150)   
    while p1.poll() is None:
        time.sleep(1)
    print "Hzz process ended, ret code:", p1.returncode


    hwwCmd="nohup python  runSimpleAn_v12" + typ  + ".py  -i samplesMar21  -j data/samples_" + date + "_tot_hww.json  -w analysis_" + date + "_tot_hww" + typ + version + " -n 16 &> log_" + date + "_tot_hww" + typ + version + ".txt&"
    print 'Start analyzing HtoWW part of the signal MC samples'
    print hwwCmd
    #subprocess.check_output(["echo", "Start Popening hww"])
    p2 = subprocess.Popen(hwwCmd, shell = True)
    time.sleep(200)   
    while p1.poll() is None:
        time.sleep(1)
    print "Hww process ended, ret code:", p2.returncode


    totalCmd="nohup python  runSimpleAn_v12" + typ  + ".py  -i samplesMar21  -j data/samples_" + date + "_total.json  -w analysis_" + date + "_total" + typ + version + " -n 16 &> log_" + date + "_total" + typ + version + ".txt&"
    print 'Start analyzing all signal, BG, and data samples.'
    print totalCmd
    p3 = subprocess.Popen(totalCmd, shell = True)
    time.sleep(7500)   
    while p3.poll() is None:
        time.sleep(10)
    print "total signal process ended, ret code:", p3.returncode


print 'all is done'
