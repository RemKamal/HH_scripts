#!/usr/bin/env python                                                                                                               

# #lines below are necessary for the use of Theano (CPU or GPU), otherwise TensorFlow on GPU will be a backend                      
# from os import environ                                                                                                            
# environ['KERAS_BACKEND'] = 'theano'                                                                                               
# # Set architecture of system (AVX instruction set is not supported on SWAN)                                                       
# environ['THEANO_FLAGS'] = 'gcc.cxxflags=-march=corei7'                                                                            
# import os                                                                                                                         
# os.environ['THEANO_FLAGS'] = "device=gpu0" #try other number like 1                                                               
# os.environ['THEANO_FLAGS'] = "floatX='float32'"                                                                                   
# import theano    

import ROOT
from ROOT import TMVA, gROOT, gApplication
from time import gmtime, strftime, localtime
import os, sys
import time
import pprint
doLD = True
doMultiClass = False
runOnGpuMachine = False

nBDTTrees = 800 #for fast debug
useKeras = True if runOnGpuMachine else False
bazingaPrinting = True
bookDNN = False
doDGtransform = False #decorrelation and gaussian transformation
useDataInsteadOfSignal = False

particleType = "Radion" if "Radion" in os.getcwd() else "BulkGraviton" 

doSR = False
doCRDY = False
doCRTT = False
doAllRegions = True

if doCRTT or doCRDY:
    useDataInsteadOfSignal = True
if doAllRegions or doSR:
    useDataInsteadOfSignal = False

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


class WritableObject:
    def __init__(self):
        self.content = []
    def write(self, string):
        self.content.append(string)


#print 'len(sys.argv) is ', len(sys.argv) 
#print 'sys.argv[0] is ', sys.argv[0] # script name
#print 'sys.argv[1] is ', sys.argv[1] # 1st additional parameter passed - list of mass points
#print 'sys.argv[2] is ', sys.argv[2] # 2nd additional parameter passed - nothing


args_are_given = len(sys.argv) > 1
if args_are_given:
    list_of_mass_points = list() if len(sys.argv) < 2 else [int(x) for x in sys.argv[1].split(',')]
    if list_of_mass_points:
        print 'list_of_mass_points is ', list_of_mass_points
    else:
        print 'please use syntax w/o spaces for comma separated list of masses: python train..py mass1,mass2,massN'
        sys.exit(1)
else:
    print 'args are not given, please use syntax w/o spaces for comma separated list of masses: python train..py mass1,mass2,massN'
    sys.exit(1)


if useKeras:
    from keras.models import Sequential
    from keras.layers.core import Dense
    #from keras.layers.core import  Activation
    from keras.regularizers import l2
    from keras import initializers
#from keras import initializations                                                                                                  
    from keras.optimizers import SGD


def bazinga(mes):
    if bazingaPrinting:
        print '-'*50
        print mes
        print '-'*50


start_time = time.time()
print 'start_time is', start_time
sigInputFile_250 = ROOT.TFile("GluGluTo{0}ToHHTo2B2ZTo2L2Nu_M-250_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root".format(particleType))
sigInputFile_260 = ROOT.TFile("GluGluTo{0}ToHHTo2B2ZTo2L2Nu_M-260_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root".format(particleType))
sigInputFile_270 = ROOT.TFile("GluGluTo{0}ToHHTo2B2ZTo2L2Nu_M-270_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root".format(particleType))
sigInputFile_300 = ROOT.TFile("GluGluTo{0}ToHHTo2B2ZTo2L2Nu_M-300_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root".format(particleType))
sigInputFile_350 = ROOT.TFile("GluGluTo{0}ToHHTo2B2ZTo2L2Nu_M-350_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root".format(particleType))
sigInputFile_400 = ROOT.TFile("GluGluTo{0}ToHHTo2B2ZTo2L2Nu_M-400_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root".format(particleType))
sigInputFile_450 = ROOT.TFile("GluGluTo{0}ToHHTo2B2ZTo2L2Nu_M-450_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root".format(particleType))
sigInputFile_500 = ROOT.TFile("GluGluTo{0}ToHHTo2B2ZTo2L2Nu_M-500_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root".format(particleType))
sigInputFile_550 = ROOT.TFile("GluGluTo{0}ToHHTo2B2ZTo2L2Nu_M-550_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root".format(particleType))
sigInputFile_600 = ROOT.TFile("GluGluTo{0}ToHHTo2B2ZTo2L2Nu_M-600_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root".format(particleType))
sigInputFile_650 = ROOT.TFile("GluGluTo{0}ToHHTo2B2ZTo2L2Nu_M-650_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root".format(particleType))
sigInputFile_700 = ROOT.TFile("GluGluTo{0}ToHHTo2B2ZTo2L2Nu_M-700_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root".format(particleType))
sigInputFile_750 = ROOT.TFile("GluGluTo{0}ToHHTo2B2ZTo2L2Nu_M-750_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root".format(particleType))
sigInputFile_800 = ROOT.TFile("GluGluTo{0}ToHHTo2B2ZTo2L2Nu_M-800_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root".format(particleType))
sigInputFile_900 = ROOT.TFile("GluGluTo{0}ToHHTo2B2ZTo2L2Nu_M-900_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root".format(particleType))
sigInputFile_1000 = ROOT.TFile("GluGluTo{0}ToHHTo2B2ZTo2L2Nu_M-1000_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v{1}_minitree.root".format(particleType, 2 if "Bulk" in particleType else 1))

