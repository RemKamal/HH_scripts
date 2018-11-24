#!/usr/bin/python
###!/cvmfs/sft.cern.ch/lcg/views/LCG_88/x86_64-slc6-gcc49-opt/bin/python
######!/usr/bin/env python
"""
======================================
Copy a tree while overwriting branches
======================================

This is an example showing how to copy a tree while overwriting one or more of
its branches with new values.
"""

from rootpy.tree import Tree, TreeModel, FloatCol, IntCol
from rootpy.io import root_open
from ROOT import TMVA
import sys
from array import array

args_are_given = len(sys.argv) > 1
#print sys.argv[0] # script name itself                                                                                                                          
#print sys.argv[1] # 1st passed argument, file with samples
#print sys.argv[2] # 2nd passed argument, comma separated list of xml trainings

prefix = 'dataset/weights/'
if args_are_given:
    dirWithMCSamples = sys.argv[1] 
    print 'dirWithMCSamples is ', dirWithMCSamples
    
    list_of_diff_mvas = list() if len(sys.argv) < 2 else [prefix + str(x) if 'xml' in x else None for x in sys.argv[2].split(',')]
    if None in list_of_diff_mvas:
        print '"mvaXml" files should be xml format, please check.' 
        sys.exit(1)
    print 'list_of_diff_mvas is ', list_of_diff_mvas
else:
    print '"dirWithMCSamples" or "mvaXml" files are not specified, please follow the syntax W/O spaces for XMLs: python fillMvaBranchOfTrees.py "dirWithMCSamples" "mvaLowMassXml,mvaHighMassXml"'
    sys.exit(1)

weightFile_lowMass = 'dataset/weights/' + list_of_diff_mvas[0]
weightFile_highMass = 'dataset/weights/' + list_of_diff_mvas[1]


TMVA.Tools.Instance()
reader_lowMass = TMVA.Reader( "!Color:!Silent" )
reader_highMass = TMVA.Reader( "!Color:!Silent" )


# myList = ['metpt', 'dR_leps', 'dR_bjets', 'btag0', 'btag1', 'hpt0', 'hpt1', 'nbjets', 'dEta_lb_min', 'mt2_bbmet', 'mt2_ZHmet' ]
# prefix = " = array('f',[0])"
# for var in myList:
#     print var + prefix


metpt = array('f',[0])
dR_leps = array('f',[0])
dR_bjets = array('f',[0])
btag0 = array('f',[0])
btag1 = array('f',[0])
hpt0 = array('f',[0])
hpt1 = array('f',[0])
nbjets = array('f',[0])
dEta_lb_min = array('f',[0])
mt2_bbmet = array('f',[0])
mt2_ZHmet = array('f',[0])

# bpt0 = array('f',[0])
# beta0 = array('f',[0])
# bphi0 = array('f',[0])
# bpt1 = array('f',[0])
# beta1 = array('f',[0])
# #5
# bphi1 = array('f',[0])
# leppt0 = array('f',[0])
# lepeta0 = array('f',[0])
# lepphi0 = array('f',[0])
# leppt1 = array('f',[0])
# #10
# lepeta1 = array('f',[0])
# lepphi1 = array('f',[0])
# metpt = array('f',[0])
# #meteta = tree.met_eta                                                                                                                                       `
# metphi = array('f',[0])
# #14
# btag0 = array('f',[0])
# btag1 = array('f',[0])
# zmass = array('f',[0])
# zpt0 = array('f',[0])
# zeta0 = array('f',[0])
# #19
# zphi0 = array('f',[0])
# hmass0 = array('f',[0])
# hmt0 = array('f',[0])
# hpt0 = array('f',[0])
# heta0 = array('f',[0])
# #24
# hphi0 = array('f',[0])
# hToZZ_mt_cosine = array('f',[0])
# hmass1 = array('f',[0])
# hmt1 = array('f',[0])
# hpt1 = array('f',[0])
# #29
# heta1 = array('f',[0])
# hphi1 = array('f',[0])
# nbjets = array('i',[0])
# njets = array('i',[0])
# nloosebjets = array('i',[0])
# #34
# #nleps = nLeps                                                                                                                                                  
# dEta_lb_min = array('f',[0])
# dEta_ZH = array('f',[0])
# dEta_bjets = array('f',[0])
# dEta_leps = array('f',[0])
# #38
# dR_lb_min = array('f',[0])
# dR_ZH = array('f',[0])
# dR_bjets = array('f',[0])
# dR_leps = array('f',[0])
# dPhi_lb_min = array('f',[0])
# #43
# dPhi_ZH = array('f',[0])
# dPhi_bjets = array('f',[0])
# dPhi_leps = array('f',[0])
# hhmt = array('f',[0])
# hh_mt_cosine = array('f',[0])
# #48
# zhmass = array('f',[0])
# zhpt = array('f',[0])
# zheta = array('f',[0])
# zhphi = array('f',[0])
# mt2_llmet = array('f',[0])
# #53
# mt2_bbmet = array('f',[0])
# mt2_b1l1b2l2met = array('f',[0])
# mt2_b1l2b2l1met = array('f',[0])
# min_mt2_blmet = array('f',[0])
# mt2_ZHmet = array('f',[0])
# #58


