
# coding: utf-8

# In[1]:

import ROOT
import time
from ROOT import TMVA
#from IPython.core.extensions import ExtensionManager
#ExtensionManager(get_ipython()).load_extension("JsMVA.JsMVAMagic")
#get_ipython().magic('jsmva on')


# In[2]:

start_time = time.time()
doMultiClass = False
nBDTTrees = 850 #for fast debug                                                 
bookDNN = False
doDGtransform = False #decorrelation and gaussian transformation  


# In[3]:

list_of_mass_points = [#which mass points for signal to combine
    260,270,300,350,400,450]
if list_of_mass_points:
    print 'list_of_mass_points is ', list_of_mass_points
else:
    print 'please use syntax w/o spaces for comma separated list of masses: python train..py mass1,mass2,massN'
    sys.exit(1)


# In[4]:

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
print 'done'


# In[5]:

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



from time import gmtime, strftime
date = strftime("%Y%b%d_%H-%M", gmtime())
fileName = None


# In[6]:

TMVA.Tools.Instance();

if doMultiClass:
        outputFile_multiClass = ROOT.TFile("TMVAOutput_" + str(list_of_mass_points[-1]) + "_multiClass_" + date + "{0}.root".format('_DG' if doDGtransform else ''), "RECREATE")
        factory = TMVA.Factory('TMVAMulticlass_' + str(list_of_mass_points[-1]), outputFile_multiClass,
                               '!V:!Silent:Color:DrawProgressBar:Transformations=I,{0}:AnalysisType=multiclass'.format("D,G" if doDGtransform else ''))
        fileName = outputFile_multiClass
else:
        outputFile_biClass = ROOT.TFile("TMVAOutput_" + str(list_of_mass_points[0]) + '_' + str(list_of_mass_points[-1]) + "_biClass_" + date + "{0}.root".format('_DG' if doDGtransform else ''), "RECREATE")
        factory = TMVA.Factory("TMVAClassification" + str(list_of_mass_points[0]) + '_' + str(list_of_mass_points[-1]), outputFile_biClass,
                               'V:!Silent:Color:DrawProgressBar:Transformations=I,{0}:AnalysisType=Classification'.format("D,G" if doDGtransform else ''))
        fileName = outputFile_biClass
fileName


# In[7]:

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
# ',bphi1"
#]
# loader.AddVariable("leppt0")
# loader.AddVariable("lepeta0")
# loader.AddVariable("lepphi0")
# loader.AddVariable("leppt1")
# loader.AddVariable("lepeta1")
# loader.AddVariable("lepphi1")
# loader.AddVariable("metpt")
# loader.AddVariable("metphi")
# loader.AddVariable("btag0")
# loader.AddVariable("btag1")
# loader.AddVariable("zmass")
# loader.AddVariable("zpt0")
# loader.AddVariable("zeta0")
# loader.AddVariable("zphi0")
# loader.AddVariable("hmass0")
# loader.AddVariable("hmt0")
# loader.AddVariable("hpt0")
# loader.AddVariable("heta0")
# loader.AddVariable("hphi0")
# loader.AddVariable("hToZZ_mt_cosine")
# loader.AddVariable("hmass1")
# loader.AddVariable("hmt1")
# loader.AddVariable("hpt1")
# loader.AddVariable("heta1")
# loader.AddVariable("hphi1")
# loader.AddVariable("nbjets")
# loader.AddVariable("njets")
# loader.AddVariable("nloosebjets")
# loader.AddVariable("dEta_lb_min")
# loader.AddVariable("dEta_ZH")
# loader.AddVariable("dEta_bjets")
# loader.AddVariable("dEta_leps")
# loader.AddVariable("dR_lb_min")
# loader.AddVariable("dR_ZH")
# loader.AddVariable("dR_bjets")
# loader.AddVariable("dR_leps")
# loader.AddVariable("dPhi_lb_min")
# loader.AddVariable("dPhi_ZH")
# loader.AddVariable("dPhi_bjets")
# loader.AddVariable("dPhi_leps")
# loader.AddVariable("hhmt")
# loader.AddVariable("hh_mt_cosine")
# loader.AddVariable("zhmass")
# loader.AddVariable("zhpt")
# loader.AddVariable("zheta")
# loader.AddVariable("zhphi")
# loader.AddVariable("mt2_llmet")
# loader.AddVariable("mt2_bbmet")
# loader.AddVariable("mt2_b1l1b2l2met")
# loader.AddVariable("mt2_b1l2b2l1met")
# loader.AddVariable("min_mt2_blmet")
# loader.AddVariable("mt2_ZHmet")
# #58                                       

