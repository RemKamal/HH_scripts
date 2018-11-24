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
from time import gmtime, strftime
import os, sys

doMultiClass = True
runOnGpuMachine = False

nBDTTrees = 850 #for fast debug
useKeras = True if runOnGpuMachine else False
bazingaPrinting = True
bookDNN = False
doDGtransform = False #decorrelation and gaussian transformation


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


sigInputFile = ROOT.TFile("BulkGraviton_M900_Hzz_minitree.root")
bgInputFile_TT = ROOT.TFile("TT_Tune_minitree.root")
bgInputFile_DY_1j = ROOT.TFile("DY1JetsToLL_M50_minitree.root")
bgInputFile_DY_2j = ROOT.TFile("DY2JetsToLL_M50_minitree.root")
bgInputFile_DY_3j = ROOT.TFile("DY3JetsToLL_M50_minitree.root")
bgInputFile_DY_4j = ROOT.TFile("DY4JetsToLL_M50_minitree.root")
bazinga('Finished initializing input samples.')
dictOfFiles = {
    sigInputFile:'sigInputFile', 
    bgInputFile_TT: 'bgInputFile_TT',
    bgInputFile_DY_1j: 'bgInputFile_DY_1j',
    bgInputFile_DY_2j: 'bgInputFile_DY_2j',
    bgInputFile_DY_3j: 'bgInputFile_DY_3j',
    bgInputFile_DY_4j: 'bgInputFile_DY_4j'
}

TMVA.Tools.Instance();

date = strftime("%Y%b%d_%H-%M", gmtime()) 

if not doMultiClass:
    outputFile_biClass = ROOT.TFile("TMVAOutput_biClass_" + date + "{0}.root".format('_DG' if doDGtransform else ''), "RECREATE")
    factory = TMVA.Factory("TMVAClassification", outputFile_biClass,
                           'V:!Silent:Color:DrawProgressBar:Transformations=I,{0}:AnalysisType=Classification'.format("D,G" if doDGtransform else ''))
    #is last D relevant?
                        
else:
    if useKeras:
        outputFile_multiClass_keras = ROOT.TFile("TMVAOutput_multiClass_keras_" + date + "{0}.root".format('_DG' if doDGtransform else ''), "RECREATE")
        factory = TMVA.Factory('TMVAMulticlass_keras', outputFile_multiClass_keras,
                               '!V:!Silent:Color:DrawProgressBar:Transformations=I,{0}:AnalysisType=multiclass'.format("D,G" if doDGtransform else ''))
        
    else:

        outputFile_multiClass = ROOT.TFile("TMVAOutput_multiClass_" + date + "{0}.root".format('_DG' if doDGtransform else ''), "RECREATE")
        factory = TMVA.Factory('TMVAMulticlass', outputFile_multiClass,
                               'V:!Silent:Color:DrawProgressBar:Transformations=I,{0}:AnalysisType=multiclass'.format("D,G" if doDGtransform else ''))



loader = ROOT.TMVA.DataLoader("dataset");

#add variables  


#loader.AddVariable("bpt0")
#loader.AddVariable("zmass")
#loader.AddVariable("metpt")
#loader.AddVariable("lepeta0")
#4


#loader.AddVariable("hmass0")
#loader.AddVariable("heta0")
#loader.AddVariable("hphi1")
#loader.AddVariable("hmass1")
#loader.AddVariable("hToZZ_mt_cosine")
loader.AddVariable("hmt0")
#10

#loader.AddVariable("dR_leps")
loader.AddVariable("hhmt")
#loader.AddVariable("dPhi_bjets")
#loader.AddVariable("zhphi")
loader.AddVariable("dR_bjets")
#15


#loader.AddVariable("beta0")
#loader.AddVariable("bphi0")
#loader.AddVariable("bpt1")
#loader.AddVariable("beta1")
#loader.AddVariable("bphi1")
#20
#loader.AddVariable("btag0")
#loader.AddVariable("btag1")
#loader.AddVariable("leppt0")
#loader.AddVariable("lepphi0")
#loader.AddVariable("leppt1")
#25
#loader.AddVariable("lepeta1")
#loader.AddVariable("lepphi1")
#loader.AddVariable("meteta")  #const var
#loader.AddVariable("metphi")
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
#35

