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
from array import array

doOnlySR = False

doNotRebinBDT = True
rebinByTemplate = False
onlyPutTogetherHistsAndTexts = False
onlyHHMTandBDT = True
rebin_factor = 1 #do not rebin here, use "modify..." script
#CRs_postfit =  True
# means all_regions_postfit = False and vice verse
prefix = "new_"

trueRun = True
channel = glob.glob("hh*eff_e_*")
if channel != [] and channel != None:
    channel = 'ee'  # comb_*")[0].split('_')[1]
else:
    channel = 'mm'

SR_bdt_sideBand = False #True if 'good_SR_bdt_sideBand' in os.getcwd() else False
# lastTwo = os.getcwd().split('_')[-2:] if not SR_bdt_sideBand else  os.getcwd().split('_good_SR_bdt_sideBand')[0].split('_')
# mass = None
# if lastTwo[-1].isdigit():
#     mass = lastTwo[-1]
# elif lastTwo[-2].isdigit():
#     mass = lastTwo[-2]
# else:
#     print 'chech mass assignment, exiting....'
#     sys.exit(1)


#minValue = 150 if massRegion == 'low' else 400
#maxValue = 1150 if massRegion == 'low' else 1400
#divideBy_forBinning = 20

#maybe will use for later iteration of analysis
#    maxValue = 1050 if massRegion == 'low' else 1300                       
#    divideBy_forBinning = 30  


#mass = int(mass) 
mass = int(os.getcwd().split('_')[-1])
rebin_dict = {
    250: 1,
    
    260: 1,
    270: 1,
    300: 2, #!                                                                                                                                            
    350: 1,
    
    400: 2, #?                                                                                                                                            
    450: 2, #2?                                                                                                                        
    451: 10, #2                                                                                                                                            
    
    500: 5,
    550 :5,
    
    600: 5,
    650: 5, #10 for eles 
    
    700 :5,
    750 :5, #10 for eles 
    800 :5, #25 for eles
    
    900: 5, #10 for eles 
    #900: 5, #10 for mm 
    1000: 5 #10 for eles
    }

def reBiner(Hist,minimum):
  """docstring for reBiner"""
  upArray = []
  nBins = -1
  for bin in range(0,Hist.GetNbinsX()):
    binC = 0
    n = Hist.GetBinContent(bin)
    e = Hist.GetBinError(bin)
    if e < 1: e = 1
    if (n*n)/(e*e) > minimum:
      upArray.append(Hist.GetBinLowEdge(bin+1))
      nBins+=1
    else:
      binC += (n*n)/(e*e)
      if binC > minimum:
        upArray.append(Hist.GetBinLowEdge(bin+1))
        nBins+=1
        binC = 0
  upArray.append(Hist.GetBinLowEdge(Hist.GetNbinsX()))
  nBins+=1
  rebinList = array.array('d',upArray)
  return (nBins,rebinList)

def rebin(hist,nbins,binList):
    """docstring for Rebin"""
    if binList != None:
        bins = array('d',binList)
        tmp = hist.Rebin(nbins,"tmp",bins)
        hist = tmp
    else:
        hist.Rebin(nbins)
#https://github.com/brynmathias/pyRootUtils/blob/cc5a5ba764226de0b4de8f72baf51d6c7fa9b109/plottingUtils.py#L227


rebin_value = rebin_dict[mass]
#print 'rebin=', rebin

range_ = ' --rMin -1000 --rMax 1000 ' if mass <= 400 else  ' --rMin -100 --rMax 100 '
mass = str(mass) 
print 'mass=', mass

CRDY_type = 'CRDY' #if SR_bdt_sideBand else glob.glob("dataCard_CRDY*hh*")[0].split('_')[1]
#doFitting = False if SR_bdt_sideBand or onlyPutTogetherHistsAndTexts else True
doFitting = True

