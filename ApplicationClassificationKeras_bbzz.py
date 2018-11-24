#!/usr/bin/env python

from ROOT import TMVA, TFile, TString
from array import array
from os.path import isfile
import os

from os import environ
environ['KERAS_BACKEND'] = 'theano'

# Set architecture of system (AVX instruction set is not supported on SWAN)    \
                                                                                
environ['THEANO_FLAGS'] = 'gcc.cxxflags=-march=corei7'

# Setup TMVA
TMVA.Tools.Instance()
TMVA.PyMethodBase.PyInitialize()
reader = TMVA.Reader("Color:!Silent")

sigFile = TFile.Open('BulkGraviton_M900_minitree.root')
bgFile_TT = TFile.Open('TT_Tune_minitree.root')
bgFile_DY2j = TFile.Open('DY2JetsToLL_M50_minitree.root')
bgFile_DY3j = TFile.Open('DY3JetsToLL_M50_minitree.root')

samples = [sigFile, bgFile_TT, bgFile_DY2j, bgFile_DY3j]
signal = sigFile.Get('tree')
background0 = bgFile_TT.Get('tree')
background1 = bgFile_DY2j.Get('tree')
background2 = bgFile_DY3j.Get('tree')



zmass = array('f',[0])
hhmt = array('f',[0])
bpt0 = array('f',[0])
dPhi_bjets = array('f',[0])
metpt = array('f',[0])
dR_bjets = array('f',[0])
hmt0 = array('f',[0])
hmass0 = array('f',[0])
dR_leps = array('f',[0])

evWgt = array('f',[0])
countWeighted = array('f',[0])
xsec = array('f',[0])
genvbosonpdgid = array('f',[0])

# variables = {zmass: 'zmass', 
#              hhmt: 'hhmt', 
#              bpt0: 'bpt0', 
#              dPhi_bjets: 'dPhi_bjets',
#              metpt: 'metpt', 
#              dR_bjets: 'dR_bjets', 
#              hmt0:  'hmt0', 
#              hmass0: 'hmass0', 
#              dR_leps: 'dR_leps'
#              }

# spectators = {evWgt: 'evWgt', 
#               countWeighted: 'countWeighted', 
#               xsec: 'xsec', 
#               genvbosonpdgid: 'genvbosonpdgid'
#               }

#add variables 
#for adr, name in variables.items():
 #   print 'name = {0}, adr = {1}'.format(name, adr)
  #  reader.AddVariable(name, adr)
    

reader.AddVariable("zmass", zmass)
reader.AddVariable("hhmt", hhmt)
reader.AddVariable("bpt0", bpt0)
reader.AddVariable("dPhi_bjets", dPhi_bjets)
reader.AddVariable("metpt", metpt)
reader.AddVariable("dR_bjets", dR_bjets)
reader.AddVariable("hmt0", hmt0)
reader.AddVariable("hmass0", hmass0)
reader.AddVariable("dR_leps", dR_leps)

reader.AddSpectator("evWgt", evWgt)
    # reader.AddSpectator("countWeighted", countWeighted)
    # reader.AddSpectator("xsec", xsec)
    # reader.AddSpectator("genvbosonpdgid", genvbosonpdgid)


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
    background0.GetEntry(i)
    background1.GetEntry(i)
    background2.GetEntry(i)
    print(reader.EvaluateMVA('PyKeras'))
