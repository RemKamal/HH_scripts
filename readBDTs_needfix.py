import ROOT
from ROOT import TMVA
from time import gmtime, strftime
#print 'import histogrammar'
#from histogrammar import *
#import matplotlib.pyplot as plt
from collections import OrderedDict


doMultiClass = False
bazingaPrinting = True
bookDNN = False
doDGtransform = True #decorrelation and gaussian transformation

def bazinga(mes):
    if bazingaPrinting:
        print '-'*50
        print mes
        print '-'*50


sigInputFile = ROOT.TFile("BulkGraviton_M900_Hzz_minitree.root")
bgInputFile_TT = ROOT.TFile("TT_Tune_minitree.root")
bgInputFile_DY_1j = ROOT.TFile("DY1JetsToLL_M50_minitree.root")
bgInputFile_DY_2j = ROOT.TFile("DY2JetsToLL_M50_minitree.root")
bgInputFile_DY_3j = ROOT.TFile("DY3JetsToLL_M50_minitree.root")
bgInputFile_DY_4j = ROOT.TFile("DY4JetsToLL_M50_minitree.root")
bazinga('Finished initializing input samples.')

TMVA.Tools.Instance();
reader = TMVA.Reader( "!Color:!Silent" )

from array import array

#will replace lines below later, but variables itself will 'stay'
# BDT                      : Ranking result (top variable is best ranked)
#                          : -----------------------------------------------
#                          : Rank : Variable      : Variable Importance
#                          : -----------------------------------------------
#                          :    1 : hmt0          : 4.906e-01
#                          :    2 : zhmass        : 3.704e-01
#                          :    3 : hpt1          : 8.812e-02
#                          :    4 : min_mt2_blmet : 5.088e-02
#                          :    5 : hhmt          : 0.000e+00
#                          :    6 : dR_bjets      : 0.000e+00
#                          :    7 : zpt0          : 0.000e+00
#                          :    8 : hpt0          : 0.000e+00

#mydict = OrderedDict()


bpt0 = array('f',[0])
beta0 = array('f',[0])
bphi0 = array('f',[0])
bpt1 = array('f',[0])
beta1 = array('f',[0])

bphi1 = array('f',[0])
leppt0 = array('f',[0])
lepeta0 = array('f',[0])
lepphi0 = array('f',[0])
leppt1 = array('f',[0])

lepeta1 = array('f',[0])
lepphi1 = array('f',[0])
metpt = array('f',[0])
#meteta = tree.met_eta
metphi = array('f',[0])

btag0 = array('f',[0])
btag1 = array('f',[0])
zmass = array('f',[0])
zpt0 = array('f',[0])
zeta0 = array('f',[0])

zphi0 = array('f',[0])
hmass0 = array('f',[0])
hmt0 = array('f',[0])
hpt0 = array('f',[0])
heta0 = array('f',[0])

hphi0 = array('f',[0])
hToZZ_mt_cosine = array('f',[0])
hmass1 = array('f',[0])
hmt1 = array('f',[0])
hpt1 = array('f',[0])

heta1 = array('f',[0])
hphi1 = array('f',[0])
nbjets = array('i',[0])
njets = array('i',[0])
nloosebjets = array('i',[0])

#nleps = nLeps
dEta_lb_min = array('f',[0])
dEta_ZH = array('f',[0])
dEta_bjets = array('f',[0])
dEta_leps = array('f',[0])

dR_lb_min = array('f',[0])
dR_ZH = array('f',[0])
dR_bjets = array('f',[0])
dR_leps = array('f',[0])
dPhi_lb_min = array('f',[0])

dPhi_ZH = array('f',[0])
dPhi_bjets = array('f',[0])
dPhi_leps = array('f',[0])
hhmt = array('f',[0])
hh_mt_cosine = array('f',[0])

zhmass = array('f',[0])
zhpt = array('f',[0])
zheta = array('f',[0])
zhphi = array('f',[0])
mt2_llmet = array('f',[0])