# In[11]:

#loader.AddSpectator("evWgt")
#loader.AddSpectator("countWeighted")
#loader.AddSpectator("xsec")
#loader.AddSpectator("genvbosonpdgid")


# In[12]:

ROOT.TMVA.gConfig().SetDrawProgressBar(True)
loader = ROOT.TMVA.DataLoader("dataset");

seenFiles = list()
count = 0
if doMultiClass:
    for m in list_of_mass_points:
        for sample, name in dictOfFiles.items():
            print 'seenFiles is ', seenFiles
            if name not in seenFiles:
                if str(m) in name:
                    bazinga('Loading {0} sample'.format(sample))
                    loader.AddTree(sample.tree, 'Signal')
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

#for signal    : 
#factory.SetSignalWeightExpression    ("evWgt")
#loader.SetWeightExpression("xsec/countWeighted")

#for background: 
#factory.SetBackgroundWeightExpression("evWgt")
#loader.SetBackgroundWeightExpression("xsec/countWeighted")




# In[13]:

mycuts = mycutb = ROOT.TCut('(zmass >= 76) && (zmass <= 106)')
loader.PrepareTrainingAndTestTree(#SigCut=
                                  mycuts, #BkgCut=
                                  mycutb,
                                  #nTrain_Signal=0, nTrain_Background=2000, nTest_Signal=10000, nTest_Background=10000, 
                                  'SplitMode=Random:NormMode=NumEvents:V=True')


# In[14]:

myList = ['metpt', 'dR_leps', 'dR_bjets', 'btag0', 'btag1', 'hpt0', 'hpt1', 'nbjets', 'dEta_lb_min', 'mt2_bbmet', 'mt2_ZHmet' ]                                            
# prefix = 'loader.DrawInputVariable("'
# for var in myList:                                                                                                                                                         
#     print prefix + var + '")'                                                                                                                                                    




# In[15]:

# loader.DrawInputVariable("metpt")
# loader.DrawInputVariable("dR_leps")
# loader.DrawInputVariable("dR_bjets")
# loader.DrawInputVariable("btag0")
# loader.DrawInputVariable("btag1")
# loader.DrawInputVariable("hpt0")
# loader.DrawInputVariable("hpt1")
# loader.DrawInputVariable("nbjets")
# loader.DrawInputVariable("dEta_lb_min")
# loader.DrawInputVariable("mt2_bbmet")
# loader.DrawInputVariable("mt2_ZHmet")


# loader.DrawInputVariable("bpt0")
# loader.DrawInputVariable("beta0")
# loader.DrawInputVariable("bphi0")
# loader.DrawInputVariable("bpt1")
# loader.DrawInputVariable("beta1")
# loader.DrawInputVariable("bphi1")
# loader.DrawInputVariable("leppt0")
# loader.DrawInputVariable("lepeta0")
# loader.DrawInputVariable("lepphi0")
# loader.DrawInputVariable("leppt1")
# loader.DrawInputVariable("lepeta1")
# loader.DrawInputVariable("lepphi1")
# loader.DrawInputVariable("metpt")
# loader.DrawInputVariable("metphi")
# loader.DrawInputVariable("btag0")
# loader.DrawInputVariable("btag1")
# loader.DrawInputVariable("zmass")
# loader.DrawInputVariable("zpt0")
# loader.DrawInputVariable("zeta0")
# loader.DrawInputVariable("zphi0")
# loader.DrawInputVariable("hmass0")
# loader.DrawInputVariable("hmt0")
# loader.DrawInputVariable("hpt0")
# loader.DrawInputVariable("heta0")
# loader.DrawInputVariable("hphi0")
# loader.DrawInputVariable("hToZZ_mt_cosine")
# loader.DrawInputVariable("hmass1")
# loader.DrawInputVariable("hmt1")
# loader.DrawInputVariable("hpt1")
# loader.DrawInputVariable("heta1")
# loader.DrawInputVariable("hphi1")
# loader.DrawInputVariable("nbjets")
# loader.DrawInputVariable("njets")
# loader.DrawInputVariable("nloosebjets")
# loader.DrawInputVariable("dEta_lb_min")
# loader.DrawInputVariable("dEta_ZH")
# loader.DrawInputVariable("dEta_bjets")
# loader.DrawInputVariable("dEta_leps")
# loader.DrawInputVariable("dR_lb_min")
# loader.DrawInputVariable("dR_ZH")
# loader.DrawInputVariable("dR_bjets")
# loader.DrawInputVariable("dR_leps")
# loader.DrawInputVariable("dPhi_lb_min")
# loader.DrawInputVariable("dPhi_ZH")
# loader.DrawInputVariable("dPhi_bjets")
# loader.DrawInputVariable("dPhi_leps")
# loader.DrawInputVariable("hhmt")
# loader.DrawInputVariable("hh_mt_cosine")
# loader.DrawInputVariable("zhmass")
# loader.DrawInputVariable("zhpt")
# loader.DrawInputVariable("zheta")
# loader.DrawInputVariable("zhphi")
# loader.DrawInputVariable("mt2_llmet")
# loader.DrawInputVariable("mt2_bbmet")
# loader.DrawInputVariable("mt2_b1l1b2l2met")
# loader.DrawInputVariable("mt2_b1l2b2l1met")
# loader.DrawInputVariable("min_mt2_blmet")
# loader.DrawInputVariable("mt2_ZHmet")

