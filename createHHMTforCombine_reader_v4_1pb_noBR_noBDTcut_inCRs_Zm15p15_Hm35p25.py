from rootpy.io import root_open
import time 

name = 'shapes'


debugMode = True # for priting with bazinga                                 
def bazinga (mes):
    if debugMode:
        print mes

methodName = 'BDT'

import ROOT
from ROOT import TMVA
import sys, os

start_time = time.time()

args_are_given = len(sys.argv) > 1
#print sys.argv[0] # script name itself                                                                                            
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
        if physRegion not in {'SR', 'CRDY', 'CRTT'}:
            print 'wrong "physRegion", please use "region:SR/CRDY/CRTT"'
            sys.exit(1)
    else:
        print 'not specified "physRegion", please use "region:SR/CRDY/CRTT"'
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


else:
    print '"dirWithMCSamples" or "mvaXml" files are not specified, please follow the syntax W/O spaces for XMLs: python createHHMTforCombine_reader.py "dirWithMCSamples" "mvaLowMassXml,mvaHighMassXml" "region:SR/CRDY/CRTT"'
    sys.exit(1)

weightFile_lowMass = list_of_diff_mvas[0]
weightFile_highMass =  list_of_diff_mvas[1]




TMVA.Tools.Instance()
reader_lowMass = TMVA.Reader( "!Color:!Silent" )
reader_highMass = TMVA.Reader( "!Color:!Silent" )


from array import array

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
    

zmass = array('f',[0])
met_pt = array('f',[0])
hmass0 = array('f',[0])

hmass1 = array('f',[0])
dR_leps = array('f',[0])
dR_bjets = array('f',[0])

zpt0 = array('f',[0])
hpt0 = array('f',[0])
hpt1 = array('f',[0])


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

post = " = array('f',[0])"
pref = 'reader_highMass.AddVariable("'
post = '", '

for v in myVars:
    print pref + v + post + v + ')'

reader_highMass.AddVariable("zmass", zmass)
reader_highMass.AddVariable("met_pt", met_pt)
reader_highMass.AddVariable("hmass0", hmass0)

reader_highMass.AddVariable("hmass1", hmass1)
reader_highMass.AddVariable("dR_leps", dR_leps)
reader_highMass.AddVariable("dR_bjets", dR_bjets)

reader_highMass.AddVariable("zpt0", zpt0)
reader_highMass.AddVariable("hpt0", hpt0)
reader_highMass.AddVariable("hpt1", hpt1)

 
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


bazinga('weightFile_highMass is {0}'.format(weightFile_highMass))
reader_highMass.BookMVA('BDT', weightFile_highMass)

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

bgInputFile_ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV_powheg_TuneCUETP8M1__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_ext1_v1 = ROOT.TFile(dirWithMCSamples + "ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext1-v1_minitree.root")

bgInputFile_ST_tW_antitop_5f_inclusiveDecays_13TeV_powheg_Py8_TuneCUETP8M1__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_ext1_v1 = ROOT.TFile(dirWithMCSamples + "ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-Py8_TuneCUETP8M1__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext1-v1_minitree.root")

bgInputFile_ST_tW_top_5f_NoFullyHadronicDecays_13TeV_powheg_TuneCUETP8M1__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_ext1_v1 = ROOT.TFile(dirWithMCSamples + "ST_tW_top_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext1-v1_minitree.root")

bgInputFile_ST_tW_top_5f_inclusiveDecays_13TeV_powheg_Py8_TuneCUETP8M1__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_ext1_v1 = ROOT.TFile(dirWithMCSamples + "ST_tW_top_5f_inclusiveDecays_13TeV-powheg-Py8_TuneCUETP8M1__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext1-v1_minitree.root")

bgInputFile_TT_TuneCUETP8M2T4_13TeV_powheg_Py8__RunIISummer16MAv2_PUMoriond17_backup_80r2as_2016_TrancheIV_v6_v1 = ROOT.TFile(dirWithMCSamples + "TT_TuneCUETP8M2T4_13TeV-powheg-Py8__RunIISummer16MAv2-PUMoriond17_backup_80r2as_2016_TrancheIV_v6-v1_minitree.root")

bgInputFile_WW_TuneCUETP8M1_13TeV_Py8__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 = ROOT.TFile(dirWithMCSamples + "WW_TuneCUETP8M1_13TeV-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root")

bgInputFile_WZ_TuneCUETP8M1_13TeV_Py8__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 = ROOT.TFile(dirWithMCSamples + "WZ_TuneCUETP8M1_13TeV-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root")

