from rootpy.io import root_open
import time 
from array import array
import math
import pprint
nameDir = 'shapes'


debugMode = True # for priting with bazinga                                 
def bazinga (mes):
    if debugMode:
        print mes

methodName = 'BDT'

import ROOT
from ROOT import TMVA
import sys, os

muonRun = os.path.exists("DoubleMuon__Run2016E-03Feb2017-v1_minitree.root")
eleRun = os.path.exists("DoubleEG__Run2016D-03Feb2017-v1_minitree.root")

if muonRun and eleRun:
    print 'cannot happen, exiting...'
    sys.exit(1)
elif eleRun:
    print 'doing eleRun'
elif muonRun:
    print 'doing muonRun'
else:
    print 'cannot happen, either eleRun or muonRun have to be processed, exiting...'
    sys.exit(1)


#for histograms
Zmasslow = 76
Zmassmid, Zmasshigh = 106, 155
Hbb_mass_binMin, Hbb_mass_binMax = 20, 220 
hmass1_oneBin_binning = array('f', [20, 90, 150, 220])

Hzz_mass_binMin, Hzz_mass_binMax = 75, 175
Zpt_binMax = 300
Hzz_pt_binMax = 300
Hbb_pt_binMax = 300
met_pt_binMax = 350
dR_binMax = 8 






start_time = time.time()

args_are_given = len(sys.argv) > 1
#print sys.argv[0] # script name itselight                                                                                            
#print sys.argv[1] # 1st passed argument, file with samples                                                                        #print sys.argv[2] # 2nd passed argument, comma separated list of xml trainings                                                         

prefix = 'dataset/weights/'
if args_are_given:
    print 'syntax: python createHHMTforCombine_reader_v2.py dirWithMCSamples mva1,mva2 physRegion bdtCut massRegion'
    dirWithMCSamples = sys.argv[1] # has to contain 10 Hzz, 10 Hww, and 17 BG samples
    print 'dirWithMCSamples is ', dirWithMCSamples

    list_of_diff_mvas = list() if len(sys.argv) < 2 else [prefix + str(x) if 'xml' in x else None for x in sys.argv[2].split(',')]
    if None in list_of_diff_mvas:
        print '"mvaXml" files should be xml format, please check.'
        sys.exit(1)
    print 'list_of_diff_mvas is ', list_of_diff_mvas

    if len(sys.argv) > 3:
        physRegion = sys.argv[3]
        if physRegion not in {"SR", "CRTT", "CRDY", "CRDYlow", "CRDYhigh", "CRDYoneBin", "CRTToneBin"}:
            print 'wrong "physRegion", please use "region:"SR", "CRTT", "CRDY", "CRDYlow", "CRDYhigh", "CRTToneBin", "CRDYoneBin"'
            sys.exit(1)
    else:
        print 'not specified "physRegion", please use "region:"SR", "CRTT", "CRDY", "CRDYlow", "CRDYhigh", "CRTToneBin", "CRDYoneBin"'
        sys.exit(1)


    if len(sys.argv) > 4:
        bdtCut = float(sys.argv[4])
        if -1 <= bdtCut <= 1:
            print 'bdtCut is ', bdtCut
            pass
        else:
            print 'BDT value is outside of the range [-1,1], please check the input'
            sys.exit(1)
    else:
        print 'please specify bdtCut value'
        sys.exit(1)

    if len(sys.argv) > 5:
        massRegion = sys.argv[5]
        if massRegion in {'low', 'high'}:
            print 'massRegion is ', massRegion
            pass
        else:
            print 'wrong mass region, please use "low or high", exiting.'
            sys.exit(1)
    else:
        print 'please specify massRegion value: "low or high"'
        sys.exit(1)

    if len(sys.argv) > 6:
        systUnc = sys.argv[6]
        print 'systUnc is', systUnc
        pass
        #else:
         #   print 'wrong mass region, please use "low or high", exiting.'
          #  sys.exit(1)
    else:
        systUnc = 'nominal'
        #print 'please specify systUnc, exiting...'
        #sys.exit(1)

    # if len(sys.argv) > 7:
    #     specialRegion = sys.argv[7]
    #     if specialRegion in {"CRDYlow", "CRDYhigh", "CRoneBin", "standard"}:
    #         print 'specialRegion is ', specialRegion
    #         pass
    #     else:
    #         print 'wrong special region, please use "CRDYlow", "CRDYhigh", "oneBin, "standard"}", exiting.'
    #         sys.exit(1)
    # else:
    #     print 'please specify specialRegion value: "CRDYlow", "CRDYhigh", "oneBin", "standard"'
    #     sys.exit(1)


else:
    print '"dirWithMCSamples" or "mvaXml" files are not specified, please follow the syntax W/O spaces for XMLs: python createHHMTforCombine_reader.py "dirWithMCSamples" "mvaLowMassXml,mvaHighMassXml" "region:SR/CRDY/CRTT"'
    sys.exit(1)

weightFile_lowMass = list_of_diff_mvas[0]
weightFile_highMass =  list_of_diff_mvas[1]

nameDir += '_' + systUnc + '/'

myVars = [  
        'zmass', 
        'met_pt', 
        'hmass0',
    
        'hmass1',
        'dR_leps',
        'dR_bjets',

        'zpt0',
        'hpt0',
        'hpt1'
]

post = " = array('f',[0])"

for v in myVars:
    print v + post
    


# metpt = array('f',[0])
# dR_leps = array('f',[0])
# dR_bjets = array('f',[0])
# btag0 = array('f',[0])
# btag1 = array('f',[0])
# hpt0 = array('f',[0])
# hpt1 = array('f',[0])
# nbjets = array('f',[0])
# dEta_lb_min = array('f',[0])
# mt2_bbmet = array('f',[0])
# mt2_ZHmet = array('f',[0])


pref = 'reader_lowMass.AddVariable("'
post = '", '

for v in myVars:
    print pref + v + post + v + ')'



# reader_lowMass.AddVariable("metpt", metpt)
# reader_lowMass.AddVariable("dR_leps", dR_leps)
# reader_lowMass.AddVariable("dR_bjets", dR_bjets)
# reader_lowMass.AddVariable("btag0", btag0)
# reader_lowMass.AddVariable("btag1", btag1)
# reader_lowMass.AddVariable("hpt0", hpt0)
# reader_lowMass.AddVariable("hpt1", hpt1)
# reader_lowMass.AddVariable("nbjets", nbjets)
# reader_lowMass.AddVariable("dEta_lb_min", dEta_lb_min)
# reader_lowMass.AddVariable("mt2_bbmet", mt2_bbmet)
# reader_lowMass.AddVariable("mt2_ZHmet", mt2_ZHmet)

 
# reader_highMass.AddVariable("metpt", metpt)
# reader_highMass.AddVariable("dR_leps", dR_leps)
# reader_highMass.AddVariable("dR_bjets", dR_bjets)
# reader_highMass.AddVariable("btag0", btag0)
# reader_highMass.AddVariable("btag1", btag1)
# reader_highMass.AddVariable("hpt0", hpt0)
# reader_highMass.AddVariable("hpt1", hpt1)
# reader_highMass.AddVariable("nbjets", nbjets)
# reader_highMass.AddVariable("dEta_lb_min", dEta_lb_min)
# reader_highMass.AddVariable("mt2_bbmet", mt2_bbmet)
# reader_highMass.AddVariable("mt2_ZHmet", mt2_ZHmet)


zz_sigInputFile_GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M_1000_narrow_13TeV_madgraph__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v2 = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-1000_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v2_minitree.root")

zz_sigInputFile_GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M_250_narrow_13TeV_madgraph__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-250_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root")

zz_sigInputFile_GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M_260_narrow_13TeV_madgraph__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-260_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root")

zz_sigInputFile_GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M_270_narrow_13TeV_madgraph__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-270_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root")

zz_sigInputFile_GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M_300_narrow_13TeV_madgraph__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-300_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root")

zz_sigInputFile_GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M_350_narrow_13TeV_madgraph__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-350_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root")

zz_sigInputFile_GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M_400_narrow_13TeV_madgraph__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-400_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root")

zz_sigInputFile_GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M_450_narrow_13TeV_madgraph__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-450_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root")

zz_sigInputFile_GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M_500_narrow_13TeV_madgraph__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-500_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root")

zz_sigInputFile_GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M_550_narrow_13TeV_madgraph__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-550_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root")

zz_sigInputFile_GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M_600_narrow_13TeV_madgraph__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-600_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root")

zz_sigInputFile_GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M_650_narrow_13TeV_madgraph__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-650_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root")

zz_sigInputFile_GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M_700_narrow_13TeV_madgraph__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-700_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root")

zz_sigInputFile_GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M_750_narrow_13TeV_madgraph__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-750_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root")

zz_sigInputFile_GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M_800_narrow_13TeV_madgraph__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-800_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root")

zz_sigInputFile_GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M_900_narrow_13TeV_madgraph__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-900_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root")

ww_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_1000_narrow_13TeV_madgraph_HWW = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-1000_narrow_13TeV-madgraph_HWW_minitree.root")

ww_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_260_narrow_13TeV_madgraph_HWW = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-260_narrow_13TeV-madgraph_HWW_minitree.root")

ww_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_270_narrow_13TeV_madgraph_HWW = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-270_narrow_13TeV-madgraph_HWW_minitree.root")

ww_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_300_narrow_13TeV_madgraph_HWW = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-300_narrow_13TeV-madgraph_HWW_minitree.root")

ww_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_350_narrow_13TeV_madgraph_HWW = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-350_narrow_13TeV-madgraph_HWW_minitree.root")

ww_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_400_narrow_13TeV_madgraph_HWW = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-400_narrow_13TeV-madgraph_HWW_minitree.root")

ww_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_450_narrow_13TeV_madgraph_HWW = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-450_narrow_13TeV-madgraph_HWW_minitree.root")

ww_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_600_narrow_13TeV_madgraph_HWW = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-600_narrow_13TeV-madgraph_HWW_minitree.root")

ww_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_650_narrow_13TeV_madgraph_HWW = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-650_narrow_13TeV-madgraph_HWW_minitree.root")

ww_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_900_narrow_13TeV_madgraph_HWW = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-900_narrow_13TeV-madgraph_HWW_minitree.root")

bgInputFile_DY1JetsToLL_M_50_TuneCUETP8M1_13TeV_madgraphMLM_Py8__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 = ROOT.TFile(dirWithMCSamples + "DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root")

bgInputFile_DY2JetsToLL_M_50_TuneCUETP8M1_13TeV_madgraphMLM_Py8__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 = ROOT.TFile(dirWithMCSamples + "DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root")

bgInputFile_DY3JetsToLL_M_50_TuneCUETP8M1_13TeV_madgraphMLM_Py8__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 = ROOT.TFile(dirWithMCSamples + "DY3JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root")

bgInputFile_DY4JetsToLL_M_50_TuneCUETP8M1_13TeV_madgraphMLM_Py8__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 = ROOT.TFile(dirWithMCSamples + "DY4JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root")

bgInputFile_ST_s_channel_4f_leptonDecays_13TeV_amcatnlo_Py8_TuneCUETP8M1__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 = ROOT.TFile(dirWithMCSamples + "ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-Py8_TuneCUETP8M1__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root")

bgInputFile_ST_t_channel_antitop_4f_inclusiveDecays_13TeV_powhegV2_madspin_Py8_TuneCUETP8M1__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 = ROOT.TFile(dirWithMCSamples + "ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-Py8_TuneCUETP8M1__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root")

