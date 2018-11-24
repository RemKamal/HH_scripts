import subprocess
import time, os, sys
import numpy as np
import glob, re, io
import pickle, itertools
import pprint
pp = pprint.PrettyPrinter(indent=4)
pp = pprint.PrettyPrinter(depth=6)
from multiprocessing import Pool
from optparse import OptionParser
import argparse

#cpLine = True
addMC = True

date = '_jan5'

trueRun = True                     #keep False for debug
run_combine_and_copy_cards = True   #keep False for debug
copy_logs = True
cpLogs = True
directo = '.'

massesIn = [260, 270, 300, 350, 400, 450,         600, 650, 900, 1000]
#massesIn = [300,450]
leptType = None


# if len(sys.argv) > 0:
#     leptType = sys.argv[1]
#     print 'all is fine, using', leptType
#     if not leptType or leptType not in ['ee_', 'mm_']:
#         print 'wrong input, please use "directory"'
#         sys.exit(1)
# else:
#     print 'not specified "leptType", please provide an input'
#     sys.exit(1)

# if len(sys.argv) > 1:
#     combinationType = sys.argv[2]
#     print 'all is fine, using', combinationType
#     if not combinationType or combinationType not in ['oneBin_combination', 'low_combination', 'high_combination', 'nominal_combination']:
#         print 'wrong input, please use "directory"'
#         sys.exit(1)
# else:
#     print 'not specified "combinationType", please provide an input'
#     sys.exit(1)





curDir = os.getcwd()
#fileOfInterest = 'higgsCombineTest.Asymptotic.mH*.root'
#low_CRTT_0.3/plots/makeDataCards/260/

logList = []

mm_bdtCuts = [0.1, 0.7, 0.99]
ee_bdtCuts = [0.4, 0.925, 0.99]


# if bdtCuts == None:
#     print 'wrong bdtCuts'
#     sys.exit(1)