bgInputFile_TT = ROOT.TFile("TT_TuneCUETP8M2T4_13TeV-powheg-Py8__RunIISummer16MAv2-PUMoriond17_backup_80r2as_2016_TrancheIV_v6-v1_minitree.root")
bgInputFile_DY_1j = ROOT.TFile("DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root")
bgInputFile_DY_2j = ROOT.TFile("DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root")
bgInputFile_DY_3j = ROOT.TFile("DY3JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root")
bgInputFile_DY_4j = ROOT.TFile("DY4JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root")

dataInputFile_0 = None
dataInputFile_1 = None
dataInputFile_2 = None
dataInputFile_3 = None
dataInputFile_4 = None
dataInputFile_5 = None
dataInputFile_6 = None
dataInputFile_7 = None
dataInputFile_8 = None

if muonRun:
    dataInputFile_Bv1 = ROOT.TFile("DoubleMuon__Run2016B-03Feb2017_ver1-v1_minitree.root")
    dataInputFile_Bv2 = ROOT.TFile("DoubleMuon__Run2016B-03Feb2017_ver2-v2_minitree.root")
    dataInputFile_C = ROOT.TFile("DoubleMuon__Run2016C-03Feb2017-v1_minitree.root")
    dataInputFile_D = ROOT.TFile("DoubleMuon__Run2016D-03Feb2017-v1_minitree.root")
    dataInputFile_E = ROOT.TFile("DoubleMuon__Run2016E-03Feb2017-v1_minitree.root")
    dataInputFile_F = ROOT.TFile("DoubleMuon__Run2016F-03Feb2017-v1_minitree.root")
    dataInputFile_G = ROOT.TFile("DoubleMuon__Run2016G-03Feb2017-v1_minitree.root")
    dataInputFile_Hv2 = ROOT.TFile("DoubleMuon__Run2016H-03Feb2017_ver2-v1_minitree.root")
    dataInputFile_Hv3 = ROOT.TFile("DoubleMuon__Run2016H-03Feb2017_ver3-v1_minitree.root")

if eleRun:
    dataInputFile_Bv1 = ROOT.TFile("DoubleEG__Run2016B-03Feb2017_ver1-v1_minitree.root")
    dataInputFile_Bv2 = ROOT.TFile("DoubleEG__Run2016B-03Feb2017_ver2-v2_minitree.root")
    dataInputFile_C = ROOT.TFile("DoubleEG__Run2016C-03Feb2017-v1_minitree.root")
    dataInputFile_D = ROOT.TFile("DoubleEG__Run2016D-03Feb2017-v1_minitree.root")
    dataInputFile_E = ROOT.TFile("DoubleEG__Run2016E-03Feb2017-v1_minitree.root")
    dataInputFile_F = ROOT.TFile("DoubleEG__Run2016F-03Feb2017-v1_minitree.root")
    dataInputFile_G = ROOT.TFile("DoubleEG__Run2016G-03Feb2017-v1_minitree.root")
    dataInputFile_Hv2 = ROOT.TFile("DoubleEG__Run2016H-03Feb2017_ver2-v1_minitree.root")
    dataInputFile_Hv3 = ROOT.TFile("DoubleEG__Run2016H-03Feb2017_ver3-v1_minitree.root")


bazinga('Finished initializing input samples.')

dictOfFiles = {}

dict_TT = {
    bgInputFile_TT: 'TT'
}

dict_DY = {
    bgInputFile_DY_1j: 'DY_1j',
    bgInputFile_DY_2j: 'DY_2j',
    bgInputFile_DY_3j: 'DY_3j',
    bgInputFile_DY_4j: 'DY_4j'
}