mt2_bbmet = array('f',[0])
mt2_b1l1b2l2met = array('f',[0])
mt2_b1l2b2l1met = array('f',[0])
min_mt2_blmet = array('f',[0])
mt2_ZHmet = array('f',[0])



listVarNames = [
'bpt0',
'beta0',
'bphi0',
'bpt1',
'beta1',

'bphi1',
'leppt0',
'lepeta0',
'lepphi0',
'leppt1',

'lepeta1',
'lepphi1',
'metpt',
#meteta = tree.met_eta
'metphi',

'btag0',
'btag1',
'zmass',
'zpt0',
'zeta0',

'zphi0',
'hmass0',
'hmt0',
'hpt0',
'heta0',

'hphi0',
'hToZZ_mt_cosine',
'hmass1',
'hmt1',
'hpt1',

'heta1',
'hphi1',
'nbjets',
'njets',
'nloosebjets',

#nleps = nLeps
'dEta_lb_min',
'dEta_ZH',
'dEta_bjets',
'dEta_leps',

'dR_lb_min',
'dR_ZH',
'dR_bjets',
'dR_leps',
'dPhi_lb_min',

'dPhi_ZH',
'dPhi_bjets',
'dPhi_leps',
'hhmt',
'hh_mt_cosine',

'zhmass',
'zhpt',
'zheta',
'zhphi',
'mt2_llmet',

'mt2_bbmet',
'mt2_b1l1b2l2met',
'mt2_b1l2b2l1met',
'min_mt2_blmet',
'mt2_ZHmet',
]


listVars = [
bpt0,
beta0,
bphi0,
bpt1,
beta1,

bphi1,
leppt0,
lepeta0,
lepphi0,
leppt1,

lepeta1,
lepphi1,
metpt,
#meteta = tree.met_eta
metphi,

btag0,
btag1,
zmass,
zpt0,
zeta0,

zphi0,
hmass0,
hmt0,
hpt0,
heta0,

hphi0,
hToZZ_mt_cosine,
hmass1,
hmt1,
hpt1,

heta1,
hphi1,
nbjets,
njets,
nloosebjets,

#nleps = nLeps
dEta_lb_min,
dEta_ZH,
dEta_bjets,
dEta_leps,

dR_lb_min,
dR_ZH,
dR_bjets,
dR_leps,
dPhi_lb_min,

dPhi_ZH,
dPhi_bjets,
dPhi_leps,
hhmt,
hh_mt_cosine,

zhmass,
zhpt,
zheta,
zhphi,
mt2_llmet,

mt2_bbmet,
mt2_b1l1b2l2met,
mt2_b1l2b2l1met,
min_mt2_blmet,
mt2_ZHmet,
]

#add variables 
for name, var in zip(listVarNames, listVars):
    reader.AddVariable(name, var)




inputBDTsList = ['dataset/weights/TMVAMulticlass_keras_BDT.weights.xml',
                 'dataset/weights/TMVAClassification_LD.weights.xml',
                 'dataset/weights/TMVAClassification_BDT.weights.xml',
                 'dataset/weights/TMVAMulticlass_BDT.weights.xml']


weightfile = inputBDTsList[2] #TMVAClassification_BDT.weights.xml

methodName = 'BDT'#G_multiClass' if doMultiClass else 'BDTG_biClass'
bazinga('Book {0} method'.format(methodName))
reader.BookMVA( methodName, weightfile )


bazinga('create output file')
fout = ROOT.TFile('fOut.root', 'recreate')


# h1 = Bin(100, -1., 1., lambda x: x) 
# h2 = Bin(100, -1., 1., lambda x: x) 
c = ROOT.TCanvas("TCanvasName", "TCanvasTitle", 600, 400)
h1 = ROOT.TH1D("h1","Classifier Output on TTbar  Events;BDT response; Events",100,-1.,1.)
h2 = ROOT.TH1D("h2","Classifier Output on Signal Events;BDT response; Events",100,-1.,1.)