variables = [
    "bdt_response",
    "bdt_response_afterCut",
    "dR_bjets",
    "dR_leps",
    "hhMt",
    "hmass0",
    "hmass1",
    #"hmass1_oneBin",
    "hpt0",
    "hpt1",
    "met_pt",
    "zmass",
    "zmass_high",
    #"zmass_oneBin",
    "zpt0"
]


files_of_interest = glob.glob("*.input.root")
print files_of_interest

CRDYfiles = [x for x in files_of_interest if 'CRDY' in x and ('CMS' in x or 'nominal' in x)  and 'eff_met' not in x]
CRTTfiles = [x for x in files_of_interest if 'CRTT.' in x and ('CMS' in x or 'nominal' in x) and 'eff_met' not in x]
SRfiles = [x for x in files_of_interest if 'SR.' in x and ('CMS' in x or 'nominal' in x)     and 'eff_met' not in x]




def modifyDatacard(var, datacards):
    if onlyHHMTandBDT and not ('hh' in var or 'bdt' in var): return
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

    if onlyHHMTandBDT and not ('hh' in varbl or 'bdt' in varbl): return
    templ_dataCard  = 'dataCard_%s_%s.txt' 
    datacards = []
    for reg in "SR", "CRTT", CRDY_type:
        datacards.append(templ_dataCard % (reg, varbl))

    # back up initial data cards
    for dc in datacards:
        if SR_bdt_sideBand and ('DY' in dc or 'TT' in dc): continue
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

    fit_CRs = 'text2workspace.py copy_dataCard_' + CRDY_type + 'nTT_hhMt.txt'
    fit_CRs_run = 'combine -M MaxLikelihoodFit -v 3  --X-rtd MINIMIZER_analytic  --cminDefaultMinimizerStrategy 0 ' + extra + ' --saveShapes --saveNormalizations --saveWithUncertainties -m ' + mass + range_ + 'copy_dataCard_' + CRDY_type + 'nTT_hhMt.root >& log_fit_CRs_' + channel + '.txt' 

    fit_all = 'text2workspace.py copy_dataCard_all_hhMt.txt'
    fit_all_run ='combine -M MaxLikelihoodFit -v 3  --X-rtd MINIMIZER_analytic  --cminDefaultMinimizerStrategy 0 ' + extra + ' --saveShapes --saveNormalizations --saveWithUncertainties -m ' + mass + range_ + 'copy_dataCard_all_hhMt.root >& log_fit_all_' + channel + '.txt'  

    fit_asymptotic = 'combine -M Asymptotic -v 3 --X-rtd MINIMIZER_analytic  --cminDefaultMinimizerStrategy 0 ' + extra + range_ + ' -m ' + mass + ' ' + 'copy_dataCard_all_hhMt.root >& log_fit_all_asymptotic' + channel + '.txt'

    #good working examples
    # combine -M MaxLikelihoodFit -v 3  --X-rtd MINIMIZER_analytic  --cminDefaultMinimizerStrategy 0  --saveShapes --saveNormalizations --saveWithUncertainties -m 300 --rMin -1000 --rMax 1000 copy_dataCard_CRDYnTT_hhMt.root >& log_fit_CRs.txt && mv fitDiagnostics.root fitDiagnostics_CRs.root
    # combine -M MaxLikelihoodFit -v 3  --X-rtd MINIMIZER_analytic  --cminDefaultMinimizerStrategy 0  --saveShapes --saveNormalizations --saveWithUncertainties -m 300 --rMin -1000 --rMax 1000 copy_dataCard_all_hhMt.root >& log_fit_all.txt &&  mv fitDiagnostics.root fitDiagnostics_all.root


    # for fit in fit_CRs, fit_all:
    print 'fit=', fit_CRs
    subprocess.call(fit_CRs, shell=True)

    if os.path.exists("copy_dataCard_CRDYnTT_hhMt.root") and os.stat('copy_dataCard_CRDYnTT_hhMt.root').st_size > 10000:
        subprocess.call(fit_CRs_run, shell=True)
    if os.path.exists("fitDiagnostics.root") and os.stat('fitDiagnostics.root').st_size > 10000:
        shutil.move("fitDiagnostics.root", "fitDiagnostics_CRs.root")
    else:
        print 'fit failed, size is small, so smth went wrong, exiting...'
        sys.exit(1)

    print 'fit=', fit_all
    subprocess.call(fit_all, shell=True)

    if os.path.exists("copy_dataCard_all_hhMt.root") and os.stat('copy_dataCard_all_hhMt.root').st_size > 10000:
        subprocess.call(fit_all_run, shell=True)

    if os.path.exists("fitDiagnostics.root") and os.stat('fitDiagnostics.root').st_size > 10000:
        shutil.move("fitDiagnostics.root", "fitDiagnostics_all.root")
    else:
        print 'fit failed, size is small, so smth went wrong, exiting...'
        sys.exit(1)

    print 'fit_asymptotic=', fit_asymptotic
    subprocess.call(fit_asymptotic, shell=True)