def runFit(masses):
    tmpList = list()
    tmpList.insert(0, masses)
    masses = tmpList
    print 'masses in runFit:', masses
    if run_combine_and_copy_cards:
        for massRegion in ['low', 'high']:
            print 'doing massRegion ', massRegion
            print
            logList_perMass = []

            bdtCuts = mm_bdtCuts if leptType == 'mm_' else ee_bdtCuts if leptType == 'ee_' else None
            for bdtCut in bdtCuts:  # [-0.9, -0.7, -0.5, -0.3, -0.1,  0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.825, 0.85, 0.9, 0.925, 0.95, 0.99]: #[-0.9,-0.5,0,0.4,0.5,0.8,0.825,0.85,0.9,0.925,0.95,0.99]:#np.arange(-0.9, 1.0, 0.1): #[0.24]: #-0.24, -0.11, 0, 0.11, 0.24]:
                # skip controversial "0" region, which can be 0.0 or some other value



                for mass in masses:
                    print 'mass=', mass
                    if mass <= 450 and massRegion == 'low':
                        pass
                    elif mass >= 450 and massRegion == 'high':
                        pass
                    else:
                        # print 'skipping, since mass is {0} and massRegion is {1}'.format(mass, massRegion)
                        continue

                    if bdtCut == 0 or not -1 < bdtCut < 1 or abs(bdtCut) < 0.001: continue
                    # numpy did not create dirs at 0 :(, instead it was created under the name '-2.22044604925e-16'
                    if massRegion == 'low' and bdtCut > 0.925: continue
                    if massRegion == 'high' and bdtCut < 0.7: continue

                    if leptType == 'mm_':
                        if mass < 300 and bdtCut == 0.1:
                            pass
                        elif 300 <= mass < 600 and bdtCut == 0.7:
                            pass
                        elif 600 <= mass and bdtCut == 0.99:
                            pass
                        else:
                            continue
                    elif leptType == 'ee_':
                        if mass <= 350 and bdtCut == 0.4:
                            pass
                        elif 400 <= mass < 600 and bdtCut == 0.925:
                            pass
                        elif 600 <= mass and bdtCut == 0.99:
                            pass
                        else:
                            continue
                    else:
                        print
                        'cannot happen, exiting'
                        sys.exit(1)

                    tmpDir = leptType + str(massRegion) + '_' + str(bdtCut) + date + '/' + str(mass)
                    # high_0.95_oct19/650
                    if os.path.exists(tmpDir):
                        print 'change dir to', tmpDir
                        os.chdir(tmpDir)
                    print 'tmpDir is', tmpDir
                    # if cpLine:
                    #     if trueRun:
                    #         #cpLine1 = "sed -i -e '$d' dataCard_SR.txt"
                    #         #cpLine2 = "sed -i -e '$d' dataCard_CRDY.txt"
                    #         dataCard_CRDYoneBin_hhMt.txt
                    #         cpLine1 = "cp dataCard_CRDYoneBin_hhMt.txt dataCard_SR.txt " + leptType + "dataCard_SR" + str(mass) + ".txt"
                    #         cpLine2 = "cp dataCard_CRDY.txt " + leptType + "dataCard_CRDY" + str(mass) + ".txt"
                    #         cpLine3 = "cp dataCard_CRTT.txt " + leptType + "dataCard_CRTT" + str(mass) + ".txt"
                    #         time.sleep(1)
                    #         print 'will:'
                    #         print cpLine1
                    #         print cpLine2
                    #         print cpLine3
                    #         #cp last line
                    #         subprocess.call(cpLine1, shell=True)
                    #         subprocess.call(cpLine2, shell=True)
                    #         subprocess.call(cpLine3, shell=True)
                    #         #cp 2nd to last line
                    #         subprocess.call(cpLine1, shell=True)
                    #         subprocess.call(cpLine2, shell=True)
                    #         subprocess.call(cpLine3, shell=True)
                    #         time.sleep(1)

                    logList_perMass.append(directo + '/' + tmpDir + '/log*')
                    logList_perMass.append(directo + '/' + tmpDir + '/higgs*')
                    logList_perMass.append(directo + '/' + tmpDir + '/comb*')
                    logList_perMass.append(directo + '/' + tmpDir + '/hh*')
                    logList_perMass.append(directo + '/' + tmpDir + '/d*mc*')
                    # fitdiagnostics root files?

                    # logList_perMass.append (directo + '/' + tmpDir + '/*hh*root')
                    # logList_perMass.append (directo + '/' + tmpDir + '/' + leptType + 'SR.input.root')
                    # logList_perMass.append (directo + '/' + tmpDir + '/' + leptType + 'CRDY.input.root')
                    # logList_perMass.append (directo + '/' + tmpDir + '/' + leptType + 'CRTT.input.root')
                    # for region in ['CRDY', 'CRTT']:
                    #     cp_cards_n_ROOTfiles = 'cp -r ../../../../../' + str(massRegion) + '_' + region + '_' + str(bdtCut) + '/plots/makeDataCards/' +str(mass) + '/test_wo_br/*' + region + '*{txt,root} .'

                    #     print cp_cards_n_ROOTfiles
                    #     print 'DIRECTORY contains:'; print glob.glob("*R*")
                    # tmpDir = str(mass)




                    # cpCommand = 'cp ' + fileOfInterest + ' ' + curDir
                    # print cpCommand

                    # if trueRun:
                    #     subprocess.call(cp_cards_n_ROOTfiles, shell=True)
                    if massRegion == 'low':
                        range_ = ' --rMin -1000 --rMax 1000 '
                    else:
                        range_ = ' --rMin -100 --rMax 100 '

                        # single CR at a time: copy dc to a new one and add to the latter MC bin-by-bin unc
                    cpSR = """cp dataCard_SR_hhMt.txt dataCard_SR_hhMt_mc.txt && echo "" >> dataCard_SR_hhMt_mc.txt && echo "* autoMCStats 0" >> dataCard_SR_hhMt_mc.txt"""
                    cpCRTT = """cp dataCard_CRTT_hhMt.txt dataCard_CRTT_hhMt_mc.txt && echo "" >> dataCard_CRTT_hhMt_mc.txt && echo "* autoMCStats 0" >> dataCard_CRTT_hhMt_mc.txt"""
                    cpCRDY = """cp dataCard_CRDY_hhMt.txt dataCard_CRDY_hhMt_mc.txt && echo "" >> dataCard_CRDY_hhMt_mc.txt && echo "* autoMCStats 0" >> dataCard_CRDY_hhMt_mc.txt"""
                    cpCRDYlow = """cp dataCard_CRDYlow_hhMt.txt dataCard_CRDYlow_hhMt_mc.txt && echo "" >> dataCard_CRDYlow_hhMt_mc.txt && echo "* autoMCStats 0" >> dataCard_CRDYlow_hhMt_mc.txt"""
                    cpCRDYhigh = """cp dataCard_CRDYhigh_hhMt.txt dataCard_CRDYhigh_hhMt_mc.txt && echo "" >> dataCard_CRDYhigh_hhMt_mc.txt && echo "* autoMCStats 0" >> dataCard_CRDYhigh_hhMt_mc.txt"""
                    cpCRDYoneBin = """cp dataCard_CRDYoneBin_hhMt.txt dataCard_CRDYoneBin_hhMt_mc.txt && echo "" >> dataCard_CRDYoneBin_hhMt_mc.txt && echo "* autoMCStats 0" >> dataCard_CRDYoneBin_hhMt_mc.txt"""
                    cpCRTToneBin = """cp dataCard_CRTToneBin_hhMt.txt dataCard_CRTToneBin_hhMt_mc.txt && echo "" >> dataCard_CRTToneBin_hhMt_mc.txt && echo "* autoMCStats 0" >> dataCard_CRTToneBin_hhMt_mc.txt"""

                    # print
                    # print cpSR
                    # print cpCRTT
                    # print cpCRDY
                    # print cpCRDYlow
                    # print cpCRDYhigh
                    # print cpCRDYoneBin
                    # print cpCRTToneBin

                    ########### all regions
                    commandJoin_oneBinCombination = "combineCards.py SR=dataCard_SR_hhMt.txt CRDY=dataCard_CRDYoneBin_hhMt.txt CRTT=dataCard_CRTToneBin_hhMt.txt > comb_" + leptType + "oneBinCombination_M" + str(
                        mass) + """_mc.txt && echo "" >> comb_""" + leptType + """oneBinCombination_M""" + str(
                        mass) + """_mc.txt &&  echo "* autoMCStats 0" >> comb_""" + leptType + """oneBinCombination_M""" + str(
                        mass) + "_mc.txt"

                    commandJoin_lowCombination = "combineCards.py SR=dataCard_SR_hhMt.txt CRDY=dataCard_CRDYlow_hhMt.txt CRTT=dataCard_CRTT_hhMt.txt > comb_" + leptType + "lowCombination_M" + str(
                        mass) + """_mc.txt && echo "" >> comb_""" + leptType + """lowCombination_M""" + str(
                        mass) + """_mc.txt &&  echo "* autoMCStats 0" >> comb_""" + leptType + """lowCombination_M""" + str(
                        mass) + "_mc.txt"

                    commandJoin_highCombination = "combineCards.py SR=dataCard_SR_hhMt.txt CRDY=dataCard_CRDYhigh_hhMt.txt CRTT=dataCard_CRTT_hhMt.txt > comb_" + leptType + "highCombination_M" + str(
                        mass) + """_mc.txt && echo "" >> comb_""" + leptType + """highCombination_M""" + str(
                        mass) + """_mc.txt &&  echo "* autoMCStats 0" >> comb_""" + leptType + """highCombination_M""" + str(
                        mass) + "_mc.txt"

                    commandJoin_nominalCombination = "combineCards.py SR=dataCard_SR_hhMt.txt CRDY=dataCard_CRDY_hhMt.txt CRTT=dataCard_CRTT_hhMt.txt > comb_" + leptType + "nominalCombination_M" + str(
                        mass) + """_mc.txt && echo "" >> comb_""" + leptType + """nominalCombination_M""" + str(
                        mass) + """_mc.txt &&  echo "* autoMCStats 0" >> comb_""" + leptType + """nominalCombination_M""" + str(
                        mass) + "_mc.txt"
                    # print
                    # print commandJoin_oneBinCombination

                    # print commandJoin_lowCombination

                    # print commandJoin_highCombination

                    # print commandJoin_nominalCombination


                    ############ CRDY and CRTT only
                    commandJoin_CRs_oneBinCombination = "combineCards.py CRDY=dataCard_CRDYoneBin_hhMt.txt CRTT=dataCard_CRTToneBin_hhMt.txt > comb_" + leptType + "CRs_oneBinCombination_M" + str(
                        mass) + """_mc.txt && echo "" >> comb_""" + leptType + "CRs_oneBinCombination_M" + str(
                        mass) + """_mc.txt &&  echo "* autoMCStats 0" >> comb_""" + leptType + "CRs_oneBinCombination_M" + str(
                        mass) + "_mc.txt"

                    commandJoin_CRs_lowCombination = "combineCards.py CRDY=dataCard_CRDYlow_hhMt.txt CRTT=dataCard_CRTT_hhMt.txt > comb_" + leptType + "CRs_lowCombination_M" + str(
                        mass) + """_mc.txt && echo "" >> comb_""" + leptType + "CRs_lowCombination_M" + str(
                        mass) + """_mc.txt &&  echo "* autoMCStats 0" >> comb_""" + leptType + "CRs_lowCombination_M" + str(
                        mass) + "_mc.txt"

                    commandJoin_CRs_highCombination = "combineCards.py CRDY=dataCard_CRDYhigh_hhMt.txt CRTT=dataCard_CRTT_hhMt.txt > comb_" + leptType + "CRs_highCombination_M" + str(
                        mass) + """_mc.txt && echo "" >> comb_""" + leptType + "CRs_highCombination_M" + str(
                        mass) + """_mc.txt &&  echo "* autoMCStats 0" >> comb_""" + leptType + "CRs_highCombination_M" + str(
                        mass) + "_mc.txt"

                    commandJoin_CRs_nominalCombination = "combineCards.py CRDY=dataCard_CRDY_hhMt.txt CRTT=dataCard_CRTT_hhMt.txt > comb_" + leptType + "CRs_nominalCombination_M" + str(
                        mass) + """_mc.txt && echo "" >> comb_""" + leptType + "CRs_nominalCombination_M" + str(
                        mass) + """_mc.txt &&  echo "* autoMCStats 0" >> comb_""" + leptType + "CRs_nominalCombination_M" + str(
                        mass) + "_mc.txt"
                    # print
                    # print commandJoin_CRs_oneBinCombination

                    # print commandJoin_CRs_lowCombination

                    # print commandJoin_CRs_highCombination

                    # print commandJoin_CRs_nominalCombination

                    cpList = [
                        cpSR,
                        cpCRTT,
                        cpCRDY,
                        cpCRDYlow,
                        cpCRDYhigh,
                        cpCRDYoneBin,
                        cpCRTToneBin
                    ]

                    joinAllList = [

                        commandJoin_oneBinCombination,
                        commandJoin_lowCombination,
                        commandJoin_highCombination,
                        commandJoin_nominalCombination
                    ]

                    joinCRsList = [
                        commandJoin_CRs_oneBinCombination,
                        commandJoin_CRs_lowCombination,
                        commandJoin_CRs_highCombination,
                        commandJoin_CRs_nominalCombination

                    ]

                    # print
                    # print 'cpList:', cpList
                    # sys.exit(1)

                    algoSpeedUp = ' --X-rtd MINIMIZER_analytic ' if addMC else ''

                    commandFit_Asymp_oneBinCombination = 'combine -M Asymptotic -v 3 --run blind ' + algoSpeedUp + ' -m ' + str(
                        mass) + ' ' + 'comb_' + leptType + 'oneBinCombination_M' + str(
                        mass) + '_mc.txt >& log_comb_' + leptType + 'oneBinCombination_M' + str(mass) + '_mc.txt'

                    commandFit_Asymp_lowCombination = 'combine -M Asymptotic -v 3 --run blind ' + algoSpeedUp + ' -m ' + str(
                        mass) + ' ' + 'comb_' + leptType + 'lowCombination_M' + str(
                        mass) + '_mc.txt >& log_comb_' + leptType + 'lowCombination_M' + str(mass) + '_mc.txt'

                    commandFit_Asymp_highCombination = 'combine -M Asymptotic -v 3 --run blind ' + algoSpeedUp + ' -m ' + str(
                        mass) + ' ' + 'comb_' + leptType + 'highCombination_M' + str(
                        mass) + '_mc.txt >& log_comb_' + leptType + 'highCombination_M' + str(mass) + '_mc.txt'

                    commandFit_Asymp_nominalCombination = 'combine -M Asymptotic -v 3 --run blind ' + algoSpeedUp + ' -m ' + str(
                        mass) + ' ' + 'comb_' + leptType + 'nominalCombination_M' + str(
                        mass) + '_mc.txt >& log_comb_' + leptType + 'nominalCombination_M' + str(mass) + '_mc.txt'

                    asympList = [
                        commandFit_Asymp_oneBinCombination,
                        commandFit_Asymp_lowCombination,
                        commandFit_Asymp_highCombination,
                        commandFit_Asymp_nominalCombination
                    ]

                    ######15 ML fits:
                    # DY
                    commandFit_ML_DY_nominal = 'combine -M MaxLikelihoodFit -v 3 ' + algoSpeedUp + ' -m ' + str(
                        mass) + range_ + ' ' + 'dataCard_CRDY_hhMt_mc.txt >& log_dataCard_CRDY_hhMt_ML_DYnominal_mc.txt'
                    # in vhbb for signal strength: combine -M MaxLikelihoodFit -m 125 -t -1 --expectSignal=1 --stepSize=0.05 --rMin=-5 --rMax=5 --robustFit==1 --saveNorm --saveShapes --plots -v 3 card
                    commandFit_ML_DY_low = 'combine -M MaxLikelihoodFit -v 3 ' + algoSpeedUp + ' -m ' + str(
                        mass) + range_ + ' ' + 'dataCard_CRDYlow_hhMt_mc.txt >& log_dataCard_CRDYlow_hhMt_ML_DYlow_mc.txt'
                    commandFit_ML_DY_high = 'combine -M MaxLikelihoodFit -v 3 ' + algoSpeedUp + ' -m ' + str(
                        mass) + range_ + ' ' + 'dataCard_CRDYhigh_hhMt_mc.txt >& log_dataCard_CRDYhigh_hhMt_ML_DYhigh_mc.txt'
                    commandFit_ML_DY_oneBin = 'combine -M MaxLikelihoodFit -v 3 ' + algoSpeedUp + ' -m ' + str(
                        mass) + range_ + ' ' + 'dataCard_CRDYoneBin_hhMt_mc.txt >& log_dataCard_CRDYoneBin_hhMt_ML_DYoneBin_mc.txt'

                    # TT 
                    TTparam = ' --robustFit=1 '
                    #DO NOT USE algoSpeedUp, it gives :
                    # Skipping r. Parameter not found in the RooFitResult.  *** Break *** segmentation violation
                    # also, add --robustFit=1 that will do a tiny! slower but maybe? more robust likelihood scan
                    # use not txt datacard but root file workspace created with text2workspace.py
                    commandFit_ML_TT_oneBin = 'text2workspace.py dataCard_CRTToneBin_hhMt_mc.txt && combine -M MaxLikelihoodFit -v 3 ' + TTparam + ' -m ' + str(mass) + range_ + ' ' + '-d dataCard_CRTToneBin_hhMt_mc.root >& log_dataCard_CRTToneBin_hhMt_ML_TToneBin_mc.txt'
                    if 'mm' in leptType and (((mass==450 and massRegion == 'low') or (mass >= 450 and massRegion == 'high')) ): TTparam += algoSpeedUp
                    commandFit_ML_TT_nominal = 'text2workspace.py dataCard_CRTT_hhMt_mc.txt && combine -M MaxLikelihoodFit -v 3 ' + TTparam + ' -m ' + str(mass) + range_ + ' ' + '-d dataCard_CRTT_hhMt_mc.root >& log_dataCard_CRTT_hhMt_ML_TTnominal_mc.txt'


                    # SR
                    commandFit_ML_SR_nominal = 'combine -M MaxLikelihoodFit -v 3 ' + algoSpeedUp + ' -m ' + str(
                        mass) + range_ + ' ' + 'dataCard_SR_hhMt_mc.txt >& log_dataCard_SR_hhMt_ML_SRnominal_mc.txt'

                    # DY with TT
                    commandFit_ML_DYnTT_low = 'combine -M MaxLikelihoodFit -v 3 ' + algoSpeedUp + ' -m ' + str(
                        mass) + range_ + ' ' + 'comb_' + leptType + 'CRs_lowCombination_M' + str(
                        mass) + '_mc.txt >& log_comb_' + leptType + 'CRs_lowCombination_M' + str(mass) + '_ML_mc.txt '
                    commandFit_ML_DYnTT_high = 'combine -M MaxLikelihoodFit -v 3 ' + algoSpeedUp + ' -m ' + str(
                        mass) + range_ + ' ' + 'comb_' + leptType + 'CRs_highCombination_M' + str(
                        mass) + '_mc.txt >& log_comb_' + leptType + 'CRs_highCombination_M' + str(mass) + '_ML_mc.txt '
                    commandFit_ML_DYnTT_oneBin = 'combine -M MaxLikelihoodFit -v 3 ' + algoSpeedUp + ' -m ' + str(
                        mass) + range_ + ' ' + 'comb_' + leptType + 'CRs_oneBinCombination_M' + str(
                        mass) + '_mc.txt >& log_comb_' + leptType + 'CRs_oneBinCombination_M' + str(
                        mass) + '_ML_mc.txt '
                    commandFit_ML_DYnTT_nominal = 'combine -M MaxLikelihoodFit -v 3 ' + algoSpeedUp + ' -m ' + str(
                        mass) + range_ + ' ' + 'comb_' + leptType + 'CRs_nominalCombination_M' + str(
                        mass) + '_mc.txt >& log_comb_' + leptType + 'CRs_nominalCombination_M' + str(
                        mass) + '_ML_mc.txt '

                    # all regions
                    commandFit_ML_highCombination = 'combine -M MaxLikelihoodFit -v 3 ' + algoSpeedUp + ' -m ' + str(mass) + range_ + ' ' + 'comb_' + leptType + 'highCombination_M' + str(mass) + '_mc.txt >& log_comb_' + leptType + 'highCombination_M' + str(mass) + '_ML_mc.txt '

                    commandFit_ML_nominalCombination = 'combine -M MaxLikelihoodFit -v 3 ' + algoSpeedUp + ' -m ' + str(mass) + range_ + ' ' + 'comb_' + leptType + 'nominalCombination_M' + str(mass) + '_mc.txt >& log_comb_' + leptType + 'nominalCombination_M' + str(mass) + '_ML_mc.txt '

                    if mass == 450 and massRegion =='low':
                        algoSpeedUp = ' '


                    commandFit_ML_lowCombination = 'combine -M MaxLikelihoodFit -v 3 ' + algoSpeedUp + ' -m ' + str(mass) + range_ + ' ' + 'comb_' + leptType + 'lowCombination_M' + str(mass) + '_mc.txt >& log_comb_' + leptType + 'lowCombination_M' + str(mass) + '_ML_mc.txt '
                    if mass == 450 and massRegion =='low' and 'ee' in leptType:
                        algoSpeedUp = ' --X-rtd MINIMIZER_analytic ' if addMC else ''
                    commandFit_ML_oneBinCombination = 'combine -M MaxLikelihoodFit -v 3 ' + algoSpeedUp + ' -m ' + str(mass) + range_ + ' ' + 'comb_' + leptType + 'oneBinCombination_M' + str(mass) + '_mc.txt >& log_comb_' + leptType + 'oneBinCombination_M' + str(mass) + '_ML_mc.txt '

                    algoSpeedUp = ' --X-rtd MINIMIZER_analytic ' if addMC else ''
                    mlList = [
                        commandFit_ML_DY_nominal,
                        commandFit_ML_DY_low,
                        commandFit_ML_DY_high,
                        commandFit_ML_DY_oneBin,

                        commandFit_ML_TT_nominal,
                        commandFit_ML_TT_oneBin,

                        commandFit_ML_SR_nominal,

                        commandFit_ML_DYnTT_nominal,
                        commandFit_ML_DYnTT_low,
                        commandFit_ML_DYnTT_high,
                        commandFit_ML_DYnTT_oneBin,

                        commandFit_ML_lowCombination,
                        commandFit_ML_highCombination,
                        commandFit_ML_oneBinCombination,
                        commandFit_ML_nominalCombination
                    ]
                    if trueRun:
                        print
                        print '-' * 50

                        print 'copying data cards'
                        for cp in cpList:
                            print 'doing', cp
                            subprocess.call(cp, shell=True)
                        print
                        print '-' * 50

                        print
                        "join all region dc's"
                        for jA in joinAllList:
                            print 'doing', jA
                            subprocess.call(jA, shell=True)
                        print
                        print '-' * 50

                        print "join CR region dc's"
                        for jCRs in joinCRsList:
                            print 'doing', jCRs
                            subprocess.call(jCRs, shell=True)
                        print
                        print '-' * 50

                        print "fit asymptotic"
                        for a in asympList:
                            print 'doing', a
                            subprocess.call(a, shell=True)
                        print
                        print '-' * 50

                        print "fit maxLikelihood"
                        for ml in mlList:
                            print 'doing', ml
                            subprocess.call(ml, shell=True)
                            # time.sleep(1)
                            # subprocess.call(commandJoin, shell=True)
                            # subprocess.call(commandFit, shell=True)
                            # time.sleep(25)
                            # subprocess.call(commandFit_ML, shell=True)
                            # time.sleep(10)

                    # subprocess.call(cpLog, shell=True)

                    print 'change dir to', curDir
                    os.chdir(curDir)
                print '=' * 50
                logList.append(logList_perMass)






