import subprocess
import time, os
import sys
import itertools
import multiprocessing
import glob



channel = glob.glob("comb_*")[0].split('_')[1]
mass = [f for f in glob.glob("comb_*") if 'CR' not in f][0].split('_')[3][1:]
range_ = ' --rMin -1000 --rMax 1000 ' if mass > 450 else  ' --rMin -100 --rMax 100 '

variables = [
    
    # "bdt_response",
    # #"bdt_response_afterCut",
    # "dR_bjets",
    # "dR_leps",
    # "hhMt",
    # #"hhMt_mc",
    # "hmass0",
    # "hmass1",
    # #"hmass1_oneBin",
    # "hpt0",
    # "hpt1",
    # "met_pt",
    "zmass",
    # #"zmass_high",
    # #"zmass_oneBin",
    # "zpt0"
    ]

#variables = [ "hmass1"]


def producePostFitRootFiles(var):
    cardCRTT = 'dataCard_CRTT_%s.txt' % var
    cardCRTTmc = 'dataCard_CRTT_%s_mc.txt' % var

    cardCRDY = 'dataCard_CRDY_%s.txt' % var
    cardCRDYmc = 'dataCard_CRDY_%s_mc.txt' % var

    cardSR = 'dataCard_SR_%s.txt' % var
    cardSRmc = 'dataCard_SR_%s_mc.txt' % var


    cpSR = " cp " + cardSR + " " + cardSRmc + """ && echo "" >> """ + cardSRmc + """ && echo "* autoMCStats 0" >> """ + cardSRmc + " && text2workspace.py " + cardSRmc

    cpCRDY = " cp " + cardCRDY + " " + cardCRDYmc + """ && echo "" >> """ + cardCRDYmc + """ && echo "* autoMCStats 0" >> """ + cardCRDYmc + " && text2workspace.py " + cardCRDYmc
    
    cpCRTT = " cp " + cardCRTT + " " + cardCRTTmc + """ && echo "" >> """ + cardCRTTmc + """ && echo "* autoMCStats 0" >> """ + cardCRTTmc + " && text2workspace.py " + cardCRTTmc

    print
    print 'cpCRDY', cpCRDY
    print 'cpCRTT', cpCRTT
    print 'cpSR', cpSR
    subprocess.call(cpSR, shell=True) 
    subprocess.call(cpCRDY, shell=True) 
    subprocess.call(cpCRTT, shell=True) 
    
    #add mc to the worskpace card
    topostfitDY = 'PostFitShapesFromWorkspace -d ' + cardCRDYmc + ' -w ' + cardCRDYmc[:-4] + '.root -o ' + channel + '_' + var + '_CRDY_postfit.root -m ' + mass + ' -f fitDiagnostics.root:fit_s --postfit --sampling --print'
    print 'topostfitDY', topostfitDY

    topostfitTT = 'PostFitShapesFromWorkspace -d ' + cardCRTTmc + ' -w ' + cardCRTTmc[:-4] + '.root -o ' + channel + '_' + var + '_CRTT_postfit.root -m ' + mass + ' -f fitDiagnostics.root:fit_s --postfit --sampling --print'
    print 'topostfitTT', topostfitTT    

    topostfitSR = 'PostFitShapesFromWorkspace -d ' + cardSRmc + ' -w ' + cardSRmc[:-4] + '.root -o ' + channel + '_' + var + '_SR_postfit.root -m ' + mass + ' -f fitDiagnostics.root:fit_s --postfit --sampling --print'
    print 'topostfitSR', topostfitSR


    print '-'*50
    subprocess.call(topostfitSR, shell=True) 
    subprocess.call(topostfitDY, shell=True) 
    subprocess.call(topostfitTT, shell=True) 
    ####for now do only DY
    print '\n'*10


def main():
    print 'starting '
    start_time = time.time()
    

    fit = 'combine -M MaxLikelihoodFit -v 3  --X-rtd MINIMIZER_analytic  --saveShapes --saveWithUncertainties -m ' + mass + range_ + ' comb_' + channel + '_nominalCombination_M' + mass + '_mc.txt' 
    
    #print 'fit', fit
    #subprocess.call(fit, shell=True)    

    pool = multiprocessing.Pool(16)  #32          
    pool.map(producePostFitRootFiles, variables)

    end_time = time.time()
    time_taken = end_time - start_time # time_taken is in seconds                                

    hours, rest = divmod(time_taken,3600)
    minutes, seconds = divmod(rest, 60)
    print
    print 'all done!'
    print "---it took {hours} hours, {minutes} minutes and {seconds:.1f} seconds to run the analysis ---".format (hours=hours, minutes=minutes, seconds=seconds)
    #raw_input("Press Enter to exit...")


if __name__ == '__main__':
    sys.exit(main())