dict_signal = {
    sigInputFile_250 : 'Signal_250',
    sigInputFile_260 : 'Signal_260',
    sigInputFile_270 : 'Signal_270',
    sigInputFile_300 : 'Signal_300',
    sigInputFile_350 : 'Signal_350',
    sigInputFile_400 : 'Signal_400',
    sigInputFile_450 : 'Signal_450',
    sigInputFile_500 : 'Signal_500',
    sigInputFile_550 : 'Signal_550',
    sigInputFile_600 : 'Signal_600',
    sigInputFile_650 : 'Signal_650',
    sigInputFile_700 : 'Signal_700',
    sigInputFile_750 : 'Signal_750',
    sigInputFile_800 : 'Signal_800',
    sigInputFile_900 : 'Signal_900',
    sigInputFile_1000 : 'Signal_1000'

}

dict_data = {
#    dataInputFile_Bv1 : 'Data_{0}_Bv1'.format('eles' if eleRun else 'muons'),
    dataInputFile_Bv2 : 'Data_{0}_Bv2'.format('eles' if eleRun else 'muons'),
    dataInputFile_C : 'Data_{0}_C'.format('eles' if eleRun else 'muons'),
    dataInputFile_D : 'Data_{0}_D'.format('eles' if eleRun else 'muons'),
    dataInputFile_E : 'Data_{0}_E'.format('eles' if eleRun else 'muons'),
    dataInputFile_F : 'Data_{0}_F'.format('eles' if eleRun else 'muons'),
    dataInputFile_G : 'Data_{0}_G'.format('eles' if eleRun else 'muons'),
    dataInputFile_Hv2 : 'Data_{0}_Hv2'.format('eles' if eleRun else 'muons'),
    dataInputFile_Hv3 : 'Data_{0}_Hv3'.format('eles' if eleRun else 'muons')

}

if useDataInsteadOfSignal:
    dictOfFiles.update(dict_data)
else:
    dictOfFiles.update(dict_signal)

if doAllRegions or doSR:
    dictOfFiles.update(dict_TT)
    dictOfFiles.update(dict_DY)
elif doCRDY and not doAllRegions:
     dictOfFiles.update(dict_DY)
elif doCRTT and not doAllRegions:
     dictOfFiles.update(dict_TT)
else:
    print 'cannot happen with dictionaries, exiting...'
    sys.exit(1)

print
print 'dictOfFiles = '
pprint.pprint( dictOfFiles)

TMVA.Tools.Instance();

date = strftime("%Y%b%d_%H-%M", localtime() )#gmtime()) 
print
print 'date is', date
fileName = None
if useKeras:
    
    if doMultiClass:
        outputFile_multiClass_keras = ROOT.TFile("TMVAOutput_" + str(list_of_mass_points[0]) + '_' + str(list_of_mass_points[-1]) + "_multiClass_keras_" + date + "{0}.root".format('_DG' if doDGtransform else ''), "RECREATE")
        factory = TMVA.Factory('TMVAMulticlass_' + str(list_of_mass_points[0]) + '_'  + str(list_of_mass_points[-1]) + '_keras', outputFile_multiClass_keras,
                               '!V:!Silent:Color:DrawProgressBar:Transformations=I,{0}:AnalysisType=multiclass'.format("D,G" if doDGtransform else ''))
        fileName = outputFile_multiClass_keras
    else:
        outputFile_biClass_keras = ROOT.TFile("TMVAOutput_" + str(list_of_mass_points[0]) + '_' + str(list_of_mass_points[-1]) + "_biClass_keras_" + date + "{0}.root".format('_DG' if doDGtransform else ''), "RECREATE")
        factory = TMVA.Factory("TMVAClassification_" + str(list_of_mass_points[0]) + '_' + str(list_of_mass_points[-1]) + "_keras", outputFile_biClass_keras,
                               'V:!Silent:Color:DrawProgressBar:Transformations=I,{0}:AnalysisType=Classification'.format("D,G" if doDGtransform else ''))
        fileName = outputFile_biClass_keras
else:

    if doMultiClass:
        outputFile_multiClass = ROOT.TFile("TMVAOutput_" + str(list_of_mass_points[0]) + '_' + str(list_of_mass_points[-1]) + "_multiClass_" + date + "{0}.root".format('_DG' if doDGtransform else ''), "RECREATE")
        factory = TMVA.Factory('TMVAMulticlass_' + str(list_of_mass_points[0]) + '_' + str(list_of_mass_points[-1]), outputFile_multiClass,
                               '!V:!Silent:Color:DrawProgressBar:Transformations=I,{0}:AnalysisType=multiclass'.format("D,G" if doDGtransform else ''))
        fileName = outputFile_multiClass
    else:
        outputFile_biClass = ROOT.TFile("TMVAOutput_" + str(list_of_mass_points[0]) + '_' + str(list_of_mass_points[-1]) + "_biClass_" + date + "{0}.root".format('_DG' if doDGtransform else ''), "RECREATE")
        factory = TMVA.Factory("TMVAClassification" + str(list_of_mass_points[0]) + '_' + str(list_of_mass_points[-1]), outputFile_biClass,
                               'V:!Silent:Color:DrawProgressBar:Transformations=I,{0}:AnalysisType=Classification'.format("D,G" if doDGtransform else ''))
        fileName = outputFile_biClass