def createCombined(mass):
    dirs_ee = glob.glob('ee*/*')
    dirs_mm = glob.glob('mm*/*')

    sorted_ee_dirs = sorted(dirs_ee, key = lambda x: x[-4:])
    sorted_mm_dirs = sorted(dirs_mm, key = lambda x: x[-4:])
    for d_e, d_m in zip(sorted_ee_dirs, sorted_mm_dirs):
        if int(d_e.split('/')[1]) not in massesIn: continue
        if int(d_e.split('/')[1]) != mass: continue
        
        if 'high' in d_e and '450' in d_e:
            dirName = 'combinedCards_451'
        else:
            dirName = 'combinedCards_' + d_e.split('/')[1]

        if not os.path.exists(dirName):
            os.makedirs(dirName)

        print 'passed mass is', mass
        cp_ee = 'cp -r ' + d_e + '/{comb_,hh}* ' + dirName
        cp_mm = 'cp -r ' + d_m + '/{comb_,hh}* ' + dirName
        if trueRun:
            print
            print '-' * 50
            print 'copying data cards'
            print cp_ee
            subprocess.call(cp_ee, shell=True)
            print cp_mm
            subprocess.call(cp_mm, shell=True)

           
            if True:
                if True:
                    # combine SRs
                    os.chdir(dirName)
                    commandJoin_SRCombination = "combineCards.py ../" + d_e + '/dataCard_SR_hhMt.txt ../' + d_m + '/dataCard_SR_hhMt.txt  > comb_tot_SRCombination_M' + str(mass) + "_mc.txt"

                    ########### all regions
                    commandJoin_oneBinCombination = "combineCards.py comb_ee_oneBinCombination_M" + str(mass) + "_mc.txt comb_mm_oneBinCombination_M" + str(mass) + "_mc.txt > comb_tot_oneBinCombination_M" + str(mass) + "_mc.txt"

                    commandJoin_lowCombination = "combineCards.py comb_ee_lowCombination_M" + str(mass) + "_mc.txt comb_mm_lowCombination_M" + str(mass) + "_mc.txt > comb_tot_lowCombination_M" + str(mass) + "_mc.txt"

                    commandJoin_highCombination = "combineCards.py comb_ee_highCombination_M" + str(mass) + "_mc.txt comb_mm_highCombination_M" + str(mass) + "_mc.txt > comb_tot_highCombination_M" + str(mass) + "_mc.txt"

                    commandJoin_nominalCombination = "combineCards.py comb_ee_nominalCombination_M" + str(mass) + "_mc.txt comb_mm_nominalCombination_M" + str(mass) + "_mc.txt > comb_tot_nominalCombination_M" + str(mass) + "_mc.txt"


                    ############ CRDY and CRTT only
                    commandJoin_CRs_oneBinCombination = "combineCards.py comb_ee_CRs_oneBinCombination_M" + str(mass) + "_mc.txt comb_mm_CRs_oneBinCombination_M" + str(mass) + "_mc.txt > comb_tot_CRs_oneBinCombination_M" + str(mass) + "_mc.txt"

                    commandJoin_CRs_highCombination = "combineCards.py comb_ee_CRs_highCombination_M" + str(mass) + "_mc.txt comb_mm_CRs_highCombination_M" + str(mass) + "_mc.txt > comb_tot_CRs_highCombination_M" + str(mass) + "_mc.txt"

                    commandJoin_CRs_lowCombination = "combineCards.py comb_ee_CRs_lowCombination_M" + str(mass) + "_mc.txt comb_mm_CRs_lowCombination_M" + str(mass) + "_mc.txt > comb_tot_CRs_lowCombination_M" + str(mass) + "_mc.txt"

                    commandJoin_CRs_nominalCombination = "combineCards.py comb_ee_CRs_nominalCombination_M" + str(mass) + "_mc.txt comb_mm_CRs_nominalCombination_M" + str(mass) + "_mc.txt > comb_tot_CRs_nominalCombination_M" + str(mass) + "_mc.txt"

                    joinAllList = [
                        commandJoin_SRCombination,
                        commandJoin_oneBinCombination,
                        commandJoin_lowCombination,
                        commandJoin_highCombination,
                        commandJoin_nominalCombination
                    ]

                    joinCRsList = [
                        commandJoin_CRs_oneBinCombination,
                        commandJoin_CRs_lowCombination,
                        commandJoin_CRs_highCombination,
                        commandJoin_CRs_nominalCombination

                    ]

                    # print
                    # print 'cpList:', cpList
                    # sys.exit(1)

                    algoSpeedUp = ' --X-rtd MINIMIZER_analytic ' if addMC else ''

                    commandFit_Asymp_oneBinCombination = 'combine -M Asymptotic -v 3 --run blind ' + algoSpeedUp + ' -m ' + str(mass) + ' ' + 'comb_tot_oneBinCombination_M' + str(mass) + '_mc.txt >& log_comb_tot_oneBinCombination_M' + str(mass) + '_mc.txt'

                    commandFit_Asymp_lowCombination = 'combine -M Asymptotic -v 3 --run blind ' + algoSpeedUp + ' -m ' + str(mass) + ' ' + 'comb_tot_lowCombination_M' + str(mass) + '_mc.txt >& log_comb_tot_lowCombination_M' + str(mass) + '_mc.txt'

                    commandFit_Asymp_highCombination = 'combine -M Asymptotic -v 3 --run blind ' + algoSpeedUp + ' -m ' + str(mass) + ' ' + 'comb_tot_highCombination_M' + str(mass) + '_mc.txt >& log_comb_tot_highCombination_M' + str(mass) + '_mc.txt'

                    commandFit_Asymp_nominalCombination = 'combine -M Asymptotic -v 3 --run blind ' + algoSpeedUp + ' -m ' + str(mass) + ' ' + 'comb_tot_nominalCombination_M' + str(mass) + '_mc.txt >& log_comb_tot_nominalCombination_M' + str(mass) + '_mc.txt'

                    asympList = [
                        commandFit_Asymp_oneBinCombination,
                        commandFit_Asymp_lowCombination,
                        commandFit_Asymp_highCombination,
                        commandFit_Asymp_nominalCombination
                    ]

                    if int(str(mass)) < 600:
                        range_ = ' --rMin -1000 --rMax 1000 '
                    else:
                        range_ = ' --rMin -100 --rMax 100 '



                    ######15 ML fits:
                    # DY
                    commandFit_ML_DY_nominal ='combineCards.py ../' + d_e + '/dataCard_CRDY_hhMt_mc.txt ../' + d_m + '/dataCard_CRDY_hhMt_mc.txt > comb_tot_dataCard_CRDY_hhMt_mc.txt && combine -M MaxLikelihoodFit -v 3 ' + algoSpeedUp + ' -m ' + str(mass) + range_ + ' ' + 'comb_tot_dataCard_CRDY_hhMt_mc.txt >& log_comb_tot_dataCard_CRDY_hhMt_ML_DY_mc.txt'
                    commandFit_ML_DY_low ='combineCards.py ../' + d_e + '/dataCard_CRDYlow_hhMt_mc.txt ../' + d_m + '/dataCard_CRDYlow_hhMt_mc.txt > comb_tot_dataCard_CRDYlow_hhMt_mc.txt && combine -M MaxLikelihoodFit -v 3 ' + algoSpeedUp + ' -m ' + str(mass) + range_ + ' ' + 'comb_tot_dataCard_CRDYlow_hhMt_mc.txt >& log_comb_tot_dataCard_CRDYlow_hhMt_ML_DY_mc.txt'

                    commandFit_ML_DY_high ='combineCards.py ../' + d_e + '/dataCard_CRDYhigh_hhMt_mc.txt ../' + d_m + '/dataCard_CRDYhigh_hhMt_mc.txt > comb_tot_dataCard_CRDYhigh_hhMt_mc.txt && combine -M MaxLikelihoodFit -v 3 ' + algoSpeedUp + ' -m ' + str(mass) + range_ + ' ' + 'comb_tot_dataCard_CRDYhigh_hhMt_mc.txt >& log_comb_tot_dataCard_CRDYhigh_hhMt_ML_DY_mc.txt'
                    if mass == 1000: algoSpeedUp = ''
                    commandFit_ML_DY_oneBin ='combineCards.py ../' + d_e + '/dataCard_CRDYoneBin_hhMt_mc.txt ../' + d_m + '/dataCard_CRDYoneBin_hhMt_mc.txt > comb_tot_dataCard_CRDYoneBin_hhMt_mc.txt && combine -M MaxLikelihoodFit -v 3 ' + algoSpeedUp + ' -m ' + str(mass) + range_ + ' ' + 'comb_tot_dataCard_CRDYoneBin_hhMt_mc.txt >& log_comb_tot_dataCard_CRDYoneBin_hhMt_ML_DY_mc.txt'
                    algoSpeedUp = ' --X-rtd MINIMIZER_analytic ' if addMC else ''
                    # TT 
                    TTparam = ' --robustFit=1 '
                    #DO NOT USE algoSpeedUp, it gives :
                    # Skipping r. Parameter not found in the RooFitResult.  *** Break *** segmentation violation
                    # also, add --robustFit=1 that will do a tiny! slower but maybe? more robust likelihood scan
                    # use not txt datacard but root file workspace created with text2workspace.py

                    commandFit_ML_TT_oneBin = 'combineCards.py ../' + d_e + '/dataCard_CRTToneBin_hhMt_mc.txt ../' + d_m + '/dataCard_CRTToneBin_hhMt_mc.txt > comb_tot_dataCard_CRTToneBin_hhMt_mc.txt && text2workspace.py comb_tot_dataCard_CRTToneBin_hhMt_mc.txt && combine -M MaxLikelihoodFit -v 3 ' + TTparam + ' -m ' + str(mass) + range_ + ' ' + '-d comb_tot_dataCard_CRTToneBin_hhMt_mc.root >& log_comb_tot_dataCard_CRTToneBin_hhMt_ML_TT_mc.txt'


                    if mass >= 450: TTparam += algoSpeedUp 
                    commandFit_ML_TT_nominal = 'combineCards.py ../' + d_e + '/dataCard_CRTT_hhMt_mc.txt ../' + d_m + '/dataCard_CRTT_hhMt_mc.txt > comb_tot_dataCard_CRTT_hhMt_mc.txt && text2workspace.py comb_tot_dataCard_CRTT_hhMt_mc.txt && combine -M MaxLikelihoodFit -v 3 ' + TTparam + ' -m ' + str(mass) + range_ + ' ' + '-d comb_tot_dataCard_CRTT_hhMt_mc.root >& log_comb_tot_dataCard_CRTT_hhMt_ML_TTnominal_mc.txt'

                    algoSpeedUp = ' --X-rtd MINIMIZER_analytic ' if addMC else ''                 

                    # SR
                    commandFit_ML_SR_nominal = 'combine -M MaxLikelihoodFit -v 3 ' + algoSpeedUp + ' -m ' + str(mass) + range_ + ' comb_tot_SRCombination_M' + str(mass) + '_mc.txt >& log_comb_tot_dataCard_SR_hhMt_ML_SRnominal_mc.txt'

                    # DY with TT
                    commandFit_ML_DYnTT_low = 'combineCards.py comb_tot_dataCard_CRTT_hhMt_mc.txt comb_tot_dataCard_CRDYlow_hhMt_mc.txt > comb_tot_CRs_lowCombination_M' + str(mass) + '_mc.txt && combine -M MaxLikelihoodFit -v 3 ' + algoSpeedUp + ' -m ' + str(mass) + range_ + ' ' + 'comb_tot_CRs_lowCombination_M' + str(mass) + '_mc.txt >& log_comb_tot_CRs_lowCombination_M' + str(mass) + '_ML_mc.txt '

                    commandFit_ML_DYnTT_high = 'combineCards.py comb_tot_dataCard_CRTT_hhMt_mc.txt comb_tot_dataCard_CRDYhigh_hhMt_mc.txt > comb_tot_CRs_highCombination_M' + str(mass) + '_mc.txt && combine -M MaxLikelihoodFit -v 3 ' + algoSpeedUp + ' -m ' + str(mass) + range_ + ' ' + 'comb_tot_CRs_highCombination_M' + str(mass) + '_mc.txt >& log_comb_tot_CRs_highCombination_M' + str(mass) + '_ML_mc.txt '

                    commandFit_ML_DYnTT_oneBin = 'combineCards.py comb_tot_dataCard_CRTToneBin_hhMt_mc.txt comb_tot_dataCard_CRDYoneBin_hhMt_mc.txt > comb_tot_CRs_oneBinCombination_M' + str(mass) + '_mc.txt && combine -M MaxLikelihoodFit -v 3 ' + algoSpeedUp + ' -m ' + str(mass) + range_ + ' ' + 'comb_tot_CRs_oneBinCombination_M' + str(mass) + '_mc.txt >& log_comb_tot_CRs_oneBinCombination_M' + str(mass) + '_ML_mc.txt '
                    if mass <450: algoSpeedUp = ' '
                    
                    commandFit_ML_DYnTT_nominal = 'combineCards.py comb_tot_dataCard_CRTT_hhMt_mc.txt comb_tot_dataCard_CRDY_hhMt_mc.txt > comb_tot_CRs_nominalCombination_M' + str(mass) + '_mc.txt && combine -M MaxLikelihoodFit -v 3 ' + algoSpeedUp + ' -m ' + str(mass) + range_ + ' ' + 'comb_tot_CRs_nominalCombination_M' + str(mass) + '_mc.txt >& log_comb_tot_CRs_nominalCombination_M' + str(mass) + '_ML_mc.txt '
                    
                    algoSpeedUp = ' --X-rtd MINIMIZER_analytic ' if addMC else ''                    


                    # all regions
                    commandFit_ML_lowCombination = 'combine -M MaxLikelihoodFit -v 3 ' + algoSpeedUp + ' -m ' + str(mass) + range_ + ' ' + 'comb_tot_lowCombination_M' + str(mass) + '_mc.txt >& log_comb_tot_lowCombination_M' + str(mass) + '_ML_mc.txt '
                    commandFit_ML_highCombination = 'combine -M MaxLikelihoodFit -v 3 ' + algoSpeedUp + ' -m ' + str(mass) + range_ + ' ' + 'comb_tot_highCombination_M' + str(mass) + '_mc.txt >& log_comb_tot_highCombination_M' + str(mass) + '_ML_mc.txt '
                    commandFit_ML_oneBinCombination = 'combine -M MaxLikelihoodFit -v 3 ' + algoSpeedUp + ' -m ' + str(mass) + range_ + ' ' + 'comb_tot_oneBinCombination_M' + str(mass) + '_mc.txt >& log_comb_tot_oneBinCombination_M' + str(mass) + '_ML_mc.txt '
                    commandFit_ML_nominalCombination = 'combine -M MaxLikelihoodFit -v 3 ' + algoSpeedUp + ' -m ' + str(mass) + range_ + ' ' + 'comb_tot_nominalCombination_M' + str(mass) + '_mc.txt >& log_comb_tot_nominalCombination_M' + str(mass) + '_ML_mc.txt '

                    mlList = [
                        commandFit_ML_DY_nominal,
                        commandFit_ML_DY_low,
                        commandFit_ML_DY_high,
                        commandFit_ML_DY_oneBin,

                        commandFit_ML_TT_nominal,
                        commandFit_ML_TT_oneBin,

                        commandFit_ML_SR_nominal,

                        commandFit_ML_DYnTT_nominal,
                        commandFit_ML_DYnTT_low,
                        commandFit_ML_DYnTT_high,
                        commandFit_ML_DYnTT_oneBin,

                        commandFit_ML_lowCombination,
                        commandFit_ML_highCombination,
                        commandFit_ML_oneBinCombination,
                        commandFit_ML_nominalCombination
                    ]
                    if trueRun:
                        print
                        print '-' * 50

                        #print 'copying data cards'
                        #for cp in cpList:
                         #   print 'doing', cp
                            #subprocess.call(cp, shell=True)
                        print
                        print '-' * 50

                        print
                        "join all region dc's"
                        for jA in joinAllList:
                            print 'doing', jA
                            subprocess.call(jA, shell=True)
                        print
                        print '-' * 50

                        print "join CR region dc's"
                        for jCRs in joinCRsList:
                            print 'doing', jCRs
                            subprocess.call(jCRs, shell=True)
                        print
                        print '-' * 50

                        print "fit asymptotic"
                        for a in asympList:
                            print 'doing', a
                            subprocess.call(a, shell=True)
                        print
                        print '-' * 50

                        print "fit maxLikelihood"
                        for ml in mlList:
                            print 'doing', ml
                            subprocess.call(ml, shell=True)
                            
                        print 'change dir to', curDir
                        os.chdir(curDir)
                #print '=' * 50
                #logList.append(logList_perMass)