#loader.AddVariable("heta1")
#loader.AddVariable("nbjets")
#loader.AddVariable("njets")  
#loader.AddVariable("nloosebjets")
#loader.AddVariable("nleps") #const var
# loader.AddVariable("dEta_lb_min")
# #40

# loader.AddVariable("dEta_ZH")
# loader.AddVariable("dEta_bjets")
# loader.AddVariable("dEta_leps")
#loader.AddVariable("dR_lb_min")
#loader.AddVariable("dR_ZH")
#45

#loader.AddVariable("dPhi_lb_min")
#loader.AddVariable("dPhi_ZH")
#loader.AddVariable("dPhi_leps")
#loader.AddVariable("hh_mt_cosine")
loader.AddVariable("zhmass")
#50
#loader.AddVariable("zhpt")
#loader.AddVariable("zheta")
# loader.AddVariable("mt2_llmet")
# loader.AddVariable("mt2_bbmet")
# loader.AddVariable("mt2_b1l1b2l2met")
# #55
# loader.AddVariable("mt2_b1l2b2l1met")
loader.AddVariable("min_mt2_blmet")
# loader.AddVariable("mt2_ZHmet")
#58

#loader.AddSpectator("evWgt")
#loader.AddSpectator("countWeighted")
#loader.AddSpectator("xsec")
#loader.AddSpectator("genvbosonpdgid")

bazinga('Finished loading vars')

ROOT.TMVA.gConfig().SetDrawProgressBar(True)


mycuts = ROOT.TCut()
mycutb = ROOT.TCut()

if doMultiClass:
    for sample, name in dictOfFiles.items():
        if 'Signal' or 'TT' in name:
            loader.AddTree(sample.tree, name)
            loader.SetWeightExpression("xsec/countWeighted", name) 
            
           
                
else:

    loader.AddSignalTree    (sigInputFile.tree,    1)   #signal weight  = 1     
    loader.AddBackgroundTree(bgInputFile_TT.tree, 1);   #background weight = 1 
    loader.AddBackgroundTree(bgInputFile_DY_1j.tree, 1)
    loader.AddBackgroundTree(bgInputFile_DY_2j.tree, 1)
    loader.AddBackgroundTree(bgInputFile_DY_3j.tree, 1)
    loader.AddBackgroundTree(bgInputFile_DY_4j.tree, 1)
    loader.SetWeightExpression("xsec/countWeighted") 

#for signal: 
#factory.SetSignalWeightExpression    ("evWgt")
#loader.SetSignalWeightExpression("xsec/countWeighted")

#for background: 
#factory.SetBackgroundWeightExpression("evWgt")
#loader.SetBackgroundWeightExpression("xsec/countWeighted")

#for both:
#loader.SetWeightExpression("xsec/countWeighted")                                                     

bazinga('Input contains {0} TTrees'.format(len(dictOfFiles)))

loader.PrepareTrainingAndTestTree(ROOT.TCut(),#SigCut=mycuts, BkgCut=mycutb,
                                  #nTrain_Signal=0, nTrain_Background=2000, nTest_Signal=10000, nTest_Background=10000, 
                                  'SplitMode=Random:NormMode=NumEvents:V=True') #False



# Define initialization                                                                                                             
def normal(shape, name=None):
    #return initializations.normal(shape, scale=0.05, name=name)                                                                    
    return initializers.normal(shape, scale=0.05, name=name)


nVars = (loader.GetDataSetInfo()).GetNVariables()


if useKeras:
    # Define model                                                                                                                      
    model = Sequential()
    model.add(Dense(12, init="normal", activation='relu', W_regularizer=l2(1e-5), input_dim=nVars ))#len(variables)))
#model.add(Dense(2, init="normal", activation='softmax'))                                                                           
#model.add(Dense(1, init="normal", activation='softmax'))                                                                           
# can have any number of inner layers and parameters                                                                                
    
    fix = len(dictOfFiles) #nTrees if nTrees==4 else 4#????                                                                                               
    model.add(Dense(fix, init="normal", activation='softmax'))
    model.add(Dense(fix, init="normal", activation='softmax'))
    