# listVarNames = [
# 'bpt0',
# 'beta0',
# 'bphi0',
# 'bpt1',
# 'beta1',

# 'bphi1',
# 'leppt0',
# 'lepeta0',
# 'lepphi0',
# 'leppt1',

# 'lepeta1',
# 'lepphi1',
# 'metpt',
# #meteta = tree.met_eta                                                                                                                                                                                                                                                                                                                                                                                          
# 'metphi',
    
# 'btag0',
# 'btag1',
# 'zmass',
# 'zpt0',
# 'zeta0',
    
# 'zphi0',
# 'hmass0',
# 'hmt0',
# 'hpt0',
# 'heta0',

# 'hphi0',
# 'hToZZ_mt_cosine',
# 'hmass1',
# 'hmt1',
# 'hpt1',

# 'heta1',
# 'hphi1',
# 'nbjets',
# 'njets',
# 'nloosebjets',

# #nleps = nLeps                                                                                                                                                                                                                                                                                                                                                                                                  
# 'dEta_lb_min',
# 'dEta_ZH',
# 'dEta_bjets',
# 'dEta_leps',

# 'dR_lb_min',
# 'dR_ZH',
# 'dR_bjets',
# 'dR_leps',
# 'dPhi_lb_min',

# 'dPhi_ZH',
# 'dPhi_bjets',
# 'dPhi_leps',
# 'hhmt',
# 'hh_mt_cosine',

# 'zhmass',
# 'zhpt',
# 'zheta',
# 'zhphi',
# 'mt2_llmet',

# 'mt2_bbmet',
# 'mt2_b1l1b2l2met',
# 'mt2_b1l2b2l1met',
# 'min_mt2_blmet',
# 'mt2_ZHmet',
# ]


# listVars = [
# bpt0,
# beta0,
# bphi0,
# bpt1,
# beta1,

# bphi1,
# leppt0,
# lepeta0,
# lepphi0,
# leppt1,

# lepeta1,
# lepphi1,
# metpt,
# #meteta = tree.met_eta                                                                                                                                                                                                                                                                                                                                                                                          
# metphi,
    
# btag0,
# btag1,
# zmass,
# zpt0,
# zeta0,

# btag0,
# btag1,
# zmass,
# zpt0,
# zeta0,

# zphi0,
# hmass0,
# hmt0,
# hpt0,
# heta0,

# hphi0,
# hToZZ_mt_cosine,
# hmass1,
# hmt1,
# hpt1,

# heta1,
# hphi1,
# nbjets,
# njets,
# nloosebjets,

# #nleps = nLeps                                                                                                                                                                                                                                                                                                                                                                                                  
# dEta_lb_min,
# dEta_ZH,
# dEta_bjets,
# dEta_leps,

# dR_lb_min,
# dR_ZH,
# dR_bjets,
# dR_leps,
# dPhi_lb_min,

# dPhi_ZH,
# dPhi_bjets,
# dPhi_leps,
# hhmt,
# hh_mt_cosine,

