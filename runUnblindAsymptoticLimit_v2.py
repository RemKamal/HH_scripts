import subprocess
import glob
import os
import sys
# run this script after combinedCards directories are ready, meaning after "createBDTvsLimitPlot_v4_4.py"

addMC = True
RunBlind = False
runBlind = " --run blind " if RunBlind else ""
dotxt2ws=True
trueRun = True

combineCards=True
curDir = os.getcwd()
algoSpeedUp = ' --X-rtd MINIMIZER_analytic ' if addMC else ''
#algoSpeedUp += " --cminDefaultMinimizerStrategy 2 --robustFit 1 "
masses_of_interest = [260, 270, 300, 350, 400, 451, 600, 650, 900, 1000]
masses_of_interest = [250, 260, 270, 300, 350, 400, 450, 451, 500, 550, 600, 650, 700, 750, 800, 900, 1000]
masses_of_interest = [450]
date = 'june4_'
studyLimitVariations=False#True
allowedVariationsList = [5] if studyLimitVariations else None


def createCombinedAreas():
    eles = glob.glob(date+"eles*") if not studyLimitVariations else glob.glob("*/"+date+"eles*")
    muons = glob.glob(date+"muons*") if not studyLimitVariations else glob.glob("*/"+date+"muons*")
    for d_e, d_m in zip(sorted(eles), sorted(muons)):
        print 'd_m', d_m
        print 'd_e', d_e
        mass = int(d_m.split('_')[-1])
        tmp_pref = d_e.split('/')[0]
        pref = int(d_e.split('/')[0]) if tmp_pref.isdigit() else None
        
        if pref and studyLimitVariations and pref in allowedVariationsList:
            combPath = str(pref) + "/combinedCards_" + str(mass)
        else:
            combPath = "combinedCards_" + str(mass)
        if not os.path.exists(combPath):
            os.makedirs(combPath)
            
        cpEleData ='cp %s/*hhMt_ee*{txt,root} %s' % (d_e, combPath)
        cpMuonData='cp %s/*hhMt_mm*{txt,root} %s' % (d_m, combPath)
        
        if trueRun:
            subprocess.call(cpEleData, shell=True)
            subprocess.call(cpMuonData, shell=True)



def fitChannelsIndividually():
    eles = glob.glob(date+"eles*") if not studyLimitVariations else glob.glob("*/"+date+"eles*")
    muons = glob.glob(date+"muons*") if not studyLimitVariations else glob.glob("*/"+date+"muons*") 
    for d_e, d_m in zip(sorted(eles), sorted(muons)):
        if studyLimitVariations and int(d_e.split('/')[0]) not in allowedVariationsList:
            continue
        print 'd_m', d_m
        print 'd_e', d_e
        mass_ee = int(d_e.split('_')[-1])
        mass_mm = int(d_m.split('_')[-1])
        if mass_ee != mass_mm:
            print 'check the mass, exiting...'
            sys.exit(1)
        mass = mass_mm
        if mass not in masses_of_interest:
            continue
        #channel = d_m.split('_')[-2]
        #channel = "ee" if channel == "eles" else "mm" if channel == "muons" else None
        #if channel == None:
         #   print 'check channel, exiting...'
          #  sys.exit(1)

        extra = ""
        range_ = ' --rMin -1000 --rMax 1000 ' if int(mass) <= 451 else ' --rMin -100 --rMax 100 '
        
        #cpEleData ='cp %s/*hhMt_ee*{txt,root} %s' % (d_e, combPath)
        #cpMuonData='cp %s/*hhMt_mm*{txt,root} %s' % (d_m, combPath)
        
        if trueRun:
            for d in d_e, d_m:
                channel = d.split('_')[-2]  
                channel = "ee" if channel == "eles" else "mm" if channel == "muons" else None                                                                    
                if channel == None: 
                    print 'check channel, exiting...'                                                                                                          
                    sys.exit(1) 
                os.chdir(d)
                fit_t2w = 'text2workspace.py copy_dataCard_all_hhMt.txt'
                print 'fit_t2w', fit_t2w
        
                fit_all_run ='combine -M MaxLikelihoodFit -v 3  --X-rtd MINIMIZER_analytic  --cminDefaultMinimizerStrategy 0 ' + extra + ' --saveShapes --saveNormalizations --saveWithUncertainties -m ' + str(mass) + range_ + 'copy_dataCard_all_hhMt.root >& log_fit_all_%s.txt' % channel
                #print 'fit_all_run', fit_all_run

                fit_asymptotic = 'combine -M Asymptotic -v 3 --X-rtd MINIMIZER_analytic  --cminDefaultMinimizerStrategy 0 ' + extra + range_ + ' -m ' + str(mass) + ' ' + 'copy_dataCard_all_hhMt.root >& log_fit_all_asymptotic_%s.txt' % channel
                print 'fit_asymptotic', fit_asymptotic
                
                subprocess.call(fit_t2w, shell=True)
                #subprocess.call(fit_all_run, shell=True)
                subprocess.call(fit_asymptotic, shell=True)

                os.chdir(curDir)