# In[16]:

if not doMultiClass:
    print('Book LD method')
    factory.BookMethod( loader, TMVA.Types.kLD, "LD", "H:!V:VarTransform=None:CreateMVAPdfs:PDFInterpolMVAPdf=Spline2:NbinsMVAPdf=50:NsmoothMVAPdf=10" )

methodName = 'BDT' # it is BDTG actually. Use BDT to let TMVAGui work, but remember to rename weights after, to use for GUI plots                                                                                                                                             
print('Book {0} method'.format(methodName))
factory.BookMethod(loader,
                   TMVA.Types.kBDT,
                   methodName,
                   "!H:!V:NTrees={0}:BoostType=Grad:Shrinkage=0.1:UseBaggedBoost=True:GradBaggingFraction=0.5:SeparationType=GiniIndex:nCuts=20:MaxDepth=3".format(nBDTTrees))




# In[17]:

#loader.DrawCorrelationMatrix("Signal") 


# In[18]:

#loader.DrawCorrelationMatrix("Background") 


# In[19]:

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


# In[20]:

if (bookDNN) :
    factory.BookMethod(DataLoader=loader, Method=TMVA.Types.kDNN, MethodTitle="DNN",
                       H = False, V=False, VarTransform="Normalize", ErrorStrategy="CROSSENTROPY",
                       Layout=["TANH|50", "TANH|50", "TANH|10", "LINEAR"],
                       TrainingStrategy=trainingStrategy,Architecture=DNNType)


# In[21]:

factory.TrainAllMethods()


# In[22]:

factory.TestAllMethods()


# In[23]:

factory.EvaluateAllMethods()


# In[24]:

#factory.DrawOutputDistribution(loader.GetName(), "LD")                                   
#factory.DrawOutputDistribution(loader.GetName(), "BDT")
#if (bookDNN) : factory.DrawOutputDistribution(loader.GetName(), "DNN")                   



# In[25]:

print 'ROC integral for LD = ',factory.GetROCIntegral(loader, 'LD')
print 'ROC integral for BDTG = ',factory.GetROCIntegral(loader, 'BDT')
#if (bookDNN) : print 'ROC integral for DNN = ',factory.GetROCIntegral(loader, 'DNN')
#ROC integral for LD = 0.999232828617
#ROC integral for BDT = 0.999716460705
#ROC integral for DNN = 0.998159885406



# In[26]:

roc = factory.GetROCCurve(loader)
roc.SaveAs('ROC_' + str(list_of_mass_points[0]) + '_' + str(list_of_mass_points[-1]) + '_' + date + '{0}.root'.format("_DG" if doDGtransform else ''))
roc.SaveAs('ROC_' + str(list_of_mass_points[0]) + '_' + str(list_of_mass_points[-1]) + '_' + date + '{0}.png'.format("_DG" if doDGtransform else ''))
roc.Draw()


# In[27]:

if fileName:
    fileName.Close()
print 'all done'


# In[28]:

for sample, name in dictOfFiles.items():
    sample.Close()


# # Reader part
# 

# In[29]:

import ROOT
from ROOT import TMVA
#from IPython.core.extensions import ExtensionManager
#ExtensionManager(get_ipython()).load_extension("JsMVA.JsMVAMagic")
#get_ipython().magic('jsmva on')


# In[30]:


weightFile = 'dataset/weights/TMVAClassification' + str(list_of_mass_points[0]) + '_' + str(list_of_mass_points[-1]) + '_BDT.weights.xml'


# In[31]:

# myList = ['metpt', 'dR_leps', 'dR_bjets', 'btag0', 'btag1', 'hpt0', 'hpt1', 'nbjets', 'dEta_lb_min', 'mt2_bbmet', 'mt2_ZHmet' ]                                            
# prefix = " = array('f',[0])"
# for var in myList:                                                                                                                                                         
#     print var + prefix                                                                                                                         
    




# In[32]:


from array import array
TMVA.Tools.Instance()
reader = TMVA.Reader( "Color:Silent" )

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



# # listVarNames

# listVarNames = [
# 'bpt0',
# 'beta0',
# 'bphi0',
# 'bpt1',
# 'beta1',
# 
# 'bphi1',
# 'leppt0',
# 'lepeta0',
# 'lepphi0',
# 'leppt1',
# 
# 'lepeta1',
# 'lepphi1',
# 'metpt',
# #meteta = tree.met_eta                                                                                                                                                                                                                                                                                                                                                                                          
# 'metphi',
#     
# 'btag0',
# 'btag1',
# 'zmass',
# 'zpt0',
# 'zeta0',
#     
# 'zphi0',
# 'hmass0',
# 'hmt0',
# 'hpt0',
# 'heta0',
# 
# 'hphi0',
# 'hToZZ_mt_cosine',
# 'hmass1',
# 'hmt1',
# 'hpt1',
# 
# 'heta1',
# 'hphi1',
# 'nbjets',
# 'njets',
# 'nloosebjets',
# 
# #nleps = nLeps                                                                                                                                                                                                                                                                                                                                                                                                  
# 'dEta_lb_min',
# 'dEta_ZH',
# 'dEta_bjets',
# 'dEta_leps',
# 
# 'dR_lb_min',
# 'dR_ZH',
# 'dR_bjets',
# 'dR_leps',
# 'dPhi_lb_min',
# 
# 'dPhi_ZH',
# 'dPhi_bjets',
# 'dPhi_leps',
# 'hhmt',
# 'hh_mt_cosine',
# 
# 'zhmass',
# 'zhpt',
# 'zheta',
# 'zhphi',
# 'mt2_llmet',
# 
# 'mt2_bbmet',
# 'mt2_b1l1b2l2met',
# 'mt2_b1l2b2l1met',
# 'min_mt2_blmet',
# 'mt2_ZHmet',
# ]

# # listVars
# 
# 

# 
# listVars = [
# bpt0,
# beta0,
# bphi0,
# bpt1,
# beta1,
# 
# bphi1,
# leppt0,
# lepeta0,
# lepphi0,
# leppt1,
# 
# lepeta1,
# lepphi1,
# metpt,
# #meteta = tree.met_eta                                                                                                                                                                                                                                                                                                                                                                                          
# metphi,
#     
# btag0,
# btag1,
# zmass,
# zpt0,
# zeta0,
# 
# btag0,
# btag1,
# zmass,
# zpt0,
# zeta0,
# 
# zphi0,
# hmass0,
# hmt0,
# hpt0,
# heta0,
# 
# hphi0,
# hToZZ_mt_cosine,
# hmass1,
# hmt1,
# hpt1,
# 
# heta1,
# hphi1,
# nbjets,
# njets,
# nloosebjets,
# 
# #nleps = nLeps                                                                                                                                                                                                                                                                                                                                                                                                  
# dEta_lb_min,
# dEta_ZH,
# dEta_bjets,
# dEta_leps,
# 
# dR_lb_min,
# dR_ZH,
# dR_bjets,
# dR_leps,
# dPhi_lb_min,
# 
# dPhi_ZH,
# dPhi_bjets,
# dPhi_leps,
# hhmt,
# hh_mt_cosine,
# 
# zhmass,
# zhpt,
# zheta,
# zhphi,
# mt2_llmet,
# 
# mt2_bbmet,
# mt2_b1l1b2l2met,
# mt2_b1l2b2l1met,
# min_mt2_blmet,
# mt2_ZHmet,
# ]
# 
# 