def extractLimits():
    # if run_combine_and_copy_cards: time.sleep(15)
    # if copy_logs:
    #     print
    #     '\/' * 50
    #     #for log_per_mass, mass in itertools.izip_longest(logList, massesIn):
    #     for idx, mass in enumerate(massesIn):
    #         #print 'log_per_mass is ', log_per_mass
    #         logPath = leptType + 'logs_' + str(mass)  # + '_' + directo #+ '_' + str(log_per_mass.split('_')[-1])
    #         if mass and not os.path.exists(logPath):
    #             os.makedirs(logPath)
    #         print 'logPath is ', logPath
    #         print
    #         'before loop over log_per_mass'
    #         for log in log_per_mass:
    #             print 'log is', log
    #             # if len(str(log)) > 30: continue
    #             # if mass <= 450 and '_0.9' in log: continue # bdt at +0.9 exists only for high mass region
    #             # cpLog = 'cp -r ../' + str(log) + ' ' + logPath
    #             cpLog = 'cp -r ' + str(log) + ' ' + logPath
    #             print 'cpLog is', cpLog
    #             print '*' * 50
    #             print
    #             if cpLogs:
    #                 subprocess.call(cpLog, shell=True)


    limits = []
    print 'DIRECTORY contains:';
    print glob.glob(leptType + "log*")
    for root, dirs, files in os.walk('.'):
        #     #print 'root={0}, dirs={1}, files={2}'.format(root, dirs, files)
        if 'logs' not in root: continue  # or 'makeDataCards/' not in root: continue

        #     #print 'root={0}, dirs={1}'.format(root, dirs)
        print 'root is ', root

        # # root is  ./low_SR_-0.9/plots/makeDataCards/260
        # # root is  ./low_SR_-0.9/plots/makeDataCards/400
        # # root is  ./low_SR_-0.8/plots/makeDataCards/260
        # # root is  ./low_SR_-0.8/plots/makeDataCards/400

        for fil in files:

            if not fil.endswith('txt') or 'log' not in fil: continue
            if leptType not in str(str(root) + '/' + fil): continue
            if fil[4:6] not in ['ee', 'mm']: continue
            # if not fil.endswith('txt'): continue
            # if len(str(fil)) > 30: continue
            if os.path.getsize(str(root) + '/' + fil) < 10000: continue  # to skip corrupted/incomplete logs with errors
            print
            print 'For file', fil
            print 'size is:'
            print os.path.getsize(str(root) + '/' + fil)
            if '_ML' in str(root) + '/' + fil: continue
            with io.open(str(root) + '/' + fil, mode='r') as f:

                print 'Full file name is', str(root) + '/' + fil
                text = f.read()
                tmp_limits = re.findall(r"r < (\d*\.\d+|\d+)", text)
                # ['0xxx', '0.0755', '0.1009', '0.1411', '0.1990', '0.2700']
                # obs       2.5%      16%       50%      84%      97.5%
                limits.append((tmp_limits[-5:], fil.split('_')[2][1:], fil.split('_')[-1][:-4]))

                #         ONLY expected limits        mass              bdt cut value

                #  Example:
                # Expected  2.5%: r < 0.0755   -2 sigma
                # Expected 16.0%: r < 0.1009   -1 sigma
                # Expected 50.0%: r < 0.1411    limit
                # Expected 84.0%: r < 0.1990   +1 sigma
                # Expected 97.5%: r < 0.2700   +2 sigma
    print
    print 'limits are:'
    pp.pprint(limits)
    # with io.open ('limits.txt', mode='w') as f:
    if len(directo) > 3:
        directo = '_' + directo
    else:
        directo = ''
    with io.open('limits_' + leptType + directo + '.txt', 'wb') as fp:
        pickle.dump(limits, fp)

    # #To read it back:
    # with open ('limits.txt', 'rb') as fp:
    #     itemlist = pickle.load(fp)