loader = ROOT.TMVA.DataLoader("dataset");
if fileName:
    print 'fileName is ', fileName
else:
    sys.exit(1)
#add variables  


#loader.AddVariable("bpt0")
loader.AddVariable("zmass")
loader.AddVariable("met_pt")
#loader.AddVariable("lepeta0")
#1


loader.AddVariable("hmass0")
#loader.AddVariable("heta0")
#loader.AddVariable("hphi1")
loader.AddVariable("hmass1")
#loader.AddVariable("hToZZ_mt_cosine")
#loader.AddVariable("hmt0")
#10

loader.AddVariable("dR_leps")
#loader.AddVariable("hhmt")
#loader.AddVariable("dPhi_bjets")
#loader.AddVariable("zhphi")
loader.AddVariable("dR_bjets")
#3


#loader.AddVariable("beta0")
#loader.AddVariable("bphi0")
#loader.AddVariable("bpt1")
#loader.AddVariable("beta1")
#loader.AddVariable("bphi1")
#20
#loader.AddVariable("btagDiscr0")
#loader.AddVariable("btagDiscr1")
#loader.AddVariable("leppt0")
#loader.AddVariable("lepphi0")
#loader.AddVariable("leppt1")
#5
#loader.AddVariable("lepeta1")
#loader.AddVariable("lepphi1")
#loader.AddVariable("meteta")  #const var
#loader.AddVariable("met_phi")
loader.AddVariable("zpt0")
#loader.AddVariable("zeta0")
#30

#loader.AddVariable("zphi0")
#HtoZZ
loader.AddVariable("hpt0")
#loader.AddVariable("hphi0")
#Htobb
#loader.AddVariable("hmt1")
loader.AddVariable("hpt1")
#7

#loader.AddVariable("heta1")
#loader.AddVariable("nbjets")
#loader.AddVariable("njets")  
#loader.AddVariable("nloosebjets") #const ahaha
#loader.AddVariable("nleps") #const var
#loader.AddVariable("dEta_lb_min")
#9

#loader.AddVariable("dEta_ZH")
#loader.AddVariable("dEta_bjets")
#loader.AddVariable("dEta_leps")
#loader.AddVariable("dR_lb_min")
#loader.AddVariable("dR_ZH")
#45

#loader.AddVariable("dPhi_lb_min")
#loader.AddVariable("dPhi_ZH")
#loader.AddVariable("dPhi_leps")
#loader.AddVariable("hh_mt_cosine")
#loader.AddVariable("zhmass")
#50
#loader.AddVariable("zhpt")
#loader.AddVariable("zheta")
#loader.AddVariable("mt2_llmet")
#loader.AddVariable("mt2_bbmet")
#loader.AddVariable("mt2_b1l1b2l2met")
#55
#loader.AddVariable("mt2_b1l2b2l1met")
#loader.AddVariable("min_mt2_blmet")
#loader.AddVariable("mt2_ZHmet")
#11




# loader.AddVariable("bpt0")
# loader.AddVariable("zmass")
# loader.AddVariable("metpt")
# loader.AddVariable("lepeta0")
# #4


# loader.AddVariable("hmass0")
# loader.AddVariable("heta0")
# loader.AddVariable("hphi1")
# loader.AddVariable("hmass1")
# loader.AddVariable("hToZZ_mt_cosine")
# loader.AddVariable("hmt0")
# #10

# loader.AddVariable("dR_leps")
# loader.AddVariable("hhmt")
# loader.AddVariable("dPhi_bjets")
# loader.AddVariable("zhphi")
# loader.AddVariable("dR_bjets")
# #15


# loader.AddVariable("beta0")
# loader.AddVariable("bphi0")
# loader.AddVariable("bpt1")
# loader.AddVariable("beta1")
# loader.AddVariable("bphi1")
# #20
# loader.AddVariable("btag0")
# loader.AddVariable("btag1")
# loader.AddVariable("leppt0")
# loader.AddVariable("lepphi0")
# loader.AddVariable("leppt1")
# #25
# loader.AddVariable("lepeta1")
# loader.AddVariable("lepphi1")
# #loader.AddVariable("meteta")  #const var
# loader.AddVariable("metphi")
# loader.AddVariable("zpt0")
# loader.AddVariable("zeta0")
# #30

