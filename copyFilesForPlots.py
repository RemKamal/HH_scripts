import os
import sys
import subprocess


trueRun = True #False

createCombineArea = 'march30'

curDir = os.getcwd()
mass = str(300) 
for chnl in 'ee_', 'mm_':
    for typ in 'CRDYlow_', 'CRDY_', 'CRDYhigh_', 'good_SR_bdt_sideBands':
        path = 'march28_' + chnl + mass + '_' + typ[:-1]   #march28_ee_300_CRDYlow
        print path
        if not os.path.exists(path):
            os.makedirs(path)
        


for channelDir in 'eles', 'muons':
    mainDir = 'analysis_mar16_btagMedium_%s_total_SR_minitrees_inpb_wBR' % channelDir
    os.chdir(mainDir)
    chnl = 'ee' if channelDir == 'eles' else 'mm'
    bdtCut = 0.4 if channelDir == 'eles'else 0.7
    for typ in 'CRDYlow_', 'CRDY_', 'CRDYhigh_', 'good_SR_bdt_sideBands':
        if 'DY' in typ:
            txts =  'find *nom*/low_{SR_,%s,CRTT_}*%s/*/make*/300/*txt  -exec cp {}    ../march28_%s_300_%s  \;' % (typ, str(bdtCut), chnl, typ[:-1])
            roots = 'find     */low_{SR_,%s,CRTT_}*%s/*/make*/300/*root -exec cp {}    ../march28_%s_300_%s  \;' % (typ, str(bdtCut), chnl, typ[:-1])

        else:
            os.chdir(typ)
            txts  = 'find  *nom*/low_*SR_*%s/*/make*/300/*txt           -exec cp {}  ../../march28_%s_300_%s  \;' % ( str(bdtCut), chnl, typ[:-1])
            roots = 'find */low_*SR_*%s/*/make*/300/*root               -exec cp {}  ../../march28_%s_300_%s  \;' % ( str(bdtCut), chnl, typ[:-1])
            
        for cmd in txts, roots:
            print cmd
            if trueRun: subprocess.call(cmd, shell=True)

        print 


    os.chdir(curDir)

#copy all new directories to the combine work area
cmd1 = 'mkdir /afs/cern.ch/user/r/rkamalie/workspace/private/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/test/mytest/jan5/jan_work/tests/' + createCombineArea
cmd2 = 'cp -r march28_*_300_* /afs/cern.ch/user/r/rkamalie/workspace/private/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/test/mytest/jan5/jan_work/tests/' + createCombineArea
cmd = cmd1 + ' && ' + cmd2
if trueRun: subprocess.call(cmd, shell=True)