def separateFilesPerVariable(files, rebin):
    print 'files=', files
    print
    for var in variables:
        if 'oneBin' in var: continue
        print 'processing variable=', var
        print
        if onlyHHMTandBDT and not ('hh' in var or 'bdt' in var): continue
        # handle the bdt_response separately, since it is a substring of the bdt_response_afterCut
        if var == 'bdt_response' and var != 'bdt_response_afterCut':
            tmp_files = [x for x in files if var in x and 'bdt_response_afterCut' not in x]
        elif var == 'zmass':
            tmp_files = [x for x in files if var in x and 'zmass_high' not in x]
        else:
            tmp_files = [x for x in files if var in x]
            
        print 'tmp_files=', tmp_files
        print
        print ' len(tmp_files)', len(tmp_files)
        print '-'*100
        if rebin:
            print 'rebin=', rebin
            putTogetherHists(tmp_files, int(rebin))
        

def putTogetherHists(files, rebin):

    #print 'files:'
    #print files

    print 
    if files == []: return
    print 'files[0]', files[0]
    innerDir = '_'.join(files[0].split('input')[0].split('_')[-2:])[:-1]
    print 'innerDir', innerDir
    varName = re.split(r'(CMS|nominal)\s*', files[0])[0] #say zmass_high_
    #if 'hma' not in varName: return
    tmpfile = prefix + varName + innerDir  + '.input.root' #hhMt_mm_SR.input.root
    #tmpfile = varName + innerDir  + '.input.root' #hhMt_mm_SR.input.root
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
            
            #if rebin_factor > 1:
            #    shape.Rebin(rebin_factor)
            print 'rebin', rebin
            print 'innerDir', innerDir
            if rebin > 1 and 'SR' in innerDir:
                #if channel == "mm" and int(mass) == 900:
                #    rebin_factor = 10