# zhmass,
# zhpt,
# zheta,
# zhphi,
# mt2_llmet,

# mt2_bbmet,
# mt2_b1l1b2l2met,
# mt2_b1l2b2l1met,
# min_mt2_blmet,
# mt2_ZHmet,
# ]


# myList = ['metpt', 'dR_leps', 'dR_bjets', 'btag0', 'btag1', 'hpt0', 'hpt1', 'nbjets', 'dEta_lb_min', 'mt2_bbmet', 'mt2_ZHmet' ]
# prefix = 'loader.AddVariable("'
# for var in myList:
#     print prefix+var+'", ' + var + ')'

reader_lowMass.AddVariable("metpt", metpt)
reader_lowMass.AddVariable("dR_leps", dR_leps)
reader_lowMass.AddVariable("dR_bjets", dR_bjets)
reader_lowMass.AddVariable("btag0", btag0)
reader_lowMass.AddVariable("btag1", btag1)
reader_lowMass.AddVariable("hpt0", hpt0)
reader_lowMass.AddVariable("hpt1", hpt1)
reader_lowMass.AddVariable("nbjets", nbjets)
reader_lowMass.AddVariable("dEta_lb_min", dEta_lb_min)
reader_lowMass.AddVariable("mt2_bbmet", mt2_bbmet)
reader_lowMass.AddVariable("mt2_ZHmet", mt2_ZHmet)


reader_highMass.AddVariable("metpt", metpt)
reader_highMass.AddVariable("dR_leps", dR_leps)
reader_highMass.AddVariable("dR_bjets", dR_bjets)
reader_highMass.AddVariable("btag0", btag0)
reader_highMass.AddVariable("btag1", btag1)
reader_highMass.AddVariable("hpt0", hpt0)
reader_highMass.AddVariable("hpt1", hpt1)
reader_highMass.AddVariable("nbjets", nbjets)
reader_highMass.AddVariable("dEta_lb_min", dEta_lb_min)
reader_highMass.AddVariable("mt2_bbmet", mt2_bbmet)
reader_highMass.AddVariable("mt2_ZHmet", mt2_ZHmet)




# reader.AddVariable("bpt0", bpt0)
# reader.AddVariable("beta0", beta0)
# reader.AddVariable("bphi0", bphi0)
# reader.AddVariable("bpt1", bpt1)
# reader.AddVariable("beta1", beta1)

# reader.AddVariable("bphi1", bphi1)
# reader.AddVariable("leppt0", leppt0)
# reader.AddVariable("lepeta0", lepeta0)
# reader.AddVariable("lepphi0", lepphi0)
# reader.AddVariable("leppt1", leppt1)

# reader.AddVariable("lepeta1", lepeta1)
# reader.AddVariable("lepphi1", lepphi1)
# reader.AddVariable("metpt", metpt)
# reader.AddVariable("metphi", metphi)
# reader.AddVariable("btag0", btag0)

# reader.AddVariable("btag1", btag1)
# reader.AddVariable("zmass", zmass)
# reader.AddVariable("zpt0", zpt0)
# reader.AddVariable("zeta0", zeta0)
# reader.AddVariable("zphi0", zphi0)

# reader.AddVariable("hmass0", hmass0)
# reader.AddVariable("hmt0", hmt0)
# reader.AddVariable("hpt0", hpt0)
# reader.AddVariable("heta0", heta0)
# reader.AddVariable("hphi0", hphi0)

# reader.AddVariable("hToZZ_mt_cosine", hToZZ_mt_cosine)
# reader.AddVariable("hmass1", hmass1)
# reader.AddVariable("hmt1", hmt1)
# reader.AddVariable("hpt1", hpt1)
# reader.AddVariable("heta1", heta1)

# reader.AddVariable("hphi1", hphi1)
# reader.AddVariable("nbjets", nbjets)
# reader.AddVariable("njets", njets)
# reader.AddVariable("nloosebjets", nloosebjets)
# reader.AddVariable("dEta_lb_min", dEta_lb_min)

