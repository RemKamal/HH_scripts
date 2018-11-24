import subprocess
import time, os
import sys
import itertools
import multiprocessing
import glob
import shutil


CRs_postfit = False #True
#means all_regions_postfit = False and vice verse

trueRun = True
channel = glob.glob("hh*eff_e_*")
if channel != [] and channel != None:
    channel = 'ee' #comb_*")[0].split('_')[1]
else:
    channel = 'mm'

mass = str(350) #[f for f in glob.glob("comb_*") if 'CR' not in f][0].split('_')[3][1:]
range_ = ' --rMin -1000 --rMax 1000 ' if mass < 450 else  ' --rMin -100 --rMax 100 '

CRDY_type = glob.glob("dataCard_CRDY*hh*")[0].split('_')[1]

variables = [
    # "bdt_response",
    # "bdt_response_afterCut",
    # "dR_bjets",
    # "dR_leps",
    "hhMt",
    # "hmass0",
    # "hmass1",
    # "hmass1_oneBin",
    # "hpt0",
    # "hpt1",
    # "met_pt",
    # "zmass",
    # "zmass_high",
    # "zmass_oneBin",
    # "zpt0"
]



def producePostFitRootFiles(var):
    cardCRTT = 'dataCard_CRTT_%s.txt' % var
    cardCRTTmc = 'dataCard_CRTT_%s_mc.txt' % var

    cardCRDY = 'dataCard_' + CRDY_type + '_%s.txt' % var
    cardCRDYmc = 'dataCard_' + CRDY_type + '_%s_mc.txt' % var

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
    fitFile = 'fitDiagnostics_CRs.root' if CRs_postfit else 'fitDiagnostics_all.root'

    topostfitDY = 'PostFitShapesFromWorkspace -d ' + cardCRDYmc + ' -w ' + cardCRDYmc[:-4] + '.root -o ' + channel + '_' + var + '_' + CRDY_type + '_postfit.root -m ' + mass + ' -f ' + fitFile + ':fit_s --postfit --sampling --print'
    print 'topostfitDY', topostfitDY

    topostfitTT = 'PostFitShapesFromWorkspace -d ' + cardCRTTmc + ' -w ' + cardCRTTmc[:-4] + '.root -o ' + channel + '_' + var + '_CRTT_postfit.root -m ' + mass + ' -f ' + fitFile + ':fit_s --postfit --sampling --print'
    print 'topostfitTT', topostfitTT    

    topostfitSR = 'PostFitShapesFromWorkspace -d ' + cardSRmc + ' -w ' + cardSRmc[:-4] + '.root -o ' + channel + '_' + var + '_SR_postfit.root -m ' + mass + ' -f ' + fitFile + ':fit_s --postfit --sampling --print'
    print 'topostfitSR', topostfitSR


    print '-'*50
    subprocess.call(topostfitSR, shell=True) 
    subprocess.call(topostfitDY, shell=True) 
    subprocess.call(topostfitTT, shell=True) 
    ####for now do only DY
    print '\n'*10




def copyAndCombineCards():
    datacards = ['dataCard_' + CRDY_type + '_hhMt.txt', 'dataCard_SR_hhMt.txt' ,'dataCard_CRTT_hhMt.txt']

    #back up initial data cards                                                                                       
    for dc in datacards:
        new_dc = 'copy_' + dc
        shutil.copyfile (dc, new_dc)
    

    comb_CRDYnCRTT = "combineCards.py copy_dataCard_" + CRDY_type + "_hhMt.txt copy_dataCard_CRTT_hhMt.txt > copy_dataCard_" + CRDY_type + "nTT_hhMt.txt"
    comb_CRsnSR = "combineCards.py CRDY=copy_dataCard_" + CRDY_type + "_hhMt.txt SR=copy_dataCard_SR_hhMt.txt CRTT=copy_dataCard_CRTT_hhMt.txt > copy_dataCard_all_hhMt.txt"

    print
#combine cards for various regions                                                                                
    for cmd in comb_CRDYnCRTT, comb_CRsnSR:
        print 'cmd=', cmd
        if trueRun: subprocess.call(cmd, shell=True)


    all_dc = glob.glob('copy_*txt')
#add BBB uncertainty to data cards                                                                                
    for dc in all_dc:#[0:1]:                                                                                          
        print 'processing', dc
        cmd = 'echo "" >> ' + dc + ' && echo "* autoMCStats 0" >> ' + dc
        print 'cmd', cmd
        if trueRun: subprocess.call(cmd, shell=True)

        
def doFits():
    #--saveShapes
    fit_CRs = 'combine -M MaxLikelihoodFit -v 3  --X-rtd MINIMIZER_analytic  --saveNormalizations --saveWithUncertainties -m ' + mass + range_ + 'copy_dataCard_' + CRDY_type + 'nTT_hhMt.txt' #   ' comb_' + channel + '_nominalCombination_M' + mass + '_mc.txt' 

    fit_all = 'combine -M MaxLikelihoodFit -v 3  --X-rtd MINIMIZER_analytic  --saveNormalizations --saveWithUncertainties -m ' + mass + range_ + 'copy_dataCard_all_hhMt.txt' #   ' comb_' + channel + '_nominalCombination_M' + mass + '_mc.txt' 
    
    #for fit in fit_CRs, fit_all:
    print 'fit=', fit_CRs
    subprocess.call(fit_CRs, shell=True)    
    shutil.move("fitDiagnostics.root", "fitDiagnostics_CRs.root")
    
    print 'fit=', fit_all
    subprocess.call(fit_all, shell=True)
    shutil.move("fitDiagnostics.root", "fitDiagnostics_all.root")




def main():
    print 'starting '
    start_time = time.time()
    

    #copyAndCombineCards()
    #doFits()

    #return 
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