# loader.AddVariable("zphi0")
# #HtoZZ
# loader.AddVariable("hpt0")
# loader.AddVariable("hphi0")
# #Htobb
# loader.AddVariable("hmt1")
# loader.AddVariable("hpt1")
# #35

# loader.AddVariable("heta1")
# loader.AddVariable("nbjets")
# loader.AddVariable("njets")  
# loader.AddVariable("nloosebjets")
# #loader.AddVariable("nleps") #const var
# loader.AddVariable("dEta_lb_min")
# #40

# loader.AddVariable("dEta_ZH")
# loader.AddVariable("dEta_bjets")
# loader.AddVariable("dEta_leps")
# loader.AddVariable("dR_lb_min")
# loader.AddVariable("dR_ZH")
# #45

# loader.AddVariable("dPhi_lb_min")
# loader.AddVariable("dPhi_ZH")
# loader.AddVariable("dPhi_leps")
# loader.AddVariable("hh_mt_cosine")
# loader.AddVariable("zhmass")
# #50
# loader.AddVariable("zhpt")
# loader.AddVariable("zheta")
# loader.AddVariable("mt2_llmet")
# loader.AddVariable("mt2_bbmet")
# loader.AddVariable("mt2_b1l1b2l2met")
# #55
# loader.AddVariable("mt2_b1l2b2l1met")
# loader.AddVariable("min_mt2_blmet")
# loader.AddVariable("mt2_ZHmet")
# #58




#loader.AddSpectator("evWgt")
#loader.AddSpectator("countWeighted")
#loader.AddSpectator("xsec")
#loader.AddSpectator("genvbosonpdgid")

bazinga('Finished loading vars')

ROOT.TMVA.gConfig().SetDrawProgressBar(True)

# doAllRegions = True
# doSR = False
# doCRDY = False
# doCRTT = False

mycuts = ROOT.TCut()
if doAllRegions:
    mycuts = ROOT.TCut("(zmass > 76) && (hmass1 > 20)")
elif not doAllRegions and doSR:
    mycuts = ROOT.TCut("(zmass > 76) && (zmass < 106) && (hmass1 > 90) && (hmass1 < 150)")
elif not doAllRegions and doCRDY:
    mycuts = ROOT.TCut("(zmass > 76) && (zmass < 106) && (((hmass1 > 20) && (hmass1 < 90)) || (hmass1 > 150))")
elif not doAllRegions and doCRTT:
    mycuts = ROOT.TCut("(zmass > 106) && (hmass1 > 90) && (hmass1 < 150)")
else:
    print 'cannot happen in working with cuts, exiting...'
    sys.exit(1)



mycutb = ROOT.TCut()
mycutb = mycuts
print
print 'for doAllRegions={0}, doCRDY={1}, doCRTT={2}, doSR={3}, useDataInsteadOfSignal = {4}, eleRun={5}, muonRun={6}'.format(doAllRegions, doCRDY, doCRTT, doSR,useDataInsteadOfSignal, eleRun, muonRun)
print 'used signal cuts:'
print mycuts.GetTitle()
print 'used bg cuts:'
print mycutb.GetTitle()
createROCpng_n_root = False

seenFiles = list()
count = 0
if doMultiClass:
    for m in list_of_mass_points:
        for sample, name in dictOfFiles.items():
            print 'seenFiles is ', seenFiles
            if name not in seenFiles:
                if str(m) in name:
                    bazinga('Loading {0} sample'.format(sample))
                    loader.AddTree(sample.tree, 'Signal', 1)
                    count +=1
                    seenFiles.append(name)
                else:
                    if 'DY' in name:
                        bazinga('Loading {0} sample'.format(sample))
                        loader.AddTree(sample.tree, 'DY')
                        loader.SetWeightExpression("xsec/countWeighted", 'DY') 
                        count +=1
                        seenFiles.append(name)
                    elif 'TT' in name:
                        bazinga('Loading {0} sample'.format(sample))
                        loader.AddTree(sample.tree, name)
                        loader.SetWeightExpression("xsec/countWeighted", name)
                        count +=1
                        seenFiles.append(name)
                    
                