bgInputFile_ST_t_channel_top_4f_inclusiveDecays_13TeV_powhegV2_madspin_Py8_TuneCUETP8M1__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 = ROOT.TFile(dirWithMCSamples + "ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-Py8_TuneCUETP8M1__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root")

#bgInputFile_ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV_powheg_TuneCUETP8M1__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_ext1_v1 = ROOT.TFile(dirWithMCSamples + "ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext1-v1_minitree.root")

bgInputFile_ST_tW_antitop_5f_inclusiveDecays_13TeV_powheg_Py8_TuneCUETP8M1__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_ext1_v1 = ROOT.TFile(dirWithMCSamples + "ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-Py8_TuneCUETP8M1__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext1-v1_minitree.root")

#bgInputFile_ST_tW_top_5f_NoFullyHadronicDecays_13TeV_powheg_TuneCUETP8M1__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_ext1_v1 = ROOT.TFile(dirWithMCSamples + "ST_tW_top_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext1-v1_minitree.root")

bgInputFile_ST_tW_top_5f_inclusiveDecays_13TeV_powheg_Py8_TuneCUETP8M1__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_ext1_v1 = ROOT.TFile(dirWithMCSamples + "ST_tW_top_5f_inclusiveDecays_13TeV-powheg-Py8_TuneCUETP8M1__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext1-v1_minitree.root")

bgInputFile_TT_TuneCUETP8M2T4_13TeV_powheg_Py8__RunIISummer16MAv2_PUMoriond17_backup_80r2as_2016_TrancheIV_v6_v1 = ROOT.TFile(dirWithMCSamples + "TT_TuneCUETP8M2T4_13TeV-powheg-Py8__RunIISummer16MAv2-PUMoriond17_backup_80r2as_2016_TrancheIV_v6-v1_minitree.root")

bgInputFile_WW_TuneCUETP8M1_13TeV_Py8__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 = ROOT.TFile(dirWithMCSamples + "WW_TuneCUETP8M1_13TeV-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root")

bgInputFile_WZ_TuneCUETP8M1_13TeV_Py8__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 = ROOT.TFile(dirWithMCSamples + "WZ_TuneCUETP8M1_13TeV-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root")

bgInputFile_ZH_HToBB_ZToLL_M125_13TeV_amcatnloFXFX_madspin_Py8__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 = ROOT.TFile(dirWithMCSamples + "ZH_HToBB_ZToLL_M125_13TeV_amcatnloFXFX_madspin_Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root")

bgInputFile_ZZ_TuneCUETP8M1_13TeV_Py8__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 = ROOT.TFile(dirWithMCSamples + "ZZ_TuneCUETP8M1_13TeV-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root")


if muonRun:
    dataInputFile_DoubleMuon__Run2016B_03Feb2017_ver1_v1 = ROOT.TFile(dirWithMCSamples + "DoubleMuon__Run2016B-03Feb2017_ver1-v1_minitree.root")
    
    dataInputFile_DoubleMuon__Run2016B_03Feb2017_ver2_v2 = ROOT.TFile(dirWithMCSamples + "DoubleMuon__Run2016B-03Feb2017_ver2-v2_minitree.root")
    
    dataInputFile_DoubleMuon__Run2016C_03Feb2017_v1 = ROOT.TFile(dirWithMCSamples + "DoubleMuon__Run2016C-03Feb2017-v1_minitree.root")
    
    dataInputFile_DoubleMuon__Run2016D_03Feb2017_v1 = ROOT.TFile(dirWithMCSamples + "DoubleMuon__Run2016D-03Feb2017-v1_minitree.root")
    
    dataInputFile_DoubleMuon__Run2016E_03Feb2017_v1 = ROOT.TFile(dirWithMCSamples + "DoubleMuon__Run2016E-03Feb2017-v1_minitree.root")

    dataInputFile_DoubleMuon__Run2016F_03Feb2017_v1 = ROOT.TFile(dirWithMCSamples + "DoubleMuon__Run2016F-03Feb2017-v1_minitree.root")

    dataInputFile_DoubleMuon__Run2016G_03Feb2017_v1 = ROOT.TFile(dirWithMCSamples + "DoubleMuon__Run2016G-03Feb2017-v1_minitree.root")
    
    dataInputFile_DoubleMuon__Run2016H_03Feb2017_ver2_v1 = ROOT.TFile(dirWithMCSamples + "DoubleMuon__Run2016H-03Feb2017_ver2-v1_minitree.root")

    dataInputFile_DoubleMuon__Run2016H_03Feb2017_ver3_v1 = ROOT.TFile(dirWithMCSamples + "DoubleMuon__Run2016H-03Feb2017_ver3-v1_minitree.root")

else:
    dataInputFile_DoubleEG__Run2016B_03Feb2017_ver1_v1 = ROOT.TFile(dirWithMCSamples + "DoubleEG__Run2016B-03Feb2017_ver1-v1_minitree.root")

    dataInputFile_DoubleEG__Run2016B_03Feb2017_ver2_v2 = ROOT.TFile(dirWithMCSamples + "DoubleEG__Run2016B-03Feb2017_ver2-v2_minitree.root")

    dataInputFile_DoubleEG__Run2016C_03Feb2017_v1 = ROOT.TFile(dirWithMCSamples + "DoubleEG__Run2016C-03Feb2017-v1_minitree.root")

    dataInputFile_DoubleEG__Run2016D_03Feb2017_v1 = ROOT.TFile(dirWithMCSamples + "DoubleEG__Run2016D-03Feb2017-v1_minitree.root")

    dataInputFile_DoubleEG__Run2016E_03Feb2017_v1 = ROOT.TFile(dirWithMCSamples + "DoubleEG__Run2016E-03Feb2017-v1_minitree.root")

    dataInputFile_DoubleEG__Run2016F_03Feb2017_v1 = ROOT.TFile(dirWithMCSamples + "DoubleEG__Run2016F-03Feb2017-v1_minitree.root")
    
    dataInputFile_DoubleEG__Run2016G_03Feb2017_v1 = ROOT.TFile(dirWithMCSamples + "DoubleEG__Run2016G-03Feb2017-v1_minitree.root")
    
    dataInputFile_DoubleEG__Run2016H_03Feb2017_ver2_v1 = ROOT.TFile(dirWithMCSamples + "DoubleEG__Run2016H-03Feb2017_ver2-v1_minitree.root")
    
    dataInputFile_DoubleEG__Run2016H_03Feb2017_ver3_v1 = ROOT.TFile(dirWithMCSamples + "DoubleEG__Run2016H-03Feb2017_ver3-v1_minitree.root")





# minizz_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_1000_narrow_13TeV_madgraph_Hzz = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-1000_narrow_13TeV-madgraph_Hzz_minitree.root")

# minizz_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_260_narrow_13TeV_madgraph_Hzz = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-260_narrow_13TeV-madgraph_Hzz_minitree.root")

# minizz_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_270_narrow_13TeV_madgraph_Hzz = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-270_narrow_13TeV-madgraph_Hzz_minitree.root")

# minizz_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_300_narrow_13TeV_madgraph_Hzz = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-300_narrow_13TeV-madgraph_Hzz_minitree.root")

# minizz_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_350_narrow_13TeV_madgraph_Hzz = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-350_narrow_13TeV-madgraph_Hzz_minitree.root")

# minizz_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_400_narrow_13TeV_madgraph_Hzz = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-400_narrow_13TeV-madgraph_Hzz_minitree.root")

# minizz_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_450_narrow_13TeV_madgraph_Hzz = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-450_narrow_13TeV-madgraph_Hzz_minitree.root")

# minizz_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_600_narrow_13TeV_madgraph_Hzz = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-600_narrow_13TeV-madgraph_Hzz_minitree.root")

# minizz_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_650_narrow_13TeV_madgraph_Hzz = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-650_narrow_13TeV-madgraph_Hzz_minitree.root")

# minizz_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_900_narrow_13TeV_madgraph_Hzz = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-900_narrow_13TeV-madgraph_Hzz_minitree.root")

# vv_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_1000_narrow_13TeV_madgraph = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-1000_narrow_13TeV-madgraph_minitree.root")

# vv_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_260_narrow_13TeV_madgraph = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-260_narrow_13TeV-madgraph_minitree.root")

# vv_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_270_narrow_13TeV_madgraph = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-270_narrow_13TeV-madgraph_minitree.root")

# vv_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_300_narrow_13TeV_madgraph = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-300_narrow_13TeV-madgraph_minitree.root")

# vv_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_350_narrow_13TeV_madgraph = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-350_narrow_13TeV-madgraph_minitree.root")

# vv_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_400_narrow_13TeV_madgraph = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-400_narrow_13TeV-madgraph_minitree.root")

# vv_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_450_narrow_13TeV_madgraph = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-450_narrow_13TeV-madgraph_minitree.root")

# vv_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_600_narrow_13TeV_madgraph = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-600_narrow_13TeV-madgraph_minitree.root")

# vv_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_650_narrow_13TeV_madgraph = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-650_narrow_13TeV-madgraph_minitree.root")

# vv_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_900_narrow_13TeV_madgraph = ROOT.TFile(dirWithMCSamples + "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-900_narrow_13TeV-madgraph_minitree.root")


# sigInputFile_260 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M260_minitree.root")
# sigInputFile_270 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M270_minitree.root")
# sigInputFile_300 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M300_minitree.root")
# sigInputFile_350 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M350_minitree.root")
# sigInputFile_400 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M400_minitree.root")
# sigInputFile_450 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M450_minitree.root")
# sigInputFile_600 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M600_minitree.root")
# sigInputFile_650 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M650_minitree.root")
# sigInputFile_900 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M900_minitree.root")
# sigInputFile_1000 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M1000_minitree.root")


# zzSigInputFile_260 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M260_Hzz_minitree.root")
# zzSigInputFile_270 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M270_Hzz_minitree.root")
# zzSigInputFile_300 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M300_Hzz_minitree.root")
# zzSigInputFile_350 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M350_Hzz_minitree.root")
# zzSigInputFile_400 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M400_Hzz_minitree.root")
# zzSigInputFile_450 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M450_Hzz_minitree.root")
# zzSigInputFile_600 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M600_Hzz_minitree.root")
# zzSigInputFile_650 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M650_Hzz_minitree.root")
# zzSigInputFile_900 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M900_Hzz_minitree.root")
# zzSigInputFile_1000 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M1000_Hzz_minitree.root")


# wwSigInputFile_260 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M260_Hww_minitree.root")
# wwSigInputFile_270 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M270_Hww_minitree.root")
# wwSigInputFile_300 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M300_Hww_minitree.root")
# wwSigInputFile_350 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M350_Hww_minitree.root")
# wwSigInputFile_400 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M400_Hww_minitree.root")
# wwSigInputFile_450 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M450_Hww_minitree.root")
# wwSigInputFile_600 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M600_Hww_minitree.root")
# wwSigInputFile_650 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M650_Hww_minitree.root")
# wwSigInputFile_900 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M900_Hww_minitree.root")
# wwSigInputFile_1000 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M1000_Hww_minitree.root")


# bgInputFile_TT = ROOT.TFile(dirWithMCSamples + "TT_Tune_minitree.root")
# bgInputFile_DY_1j = ROOT.TFile(dirWithMCSamples + "DY1JetsToLL_M50_minitree.root")
# bgInputFile_DY_2j = ROOT.TFile(dirWithMCSamples + "DY2JetsToLL_M50_minitree.root")
# bgInputFile_DY_3j = ROOT.TFile(dirWithMCSamples + "DY3JetsToLL_M50_minitree.root")
# bgInputFile_DY_4j = ROOT.TFile(dirWithMCSamples + "DY4JetsToLL_M50_minitree.root")


