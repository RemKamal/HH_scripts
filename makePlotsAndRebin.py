import glob
import subprocess
import os
from multiprocessing import Pool
import sys

prefix = "June7"

studyLimitVariations = False#True
useMulticore=False
specialDirs=False#True
trueRun=True

metCutApplied = True
HHtype = "Radion" #"BGrav"

onlyMuons = False
onlyEles = True

createDirsList = []#[1, 2, 5, 10, 15, 20]
rebinAllowedList = createDirsList #[]
passOnlyThisDir = True if rebinAllowedList else False

masses_of_interest = [250, 260, 270, 300, 350, 400, 450, 451, 500, 550, 600, 650, 700, 750, 800, 900, 1000]
masses_of_interest = [250]
copy_txtNroots = True
curDir = os.getcwd()
copyPythons = True


def someCopyCommands(m, dirs):
    print 'os.getcwd()', os.getcwd()
    print 'dirs=', dirs
    for d in dirs:
        mass = int(d.split('_')[-1].strip('/'))
        if mass not in masses_of_interest:
            continue

        # if not studyLimitVariations:
        #     cmdMuon="cp ../%s/%s_muons_%s/hhMt_mm_*input.root %s_muons_%s/" % (prefix, prefix, m, prefix, m)
        #     cmsEle="cp ../%s/%s_eles_%s/hhMt_ee_*input.root %s_eles_%s/" % (prefix, prefix, m, prefix, m)
        #     cmds = [cmdMuon, cmsEle]
        # else:
        #     tmp_mass =  int(d.split('_')[-1])
        #     if m != tmp_mass:
        #         print "m={}, tmp_mass={}".format(m, tmp_mass)
        #         print 'check mass and directory, smth is wrong....exiting'
        #         sys.exit(1)
        #     leptType = d.split('_')[-2]
        #     cmdMuon="cp ../%s/%s_muons_%s/hhMt_mm_*input.root %s/" % (prefix, prefix, m, d)
        #     cmdEle="cp ../%s/%s_eles_%s/hhMt_ee_*input.root %s/" % (prefix, prefix, m, d)

        if not studyLimitVariations:
            cmdMuon="cp ../%s/%s_muons_%s/* %s_muons_%s/" % (prefix, prefix, m, prefix, m)
            cmsEle="cp ../%s/%s_eles_%s/* %s_eles_%s/" % (prefix, prefix, m, prefix, m)
            cmds = [cmdMuon, cmsEle]
        else:   
            tmp_mass =  int(d.split('_')[-1])
            if m != tmp_mass:
                print "m={}, tmp_mass={}".format(m, tmp_mass)
                print 'check mass and directory, smth is wrong....exiting'
                sys.exit(1)
            leptType = d.split('_')[-2]
            cmdMuon="cp ../%s/%s_muons_%s/* %s/" % (prefix, prefix, m, d)
            cmdEle="cp ../%s/%s_eles_%s/* %s/" % (prefix, prefix, m, d)


            cmds = [cmdMuon] if leptType == "muons" else [cmdEle] if leptType == "eles" else None
            if cmds == None:
                print 'check cmd, smth is wrong with the type of directory in the loop, exiting...'
                sys.exit(1)

            
    #cmd_transferLimit_Muon="""find april*muons* -name "higgsCombineTest.Asymptotic.mH*root" -exec cp {} limits_muons \;"""
    #cmd_transferLimit_Ele="""find april*eles* -name "higgsCombineTest.Asymptotic.mH*root" -exec cp {} limits_eles \;"""
        for cmd in cmds:
            print 'cmd=', cmd
            if trueRun:
                subprocess.call(cmd, shell=True)

def runPlots(d):
    print 'd=', d
    rebin = 0 if not studyLimitVariations else d.split('/')[0]
    if passOnlyThisDir and int(rebin) not in rebinAllowedList:
        return
    if trueRun: subprocess.call("cp *.py " + d, shell=True)
    os.chdir(d)
    channel = d.split('_')[-2]
    channel = "eles" if "eles" in channel else "muons" if "muons" in channel else None
    if channel == None:
        print 'check channel.., exiting...'
        sys.exit(1)
        putTogetherHists_makePostfitRoots_v4_met_radion_eles.py
    cmd = "python putTogetherHists_makePostfitRoots_v4{}_{}_{}.py --rebin ".format("_met" if metCutApplied else "", HHtype, channel) + str(rebin)
    print 'cmd=', cmd
    if trueRun: subprocess.call(cmd, shell=True)
    os.chdir(curDir)

if __name__ == '__main__':
    directories = glob.glob(prefix + "*/")
    if onlyMuons:
        directories = [x for x in directories if 'muons' in x]
    elif onlyEles:
        directories = [x for x in directories if 'eles' in x]
    else:
        pass
    print 'directories', directories

    if copyPythons:
        for d in directories:
            mass = int(d.split('_')[-1].strip('/'))
            if mass not in masses_of_interest:
                continue
            if trueRun:
                subprocess.call("cp *py " + d, shell=True)
        
    if specialDirs:
        #directories = [ prefix+x for x in ["_eles_900", "_muons_900"] ]
        directories = [ prefix+x for x in ["_eles_900"] ]
        #directories = ["may27_eles_900"]
    if studyLimitVariations:
        for d in createDirsList:
            d = str(d)
            for inDir in directories:
                if not os.path.exists(d + '/' + inDir):
                    print 'making an empty dir', d + '/' + inDir
                    os.makedirs(d + '/' + inDir)

        print 'directories', directories
        tmp_dirs = ["*/" + x for x in directories]
        print 'tmp_dirs', tmp_dirs
        directories = []
        for d in tmp_dirs:
            dirs = glob.glob(d)
            print 'dirs', dirs
            directories.extend(dirs)
        print 'directories', directories

    if copy_txtNroots:
        for m in masses_of_interest:
            someCopyCommands(m, directories)
        
    #sys.exit(1)
    if useMulticore:
        pool = Pool(processes=len(directories))
        pool.map(runPlots, directories)
    else:
        for d in directories:
            mass = int(d.split('_')[-1].strip('/'))
            if mass not in masses_of_interest:
                continue
            runPlots(d)
