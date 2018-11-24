import subprocess
import glob
import os
# run this script after combinedCards directories are ready, meaning after "createBDTvsLimitPlot_v4_4.py"

addMC = True
RunBlind = False
runBlind = " --run blind " if RunBlind else ""
dotxt2ws=False
trueRun = False

algoSpeedUp = ' --X-rtd MINIMIZER_analytic ' if addMC else ''
#algoSpeedUp += " --cminDefaultMinimizerStrategy 2 --robustFit 1 "


for d in glob.glob("combinedCards_*"):
    if 'txt' in d: continue
    print d
    mass = d.split('_')[-1]
    #if int(mass) not in [450, 451]: continue
    os.chdir(d)
    


    range_ = ' --rMin -1000 --rMax 1000 ' if int(mass) <= 451 else ' --rMin -100 --rMax 100 '
# to run separately each channel individually
#commandFit_Asymp_nominalCombination = 'combine -M Asymptotic -v 3 ' + runBlind + algoSpeedUp + range_ + ' -m ' + str(mass) + ' ' + 'comb_' + leptType + 'nominalCombination_M' + str( mass) + '_mc.txt >& log_comb_' + leptType + 'nominalCombination_M' + str(mass) + '_mc.txt'
    txt2w = "text2workspace.py comb_tot_nominalCombination_M" + str(mass) + "_mc.txt "
    print txt2w
    commandFit_Asymp_nominalCombination = 'combine -M Asymptotic -v 3 ' + runBlind + algoSpeedUp + range_ + ' -m ' + str(mass) + ' ' + 'comb_tot_nominalCombination_M' + str(mass) + '_mc.txt >& log_comb_tot_nominalCombination_M' + str(mass) + '_mc.txt'
    print commandFit_Asymp_nominalCombination
    if trueRun:
        if dotxt2ws:
            subprocess.call(txt2w, shell=True)
        subprocess.call(commandFit_Asymp_nominalCombination, shell=True)
    print 
    os.chdir("../")


subprocess.call("find comb*/higgsCombineTest.Asymptotic* -exec cp {} . \;", shell=True)