#                elif channel == "mm" and int(mass) == 650:
 #                   rebin_factor = 20
                #else:
                rebin_factor = rebin

                xbins_list = []
                nbins=shape.GetNbinsX()
                dummy_var = 10000 # some big number
                for i in range(1, nbins+1, rebin_factor):
                    #print i                                                                                                                              
                    dummy_var = i
                    #print shape.GetBinContent(i)                                                                                                         
                    xbins_list.append(shape.GetBinLowEdge(i))
                print 'xbins_list[-1] before adding the last high element explicitly', xbins_list[-1]
                print 'shape.GetBinLowEdge(nbins)', shape.GetBinLowEdge(nbins)
                print 'shape.GetBinCenter(nbins) + shape.GetXaxis().GetBinWidth(nbins)/2', shape.GetBinCenter(nbins) + shape.GetXaxis().GetBinWidth(nbins)/2
                if xbins_list[-1] < shape.GetBinCenter(nbins) + shape.GetXaxis().GetBinWidth(nbins)/2:#shape.GetBinLowEdge(nbins):
                  #xbins_list.append(shape.GetBinLowEdge(nbins)) #shape.GetBinCenter(nbins) + shape.GetXaxis().GetBinWidth(nbins)/2)
                  xbins_list.append(shape.GetBinCenter(nbins) + shape.GetXaxis().GetBinWidth(nbins)/2)
                xbins = array("d", xbins_list)
                #print 'xbins=', xbins      
                print 'inside rebin'
                print 'varName', varName
                print 'shape.GetName()', shape.GetName()
                print 'int(mass)', int(mass)
                if 'hhMt' in varName and int(mass) > 451:
                  xbins_list = [shape.GetBinLowEdge(1)]
                  xbins_list += [600, 800, 1000, shape.GetBinCenter(nbins) + shape.GetXaxis().GetBinWidth(nbins)/2]
                  xbins = array("d", xbins_list)


                if True:
                  print 'inside meaningless true'
                  #xbins_list = [400, 500, 600, 700, 800, 900, 1000, 1300]
                  #xbins_list = [400, 450, 500, 550, 600, 650, 700, 750, 800, 900, 1000, 1400]
                  pass
                  #xbins = array("d", [400, 500, 600, 700, 800, 900, 1000, 1300]) #xbins_list
                  #shape = shape.Rebin(len(xbins)-1, shape.GetName(), xbins)
                    #histos['hhMt{0}'.format(postf)]  = ROOT.TH1F('hhMt{0}'.format(postf), '\;#tilde{M_{T}}(HH) [GeV]; Events', (maxValue - minValue)/divideBy_forBinning, m\inValue, maxValue)
                    
                if True:
                  print 'inside meaningFULL true'
                  print 'xbins_list', xbins_list
                  if rebinByTemplate and xbins_list != []: #nbins%rebin_factor !=0 and xbins_list != []:
                    print 'complicated rebin=', rebin_factor
                    print 'mass=', mass
                    print 'nbins=', nbins
                    print 'xbins_list=', xbins_list
                  
                    if doNotRebinBDT and 'bdt' in varName:
                      print 'bdt, do not rebin'
                      pass
                    else:
                      print 'not a bdt, rebin'
                      print 'IMPORTANT begin, shape.GetNbinsX()=', shape.GetNbinsX()
                      shape = shape.Rebin(len(xbins)-1, shape.GetName(), xbins)
                      print 'IMPORTANT changed, shape.GetNbinsX()=', shape.GetNbinsX()
                    #https://root-forum.cern.ch/t/rebbing-a-histogram-in-pyroot/17862                                                                     
                    #https://github.com/brynmathias/pyRootUtils/blob/master/plottingUtils.py#L227                                                         
                  else:
                # data_hist = ROOT.TH1F("data_hist","data_hist",nbins,DY.GetBinLowEdge(1),DY.GetBinCenter(nbins)+DY.GetXaxis().GetBinWidth(nbins)/2)      
                    print 'simple rebinning, rebin=', rebin_factor
                    print 'rebin=', 
                    print 'mass=', mass
                    print 'begin, shape.GetNbinsX()=', shape.GetNbinsX()
                    if doNotRebinBDT and 'bdt' in varName:
                      print 'bdt, do not rebin'
                      pass
                    else:
                      print 'not a bdt, rebin'
                      shape.Rebin(rebin_factor)
                      print 'IMPORTANT simple change, shape.GetNbinsX()=', shape.GetNbinsX()
                    print 'after, shape.GetNbinsX()=', shape.GetNbinsX()
                    



            print 'before draw'
            shape.SetDirectory(0)
            #shape.Print()
            #shap = shape.Clone()
            
            #hists.append (shape)
            if shape.GetName() not in hists:
                #hists.add (shape)
              print 'finalised shape has N bins', shape.GetName(), shape.GetNbinsX()
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
          print 'v.GetName()', v.GetName()
          print 'v.GetNbinsX()', v.GetNbinsX()
            #https://root.cern.ch/root/htmldoc/guides/users-guide/InputOutput.html#retrieving-objects-from-disk
          v.Write(k, ROOT.TObject.kOverwrite)#key.GetName())
            #print h.GetName()
        print 'after LOOP'
        output.Close()
    os.rename(tmpfile, tmpfile.strip(prefix))    


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
    print 'doing producePostFitRootFiles'
    if onlyHHMTandBDT and not ('hh' in var or 'bdt' in var): return

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

        topostfitDY = "PostFitShapesFromWorkspace -d " + cardCRDYmc + " -w " + cardCRDYmc[:-4] + ".root -o " + channel + "_" + var + "_" + CRDY_type + postfit_type + ".root -m " + mass + " -f " + fitFile + ":fit_s --postfit --sampling --print >& log_PostFitShapesFromWorkspace_" + channel + "_" + CRDY_type + "_" + var + postfit_type + ".txt"
        print "topostfitDY", topostfitDY

        topostfitTT = "PostFitShapesFromWorkspace -d " + cardCRTTmc + " -w " + cardCRTTmc[:-4] + ".root -o " + channel + "_" + var + "_CRTT" + postfit_type + ".root -m " + mass + " -f " + fitFile + ":fit_s --postfit --sampling --print >& log_PostFitShapesFromWorkspace_" + channel + "_CRTT_" + var + postfit_type + ".txt"
        print "topostfitTT", topostfitTT

        topostfitSR = "PostFitShapesFromWorkspace -d " + cardSRmc + " -w " + cardSRmc[:-4] + ".root -o " + channel + "_" + var + "_SR" + postfit_type +  ".root -m " + mass + " -f " + fitFile + ":fit_s --postfit --sampling --print >& log_PostFitShapesFromWorkspace_" + channel + "_SR_" + var + postfit_type + ".txt" 
        print "topostfitSR", topostfitSR

        log_postfit =  " >& log_PostFitShapesFromWorkspace_" + channel + "_" + "%s" + "_" + var + postfit_type + ".txt" 
        
        print '-' * 50

        os.system(topostfitSR)  #subprocess.call(topostfitSR, shell=True)
        if not SR_bdt_sideBand:
            os.system(topostfitDY) #+ log_postfit % CRDY_type
            os.system(topostfitTT) 
            #subprocess.call(topostfitDY, shell=True)
            #subprocess.call(topostfitTT, shell=True)
    ####for now do only DY
        print '\n' * 10


