from rootpy.io import root_open
debugMode = True # for priting with bazinga                                                       

def bazinga (mes):
    if debugMode:
        print mes

methodName = 'BDT'

import ROOT
from ROOT import TMVA
import sys, os

args_are_given = len(sys.argv) > 1
#print sys.argv[0] # script name itself                                                                                            
#print sys.argv[1] # 1st passed argument, file with samples                                                                        #print sys.argv[2] # 2nd passed argument, comma separated list of xml trainings                                                         

prefix = 'dataset/weights/'
if args_are_given:

    dirWithMCSamples = sys.argv[1]
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


else:
    print '"dirWithMCSamples" or "mvaXml" files are not specified, please follow the syntax W/O spaces for XMLs: python createHHMTforCombine_reader.py "dirWithMCSamples" "mvaLowMassXml,mvaHighMassXml" "region:SR/CRDY/CRTT"'
    sys.exit(1)

weightFile_lowMass = list_of_diff_mvas[0]
weightFile_highMass =  list_of_diff_mvas[1]




TMVA.Tools.Instance()
reader_lowMass = TMVA.Reader( "!Color:!Silent" )
reader_highMass = TMVA.Reader( "!Color:!Silent" )

from array import array

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



bazinga('weightFile_lowMass is {0}'.format(weightFile_lowMass))
reader_lowMass.BookMVA('BDT', weightFile_lowMass)


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


bazinga('weightFile_highMass is {0}'.format(weightFile_highMass))
reader_highMass.BookMVA('BDT', weightFile_highMass)


sigInputFile_260 = ROOT.TFile("BulkGraviton_M260_Hzz_minitree.root")
sigInputFile_270 = ROOT.TFile("BulkGraviton_M270_Hzz_minitree.root")
sigInputFile_300 = ROOT.TFile("BulkGraviton_M300_Hzz_minitree.root")
sigInputFile_350 = ROOT.TFile("BulkGraviton_M350_Hzz_minitree.root")
sigInputFile_400 = ROOT.TFile("BulkGraviton_M400_Hzz_minitree.root")
sigInputFile_450 = ROOT.TFile("BulkGraviton_M450_Hzz_minitree.root")
sigInputFile_600 = ROOT.TFile("BulkGraviton_M600_Hzz_minitree.root")
sigInputFile_650 = ROOT.TFile("BulkGraviton_M650_Hzz_minitree.root")
sigInputFile_900 = ROOT.TFile("BulkGraviton_M900_Hzz_minitree.root")
sigInputFile_1000 = ROOT.TFile("BulkGraviton_M1000_Hzz_minitree.root")


bgInputFile_TT = ROOT.TFile("TT_Tune_minitree.root")
bgInputFile_DY_1j = ROOT.TFile("DY1JetsToLL_M50_minitree.root")
bgInputFile_DY_2j = ROOT.TFile("DY2JetsToLL_M50_minitree.root")
bgInputFile_DY_3j = ROOT.TFile("DY3JetsToLL_M50_minitree.root")
bgInputFile_DY_4j = ROOT.TFile("DY4JetsToLL_M50_minitree.root")

dictOfFiles = {
    sigInputFile_260:'Signal_260',
    sigInputFile_270:'Signal_270',
    sigInputFile_300:'Signal_300',
    sigInputFile_350:'Signal_350',
    sigInputFile_400:'Signal_400',
    sigInputFile_450:'Signal_450',
    sigInputFile_600:'Signal_600',
    sigInputFile_650:'Signal_650',
    sigInputFile_900:'Signal_900',
    sigInputFile_1000:'Signal_1000',
    bgInputFile_TT: 'TT',
    bgInputFile_DY_1j: 'DY_1j',
    bgInputFile_DY_2j: 'DY_2j',
    bgInputFile_DY_3j: 'DY_3j',
    bgInputFile_DY_4j: 'DY_4j'
}


outDir = massPoint + '_' + physRegion  + '_' + str(bdtCut) + '/'

print 'outDir is ', outDir
if not os.path.exists(outDir):
    os.makedirs(outDir)


#sigInputFile_260

for sample, name in dictOfFiles.items():
    #if 'Signal' not in name: continue
    bazinga('processing {0}'.format(physRegion) )
    if 'Signal' in name:
        mass = int(name[7:])
    else:
        mass = -10 # for BG

    bazinga('process {0}'.format(name))
    histos = {

        'hhMt_long'      :ROOT.TH1F('hhMt_long', ';"HiggsHiggson" transverse mass [GeV]; Events', 55, 200, 1300),
        'bdt_response'      :ROOT.TH1F('bdt_response', ';"BDT response; p.d.u.', 100, -1., +1.)
        
        }




    for key in histos:
        histos[key].Sumw2()
        histos[key].SetDirectory(0)


    ievt = 0
    fO = root_open(outDir + name + '_hhmt.root', "recreate")
    bazinga('before loop over {0}'.format(sample.GetName() ) )
    for entry in sample.tree:

        if physRegion == 'SR':
            if entry.zmass < 76 or entry.zmass > 106: continue
            if entry.hmass1 < 90 or entry.hmass1 > 150: continue
        elif physRegion == 'CRDY':
            if entry.zmass < 76 or entry.zmass > 106: continue
            if entry.hmass1 >= 90 and entry.hmass1 <= 150: continue
        elif physRegion == 'CRTT':
            if entry.zmass >= 76 and entry.zmass <= 106: continue
            if entry.hmass1 < 90 or entry.hmass1 > 150: continue
        else:
            print 'smth is wrong with physRegion' 
            sys.exit(1)


        metpt[0] = entry.metpt
        dR_leps[0] = entry.dR_leps
        dR_bjets[0] = entry.dR_bjets
        btag0[0] = entry.btag0
        btag1[0] = entry.btag1
        hpt0[0] = entry.hpt0
        hpt1[0] = entry.hpt1
        nbjets[0] = entry.nbjets
        dEta_lb_min[0] = entry.dEta_lb_min
        mt2_bbmet[0] = entry.mt2_bbmet
        mt2_ZHmet[0] = entry.mt2_ZHmet

        eqLumi = entry.xsec/entry.countWeighted
        if massPoint > 450:
            output = reader_highMass.EvaluateMVA(methodName)
        else:
            output = reader_lowMass.EvaluateMVA(methodName)
        histos['bdt_response'].Fill(output)
        
        if output > bdtCut:
            histos['hhMt_long'].Fill(entry.hhmt, eqLumi)
    
        if 'Signal' in name:
            if (ievt%200)==0 : print 'For tree ', dictOfFiles[sample], ' event ', ievt,' has hhmt = ',entry.hhmt,' and MVA output = ', output
        else:
            if (ievt%10000)==0 : print 'For tree ', dictOfFiles[sample], ' event ', ievt,' has hhmt = ',entry.hhmt,' and MVA output = ', output
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