# bgInputFile_ST_t_antitop_inclusive_powheg = ROOT.TFile(dirWithMCSamples + "ST_t_antitop_inclusive_powheg_minitree.root")
# bgInputFile_ST_tW_top_5f_inclusive = ROOT.TFile(dirWithMCSamples + "ST_tW_top_5f_inclusive_minitree.root")
# bgInputFile_ST_tW_antitop_5f_NFHDecay = ROOT.TFile(dirWithMCSamples + "ST_tW_antitop_5f_NFHDecay_minitree.root")
# bgInputFile_ST_s_channel_4f = ROOT.TFile(dirWithMCSamples + "ST_s-channel_4f_minitree.root")
# bgInputFile_ST_tW_antitop_5f_inclusive = ROOT.TFile(dirWithMCSamples + "ST_tW_antitop_5f_inclusive_minitree.root")
# bgInputFile_ST_tW_top_5f_NFHDecay = ROOT.TFile(dirWithMCSamples + "ST_tW_top_5f_NFHDecay_minitree.root")
# bgInputFile_ST_t_top_inclusive_powheg = ROOT.TFile(dirWithMCSamples + "ST_t_top_inclusive_powheg_minitree.root")

# bgInputFile_ZZ_Tune = ROOT.TFile(dirWithMCSamples + "ZZ_Tune_minitree.root")
# bgInputFile_WZ_Tune = ROOT.TFile(dirWithMCSamples + "WZ_Tune_minitree.root")
# bgInputFile_WW_Tune = ROOT.TFile(dirWithMCSamples + "WW_Tune_minitree.root")
# bgInputFile_ZH_powheg = ROOT.TFile(dirWithMCSamples + "ZH_powheg_minitree.root")

# muon2016dataInputFile = ROOT.TFile(dirWithMCSamples + "muon2016data_minitree.root")

dictOfFiles = {
    zz_sigInputFile_GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M_1000_narrow_13TeV_madgraph__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v2 : "GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-1000_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v2",

    zz_sigInputFile_GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M_250_narrow_13TeV_madgraph__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 : "GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-250_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1",

    zz_sigInputFile_GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M_260_narrow_13TeV_madgraph__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 : "GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-260_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1",

    zz_sigInputFile_GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M_270_narrow_13TeV_madgraph__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 : "GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-270_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1",

    zz_sigInputFile_GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M_300_narrow_13TeV_madgraph__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 : "GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-300_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1",

    zz_sigInputFile_GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M_350_narrow_13TeV_madgraph__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 : "GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-350_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1",

    zz_sigInputFile_GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M_400_narrow_13TeV_madgraph__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 : "GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-400_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1",

    zz_sigInputFile_GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M_450_narrow_13TeV_madgraph__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 : "GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-450_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1",

    zz_sigInputFile_GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M_500_narrow_13TeV_madgraph__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 : "GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-500_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1",

    zz_sigInputFile_GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M_550_narrow_13TeV_madgraph__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 : "GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-550_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1",

    zz_sigInputFile_GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M_600_narrow_13TeV_madgraph__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 : "GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-600_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1",

    zz_sigInputFile_GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M_650_narrow_13TeV_madgraph__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 : "GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-650_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1",

    zz_sigInputFile_GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M_700_narrow_13TeV_madgraph__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 : "GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-700_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1",

    zz_sigInputFile_GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M_750_narrow_13TeV_madgraph__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 : "GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-750_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1",

    zz_sigInputFile_GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M_800_narrow_13TeV_madgraph__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 : "GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-800_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1",

    zz_sigInputFile_GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M_900_narrow_13TeV_madgraph__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 : "GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-900_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1",

    ww_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_1000_narrow_13TeV_madgraph_HWW : "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-1000_narrow_13TeV-madgraph_HWW",

    ww_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_260_narrow_13TeV_madgraph_HWW : "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-260_narrow_13TeV-madgraph_HWW",

    ww_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_270_narrow_13TeV_madgraph_HWW : "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-270_narrow_13TeV-madgraph_HWW",

    ww_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_300_narrow_13TeV_madgraph_HWW : "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-300_narrow_13TeV-madgraph_HWW",

    ww_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_350_narrow_13TeV_madgraph_HWW : "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-350_narrow_13TeV-madgraph_HWW",

    ww_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_400_narrow_13TeV_madgraph_HWW : "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-400_narrow_13TeV-madgraph_HWW",

    ww_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_450_narrow_13TeV_madgraph_HWW : "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-450_narrow_13TeV-madgraph_HWW",

    ww_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_600_narrow_13TeV_madgraph_HWW : "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-600_narrow_13TeV-madgraph_HWW",

    ww_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_650_narrow_13TeV_madgraph_HWW : "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-650_narrow_13TeV-madgraph_HWW",

    ww_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_900_narrow_13TeV_madgraph_HWW : "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-900_narrow_13TeV-madgraph_HWW",

    bgInputFile_DY1JetsToLL_M_50_TuneCUETP8M1_13TeV_madgraphMLM_Py8__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 : "DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1",

    bgInputFile_DY2JetsToLL_M_50_TuneCUETP8M1_13TeV_madgraphMLM_Py8__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 : "DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1",

    bgInputFile_DY3JetsToLL_M_50_TuneCUETP8M1_13TeV_madgraphMLM_Py8__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 : "DY3JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1",

    bgInputFile_DY4JetsToLL_M_50_TuneCUETP8M1_13TeV_madgraphMLM_Py8__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 : "DY4JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1",

    bgInputFile_ST_s_channel_4f_leptonDecays_13TeV_amcatnlo_Py8_TuneCUETP8M1__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 : "ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-Py8_TuneCUETP8M1__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1",

    bgInputFile_ST_t_channel_antitop_4f_inclusiveDecays_13TeV_powhegV2_madspin_Py8_TuneCUETP8M1__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 : "ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-Py8_TuneCUETP8M1__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1",

    bgInputFile_ST_t_channel_top_4f_inclusiveDecays_13TeV_powhegV2_madspin_Py8_TuneCUETP8M1__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 : "ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-Py8_TuneCUETP8M1__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1",

    #bgInputFile_ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV_powheg_TuneCUETP8M1__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_ext1_v1 : "ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext1-v1",

    bgInputFile_ST_tW_antitop_5f_inclusiveDecays_13TeV_powheg_Py8_TuneCUETP8M1__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_ext1_v1 : "ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-Py8_TuneCUETP8M1__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext1-v1",

    #bgInputFile_ST_tW_top_5f_NoFullyHadronicDecays_13TeV_powheg_TuneCUETP8M1__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_ext1_v1 : "ST_tW_top_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext1-v1",

    bgInputFile_ST_tW_top_5f_inclusiveDecays_13TeV_powheg_Py8_TuneCUETP8M1__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_ext1_v1 : "ST_tW_top_5f_inclusiveDecays_13TeV-powheg-Py8_TuneCUETP8M1__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext1-v1",

    bgInputFile_TT_TuneCUETP8M2T4_13TeV_powheg_Py8__RunIISummer16MAv2_PUMoriond17_backup_80r2as_2016_TrancheIV_v6_v1 : "TT_TuneCUETP8M2T4_13TeV-powheg-Py8__RunIISummer16MAv2-PUMoriond17_backup_80r2as_2016_TrancheIV_v6-v1",

    bgInputFile_WW_TuneCUETP8M1_13TeV_Py8__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 : "WW_TuneCUETP8M1_13TeV-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1",

    bgInputFile_WZ_TuneCUETP8M1_13TeV_Py8__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 : "WZ_TuneCUETP8M1_13TeV-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1",

    bgInputFile_ZH_HToBB_ZToLL_M125_13TeV_amcatnloFXFX_madspin_Py8__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 : "ZH_HToBB_ZToLL_M125_13TeV_amcatnloFXFX_madspin_Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1",

    bgInputFile_ZZ_TuneCUETP8M1_13TeV_Py8__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 : "ZZ_TuneCUETP8M1_13TeV-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1",



    # minizz_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_1000_narrow_13TeV_madgraph_Hzz : "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-1000_narrow_13TeV-madgraph_Hzz",

    # minizz_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_260_narrow_13TeV_madgraph_Hzz : "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-260_narrow_13TeV-madgraph_Hzz",

    # minizz_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_270_narrow_13TeV_madgraph_Hzz : "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-270_narrow_13TeV-madgraph_Hzz",

    # minizz_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_300_narrow_13TeV_madgraph_Hzz : "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-300_narrow_13TeV-madgraph_Hzz",

    # minizz_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_350_narrow_13TeV_madgraph_Hzz : "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-350_narrow_13TeV-madgraph_Hzz",

    # minizz_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_400_narrow_13TeV_madgraph_Hzz : "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-400_narrow_13TeV-madgraph_Hzz",

    # minizz_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_450_narrow_13TeV_madgraph_Hzz : "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-450_narrow_13TeV-madgraph_Hzz",

    # minizz_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_600_narrow_13TeV_madgraph_Hzz : "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-600_narrow_13TeV-madgraph_Hzz",

    # minizz_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_650_narrow_13TeV_madgraph_Hzz : "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-650_narrow_13TeV-madgraph_Hzz",

    # minizz_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_900_narrow_13TeV_madgraph_Hzz : "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-900_narrow_13TeV-madgraph_Hzz",

    # vv_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_1000_narrow_13TeV_madgraph : "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-1000_narrow_13TeV-madgraph",

    # vv_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_260_narrow_13TeV_madgraph : "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-260_narrow_13TeV-madgraph",

    # vv_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_270_narrow_13TeV_madgraph : "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-270_narrow_13TeV-madgraph",

    # vv_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_300_narrow_13TeV_madgraph : "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-300_narrow_13TeV-madgraph",

    # vv_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_350_narrow_13TeV_madgraph : "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-350_narrow_13TeV-madgraph",

    # vv_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_400_narrow_13TeV_madgraph : "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-400_narrow_13TeV-madgraph",

    # vv_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_450_narrow_13TeV_madgraph : "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-450_narrow_13TeV-madgraph",

    # vv_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_600_narrow_13TeV_madgraph : "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-600_narrow_13TeV-madgraph",

    # vv_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_650_narrow_13TeV_madgraph : "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-650_narrow_13TeV-madgraph",

    # vv_sigInputFile_GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M_900_narrow_13TeV_madgraph : "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-900_narrow_13TeV-madgraph"

}

# dictOfFiles = {
if muonRun:
    dataDictMuons = {

        dataInputFile_DoubleMuon__Run2016B_03Feb2017_ver1_v1 : "DoubleMuon__Run2016B-03Feb2017_ver1-v1",

        dataInputFile_DoubleMuon__Run2016B_03Feb2017_ver2_v2 : "DoubleMuon__Run2016B-03Feb2017_ver2-v2",

        dataInputFile_DoubleMuon__Run2016C_03Feb2017_v1 : "DoubleMuon__Run2016C-03Feb2017-v1",

        dataInputFile_DoubleMuon__Run2016D_03Feb2017_v1 : "DoubleMuon__Run2016D-03Feb2017-v1",

        dataInputFile_DoubleMuon__Run2016E_03Feb2017_v1 : "DoubleMuon__Run2016E-03Feb2017-v1",

        dataInputFile_DoubleMuon__Run2016F_03Feb2017_v1 : "DoubleMuon__Run2016F-03Feb2017-v1",

        dataInputFile_DoubleMuon__Run2016G_03Feb2017_v1 : "DoubleMuon__Run2016G-03Feb2017-v1",

        dataInputFile_DoubleMuon__Run2016H_03Feb2017_ver2_v1 : "DoubleMuon__Run2016H-03Feb2017_ver2-v1",

        dataInputFile_DoubleMuon__Run2016H_03Feb2017_ver3_v1 : "DoubleMuon__Run2016H-03Feb2017_ver3-v1",

        }
