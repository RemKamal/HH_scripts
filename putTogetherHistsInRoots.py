from ROOT import TFile
import ROOT
import glob
import sys
import time
import re

vars = [
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

CRDYfiles = [x for x in files_of_interest if 'CRDY' in x and ('CMS' in x or 'nominal' in x) and 'eff_met' not in x]
CRTTfiles = [x for x in files_of_interest if 'CRTT.' in x and ('CMS' in x or 'nominal' in x) and 'eff_met' not in x]
SRfiles = [x for x in files_of_interest if 'SR.' in x and ('CMS' in x or 'nominal' in x) and 'eff_met' not in x]

dict_rename = {
    "eff_b_heavy" : "btag_heavy",
    "eff_b_light" : "btag_light",
    "WW" : "hww",
    "ZZ" : "hzz",
    #
    }

def separateFilesPerVariable(files):
    print 'files=', files
    print
    for var in vars:
        #if 'hh' not in var: continue
        print 'processing var=', var
        print
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
for idx, list_of_files in enumerate([SRfiles, CRTTfiles, CRDYfiles]):
    #if 'new' in fil: continue
    #read3(fil)
    #if idx >1: continue
    separateFilesPerVariable (list_of_files)

end = time.time()
print
print "it took {0} seconds".format(end-start)