# import array
# 
# TMVA.Tools.Instance()
# reader = TMVA.Reader( "Color:Silent" )
# 
# 
# 
# n=0
# for var in listVarNames:
#     exec('var'+str(n)+' = array.array(\'f\',[0])')
#     exec('reader.AddVariable("'+var+'",var'+str(n)+')')
#     n+=1

# In[33]:

# prefix = 'reader.AddVariable("'

# myList = ['metpt', 'dR_leps', 'dR_bjets', 'btag0', 'btag1', 'hpt0', 'hpt1', 'nbjets', 'dEta_lb_min', 'mt2_bbmet', 'mt2_ZHmet' ]                                            
# for var in myList:                                                                                                                                                         
#     print prefix + var + '", ' + var +  ')'                                                                                                    
    



# reader.AddVariable("bpt0", bpt0)
# reader.AddVariable("beta0", beta0)
# reader.AddVariable("bphi0", bphi0)
# reader.AddVariable("bpt1", bpt1)
# reader.AddVariable("beta1", beta1)
# 
# reader.AddVariable("bphi1", bphi1)
# reader.AddVariable("leppt0", leppt0)
# reader.AddVariable("lepeta0", lepeta0)
# reader.AddVariable("lepphi0", lepphi0)
# reader.AddVariable("leppt1", leppt1)
# 
# reader.AddVariable("lepeta1", lepeta1)
# reader.AddVariable("lepphi1", lepphi1)
# reader.AddVariable("metpt", metpt)
# reader.AddVariable("metphi", metphi)
# reader.AddVariable("btag0", btag0)
# 
# reader.AddVariable("btag1", btag1)
# reader.AddVariable("zmass", zmass)
# reader.AddVariable("zpt0", zpt0)
# reader.AddVariable("zeta0", zeta0)
# reader.AddVariable("zphi0", zphi0)
# 
# reader.AddVariable("hmass0", hmass0)
# reader.AddVariable("hmt0", hmt0)
# reader.AddVariable("hpt0", hpt0)
# reader.AddVariable("heta0", heta0)
# reader.AddVariable("hphi0", hphi0)
# 
# reader.AddVariable("hToZZ_mt_cosine", hToZZ_mt_cosine)
# reader.AddVariable("hmass1", hmass1)
# reader.AddVariable("hmt1", hmt1)
# reader.AddVariable("hpt1", hpt1)
# reader.AddVariable("heta1", heta1)
# 
# reader.AddVariable("hphi1", hphi1)
# reader.AddVariable("nbjets", nbjets)
# reader.AddVariable("njets", njets)
# reader.AddVariable("nloosebjets", nloosebjets)
# reader.AddVariable("dEta_lb_min", dEta_lb_min)
# 
# reader.AddVariable("dEta_ZH", dEta_ZH)
# reader.AddVariable("dEta_bjets", dEta_bjets)
# reader.AddVariable("dEta_leps", dEta_leps)
# reader.AddVariable("dR_lb_min", dR_lb_min)
# reader.AddVariable("dR_ZH", dR_ZH)
# 
# reader.AddVariable("dR_bjets", dR_bjets)
# reader.AddVariable("dR_leps", dR_leps)
# reader.AddVariable("dPhi_lb_min", dPhi_lb_min)
# reader.AddVariable("dPhi_ZH", dPhi_ZH)
# reader.AddVariable("dPhi_bjets", dPhi_bjets)
# 
# reader.AddVariable("dPhi_leps", dPhi_leps)
# reader.AddVariable("hhmt", hhmt)
# reader.AddVariable("hh_mt_cosine", hh_mt_cosine)
# reader.AddVariable("zhmass", zhmass)
# reader.AddVariable("zhpt", zhpt)
# 
# reader.AddVariable("zheta", zheta)
# reader.AddVariable("zhphi", zhphi)
# reader.AddVariable("mt2_llmet", mt2_llmet)
# reader.AddVariable("mt2_bbmet", mt2_bbmet)
# reader.AddVariable("mt2_b1l1b2l2met", mt2_b1l1b2l2met)
# 
# reader.AddVariable("mt2_b1l2b2l1met", mt2_b1l2b2l1met)
# reader.AddVariable("min_mt2_blmet", min_mt2_blmet)
# reader.AddVariable("mt2_ZHmet", mt2_ZHmet)

# list_of_diff_mvas = [# xml mva files go here
#     'dataset/weights/TMVAClassification270_BDT.weights.xml
#     ]
# weightsFile = 'dataset/weights/TMVAClassification270_BDT.weights.xml-
# print type(list_of_diff_mvas)

