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
import time

doMultiClass = False
runOnGpuMachine = False

nBDTTrees = 850 #for fast debug
useKeras = True if runOnGpuMachine else False
bazingaPrinting = True
bookDNN = False
doDGtransform = False #decorrelation and gaussian transformation
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
bazinga('Finished initializing input samples.')
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

TMVA.Tools.Instance();

date = strftime("%Y%b%d_%H-%M", gmtime()) 
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
#loader.AddVariable("zmass")
loader.AddVariable("metpt")
#loader.AddVariable("lepeta0")
#1


#loader.AddVariable("hmass0")
#loader.AddVariable("heta0")
#loader.AddVariable("hphi1")
#loader.AddVariable("hmass1")
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
loader.AddVariable("btag0")
loader.AddVariable("btag1")
#loader.AddVariable("leppt0")
#loader.AddVariable("lepphi0")
#loader.AddVariable("leppt1")
#5
#loader.AddVariable("lepeta1")
#loader.AddVariable("lepphi1")
#loader.AddVariable("meteta")  #const var
#loader.AddVariable("metphi")
#loader.AddVariable("zpt0")
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
loader.AddVariable("nbjets")
#loader.AddVariable("njets")  
#loader.AddVariable("nloosebjets")
#loader.AddVariable("nleps") #const var
loader.AddVariable("dEta_lb_min")
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
loader.AddVariable("mt2_bbmet")
#loader.AddVariable("mt2_b1l1b2l2met")
#55
#loader.AddVariable("mt2_b1l2b2l1met")
#loader.AddVariable("min_mt2_blmet")
loader.AddVariable("mt2_ZHmet")
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


mycuts = ROOT.TCut("(zmass > 76) && (zmass < 106)")
mycutb = ROOT.TCut()
mycutb = mycuts


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
    for m in list_of_mass_points:
        for sample, name in dictOfFiles.items():
            if str(m) in name:
                print 'adding ', sample
                loader.AddSignalTree    (sample.tree,    1)   #signal weight  = 1     
                count +=1
    loader.AddBackgroundTree(bgInputFile_TT.tree, 1);   #background weight = 1 
    loader.AddBackgroundTree(bgInputFile_DY_1j.tree, 1)
    loader.AddBackgroundTree(bgInputFile_DY_2j.tree, 1)
    loader.AddBackgroundTree(bgInputFile_DY_3j.tree, 1)
    loader.AddBackgroundTree(bgInputFile_DY_4j.tree, 1)
    loader.SetBackgroundWeightExpression("xsec/countWeighted") 
    count +=5

print 'loaded {0} trees'.format(count)

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
    bazinga('Book LD method')
    factory.BookMethod( loader, TMVA.Types.kLD, "LD", "H:!V:VarTransform=None:CreateMVAPdfs:PDFInterpolMVAPdf=Spline2:NbinsMVAPdf=50:NsmoothMVAPdf=10" )

methodName = 'BDT' # it is BDTG actually. Use BDT to let TMVAGui work, but remember to rename weights after, to use for GUI plots
bazinga('Book {0} method'.format(methodName))
factory.BookMethod(loader,
                   TMVA.Types.kBDT,
                   methodName,
                   "!H:!V:NTrees={0}:BoostType=Grad:Shrinkage=0.1:UseBaggedBoost=True:GradBaggingFraction=0.5:SeparationType=GiniIndex:nCuts=20:MaxDepth=3".format(nBDTTrees))






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
time_taken = end_time - start_time # time_taken is in seconds                                                      
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