# reader.AddVariable("dEta_ZH", dEta_ZH)
# reader.AddVariable("dEta_bjets", dEta_bjets)
# reader.AddVariable("dEta_leps", dEta_leps)
# reader.AddVariable("dR_lb_min", dR_lb_min)
# reader.AddVariable("dR_ZH", dR_ZH)

# reader.AddVariable("dR_bjets", dR_bjets)
# reader.AddVariable("dR_leps", dR_leps)
# reader.AddVariable("dPhi_lb_min", dPhi_lb_min)
# reader.AddVariable("dPhi_ZH", dPhi_ZH)
# reader.AddVariable("dPhi_bjets", dPhi_bjets)

# reader.AddVariable("dPhi_leps", dPhi_leps)
# reader.AddVariable("hhmt", hhmt)
# reader.AddVariable("hh_mt_cosine", hh_mt_cosine)
# reader.AddVariable("zhmass", zhmass)
# reader.AddVariable("zhpt", zhpt)

# reader.AddVariable("zheta", zheta)
# reader.AddVariable("zhphi", zhphi)
# reader.AddVariable("mt2_llmet", mt2_llmet)
# reader.AddVariable("mt2_bbmet", mt2_bbmet)
# reader.AddVariable("mt2_b1l1b2l2met", mt2_b1l1b2l2met)

# reader.AddVariable("mt2_b1l2b2l1met", mt2_b1l2b2l1met)
# reader.AddVariable("min_mt2_blmet", min_mt2_blmet)
# reader.AddVariable("mt2_ZHmet", mt2_ZHmet)

reader_lowMass.BookMVA('BDT', weightFile_lowMass )
reader_highMass.BookMVA('BDT', weightFile_highMass )








h1 = ROOT.TH1D("h1","Classifier Output on Background Events",100,-1.0,1.0)
h2 = ROOT.TH1D("h2","Classifier Output on Signal Events",100,-1.0,1.0)

samplesList = []
for root, dirs, files in os.walk(dirWithMCSamples):
    for name in files:
        if 'tree.root' in name:
            massPoint = name[14:-18]
            samplesList.append (name, massPoint)


print samplesList
sys.exit(1)
print 'all is fine, specifically exiting early.'



lowMassRegion = [260, 270, 300, 350, 400, 450]
highMassRegion = [600, 650, 900, 1000]

for sample in samplesList:
    if sample:
        # first open the file and load tree
        f = root_open(sample, "read")
        tree = Tree("tree") #, model=Event)
        
        """
        This section below takes the input tree and copies it while overwriting a
        branch with new values.
        """

        # Now we want to copy the tree above into a new file while overwriting a branch
        # First create a new file to save the new tree in:
        f_copy = root_open(sample[:-5] + "_withMva.root", "recreate")
        
        # You may not know the entire model of the original tree but only the branches
        # you intend to overwrite, so I am not specifying the model=Event below as an
        # example of how to deal with this in general:
        tree_copy = Tree("tree")
        
        # Here we specify the buffer for the new tree to use. We use the same buffer as
        # the original tree. This creates all the same branches in the new tree but
        # their addresses point to the same memory used by the original tree.
        tree_copy.set_buffer(tree._buffer, create_branches=True)
        mass = sample[14:-18]
        # Now loop over the original tree and fill the new tree
        for entry in tree:
            # Overwrite a branch value. This changes the value that will be written to
            # the new tree but leaves the value unchanged in the original tree on disk.

            if 'Bulk' in sample and mass > 450: 
                entry.bdtOutput = reader_highMass.EvaluateMVA("BDT")
            else:
                # for low mass signal and all BG's use low mass BDT
                entry.bdtOutput = reader_lowMass.EvaluateMVA("BDT")   
            #entry.bdtOutput_multiclass = reader.EvaluateMVA("BDTG")
            #entry.dnnOutput = reader.EvaluateMVA("DNN")
            # "entry" is actually the buffer, which is shared between both trees.
            tree_copy.Fill()

    
        # tree_copy is now a copy of tree where the "mva" branches have been overwritten with new values
        tree_copy.Write()
        f_copy.Close()
        f.Close()