# j = 0
# for mva in list_of_diff_mvas:
#     print 'mva is ', mva
#     print 'mva type is ', type(mva)
#     print 'mva[-15:-11] is ', mva[-15:-11]
#     print 'mva is ', mva
#     reader.BookMVA('BDT', list_of_diff_mvas[j] )
#     j +=1 
#     

# In[34]:

reader.AddVariable("metpt", metpt)
reader.AddVariable("dR_leps", dR_leps)
reader.AddVariable("dR_bjets", dR_bjets)
reader.AddVariable("btag0", btag0)
reader.AddVariable("btag1", btag1)
reader.AddVariable("hpt0", hpt0)
reader.AddVariable("hpt1", hpt1)
reader.AddVariable("nbjets", nbjets)
reader.AddVariable("dEta_lb_min", dEta_lb_min)
reader.AddVariable("mt2_bbmet", mt2_bbmet)
reader.AddVariable("mt2_ZHmet", mt2_ZHmet)


# In[35]:

reader.BookMVA('BDT', weightFile)


# In[36]:

hTT = ROOT.TH1D("hTT","Classifier Output on TT Background Events",100,-1.,1.)
hDY_2j = ROOT.TH1D("hDY_2j","Classifier Output on Dy_2j Background Events",100,-1.,1.)

hS450 = ROOT.TH1D("hS450","Classifier Output on Signal 450 GeV Events",100,-1.,1.)
hS300 = ROOT.TH1D("hS300","Classifier Output on Signal 300 GeV Events",100,-1.,1.)
hS260 = ROOT.TH1D("hS260","Classifier Output on Signal 260 GeV Events",100,-1.,1.)


# In[37]:


    
# suffix = '[0] = entry.'
# for var in myList:
#     myst = '    {0}'.format(var) + suffix + '{0}'.format(var) 
#     print myst


# In[38]:

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




#sigInputFile_260


# In[59]:

ievt = 0

for entry in sigInputFile_260.tree: 
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

    
    output = reader.EvaluateMVA(methodName)
  
    hS260.Fill(output)
    
    
    if (ievt%200)==0 : print 'For tree ', dictOfFiles[sigInputFile_260], ' event ',ievt,' has btag0=',btag0[0],'and MVA output =', output
    ievt += 1
#    if (ievt > 20000) : break

print 'max for hS260 is ', hS260.GetMaximum()
hS260.Draw()
#ROOT.gPad.Draw()   


# In[40]:

#sigInputFile_300


# In[41]:

ievt = 0

for entry in sigInputFile_300.tree: 
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

    
    output = reader.EvaluateMVA(methodName)
  
    hS300.Fill(output)
    
    
    if (ievt%200)==0 : print 'For tree ', dictOfFiles[sigInputFile_300], ' event ',ievt,' has btag0=',btag0[0],'and MVA output =', output
    ievt += 1
#    if (ievt > 20000) : break

print 'max for hS300 is ', hS300.GetMaximum()
hS300.Draw()
#ROOT.gPad.Draw()   


# In[42]:

ievt = 0

for entry in sigInputFile_450.tree: 
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

    
    output = reader.EvaluateMVA(methodName)
  
    hS450.Fill(output)
    
    
    if (ievt%200)==0 : print 'For tree ', dictOfFiles[sigInputFile_450], ' event ',ievt,' has btag0=',btag0[0],'and MVA output =', output
    ievt += 1
#    if (ievt > 20000) : break

print 'max for hS450 is ', hS450.GetMaximum()
hS450.Draw()
#ROOT.gPad.Draw()   


# In[43]:

#weightFile


# In[45]:

ievt = 0
for entry in bgInputFile_TT.tree: 
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
    
    
    output = reader.EvaluateMVA(methodName)
  
    hTT.Fill(output)
    
    
    if (ievt%10000)==0 : print 'For tree ', dictOfFiles[bgInputFile_TT], ' event ',ievt,' has btag0=',btag0[0],'and MVA output =', output
    ievt += 1
#    if (ievt > 20000) : break
print 'max for hTT is ', hTT.GetMaximum()
hTT.Draw("")
#ROOT.gPad.Draw()   


# In[46]:

ievt = 0