else:
    dataDictEles = {


        dataInputFile_DoubleEG__Run2016B_03Feb2017_ver1_v1 : "DoubleEG__Run2016B-03Feb2017_ver1-v1",

        dataInputFile_DoubleEG__Run2016B_03Feb2017_ver2_v2 : "DoubleEG__Run2016B-03Feb2017_ver2-v2",

        dataInputFile_DoubleEG__Run2016C_03Feb2017_v1 : "DoubleEG__Run2016C-03Feb2017-v1",

        dataInputFile_DoubleEG__Run2016D_03Feb2017_v1 : "DoubleEG__Run2016D-03Feb2017-v1",

        dataInputFile_DoubleEG__Run2016E_03Feb2017_v1 : "DoubleEG__Run2016E-03Feb2017-v1",

        dataInputFile_DoubleEG__Run2016F_03Feb2017_v1 : "DoubleEG__Run2016F-03Feb2017-v1",

        dataInputFile_DoubleEG__Run2016G_03Feb2017_v1 : "DoubleEG__Run2016G-03Feb2017-v1",
        
        dataInputFile_DoubleEG__Run2016H_03Feb2017_ver2_v1 : "DoubleEG__Run2016H-03Feb2017_ver2-v1",
        
        dataInputFile_DoubleEG__Run2016H_03Feb2017_ver3_v1 : "DoubleEG__Run2016H-03Feb2017_ver3-v1",


        }


if muonRun:
    dictOfFiles.update(dataDictMuons)
else:
    dictOfFiles.update(dataDictEles)

#     sigInputFile_260:'BulkGraviton_M260',
#     sigInputFile_270:'BulkGraviton_M270',
#     sigInputFile_300:'BulkGraviton_M300',
#     sigInputFile_350:'BulkGraviton_M350',
#     sigInputFile_400:'BulkGraviton_M400',
#     sigInputFile_450:'BulkGraviton_M450',
#     sigInputFile_600:'BulkGraviton_M600',
#     sigInputFile_650:'BulkGraviton_M650',
#     sigInputFile_900:'BulkGraviton_M900',
#     sigInputFile_1000:'BulkGraviton_M1000',
   
#     zzSigInputFile_260:'BulkGraviton_M260_Hzz',
#     zzSigInputFile_270:'BulkGraviton_M270_Hzz',
#     zzSigInputFile_300:'BulkGraviton_M300_Hzz',
#     zzSigInputFile_350:'BulkGraviton_M350_Hzz',
#     zzSigInputFile_400:'BulkGraviton_M400_Hzz',
#     zzSigInputFile_450:'BulkGraviton_M450_Hzz',
#     zzSigInputFile_600:'BulkGraviton_M600_Hzz',
#     zzSigInputFile_650:'BulkGraviton_M650_Hzz',
#     zzSigInputFile_900:'BulkGraviton_M900_Hzz',
#     zzSigInputFile_1000:'BulkGraviton_M1000_Hzz',
   
    
#     wwSigInputFile_260:'BulkGraviton_M260_Hww',
#     wwSigInputFile_270:'BulkGraviton_M270_Hww',
#     wwSigInputFile_300:'BulkGraviton_M300_Hww',
#     wwSigInputFile_350:'BulkGraviton_M350_Hww',
#     wwSigInputFile_400:'BulkGraviton_M400_Hww',
#     wwSigInputFile_450:'BulkGraviton_M450_Hww',
#     wwSigInputFile_600:'BulkGraviton_M600_Hww',
#     wwSigInputFile_650:'BulkGraviton_M650_Hww',
#     wwSigInputFile_900:'BulkGraviton_M900_Hww',
#     wwSigInputFile_1000:'BulkGraviton_M1000_Hww',
   
#     bgInputFile_TT: 'TT_Tune',
#     bgInputFile_DY_1j: 'DY1JetsToLL_M50',
#     bgInputFile_DY_2j: 'DY2JetsToLL_M50',
#     bgInputFile_DY_3j: 'DY3JetsToLL_M50',
#     bgInputFile_DY_4j: 'DY4JetsToLL_M50',

#     bgInputFile_ST_s_channel_4f: 'ST_s-channel_4f',
#     bgInputFile_ST_t_top_inclusive_powheg: 'ST_t_top_inclusive_powheg',
#     bgInputFile_ST_t_antitop_inclusive_powheg: 'ST_t_antitop_inclusive_powheg',
#     bgInputFile_ST_tW_top_5f_inclusive: 'ST_tW_top_5f_inclusive',
#     bgInputFile_ST_tW_antitop_5f_inclusive: 'ST_tW_antitop_5f_inclusive',
#     bgInputFile_ST_tW_top_5f_NFHDecay: 'ST_tW_top_5f_NFHDecay',
#     bgInputFile_ST_tW_antitop_5f_NFHDecay: 'ST_tW_antitop_5f_NFHDecay',

#     bgInputFile_ZH_powheg: 'ZH_powheg',
#     bgInputFile_ZZ_Tune: 'ZZ_Tune',
#     bgInputFile_WW_Tune: 'WW_Tune',
#     bgInputFile_WZ_Tune: 'WZ_Tune',

#     muon2016dataInputFile: 'muon2016data',
    
#}


# myVars = ['metpt',
#           'dR_leps',
#           'dR_bjets',
#           'btag0',
#           'btag1',
#           'hpt0',
#           'hpt1',
#           'nbjets',
#           'dEta_lb_min'
#           ]
#for v in myVars:
 #   print "histos['" + v + "'].Fill(entry." + v + ', eqLumi)'

print 'Doing massRegion ', massRegion

outDir = nameDir + massRegion + '_' + physRegion  + '_' + str(bdtCut) + '/'

print 'outDir is ', outDir
if not os.path.exists(outDir):
    os.makedirs(outDir)

muonIsThere = any('Muon' in x for x in dictOfFiles.values() ) 
eleIsThere  = any('EG' in y for y in dictOfFiles.values() )
print 'muonIsThere is', muonIsThere
print 'eleIsThere is', eleIsThere

if muonIsThere and eleIsThere:
    print 'keep only one type of data per time, exiting...'
    sys.exit(1)
elif muonIsThere and not eleIsThere and muonRun and not eleRun:
    leptonType = "mm"
elif eleIsThere and not muonIsThere and not muonRun and eleRun:
    leptonType = "ee"
else:
    print 'no data, exiting...'
    

TMVA.Tools.Instance()
reader_lowMass = TMVA.Reader( "!Color:!Silent" )
reader_highMass = TMVA.Reader( "!Color:!Silent" )

zmass = array('f',[0])
met_pt = array('f',[0])
hmass0 = array('f',[0])

hmass1 = array('f',[0])
dR_leps = array('f',[0])
dR_bjets = array('f',[0])
    
zpt0 = array('f',[0])
hpt0 = array('f',[0])
hpt1 = array('f',[0])


reader_lowMass.AddVariable("zmass", zmass)
reader_lowMass.AddVariable("met_pt", met_pt)
reader_lowMass.AddVariable("hmass0", hmass0)

reader_lowMass.AddVariable("hmass1", hmass1)
reader_lowMass.AddVariable("dR_leps", dR_leps)
reader_lowMass.AddVariable("dR_bjets", dR_bjets)
    
reader_lowMass.AddVariable("zpt0", zpt0)
reader_lowMass.AddVariable("hpt0", hpt0)
reader_lowMass.AddVariable("hpt1", hpt1)

bazinga('weightFile_lowMass is {0}'.format(weightFile_lowMass))
reader_lowMass.BookMVA('BDT', weightFile_lowMass)

reader_highMass.AddVariable("zmass", zmass)
reader_highMass.AddVariable("met_pt", met_pt)
reader_highMass.AddVariable("hmass0", hmass0)
    
reader_highMass.AddVariable("hmass1", hmass1)
reader_highMass.AddVariable("dR_leps", dR_leps)
reader_highMass.AddVariable("dR_bjets", dR_bjets)
    
reader_highMass.AddVariable("zpt0", zpt0)
reader_highMass.AddVariable("hpt0", hpt0)
reader_highMass.AddVariable("hpt1", hpt1)
    
bazinga('weightFile_highMass is {0}'.format(weightFile_highMass))
reader_highMass.BookMVA('BDT', weightFile_highMass)

for sample, name in dictOfFiles.items():
    print 'doing muonRun={0} for {1}'.format(muonRun, systUnc)
    if muonRun and 'eff_e' in systUnc:
        print 'in muon'
        break#continue
    elif eleRun and ('eff_m_I' in systUnc or 'eff_m_tr' in systUnc):
        print 'in ele'
        break#continue
    else:
        pass

    myVars = [  
        'zmass', 
        'met_pt', 
        'hmass0',
        
        'hmass1',
        'dR_leps',
        'dR_bjets',
        
        'zpt0',
        'hpt0',
        'hpt1'
        ]
    


    #if 'Signal' not in name: continue
    bazinga('processing {0}'.format(physRegion) )
    if 'Glu' in name:
        print 'name is', name
        idx1 = name.find("_M-")
        idx2 = name.find("narrow")
        
        tmpM = name[idx1+3: idx2-1]
        print 'tmp mass is', tmpM
        if not any(c.isalpha() for c in tmpM):
            mass = int(tmpM)
            print 'mass is', mass
        else:
            print 'smth is wrong with extracting mass number from the signal sample, exiting..'
            print 'mass is', mass
            sys.exit(1)
        print 'name is {0} and mass is {1}'.format(name, mass)
        if massRegion == 'low' and mass > 450: continue
        if massRegion == 'high' and mass <  450: continue
    
    reader = reader_lowMass if massRegion == 'low' else reader_highMass    

    bazinga('process {0}'.format(name))
    minValue = 150 if massRegion == 'low' else 400
    maxValue = 1150 if massRegion == 'low' else 1400
    centinel = maxValue-1


    postf = ''
    trk, idi, iso, trig = 0, 0, 0, 0
    
    if 'ID' in systUnc:
        
        if 'eff_m' in systUnc:
            postf = 'CMS_eff_m_IDUp' if 'Up' in systUnc else 'CMS_eff_m_IDDown' if 'Down' in systUnc else None
        if 'eff_e' in systUnc:
            postf = 'CMS_eff_e_IDUp' if 'Up' in systUnc else 'CMS_eff_e_IDDown' if 'Down' in systUnc else None
        idi = 2 if 'Up' in systUnc else 1 if 'Down' in systUnc else None

    if 'ISO' in systUnc:
        
        if 'eff_m' in systUnc:
            postf = 'CMS_eff_m_ISOUp' if 'Up' in systUnc else 'CMS_eff_m_ISODown' if 'Down' in systUnc else None
        if 'eff_e' in systUnc:
            print 'nothing for electrons!'
            sys.exit(1)
        iso = 2 if 'Up' in systUnc else 1 if 'Down' in systUnc else None

    if 'tracker' in systUnc:
        if 'eff_m' in systUnc:
            postf = 'CMS_eff_m_trackerUp' if 'Up' in systUnc else 'CMS_eff_m_trackerDown' if 'Down' in systUnc else None
        if 'eff_e' in systUnc:
            postf = 'CMS_eff_e_trackerUp' if 'Up' in systUnc else 'CMS_eff_e_trackerDown' if 'Down' in systUnc else None
        trk = 2 if 'Up' in systUnc else 1 if 'Down' in systUnc else None
    if 'trigger' in systUnc:
        if 'eff_m' in systUnc:
            postf = 'CMS_eff_m_triggerUp' if 'Up' in systUnc else 'CMS_eff_m_triggerDown' if 'Down' in systUnc else None
        if 'eff_e' in systUnc:
            postf = 'CMS_eff_e_triggerUp' if 'Up' in systUnc else 'CMS_eff_e_triggerDown' if 'Down' in systUnc else None
        trig = 2 if 'Up' in systUnc else 1 if 'Down' in systUnc else None            


    if trk == None or idi == None or iso == None or trig == None:
        print 'trk={0}, idi={1}, iso={2}, trig={3}'.format(trk, idi, iso, trig)
        print 'wrong param, exit'
        sys.exit(1)


    if 'btag' in systUnc:
        if 'light' in systUnc:
            postf = 'CMS_btag_lightUp' if 'Up' in systUnc else 'CMS_btag_lightDown' if 'Down' in systUnc else None
        elif 'heavy' in systUnc:
            postf = 'CMS_btag_heavyUp' if 'Up' in systUnc else 'CMS_btag_heavyDown' if 'Down' in systUnc else None
        else:
            print 'check btag systematics'
            sys.exit(1)
        
    if 'scale_j' in systUnc:
        postf = 'CMS_scale_jUp' if 'Up' in systUnc else 'CMS_scale_jDown' if 'Down' in systUnc else None

    if 'res_j' in systUnc:
        postf = 'CMS_res_jUp' if 'Up' in systUnc else'CMS_res_jDown' if 'Down' in systUnc else None


    if 'met' in systUnc:
        if 'JetEn' in systUnc:
            postf = 'CMS_eff_met_JetEnUp' if 'Up' in systUnc else 'CMS_eff_met_JetEnDown' if 'Down' in systUnc else None
        elif 'Unclustered' in systUnc:
            postf = 'CMS_eff_met_UnclusteredEnUp' if 'Up' in systUnc else 'CMS_eff_met_UnclusteredEnDown' if 'Down' in systUnc else None
        elif 'JetRes' in systUnc:
            postf = 'CMS_eff_met_JetResUp' if 'Up' in systUnc else 'CMS_eff_met_JetResDown' if 'Down' in systUnc else None

        else:
            print 'met postf is wrong'
            sys.exit(1)


    

