#!/usr/bin/env python

from ROOT import TMVA, TFile, TString
from array import array
from subprocess import call
from os.path import isfile

from os import environ
environ['KERAS_BACKEND'] = 'theano'

# Set architecture of system (AVX instruction set is not supported on SWAN)    \
                                                                                
environ['THEANO_FLAGS'] = 'gcc.cxxflags=-march=corei7'




# Setup TMVA
TMVA.Tools.Instance()
TMVA.PyMethodBase.PyInitialize()
reader = TMVA.Reader("Color:!Silent")

# Load data
if not isfile('tmva_class_example.root'):
    call(['curl', '-O', 'http://root.cern.ch/files/tmva_class_example.root'])

data = TFile.Open('tmva_class_example.root')
signal = data.Get('TreeS')
background = data.Get('TreeB')

branches = {}
for branch in signal.GetListOfBranches():
    branchName = branch.GetName()
    branches[branchName] = array('f', [-999])
    reader.AddVariable(branchName, branches[branchName])
    signal.SetBranchAddress(branchName, branches[branchName])
    background.SetBranchAddress(branchName, branches[branchName])

# Book methods
reader.BookMVA('PyKeras', TString('dataset/weights/TMVAClassification_PyKeras.weights.xml'))

# Print some example classifications
print('Some signal example classifications:')
for i in range(20):
    signal.GetEntry(i)
    print(reader.EvaluateMVA('PyKeras'))
print('')

print('Some background example classifications:')
for i in range(20):
    background.GetEntry(i)
    print(reader.EvaluateMVA('PyKeras'))