for entry in bgInputFile_DY_2j.tree: 
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
    
    
    output = reader.EvaluateMVA(methodName)
  
    hDY_2j.Fill(output)
    
    
    if (ievt%10000)==0 : print 'For tree ', dictOfFiles[bgInputFile_DY_2j], ' event ',ievt,' has btag0=',btag0[0],'and MVA output =', output
    ievt += 1
#    if (ievt > 20000) : break
print 'max for hDY_2j is ', hDY_2j.GetMaximum()
hDY_2j.Draw("")
#ROOT.gPad.Draw()   


# In[47]:


# hS260.Draw()

# hS300.SetLineColor(ROOT.kGreen+2)
# hS300.Draw("SAME")

# hS450.SetLineColor(ROOT.kBlack)
# hS450.Draw("SAME")


# hDY_2j.SetLineColor(ROOT.kMagenta+3)
# hDY_2j.Draw("SAME")

# hTT.SetLineColor(ROOT.kRed+3)
# hTT.Draw("SAME")

# ROOT.gPad.Draw()
# #ROOT.gPad.BuildLegend()


# In[48]:

mymax = max(hTT.GetMaximum(), hDY_2j.GetMaximum())
#mymax


# In[49]:

hS260.Scale(mymax/hS260.GetMaximum())
hS260.Draw()

ROOT.gPad.Draw()

#ROOT.gPad.BuildLegend()


# In[50]:

hS300.Scale(mymax/hS300.GetMaximum())
hS300.SetLineColor(ROOT.kGreen+2)
hS300.Draw("")
#ROOT.gPad.Draw()

#ROOT.gPad.BuildLegend()


# In[51]:


hS450.Scale(mymax/hS450.GetMaximum())
hS450.SetLineColor(ROOT.kBlack)
hS450.Draw("")

#ROOT.gPad.Draw()

#ROOT.gPad.BuildLegend()


# In[52]:


hDY_2j.SetLineColor(ROOT.kMagenta+3)
hDY_2j.Draw("")

#ROOT.gPad.Draw()

#ROOT.gPad.BuildLegend()


# In[53]:

hTT.Scale(mymax/hTT.GetMaximum())
hTT.SetLineColor(ROOT.kRed+3)
hTT.Draw("")
#ROOT.gPad.Draw()

#ROOT.gPad.BuildLegend()


# In[54]:


# hS260.Draw()

# hS300.SetLineColor(ROOT.kGreen+2)
# hS300.Draw("SAME")

# hS450.SetLineColor(ROOT.kBlack)
# hS450.Draw("SAME")


# hDY_2j.SetLineColor(ROOT.kMagenta+3)
# hDY_2j.Draw("SAME")

# hTT.SetLineColor(ROOT.kRed+3)
# hTT.Draw("SAME")
# ROOT.gPad.Draw()

#ROOT.gPad.BuildLegend()


# In[55]:


end_time = time.time()
time_taken = end_time - start_time # time_taken is in seconds                                                                                                                                                                     
hours, rest = divmod(time_taken,3600)
minutes, seconds = divmod(rest, 60)
print( "---it took {hours} hours, {minutes} minutes and {seconds:.1f} seconds to run the analysis ---".format (hours=hours, minutes=minutes, seconds=seconds) )


# In[ ]:




# In[ ]:




# In[64]:

hhmt = ROOT.TH1D("hhmt","hhmt of Signal 450 GeV Events",40,200.,600.)

ievt = 0

for entry in sigInputFile_450.tree: 
    if entry.zmass <= 76 or entry.zmass >= 106: continue
    if entry.hmass1 <= 90 or entry.hmass1 >= 150: continue
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

    
    output = reader.EvaluateMVA(methodName)
    if output < -0.11: continue
    hS450.Fill(output)
    hhmt.Fill(entry.hhmt)
    
    if (ievt%200)==0 : print 'For tree ', dictOfFiles[sigInputFile_450], ' event ',ievt,' has btag0=',btag0[0],'and MVA output =', output
    ievt += 1
#    if (ievt > 20000) : break

print 'max for hS450 is ', hS450.GetMaximum()
hhmt.Draw()
#ROOT.gPad.Draw()   


# In[69]:


hhmt = ROOT.TH1D("hhmt","hhmt of TT Events",40,200.,600.)

ievt = 0