# Bundle = UntypedLabel 
# histograms = Bundle(
#     BDT_tt      = Bin(100, -1., 1., lambda bdts: bdts[0]),
#     BDT_sig = Bin(100, -1., 1., lambda bdts: bdts[1]))
#     )


ievt = 0
bazinga('before loop over 1st tree')
for entry in bgInputFile_TT.tree:
    
    zhmass[0] = entry.zhmass
    hhmt[0] = entry.hhmt
    hpt0[0] = entry.hpt0
    hpt1[0] = entry.hpt1
    #dPhi_bjets[0] = entry.dPhi_bjets
    zpt0[0] = entry.zpt0
    dR_bjets[0] = entry.dR_bjets
    hmt0[0] = entry.hmt0
    #hmass0[0] = entry.hmass0
    #dR_leps[0] = entry.dR_leps
    min_mt2_blmet[0] = entry.min_mt2_blmet
    
    output = reader.EvaluateMVA(methodName)
  
    h1.Fill(output)
    
    
    if (ievt%10000)==0 : print 'TTbar Event ',ievt,'hhmt=',hhmt[0],'MVA output =',output
    ievt += 1
#    if (ievt > 20000) : break
    


# h1.Draw()
# ROOT.gPad.Draw()


ievt = 0

for entry in sigInputFile.tree:
    
  
    zhmass[0] = entry.zhmass
    hhmt[0] = entry.hhmt
    hpt0[0] = entry.hpt0
    hpt1[0] = entry.hpt1
    #dPhi_bjets[0] = entry.dPhi_bjets
    zpt0[0] = entry.zpt0
    dR_bjets[0] = entry.dR_bjets
    hmt0[0] = entry.hmt0
    #hmass0[0] = entry.hmass0
    #dR_leps[0] = entry.dR_leps
    min_mt2_blmet[0] = entry.min_mt2_blmet
    
    output = reader.EvaluateMVA(methodName)
  
    h2.Fill(output)
    
    
    if (ievt%500)==0 : print 'Signal event ',ievt,'hhmt=',hhmt[0],'MVA output =',output
    ievt += 1
#    if (ievt > 20000) : break


bazinga('finished 2nd histogram fill')
# rooth1 = h1.plot.root("TT BDT output", "")
# rooth2 = h2.plot.root("signal BDT outpur", "")
bazinga('h1max')
h1max = h1.GetMaximum()
bazinga('h2max')
h2max = h2.GetMaximum()
print 'h1max is ', h1max
print 'h2max is ', h2max

h2.Scale(h1max/h2max)                  
h2.SetLineColor(ROOT.kRed) 


# ROOT.gPad.Draw()
ROOT.gStyle.SetOptStat(0)

cloneh1 = h1.Clone('cloneh1')
cloneh2 = h2.Clone('cloneh2')

cloneh1.SetDirectory(0)
cloneh2.SetDirectory(0)

fout.cd()
#c.cd()
h1.Draw()
h2.Draw('same')
h1.Write('h1')#, ROOT.TObject.kOverwrite)
h2.Write('h2')#, ROOT.TObject.kOverwrite)
bazinga('creating canvas')
c.Write()
fout.ls()
#fout.Write()
fout.Close()


cloneh1.Draw()
cloneh2.Draw('same')
c.Draw()
bazinga('save canvases')
c.SaveAs('canvasReader.png')
c.SaveAs('canvasReader.root')

bazinga('close file')
#fout.Write()







# date = strftime("%Y%b%d_%H-%M", gmtime()) 

# if not doMultiClass:
#     outputFile_biClass = ROOT.TFile("TMVAOutput_biClass_" + date + "{0}.root".format('_DG' if doDGtransform else ''), "RECREATE")
#     factory = TMVA.Factory("TMVAClassification", outputFile_biClass,
#                            'V:!Silent:Color:DrawProgressBar:Transformations=I,{0}:AnalysisType=Classification'.format("D,G" if doDGtransform else ''))
#     #is last D relevant?
                        