else:
    if not useDataInsteadOfSignal:
        for m in list_of_mass_points:
            for sample, name in dictOfFiles.items():
                if str(m) in name:
                    print 'adding ', sample
                    loader.AddSignalTree    (sample.tree,    1)   #signal weight  = 1     
                    count +=1
    else:
        #in case of running with data instead of signal
        for samp, name in dict_data.items():
             print 'adding ', samp
             loader.AddSignalTree    (samp.tree,    1)   #signal weight  = 1                                             
             count +=1

    if doAllRegions or doSR:
        loader.AddBackgroundTree(bgInputFile_TT.tree, 1);   #background weight = 1 
        loader.AddBackgroundTree(bgInputFile_DY_1j.tree, 1)
        loader.AddBackgroundTree(bgInputFile_DY_2j.tree, 1)
        loader.AddBackgroundTree(bgInputFile_DY_3j.tree, 1)
        loader.AddBackgroundTree(bgInputFile_DY_4j.tree, 1)
        loader.SetBackgroundWeightExpression("xsec/countWeighted") 
        count +=5
    elif doCRDY and not doAllRegions:
        loader.AddBackgroundTree(bgInputFile_DY_1j.tree, 1)
        loader.AddBackgroundTree(bgInputFile_DY_2j.tree, 1)
        loader.AddBackgroundTree(bgInputFile_DY_3j.tree, 1)
        loader.AddBackgroundTree(bgInputFile_DY_4j.tree, 1)
        loader.SetBackgroundWeightExpression("xsec/countWeighted")
        count +=4
    elif doCRTT and not doAllRegions:
        loader.AddBackgroundTree(bgInputFile_TT.tree, 1);   #background weight = 1 
        loader.SetBackgroundWeightExpression("xsec/countWeighted")
        count +=1
    else:
        print 'cannot happen in working with cuts, exiting...'
        sys.exit(1)


            # elif 'DY' or 'TT' in name:
            #     loader.AddBackgroundTree(sample.tree, 1)
            #     loader.SetBackgroundWeightExpression("xsec/countWeighted")  
            #     count +=1
            # else:
            #     print 'smth is wrong, exiting...'
            #     sys.exit(1)


print 'loaded {0} trees'.format(count)
#dataLoader = loader.GetDataSetInfo()
#print dataLoader
# orig_stdout = sys.stdout
# #https://stackoverflow.com/questions/7152762/how-to-redirect-print-output-to-a-file-using-python

# # example with redirection of sys.stdout
# foo = WritableObject()                   # a writable object
# sys.stdout = foo  
# #https://stackoverflow.com/questions/2321939/assign-output-of-print-to-a-variable-in-python

# #print 'here are dataLoader.PrintClasses():'
# classes = dataLoader.PrintClasses()
# sys.stdout = orig_stdout

# #classes = foo.content
# print 'classes are:', classes





#for signal: 
#factory.SetSignalWeightExpression    ("evWgt")
#loader.SetSignalWeightExpression("xsec/countWeighted")

#for background: 
#factory.SetBackgroundWeightExpression("evWgt")
#loader.SetBackgroundWeightExpression("xsec/countWeighted")

#for both:
#loader.SetWeightExpression("xsec/countWeighted")                                                     

bazinga('Input contains {0} TTrees'.format(count))#len(dictOfFiles) if not doMultiClass else count))

loader.PrepareTrainingAndTestTree(#ROOT.TCut(),#SigCut=
                                  mycuts, mycutb,
                                  #nTrain_Signal=0, nTrain_Background=2000, nTest_Signal=10000, nTest_Background=10000, 
                                  'SplitMode=Random:NormMode=NumEvents:V=True') #False








# Define initialization                                                                                                             
def normal(shape, name=None):
    #return initializations.normal(shape, scale=0.05, name=name)                                                                    
    return initializers.normal(shape, scale=0.05, name=name)


nVars = (loader.GetDataSetInfo()).GetNVariables()
# print 'nVars=', nVars
# for cls in ['Signal', 'Background']:
#     (loader.GetDataSetInfo()).PrintCorrelationMatrix(cls)


#sys.exit(1)


if useKeras:
    # Define model                                                                                                                      
    model = Sequential()
    model.add(Dense(12, init="normal", activation='relu', W_regularizer=l2(1e-5), input_dim=nVars ))#len(variables)))
#model.add(Dense(2, init="normal", activation='softmax'))                                                                           
#model.add(Dense(1, init="normal", activation='softmax'))                                                                           
# can have any number of inner layers and parameters                                                                                
    
    numTrees = len(dictOfFiles) #nTrees if nTrees==4 else 4#????                                                                                               
    model.add(Dense(numTrees, init="normal", activation='softmax'))
    model.add(Dense(numTrees, init="normal", activation='softmax'))
    

# Set loss and optimizer                                                                                                            
    model.compile(loss='categorical_crossentropy', optimizer=SGD(lr=0.01), metrics=['accuracy',])
    
    # Store model to file                                                                                                               
    model.save('model_HH.h5')
    model.summary()



