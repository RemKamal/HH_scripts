from ROOT import TFile
import os
import ROOT
import glob
import sys
import time
import re
import shutil
from array import array
import sys

# channels = glob.glob("dataCard_hhMt_mm.txt")
# if channels == []:
#     channel = "ee"
# else:
#     channel = "mm"

channel = os.getcwd().split('_')[-2]

if channel == "eles":
    channel = "ee"
else:
    channel = "mm"
#channels = ["mm", "ee"]

mass = int(os.getcwd().split('_')[-1])
rebin_dict = {
    260: 1,
    270: 1,
    300: 2, #!
    350: 1,

    400: 4, #?
    450: 2, #2?


    451: 2, #?

    600: 5,
    650: 10,
    900: 5, #10 for mm
    1000: 5
    }

rebin = rebin_dict[mass]

prefix = "new_"

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

dcards = [
    "dataCard_CRDY_hhMt.txt",
    "dataCard_CRTT_hhMt.txt",
    "dataCard_SR_hhMt.txt"
    ]
#for dc in dcards:
 #   if not os.path.exists("original_"+d):
  #      shutil.copyfile(d, "original_"+d) 

files_of_interest = glob.glob("*.input.root")
files_of_interest = [x for x in files_of_interest if "new_" not in x]
#print files_of_interest

CRDYfiles = [x for x in files_of_interest if 'CRDY' in x and not ('CMS' in x or 'nominal' in x) and 'eff_met' not in x]
CRTTfiles = [x for x in files_of_interest if 'CRTT.' in x and not ('CMS' in x or 'nominal' in x) and 'eff_met' not in x]
SRfiles = [x for x in files_of_interest if 'SR.' in x and not ('CMS' in x or 'nominal' in x) and 'eff_met' not in x]

dict_rename = {
    "eff_b_heavy" : "btag_heavy",
    "eff_b_light" : "btag_light",
    "WW" : "hww",
    "ZZ" : "hzz",
    #
    }

def separateFilesPerVariable(files, channel):
    print 'files=', files
    print
    for var in variables:
        #if 'hh' not in var: continue
        print 'processing var=', var
        print
        tmp_files = [x for x in files if var in x and channel in x]
        print 'tmp_files=', tmp_files
        print
        print ' len(tmp_files)', len(tmp_files)
        print '-'*100
        if tmp_files == []: continue
        putTogetherHists(tmp_files)
        

def putTogetherHists(files):

    #print 'files:'
    #print files
    
    print 
    
    print 'files[0]', files[0]
    innerDir = '_'.join(files[0].split('input')[0].split('_')[-2:])[:-1]
    print 'innerDir', innerDir
    #varName = re.split(r'(CMS|nominal)\s*', files[0])[0] #say zmass_high_
    varName = re.split(r'(.input.)\s*', files[0])[0] #say zmass_high_
    #if 'hma' not in varName: return
    print 'varName=', varName
    #tmpfile = prefix + varName + innerDir  + '.input.root' #hhMt_mm_SR.input.root
    #tmpfile = varName + '.input.root' #hhMt_mm_SR.input.root
    tmpfile = prefix + varName + '.input.root'
    print 'tmpfile', tmpfile
    

    #inf = glob.glob("hh*root")
    #for f in inf:
        #shutil.copyfile(f, "original_"+f)

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
            if False:#'data' in shape.GetName(): 
                for bin in shape:
                    print 'bin=', bin
            #print 'before draw'
            if rebin > 1 and 'SR' in innerDir:
                #print 'Rebining...'
                #Double_t xbins[25] = {...} array of low-edges (xbins[25] is the upper edge of last bin
                #h1->Rebin(24,"hnew",xbins);  //creates a new variable bin size histogram hnew
                xbins_list = []
                #array("d", [])
                nbins=shape.GetNbinsX() 
                #print nbins
                #print shape.GetXaxis().GetBinWidth(nbins)/2
                #print shape.GetBinLowEdge(1)
                #print shape.GetBinCenter(nbins)
                #print shape.GetBinCenter(nbins) + shape.GetXaxis().GetBinWidth(nbins)/2
                #firstBin = shape.GetBinLowEdge(1)
                #thirdBin = 
                if channel == "mm" and int(mass) == 900:
                    rebin_factor = 10
                #elif channel == "mm" and int(mass) == 650:
                 #   rebin_factor = 20
                else:
                    rebin_factor = rebin
                dummy_var = 0
                for i in range(1, nbins+1, rebin_factor):
                    #print i
                    dummy_var = i
                    #print shape.GetBinContent(i)
                    xbins_list.append(shape.GetBinLowEdge(i))
                #for idx, bin in enumerate(shape, start=1):
                 #   print 'idx', idx
                  #  print 'bin', bin
                   # print 'shape.GetBinLowEdge(idx)', shape.GetBinLowEdge(idx)
                if dummy_var < nbins:
                    xbins_list.append(shape.GetBinCenter(nbins) + shape.GetXaxis().GetBinWidth(nbins)/2)
                xbins = array("d", xbins_list)
                #print 'xbins=', xbins
                if nbins%rebin_factor !=0 and xbins_list != []:
                    print 'rebinning with a variable length, rebin=', rebin_factor
                    shape = shape.Rebin(len(xbins)-1, shape.GetName(), xbins)
                    #https://root-forum.cern.ch/t/rebbing-a-histogram-in-pyroot/17862
                    #https://github.com/brynmathias/pyRootUtils/blob/master/plottingUtils.py#L227
                else:
                # data_hist = ROOT.TH1F("data_hist","data_hist",nbins,DY.GetBinLowEdge(1),DY.GetBinCenter(nbins)+DY.GetXaxis().GetBinWidth(nbins)/2) 
                    print 'simple rebinning, rebin=', rebin_factor
                    shape.Rebin(rebin_factor)
                #for idx, bin in enumerate(shape, start=1):
                 #   print idx
                  #  print bin
                   # print 'shape.GetBinLowEdge(idx)', shape.GetBinLowEdge(idx) 
            if False:#'data' in shape.GetName():
                for bin in shape:
                    print 'bin=', bin
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
        if int(mass) == 600 and 'signal_hww_CMS_scale_jDown' not in hists:
            hists['signal_hww_CMS_scale_jDown'] = hists['signal_hww_CMS_scale_jUp'].Clone()
            print '*'*200
            print 'just created %s in the file %s' % (hists['signal_hww_CMS_scale_jDown'] , output)
        for k,v in hists.items():
        
            #for (k, v) in dict_rename.items():
             #   if k in h.GetName():
              #      h.SetName(h.GetName().replace(k, v))
            #h.Write()#key.GetName())
            #https://root.cern.ch/input-and-output
            #https://root.cern.ch/root/htmldoc/guides/users-guide/InputOutput.html#retrieving-objects-from-disk
            v.Write(k ,ROOT.TObject.kOverwrite)#key.GetName())
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




start = time.time()
files_to_pass = [SRfiles, CRTTfiles, CRDYfiles]
#files_to_pass = [CRTTfiles]

for idx, list_of_files in enumerate(files_to_pass):
    #if 'new' in fil: continue
    #read3(fil)
    #if idx >1: continue
    #for channel in channels:
    separateFilesPerVariable (list_of_files, channel)

end = time.time()
print
print "it took {0} seconds".format(end-start)