# else:
#     outputFile_multiClass = ROOT.TFile("TMVAOutput_multiClass_" + date + "{0}.root".format('_DG' if doDGtransform else ''), "RECREATE")
#     factory = TMVA.Factory('TMVAMulticlass', outputFile_multiClass,
#                            'V:!Silent:Color:DrawProgressBar:Transformations=I,{0}:AnalysisType=multiclass'.format("D,G" if doDGtransform else ''))



# loader = ROOT.TMVA.DataLoader("dataset");

# #add variables  


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
# #loader.AddVariable("zhphi")
# loader.AddVariable("dR_bjets")
# #15


# loader.AddVariable("beta0")
# #loader.AddVariable("bphi0")
# loader.AddVariable("bpt1")
# loader.AddVariable("beta1")
# #loader.AddVariable("bphi1")
# #20
# loader.AddVariable("btag0")
# loader.AddVariable("btag1")
# loader.AddVariable("leppt0")
# #loader.AddVariable("lepphi0")
# loader.AddVariable("leppt1")
# #25
# loader.AddVariable("lepeta1")
# #loader.AddVariable("lepphi1")
# #loader.AddVariable("meteta")  #const var
# loader.AddVariable("metphi")
# loader.AddVariable("zpt0")
# loader.AddVariable("zeta0")
# #30

# #loader.AddVariable("zphi0")
# #HtoZZ
# loader.AddVariable("hpt0")
# #loader.AddVariable("hphi0")
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
# #loader.AddVariable("dPhi_leps")
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

# #loader.AddSpectator("evWgt")
# #loader.AddSpectator("countWeighted")
# #loader.AddSpectator("xsec")
# #loader.AddSpectator("genvbosonpdgid")

# bazinga('Finished loading vars')

# ROOT.TMVA.gConfig().SetDrawProgressBar(True)


# mycuts = ROOT.TCut()
# mycutb = ROOT.TCut()

# loader.AddSignalTree    (sigInputFile.tree,    1)   #signal weight  = 1     
# loader.AddBackgroundTree(bgInputFile_TT.tree, 1);   #background weight = 1 
# loader.AddBackgroundTree(bgInputFile_DY_1j.tree, 1)
# loader.AddBackgroundTree(bgInputFile_DY_2j.tree, 1)
# loader.AddBackgroundTree(bgInputFile_DY_3j.tree, 1)
# loader.AddBackgroundTree(bgInputFile_DY_4j.tree, 1)

# #for signal: 
# #factory.SetSignalWeightExpression    ("evWgt")
# #loader.SetSignalWeightExpression("xsec/countWeighted")

# #for background: 
# #factory.SetBackgroundWeightExpression("evWgt")
# #loader.SetBackgroundWeightExpression("xsec/countWeighted")

# #for both:
# loader.SetWeightExpression("xsec/countWeighted")                                                     

# loader.PrepareTrainingAndTestTree(ROOT.TCut(),#SigCut=mycuts, BkgCut=mycutb,
#                                   #nTrain_Signal=0, nTrain_Background=2000, nTest_Signal=10000, nTest_Background=10000, 
#                                   'SplitMode=Random:NormMode=NumEvents:V=True') #False

# #works only in SWAN
# bazinga('Before drawing few histograms.')
# #loader.DrawInputVariable("hhmt")
# #loader.DrawCorrelationMatrix("Signal") 

# bazinga('Book LD method')
# #factory.BookMethod( loader,TMVA.Types.kLD, "LD",
#         #            '!H!V:!VarTransform="None":CreateMVAPdfs:PDFInterpol="Spline2":Nbins=50:Nsmooth=10' )
# factory.BookMethod( loader, TMVA.Types.kLD, "LD", 
#                     "H:!V:VarTransform=None:CreateMVAPdfs:PDFInterpolMVAPdf=Spline2:NbinsMVAPdf=50:NsmoothMVAPdf=10" )

# methodName = 'BDTG_multiClass' if doMultiClass else 'BDTG_biClass'
# bazinga('Book {0} method'.format(methodName))