bgInputFile_ZH_HToBB_ZToLL_M125_13TeV_amcatnloFXFX_madspin_Py8__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 = ROOT.TFile(dirWithMCSamples + "ZH_HToBB_ZToLL_M125_13TeV_amcatnloFXFX_madspin_Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root")

bgInputFile_ZZ_TuneCUETP8M1_13TeV_Py8__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 = ROOT.TFile(dirWithMCSamples + "ZZ_TuneCUETP8M1_13TeV-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root")

dataInputFile_DoubleMuon__Run2016B_03Feb2017_ver1_v1 = ROOT.TFile(dirWithMCSamples + "DoubleMuon__Run2016B-03Feb2017_ver1-v1_minitree.root")

dataInputFile_DoubleMuon__Run2016B_03Feb2017_ver2_v2 = ROOT.TFile(dirWithMCSamples + "DoubleMuon__Run2016B-03Feb2017_ver2-v2_minitree.root")

dataInputFile_DoubleMuon__Run2016C_03Feb2017_v1 = ROOT.TFile(dirWithMCSamples + "DoubleMuon__Run2016C-03Feb2017-v1_minitree.root")

dataInputFile_DoubleMuon__Run2016D_03Feb2017_v1 = ROOT.TFile(dirWithMCSamples + "DoubleMuon__Run2016D-03Feb2017-v1_minitree.root")

dataInputFile_DoubleMuon__Run2016E_03Feb2017_v1 = ROOT.TFile(dirWithMCSamples + "DoubleMuon__Run2016E-03Feb2017-v1_minitree.root")

dataInputFile_DoubleMuon__Run2016F_03Feb2017_v1 = ROOT.TFile(dirWithMCSamples + "DoubleMuon__Run2016F-03Feb2017-v1_minitree.root")

dataInputFile_DoubleMuon__Run2016G_03Feb2017_v1 = ROOT.TFile(dirWithMCSamples + "DoubleMuon__Run2016G-03Feb2017-v1_minitree.root")

dataInputFile_DoubleMuon__Run2016H_03Feb2017_ver2_v1 = ROOT.TFile(dirWithMCSamples + "DoubleMuon__Run2016H-03Feb2017_ver2-v1_minitree.root")

dataInputFile_DoubleMuon__Run2016H_03Feb2017_ver3_v1 = ROOT.TFile(dirWithMCSamples + "DoubleMuon__Run2016H-03Feb2017_ver3-v1_minitree.root")



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

    bgInputFile_ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV_powheg_TuneCUETP8M1__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_ext1_v1 : "ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext1-v1",

    bgInputFile_ST_tW_antitop_5f_inclusiveDecays_13TeV_powheg_Py8_TuneCUETP8M1__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_ext1_v1 : "ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-Py8_TuneCUETP8M1__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext1-v1",

    bgInputFile_ST_tW_top_5f_NoFullyHadronicDecays_13TeV_powheg_TuneCUETP8M1__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_ext1_v1 : "ST_tW_top_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext1-v1",

    bgInputFile_ST_tW_top_5f_inclusiveDecays_13TeV_powheg_Py8_TuneCUETP8M1__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_ext1_v1 : "ST_tW_top_5f_inclusiveDecays_13TeV-powheg-Py8_TuneCUETP8M1__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext1-v1",

    bgInputFile_TT_TuneCUETP8M2T4_13TeV_powheg_Py8__RunIISummer16MAv2_PUMoriond17_backup_80r2as_2016_TrancheIV_v6_v1 : "TT_TuneCUETP8M2T4_13TeV-powheg-Py8__RunIISummer16MAv2-PUMoriond17_backup_80r2as_2016_TrancheIV_v6-v1",

    bgInputFile_WW_TuneCUETP8M1_13TeV_Py8__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 : "WW_TuneCUETP8M1_13TeV-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1",

    bgInputFile_WZ_TuneCUETP8M1_13TeV_Py8__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 : "WZ_TuneCUETP8M1_13TeV-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1",

    bgInputFile_ZH_HToBB_ZToLL_M125_13TeV_amcatnloFXFX_madspin_Py8__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 : "ZH_HToBB_ZToLL_M125_13TeV_amcatnloFXFX_madspin_Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1",

    bgInputFile_ZZ_TuneCUETP8M1_13TeV_Py8__RunIISummer16MAv2_PUMoriond17_80r2as_2016_TrancheIV_v6_v1 : "ZZ_TuneCUETP8M1_13TeV-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1",

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

# dictOfFiles = {


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