# Set loss and optimizer                                                                                                            
    model.compile(loss='categorical_crossentropy', optimizer=SGD(lr=0.01), metrics=['accuracy',])
    
    # Store model to file                                                                                                               
    model.save('model.h5')
    model.summary()



#works only in SWAN
bazinga('Before drawing few histograms.')
#loader.DrawInputVariable("hhmt")
#loader.DrawCorrelationMatrix("Signal") 

bazinga('Book LD method')
factory.BookMethod( loader, TMVA.Types.kLD, "LD", "H:!V:VarTransform=None:CreateMVAPdfs:PDFInterpolMVAPdf=Spline2:NbinsMVAPdf=50:NsmoothMVAPdf=10" )

methodName = 'BDT' # to let TMVAGui work 
#G_multiClass' if doMultiClass else 'BDTG_biClass'
bazinga('Book {0} method'.format(methodName))

factory.BookMethod(loader,
                   TMVA.Types.kBDT,
                   methodName,
                   "!H:!V:NTrees={0}:BoostType=Grad:Shrinkage=0.1:UseBaggedBoost=True:GradBaggingFraction=0.5:SeparationType=GiniIndex:nCuts=20:MaxDepth=1".format(nBDTTrees))






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
    #when more signal sample is available, the method below would be preferrable, or more layers in BDT (MaxDepth)
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
    pass
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


    print 'ROC integral for LD = ',factory.GetROCIntegral(loader, 'LD')
    print 'ROC integral for BDT = ',factory.GetROCIntegral(loader, methodName)
    if bookDNN: 
        print 'ROC integral for DNN = ',factory.GetROCIntegral(loader, 'DNN')
else:
    tgr = factory.GetROCCurve(loader)#, methodName) 
    print 'ROC integral for BDT = ', tgr.Integral()


if not doMultiClass:
    roc = factory.GetROCCurve(loader)
    bazinga('Saving ROC')
    roc.SaveAs('ROC_' + date + '{0}.root'.format("_DG" if doDGtransform else ''))
    roc.SaveAs('ROC_' + date + '{0}.png'.format("_DG" if doDGtransform else ''))
    roc.Draw()

bazinga('Closing output file.')

if doMultiClass and useKeras:
    outputFile_multiClass_keras.Close()
elif doMultiClass:
    outputFile_multiClass.Close()
else:
    outputFile_biClass.Close()


for sample, name in dictOfFiles.items():
    sample.Close()
                  
 

                 

tmvaFileToOpen = (outputFile_multiClass if doMultiClass else outputFile_biClass).GetName()


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

if os.path.isfile(tmvaFileToOpen):
    print 'File exists'
    if os.path.getsize(tmvaFileToOpen) > 0:
        print 'File has non-zero size'
        if (outputFile_multiClass if doMultiClass else outputFile_biClass).IsZombie():
            print 'File is ZOMBIE'
            sys.exit(1)
        else:
            bazinga('doMultiClass = {0}, runOnGpuMachine = {1}'.format(doMultiClass, runOnGpuMachine))
            if runOnGpuMachine:
                print ('Do nothing, GPU seems not to like the GUI')
            else:
                exit(1)
                if doMultiClass:
                    bazinga ('Opening created output file for multiclass.')
                    TMVA.TMVAMultiClassGui(tmvaFileToOpen)
                    raw_input('Press Enter to exit')
                else:
                    TMVA.TMVAGui(tmvaFileToOpen)
                    raw_input('Press Enter to exit')
                




#lines below are not working
# bazinga (outputFile_multiClass if doMultiClass else outputFile_biClass)
# # open the GUI for the result macros    
# print ( "TMVAGui(\"%s\")" % "TMVAOutput_biClass_2017May08_10-24.root" )
# gROOT.ProcessLine( "TMVA.TMVAGui(\"%s\")" % "TMVAOutput_biClass_2017May08_10-24.root" )
# # keep the ROOT thread running
# gApplication.Run() 