# factory.BookMethod(loader,
#                    TMVA.Types.kBDT,
#                    methodName,
#                    "!H:!V:NTrees=850:BoostType=Grad:Shrinkage=0.1:UseBaggedBoost=True:GradBaggingFraction=0.5:SeparationType=GiniIndex:nCuts=20:MaxDepth=1")






# DNNType = 'Standard'
# #DNNType = 'CPU'   # use new implementation                                               
# trainingStrategyFast = [{
#         "LearningRate": 1e-1,
#         "Momentum": 0.0,
#         "Repetitions": 1,
#         "ConvergenceSteps": 100,
#         "BatchSize": 50,
#         "TestRepetitions": 7,
#         "WeightDecay": 0.001,
#         "Regularization": "NONE",
#         "DropConfig": "0.0+0.5+0.5+0.5",
#         "DropRepetitions": 1,
#         "Multithreading": True
        
#     }]

# trainingStrategy = [{
#         "LearningRate": 1e-1,
#         "Momentum": 0.0,
#         "Repetitions": 1,
#         "ConvergenceSteps": 100,
#         "BatchSize": 50,
#         "TestRepetitions": 4,
#         "WeightDecay": 0.001,
#         "Regularization": "NONE",
#         "DropConfig": "0.0+0.5+0.5+0.5",
#         "DropRepetitions": 1,
#         "Multithreading": True
        
#     },  {
#         "LearningRate": 1e-2,
#         "Momentum": 0.5,
#         "Repetitions": 1,
#         "ConvergenceSteps": 100,
#         "BatchSize": 50,
#         "TestRepetitions": 2,
#         "WeightDecay": 0.001,
#         "Regularization": "TRUE",
#         "DropConfig": "0.0+0.1+0.1+0.1",
#         "DropRepetitions": 1,
#         "Multithreading": True
        
#     }, {
#         "LearningRate": 1e-3,
#         "Momentum": 0.3,
#         "Repetitions": 1,
#         "ConvergenceSteps": 100,
#         "BatchSize": 50,
#         "TestRepetitions": 2,
#         "WeightDecay": 0.001,
#         "Regularization": "NONE",
#         "Multithreading": True
    
        
# }]


# if bookDNN :
#     print 'Booking DNN method.'
#     factory.BookMethod(DataLoader=loader, Method=TMVA.Types.kDNN, MethodTitle="DNN",
#                        H = False, V=False, VarTransform="Normalize", ErrorStrategy="CROSSENTROPY",
#                        Layout=["TANH|50", "TANH|50", "TANH|10", "LINEAR"],
#                        TrainingStrategy=trainingStrategy,Architecture=DNNType)
    


# bazinga('Let the training begin!(c)')

# factory.TrainAllMethods()
# bazinga('Test all methods')

# factory.TestAllMethods()

# bazinga('Evaluate all methods')
# factory.EvaluateAllMethods()

# bazinga('Draw some output distributions')
# #factory.DrawOutputDistribution(loader.GetName(), "LD")                                   
# #factory.DrawOutputDistribution(loader.GetName(), methodName)
# if bookDNN:
#     pass
# #factory.DrawOutputDistribution(loader.GetName(), "DNN")                   

# print 'ROC integral for LD = ',factory.GetROCIntegral(loader, 'LD')
# print 'ROC integral for BDTG = ',factory.GetROCIntegral(loader, methodName)
# if bookDNN: 
#     print 'ROC integral for DNN = ',factory.GetROCIntegral(loader, 'DNN')

# roc = factory.GetROCCurve(loader)
# bazinga('Saving ROC')
# roc.SaveAs('ROC_' + date + '{0}.root'.format("_DG" if doDGtransform else ''))
# roc.SaveAs('ROC_' + date + '{0}.png'.format("_DG" if doDGtransform else ''))
# roc.Draw()

# bazinga('Closing output file.')
# outputFile_multiClass.Close() if doMultiClass else outputFile_biClass.Close()    
