#!/usr/bin/env python
import time
import subprocess 
import sys, os

trueRun = False
noSleep = True

today = 'May25_altern'
version = '_inpb_wBR'
jsons = [ 
    #'test_bbZZ_withMuons_v4.json',#'test_bbZZ.json',
    #'test_bbZZ_withEles.json',#'test_bbZZ_noTTnDY.json'
    #'toMakeDataCard_samples_1pb_bbZZ_muons_with_bbVV_test.json',
    #'toMakeDataCard_samples_1pb_bbZZ_eles_with_bbVV_test.json',
    #'toMakeDataCard_samples_1pb_bbZZ_muons_with_bbVV_test.json',
    #'toMakeDataCard_samples_1pb_bbZZ_muons_with_bbVV_v3_with_bbtautau.json',
    #'toMakeDataCard_samples_1pb_bbZZ_eles_with_bbVV_v3_with_bbtautau.json'

    #'toMakeDataCard_samples_1pb_eles_BGrav_cutFlow.json',
    #'toMakeDataCard_samples_1pb_muons_BGrav_cutFlow.json'

    "new_toMakeDataCard_samples_1pb_eles_BGrav.json",
    "new_toMakeDataCard_samples_1pb_eles_Radion.json",
    "new_toMakeDataCard_samples_1pb_muons_BGrav.json",
    "new_toMakeDataCard_samples_1pb_muons_Radion.json"
    #"toMakeDataCard_samples_1pb_eles_BGrav.json",
    #"toMakeDataCard_samples_1pb_eles_Radion.json",
    #"toMakeDataCard_samples_1pb_muons_BGrav.json",
    #"toMakeDataCard_samples_1pb_muons_Radion.json"
    ]


runTypes = ['DoCuts', 'SaveTrees']

muons = 0
electrons = 1

#channel = muons
#channel = electrons


typeList = [
    'SR',
    #'CRDY',
    # 'CRTT',
    # 'CRDY_0b',
    #'CRDY_1b'
    #
    ]

runTyp =  runTypes[1]

# if len(sys.argv) > 1:
#     regionArgument = sys.argv[1] 
#     if regionArgument != 'minitrees':
#         print 'Are you sure about region?'
#         sys.exit(1)
# else:
#     regionArgument = None

# if not regionArgument:
#     print 'please specify "regionArgument", exiting...'
#     sys.exit(1)

def run(json, postfix, date):
    regionArgument = 'minitrees'
    for typ in typeList:
        print 'regionArgument is ', regionArgument
        print 'postfix=', postfix
        print 'json=', json
    #typ = typ if regionArgument is None else regionArgument
        print 'typ is ', typ
        print "date=", date
        channel = 0 if "muons" in json else 1 if "eles" in json else None
    #totalCmd="echo 20000 | dc -e '?[q]sQ[d1=Qd1-lFx*]dsFxp'"
#runSimpleAn_v18_minitrees_indev_v1_muons_VTC.py runSimpleAn_v18_minitrees_indev_v1_VTC_muons_copy.py

        totalCmd = "nohup python runSimpleAn_v18_" + regionArgument  + "_indev_v1_VTC" + postfix + "_copy_0.py  -i samples20May2018  -j data/" + json + " -w analysis_" + date + "_total_" + typ + '_' + regionArgument + version + " -r " + typ + " -n 32 -t " + runTyp + " --channel2run " + str(channel) + " &> log_" + date + "_total_" + typ + '_' + regionArgument + version + ".txt&"
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
            print 'job number of the process in bash is ', (p3.pid+1)
        print '=/='*50




if __name__ == "__main__":
    for json in jsons:
        date = today
        postfix = '_muons' if 'muons' in json else '_eles' if 'eles' in json else ''
        date += postfix

        #json = jsons[channel]
        #print json 
        #print 'postfix=', postfix
        #print 'json=', json

        if postfix not in json:
            print 'smth is wrong, continue...'#exiting....'                                                   
            continue #sys.exit(1) 

        date += '_BGrav' if 'BGrav' in json else '_Radion' if 'Radion' in json else "wrong"
        if "wrong" in date:
            print 'smth is wrong, exiting....'
            sys.exit(1)

        #print "date=", date
        run(json, postfix, date)
    print 
    print 'all is done!'