def main(args):
    print 'in main'
    start_time = time.time()
    global leptType 
    leptType = args.leptType
    p = Pool(len(massesIn))
    print 'p=', p
    #listOfLists = [[massesIn[x]] for x in range(len(massesIn))]
    #print type(listOfLists)
    print 'type(massesIn), massesIn:', type(massesIn), massesIn
    print 'type(runFit), runFit:', type(runFit), runFit
    
    #p.map(runFit, massesIn)
    
    p.map(createCombined, massesIn)
    


    #print 'loglist is'
    #pp.pprint(logList)

    end_time = time.time()
    time_taken = end_time - start_time  # time_taken is in seconds

    hours, rest = divmod(time_taken, 3600)
    minutes, seconds = divmod(rest, 60)
    print
    print "---it took {hours} hours, {minutes} minutes and {seconds:.1f} seconds to run the analysis ---".format(hours=hours,
                                                                                                           minutes=minutes,
                                                                                                           seconds=seconds)
    #    sys.exit(1)
    #extractLimits()


if __name__ == "__main__":

#use %% below and not just %, otherwise python raises ValueError: unsupported format character 'p' (0x70) at index 6
    usage = """
    %%prog [options]
    Run Asymptotic and ML fits on ee and mm directories separately,
    store results in log files.
    """
    print 'before parser'
    parser = argparse.ArgumentParser(usage=usage)
    #parser = OptionParser(usage=usage)
    parser.add_argument("--leptType",  default=None,
                        #if you use leptT or any other substring of leptType, that would work too!
                      help="Which channels to run: ee_ or mm_", choices=['ee_', 'mm_'])
    #(options, args) = parser.parse_args()
    print 'after parser'
    args = parser.parse_args()

    sys.exit(main(args))

