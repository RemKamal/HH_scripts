import os
import sys
import subprocess
import time

start_time = time.time()

trueRun = True #False

createCombineArea = 'march30'

if not os.path.exists(createCombineArea + '_forLimits'):
    os.makedirs(createCombineArea + '_forLimits')

curDir = os.getcwd()
massesIn = [260, 270, 300, 350, 400, 450,    451,     600, 650, 900, 1000]         

#if WANT to copy txts and roots for ALL variables - remove 'hh' for txts and roots 

for chnl in 'ee_', 'mm_':
    for typ in 'nominal', '':
        if typ != '':
            for mass in massesIn:
                mass = str(mass)
                path = createCombineArea + '_forLimits/' + chnl + mass
                print path
                if not os.path.exists(path):
                    os.makedirs(path)
        

mm_bdtCuts = [0.1, 0.7, 0.99]
ee_bdtCuts = [0.4, 0.925, 0.99]




for channelDir in 'eles', 'muons':
    mainDir = 'analysis_mar16_btagMedium_%s_total_SR_minitrees_inpb_wBR' % channelDir
    os.chdir(mainDir)
    chnl = 'ee_' if channelDir == 'eles' else 'mm_'
    doMuons = True if chnl == 'mm_' else False
    doEles = True if chnl == 'ee_' else False

    bdtCuts = ee_bdtCuts if channelDir == 'eles' else mm_bdtCuts
    for mass in massesIn:

        for bdtCut in bdtCuts:

            if 260 <= mass <= 270:
                if doMuons and bdtCut == 0.1:
                    pass
                elif doEles and bdtCut == 0.4:
                    pass
                else:
                    continue
            elif 300 <= mass <= 350:
                if doMuons and bdtCut == 0.7:
                    pass
                elif doEles and bdtCut == 0.4:
                    pass
                else:
                    continue
                
            elif 400 <= mass <= 451:
                if doMuons and bdtCut == 0.7:
                    pass
                elif doEles and bdtCut == 0.925:
                    pass
                else:
                    continue
                
            elif 600 <= mass <= 1000:
                if doMuons and bdtCut == 0.99:
                    pass
                elif doEles and bdtCut == 0.99:
                    pass
                else:
                    continue
                
            else:
                print 'cannott happen'
                continue

            massFrom = mass
            if mass <= 450:
                region = 'low_'
            elif mass == 451:
                region = 'high_'
                massFrom = 450
            else:
                region = 'high_'

            txts =  'find *nom*/%s{SR_,CRDY_,CRTT_}*%s/*/make*/%s/dat*hh*txt  -exec cp {}    ../%s  \;' % (region, str(bdtCut), str(massFrom), createCombineArea + '_forLimits/' + chnl + str(mass))
            roots = 'find     */%s{SR_,CRDY_,CRTT_}*%s/*/make*/%s/hh*root     -exec cp {}    ../%s  \;' % (region, str(bdtCut), str(massFrom), createCombineArea + '_forLimits/' + chnl + str(mass))

        # else:
        #     os.chdir(typ)
        #     txts  = 'find  *nom*/low_*SR_*%s/*/make*/300/*txt           -exec cp {}  ../../march28_%s_300_%s  \;' % ( str(bdtCut), chnl, typ[:-1])
        #     roots = 'find */low_*SR_*%s/*/make*/300/*root               -exec cp {}  ../../march28_%s_300_%s  \;' % ( str(bdtCut), chnl, typ[:-1])
            
            for cmd in txts, roots:
                print cmd
                if trueRun: subprocess.call(cmd, shell=True)

            print 


    os.chdir(curDir)



#copy all new directories to the combine work area
#cmd1 = 'mkdir /afs/cern.ch/user/r/rkamalie/workspace/private/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/test/mytest/jan5/jan_work/tests/' + createCombineArea + '_forLimits/'
cmd2 = 'cp -r ' + createCombineArea + '_forLimits/ /afs/cern.ch/user/r/rkamalie/workspace/private/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/test/mytest/jan5/jan_work/tests/' 
cmd = cmd2 #cmd1 + ' && ' + cmd2
print cmd
if trueRun: subprocess.call(cmd, shell=True)

