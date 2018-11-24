import shutil
import subprocess
import glob

useAlgo = True # --X-rtd MINIMIZER_analytic
trueRun = False

datacards = ['dataCard_CRDY_hhMt.txt', 'dataCard_SR_hhMt.txt' ,'dataCard_CRTT_hhMt.txt'] 

#back up initial data cards
for dc in datacards:
    new_dc = 'copy_' + dc
    shutil.copyfile (dc, new_dc)
    cmd = 'python DataCardsREwriter_v2.py -i ' + new_dc + ' -o noSignal_' + dc
    print 'cmd', cmd
    if trueRun: subprocess.call(cmd, shell=True)



comb_CRDYnSR = "combineCards.py noSignal_dataCard_CRDY_hhMt.txt noSignal_dataCard_SR_hhMt.txt > noSignal_dataCard_CRDYnSR_hhMt.txt"
comb_CRTTnSR = "combineCards.py noSignal_dataCard_CRTT_hhMt.txt noSignal_dataCard_SR_hhMt.txt > noSignal_dataCard_CRTTnSR_hhMt.txt"
comb_CRDYnCRTT = "combineCards.py noSignal_dataCard_CRDY_hhMt.txt noSignal_dataCard_CRTT_hhMt.txt > noSignal_dataCard_CRDYnTT_hhMt.txt"
comb_CRsnSR = "combineCards.py CRDY=noSignal_dataCard_CRDY_hhMt.txt SR=noSignal_dataCard_SR_hhMt.txt CRTT=noSignal_dataCard_CRTT_hhMt.txt > noSignal_dataCard_all_hhMt.txt"

print 
#combine cards for various regions
for cmd in comb_CRDYnSR, comb_CRTTnSR, comb_CRDYnCRTT, comb_CRsnSR:
    print 'cmd', cmd
    if trueRun: subprocess.call(cmd, shell=True)
    
print
all_dc = glob.glob('noSignal_*txt')
#add BBB uncertainty to data cards
for dc in all_dc:#[0:1]:
    print 'processing', dc
    cmd = 'echo "" >> ' + dc + ' && echo "* autoMCStats 0" >> ' + dc
    print 'cmd', cmd
    if trueRun: subprocess.call(cmd, shell=True)
    algo = ' --X-rtd MINIMIZER_analytic ' if useAlgo else ''
    fitCmd = 'text2workspace.py --X-allow-no-signal ' + dc + ' && combine -M MaxLikelihoodFit  -m 350  --rMin -100 --rMax 100  -v 3 ' + algo +  dc.replace('txt', 'root') + ' >& log_' + dc 
    print 'fitCmd', fitCmd
    if trueRun: subprocess.call(fitCmd, shell=True)
    
