from ROOT import TFile
import ROOT
import glob
import re
import subprocess
import time, os
import sys
import itertools
import multiprocessing
import glob
import shutil
import getopt
from copy import deepcopy

onlyPutTogetherHistsAndTexts = True #False
onlyHHMT = True
rebin_factor = 1
#CRs_postfit =  True
# means all_regions_postfit = False and vice verse

trueRun = True
channel = glob.glob("hh*eff_e_*")
if channel != [] and channel != None:
    channel = 'ee'  # comb_*")[0].split('_')[1]
else:
    channel = 'mm'

mass = os.getcwd().split('_')[-1]
range_ = ' --rMin -1000 --rMax 1000 ' if mass <= 400 else  ' --rMin -100 --rMax 100 '
mass = str(mass)  # [f for f in glob.glob("comb_*") if 'CR' not in f][0].split('_')[3][1:]

SR_bdt_sideBand = True if 'good_SR_bdt_sideBand' in os.getcwd() else False
CRDY_type = 'CRDY' if SR_bdt_sideBand else glob.glob("dataCard_CRDY*hh*")[0].split('_')[1]
doFitting = False if SR_bdt_sideBand or onlyPutTogetherHistsAndTexts else True

variables = [
    "bdt_response",
    "bdt_response_afterCut",
    "dR_bjets",
    "dR_leps",
    "hhMt",
    "hmass0",
    "hmass1",
    "hmass1_oneBin",
    "hpt0",
    "hpt1",
    "met_pt",
    "zmass",
    "zmass_high",
    "zmass_oneBin",
    "zpt0"
]


files_of_interest = glob.glob("*.input.root")
print files_of_interest

CRDYfiles = [x for x in files_of_interest if 'CRDY' in x and ('CMS' in x or 'nominal' in x)  and 'eff_met' not in x]
CRTTfiles = [x for x in files_of_interest if 'CRTT.' in x and ('CMS' in x or 'nominal' in x) and 'eff_met' not in x]
SRfiles = [x for x in files_of_interest if 'SR.' in x and ('CMS' in x or 'nominal' in x)     and 'eff_met' not in x]




def modifyDatacard(var, datacards):
    print 'working with', var
    #templ_dataCard  = 'dataCard_%s_%s.txt'
    mod_datacards = deepcopy(datacards)
    mod_datacards= [ 'copy_' + x for x in mod_datacards]
    #for reg in "SR", "CRTT", CRDY_type:
     #   datacards.append(templ_dataCard % (reg, var))
    
    for dc in mod_datacards:
        # back up initial data cards, they will be used by other functions later, below we rewrite old once
        #new_dc = dc[:-4] + '_original.txt'
        #shutil.copyfile(dc, new_dc)
        if SR_bdt_sideBand:
            if 'DY' in dc or 'TT' in dc:
                continue
        cmd = 'python  DataCardsREwriter_v2.py  -i ' + dc  + ' -o ' + dc
        print 'cmd=', cmd
        subprocess.call(cmd, shell=True)

def copyAndCombineCards(varbl):
    print 'working with', varbl

    if onlyHHMT and 'hh' not in varbl: return
    templ_dataCard  = 'dataCard_%s_%s.txt' 
    datacards = []
    for reg in "SR", "CRTT", CRDY_type:
        datacards.append(templ_dataCard % (reg, varbl))

    # back up initial data cards
    for dc in datacards:
        #if SR_bdt_sideBand and ('DY' in dc or 'TT' in dc): continue
        new_dc = 'copy_' + dc
        shutil.copyfile(dc, new_dc)

    modifyDatacard(varbl, datacards)

    if 'hhMt' in varbl and not SR_bdt_sideBand:
        comb_CRDYnCRTT = "combineCards.py copy_dataCard_" + CRDY_type + "_hhMt.txt copy_dataCard_CRTT_hhMt.txt > copy_dataCard_" + CRDY_type + "nTT_hhMt.txt"
        comb_CRsnSR = "combineCards.py CRDY=copy_dataCard_" + CRDY_type + "_hhMt.txt SR=copy_dataCard_SR_hhMt.txt CRTT=copy_dataCard_CRTT_hhMt.txt > copy_dataCard_all_hhMt.txt && cp copy_dataCard_all_hhMt.txt dataCard_hhMt_" + channel + ".txt"
        print
    # combine cards for various regions for HHMT only

        for cmd in comb_CRDYnCRTT, comb_CRsnSR:
            print 'cmd=', cmd
            if trueRun: subprocess.call(cmd, shell=True)

    all_dc = glob.glob('copy_*' + varbl + '*.txt')
    # add BBB uncertainty to data cards
    for dc in all_dc:  # [0:1]:
        print 'processing', dc
        cmd = 'echo "" >> ' + dc + ' && echo "* autoMCStats 0" >> ' + dc
        print 'cmd', cmd
        if trueRun: subprocess.call(cmd, shell=True)

    #if varbl != 'hhMt': return
    #print 'working with HHMT only'


