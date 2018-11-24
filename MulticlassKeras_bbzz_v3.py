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


from ROOT import TMVA, TFile, TTree, TCut, gROOT
from os.path import isfile




nBDTTrees = 50# for debug
useWeights = True
doBDT = True
bazingaPrinting = True
doDGtransform = False #decorrelation and gaussian transformation                          



from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.regularizers import l2
from keras import initializers
#from keras import initializations
from keras.optimizers import SGD

# Setup TMVA
TMVA.Tools.Instance()
#TMVA.PyMethodBase.PyInitialize()

output = TFile.Open('TMVA_bbzz_v3.root', 'RECREATE')
factory = TMVA.Factory('TMVAMulticlass_keras', output,#'TMVAClassification', output,
    '!V:!Silent:Color:DrawProgressBar:Transformations=D,G:AnalysisType=multiclass')


sigFile = TFile.Open('BulkGraviton_M900_minitree.root')
bgFile_TT = TFile.Open('TT_Tune_minitree.root')
bgFile_DY1j = TFile.Open('DY1JetsToLL_M50_minitree.root')
bgFile_DY2j = TFile.Open('DY2JetsToLL_M50_minitree.root')
bgFile_DY3j = TFile.Open('DY3JetsToLL_M50_minitree.root')
bgFile_DY4j = TFile.Open('DY4JetsToLL_M50_minitree.root')

samples = [sigFile, bgFile_TT, bgFile_DY1j, bgFile_DY2j, bgFile_DY3j, bgFile_DY4j]
signal_900GeV = sigFile.Get('tree')
background_TT = bgFile_TT.Get('tree')
background_DY_1j = bgFile_DY1j.Get('tree')
background_DY_2j = bgFile_DY2j.Get('tree')
background_DY_3j = bgFile_DY3j.Get('tree')
background_DY_4j = bgFile_DY4j.Get('tree')


variables = ['hmt0', 'hhmt', 'dR_bjets', 'zpt0', 'hpt0', 'hpt1', 'zhmass', 'min_mt2_blmet']


dataloader = TMVA.DataLoader('dataset')
for var in variables:#in signal.GetListOfBranches():
    dataloader.AddVariable(var)#branch.GetName())

#dataloader.AddSpectator('evWgt') #????????
# 36046+33590+22966 +2424 = 95026

trees = {
    signal_900GeV: 'Signal_900GeV',
    background_TT: 'Background_TT',
    background_DY_1j: 'Background_DY_1j',
    background_DY_2j: 'Background_DY_2j',
    background_DY_3j: 'Background_DY_3j',
    background_DY_4j: 'Background_DY_4j'
    }

for k, v in trees.items():
    print 'here we are loading trees for ', v
    dataloader.AddTree(k, v)
    if useWeights:
        dataloader.SetWeightExpression('xsec/countWeighted', v)   
# dataloader.AddTree(signal, 'Signal')
# dataloader.AddTree(background0, 'Background_0')
# dataloader.AddTree(background1, 'Background_1')
# dataloader.AddTree(background2, 'Background_2')
nTrees = len(trees)
print 'nTrees is ', nTrees

dataloader.PrepareTrainingAndTestTree(TCut(''),
        'SplitMode=Random:NormMode=NumEvents:!V')

 
    #dataloader.SetSignalWeightExpression('evWgt')
    #dataloader.SetBackgroundWeightExpression('evWgt')
# Generate model

# Define initialization
def normal(shape, name=None):
    #return initializations.normal(shape, scale=0.05, name=name)
    return initializers.normal(shape, scale=0.05, name=name)
# #
# # NO// Copied from tmvaglob.C
# void NormalizeHists( TH1* sig, TH1* bkg )
# {
#     if (sig->GetSumw2N() == 0) sig->Sumw2();
#     if (bkg->GetSumw2N() == 0) bkg->Sumw2();

#     if (sig->GetSumOfWeights()!=0) {
#         Float_t dx = (sig->GetXaxis()->GetXmax() - sig->GetXaxis()->GetXmin())/sig->GetNbinsX();
#         sig->Scale( 1.0/sig->GetSumOfWeights()/dx );
#     }
#     if (bkg->GetSumOfWeights()!=0) {
#         Float_t dx = (bkg->GetXaxis()->GetXmax() - bkg->GetXaxis()->GetXmin())/bkg->GetNbinsX();
#         bkg->Scale( 1.0/bkg->GetSumOfWeights()/dx );
#     }
# }
# https://github.com/degrutto/VHbbUF/blob/master/run2/TrainBDT.C

# #

# Define model
model = Sequential()
model.add(Dense(12, init="normal", activation='relu', W_regularizer=l2(1e-5), input_dim=len(variables)))
#model.add(Dense(2, init="normal", activation='softmax'))
#model.add(Dense(1, init="normal", activation='softmax'))
# can have any number of inner layers and parameters

fix = nTrees if nTrees==4 else 4#????
model.add(Dense(fix, init="normal", activation='softmax')) 
model.add(Dense(nTrees, init="normal", activation='softmax')) 


# Set loss and optimizer
model.compile(loss='categorical_crossentropy', optimizer=SGD(lr=0.01), metrics=['accuracy',])

# Store model to file
model.save('model.h5')
model.summary()

# Book methods
#factory.BookMethod(dataloader, TMVA.Types.kFisher, 'Fisher',
 #       '!H:!V:Fisher:VarTransform=D,G')


#   export NeuroBayes=/afs/cern.ch/sw/lcg/external/neurobayes_expert/latest/

# factory.BookMethod(dataloader, TMVA.Types.kPyKeras, 
#                    "PyKeras",
#                    #"H:!V:VarTransform=D,G:FilenameModel=model.h5:NumEpochs=20:BatchSize=32"
#                    )


#factory.BookMethod(dataloader, TMVA.Types.kBDT, "BDT",
 #                  "V:NTrees=850:MinNodeSize=2.5%:MaxDepth=3:BoostType=GradBoost=1:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" )

if doBDT:
    factory.BookMethod(dataloader, TMVA.Types.kBDT,
                       "BDT",
                       #"!H:!V:NTrees=850:BoostType=Grad:Shrinkage=0.1:UseBaggedGrad:GradBaggingFraction=0.5:SeparationType=GiniIndex:nCuts=30:NNodesMax=3")
                       "!H:!V:NTrees={0}:BoostType=Grad:Shrinkage=0.1:UseBaggedBoost=True:GradBaggingFraction=0.5:SeparationType=GiniIndex:nCuts=20:MaxDepth=1".format(nBDTTrees))


# Run TMVA
factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()

# score = model.evaluate 
# print 'Test score ', score[0]
# print 'Train score ', score[1]

output.Close()

for s in samples:
    s.Close()