#    if 'CMS_pu' in systUnc:
 #       postf = 'CMS_puUp' if 'Up' in systUnc else 'CMS_puDown' if 'Down' in systUnc else None

    if postf == None:
        print 'postf ==None'
        sys.exit(1)
    elif postf == '':
        if systUnc == 'nominal':
            print 'doing nominal'
        else:
            print 'postf is wrong'
            sys.exit(1)
    elif postf == systUnc:
        print 'doing', systUnc
    else:
        print 'postf is unknown'
        sys.exit(1)

    print 'postf is', postf 
    if 'nominal' not in systUnc:
        postf = '_' + postf#[4:]

    histos = {
        'bdt_response{0}'.format(postf)      :ROOT.TH1F('bdt_response{0}'.format(postf), ';BDT response; Events', 100, -1., +1.),
        'bdt_response_afterCut{0}'.format(postf)      :ROOT.TH1F('bdt_response_afterCut{0}'.format(postf), ';BDT response; Events', 100, -1., +1.),

        #'dEta_lb_min'       :ROOT.TH1F('dEta_lb_min', ';|#Delta#eta|_{min}(l, b); Events', 20, 0, 5),
        # 'dEta_ZH'       :ROOT.TH1F('dEta_ZH', ';|#Delta#eta|(Z_{ll}, H_{bb}); Events', 20, 0, 5),
        'dEta_bjets{0}'.format(postf)       :ROOT.TH1F('dEta_bjets{0}'.format(postf), ';#Delta#eta(b_{1}, b_{2}); Events', 40, -5., 5),
        'dEta_bjets_abs{0}'.format(postf)       :ROOT.TH1F('dEta_bjets_abs{0}'.format(postf), ';|#Delta#eta|(b_{1}, b_{2}); Events', 20, 0, 5),
        # 'dEta_leps'       :ROOT.TH1F('dEta_leps', ';|#Delta#eta|(l_{1}, l_{2}); Events', 20, 0, 5),

        # 'dPhi_lb_min'       :ROOT.TH1F('dPhi_lb_min', ';|#Delta#phi|_{min}(l, b); Events', 20, 0, 5),
        # 'dPhi_ZH'       :ROOT.TH1F('dPhi_ZH', ';|#Delta#phi|(Z_{ll}, H_{bb}); Events', 20, 0, 5),
        # 'dPhi_bjets'       :ROOT.TH1F('dPhi_bjets', ';|#Delta#phi|(b_{1}, b_{2}); Events', 20, 0, 5),
        # 'dPhi_leps'       :ROOT.TH1F('dPhi_leps', ';|#Delta#phi|(l_{1}, l_{2}); Events', 20, 0, 5),

        # 'dR_lb_min'       :ROOT.TH1F('dR_lb_min', ';#DeltaR_{min}(l, b); Events', 20, 0, 8),
        # 'dR_ZH'       :ROOT.TH1F('dR_ZH', ';#DeltaR(Z_{ll}, H_{bb}); Events', 20, 0, 8),
        'dR_bjets{0}'.format(postf)       :ROOT.TH1F('dR_bjets{0}'.format(postf), ';#DeltaR(b_{1}, b_{2}); Events', 20, 0, dR_binMax), #8
        'dR_leps{0}'.format(postf)       :ROOT.TH1F('dR_leps{0}'.format(postf), ';#DeltaR(l_{1}, l_{2}); Events', 20, 0, dR_binMax), #8

      
        #'nbjets_raw':ROOT.TH1F('nbjets_raw'     ,';b-jet multiplicity; Events'                          , 7,0,7),
        #'nbjets':ROOT.TH1F('nbjets'     ,';b-jet multiplicity; Events'                          , 7,0,7),
        #'metpt_raw'     :ROOT.TH1F('metpt_raw'      ,';MET [GeV]; Events'                , 35,0,350),
        #'njets_raw'     :ROOT.TH1F('njets_raw'  ,';Jet multiplicity; Events'                            , 9,0,9),
        #'nleps_raw'             :ROOT.TH1F('nleps_raw'          ,';Lepton multiplicity; Events'                         , 3,1,4),


        'met_pt{0}'.format(postf)     :ROOT.TH1F('met_pt{0}'.format(postf)      ,';MET [GeV]; Events'                , 35,0, met_pt_binMax), #350
        # 'nleps'         :ROOT.TH1F('nleps'              ,';Lepton multiplicity; Events'                         , 3,1,4),
        # 'bjetpt'    :ROOT.TH1F('bjetpt'     ,';p_{T}(b jet) [GeV]; Events'              , 35,0,350),
        # 'bjeteta'   :ROOT.TH1F('bjeteta'    ,';#eta(b jet); Events'                     , 20,-2.4,2.4),
        # 'leppt'     :ROOT.TH1F('leppt'      ,';p_{T}(lepton) [GeV]; Events'             , 25,0,250),
        # 'lepeta'    :ROOT.TH1F('lepeta'     ,';#eta(lepton); Events'                    , 20,-2.4,2.4),

        'bjet0pt{0}'.format(postf)       :ROOT.TH1F('bjet0pt{0}'.format(postf)    ,';Leading b-Jet p_{T} [GeV]; Events'       , 70, 20., 300.),
        'bjet1pt{0}'.format(postf)       :ROOT.TH1F('bjet1pt{0}'.format(postf)    ,';Subleading b-Jet p_{T} [GeV]; Events'        , 70, 20., 300.),
        'bjet0eta{0}'.format(postf)      :ROOT.TH1F('bjet0eta{0}'.format(postf)   ,';Leading b-Jet #eta; Events'                          , 40, -2.4, 2.4),
        'bjet1eta{0}'.format(postf)      :ROOT.TH1F('bjet1eta{0}'.format(postf)   ,';Subleading b-Jet #eta; Events'                       , 40, -2.4, 2.4),
        'btagDiscr0{0}'.format(postf)       :ROOT.TH1F('btagDiscr0{0}'.format(postf)  ,';Leading b-Jet CMVAV2 discriminant; Events'            , 75, -0.5, 1.),
        'btagDiscr1{0}'.format(postf)       :ROOT.TH1F('btagDiscr1{0}'.format(postf)  ,';Subleading b-Jet CMVAV2 discriminant; Events'         , 75, -0.5, 1.),

        'lep0pt{0}'.format(postf)        :ROOT.TH1F('lep0pt{0}'.format(postf)             ,';Leading Lepton p_{T} [GeV]; Events'          , 75, 0., 150.),
        'lep1pt{0}'.format(postf)        :ROOT.TH1F('lep1pt{0}'.format(postf)             ,';Subleading Lepton p_{T} [GeV]; Events'       , 75, 0., 150.),
        'lep0eta{0}'.format(postf)       :ROOT.TH1F('lep0eta{0}'.format(postf)    ,';Leading Lepton #eta ; Events'                    , 40, -2.4, 2.4),
        'lep1eta{0}'.format(postf)       :ROOT.TH1F('lep1eta{0}'.format(postf)    ,';Subleading Lepton #eta ; Events'             , 40, -2.4, 2.4),

        'lep0iso03{0}'.format(postf)        :ROOT.TH1F('lep0iso03{0}'.format(postf)             ,';Leading Lepton relIso03 [GeV]; Events'          , 50, 0., 0.4),
        'lep1iso03{0}'.format(postf)        :ROOT.TH1F('lep1iso03{0}'.format(postf)             ,';Subleading Lepton relIso03 [GeV]; Events'          , 50, 0., 0.4),
        'lep0iso04{0}'.format(postf)        :ROOT.TH1F('lep0iso04{0}'.format(postf)             ,';Leading Lepton relIso04 [GeV]; Events'          , 50, 0., 0.4),
        'lep1iso04{0}'.format(postf)        :ROOT.TH1F('lep1iso04{0}'.format(postf)             ,';Subleading Lepton relIso04 [GeV]; Events'          , 50, 0., 0.4),

        'sf_trk{0}'.format(postf)        :ROOT.TH1F('sf_trk{0}'.format(postf)             ,';Tracker SF; Events'          , 50, 0.75, 1.25),
        'sf_id{0}'.format(postf)        :ROOT.TH1F('sf_id{0}'.format(postf)             ,';ID SF; Events'          , 50, 0.75, 1.25),
        'sf_iso{0}'.format(postf)        :ROOT.TH1F('sf_iso{0}'.format(postf)             ,';ISO SF; Events'          , 50, 0.75, 1.25),
        'sf_dilep{0}'.format(postf)        :ROOT.TH1F('sf_dilep{0}'.format(postf)             ,';Trigger SF; Events'          , 50, 0.75, 1.25),

        'btag0sf{0}'.format(postf)        :ROOT.TH1F('btag0sf{0}'.format(postf)             ,';Leading b-jet SF; Events'          , 70, 0.8, 1.5),
        'btag1sf{0}'.format(postf)        :ROOT.TH1F('btag1sf{0}'.format(postf)             ,';Subleading b-jet SF; Events'          , 70, 0.1, 1.5),

        'lep_sf{0}'.format(postf)        :ROOT.TH1F('lep_sf{0}'.format(postf)             ,';Total lepton event SF; Events'          , 70, 0.55, 1.25),
        'bjet_sf{0}'.format(postf)        :ROOT.TH1F('bjet_sf{0}'.format(postf)             ,';Total b-jet event SF; Events'          , 70, 0.6, 2.),

        'dyLOtoNLO_sf{0}'.format(postf)        :ROOT.TH1F('dyLOtoNLO_sf{0}'.format(postf)             ,';DY LO to NLO weight; Events'          , 50, 0.5, 1.5),
        'EWK_sf{0}'.format(postf)        :ROOT.TH1F('EWK_sf{0}'.format(postf)             ,';EWK shape correction weight; Events'          , 50, 0.5, 2),
        #'hCSVmass'      :ROOT.TH1F('hCSVmass', ';HCSV mass [GeV]; Events', 40, 85, 165),
        # 'hCSVmass_long'      :ROOT.TH1F('hCSVmass_long', ';HCSV mass [GeV]; Events', 45, 30, 220),
        #'hCSVpt'      :ROOT.TH1F('hCSVpt', ';HCSV p_{T} [GeV]; Events', 50, 0, 400),
        #'hZZpt'      :ROOT.TH1F('hZZpt', ';H#rightarrowZZ p_{T} [GeV]; Events', 50, 0, 400),
        # 'hZZmt'      :ROOT.TH1F('hZZmt', ';H#rightarrowZZ transverse mass [GeV]; Events', 40, 50, 450),
        # 'hZZmt_long'      :ROOT.TH1F('hZZmt_long', ';H#rightarrowZZ transverse mass [GeV]; Events', 100, 50, 1050),

        #'hhMt'      :ROOT.TH1F('hhMt', ';"HiggsHiggson" transverse mass [GeV]; Events', 40, 550, 950),

        'zmass{0}'.format(postf)      :ROOT.TH1F('zmass{0}'.format(postf), ';Z mass [GeV]; Events', 15, Zmasslow, Zmassmid), # 76 and 106
        'zmass_oneBin{0}'.format(postf)      :ROOT.TH1F('zmass_oneBin{0}'.format(postf), ';Z mass [GeV]; Events', 1, Zmasslow, Zmassmid), # 76 and 106
        'zmass_high{0}'.format(postf)      :ROOT.TH1F('zmass_high{0}'.format(postf), ';Z mass [GeV]; Events', 25, 105, Zmasshigh), #155
        #'zmass_long'      :ROOT.TH1F('zmass_long', ';Z mass [GeV]; Events', 40, 76, 156), 
        #'zmass_mid'      :ROOT.TH1F('zmass_mid', ';Z mass [GeV]; Events', 35, 75, 110),

        

        'hmass0{0}'.format(postf)      :ROOT.TH1F('hmass0{0}'.format(postf), ';#tilde{M}(ZZ) [GeV]; Events', 25, Hzz_mass_binMin, Hzz_mass_binMax), #75, 175

        'hmass1{0}'.format(postf)      :ROOT.TH1F('hmass1{0}'.format(postf), ';Hbb mass [GeV]; Events', 40, Hbb_mass_binMin, Hbb_mass_binMax), # 20 and 220
        'hmass1_oneBin{0}'.format(postf)      :ROOT.TH1F('hmass1_oneBin{0}'.format(postf), ';Hbb mass [GeV]; Events', len(hmass1_oneBin_binning)-1, hmass1_oneBin_binning),
        #'zHMass'      :ROOT.TH1F('zHMass', ';ZH mass [GeV]; Events', 50, 115, 315),
        #'zHTransMass'      :ROOT.TH1F('zHTransMass', ';ZH transverse mass [GeV]; Events', 50, 115, 315),
        #'zMass_long'      :ROOT.TH1F('zMass_long', ';Z mass [GeV]; Events', 50, 20, 220),
        'zpt0{0}'.format(postf)      :ROOT.TH1F('zpt0{0}'.format(postf), ';Z p_{T} [GeV]; Events', 50, 0, Zpt_binMax), #300
        'hpt0{0}'.format(postf)      :ROOT.TH1F('hpt0{0}'.format(postf), ';#tilde{p_{T}}(ZZ) [GeV]; Events', 50, 0, Hzz_pt_binMax), #300  #?  \mbox{Z*} maybe
        'hpt1{0}'.format(postf)      :ROOT.TH1F('hpt1{0}'.format(postf), ';Hbb p_{T} [GeV]; Events', 50, 0, Hbb_pt_binMax), #300
        

        # 'mt2_llmet' :ROOT.TH1F('mt2_llmet', ';l_{1}l_{2}met mt2[GeV]; Events', 50, 0, 300),
        # 'mt2_b1l1b2l2met':ROOT.TH1F('mt2_b1l1b2l2met', ';b_{1}l_{1}b_{2}l_{2}met mt2 [GeV]; Events', 50, 0, 300),
        # 'mt2_b1l2b2l1met':ROOT.TH1F('mt2_b1l2b2l1met', ';b_{1}l_{2}b_{2}l_{1}met mt2 [GeV]; Events', 50, 0, 300),
        # 'mt2_bbmet':ROOT.TH1F('mt2_bbmet', ';b_{1}b_{2}met mt2[GeV]; Events', 50, 0, 300),
        # 'mt2_ZHmet':ROOT.TH1F('mt2_ZHmet', ';ZHmet mt2[GeV]; Events', 100, 0, 1000),
        # 'min_mt2_blmet':ROOT.TH1F('min_mt2_blmet', ';blmet mt2 [GeV]; Events', 50, 0, 300),

        }

    # if systUnc not in  [
    #     'nominal',
    #     'CMS_btag_lightUp', 'CMS_btag_heavyUp', 'CMS_eff_m_IDUp', 'CMS_eff_m_ISOUp', 'CMS_eff_m_trackerUp', 'CMS_eff_m_triggerUp', 'CMS_eff_e_IDUp', 'CMS_eff_e_trackerUp', 'CMS_eff_e_triggerUp',
    #     'CMS_eff_met_JetEnUp', 'CMS_eff_met_UnclusteredEnUp', 'CMS_eff_met_JetResUp', 'CMS_scale_jUp', 'CMS_res_jUp',

    #     'CMS_btag_lightDown', 'CMS_btag_heavyDown', 'CMS_eff_m_IDDown', 'CMS_eff_m_ISODown', 'CMS_eff_m_trackerDown', 'CMS_eff_m_triggerDown', 'CMS_eff_e_IDDown', 'CMS_eff_e_trackerDown', 'CMS_eff_e_triggerDown',
    #     'CMS_eff_met_JetEnDown', 'CMS_eff_met_UnclusteredEnDown', 'CMS_eff_met_JetResDown', 'CMS_scale_jDown', 'CMS_res_jDown'
    #     ]:
    #     print 'wrong systematics, should match spefified list in produceTonsOfHHMThist_v3.py'
    #     sys.exit(1)
        
    #histos['hhMt{0}'.format(postf)]  = ROOT.TH1F('hhMt{0}'.format(postf), ';HH transverse mass [GeV]; Events', (maxValue - minValue)/20, minValue, maxValue)
    #tilde{M}(ZZ)
    if (physRegion == "CRDYoneBin" or physRegion == "CRTToneBin"):
        histos['hhMt{0}'.format(postf)]  = ROOT.TH1F('hhMt{0}'.format(postf), ';#tilde{M_{T}}(HH) [GeV]; Events', (maxValue - minValue)/1000, minValue, maxValue)
    else:
        histos['hhMt{0}'.format(postf)]  = ROOT.TH1F('hhMt{0}'.format(postf), ';#tilde{M_{T}}(HH) [GeV]; Events', (maxValue - minValue)/20, minValue, maxValue)


    #pprint.pprint(histos)

    for key in histos:
        histos[key].Sumw2()
        histos[key].SetDirectory(0)


    ievt = 0
    
    print 'leptonType is', leptonType
    fO = root_open(outDir + name + '_shapes_' + leptonType + '_' + systUnc + '.root', "recreate")
    bazinga('before loop over {0}'.format(sample.GetName() ) )
    for entry in sample.tree:

        if  leptonType == "ee" and entry.leppt0 <=25: continue
        if  leptonType == "ee" and (entry.lep0Iso03>0.06 or entry.lep1Iso03>0.06): continue
        if  leptonType == "mm" and (entry.lep0Iso04>0.15 or entry.lep1Iso04>0.15): continue
        if (1.4442 < abs(entry.lepeta0) < 1.566) or (1.4442 < abs(entry.lepeta1) <1.566): continue
        
 
        # if physRegion == 'SR':
        #     if entry.zmass < 76 or entry.zmass > 106: continue
        #     if entry.hmass1 < 90 or entry.hmass1 > 150: continue
        # elif physRegion == 'CRDY':
        #     if entry.zmass < 76 or entry.zmass > 106: continue
        #     if entry.hmass1 >= 90 and entry.hmass1 <= 150: continue
        # elif physRegion == 'CRTT':
        #     if entry.zmass <= 106: continue
        #     if entry.hmass1 < 90 or entry.hmass1 > 150: continue
        # else:
        #     print 'smth is wrong with physRegion' 
        #     sys.exit(1)


