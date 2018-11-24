from ROOT import TFile
import ROOT
import sys

import pprint as pp

fname = 'plotter.root'
beforeBDTcutDir = 'bdt_response'
postFix = '_afterCut'
afterBDTcutDir = beforeBDTcutDir + postFix

runEE = True

ee_dirs = ['low_SR_0.4', 'low_SR_0.925', 'high_SR_0.99']
mm_dirs = ['low_SR_0.1', 'low_SR_0.7', 'high_SR_0.99']

#shapes_nominal/    /plots/Stack/     300/   plotter.root



def read_before_cut(fname, cutDir):
    print 'fname is', fname
    shapes_file = ROOT.TFile.Open(fname)
    print 'ROOT tfile path is', shapes_file

    print 'list of Keys is', ROOT.gDirectory.GetListOfKeys().ls()
    print 'gonna cd'
    print shapes_file.cd(cutDir)
    shapes = ROOT.gDirectory.GetListOfKeys()
    hists = []
    print shapes

        # Since the nominal and varied shapes share the same binning,
        # take any of the histograms found in the shapes file.
    dict_process_vs_events = {}
    for idx, shape in enumerate(shapes):
        shape = ROOT.gDirectory.Get(shapes[idx].GetName())
        #print 'before draw'
        #shape.Print()
        name = shape.GetName()
        if 'data' in name: continue
        nEntries = shape.GetEntries()
        print 'shape.GetEntries():', shape.GetEntries()
        
        dict_process_vs_events[name] = nEntries
    #print dict_process_vs_events
    return dict_process_vs_events



    if False:
            #inp = ROOT.TFile.Open(inputfile,'read')
        output = ROOT.TFile.Open(tmpfile,'recreate')
        output.mkdir(beforeBDTcutDir)
        output.cd(beforeBDTcutDir)
        for h in hists:
            h.Write()#key.GetName())
        output.Close()
        
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


dirs = ee_dirs if runEE else mm_dirs

pref = 'shapes_nominal/'
masses = [260, 270, 300, 350, 400, 450, 600, 650, 900, 1000]
#masses = [300, 900]

dict_masses_before_cut = {}
dict_masses_after_cut = {}
for m in masses:
    for d in dirs:
        fileIn = pref + d + '/plots/Stack/' + str(m) + '/plotter.root'
        if runEE:
            if m < 400 and '0.4' not in d: continue
            if 400 <= m <=450 and '0.925' not in d: continue
            if m >= 600 and '0.99' not in d: continue
        else:
            if m <= 270 and '0.1'not in d: continue
            if 300 <= m<=450 and '0.7' not in d: continue
            if m >= 600and '0.99' not in d: continue
        print 'processing mass = ', m
        dict_masses_before_cut[m] = read_before_cut(fileIn, beforeBDTcutDir)
        dict_masses_after_cut[m] = read_before_cut(fileIn, afterBDTcutDir)
        
print 'dict_masses_before_cut:'
pp.pprint(dict_masses_before_cut)
print '~'*200
print 'dict_masses_after_cut:'
pp.pprint(dict_masses_after_cut)
print '-'*200


import collections

dict_masses_before_cut = collections.OrderedDict(sorted(dict_masses_before_cut.items()))
dict_masses_after_cut = collections.OrderedDict(sorted(dict_masses_after_cut.items()))

dict_mass_vs_eff = collections.OrderedDict()

print '='*200
ZH_list, ST_list, TT_list, DY_list, VV_list, HZZ_list, HWW_list = [] ,[], [], [] ,[], [], []

for (k_bef, innerDic_bef), (k_aft, innerDic_aft) in zip (dict_masses_before_cut.items(), dict_masses_after_cut.items()):
    #print k_bef, ':', innerDic_bef
    #print k_aft, ':', innerDic_aft
    innerDic_bef = collections.OrderedDict(sorted(innerDic_bef.items()))
    innerDic_aft = collections.OrderedDict(sorted(innerDic_aft.items()))

    print k_bef
    if k_bef == k_aft:
        for (k1, v1), (k2, v2) in zip (innerDic_bef.items(), innerDic_aft.items()):
            print
            print k1, ':', v1
            print k2, ':', v2
            #print '-'
            if k1 in k2:
                eff = round(100.*v2/v1, 1)
                print 'for mass={0} , for process {1}, eff = {2}'.format(k_bef, k1, eff) 
                if 'ST' in k1:
                    ST_list.append(eff)
                elif 'TT' in k1:
                    TT_list.append(eff)
                elif 'DY' in k1:
                    DY_list.append(eff)
                elif 'ZH' in k1:
                    ZH_list.append(eff)
                elif 'VV' in k1:
                    VV_list.append(eff)
                elif 'ZZ' in k1:
                    HZZ_list.append(eff)
                elif 'WW' in k1:
                    HWW_list.append(eff)

process_names = ['ZH', 'Single top', 'TT', 'Drell-Yan', 'Dibosons', 'signa_hzz', 'signal_hww']
leptType = 'ee_' if runEE else 'mm_'
for idx, process in enumerate([ZH_list, ST_list, TT_list, DY_list, VV_list, HZZ_list, HWW_list]):
    print '{0}eff_array_{1} = {2}'.format(leptType, process_names[idx], process)