#works only in SWAN
bazinga('Before drawing few histograms.')
#loader.DrawInputVariable("hhmt")
#loader.DrawCorrelationMatrix("Signal") 


if not doMultiClass:
    if doLD:
        bazinga('Book LD method')
        factory.BookMethod( loader, TMVA.Types.kLD, "LD", "H:!V:VarTransform=None:CreateMVAPdfs:PDFInterpolMVAPdf=Spline2:NbinsMVAPdf=50:NsmoothMVAPdf=10" )
    else:
        pass

methodName = 'BDT' # it is BDTG actually. Use BDT to let TMVAGui work, but remember to rename weights after, to use for GUI plots
bazinga('Book {0} method'.format(methodName))
factory.BookMethod(loader,
                   TMVA.Types.kBDT,
                   methodName,
                   "!H:!V:NTrees={0}:BoostType=Grad:Shrinkage=0.1:UseBaggedBoost=True:GradBaggingFraction=0.5:SeparationType=GiniIndex:nCuts=30:MaxDepth=3".format(nBDTTrees))






DNNType = 'Standard'
#DNNType = 'CPU'   # use new implementation                                               
trainingStrategyFast = [{
        "LearningRate": 1e-1,
        "Momentum": 0.0,
        "Repetitions": 1,
        "ConvergenceSteps": 100,
        "BatchSize": 50,
        "TestRepetitions": 7,
        "WeightDecay": 0.001,
        "Regularization": "NONE",
        "DropConfig": "0.0+0.5+0.5+0.5",
        "DropRepetitions": 1,
        "Multithreading": True
        
        }]

trainingStrategy = [{
        "LearningRate": 1e-1,
        "Momentum": 0.0,
        "Repetitions": 1,
        "ConvergenceSteps": 100,
        "BatchSize": 50,
        "TestRepetitions": 4,
        "WeightDecay": 0.001,
        "Regularization": "NONE",
        "DropConfig": "0.0+0.5+0.5+0.5",
        "DropRepetitions": 1,
        "Multithreading": True
        
        },  {
        "LearningRate": 1e-2,
        "Momentum": 0.5,
        "Repetitions": 1,
        "ConvergenceSteps": 100,
        "BatchSize": 50,
        "TestRepetitions": 2,
        "WeightDecay": 0.001,
        "Regularization": "TRUE",
        "DropConfig": "0.0+0.1+0.1+0.1",
        "DropRepetitions": 1,
        "Multithreading": True
        
        }, {
        "LearningRate": 1e-3,
        "Momentum": 0.3,
        "Repetitions": 1,
        "ConvergenceSteps": 100,
        "BatchSize": 50,
        "TestRepetitions": 2,
        "WeightDecay": 0.001,
        "Regularization": "NONE",
        "Multithreading": True
    
        
        }]


if bookDNN :
    print 'Booking DNN method.'
    #when more signal sample is available, the method below would be preferrable, or more layers in BDT (MaxDepth) can be used
    factory.BookMethod(DataLoader=loader, Method=TMVA.Types.kDNN, MethodTitle="DNN",
                       H = False, V=False, VarTransform="Normalize", ErrorStrategy="CROSSENTROPY",
                       Layout=["TANH|50", "TANH|50", "TANH|10", "LINEAR"],
                       TrainingStrategy=trainingStrategy,Architecture=DNNType)
    


bazinga('Let the training begin!(c)')
factory.TrainAllMethods()

bazinga('Test all methods')
factory.TestAllMethods()

bazinga('Evaluate all methods')
factory.EvaluateAllMethods()

bazinga('Draw some output distributions')
#factory.DrawOutputDistribution(loader.GetName(), "LD")                                   
#factory.DrawOutputDistribution(loader.GetName(), methodName)
if bookDNN:
    bazinga('DNN was trained too.')

#factory.DrawOutputDistribution(loader.GetName(), "DNN")                   