def main(argv):
   inputfile = None
   outputfile = None
   rebin = None
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile=", "rebin="])
   except getopt.GetoptError:
      print 'test.py -i <inputfile> -o <outputfile> --rebin <rebinNumber>' 
      #print 'opts=', opts
      #print 'args', args
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("--rebin"):
         rebin = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg

   if inputfile and outputfile:
       print 'Input file is "', inputfile
       print 'Output file is "', outputfile
   if int(rebin) > 0:
       print 'rebin', rebin
       rebin = rebin
   else:
       rebin = rebin_value
   start_time = time.time()
   all_files = [SRfiles] if doOnlySR else [SRfiles, CRTTfiles, CRDYfiles]
   for idx, list_of_files in enumerate(all_files):
       # if 'new' in fil: continue
       # read3(fil)
       # if idx >1: continue
       #pass
     separateFilesPerVariable(list_of_files, rebin)


   #processFile(inputfile, outputfile)
   for var in variables:
       print 'processing var=', var
       if onlyPutTogetherHistsAndTexts and 'hh' not in var: continue                                                                                  
       if onlyHHMTandBDT and not ('hh' in var or 'bdt' in var): continue
       print 'after processing var=', var
       print
       copyAndCombineCards(var)


   print 'before fitting'
   if doFitting:
       doFits()
   ######################## use datacard rewriter in producePostFitRootFiles and copyAndCombineCards before doing any other work
   #print 'intentional early return'; return
   print 'before pool'
   if onlyPutTogetherHistsAndTexts:
       print 'in onlyPutTogetherHistsAndTexts returning'
       return

   pool = multiprocessing.Pool(16)  # 32
   pool.map(producePostFitRootFiles, variables)
   print 'after pool'
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