#            for v in myVars:
 #               #print  v + '[0] = entry.' + v
        
        # if 'eff_m' in systUnc or 'eff_e' in systUnc:
        #     l_nomUpDown = 0 if systUnc == 'nominal' else 2 if 'Up' in systUnc else 1 if 'Down' in systUnc else None
        # if l_nomUpDown = None:
        #     print 'wring l_nomUpDown'
        #     sys.exit(1)

        #print 'entry.weight_SF_TRK[0]={0}, entry.weight_SF_LooseIDnISO[0]={1}, entry.weight_SF_Dilep[0]={2}'.format(entry.weight_SF_TRK[0], entry.weight_SF_LooseIDnISO[0], entry.weight_SF_Dilep[0])
        # if hasattr(entry, "weight_SF_TRK"):#"):
        #     print(entry.weight_SF_TRK[0])
        # else:
        #     print("no way!")
        sf_trk = getattr(entry,'weight_SF_TRK', None)[trk]
        sf_id = getattr(entry,'weight_SF_LooseID', None)[idi]
        sf_iso = getattr(entry,'weight_SF_LooseISO', None)[iso]
        #separately id and iso for electrons have no Up and Down, use combined version:
        sf_idNiso = getattr(entry,'weight_SF_LooseIDnISO', None)[idi] 
        sf_trig = getattr(entry,'weight_SF_Dilep', None)[trig]

        if eleRun and 'Double' not in name:
            if not sf_trk or not sf_idNiso or not sf_trig:
                print sf_trk
                print sf_idNiso
                print sf_trig
                sys.exit(1)
            else:
                sf_iso = 1.
                sf_id = sf_idNiso

        elif muonRun and 'Double' not in name:
            if not sf_trk or not sf_id or not sf_iso or not sf_trig:
                print sf_trk
                print sf_id
                print sf_iso
                print sf_trig
                sys.exit(1)
        elif 'Double' in name and (eleRun or muonRun):
            pass
        else:
            print 'cannot happen'
            sys.exit(1)
        #print '6'*500
        #print 'trk={0} ,  idi={1} ,  iso={2} ,  trig={3}'.format(trk ,  idi ,  iso ,  trig)
        #print 'sf_trk={0} ,  sf_id={1} ,  sf_iso={2} ,  sf_trig={3}'.format(sf_trk ,  sf_id ,  sf_iso ,  sf_trig)
        leps_SF = sf_trk * sf_id * sf_iso * sf_trig if 'Double' not in name else 1
        #print 'sf_1={0},sf_2={1},sf_3={2}'.format(sf_1, sf_2, sf_3)
        #print 'l_nomUpDown is',l_nomUpDown
        #print 'leps_SF is', leps_SF

        #check =  entry.weight_SF_TRK[0] * entry.weight_SF_LooseIDnISO[0] * entry.weight_SF_Dilep[0]
        #print 'check is', check
        #leps_SF_up = entry.weight_SF_TRK[2] * entry.weight_SF_LooseIDnISO[2] * entry.weight_SF_Dilep[2]
        #leps_SF_down = entry.weight_SF_TRK[1] * entry.weight_SF_LooseIDnISO[1] * entry.weight_SF_Dilep[1]

        