if not doMultiClass:
    
    # Double_t GetROCIntegral(DataLoader *loader,TString theMethodName);
    #  Double_t GetROCIntegral(TString  datasetname,TString theMethodName);
    
    #  // Methods to get a TGraph for an indicated method in dataset.
    #  // Optional title and axis added with fLegend=kTRUE.
    #  // Argument iClass used in multiclass settings, otherwise ignored.
    #  TGraph* GetROCCurve(DataLoader *loader, TString theMethodName, Bool_t setTitles=kTRUE, UInt_t iClass=0);
    #  TGraph* GetROCCurve(TString datasetname, TString theMethodName, Bool_t setTitles=kTRUE, UInt_t iClass=0);

    #  // Methods to get a TMultiGraph for a given class and all methods in dataset.
    #  TMultiGraph* GetROCCurveAsMultiGraph(DataLoader *loader, UInt_t iClass);
    #  TMultiGraph* GetROCCurveAsMultiGraph(TString datasetname, UInt_t iClass);
    
    #  // Draw all ROC curves of a given class for all methods in the dataset.
    #  TCanvas* GetROCCurve(DataLoader *loader, UInt_t iClass=0);
    #  TCanvas* GetROCCurve(TString datasetname, UInt_t iClass=0);


    if not doMultiClass:
        if doLD:
            print 'ROC integral for LD = ',factory.GetROCIntegral(loader, 'LD')
    print 'ROC integral for BDT = ',factory.GetROCIntegral(loader, methodName)
    if bookDNN: 
        print 'ROC integral for DNN = ',factory.GetROCIntegral(loader, 'DNN')
else:
    #tgr = factory.GetROCCurve(loader)#, methodName) 
    pass
    #print 'ROC integral for BDT = ', tgr.Integral()


if not doMultiClass:
    roc = factory.GetROCCurve(loader)
    if createROCpng_n_root:
        bazinga('Saving ROC')
        roc.SaveAs('ROC_' + str(list_of_mass_points[-1]) + '_' + date + '{0}.root'.format("_DG" if doDGtransform else ''))
        roc.SaveAs('ROC_' + str(list_of_mass_points[-1]) + '_' + date + '{0}.png'.format("_DG" if doDGtransform else ''))
    roc.Draw()

bazinga('Closing "{0}".'.format(fileName))

fileName.Close()

# if doMultiClass and useKeras:
#     outputFile_multiClass_keras.Close()
# elif doMultiClass and not useKeras:
#     outputFile_multiClass.Close()
# elif not doMultiClass and useKeras:
#     outputFile_biClass_keras.Close()
# else:
#     outputFile_biClass.Close()


for sample, name in dictOfFiles.items():
    sample.Close()
    


end_time = time.time()
print 'end_time is', end_time
time_taken = end_time - start_time # time_taken is in seconds                                                      
print 'time_taken is', time_taken

hours, rest = divmod(time_taken,3600)
minutes, seconds = divmod(rest, 60)
bazinga( "---it took {hours} hours, {minutes} minutes and {seconds:.1f} seconds to run the analysis ---".format (hours=hours, minutes=minutes, seconds=seconds) )



# # ROOT.gInterpreter.Declare("""
# # void LaunchMultiGUI(){
# # TMVA::TMVAMultiClassGui("TMVA.root");
# # }
# # """)

# # ROOT.gInterpreter.Declare("""                                                                                                                                      void LaunchClasGUI(){
# # TMVA::TMVAGui("TMVA.root");
# # }
# # """)

# # ROOT.gInterpreter.Declare("""                                                                                                                                      void LaunchRegGUI(){
# # TMVA::TMVARegGui("TMVA.root");
# # }
# # """)




# comment-out since new 'gui' script is preferrable
#tmvaFileToOpen = (outputFile_multiClass if doMultiClass else outputFile_biClass).GetName()
# if os.path.isfile(tmvaFileToOpen):
#     print 'File exists'
#     if os.path.getsize(tmvaFileToOpen) > 0:
#         print 'File has non-zero size'
#         if (outputFile_multiClass if doMultiClass else outputFile_biClass).IsZombie():
#             print 'File is ZOMBIE'
#             sys.exit(1)
#         else:
#             bazinga('doMultiClass = {0}, runOnGpuMachine = {1}'.format(doMultiClass, runOnGpuMachine))
#             if runOnGpuMachine:
#                 print ('Do nothing, GPU seems not to like the GUI')
#             else:
#                 exit(1)
#                 if doMultiClass:
#                     bazinga ('Opening created output file for multiclass.')
#                     TMVA.TMVAMultiClassGui(tmvaFileToOpen)
#                     raw_input('Press Enter to exit')
#                 else:
#                     TMVA.TMVAGui(tmvaFileToOpen)
#                     raw_input('Press Enter to exit')
                




#lines below are not working, are taken from SWAN
# bazinga (outputFile_multiClass if doMultiClass else outputFile_biClass)
# # open the GUI for the result macros    
# print ( "TMVAGui(\"%s\")" % "TMVAOutput_biClass_2017May08_10-24.root" )
# gROOT.ProcessLine( "TMVA.TMVAGui(\"%s\")" % "TMVAOutput_biClass_2017May08_10-24.root" )
# # keep the ROOT thread running
# gApplication.Run() 
