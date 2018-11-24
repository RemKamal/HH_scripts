#!/usr/bin/env python

from ROOT import TMVA, TFile, TTree, TCut, gROOT
from os.path import isfile

from os import environ
environ['KERAS_BACKEND'] = 'theano'

# Set architecture of system (AVX instruction set is not supported on SWAN)     
environ['THEANO_FLAGS'] = 'gcc.cxxflags=-march=corei7'

useWeights = True
doBDT = True

from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.regularizers import l2
from keras import initializations
from keras.optimizers import SGD

# Setup TMVA
TMVA.Tools.Instance()
TMVA.PyMethodBase.PyInitialize()

output = TFile.Open('TMVA_bbzz.root', 'RECREATE')
factory = TMVA.Factory('TMVAClassification', output,
    '!V:!Silent:Color:DrawProgressBar:Transformations=D,G:AnalysisType=multiclass')


sigFile = TFile.Open('BulkGraviton_M900_minitree.root')
bgFile_TT = TFile.Open('TT_Tune_minitree.root')
bgFile_DY2j = TFile.Open('DY2JetsToLL_M50_minitree.root')
bgFile_DY3j = TFile.Open('DY3JetsToLL_M50_minitree.root')

samples = [sigFile, bgFile_TT, bgFile_DY2j, bgFile_DY3j]
signal = sigFile.Get('tree')
background0 = bgFile_TT.Get('tree')
background1 = bgFile_DY2j.Get('tree')
background2 = bgFile_DY3j.Get('tree')

variables = ['zmass', 'hhmt', 'bpt0', 'dPhi_bjets', 'metpt', 'dR_bjets', 'hmt0', 'hmass0', 'dR_leps']


dataloader = TMVA.DataLoader('dataset')
for var in variables:#in signal.GetListOfBranches():
    dataloader.AddVariable(var)#branch.GetName())

dataloader.AddSpectator('evWgt') #????????
# 36046+33590+22966 +2424 = 95026

trees = {
    signal: 'Signal',
    background0: 'Background_0',
    background1: 'Background_1',
    background2: 'Background_2'
    }
for k, v in trees.items():
    print 'here we are loading trees for ', v
    dataloader.AddTree(k, v)
    
# dataloader.AddTree(signal, 'Signal')
# dataloader.AddTree(background0, 'Background_0')
# dataloader.AddTree(background1, 'Background_1')
# dataloader.AddTree(background2, 'Background_2')
nTrees = len(trees)
print 'nTrees is ', nTrees

dataloader.PrepareTrainingAndTestTree(TCut(''),
        'SplitMode=Random:NormMode=NumEvents:!V')

if useWeights:
    for k, v in trees.items():
        print 'here we are loading weights for ', v
        dataloader.SetWeightExpression('evWgt', v)
    #dataloader.SetSignalWeightExpression('evWgt')
    #dataloader.SetBackgroundWeightExpression('evWgt')
# Generate model

# Define initialization
def normal(shape, name=None):
    return initializations.normal(shape, scale=0.05, name=name)

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
model.add(Dense(12, init=normal, activation='relu', W_regularizer=l2(1e-5), input_dim=len(variables)))
#model.add(Dense(2, init=normal, activation='softmax'))
#model.add(Dense(1, init=normal, activation='softmax'))
# can have any number of inner layers and parameters
model.add(Dense(nTrees, init=normal, activation='softmax')) 
fix = nTrees if nTrees==4 else 4#????
model.add(Dense(fix, init=normal, activation='softmax')) 



# Set loss and optimizer
model.compile(loss='categorical_crossentropy', optimizer=SGD(lr=0.01), metrics=['accuracy',])

# Store model to file
model.save('model.h5')
model.summary()

# Book methods
factory.BookMethod(dataloader, TMVA.Types.kFisher, 'Fisher',
        '!H:!V:Fisher:VarTransform=D,G')
factory.BookMethod(dataloader, TMVA.Types.kPyKeras, "PyKeras",
        'H:!V:VarTransform=D,G:FilenameModel=model.h5:NumEpochs=5:BatchSize=32')

#factory.BookMethod(dataloader, TMVA.Types.kBDT, "BDT",
 #                  "V:NTrees=850:MinNodeSize=2.5%:MaxDepth=3:BoostType=GradBoost=1:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" )

if doBDT:
    factory.BookMethod(dataloader, TMVA.Types.kBDT,
                       "BDTG",
                       "!H:!V:NTrees=50:BoostType=Grad:Shrinkage=0.1:UseBaggedGrad:GradBaggingFraction=0.5:SeparationType=GiniIndex:nCuts=30:NNodesMax=3"
                       )


# Run TMVA
factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()

for s in samples:
    s.Close()
