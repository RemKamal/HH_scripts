from rootpy.io import root_open
debugMode = True # for priting with bazinga                                                       
import time 

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

    if len(sys.argv) > 5:
        massRegion = sys.argv[5]
        if massRegion in {'low', 'high'}:
            print 'massRegion is ', massRegion
            pass
        else:
            print 'wrong mass region, pease use "low or high", exiting.'
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


sigInputFile_260 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M260_Hzz_minitree.root")
sigInputFile_270 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M270_Hzz_minitree.root")
sigInputFile_300 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M300_Hzz_minitree.root")
sigInputFile_350 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M350_Hzz_minitree.root")
sigInputFile_400 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M400_Hzz_minitree.root")
sigInputFile_450 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M450_Hzz_minitree.root")
sigInputFile_600 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M600_Hzz_minitree.root")
sigInputFile_650 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M650_Hzz_minitree.root")
sigInputFile_900 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M900_Hzz_minitree.root")
sigInputFile_1000 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M1000_Hzz_minitree.root")


wwSigInputFile_260 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M260_Hww_minitree.root")
wwSigInputFile_270 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M270_Hww_minitree.root")
wwSigInputFile_300 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M300_Hww_minitree.root")
wwSigInputFile_350 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M350_Hww_minitree.root")
wwSigInputFile_400 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M400_Hww_minitree.root")
wwSigInputFile_450 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M450_Hww_minitree.root")
wwSigInputFile_600 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M600_Hww_minitree.root")
wwSigInputFile_650 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M650_Hww_minitree.root")
wwSigInputFile_900 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M900_Hww_minitree.root")
wwSigInputFile_1000 = ROOT.TFile(dirWithMCSamples + "BulkGraviton_M1000_Hww_minitree.root")


bgInputFile_TT = ROOT.TFile(dirWithMCSamples + "TT_Tune_minitree.root")
bgInputFile_DY_1j = ROOT.TFile(dirWithMCSamples + "DY1JetsToLL_M50_minitree.root")
bgInputFile_DY_2j = ROOT.TFile(dirWithMCSamples + "DY2JetsToLL_M50_minitree.root")
bgInputFile_DY_3j = ROOT.TFile(dirWithMCSamples + "DY3JetsToLL_M50_minitree.root")
bgInputFile_DY_4j = ROOT.TFile(dirWithMCSamples + "DY4JetsToLL_M50_minitree.root")


bgInputFile_ST_t_antitop_inclusive_powheg = ROOT.TFile(dirWithMCSamples + "ST_t_antitop_inclusive_powheg_minitree.root")
bgInputFile_ST_tW_top_5f_inclusive = ROOT.TFile(dirWithMCSamples + "ST_tW_top_5f_inclusive_minitree.root")
bgInputFile_ST_tW_antitop_5f_NFHDecay = ROOT.TFile(dirWithMCSamples + "ST_tW_antitop_5f_NFHDecay_minitree.root")
bgInputFile_ST_s_channel_4f = ROOT.TFile(dirWithMCSamples + "ST_s-channel_4f_minitree.root")
bgInputFile_ST_tW_antitop_5f_inclusive = ROOT.TFile(dirWithMCSamples + "ST_tW_antitop_5f_inclusive_minitree.root")
bgInputFile_ST_tW_top_5f_NFHDecay = ROOT.TFile(dirWithMCSamples + "ST_tW_top_5f_NFHDecay_minitree.root")
bgInputFile_ST_t_top_inclusive_powheg = ROOT.TFile(dirWithMCSamples + "ST_t_top_inclusive_powheg_minitree.root")

bgInputFile_ZZ_Tune = ROOT.TFile(dirWithMCSamples + "ZZ_Tune_minitree.root")
bgInputFile_WZ_Tune = ROOT.TFile(dirWithMCSamples + "WZ_Tune_minitree.root")
bgInputFile_WW_Tune = ROOT.TFile(dirWithMCSamples + "WW_Tune_minitree.root")
bgInputFile_ZH_powheg = ROOT.TFile(dirWithMCSamples + "ZH_powheg_minitree.root")

muon2016dataInputFile = ROOT.TFile(dirWithMCSamples + "muon2016data_minitree.root")