end_time = time.time()
time_taken = end_time - start_time  # time_taken is in seconds                                                                                                  

hours, rest = divmod(time_taken, 3600)
minutes, seconds = divmod(rest, 60)
print
print 'all done!'
print "---it took {hours} hours, {minutes} minutes and {seconds:.1f} seconds to run the analysis ---".format(hours=hours,
                                                                                                             minutes=minutes,
                                                                                                             seconds=seconds)

# rkamalie@lxplus022:~/workspace/private/July31/v2/CMSSW_8_0_25/src/VHbbAnalysis/Heppy/test/analysis_mar16_btagMedium_eles_total_SR_minitrees_inpb_wBR$ lt shapes_nominal/l*_SR_0.*/plots/makeDataCards/*/da*hh*
# -rw-r--r--. 1 rkamalie zh 6746 Mar 17 20:51 shapes_nominal/low_SR_0.925/plots/makeDataCards/260/dataCard_SR_hhMt.txt
# -rw-r--r--. 1 rkamalie zh 6746 Mar 17 21:13 shapes_nominal/low_SR_0.925/plots/makeDataCards/270/dataCard_SR_hhMt.txt
# -rw-r--r--. 1 rkamalie zh 6746 Mar 17 21:55 shapes_nominal/low_SR_0.925/plots/makeDataCards/300/dataCard_SR_hhMt.txt
# -rw-r--r--. 1 rkamalie zh 6746 Mar 17 22:18 shapes_nominal/low_SR_0.925/plots/makeDataCards/350/dataCard_SR_hhMt.txt
# -rw-r--r--. 1 rkamalie zh 6746 Mar 17 22:38 shapes_nominal/low_SR_0.925/plots/makeDataCards/400/dataCard_SR_hhMt.txt
# -rw-r--r--. 1 rkamalie zh 6746 Mar 17 22:48 shapes_nominal/low_SR_0.925/plots/makeDataCards/450/dataCard_SR_hhMt.txt
# -rw-r--r--. 1 rkamalie zh 6747 Mar 22 12:02 shapes_nominal/low_SR_0.4/plots/makeDataCards/260/dataCard_SR_hhMt.txt
# -rw-r--r--. 1 rkamalie zh 6747 Mar 22 12:03 shapes_nominal/low_SR_0.4/plots/makeDataCards/270/dataCard_SR_hhMt.txt
# -rw-r--r--. 1 rkamalie zh 6747 Mar 22 12:05 shapes_nominal/low_SR_0.4/plots/makeDataCards/300/dataCard_SR_hhMt.txt
# -rw-r--r--. 1 rkamalie zh 6747 Mar 22 12:08 shapes_nominal/low_SR_0.4/plots/makeDataCards/350/dataCard_SR_hhMt.txt
# -rw-r--r--. 1 rkamalie zh 6747 Mar 22 12:09 shapes_nominal/low_SR_0.4/plots/makeDataCards/400/dataCard_SR_hhMt.txt
# rkamalie@lxplus022:~/workspace/private/July31/v2/CMSSW_8_0_25/src/VHbbAnalysis/Heppy/test/analysis_mar16_btagMedium_eles_total_SR_minitrees_inpb_wBR$ lt shapes_nominal/h*_SR_0.*/plots/makeDataCards/*/da*hh*
# -rw-r--r--. 1 rkamalie zh 6745 Mar 17 22:18 shapes_nominal/high_SR_0.925/plots/makeDataCards/450/dataCard_SR_hhMt.txt
# -rw-r--r--. 1 rkamalie zh 6745 Mar 17 22:41 shapes_nominal/high_SR_0.99/plots/makeDataCards/600/dataCard_SR_hhMt.txt
# -rw-r--r--. 1 rkamalie zh 6745 Mar 17 23:04 shapes_nominal/high_SR_0.99/plots/makeDataCards/650/dataCard_SR_hhMt.txt
# -rw-r--r--. 1 rkamalie zh 6745 Mar 17 23:28 shapes_nominal/high_SR_0.99/plots/makeDataCards/900/dataCard_SR_hhMt.txt
# -rw-r--r--. 1 rkamalie zh 6746 Mar 17 23:49 shapes_nominal/high_SR_0.99/plots/makeDataCards/1000/dataCard_SR_hhMt.txt
# rkamalie@lxplus022:~/workspace/private/July31/v2/CMSSW_8_0_25/src/VHbbAnalysis/Heppy/test/analysis_mar16_btagMedium_eles_total_SR_minitrees_inpb_wBR$ cd ../analysis_mar16_btagMedium_muons_total_SR_minitrees_inpb_wBR/
# rkamalie@lxplus022:~/workspace/private/July31/v2/CMSSW_8_0_25/src/VHbbAnalysis/Heppy/test/analysis_mar16_btagMedium_muons_total_SR_minitrees_inpb_wBR$ lt shapes_nominal/l*_SR_0.*/plots/makeDataCards/*/da*hh*
# -rw-r--r--. 1 rkamalie zh 6747 Mar 17 15:31 shapes_nominal/low_SR_0.1/plots/makeDataCards/260/dataCard_SR_hhMt.txt
# -rw-r--r--. 1 rkamalie zh 6747 Mar 17 15:43 shapes_nominal/low_SR_0.7/plots/makeDataCards/260/dataCard_SR_hhMt.txt
# -rw-r--r--. 1 rkamalie zh 6747 Mar 17 15:54 shapes_nominal/low_SR_0.1/plots/makeDataCards/270/dataCard_SR_hhMt.txt
# -rw-r--r--. 1 rkamalie zh 6747 Mar 17 16:07 shapes_nominal/low_SR_0.7/plots/makeDataCards/270/dataCard_SR_hhMt.txt
# -rw-r--r--. 1 rkamalie zh 6747 Mar 17 16:22 shapes_nominal/low_SR_0.1/plots/makeDataCards/300/dataCard_SR_hhMt.txt
# -rw-r--r--. 1 rkamalie zh 6747 Mar 17 16:36 shapes_nominal/low_SR_0.7/plots/makeDataCards/300/dataCard_SR_hhMt.txt
# -rw-r--r--. 1 rkamalie zh 6747 Mar 17 16:50 shapes_nominal/low_SR_0.1/plots/makeDataCards/350/dataCard_SR_hhMt.txt
# -rw-r--r--. 1 rkamalie zh 6747 Mar 17 17:03 shapes_nominal/low_SR_0.7/plots/makeDataCards/350/dataCard_SR_hhMt.txt
# -rw-r--r--. 1 rkamalie zh 6747 Mar 17 17:15 shapes_nominal/low_SR_0.1/plots/makeDataCards/400/dataCard_SR_hhMt.txt
# -rw-r--r--. 1 rkamalie zh 6747 Mar 17 17:26 shapes_nominal/low_SR_0.7/plots/makeDataCards/400/dataCard_SR_hhMt.txt
# -rw-r--r--. 1 rkamalie zh 6747 Mar 17 17:38 shapes_nominal/low_SR_0.7/plots/makeDataCards/450/dataCard_SR_hhMt.txt
# rkamalie@lxplus022:~/workspace/private/July31/v2/CMSSW_8_0_25/src/VHbbAnalysis/Heppy/test/analysis_mar16_btagMedium_muons_total_SR_minitrees_inpb_wBR$ lt shapes_nominal/h*_SR_0.*/plots/makeDataCards/*/da*hh*
# -rw-r--r--. 1 rkamalie zh 6746 Mar 17 15:30 shapes_nominal/high_SR_0.7/plots/makeDataCards/450/dataCard_SR_hhMt.txt
# -rw-r--r--. 1 rkamalie zh 6745 Mar 17 15:40 shapes_nominal/high_SR_0.99/plots/makeDataCards/600/dataCard_SR_hhMt.txt
# -rw-r--r--. 1 rkamalie zh 6745 Mar 17 15:50 shapes_nominal/high_SR_0.99/plots/makeDataCards/650/dataCard_SR_hhMt.txt
# -rw-r--r--. 1 rkamalie zh 6745 Mar 17 16:00 shapes_nominal/high_SR_0.99/plots/makeDataCards/900/dataCard_SR_hhMt.txt
# -rw-r--r--. 1 rkamalie zh 6746 Mar 17 16:13 shapes_nominal/high_SR_0.99/plots/makeDataCards/1000/dataCard_SR_hhMt.txt