def doFits():
    extra = '' 
    #extra = ' --cminDefaultMinimizerTolerance 0.05 '

    fit_CRs = 'combine -M MaxLikelihoodFit -v 3  --X-rtd MINIMIZER_analytic  --cminDefaultMinimizerStrategy 0 ' + extra + ' --saveShapes --saveNormalizations --saveWithUncertainties -m ' + mass + range_ + 'copy_dataCard_' + CRDY_type + 'nTT_hhMt.txt >& log_fit_CRs.txt' 

    fit_all = 'combine -M MaxLikelihoodFit -v 3  --X-rtd MINIMIZER_analytic  --cminDefaultMinimizerStrategy 0 ' + extra + ' --saveShapes --saveNormalizations --saveWithUncertainties -m ' + mass + range_ + 'copy_dataCard_all_hhMt.txt >& log_fit_all.txt'  

    # for fit in fit_CRs, fit_all:
    print 'fit=', fit_CRs
    subprocess.call(fit_CRs, shell=True)
    shutil.move("fitDiagnostics.root", "fitDiagnostics_CRs.root")

    print 'fit=', fit_all
    subprocess.call(fit_all, shell=True)
    shutil.move("fitDiagnostics.root", "fitDiagnostics_all.root")



def separateFilesPerVariable(files):
    print 'files=', files
    print
    for var in variables:
        #if 'hh' not in var: continue
        print 'processing var=', var
        print
        # handle the bdt_response separately, since it is a substring of the bdt_response_afterCut
        if var == 'bdt_response' and var != 'bdt_response_afterCut':
            tmp_files = [x for x in files if var in x and 'bdt_response_afterCut' not in x]
        else:
            tmp_files = [x for x in files if var in x]
            
        print 'tmp_files=', tmp_files
        print
        print ' len(tmp_files)', len(tmp_files)
        print '-'*100
        putTogetherHists(tmp_files)
        