#        b_light_nomUpDown = 0 if systUnc == 'nominal' else 2 if systUnc == 'btag_lightUp' else 1 if systUnc == 'btag_lightDown' else None
 #       b_heavy_nomUpDown = 0 if systUnc == 'nominal' else 2 if systUnc == 'btag_heavyUp' else 1 if systUnc == 'btag_heavyDown' else None
        

        #btags_SF = entry.Jet_btagWeightCMVAV2[entry.hJCMVAV2idx[0]] * entry.Jet_btagWeightCMVAV2[entry.hJCMVAV2idx[1]] 
        #print 'btags_SF is ', btags_SF


        b_nomUpDown = ''
        flav = ''
        if 'btag' in systUnc:
            b_nomUpDown = '' if systUnc == 'nominal' else '_up' if 'Up' in systUnc else '_down' if 'Down' in systUnc else ''
            flav = '_lf' if 'light' in systUnc else '_hf' if 'heavy' in systUnc else ''


        # print 'b_nomUpDown =', b_nomUpDown
        # print 'flav=', flav
        # print 'Jet_btagWeightCMVAV2{0}{1}'.format(b_nomUpDown, flav)
        b_sf_1 = getattr(entry, 'Jet_btagWeightCMVAV2{0}{1}'.format(b_nomUpDown, flav), None)[entry.hJCMVAV2idx[0]]
        b_sf_2 = getattr(entry, 'Jet_btagWeightCMVAV2{0}{1}'.format(b_nomUpDown, flav), None)[entry.hJCMVAV2idx[1]]
        if (not b_sf_1 or not b_sf_2) and 'Double' not in name:
            #print 'problem with b_sf_...'
            sys.exit(1)

        btags_SF = b_sf_1 * b_sf_2  if 'Double' not in name else 1 
        #print 'b_sf_1={0},b_sf_2={1}'.format(b_sf_1, b_sf_2)
        #print 'b_nomUpDown is', b_nomUpDown
        #print 'flav is', flav
        #print 'another btags_SF is ', btags_SF        

        # btags_SF_up_light = entry.Jet_btagWeightCMVAV2_up_light[entry.hJCMVAV2idx[0]] * entry.Jet_btagWeightCMVAV2_up_light[entry.hJCMVAV2idx[1]] 
        # btags_SF_down_light = entry.Jet_btagWeightCMVAV2_down_light[entry.hJCMVAV2idx[0]] * entry.Jet_btagWeightCMVAV2_down_light[entry.hJCMVAV2idx[1]] 

        # btags_SF_up_heavy = entry.Jet_btagWeightCMVAV2_up_heavy[entry.hJCMVAV2idx[0]] * entry.Jet_btagWeightCMVAV2_up_heavy[entry.hJCMVAV2idx[1]] 
        # btags_SF_down_heavy = entry.Jet_btagWeightCMVAV2_down_heavy[entry.hJCMVAV2idx[0]] * entry.Jet_btagWeightCMVAV2_down_heavy[entry.hJCMVAV2idx[1]] 

        dyLOtoNLOw = 1.
        EWKw = 1.
        if 'DY' in name and 'Jets' in name:
            etabb = abs(entry.dEta_bjets)
            if etabb < 5: 
                dyLOtoNLOw = 1.*(0.940679 + 0.0306119*etabb -0.0134403*etabb*etabb + 0.0132179*etabb*etabb*etabb -0.00143832*etabb*etabb*etabb*etabb)
        # 1.153 in front of the long line above, I assume to be a k-factor and we already use 1.23, so it is removed.
        #https://github.com/GLP90/Xbb/blob/merge_silvio/python/write_regression_systematics.py#L2278
            if entry.zpt0 > 100. and  entry.zpt0 < 3000:
                print 'EWK weight'
                EWKw = -0.1808051+6.04146*(pow((entry.zpt0+759.098),-0.242556))
                #https://github.com/GLP90/Xbb/blob/merge_silvio/python/write_regression_systematics.py#L2240



        if 'Double' not in name:
            jer_up_0 = entry.Jet_corr_JERUp[entry.hJCMVAV2idx[0]]/entry.Jet_corr_JER[entry.hJCMVAV2idx[0]] if entry.Jet_corr_JER[entry.hJCMVAV2idx[0]] != 0 else None
            jer_down_0 = entry.Jet_corr_JERDown[entry.hJCMVAV2idx[0]]/entry.Jet_corr_JER[entry.hJCMVAV2idx[0]] if entry.Jet_corr_JER[entry.hJCMVAV2idx[0]] != 0 else None

            jer_up_1 = entry.Jet_corr_JERUp[entry.hJCMVAV2idx[1]]/entry.Jet_corr_JER[entry.hJCMVAV2idx[1]] if entry.Jet_corr_JER[entry.hJCMVAV2idx[1]]  != 0 else None
            jer_down_1 = entry.Jet_corr_JERDown[entry.hJCMVAV2idx[1]]/entry.Jet_corr_JER[entry.hJCMVAV2idx[1]] if entry.Jet_corr_JER[entry.hJCMVAV2idx[1]]  != 0 else None

            jec_up_0 = entry.Jet_corr_JECUp[entry.hJCMVAV2idx[0]]/entry.Jet_corr[entry.hJCMVAV2idx[0]] if entry.Jet_corr_JER[entry.hJCMVAV2idx[0]] != 0else None
            jec_down_0 = entry.Jet_corr_JECDown[entry.hJCMVAV2idx[0]]/entry.Jet_corr[entry.hJCMVAV2idx[0]] if entry.Jet_corr_JER[entry.hJCMVAV2idx[0]] != 0else None

            jec_up_1 = entry.Jet_corr_JECUp[entry.hJCMVAV2idx[1]]/entry.Jet_corr[entry.hJCMVAV2idx[1]] if entry.Jet_corr_JER[entry.hJCMVAV2idx[1]]  != 0 else None
            jec_down_1 = entry.Jet_corr_JECDown[entry.hJCMVAV2idx[1]]/entry.Jet_corr[entry.hJCMVAV2idx[1]] if entry.Jet_corr_JER[entry.hJCMVAV2idx[1]]  != 0 else None

            if any(x is None for x in [jer_up_0, jer_down_0, jer_up_1, jer_down_1, jec_up_0, jec_down_0, jec_up_1, jec_down_1]):
                continue


        if 'Double' not in name:
        #================================================
            w_jer_up = math.sqrt(jer_up_0*jer_up_1)
            w_jer_down = math.sqrt(jer_down_0*jer_down_1)
            
            w_jec_up = math.sqrt(jec_up_0*jec_up_1)
            w_jec_down = math.sqrt(jec_down_0*jec_down_1)
        else:
            w_jer_up, w_jer_down, w_jec_up, w_jec_down = 1, 1, 1, 1

        met_weight = 1.        
        modifierW = 1.

        if 'res_j' in systUnc:
            if 'Up' in systUnc:
                modifierW = w_jer_up
                if entry.met_pt !=0:
                    met_weight = entry.met_shifted_JetResUp_pt/entry.met_pt
                else:
                    continue
            elif 'Down' in systUnc:
                modifierW = w_jer_down
                if entry.met_pt !=0:
                    met_weight = entry.met_shifted_JetResDown_pt/entry.met_pt
                else:
                    continue
            else:
                sys.exit(1)

        
        
        if 'scale_j' in systUnc:
            if 'Up' in systUnc:
                btags_SF = entry.Jet_btagWeightCMVAV2_up_jes[entry.hJCMVAV2idx[0]] * entry.Jet_btagWeightCMVAV2_up_jes[entry.hJCMVAV2idx[1]] 
                #print 'inside if btags_SF is', btags_SF
                modifierW = w_jec_up
                if entry.met_pt !=0:
                    met_weight = entry.met_shifted_JetEnUp_pt/entry.met_pt 
                else:
                    continue
            elif 'Down'in systUnc:
                btags_SF = entry.Jet_btagWeightCMVAV2_down_jes[entry.hJCMVAV2idx[0]] * entry.Jet_btagWeightCMVAV2_down_jes[entry.hJCMVAV2idx[1]] 
                #print 'inside elif btags_SF is', btags_SF
                modifierW = w_jec_down
                if entry.met_pt !=0:
                    met_weight = entry.met_shifted_JetEnDown_pt/entry.met_pt 
                else:
                    continue
            else:
                sys.exit(1)


        met_weight_phi = 1.
        if 'met' in systUnc:
            #print '7'*500
            #CMS_eff_met_JetEnUp
            mis = postf[9:] 
            #print postf
            #print mis
            #print systUnc
            if 'CMS_eff_' + mis != systUnc:
                print 'check MET'
                sys.exit(1)
            #print 'mis =', mis
            one, two = mis.split('_')
            metString = one + '_shifted_' + two
            #print 'metString=',metString
            metShift_pt = getattr(entry, metString + '_pt', None)
            metShift_phi = getattr(entry, metString + '_phi', None)
           #phi does not matter to 1st order?
            if metShift_pt != None and entry.met_pt !=0:
                met_weight = metShift_pt / entry.met_pt
            else:
                print 'check metShift_pt'
                sys.exit(1)
            if metShift_phi != None and entry.met_phi !=0:
                met_weight_phi = metShift_phi / entry.met_phi
            else:
                print 'check metShift_phi'
                sys.exit(1)

        
        extraWeight = leps_SF * btags_SF
        #print 'btags_SF is again', btags_SF
