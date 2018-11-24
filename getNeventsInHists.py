from ROOT import TFile
import ROOT
import glob
import sys
import time
import pprint
files_of_interest = glob.glob("*.input.root")
print files_of_interest

CRDYfiles = [x for x in files_of_interest if 'CRDY.' in x and ('CMS' in x or 'nominal' in x)]
CRTTfiles = [x for x in files_of_interest if 'CRTT.' in x and ('CMS' in x or 'nominal' in x)]
SRfiles = [x for x in files_of_interest if 'SR.' in x and ('CMS' in x or 'nominal' in x)]
dict_events = {}

files_of_interest_mm = [
    "hhMt_nominal_mm_CRDYlow.input.root",
    "hhMt_nominal_mm_CRDY.input.root",
    "hhMt_nominal_mm_CRDYhigh.input.root",
    "hhMt_nominal_mm_CRTT.input.root"
    ]

files_of_interest_ee = [
    "hhMt_nominal_ee_CRDYlow.input.root",
    "hhMt_nominal_ee_CRDY.input.root",
    "hhMt_nominal_ee_CRDYhigh.input.root",
    "hhMt_nominal_ee_CRTT.input.root"
    ]

if glob.glob('*mm*') == []:
    files_of_interest = files_of_interest_ee
else:
    files_of_interest =files_of_interest_mm




dict_rename = {
    "eff_b_heavy" : "btag_heavy",
    "eff_b_light" : "btag_light",
    "WW" : "hww",
    "ZZ" : "hzz",
    #
    }


def getNevents(fil):

    innerDir = '_'.join(fil.split('input')[0].split('_')[-2:])[:-1]
    print 'innerDir', innerDir
    region = fil.split('input')[0].split('_')[-1][:-1]
    print 'region',region
    dict_events[region] = {}

    shapes_file = ROOT.TFile.Open(fil, 'read')
    print shapes_file.cd(innerDir)
    shapes = ROOT.gDirectory.GetListOfKeys()
    for idx, shape in enumerate(shapes):
        shape = ROOT.gDirectory.Get(shapes[idx].GetName())
        print 'before draw'
        dict_events[region][shape.GetName()] = shape.Integral()#GetEntries()
        
            #shape.Print()
            #shap = shape.Clone()
        #shape.SetDirectory(0)
            #hists.append (shape)
        #if shape.GetName() not in hists:
                #hists.add (shape)
         #   hists[shape.GetName()] = shape


    #print 'hists', hists
    #print 'len(hists)', len(hists)
    return 

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
        


def putTogetherHists(files):

    #print 'files:'
    #print files

    print 
    
    print 'files[0]', files[0]
    innerDir = '_'.join(files[0].split('input')[0].split('_')[-2:])[:-1]
    print 'innerDir', innerDir
    tmpfile = 'hhMt_' + innerDir  + '.input.root' #hhMt_mm_SR.input.root
    print 'tmpfile', tmpfile
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


def normaliseDictionary(dict_btagMedium_ee_350):
    new_dict_btagMedium_ee_350 = {}
    for k, v in dict_btagMedium_ee_350.items():
    #if 'CRDY' != k: continue
        print (k)
        print (v)
        BGs = [va for ke, va in v.items() if 'data' not in ke]
    #print ('BGs', BGs)
        totBG = sum(BGs)
        print ('totBG', totBG)
        factor = 1./totBG
    #print (factor)
        new_dict_btagMedium_ee_350[k] = {}
        for key, val in v.items():
        #print (val)
            val = val*factor
            print (key, val)
            new_dict_btagMedium_ee_350[k][key] = val
        print ('----------------')
    return new_dict_btagMedium_ee_350

start = time.time()
for idx, fil in enumerate(files_of_interest):
    #if 'new' in fil: continue
    #read3(fil)
    #if idx >1: continue
    getNevents(fil)

pprint.pprint(dict_events)
#new_dict_events = {}

new_dict_events = normaliseDictionary(dict_events)
print
print 'new_dict_events = '
pprint.pprint(new_dict_events)


end = time.time()
print
print "it took {0} seconds".format(end-start)