def putTogetherHists(files):

    #print 'files:'
    #print files

    print 
    if files == []: return
    print 'files[0]', files[0]
    innerDir = '_'.join(files[0].split('input')[0].split('_')[-2:])[:-1]
    print 'innerDir', innerDir
    varName = re.split(r'(CMS|nominal)\s*', files[0])[0] #say zmass_high_
    #if 'hma' not in varName: return

    tmpfile = varName + innerDir  + '.input.root' #hhMt_mm_SR.input.root
    print 'tmpfile', tmpfile

    #return
    hists = dict()#set()#[]
    for f in files:
        print 'working with file', f
        
        shapes_file = ROOT.TFile.Open(f, 'read')
        #print 'shapes_file.IsZombie()', shapes_file.IsZombie()
        #print 'list of Keys is', ROOT.gDirectory.GetListOfKeys().ls()
        #print 'gonna cd'
        print shapes_file.cd(innerDir)
        shapes = ROOT.gDirectory.GetListOfKeys()
        
        #print 'shapes', shapes
        # Since the nominal and varied shapes share the same binning,
        # take any of the histograms found in the shapes file.
        for idx, shape in enumerate(shapes):
            shape = ROOT.gDirectory.Get(shapes[idx].GetName())
            if rebin_factor > 1:
                shape.Rebin(rebin_factor)
            print 'before draw'
            #shape.Print()
            #shap = shape.Clone()
            shape.SetDirectory(0)
            #hists.append (shape)
            if shape.GetName() not in hists:
                #hists.add (shape)
                hists[shape.GetName()] = shape


    #print 'hists', hists
    print 'len(hists)', len(hists)
    #return 

    if True:
            #inp = ROOT.TFile.Open(inputfile,'read')
        output = ROOT.TFile.Open(tmpfile,'recreate')
        output.mkdir(innerDir)
        output.cd(innerDir)
        print 'before LOOP'
        #for h in hists:

        print 'mass=', mass
        if hists['signal_hww_CMS_res_jUp'].Integral() == 0.00 and int(mass) == 600:
            print 'voila here check '
            print '\n'*100
            print "hists['signal_hww_CMS_res_jUp'].Integral()", hists['signal_hww_CMS_res_jUp'].Integral()
            print "hists['signal_hww'].Integral()", hists['signal_hww'].Integral()
            hists['signal_hww_CMS_res_jUp'] = hists['signal_hww_CMS_res_jDown'].Clone('signal_hww_CMS_res_jUp')
            print 'after fix'
            print "hists['signal_hww_CMS_res_jUp'].Integral()", hists['signal_hww_CMS_res_jUp'].Integral()
            print "hists['signal_hww'].Integral()", hists['signal_hww'].Integral()

        if hists['signal_hww_CMS_scale_jDown'].Integral() == 0.00 and int(mass) == 600:
            print 'voila here check '
            print '\n'*100
            print "hists['signal_hww_CMS_scale_jDown'].Integral()", hists['signal_hww_CMS_scale_jDown'].Integral()
            print "hists['signal_hww'].Integral()", hists['signal_hww'].Integral()
            hists['signal_hww_CMS_scale_jDown'] = hists['signal_hww_CMS_res_jDown'].Clone('signal_hww_CMS_scale_jUp')
            print 'after fix'
            print "hists['signal_hww_CMS_scale_jDown'].Integral()", hists['signal_hww_CMS_scale_jDown'].Integral()
            print "hists['signal_hww'].Integral()", hists['signal_hww'].Integral()


        for k,v in hists.items():
        
            #for (k, v) in dict_rename.items():
             #   if k in h.GetName():
              #      h.SetName(h.GetName().replace(k, v))
            #h.Write()#key.GetName())
            #https://root.cern.ch/input-and-output
            #https://root.cern.ch/root/htmldoc/guides/users-guide/InputOutput.html#retrieving-objects-from-disk
            v.Write(k, ROOT.TObject.kOverwrite)#key.GetName())
            #print h.GetName()
        print 'after LOOP'
        output.Close()
        


def read3(fname):

    print
    print 'processing', fname
    shapes_file = ROOT.TFile.Open(fname)
    innerDir = fname[:-11]
    tmpfile = 'new_' + fname
    print 'tfile path is', shapes_file
    print 'list of keys'
    print 'list of Keys is', ROOT.gDirectory.GetListOfKeys().ls()
    print 'gonna cd'
    print shapes_file.cd(innerDir)
    shapes = ROOT.gDirectory.GetListOfKeys()
    hists = []
    print shapes
        # Since the nominal and varied shapes share the same binning,
        # take any of the histograms found in the shapes file.
    for idx, shape in enumerate(shapes):
        shape = ROOT.gDirectory.Get(shapes[idx].GetName())
        print 'before draw'
        #shape.Print()
        hists.append (shape)

    if True:
            #inp = ROOT.TFile.Open(inputfile,'read')
        output = ROOT.TFile.Open(tmpfile,'recreate')
        output.mkdir(innerDir)
        output.cd(innerDir)
        print 'before LOOP'
        for h in hists:
            for (k, v) in dict_rename.items():
                if k in h.GetName():
                    h.SetName(h.GetName().replace(k, v))
            h.Write()#key.GetName())
            print h.GetName()
        print 'after LOOP'
        output.Close()
        
        

#=======================================
        # obj = ROOT.TObject
        # for key in ROOT.gDirectory.GetListOfKeys():
        #         #inp.cd()
        #     obj = key.ReadObj()
        #         #if obj.GetName() == job.tree:
        #         #   continue
        #     output.cd()
        #     obj.Write(key.GetName())
        # outfile.Close()
        # infile.Close()