outDir = name + massRegion + '_' + physRegion  + '_' + str(bdtCut) + '/'

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
elif muonIsThere and not eleIsThere:
    leptonType = "mumu"
elif eleIsThere and not muonIsThere:
    leptonType = "elel"
else:
    print 'no data, exiting...'
    
for sample, name in dictOfFiles.items():
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
        if massRegion == 'high' and mass <=  450: continue
    
    reader = reader_lowMass if massRegion == 'low' else reader_highMass    

    bazinga('process {0}'.format(name))
    minValue = 100
    maxValue = 1200
    centinel = maxValue-1
    histos = {
        'hhMt_long'      :ROOT.TH1F('hhMt_long', ';"HiggsHiggson" transverse mass [GeV]; Events', (maxValue - minValue)/20, minValue, maxValue),
        'bdt_response'      :ROOT.TH1F('bdt_response', ';BDT response; Events', 100, -1., +1.),
        'bdt_response_afterCut'      :ROOT.TH1F('bdt_response_afterCut', ';BDT response; Events', 100, -1., +1.),

        'dEta_lb_min'       :ROOT.TH1F('dEta_lb_min', ';|#Delta#eta|_{min}(l, b); Events', 20, 0, 5),
        # 'dEta_ZH'       :ROOT.TH1F('dEta_ZH', ';|#Delta#eta|(Z_{ll}, H_{bb}); Events', 20, 0, 5),
        # 'dEta_bjets'       :ROOT.TH1F('dEta_bjets', ';|#Delta#eta|(b_{1}, b_{2}); Events', 20, 0, 5),
        # 'dEta_leps'       :ROOT.TH1F('dEta_leps', ';|#Delta#eta|(l_{1}, l_{2}); Events', 20, 0, 5),

        # 'dPhi_lb_min'       :ROOT.TH1F('dPhi_lb_min', ';|#Delta#phi|_{min}(l, b); Events', 20, 0, 5),
        # 'dPhi_ZH'       :ROOT.TH1F('dPhi_ZH', ';|#Delta#phi|(Z_{ll}, H_{bb}); Events', 20, 0, 5),
        # 'dPhi_bjets'       :ROOT.TH1F('dPhi_bjets', ';|#Delta#phi|(b_{1}, b_{2}); Events', 20, 0, 5),
        # 'dPhi_leps'       :ROOT.TH1F('dPhi_leps', ';|#Delta#phi|(l_{1}, l_{2}); Events', 20, 0, 5),

        # 'dR_lb_min'       :ROOT.TH1F('dR_lb_min', ';#DeltaR_{min}(l, b); Events', 20, 0, 8),
        # 'dR_ZH'       :ROOT.TH1F('dR_ZH', ';#DeltaR(Z_{ll}, H_{bb}); Events', 20, 0, 8),
        'dR_bjets'       :ROOT.TH1F('dR_bjets', ';#DeltaR(b_{1}, b_{2}); Events', 20, 0, 8),
        'dR_leps'       :ROOT.TH1F('dR_leps', ';#DeltaR(l_{1}, l_{2}); Events', 20, 0, 8),

      
        #'nbjets_raw':ROOT.TH1F('nbjets_raw'     ,';b-jet multiplicity; Events'                          , 7,0,7),
        'nbjets':ROOT.TH1F('nbjets'     ,';b-jet multiplicity; Events'                          , 7,0,7),
        #'metpt_raw'     :ROOT.TH1F('metpt_raw'      ,';MET [GeV]; Events'                , 35,0,350),
        #'njets_raw'     :ROOT.TH1F('njets_raw'  ,';Jet multiplicity; Events'                            , 9,0,9),
        #'nleps_raw'             :ROOT.TH1F('nleps_raw'          ,';Lepton multiplicity; Events'                         , 3,1,4),


        'met_pt'     :ROOT.TH1F('met'      ,';MET [GeV]; Events'                , 35,0,350),
        # 'nleps'         :ROOT.TH1F('nleps'              ,';Lepton multiplicity; Events'                         , 3,1,4),
        # 'bjetpt'    :ROOT.TH1F('bjetpt'     ,';p_{T}(b jet) [GeV]; Events'              , 35,0,350),
        # 'bjeteta'   :ROOT.TH1F('bjeteta'    ,';#eta(b jet); Events'                     , 20,-2.4,2.4),
        # 'leppt'     :ROOT.TH1F('leppt'      ,';p_{T}(lepton) [GeV]; Events'             , 25,0,250),
        # 'lepeta'    :ROOT.TH1F('lepeta'     ,';#eta(lepton); Events'                    , 20,-2.4,2.4),
        # 'bjet0pt'       :ROOT.TH1F('bjet0pt'    ,';Leading b-Jet p_{T} [GeV]; Events'       , 35, 0., 350.),
        # 'bjet1pt'       :ROOT.TH1F('bjet1pt'    ,';Subleading b-Jet p_{T} [GeV]; Events'        , 25, 0., 250.),
        # 'bjet0eta'      :ROOT.TH1F('bjet0eta'   ,';Leading b-Jet #eta; Events'                          , 20, -2.4, 2.4),
        # 'bjet1eta'      :ROOT.TH1F('bjet1eta'   ,';Subleading b-Jet #eta; Events'                       , 20, -2.4, 2.4),
        'btagDiscr0'       :ROOT.TH1F('btagDiscrCSV0'  ,';Leading b-Jet CSV SF; Events'            , 60, 0.4, 1.),
        'btagDiscr1'       :ROOT.TH1F('btagDiscrCSV1'  ,';Subleading b-Jet CSV SF; Events'         , 60, 0.4, 1.),
        # 'lep0pt'        :ROOT.TH1F('lep0pt'             ,';Leading Lepton p_{T} [GeV]; Events'          , 25, 0., 250.),
        # 'lep1pt'        :ROOT.TH1F('lep1pt'             ,';Subleading Lepton p_{T} [GeV]; Events'       , 20, 0., 200.),
        # 'lep0eta'       :ROOT.TH1F('lep0eta'    ,';Leading Lepton #eta ; Events'                    , 20, -2.4, 2.4),
        # 'lep1eta'       :ROOT.TH1F('lep1eta'    ,';Subleading Lepton #eta ; Events'             , 20, -2.4, 2.4),
        'hCSVmass'      :ROOT.TH1F('hCSVmass', ';HCSV mass [GeV]; Events', 40, 85, 165),
        # 'hCSVmass_long'      :ROOT.TH1F('hCSVmass_long', ';HCSV mass [GeV]; Events', 45, 30, 220),
        'hCSVpt'      :ROOT.TH1F('hCSVpt', ';HCSV p_{T} [GeV]; Events', 50, 0, 400),
        'hZZpt'      :ROOT.TH1F('hZZpt', ';H#rightarrowZZ p_{T} [GeV]; Events', 50, 0, 400),
        # 'hZZmt'      :ROOT.TH1F('hZZmt', ';H#rightarrowZZ transverse mass [GeV]; Events', 40, 50, 450),
        # 'hZZmt_long'      :ROOT.TH1F('hZZmt_long', ';H#rightarrowZZ transverse mass [GeV]; Events', 100, 50, 1050),

        #'hhMt'      :ROOT.TH1F('hhMt', ';"HiggsHiggson" transverse mass [GeV]; Events', 40, 550, 950),

        'zmass'      :ROOT.TH1F('zmass', ';Z mass [GeV]; Events', 20, 70, 110),
        'hmass0'      :ROOT.TH1F('hmass0', ';Hbb mass [GeV]; Events', 25, 75, 175),
        'hmass1'      :ROOT.TH1F('hmass1', ';HZZ mass [GeV]; Events', 25, 75, 175),
        #'zHMass'      :ROOT.TH1F('zHMass', ';ZH mass [GeV]; Events', 50, 115, 315),
        #'zHTransMass'      :ROOT.TH1F('zHTransMass', ';ZH transverse mass [GeV]; Events', 50, 115, 315),
        #'zMass_long'      :ROOT.TH1F('zMass_long', ';Z mass [GeV]; Events', 50, 20, 220),
        'zpt0'      :ROOT.TH1F('zpt0', ';Z p_{T} [GeV]; Events', 50, 0, 300),
        'hpt0'      :ROOT.TH1F('hpt0', ';Hbb p_{T} [GeV]; Events', 50, 0, 300),
        'hpt1'      :ROOT.TH1F('hpt1', ';HZZ p_{T} [GeV]; Events', 50, 0, 300),
        

        # 'mt2_llmet' :ROOT.TH1F('mt2_llmet', ';l_{1}l_{2}met mt2[GeV]; Events', 50, 0, 300),
        # 'mt2_b1l1b2l2met':ROOT.TH1F('mt2_b1l1b2l2met', ';b_{1}l_{1}b_{2}l_{2}met mt2 [GeV]; Events', 50, 0, 300),
        # 'mt2_b1l2b2l1met':ROOT.TH1F('mt2_b1l2b2l1met', ';b_{1}l_{2}b_{2}l_{1}met mt2 [GeV]; Events', 50, 0, 300),
        # 'mt2_bbmet':ROOT.TH1F('mt2_bbmet', ';b_{1}b_{2}met mt2[GeV]; Events', 50, 0, 300),
        # 'mt2_ZHmet':ROOT.TH1F('mt2_ZHmet', ';ZHmet mt2[GeV]; Events', 100, 0, 1000),
        # 'min_mt2_blmet':ROOT.TH1F('min_mt2_blmet', ';blmet mt2 [GeV]; Events', 50, 0, 300),

        }




    for key in histos:
        histos[key].Sumw2()
        histos[key].SetDirectory(0)


    ievt = 0
    
    print 'leptonType is', leptonType
    fO = root_open(outDir + name + '_shapes_' + leptonType +  '.root', "recreate")
    bazinga('before loop over {0}'.format(sample.GetName() ) )
    for entry in sample.tree:

        if physRegion == 'SR':
            if entry.zmass < 76 or entry.zmass > 106: continue
            if entry.hmass1 < 90 or entry.hmass1 > 150: continue
        elif physRegion == 'CRDY':
            if entry.zmass < 76 or entry.zmass > 106: continue
            if entry.hmass1 >= 90 and entry.hmass1 <= 150: continue
        elif physRegion == 'CRTT':
            if entry.zmass <= 106: continue
            if entry.hmass1 < 90 or entry.hmass1 > 150: continue
        else:
            print 'smth is wrong with physRegion' 
            sys.exit(1)