#print 'modifierW is', modifierW
        #print 'met_weight is',met_weight
        #print 'leps_SF={0}, btags_SF={1}'.format(leps_SF, btags_SF)

    # JEC Up(Down): event weight = bTagWeightJECUp(Down)
    #>>>>>>>>>>>>>>>>>
    # Jet_pt * Jet_corr_JECUp(Down)/Jet_corr
    # HCSV_mass * sqrt( Jet_corr_JECUp(Down)[hJetInd1] * Jet_corr_JECUp(Down)[hJetInd2]  / Jet_corr[hJetInd1]  / Jet_corr[hJetInd2]   )
    # (HCSV_pt := recompute the 4-vector, it will be easier...)
    # met_shifted_JetEnUp(Down)_pt

    # JER Up(Down): event weight = bTagWeight
    #>>>>>>>>>>>>>>
    # Jet_pt * Jet_corr_JERUp(Down)/Jet_corr_JER
    # HCSV_mass * sqrt( Jet_corr_JERUp(Down)[hJetInd1] * Jet_corr_JERUp(Down)[hJetInd2]  / Jet_corr[hJetInd1]  / Jet_corr[hJetInd2]   )
    # (HCSV_pt := recompute the 4-vector, it will be easier...)
    # met_pt
        if 'Double' in name: #dictOfFiles[sample]
            met_weight = 1.
            met_weight_phi = 1.
            modifierW = 1.
        #print 'met_weight={0}, modifierW = {1} for {2}, and met_weight_phi = {3}'.format(met_weight, modifierW, name, met_weight_phi)

        
        b0pt = entry.bpt0 * modifierW
        b0eta = entry.beta0 * modifierW #?
        b0phi = entry.bphi0 * modifierW #?
        b0mass = entry.bmass0 * modifierW
        b0tlv = ROOT.TLorentzVector()
        b0tlv.SetPtEtaPhiM(b0pt, b0eta, b0phi, b0mass)

        b1pt = entry.bpt1 * modifierW
        b1eta = entry.beta1 * modifierW #?
        b1phi = entry.bphi1 * modifierW #?
        b1mass = entry.bmass1 * modifierW
        b1tlv = ROOT.TLorentzVector()
        b1tlv.SetPtEtaPhiM(b1pt, b1eta, b1phi, b1mass)

        dR_bjets_shifted = b0tlv.DeltaR (b1tlv)
        #print '8' *500
        #print 'dR_bjets_shifted = {0}, entry.dR_bjets = {1}'.format(dR_bjets_shifted, entry.dR_bjets)

        zmass[0] = entry.zmass
        met_pt[0] = entry.met_pt * met_weight
        hmass0[0] = entry.hmass0
        hmass1[0] = entry.hmass1 * modifierW
        dR_leps[0] = entry.dR_leps
        dR_bjets[0] = dR_bjets_shifted #entry.dR_bjets
        zpt0[0] = entry.zpt0
        hpt0[0] = entry.hpt0
        hpt1[0] = entry.hpt1 * modifierW

        if 'SR' in physRegion:
            if zmass[0] < 76 or zmass[0] > 106: continue
            if hmass1[0] < 90 or hmass1[0] > 150: continue
        elif 'CRDY' in physRegion:
            if zmass[0] < 76 or zmass[0] > 106: continue
            if hmass1[0] >= 90 and hmass1[0] <= 150: continue
        elif 'CRTT' in physRegion:
            if zmass[0] <= 106: continue
            if hmass1[0] < 90 or hmass1[0] > 150: continue
        else:
            print 'smth is wrong with physRegion' 
            sys.exit(1)

        if hmass1[0] < 20: continue #remove QCD

        
        if physRegion  == "CRDYlow":
            if hmass1[0] >= 90: continue
        elif physRegion == "CRDYhigh":
            if hmass1[0] <= 150: continue
        else:
            pass

        Z_p4=ROOT.TLorentzVector()
        missing_p4=ROOT.TLorentzVector()
        hh_tlv = ROOT.TLorentzVector()
        Htobb_p4 = ROOT.TLorentzVector()

        Z_p4.SetPtEtaPhiM(zpt0[0], entry.zeta0, entry.zphi0, zmass[0])
        Htobb_p4.SetPtEtaPhiM(hpt1[0], entry.heta1, entry.hphi1, hmass1[0])
        missing_p4.SetPtEtaPhiM(met_pt[0], entry.met_eta, entry.met_phi*met_weight_phi, entry.met_mass*met_weight)
# build HH candidate and draw mass transverse                                                                                                 
        hh_Mt = (Htobb_p4 + Z_p4 + missing_p4).Mt()
        #print 'hh_Mt is', hh_Mt
        #print 'entry.hhmt is', entry.hhmt 

        if 'Double' not in name:
            if round(entry.evWgt,6) != round(entry.xsec/entry.countWeighted, 6):
                print 'wrong event weight, exiting'
                print 'entry.evWgt is', entry.evWgt
                if entry.countWeighted !=0:
                    print 'entry.xsec/entry.countWeighted, which is {0}/{1} = {2}'.format(entry.xsec, entry.countWeighted,entry.xsec/entry.countWeighted)
                sys.exit(1)
            else:
                eqLumi = entry.evWgt * extraWeight
                if 'DY' in name and 'Jets' in name:
                    eqLumi *= dyLOtoNLOw * EWKw
        else:
            eqLumi = 1
            #if massPoint > 450:


        
            
        output = reader.EvaluateMVA(methodName)
            #else:
             #   output = reader_lowMass.EvaluateMVA(methodName)
        
        #eqLumi *= lumi
        histos['bdt_response{0}'.format(postf)].Fill(output, eqLumi)        

        if physRegion == 'SR':
            if not output > bdtCut:
                #print 'in SR, but cut is lower, skip'
                continue
        else:
            #print 'in CRxy'
            pass

        
        # this means all distributions for SR are after they pass BDT cut, for CRs w/o BDT cut at all
        histos['bdt_response_afterCut{0}'.format(postf)].Fill(output, eqLumi)
        #if 'nominal' not in systUnc:
        if hh_Mt < minValue:
            hh_Mt = minValue + 1 
        histos['hhMt{0}'.format(postf)].Fill(min(hh_Mt, centinel), eqLumi)


        #histos['zmass_long'].Fill(zmass[0], eqLumi)
        #histos['zmass_mid'].Fill(zmass[0], eqLumi)

        if zmass[0] > Zmasshigh: #155:
            zmass[0] = Zmasshigh - 1 
        histos['zmass_high{0}'.format(postf)].Fill(zmass[0], eqLumi)
        if zmass[0] > Zmassmid: #106
            zmass[0] = Zmassmid - 1 
        histos['zmass{0}'.format(postf)].Fill(zmass[0], eqLumi)
        histos['zmass_oneBin{0}'.format(postf)].Fill(zmass[0], eqLumi)

        histos['met_pt{0}'.format(postf)].Fill(min(met_pt[0], met_pt_binMax-1), eqLumi)


        histos['hmass0{0}'.format(postf)].Fill(max(min(hmass0[0], Hzz_mass_binMax-1), Hzz_mass_binMin+1), eqLumi)
#        if hmass1[0] < Hbb_mass_binMin:
 #           hmass1[0] = Hbb_mass_binMin + 1
  #      if hmass1[0] > Hbb_mass_binMax:
   #        hmass1[0] = Hbb_mass_binMax - 1
        histos['hmass1{0}'.format(postf)].Fill(max(min(hmass1[0], Hbb_mass_binMax-1), Hbb_mass_binMin+1), eqLumi)
        histos['hmass1_oneBin{0}'.format(postf)].Fill(max(min(hmass1[0], Hbb_mass_binMax-1), Hbb_mass_binMin+1), eqLumi)

        histos['dR_leps{0}'.format(postf)].Fill(min(dR_leps[0], dR_binMax-1), eqLumi)
        histos['dR_bjets{0}'.format(postf)].Fill(min(dR_bjets[0], dR_binMax-1), eqLumi)
        histos['dEta_bjets{0}'.format(postf)].Fill(entry.dEta_bjets, eqLumi)
        histos['dEta_bjets_abs{0}'.format(postf)].Fill(abs(entry.dEta_bjets), eqLumi)
        histos['zpt0{0}'.format(postf)].Fill(min(zpt0[0], Zpt_binMax-1), eqLumi)
        histos['hpt0{0}'.format(postf)].Fill(min(hpt0[0], Hzz_pt_binMax-1), eqLumi)
        histos['hpt1{0}'.format(postf)].Fill(min(hpt1[0], Hbb_pt_binMax-1), eqLumi)

        histos['bjet0pt{0}'.format(postf)].Fill(entry.bpt0, eqLumi)
        histos['bjet1pt{0}'.format(postf)].Fill(entry.bpt1, eqLumi)
        histos['bjet0eta{0}'.format(postf)].Fill(entry.beta0, eqLumi)
        histos['bjet1eta{0}'.format(postf)].Fill(entry.beta1, eqLumi)
        histos['btagDiscr0{0}'.format(postf)].Fill(entry.btagDiscr0, eqLumi)
        histos['btagDiscr1{0}'.format(postf)].Fill(entry.btagDiscr1, eqLumi)

        histos['btag0sf{0}'.format(postf)].Fill(b_sf_1, eqLumi)
        histos['btag1sf{0}'.format(postf)].Fill(b_sf_2, eqLumi)
        histos['bjet_sf{0}'.format(postf)].Fill(btags_SF, eqLumi)

        histos['lep0pt{0}'.format(postf)].Fill(entry.leppt0, eqLumi)
        histos['lep1pt{0}'.format(postf)].Fill(entry.leppt1, eqLumi)
        histos['lep0eta{0}'.format(postf)].Fill(entry.lepeta0, eqLumi)
        histos['lep1eta{0}'.format(postf)].Fill(entry.lepeta1, eqLumi)

        histos['lep0iso03{0}'.format(postf)].Fill(entry.vLeptons_pfRelIso03[0], eqLumi)
        histos['lep1iso03{0}'.format(postf)].Fill(entry.vLeptons_pfRelIso03[1], eqLumi)
        histos['lep0iso04{0}'.format(postf)].Fill(entry.vLeptons_pfRelIso04[0], eqLumi)
        histos['lep1iso04{0}'.format(postf)].Fill(entry.vLeptons_pfRelIso04[1], eqLumi)

        histos['sf_trk{0}'.format(postf)].Fill(sf_trk, eqLumi)
        histos['sf_id{0}'.format(postf)].Fill(sf_id, eqLumi)
        histos['sf_iso{0}'.format(postf)].Fill(sf_iso, eqLumi)
        histos['sf_dilep{0}'.format(postf)].Fill(sf_trig, eqLumi)
        histos['lep_sf{0}'.format(postf)].Fill(leps_SF, eqLumi)

        histos['dyLOtoNLO_sf{0}'.format(postf)].Fill(dyLOtoNLOw, eqLumi)
        histos['EWK_sf{0}'.format(postf)].Fill(EWKw, eqLumi)



        if 'HWW' in name or 'Hzz' in name:
            if (ievt%100)==0 : print 'For tree ', dictOfFiles[sample], ' event ', ievt,' has hhmt = ',hh_Mt,' and MVA output = ', output, ' xsec is ', entry.xsec, ' nEvents is ', entry.countWeighted, ' eqLumi is', eqLumi, ' systUnc is', systUnc
        else:
            if (ievt%10000)==0 : print 'For tree ', dictOfFiles[sample], ' event ', ievt,' has hhmt = ',hh_Mt,' and MVA output = ', output, ' xsec is ', entry.xsec, ' nEvents is ', entry.countWeighted, ' eqLumi is', eqLumi, ' systUnc is', systUnc

        ievt += 1
#    if (ievt > 20000) : break

    print 'max of BDT response histogram is ', histos['bdt_response{0}'.format(postf)].GetMaximum()

    
    if sample:
        if sample.IsOpen():
            print 'sample.IsOpen() is ', sample.IsOpen()
            bazinga('closing "sample" file')
            doHack = True
            if not doHack:
                sample.Close()
            else:
                closeFile = ROOT.TFile.Close(sample)
                bazinga('after hack of closing "sample" file')
                print 'closeFile is ', closeFile
                print 'sample.IsOpen() is ', sample.IsOpen()
            print 'sample is ', sample

    bazinga('cd into outpur file {0}'.format(fO.GetName()) )
    fO.cd()
    for key in histos: 
        bazinga('save histograms for  {0}'.format(fO.GetName()) )
        histos[key].Write()
    bazinga('closing output file')
    fO.close()
    #time.sleep(15)
    #print 'time.sleep(15)'


end_time = time.time()
time_taken = end_time - start_time # time_taken is in seconds                                                                                                                                   
hours, rest = divmod(time_taken,3600)
minutes, seconds = divmod(rest, 60)
bazinga( "---it took {hours} hours, {minutes} minutes and {seconds:.1f} seconds to run the analysis ---".format (hours=hours, minutes=minutes, seconds=seconds) )