dictOfFiles = {
    sigInputFile_260:'BulkGraviton_M260_Hzz',
    sigInputFile_270:'BulkGraviton_M270_Hzz',
    sigInputFile_300:'BulkGraviton_M300_Hzz',
    sigInputFile_350:'BulkGraviton_M350_Hzz',
    sigInputFile_400:'BulkGraviton_M400_Hzz',
    sigInputFile_450:'BulkGraviton_M450_Hzz',
    sigInputFile_600:'BulkGraviton_M600_Hzz',
    sigInputFile_650:'BulkGraviton_M650_Hzz',
    sigInputFile_900:'BulkGraviton_M900_Hzz',
    sigInputFile_1000:'BulkGraviton_M1000_Hzz',
   
    
    wwSigInputFile_260:'BulkGraviton_M260_Hww',
    wwSigInputFile_270:'BulkGraviton_M270_Hww',
    wwSigInputFile_300:'BulkGraviton_M300_Hww',
    wwSigInputFile_350:'BulkGraviton_M350_Hww',
    wwSigInputFile_400:'BulkGraviton_M400_Hww',
    wwSigInputFile_450:'BulkGraviton_M450_Hww',
    wwSigInputFile_600:'BulkGraviton_M600_Hww',
    wwSigInputFile_650:'BulkGraviton_M650_Hww',
    wwSigInputFile_900:'BulkGraviton_M900_Hww',
    wwSigInputFile_1000:'BulkGraviton_M1000_Hww',
   
    bgInputFile_TT: 'TT_Tune',
    bgInputFile_DY_1j: 'DY1JetsToLL_M50',
    bgInputFile_DY_2j: 'DY2JetsToLL_M50',
    bgInputFile_DY_3j: 'DY3JetsToLL_M50',
    bgInputFile_DY_4j: 'DY4JetsToLL_M50',

    bgInputFile_ST_s_channel_4f: 'ST_s-channel_4f',
    bgInputFile_ST_t_top_inclusive_powheg: 'ST_t_top_inclusive_powheg',
    bgInputFile_ST_t_antitop_inclusive_powheg: 'ST_t_antitop_inclusive_powheg',
    bgInputFile_ST_tW_top_5f_inclusive: 'ST_tW_top_5f_inclusive',
    bgInputFile_ST_tW_antitop_5f_inclusive: 'ST_tW_antitop_5f_inclusive',
    bgInputFile_ST_tW_top_5f_NFHDecay: 'ST_tW_top_5f_NFHDecay',
    bgInputFile_ST_tW_antitop_5f_NFHDecay: 'ST_tW_antitop_5f_NFHDecay',

    bgInputFile_ZH_powheg: 'ZH_powheg',
    bgInputFile_ZZ_Tune: 'ZZ_Tune',
    bgInputFile_WW_Tune: 'WW_Tune',
    bgInputFile_WZ_Tune: 'WZ_Tune',

    muon2016dataInputFile: 'muon2016data',
    
}



print 'Doing massRegion ', massRegion

outDir = massRegion + '_' + physRegion  + '_' + str(bdtCut) + '/'

print 'outDir is ', outDir
if not os.path.exists(outDir):
    os.makedirs(outDir)


for sample, name in dictOfFiles.items():
    #if 'Signal' not in name: continue
    bazinga('processing {0}'.format(physRegion) )
    if 'Bulk' in name:
        print 'name is', name
        tmp = name[14:-4]
        print 'tmp is', tmp
        if not any(c.isalpha() for c in tmp):
            mass = int(tmp)
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
        if 'data' not in name:
            eqLumi = entry.xsec/entry.countWeighted
        else:
            eqLumi = 1
            #if massPoint > 450:
        output = reader.EvaluateMVA(methodName)
            #else:
             #   output = reader_lowMass.EvaluateMVA(methodName)
        histos['bdt_response'].Fill(output, eqLumi)
        
        if output > bdtCut:
            histos['hhMt_long'].Fill(min(entry.hhmt, centinel), eqLumi)
    
        if 'Bulk' in name:
            if (ievt%200)==0 : print 'For tree ', dictOfFiles[sample], ' event ', ievt,' has hhmt = ',entry.hhmt,' and MVA output = ', output, ' xsec is ', entry.xsec, ' nEvents is ', entry.countWeighted
        else:
            if (ievt%10000)==0 : print 'For tree ', dictOfFiles[sample], ' event ', ievt,' has hhmt = ',entry.hhmt,' and MVA output = ', output, ' xsec is ', entry.xsec, ' nEvents is ', entry.countWeighted
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