#            for v in myVars:
 #               print  v + '[0] = entry.' + v
  
        zmass[0] = entry.zmass
        met_pt[0] = entry.met_pt
        hmass0[0] = entry.hmass0
        hmass1[0] = entry.hmass1
        dR_leps[0] = entry.dR_leps
        dR_bjets[0] = entry.dR_bjets
        zpt0[0] = entry.zpt0
        hpt0[0] = entry.hpt0
        hpt1[0] = entry.hpt1  
        
        lumi = 35900.
        if 'Double' not in name:
            if round(entry.evWgt,6) != round(entry.xsec/entry.countWeighted, 6):
                print 'wrong event weight, exiting'
                print 'entry.evWgt is', entry.evWgt
                print 'entry.xsec/entry.countWeighted, which is {0}/{1} = {2}'.format(entry.xsec, entry.countWeighted,entry.xsec/entry.countWeighted)
                sys.exit(1)
            else:
                eqLumi = entry.evWgt
        else:
            eqLumi = 1
            #if massPoint > 450:
        output = reader.EvaluateMVA(methodName)
            #else:
             #   output = reader_lowMass.EvaluateMVA(methodName)
        
        #eqLumi *= lumi
        histos['bdt_response'].Fill(output, eqLumi)        

        if physRegion == 'SR':
            if not output > bdtCut:
                #print 'in SR, but cut is lower, skip'
                continue
        else:
            #print 'in CRxy'
            pass
        
        # this means all distributions for SR are after they pass BDT cut, for CRs w/o BDT cut at all
        histos['hhMt_long'].Fill(min(entry.hhmt, centinel), eqLumi)
        histos['bdt_response_afterCut'].Fill(output, eqLumi)
        histos['zmass'].Fill(entry.zmass, eqLumi)
        histos['met_pt'].Fill(entry.met_pt, eqLumi)
        histos['hmass0'].Fill(entry.hmass0, eqLumi)
        histos['hmass1'].Fill(entry.hmass1, eqLumi)
        histos['dR_leps'].Fill(entry.dR_leps, eqLumi)
        histos['dR_bjets'].Fill(entry.dR_bjets, eqLumi)
        histos['zpt0'].Fill(entry.zpt0, eqLumi)
        histos['hpt0'].Fill(entry.hpt0, eqLumi)
        histos['hpt1'].Fill(entry.hpt1, eqLumi)



        if 'HWW' in name:
            if (ievt%100)==0 : print 'For tree ', dictOfFiles[sample], ' event ', ievt,' has hhmt = ',entry.hhmt,' and MVA output = ', output, ' xsec is ', entry.xsec, ' nEvents is ', entry.countWeighted, ' eqLumi is', eqLumi
        else:
            if (ievt%10000)==0 : print 'For tree ', dictOfFiles[sample], ' event ', ievt,' has hhmt = ',entry.hhmt,' and MVA output = ', output, ' xsec is ', entry.xsec, ' nEvents is ', entry.countWeighted, ' eqLumi is', eqLumi
        ievt += 1
#    if (ievt > 20000) : break

    print 'max of BDT response histogram is ', histos['bdt_response'].GetMaximum()

    
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