def rebinChannels():
    for d_e, d_m in zip(glob.glob(date+"eles*"), glob.glob(date+"muons*")):
        print 'd_e', d_e
        print 'd_m', d_m

        mass = int(d_m.split('_')[-1])
        if mass not in masses_of_interest:
            continue
        combPath = "combinedCards_" + str(mass)

        os.chdir(d_e)
        runRebin ='cp ../modifyAndPutTogetherHistsInRoots.py . && python modifyAndPutTogetherHistsInRoots.py'
        if trueRun:
            subprocess.call(runRebin, shell=True)

        os.chdir(curDir + '/' + d_m)
        runRebin ='cp ../modifyAndPutTogetherHistsInRoots.py . && python modifyAndPutTogetherHistsInRoots.py'
        if trueRun:
                subprocess.call(runRebin, shell=True)
        os.chdir(curDir)
        cpEleData ='cp %s/*hhMt_ee*{txt,root} %s' % (d_e, combPath)
        cpMuonData='cp %s/*hhMt_mm*{txt,root} %s' % (d_m, combPath)

        if trueRun:
            subprocess.call(cpEleData, shell=True)
            subprocess.call(cpMuonData, shell=True)


def performRenamingOfNewRoots(dire):
    dirs = glob.glob(dire)
    #if dirs == []:
     #   for m in masses_of_interest:
    #os.makedirs(dire + )
    for d in dirs:
        print 'inside performRenamingOfNewRoots with passed in d=', d
        cmd = d + "*/new*.input.root"
        print 'cmd=', cmd
        files = glob.glob(cmd)
        print 'files=', files
        for f in files:
            print f
            mass = int(f.split('/')[-2].split('_')[-1])
            print 'mass=', mass
            if mass not in masses_of_interest:
                continue
            cmdRename = "mv %s %s" % (f, f.replace("new_", ""))
            print "cmdRename=", cmdRename
            if trueRun:
                subprocess.call(cmdRename, shell=True)

    
def runFits():
    dirs_comb = glob.glob("combinedCards_*") if not studyLimitVariations else glob.glob("*/combinedCards_*")
    for d in dirs_comb:
        if studyLimitVariations and int(d.split('/')[0]) not in allowedVariationsList:
            continue
        if 'txt' in d: continue
        print d
        mass = int(d.split('_')[-1])
        if mass not in masses_of_interest:
            continue
    #if int(mass) not in [450, 451]: continue
        os.chdir(d)
    
        rebin = ""
        
        range_ = ' --rMin -1000 --rMax 1000 ' if int(mass) <= 451 else ' --rMin -100 --rMax 100 '
# to run separately each channel individually
#commandFit_Asymp_nominalCombination = 'combine -M Asymptotic -v 3 ' + runBlind + algoSpeedUp + range_ + ' -m ' + str(mass) + ' ' + 'comb_' + leptType + 'nominalCombination_M' + str( mass) + '_mc.txt >& log_comb_' + leptType + 'nominalCombination_M' + str(mass) + '_mc.txt'
        commandJoin_nominalCombination = "combineCards.py dataCard_hhMt_ee.txt dataCard_hhMt_mm.txt  > comb_tot_nominalCombination_M"  + str(mass) + '_mc.txt && echo "" >> comb_tot_nominalCombination_M' + str(mass) + '_mc.txt && echo "* autoMCStats 0" >> comb_tot_nominalCombination_M'  + str(mass) + "_mc.txt " #text2workspace.py " + ' %s/comb_tot_nominalCombination_M' % combPath+ str(mass) + "_mc.txt"
        print 'commandJoin_nominalCombination=', commandJoin_nominalCombination
        if trueRun and combineCards:
            subprocess.call(commandJoin_nominalCombination, shell=True)


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
    #subprocess.call("find comb*/higgsCombineTest.Asymptotic* -exec cp {} . \;", shell=True)

def runCommand(cmds):
    for cmd in cmds:
        print 'cmd=', cmd
        if trueRun:
            subprocess.call(cmd, shell=True)


def copyHiggsRoots():
    if not studyLimitVariations:
        subprocess.call("find comb*/higgsCombineTest.Asymptotic* -exec cp {} . \;", shell=True)
    else:
        for d in glob.glob("*"):
            if not d.isdigit():
                continue
            if studyLimitVariations and int(d.split('/')[0]) not in allowedVariationsList:
                continue
            cmd = "find %s/comb*/higgsCombineTest.Asymptotic* -exec cp {} . \;" % d
            print 'cmd=', cmd
            subprocess.call(cmd, shell=True)

def someCopyCommands():
    #cmdMuon="cp ../may24/may24_muons_650/hhMt_mm_*input.root may24_muons_650/"
    #cmsEle="cp ../may24/may24_eles_650/hhMt_ee_*input.root may24_eles_650/"
    elePath = "limits_eles/"
    muonPath = "limits_muons/"
    if not os.path.exists(elePath):
        os.makedirs(elePath)

    if not os.path.exists(muonPath):
        os.makedirs(muonPath)

    if not studyLimitVariations:
        cmd_transferLimit_Muon="""find may*muons* -name "higgsCombineTest.Asymptotic.mH*root" -exec cp {} limits_muons \;"""
        cmd_transferLimit_Ele="""find may*eles* -name "higgsCombineTest.Asymptotic.mH*root" -exec cp {} limits_eles \;"""
        runCommand([cmd_transferLimit_Muon, cmd_transferLimit_Ele])
    else:
        dires = glob.glob("*")
        print 'dires=', dires
        for d in dires:
            print 'd=', d
            if not d.isdigit():
                continue
            if studyLimitVariations and int(d.split('/')[0]) not in allowedVariationsList:
                continue
            cmd_transferLimit_Muon="""find %s/may*muons* -name "higgsCombineTest.Asymptotic.mH*root" -exec cp {} limits_muons \;"""  % d
            cmd_transferLimit_Ele ="""find %s/may*eles* -name "higgsCombineTest.Asymptotic.mH*root" -exec cp {} limits_eles \;"""   % d
            runCommand([cmd_transferLimit_Muon, cmd_transferLimit_Ele])


if __name__ == "__main__":
    #performRenamingOfNewRoots("may24_*s_") if not studyLimitVariations else performRenamingOfNewRoots("*/may24_*s_")
    #fitChannelsIndividually()
    createCombinedAreas()
    #performRenamingOfNewRoots("combinedCards_") if not studyLimitVariations else performRenamingOfNewRoots("*/combinedCards_")
    runFits()
    #someCopyCommands()
    copyHiggsRoots()


#performRenamingOfNewRoots()

#rebinChannels()
