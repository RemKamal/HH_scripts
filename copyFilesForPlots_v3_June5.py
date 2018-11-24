import os
import sys
import subprocess
import glob

trueRun = True

doMETcut = True

createCombineArea = 'June5'
prefDir = 'analysis_May25_%s_Radion_total_SR_minitrees_inpb_wBR' 
#'analysis_mar16_btagMedium_%s_total_SR_minitrees_inpb_wBR' 

curDir = os.getcwd()

#masses = [260, 270, 300, 350, 400, 450,     451, 600, 650, 900, 1000]
masses = [250, 260, 270, 300, 350, 400, 450,     451, 500, 550, 600, 650, 700, 750, 800, 900, 1000]
#masses = [500, 550]
paths = []

justThisChannel = "eles"

def getRootsFiles():
    for mass in masses:
        print 'doing mass', mass
        for channelDir in 'eles', 'muons':
            if justThisChannel:
                channelDir = justThisChannel
    
        
        #for typ in 'CRDYlow_', 'CRDY_', 'CRDYhigh_', 'good_SR_bdt_sideBands':
            path = createCombineArea + '_' + channelDir + '_' +  str(mass) #+ '_' + typ[:-1]   #march28_ee_300_CRDYlow
            print path
            paths.append(path)
            if os.getcwd() == curDir and not os.path.exists(path):
                os.makedirs(path)

            mainDir = prefDir % channelDir
            if os.getcwd() == curDir :
                print 'cd to ', mainDir
                os.chdir(mainDir)

         
            leptType = "mm_" if channelDir == "muons" else "ee_" if channelDir == "eles" else None
            if leptType == None:
                print 'wrong leptType, exiting...'
                sys.exit(1)

            bdtCut = None
            metcut = None
            
            if 250 <= mass <=300:
                metcut = 40
            elif 350 <= mass <=600:
                metcut = 75
            elif 650<= mass <= 1000:
                metcut = 100
            else:
                print 'cannot happen, check metcut, exiting...'
                sys.exit(1)

            if leptType == 'mm_':
                if mass < 300:
                    bdtCut = 0.1
                
                elif 300 <= mass < 500:
                    bdtCut = 0.7
                
                elif 500 <= mass:
                    bdtCut = 0.99
                
                else:
                    continue
            elif leptType == 'ee_':
                if mass <= 350:
                    bdtCut = 0.4
                
                elif 400 <= mass < 500:
                    bdtCut = 0.925
                    pass
                elif 500 <= mass:
                    bdtCut = 0.99
                
                else:
                    continue
            else:
                print 'cannot happen, exiting'
                sys.exit(1)

            if bdtCut == None:
                print 'cannot happen, exiting'
                sys.exit(1)

            region = "low" if mass <= 450 else "high"
            tmp_mass = None
            if mass == 451:
                tmp_mass = 451
                mass = 450
            txts =  'find *nom*/%s_{SR_,CRDY_,CRTT_}*%s_met%s/*/make*/%s/*txt  -exec cp {}    ../%s  \;' % (region, str(bdtCut), str(metcut), str(mass), path)
            roots = 'find     */%s_{SR_,CRDY_,CRTT_}*%s_met%s/*/make*/%s/*root -exec cp {}    ../%s  \;' % (region, str(bdtCut), str(metcut), str(mass), path)
    #shapes_CMS_btag_heavyDown/low_CRDY_0.4/plots/makeDataCards/400/dataCard_CRDY_zmass_oneBin_CMS_btag_heavyDown.txt

        #print 'txts=', txts
        #print 'roots=', roots
        
        #os.chdir("../")
            for cmd in txts, roots:
                print cmd
                if trueRun: 
                    subprocess.call(cmd, shell=True)
                    print 
            
            print 'cd back to', curDir
            os.chdir(curDir)
            print
            if tmp_mass:
                mass = tmp_mass
                tmp_mass = None

 
            if justThisChannel:
                break
#sys.exit(1)

def copyToCombineArea():
#copy all new directories to the combine work area
    cmd1 = 'mkdir -p /afs/cern.ch/user/r/rkamalie/workspace/private/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/test/mytest/jan5/jan_work/tests/' + createCombineArea
    if trueRun: subprocess.call(cmd1, shell=True)
    global paths
    if paths == []:
        paths = glob.glob(createCombineArea + "_*_*")
    for p in paths:
        cmd2 = 'cp -r ' + p + ' /afs/cern.ch/user/r/rkamalie/workspace/private/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/test/mytest/jan5/jan_work/tests/' + createCombineArea
        print cmd2
        if trueRun: subprocess.call(cmd2, shell=True)


if __name__ == "__main__":
    getRootsFiles()
    copyToCombineArea()