def producePostFitRootFiles(var):

    if onlyHHMT and 'hh' not in var: return

    cardCRTT = 'dataCard_CRTT_%s.txt' % var
    cardCRTTmc = 'copy_dataCard_CRTT_%s.txt' % var

    cardCRDY = 'dataCard_' + CRDY_type + '_%s.txt' % var
    cardCRDYmc = 'copy_dataCard_' + CRDY_type + '_%s.txt' % var

    cardSR = 'dataCard_SR_%s.txt' % var
    cardSRmc = 'copy_dataCard_SR_%s.txt' % var

    cpSR = "text2workspace.py " + cardSRmc #" cp " + cardSR + " " + cardSRmc + """ && echo "" >> """ + cardSRmc + """ && echo "* autoMCStats 0" >> """ + cardSRmc + " && text2workspace.py " + cardSRmc

    cpCRDY = "text2workspace.py " + cardCRDYmc #" cp " + cardCRDY + " " + cardCRDYmc + """ && echo "" >> """ + cardCRDYmc + """ && echo "* autoMCStats 0" >> """ + cardCRDYmc + " && text2workspace.py " + cardCRDYmc

    cpCRTT = "text2workspace.py " + cardCRTTmc #" cp " + cardCRTT + " " + cardCRTTmc + """ && echo "" >> """ + cardCRTTmc + """ && echo "* autoMCStats 0" >> """ + cardCRTTmc + " && text2workspace.py " + cardCRTTmc



    print
    print 'cpCRDY', cpCRDY
    print 'cpCRTT', cpCRTT
    print 'cpSR', cpSR
    subprocess.call(cpSR, shell=True)
    if not SR_bdt_sideBand:
        subprocess.call(cpCRDY, shell=True)
        subprocess.call(cpCRTT, shell=True)

    for postfit_type in '_CRsPostfit', '_FullPostfit':
        fitFile = 'fitDiagnostics_CRs.root' if 'CRs' in postfit_type else 'fitDiagnostics_all.root'
        #postfit_type = '_CRsPostfit' if CRs_postfit else '_FullPostfit'

        topostfitDY = 'PostFitShapesFromWorkspace -d ' + cardCRDYmc + ' -w ' + cardCRDYmc[:-4] + '.root -o ' + channel + '_' + var + '_' + CRDY_type + postfit_type + '.root -m ' + mass + ' -f ' + fitFile + ':fit_s --postfit --sampling --print'
        print 'topostfitDY', topostfitDY

        topostfitTT = 'PostFitShapesFromWorkspace -d ' + cardCRTTmc + ' -w ' + cardCRTTmc[:-4] + '.root -o ' + channel + '_' + var + '_CRTT' + postfit_type + '.root -m ' + mass + ' -f ' + fitFile + ':fit_s --postfit --sampling --print'
        print 'topostfitTT', topostfitTT

        topostfitSR = 'PostFitShapesFromWorkspace -d ' + cardSRmc + ' -w ' + cardSRmc[:-4] + '.root -o ' + channel + '_' + var + '_SR' + postfit_type +  '.root -m ' + mass + ' -f ' + fitFile + ':fit_s --postfit --sampling --print'
        print 'topostfitSR', topostfitSR


        print '-' * 50
        subprocess.call(topostfitSR, shell=True)
        if not SR_bdt_sideBand:
            subprocess.call(topostfitDY, shell=True)
            subprocess.call(topostfitTT, shell=True)
    ####for now do only DY
        print '\n' * 10


def main(argv):
   inputfile = None
   outputfile = None
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'test.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg

   if inputfile and outputfile:
       print 'Input file is "', inputfile
       print 'Output file is "', outputfile

   start_time = time.time()
   for idx, list_of_files in enumerate([SRfiles, CRTTfiles, CRDYfiles]):
       # if 'new' in fil: continue
       # read3(fil)
       # if idx >1: continue
       #pass
       separateFilesPerVariable(list_of_files)


   #processFile(inputfile, outputfile)
   for var in variables:
       if onlyPutTogetherHistsAndTexts and 'hh' not in var: continue                                                                                                                       
       print 'processing var=', var
       print
       copyAndCombineCards(var)



   if doFitting:
       doFits()
   ######################## use datacard rewriter in producePostFitRootFiles and copyAndCombineCards before doing any other work
   #print 'intentional early return'; return
   if onlyPutTogetherHistsAndTexts:
       return

   pool = multiprocessing.Pool(16)  # 32
   pool.map(producePostFitRootFiles, variables)

   plotCmd = 'python  plotCardshapes_postfit1_10.py'
   print 'plotCmd=', plotCmd
   subprocess.call(plotCmd, shell=True)

   end_time = time.time()
   time_taken = end_time - start_time  # time_taken is in seconds

   hours, rest = divmod(time_taken, 3600)
   minutes, seconds = divmod(rest, 60)
   print
   print 'all done!'
   print "---it took {hours} hours, {minutes} minutes and {seconds:.1f} seconds to run the analysis ---".format(hours=hours,
                                                                                                          minutes=minutes,
                                                                                                          seconds=seconds)
   # raw_input("Press Enter to exit...")





if __name__ == "__main__":
   main(sys.argv[1:])