for entry in bgInputFile_TT.tree: 
    if entry.zmass <= 76 or entry.zmass >= 106: continue
    #CRDY
    #if entry.hmass1 <= 90 or entry.hmass1 >= 150: continue
    if entry.hmass1 > 90 and entry.hmass1 < 150: continue

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

    
    output = reader.EvaluateMVA(methodName)
    if output > 0.61: 
        hTT.Fill(output)
        hhmt.Fill(entry.hhmt)
    
        if (ievt%10000)==0 : print 'For tree ', dictOfFiles[bgInputFile_TT], ' event ',ievt,' has btag0=',btag0[0],'and MVA output =', output
        ievt += 1
#    if (ievt > 20000) : break

print 'max for hTT is ', hTT.GetMaximum()
hhmt.Draw()
#ROOT.gPad.Draw()   


# In[70]:


hhmt = ROOT.TH1D("hhmt","hhmt of TT Events",40,200.,600.)

ievt = 0

for entry in bgInputFile_TT.tree: 
    #CRTT
    #if entry.zmass <= 76 or entry.zmass >= 106: continue
    if entry.zmass > 76 and entry.zmass < 106: continue

    #CRDY
    if entry.hmass1 <= 90 or entry.hmass1 >= 150: continue
    #if entry.hmass1 > 90 and entry.hmass1 < 150: continue

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

    
    output = reader.EvaluateMVA(methodName)
    if output > 0.61: 
        hTT.Fill(output)
        hhmt.Fill(entry.hhmt)
    
        if (ievt%10000)==0 : print 'For tree ', dictOfFiles[bgInputFile_TT], ' event ',ievt,' has btag0=',btag0[0],'and MVA output =', output
        ievt += 1
#    if (ievt > 20000) : break

print 'max for hTT is ', hTT.GetMaximum()
hhmt.Draw()
#ROOT.gPad.Draw()   


# In[76]:


hhmt = ROOT.TH1D("hhmt","hhmt of DY_2j Events",40,200.,600.)

ievt = 0

for entry in bgInputFile_DY_2j.tree: 
    #CRTT
    if entry.zmass <= 76 or entry.zmass >= 106: continue
    #if entry.zmass > 76 and entry.zmass < 106: continue

    #CRDY
    #if entry.hmass1 <= 90 or entry.hmass1 >= 150: continue
    if entry.hmass1 > 90 and entry.hmass1 < 150: continue

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

    
    output = reader.EvaluateMVA(methodName)
    if output > 0.61: 
        hDY_2j.Fill(output)
        hhmt.Fill(entry.hhmt)
    
        if (ievt%10000)==0 : print 'For tree ', dictOfFiles[bgInputFile_DY_2j], ' event ',ievt,' has btag0=',btag0[0],'and MVA output =', output
        ievt += 1
#    if (ievt > 20000) : break

print 'max for hTT is ', hTT.GetMaximum()
hhmt.Draw()
#ROOT.gPad.Draw()   


# In[74]:


hhmt = ROOT.TH1D("hhmt","hhmt of DY_2j Events",40,200.,600.)

ievt = 0

for entry in bgInputFile_DY_2j.tree: 
    #CRTT
    #if entry.zmass <= 76 or entry.zmass >= 106: continue
    if entry.zmass > 76 and entry.zmass < 106: continue

    #CRDY
    if entry.hmass1 <= 90 or entry.hmass1 >= 150: continue
    #if entry.hmass1 > 90 and entry.hmass1 < 150: continue

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

    
    output = reader.EvaluateMVA(methodName)
    if output > 0.61: 
        hDY_2j.Fill(output)
        hhmt.Fill(entry.hhmt)
    
        if (ievt%10000)==0 : print 'For tree ', dictOfFiles[bgInputFile_DY_2j], ' event ',ievt,' has btag0=',btag0[0],'and MVA output =', output
        ievt += 1
#    if (ievt > 20000) : break

print 'max for hTT is ', hTT.GetMaximum()
hhmt.Draw()
#ROOT.gPad.Draw()   


# In[79]:

fOut = ROOT.TFile.Open('minitree.root', "recreate")                                                                                                                         
hhmt.Write()
fOut.Close()
        


# In[80]:

#get_ipython().system('ls -rtl *mini*')


# In[81]:

# fIn = ROOT.TFile.Open('minitree.root')
# fIn.ls()


# # In[85]:

# hhmt_histo = fIn.Get('hhmt')
# hhmt_histo.Draw()
# ROOT.gPad.Draw()   # WILL NOT BE drawn otherwise!


# # In[ ]:



