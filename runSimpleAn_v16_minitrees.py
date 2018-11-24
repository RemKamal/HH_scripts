#!/usr/bin/env python

from rootpy.tree import Tree, TreeModel
from rootpy.tree import IntCol, FloatCol, FloatArrayCol
from rootpy.io import root_open
import inspect


import optparse
import os, io # f@cking Python 2.X
import sys
import json
import pickle
import ROOT
from subprocess import Popen, PIPE
from functools import partial
import pickle 
import time
from math import sqrt as sqroot
from math import cos as cosine

from ROOT import TLorentzVector
#from getHHMass_rk import computeHHMass # def computeHHMass(leps, met, bjets)
from operator import itemgetter, attrgetter, methodcaller

# to set CMS Pub style, use personal modified version instead
#sys.path.append('/afs/cern.ch/user/r/rkamalie/workspace/private/tdr-style')
#import tdrstyle
#import copy

# to open image from the directory using Python
#from PIL import Image                                                    
#import matplotlib.pyplot as plt 
#import matplotlib.image as mpimg                     

# for test execution w/o json files of samples
inGlobalFile="/afs/cern.ch/user/r/rkamalie/workspace/public/HHtree_from_Loop_4copy.root"

# to enable cProfiler, uncomment the decorator above the def main()


#several debug functions                                                              

debugRun = False # for quick runs with debugFractionOfEvents
debugFractionOfEvents = 1./5 #*1./5 additionally for BG

debugMode = False # for priting with bazinga
def bazinga (mes):
    if debugMode:
        print mes


def whoami():
    return inspect.stack()[1][3]

def whoisdaddy():
    return inspect.stack()[2][3]

def printme():
    print "Calling within the fcn '{me}', caller fcn is '{dad}'".format( me=whoami(), dad=whoisdaddy()) 

import cProfile

def do_cprofile(func):
    def profiled_func(*args, **kwargs):
        profile = cProfile.Profile()
        try:
            profile.enable()
            result = func(*args, **kwargs)
            profile.disable()
            return result
        finally:
            profile.print_stats()
    return profiled_func


if "mt2_bisect_cc.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gROOT.LoadMacro("/afs/cern.ch/user/c/cheidegg/public/mT2code/mt2_bisect.cc")

from ROOT import mt2_bisect
import array
## mt2 from:
#https://github.com/CERN-PH-CMG/cmgtools-lite/blob/80X/TTHAnalysis/python/tools/leptonBuilderEWK.py#L431
#and
#https://github.com/CERN-PH-CMG/cmg-cmssw/blob/heppy_80X/PhysicsTools/Heppy/src/Davismt2.cc#L25
def mt_cosine(pt1, pt2, phi1, phi2):
        return sqroot(2*pt1*pt2*(1-cosine(phi1-phi2)))

def mt2(mt2maker, obj1, obj2, met, useGenMet = False):
    
    vector_met     = array.array('d', [0, met.Px(), met.Py()])
    vector_obj1    = array.array('d', [obj1.M(), obj1.Px(), obj1.Py()])
    vector_obj2    = array.array('d', [obj2.M(), obj2.Px(), obj2.Py()])

    if useGenMet:
        vector_met = array.array('d', [0, self.metgen[var]*cos(self.metgenphi[var]), self.metgen[var]*sin(self.metgenphi[var])])

    mt2maker.set_momenta(vector_obj1, vector_obj2, vector_met)
    mt2maker.set_mn(0)

    return mt2maker.get_mt2()

# define the model
class Event(TreeModel):
    btag0 = FloatCol()
    bpt0 = FloatCol()
    beta0 = FloatCol()
    bphi0 = FloatCol()
    
    leppt0 = FloatCol()
    lepeta0 = FloatCol()
    lepphi0 = FloatCol()
    
    btag1 = FloatCol()
    bpt1 = FloatCol()
    beta1 = FloatCol()
    bphi1 = FloatCol()

    leppt1 = FloatCol()
    lepeta1 = FloatCol()
    lepphi1 = FloatCol()

    zmass = FloatCol()
    zpt0 = FloatCol()
    zeta0 = FloatCol()
    zphi0 = FloatCol()
    
    #hToZZ
    hpt0 = FloatCol()
    heta0 = FloatCol()
    hphi0 = FloatCol()
    hmass0 = FloatCol()
    hmt0 = FloatCol()
    hToZZ_mt_cosine = FloatCol()

    #Htobb
    hpt1 = FloatCol()
    heta1 = FloatCol()
    hphi1 = FloatCol()
    hmass1 = FloatCol()
    hmt1 = FloatCol()


    metpt = FloatCol()
    meteta = FloatCol()
    metphi = FloatCol()

    nleps = IntCol()
    nbjets = IntCol()
    nloosebjets = IntCol()
    njets = IntCol()

    dEta_lb_min = FloatCol()
    dEta_ZH = FloatCol()
    dEta_bjets = FloatCol()
    dEta_leps = FloatCol()

    dR_lb_min = FloatCol()
    dR_ZH = FloatCol()
    dR_bjets = FloatCol()
    dR_leps = FloatCol()

    dPhi_lb_min = FloatCol()
    dPhi_ZH = FloatCol()
    dPhi_bjets = FloatCol()
    dPhi_leps = FloatCol()

    hhmt = FloatCol()
    hh_mt_cosine = FloatCol()

    zhmass = FloatCol()
    zhpt = FloatCol()
    zheta = FloatCol()
    zhphi = FloatCol()
    
    mt2_llmet = FloatCol()
    mt2_b1l1b2l2met = FloatCol()
    mt2_b1l2b2l1met = FloatCol()
    mt2_bbmet = FloatCol()
    mt2_ZHmet = FloatCol()
    min_mt2_blmet = FloatCol()


    # btagWeightCSV_up_lf = FloatCol()
    # btagWeightCSV_up_lfstats1 = FloatCol()
    # btagWeightCSV_up_lfstats2 = FloatCol()

    # btagWeightCSV_up_hf = FloatCol()
    # btagWeightCSV_up_hfstats1 = FloatCol()
    # btagWeightCSV_up_hfstats2 = FloatCol()

    # btagWeightCSV_down_lf = FloatCol()
    # btagWeightCSV_down_lfstats1 = FloatCol()
    # btagWeightCSV_down_lfstats2 = FloatCol()

    # btagWeightCSV_down_hf = FloatCol()
    # btagWeightCSV_down_hfstats1 = FloatCol()
    # btagWeightCSV_down_hfstats2 = FloatCol()

    genvbosonpdgid = IntCol()
    evWgt = FloatCol()
    xsec = FloatCol()
    countWeighted = FloatCol()
    
    bdtOutput = FloatCol()
    #bdtOutput_multiclass = FloatCol()
    #dnnOutput = FloatCol()
    
    #num_vals = IntCol()
    #### variable-length array
    #vals = FloatArrayCol(5, length_name='num_vals')




"""
Perform the analysis on a single file
"""
def runSimplestAn(inFileURLorList, outFileURL, xsec=None, denominator=None, isSignal = False, splitSignal = None, whichChannel = 0, physRegion = None, passLoose = False):

    outFileName = "_minitree.root" if passLoose else "_histograms.root"
    fO = root_open(outFileURL + outFileName, "recreate")
    minitree = Tree("tree", model=Event)

    if passLoose:
        print 'will "SaveTrees"'
    else:
        print 'will "DoCuts"'
        

    bazinga('before list of binLabels')
    bazinga('analyzing region: ')
    bazinga(physRegion)

    binLabels = ['no cut', 'V pdgId', 'ele or mu channel', 'trigger', '>=2b-jets', '90<Hbb<150',  '2leps', '76<Z<106', 'met>20','hhMt>250']
    lastEffBin = len(binLabels)+1
    # book a ton of histograms
    histos={
        'dEta_lb_min'       :ROOT.TH1F('dEta_lb_min', ';|#Delta#eta|_{min}(l, b); Events', 20, 0, 5),
        'dEta_ZH'       :ROOT.TH1F('dEta_ZH', ';|#Delta#eta|(Z_{ll}, H_{bb}); Events', 20, 0, 5),
        'dEta_bjets'       :ROOT.TH1F('dEta_bjets', ';|#Delta#eta|(b_{1}, b_{2}); Events', 20, 0, 5),
        'dEta_leps'       :ROOT.TH1F('dEta_leps', ';|#Delta#eta|(l_{1}, l_{2}); Events', 20, 0, 5),

        'dPhi_lb_min'       :ROOT.TH1F('dPhi_lb_min', ';|#Delta#phi|_{min}(l, b); Events', 20, 0, 5),
        'dPhi_ZH'       :ROOT.TH1F('dPhi_ZH', ';|#Delta#phi|(Z_{ll}, H_{bb}); Events', 20, 0, 5),
        'dPhi_bjets'       :ROOT.TH1F('dPhi_bjets', ';|#Delta#phi|(b_{1}, b_{2}); Events', 20, 0, 5),
        'dPhi_leps'       :ROOT.TH1F('dPhi_leps', ';|#Delta#phi|(l_{1}, l_{2}); Events', 20, 0, 5),
        
        'dR_lb_min'       :ROOT.TH1F('dR_lb_min', ';#DeltaR_{min}(l, b); Events', 20, 0, 8),
        'dR_ZH'       :ROOT.TH1F('dR_ZH', ';#DeltaR(Z_{ll}, H_{bb}); Events', 20, 0, 8),
        'dR_bjets'       :ROOT.TH1F('dR_bjets', ';#DeltaR(b_{1}, b_{2}); Events', 20, 0, 8),
        'dR_leps'       :ROOT.TH1F('dR_leps', ';#DeltaR(l_{1}, l_{2}); Events', 20, 0, 8),
        # book analysis independent histograms
        #*************************************
        'cutFlow'       :ROOT.TH1F('cutFlow', ';; Events', lastEffBin-1, 1, lastEffBin),
        'cutFlowEff'       :ROOT.TH1F('cutFlowEff', ';; Efficiency, %', lastEffBin-1, 1, lastEffBin),
        
        'nbjets_raw':ROOT.TH1F('nbjets_raw'	,';b-jet multiplicity; Events'				, 7,0,7),
        'metpt_raw'     :ROOT.TH1F('metpt_raw'      ,';MET [GeV]; Events'                , 35,0,350),
        'njets_raw'	:ROOT.TH1F('njets_raw'	,';Jet multiplicity; Events'				, 9,0,9),
        'nleps_raw'		:ROOT.TH1F('nleps_raw'		,';Lepton multiplicity; Events'				, 3,1,4),
        # #   book histograms for HH specific signature of 2b, 2l, 2nu(met)
        # #****************************************************************
        'metpt'     :ROOT.TH1F('metpt'      ,';MET [GeV]; Events'                , 35,0,350),
        'nleps'		:ROOT.TH1F('nleps'		,';Lepton multiplicity; Events'				, 3,1,4),
        'bjetpt'    :ROOT.TH1F('bjetpt'     ,';p_{T}(b jet) [GeV]; Events'              , 35,0,350),
        'bjeteta'   :ROOT.TH1F('bjeteta'    ,';#eta(b jet); Events'                     , 20,-2.4,2.4),
        'leppt'     :ROOT.TH1F('leppt'      ,';p_{T}(lepton) [GeV]; Events'             , 25,0,250),
        'lepeta'    :ROOT.TH1F('lepeta'     ,';#eta(lepton); Events'                    , 20,-2.4,2.4),
        'bjet0pt'	:ROOT.TH1F('bjet0pt'	,';Leading b-Jet p_{T} [GeV]; Events'	    , 35, 0., 350.),
        'bjet1pt'	:ROOT.TH1F('bjet1pt'	,';Subleading b-Jet p_{T} [GeV]; Events'	, 25, 0., 250.),
        'bjet0eta'	:ROOT.TH1F('bjet0eta'	,';Leading b-Jet #eta; Events'				, 20, -2.4, 2.4),
        'bjet1eta'	:ROOT.TH1F('bjet1eta'	,';Subleading b-Jet #eta; Events'			, 20, -2.4, 2.4),
        'btagCSV0'       :ROOT.TH1F('btagCSV0'	,';Leading b-Jet CSV SF; Events'	    , 60, 0.4, 1.),
        'btagCSV1'       :ROOT.TH1F('btagCSV1'	,';Subleading b-Jet CSV SF; Events'	    , 60, 0.4, 1.),
        'lep0pt'	:ROOT.TH1F('lep0pt'		,';Leading Lepton p_{T} [GeV]; Events'		, 25, 0., 250.),
        'lep1pt'	:ROOT.TH1F('lep1pt'		,';Subleading Lepton p_{T} [GeV]; Events'	, 20, 0., 200.),
        'lep0eta'	:ROOT.TH1F('lep0eta'	,';Leading Lepton #eta ; Events'		    , 20, -2.4, 2.4),
        'lep1eta'	:ROOT.TH1F('lep1eta'	,';Subleading Lepton #eta ; Events'	        , 20, -2.4, 2.4),
        'hCSVmass'      :ROOT.TH1F('hCSVmass', ';HCSV mass [GeV]; Events', 40, 85, 165),
        'hCSVmass_long'      :ROOT.TH1F('hCSVmass_long', ';HCSV mass [GeV]; Events', 45, 30, 220),
        'hCSVpt'      :ROOT.TH1F('hCSVpt', ';HCSV p_{T} [GeV]; Events', 50, 0, 400),
        'hZZpt'      :ROOT.TH1F('hZZpt', ';H#rightarrowZZ p_{T} [GeV]; Events', 50, 0, 400),
        'hZZmt'      :ROOT.TH1F('hZZmt', ';H#rightarrowZZ transverse mass [GeV]; Events', 40, 50, 450),
        'hZZmt_long'      :ROOT.TH1F('hZZmt_long', ';H#rightarrowZZ transverse mass [GeV]; Events', 100, 50, 1050),
        # the name of hist below reflects the fact of unimportance of signal sample for some studies 
        'hhMt'      :ROOT.TH1F('hhMt', ';"HiggsHiggson" transverse mass [GeV]; Events', 40, 550, 950),
        'hhMt_long'      :ROOT.TH1F('hhMt_long', ';"HiggsHiggson" transverse mass [GeV]; Events', 90, 200, 1100),
        'zMass'      :ROOT.TH1F('zMass', ';Z mass [GeV]; Events', 20, 70, 110),
        'zHMass'      :ROOT.TH1F('zHMass', ';ZH mass [GeV]; Events', 50, 115, 315),
        'zHTransMass'      :ROOT.TH1F('zHTransMass', ';ZH transverse mass [GeV]; Events', 50, 115, 315),
        'zMass_long'      :ROOT.TH1F('zMass_long', ';Z mass [GeV]; Events', 50, 20, 220),
        'zPt'      :ROOT.TH1F('zPt', ';Z p_{T} [GeV]; Events', 50, 0, 300),


        'dEta_lb_min_beforeMETcut'       :ROOT.TH1F('dEta_lb_min_beforeMETcut', ';|#Delta#eta|_{min}(l, b); Events', 20, 0, 5),
        'dEta_ZH_beforeMETcut'       :ROOT.TH1F('dEta_ZH_beforeMETcut', ';|#Delta#eta|(Z_{ll}, H_{bb}); Events', 20, 0, 5),
        'dEta_bjets_beforeMETcut'       :ROOT.TH1F('dEta_bjets_beforeMETcut', ';|#Delta#eta|(b_{1}, b_{2}); Events', 20, 0, 5),
        'dEta_leps_beforeMETcut'       :ROOT.TH1F('dEta_leps_beforeMETcut', ';|#Delta#eta|(l_{1}, l_{2}); Events', 20, 0, 5),

        'dPhi_lb_min_beforeMETcut'       :ROOT.TH1F('dPhi_lb_min_beforeMETcut', ';|#Delta#phi|_{min}(l, b); Events', 20, 0, 5),
        'dPhi_ZH_beforeMETcut'       :ROOT.TH1F('dPhi_ZH_beforeMETcut', ';|#Delta#phi|(Z_{ll}, H_{bb}); Events', 20, 0, 5),
        'dPhi_bjets_beforeMETcut'       :ROOT.TH1F('dPhi_bjets_beforeMETcut', ';|#Delta#phi|(b_{1}, b_{2}); Events', 20, 0, 5),
        'dPhi_leps_beforeMETcut'       :ROOT.TH1F('dPhi_leps_beforeMETcut', ';|#Delta#phi|(l_{1}, l_{2}); Events', 20, 0, 5),
        
        'dR_lb_min_beforeMETcut'       :ROOT.TH1F('dR_lb_min_beforeMETcut', ';#DeltaR_{min}(l, b); Events', 20, 0, 8),
        'dR_ZH_beforeMETcut'       :ROOT.TH1F('dR_ZH_beforeMETcut', ';#DeltaR(Z_{ll}, H_{bb}); Events', 20, 0, 8),
        'dR_bjets_beforeMETcut'       :ROOT.TH1F('dR_bjets_beforeMETcut', ';#DeltaR(b_{1}, b_{2}); Events', 20, 0, 8),
        'dR_leps_beforeMETcut'       :ROOT.TH1F('dR_leps_beforeMETcut', ';#DeltaR(l_{1}, l_{2}); Events', 20, 0, 8),


        'metpt_beforeMETcut'     :ROOT.TH1F('metpt_beforeMETcut'      ,';MET [GeV]; Events'                , 35,0,350),
        'nleps_beforeMETcut'		:ROOT.TH1F('nleps_beforeMETcut'		,';Lepton multiplicity; Events'				, 3,1,4),
        'bjetpt_beforeMETcut'    :ROOT.TH1F('bjetpt_beforeMETcut'     ,';p_{T}(b jet) [GeV]; Events'              , 35,0,350),
        'bjeteta_beforeMETcut'   :ROOT.TH1F('bjeteta_beforeMETcut'    ,';#eta(b jet); Events'                     , 20,-2.4,2.4),
        'leppt_beforeMETcut'     :ROOT.TH1F('leppt_beforeMETcut'      ,';p_{T}(lepton) [GeV]; Events'             , 25,0,250),
        'lepeta_beforeMETcut'    :ROOT.TH1F('lepeta_beforeMETcut'     ,';#eta(lepton); Events'                    , 20,-2.4,2.4),
        'bjet0pt_beforeMETcut'	:ROOT.TH1F('bjet0pt_beforeMETcut'	,';Leading b-Jet p_{T} [GeV]; Events'	    , 35, 0., 350.),
        'bjet1pt_beforeMETcut'	:ROOT.TH1F('bjet1pt_beforeMETcut'	,';Subleading b-Jet p_{T} [GeV]; Events'	, 25, 0., 250.),
        'bjet0eta_beforeMETcut'	:ROOT.TH1F('bjet0eta_beforeMETcut'	,';Leading b-Jet #eta; Events'				, 20, -2.4, 2.4),
        'bjet1eta_beforeMETcut'	:ROOT.TH1F('bjet1eta_beforeMETcut'	,';Subleading b-Jet #eta; Events'			, 20, -2.4, 2.4),
        'btagCSV0_beforeMETcut'       :ROOT.TH1F('btagCSV0_beforeMETcut'	,';Leading b-Jet CSV SF; Events'	    , 60, 0.4, 1.),
        'btagCSV1_beforeMETcut'       :ROOT.TH1F('btagCSV1_beforeMETcut'	,';Subleading b-Jet CSV SFt; Events'	    , 60, 0.4, 1.),
        'lep0pt_beforeMETcut'	:ROOT.TH1F('lep0pt_beforeMETcut'		,';Leading Lepton p_{T} [GeV]; Events'		, 25, 0., 250.),
        'lep1pt_beforeMETcut'	:ROOT.TH1F('lep1pt_beforeMETcut'		,';Subleading Lepton p_{T} [GeV]; Events'	, 20, 0., 200.),
        'lep0eta_beforeMETcut'	:ROOT.TH1F('lep0eta_beforeMETcut'	,';Leading Lepton #eta ; Events'		    , 20, -2.4, 2.4),
        'lep1eta_beforeMETcut'	:ROOT.TH1F('lep1eta_beforeMETcut'	,';Subleading Lepton #eta ; Events'	        , 20, -2.4, 2.4),
        'hCSVmass_beforeMETcut'      :ROOT.TH1F('hCSVmass_beforeMETcut', ';HCSV mass [GeV]; Events', 40, 85, 165),
        'hCSVmass_long_beforeMETcut'      :ROOT.TH1F('hCSVmass_long_beforeMETcut', ';HCSV mass [GeV]; Events', 45, 30, 220),
        'hCSVpt_beforeMETcut'      :ROOT.TH1F('hCSVpt_beforeMETcut', ';HCSV p_{T} [GeV]; Events', 50, 0, 400),
        'hZZpt_beforeMETcut'      :ROOT.TH1F('hZZpt_beforeMETcut', ';H#rightarrowZZ p_{T} [GeV]; Events', 50, 0, 400),
        'hZZmt_beforeMETcut'      :ROOT.TH1F('hZZmt_beforeMETcut', ';H#rightarrowZZ transverse mass [GeV]; Events', 40, 50, 450),
        'hZZmt_long_beforeMETcut'      :ROOT.TH1F('hZZmt_long_beforeMETcut', ';H#rightarrowZZ transverse mass [GeV]; Events', 100, 50, 1050),
        # the name of hist below reflects the fact of unimportance of signal sample for some studies 
        'hhMt_beforeMETcut'      :ROOT.TH1F('hhMt_beforeMETcut', ';"HiggsHiggson" transverse mass [GeV]; Events', 40, 550, 950),
        'hhMt_long_beforeMETcut'      :ROOT.TH1F('hhMt_long_beforeMETcut', ';"HiggsHiggson" transverse mass [GeV]; Events', 90, 200, 1100),
        'zMass_beforeMETcut'      :ROOT.TH1F('zMass_beforeMETcut', ';Z mass [GeV]; Events', 20, 70, 110),
        'zHMass_beforeMETcut'      :ROOT.TH1F('zHMass_beforeMETcut', ';ZH mass [GeV]; Events', 50, 115, 315),
        'zHTransMass_beforeMETcut'      :ROOT.TH1F('zHTransMass_beforeMETcut', ';ZH transverse mass [GeV]; Events', 50, 115, 315),
        'zMass_long_beforeMETcut'      :ROOT.TH1F('zMass_long_beforeMETcut', ';Z mass [GeV]; Events', 50, 20, 220),
        'zPt_beforeMETcut'      :ROOT.TH1F('zPt_beforeMETcut', ';Z p_{T} [GeV]; Events', 50, 0, 300),

        'mt2_llmet_beforeMETCut' :ROOT.TH1F('mt2_llmet_beforeMETCut', ';l_{1}l_{2}met mt2[GeV]; Events', 50, 0, 300),
        'mt2_b1l1b2l2met_beforeMETCut':ROOT.TH1F('mt2_b1l1b2l2met_beforeMETCut', ';b_{1}l_{1}b_{2}l_{2}met mt2 [GeV]; Events', 50, 0, 300),
        'mt2_b1l2b2l1met_beforeMETCut':ROOT.TH1F('mt2_b1l2b2l1met_beforeMETCut', ';b_{1}l_{2}b_{2}l_{1}met mt2 [GeV]; Events', 50, 0, 300),
        'mt2_bbmet_beforeMETCut':ROOT.TH1F('mt2_bbmet_beforeMETCut', ';b_{1}b_{2}met mt2[GeV]; Events', 50, 0, 300),
        'mt2_ZHmet_beforeMETCut':ROOT.TH1F('mt2_ZHmet_beforeMETCut', ';ZHmet mt2[GeV]; Events', 100, 0, 1000),
        'min_mt2_blmet_beforeMETCut':ROOT.TH1F('min_mt2_blmet_beforeMETCut', ';blmet mt2 [GeV]; Events', 50, 0, 300),

 
        'mt2_llmet' :ROOT.TH1F('mt2_llmet', ';l_{1}l_{2}met mt2[GeV]; Events', 50, 0, 300),
        'mt2_b1l1b2l2met':ROOT.TH1F('mt2_b1l1b2l2met', ';b_{1}l_{1}b_{2}l_{2}met mt2 [GeV]; Events', 50, 0, 300),
        'mt2_b1l2b2l1met':ROOT.TH1F('mt2_b1l2b2l1met', ';b_{1}l_{2}b_{2}l_{1}met mt2 [GeV]; Events', 50, 0, 300),
        'mt2_bbmet':ROOT.TH1F('mt2_bbmet', ';b_{1}b_{2}met mt2[GeV]; Events', 50, 0, 300),
        'mt2_ZHmet':ROOT.TH1F('mt2_ZHmet', ';ZHmet mt2[GeV]; Events', 100, 0, 1000),
        'min_mt2_blmet':ROOT.TH1F('min_mt2_blmet', ';blmet mt2 [GeV]; Events', 50, 0, 300),

        'hh_mt_cosine_beforeMETcut':ROOT.TH1F('hh_mt_cosine_beforeMETcut', ';"HiggsHiggson" transverse mass [GeV]; Events', 50, 10, 1010),
        'hToZZ_mt_cosine_long_beforeMETcut':ROOT.TH1F('hToZZ_mt_cosine_long_beforeMETcut', ';H#rightarrowZZ transverse mass [GeV]; Events', 100, 50, 1050),
        'hToZZ_mt_cosine_beforeMETcut':ROOT.TH1F('hToZZ_mt_cosine_beforeMETcut', ';H#rightarrowZZ transverse mass [GeV]; Events', 40, 50, 450),


        'hh_mt_cosine':ROOT.TH1F('hh_mt_cosine', ';"HiggsHiggson" transverse mass [GeV]; Events', 50, 10, 1010),
        'hToZZ_mt_cosine_long':ROOT.TH1F('hToZZ_mt_cosine_long', ';H#rightarrowZZ transverse mass [GeV]; Events', 100, 50, 1050),
        'hToZZ_mt_cosine':ROOT.TH1F('hToZZ_mt_cosine', ';H#rightarrowZZ transverse mass [GeV]; Events', 40, 50, 450),


        }
    bazinga('after histos')
    for key in histos:
        histos[key].Sumw2()
        histos[key].SetDirectory(0)



    fIn = None
    tree= None
    ch = None
    fc = None
    listOfFiles = 0
    print 'printing file name ', inFileURLorList
    file_name, file_ext = os.path.splitext(inFileURLorList)
    #print file_ext

    #exp_str = 'X509_USER_PROXY=/afs/cern.ch/user/r/rkamalie/x509up_u27011'
    #print 'option for "call" is ', exp_str 
    
    #import subprocess
    #subprocess.call(['export', exp_str])
    fileName = None
    countWeighted = 0
    count = 0
    HtoZZfactor = 0
    HtoWWfactor = 0
    HtoZZ = 0
    HtoWW = 0
    massIdx = None
    masses = [260, 270, 300, 350, 400, 450, 600, 650, 900, 1000]

    # zz is norm to 5000 pb for low mass and 25000 pb for high mass
    zzFactors = [1472.493815525975, 1796.622349982034, 2801.277382486414, 6074.2270546073005, 10359.259105788755, 19761.283692988694, 5441.436539246361, 8882.966910948257, 40816.32653061225, 70175.43859649122]
    # ww is norm to 400 pb for low mass and 2000 pb for high mass                                      
    wwFactors = [7362.469077629874, 8983.11174991017, 14006.38691243207, 30371.135273036503, 51796.295528943774, 98806.41846494348, 27207.182696231805, 44414.83455474128, 204081.63265306124, 350877.1929824561]

    if file_ext == '.root':
        fIn=ROOT.TFile.Open(inFileURLorList)
        tree=fIn.Get('tree')
        countWeighted=fIn.Get('CountWeighted').GetBinContent(1)
        if isSignal: #fix me for BG samples, after they are skimmed with the new version of the skimming script
            count=fIn.Get('Count').GetBinContent(1)
        print '\n...analysing %s' % inFileURLorList
    elif file_ext == '.txt':
        ch = ROOT.TChain("tree")
        fc = ROOT.TFileCollection("fc","",inFileURLorList)
        ch.AddFileInfoList(fc.GetList())
        tree=ch
        #print '\n', ch, fc, tree
        #print inFileURLorList
        with io.open (inFileURLorList, mode = 'rt', encoding='utf-8') as f:
            #print f
            listOfFiles = list (f.read().split('\n') )[:-1]
            # loop over root files in the list taken from .txt file
            
            for f in xrange (len (listOfFiles)):
                fIn=ROOT.TFile.Open(listOfFiles[f])
                if fIn.IsZombie() or not fIn.IsOpen():    
                    print 'error occurred while reading the file, it happens with EOS, rerun.'
                    exit(1)
                else:
                    fileName = fIn.GetName()
                    # if False: #'GluGlu' in fileName:

                    #     # hToZZ = 1.* tree.Draw("tree.genHiggsDecayMode"," tree.genHiggsDecayMode%1000==23", "goff")
                    #     # hToWW = 1.* tree.Draw("tree.genHiggsDecayMode"," tree.genHiggsDecayMode%1000==24", "goff")

                    #     # HtoZZfactor = hToZZ / (hToZZ + hToWW)
                    #     # HtoWWfactor = hToWW / (hToZZ + hToWW)

                    #     # print 'fileName is ', fileName
                    #     # print 'GluGlu has HtoZZfactor= ', HtoZZfactor
                    #     # print 'GluGlu has HtoWWfactor= ', HtoWWfactor
                    #     print 'fileName is ', fileName
                    #     if '260' in fileName:
                    #         print 'in the ISSUE with', fileName
                    #         hToZZ = 10148.0
                    #         hToWW = 245278.
                    #         massIdx = 0
                    #     elif '270' in fileName:
                    #         hToZZ = 10404.0
                    #         hToWW = 249255.
                    #         massIdx = 1
                    #     elif '300' in fileName:
                    #         hToZZ = 11147.0
                    #         hToWW = 259790.
                    #         massIdx = 2
                    #     elif '350' in fileName:
                    #         hToZZ = 11720.0
                    #         hToWW = 268840.
                    #         massIdx = 3
                    #     elif '400' in fileName:
                    #         hToZZ = 12056.0
                    #         hToWW = 272878.
                    #         massIdx = 4
                    #     elif '450' in fileName:
                    #         hToZZ = 12259.0
                    #         hToWW = 275748.
                    #         massIdx = 5
                    #     elif '600' in fileName:
                    #         hToZZ = 12445.0
                    #         hToWW = 280126.
                    #         massIdx = 6
                    #     elif '650' in fileName:
                    #         hToZZ = 12480.0
                    #         hToWW = 280922.
                    #         massIdx = 7
                    #     elif '900' in fileName:
                    #         hToZZ = 12581.0
                    #         hToWW = 282375.
                    #         massIdx = 8
                    #     elif '1000' in fileName:
                    #         hToZZ = 12328.0
                    #         hToWW = 279826.
                    #         massIdx = 9
                    #     else:
                    #         print 'in the else with', fileName
                    #         print 'cannt happen'
                    #         sys.exit(1)

                    #     if massIdx is None or massIdx < 0 or massIdx > 9:
                    #         print 'problem with massIdx, exiting'
                    #         sys.exit(1)

                    #     if 'Hzz' in splitSignal:
                    #         countWeighted += hToZZ
                    #     elif 'Hww' in splitSignal:
                    #         countWeighted += hToWW
                    #     elif 'No' in splitSignal:
                    #         countWeighted += (hToZZ + hToWW)
                    #     else:  
                    #         print 'cannt happen'
                    #         sys.exit(1)
                    #     print 'doing signal = {0}'.format(fIn)
                    #     print 'splitSignal = {0}'.format(splitSignal)

                    #else:
                    print 'doing = {0}'.format(fIn)
                    print 'fileName is ', fileName
                    countWeighted += fIn.Get('CountWeighted').GetBinContent(1)
                    count += fIn.Get('Count').GetBinContent(1)
                    #             if isSignal: #fix me
    #                count += fIn.Get('Count').GetBinContent(1)
      #          if isSignal: #fix me
     #               print 'File ',fIn, ' has Count equal to ', count
                    print 'File ',fIn, ' has CountWeighted equal to {0} and count to {1}'.format( fIn.Get('CountWeighted').GetBinContent(1), fIn.Get('Count').GetBinContent(1))
            print 
            print '...analysing {0} files in {1} with {2} countWeighted and count {3} events'.format ( len(listOfFiles), inFileURLorList, countWeighted, count )
            if countWeighted ==0:
                countWeighted = count
            # if 'GluGlu' in fileName:
            #     if 'Hzz' in splitSignal and HtoZZfactor !=0:   
            #         countWeighted *= HtoZZfactor
            #     elif 'Hww' in splitSignal and HtoWWfactor !=0:   
            #         countWeighted *= HtoZZfactor
            # else:
            #     pass
       #     if isSignal:#fix me
        #        print '...analysing {} files in {} with {} Count events'.format ( len(listOfFiles), inFileURLorList, count )
    else:
        print 'something went wrong, bad input file'
        
    if fileName == None:
        print 'fileName is None, exiting...'
        exit(1)

    if 'ata' in fileName:
        print 'For data sample {0} countWeighted taken from COUNT is {1}'.format(fileName, countWeighted)

    if countWeighted == 0:
        print 'Something is wrong with "countWeighted", please check!'
        exit(1)
        
    branchingRatios = [0.0012 #HtoZZ
                       , 0.0266 #HtoWW
                       , 0.02787 #HtoVV
                       ]
    zz = 0
    ww = 1
    vv = 2
    branchingRatio = None

    if 'GluGlu' not in fileName:
        global debugFractionOfEvents
        debugFractionOfEvents *= 1./5
        branchingRatio = 1
    else:
        if 'Hzz' in splitSignal:
            branchingRatio = branchingRatios[zz]
        elif 'Hww' in splitSignal:
            branchingRatio = branchingRatios[ww]
        else:
            branchingRatio = branchingRatios[vv]



    if not branchingRatio:
        print 'smth is wrong with branchingRatio, exiting...'
        sys.exit(1)

    if debugRun:
        countWeighted *= debugFractionOfEvents
 #       if isSignal: #fix me
  #          count *= debugFractionOfEvents


#print 'tree is ', str(tree)
    totalEntries = tree.GetEntries() * debugFractionOfEvents if debugRun else tree.GetEntries() 
    print '\nTotal number of entries is ', totalEntries
    bazinga('before loop over entries')
    start = time.time()

    evWgt=1.0

    per_cent = 0
    start = 0
    fiveJobs = 0
    ninFiveJobs = 0
    bazinga('before loop over entries')
    for i in xrange(0,int(totalEntries)):
                      
        histos['cutFlow'].Fill(1,1) # no cut         
        bazinga('before get entry')
        tree.GetEntry(i)
        bazinga('before v_id')
        v_id = None
        if xsec is None:# or xsec==1.:
            #print 'doing Data'
            pass
        else:  # below is a hack to avoid segm. viol.
            for index in xrange ( 0, len (tree.GenVbosons_pdgId) ):
                v_id = abs ( int ( float(tree.GenVbosons_pdgId[0]) ) )

        if splitSignal == "No":
            #print 'all is fine, go further'
            pass
          
        elif splitSignal == "Hzz":
            #print 'in the Hzz'
            #print 'v_id is ', v_id
#if 'GluGlu' in fileName and HtoZZfactor !=0:
             #   countWeighted *= HtoZZfactor
            #print 'countWeighted in Hzz is ', countWeighted
            if not v_id == 23:
                #print 'before Hzz skip'
                continue    # limit to HtoZZ
        elif splitSignal == "Hww":
            #print '\nin the Hww'
            #print 'v_id is ', v_id
            
            #print 'countWeighted in Hww is ', countWeighted
            if not v_id == 24:
                #print 'before Hww skip'
                continue    # limit to HtoWW
        else:
            print 'smth went wrong splitting the signal'
            print 'v_id is ', v_id 
            print 'splitSignal is ', splitSignal

        histos['cutFlow'].Fill(2,1) # splitSignal
        
        if whichChannel == 0: #muons
            if tree.Vtype != 0: continue
                
        elif whichChannel == 1: #electrons
            if tree.Vtype != 1: continue
        else:
            print 'wrong channel type, only electron or muon are possible, exiting...'
            exit(1)

        histos['cutFlow'].Fill(3,1) # ele or mu channel

        #print 'countWeighted is ', countWeighted
        
        if tree.Vtype == 1: #Int_t OR of ['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*', 'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v*']*
            #if not tree.HLT_ttH_DL_elel: continue
            if not tree.HLT_BIT_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v: continue  
        elif tree.Vtype == 0:
            if not tree.HLT_ttH_DL_mumu: continue #Int_t OR of ['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v*', 'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v*']*
        else:
            continue
            #pass
        histos['cutFlow'].Fill(4,1) #trigger


        if i%100==0 : 
            if xsec is None:# or xsec==1:
                print 'doing Data' 
            if passLoose:
                print 'loose cuts applied, will store vars for BDT'
            else:
                print 'will run analysis cuts and create histograms'

            print 'isSignal, splitSignal are ', isSignal, splitSignal
            print 'xsec is ', xsec
            print 'evWgt is ', evWgt
            print 'countWeighted is ', countWeighted 
            print 'fileName is', fileName
#            if isSignal:
 #               print 'count is ', count
            bazinga ("before 1%")
            per_cent = float(100.*i)/float(totalEntries)
            if int(per_cent) == 5:
                fiveJobs = time.time()
                #print start, fiveJobs
                print 'it takes {:6.2f} seconds to analyse 5 jobs, {:6.2f} seconds remain'. format(fiveJobs-start, (fiveJobs-start)*(float(100-5)/float(5)))
            bazinga ("before 95%")
            if int(per_cent) == 95:
                ninFiveJobs = time.time()
                print 'it took {:6.2f} seconds to analyse 95 jobs, {:6.2f} seconds remain'. format(ninFiveJobs-start, fiveJobs-start)

            sys.stdout.write('\r [ %d/100 ] done' % int(per_cent) )
            print '\n'



        nJets , nBJets, nLooseBJets = 0,0,0
        jetsP4 = []
        looseBJetsListOfTuples = []
        bJetsListOfTuples =[]
        bazinga('before loop for jets')
        # independent loop over jets in the event
        for ij in xrange(0,tree.nJet):

            #get the kinematics and select the jet
            jp4=ROOT.TLorentzVector()
            bjp4=ROOT.TLorentzVector()
            lbjp4=ROOT.TLorentzVector()
            jp4.SetPtEtaPhiM(tree.Jet_pt[ij],tree.Jet_eta[ij],tree.Jet_phi[ij],tree.Jet_mass[ij])
            if jp4.Pt()<30 or ROOT.TMath.Abs(jp4.Eta())>2.4 : continue
            jetsP4.append(jp4)

            #count selected jet
            nJets +=1

            #save P4 for b-tagged jet
            #print 'tree.Jet_btagCSV[ij] is ', tree.Jet_btagCSV[ij]
            if tree.Jet_btagCSV[ij]>= 0.8: # CSV WP Medium, Spring
             #   print 'inside >=0.8'
                nBJets += 1
                bjp4 = jp4
                bJetsListOfTuples.append(( bjp4,tree.Jet_btagCSV[ij]) )
            elif 0.2 < tree.Jet_btagCSV[ij] and tree.Jet_btagCSV[ij] < 0.8:
              #  print 'inside 0.2<...<0.8.'
                nLooseBJets += 1
                lbjp4 = jp4
                looseBJetsListOfTuples.append( (lbjp4,tree.Jet_btagCSV[ij]) )
            else:
                continue #pass
        
        #bJetsP4 = []
        bJetsListOfTuples_tmp = sorted(bJetsListOfTuples, key=itemgetter(1), reverse = True)
        #sortedByCsv
        bJetsP4 = map(itemgetter(0), bJetsListOfTuples_tmp )
        bJetsCSV = map(itemgetter(1), bJetsListOfTuples_tmp )
        looseBJetsListOfTuples_tmp = sorted(looseBJetsListOfTuples, key=itemgetter(1), reverse = True)
        looseBJetsP4_sortedByCsv = map(itemgetter(0), looseBJetsListOfTuples_tmp )
        looseBJetsCSV = map(itemgetter(1), looseBJetsListOfTuples_tmp )

        

        nLeps = 0
        lepsP4 = []
        bazinga('before loop for leptons')
        # independent loop over leptons in the event
        nvLeps = 0
        for emu in xrange(0, tree.nvLeptons):
            nvLeps = tree.nvLeptons
            #print 'inside nvLeptons'
           # if tree.genHiggsDecayMode%10000 == 23:  # work only with HtoZZ decay
           #     if tree.Vtype ==0 or tree.Vtype==1: # limit to Ztoee or Ztomm
                    #save P4 for leptons
            lp4 = ROOT.TLorentzVector()
            lp4.SetPtEtaPhiM(tree.vLeptons_pt[emu],tree.vLeptons_eta[emu],tree.vLeptons_phi[emu],tree.vLeptons_mass[emu])
            # select >  20, 15, 15, 15, .... GeV leptons
            #print 'emu before loop is ', emu
            if emu==0:
                if lp4.Pt()<20:
                    print 'emu is ', emu
                    print 'lp4.Pt() is equal to ', lp4.Pt() 
                    print 'while tree.vLeptons_pt is ', tree.vLeptons_pt[emu]
                #if lp4.Pt()<20:
                    continue #attention, Eta is limited to 2.4
            else:
                if lp4.Pt()<15:
                    #print 'emu is ', emu
                    #print 'lp4.Pt() is equal to ', lp4.Pt() 
                    #print 'while tree.vLeptons_pt is ', tree.vLeptons_pt[emu]
                    #if lp4.Pt()<15: 
                    continue

    
            lepsP4.append(lp4)
            nLeps += 1
        
        #print 'nLeps is ', nLeps
        if nLeps != nvLeps:
                print 'nLeps is {0}, while nvLeps is {1}.'.format ( nLeps, nvLeps )
            #apply WPs from EG POG
            #nGoodLep +=1




        #histos['cutFlow'].Fill(1,1) # no cut         
        bazinga('before njets_raw Fill')



        lumino = 1.       #36800.
        if xsec and countWeighted != 0: 
            #fix me proper usage of selLepEff when two leptons are in the event!
            evWgt = xsec * (lumino / countWeighted) 
            # if 'GluGlu' in fileName:
            #     if 'Hzz' in fileName:
            #         evWgt *= branchingRatio# * zzFactors[massIdx]
            #     elif 'Hww' in fileName:
            #         evWgt *= branchingRatio# * wwFactors[massIdx]
            #     else:
            #         evWgt *= branchingRatio# * wwFactors[massIdx] #use same factor for total sample
            #     print 'For {0} BR is {1}'.format(fileName, branchingRatio)
            if nBJets > 0:
                evWgt *= bJetsCSV[0]
                if nBJets >1 and 'b' not in physRegion:
                    evWgt *= bJetsCSV[1]
                    
                        
                    #apply only one btag CSV SF if it is CR DY with 0 or 1 b-jets

        # fill raw histograms, before any cuts are applied
        # for ANY jet
        histos['njets_raw'].Fill(tree.nJet, evWgt)
        histos['nbjets_raw'].Fill(nBJets, evWgt) # how many remain to be 'good'=loose  b-jets 
        histos['metpt_raw'].Fill(tree.met_pt, evWgt)
        histos['nleps_raw'].Fill(nLeps, evWgt)



        # start HH selection 
        #*******************

        bazinga('asked for b-jets')
        
        if physRegion == "SR" and not passLoose:
            #print 'doing ', physRegion
            if nBJets < 2 : continue  
        elif physRegion == "SR" and passLoose:
            if nBJets < 0 : continue
        elif physRegion == "CRTT":
            #print 'doing ', physRegion
            if nBJets < 2 : continue    
        elif physRegion == "CRDY":
            #print 'doing ', physRegion
            if nBJets < 2 : continue    
        elif physRegion == "CRDY_1b":
            #print 'doing ', physRegion
            if nBJets is not 1: continue    
        elif physRegion == "CRDY_0b":
            #print 'doing ', physRegion
            if nBJets is not 0: continue    
        else:
            #print 'doing ', physRegion
            exit(1)

        histos['cutFlow'].Fill(5, 1) # N of b-jets    


        
        Htobb_p4=ROOT.TLorentzVector()	

        bazinga('nbjets and loose jet are: ')
        
        if nBJets==0 and nLooseBJets>=2:
            bazinga('inside 0 bjets')
            Htobb_p4 = looseBJetsP4_sortedByCsv[0] + looseBJetsP4_sortedByCsv[1]
        elif nBJets==1 and nLooseBJets>=1:
            Htobb_p4 = bJetsP4[0] + looseBJetsP4_sortedByCsv[0]
            bazinga('inside 1 bjets')
            
        elif nBJets >=2:
            Htobb_p4.SetPtEtaPhiM(tree.HCSV_pt,tree.HCSV_eta,tree.HCSV_phi,tree.HCSV_mass) 
        else:
            #print 'in the continue...'
            continue #pass


        bazinga (nBJets)
        bazinga(nLooseBJets)
        # print 'len(bJetsP4) is ', len(bJetsP4)
        # print 'bJetsP4: ', bJetsP4
        # print 'len(looseBJetsP4_sortedByCsv) is ', len(looseBJetsP4_sortedByCsv)
        # print 'looseBJetsP4_sortedByCsv ', looseBJetsP4_sortedByCsv
        tmpBJet = bJetsP4 + looseBJetsP4_sortedByCsv
        bJetsP4 = tmpBJet[:2]
       # print 'after tmpt, bJetsP4 is ', bJetsP4
        tmpBJetsCSV = bJetsCSV + looseBJetsCSV
        #print 'tmpBJetsCSV is ', tmpBJetsCSV
        bJetsCSV = tmpBJetsCSV[:2]
        #print 'after tmp, bJetsCSV is ', bJetsCSV

        bazinga('before Htobb.M')
        
        if physRegion == "SR" and not passLoose:
         #   print 'doing ', physRegion
            if Htobb_p4.M() < 90 or Htobb_p4.M() > 150: continue 
        elif physRegion == "SR" and passLoose:
            if Htobb_p4.M() < 75 or Htobb_p4.M() > 175: continue
        elif physRegion == "CRTT":
          #  print 'doing ', physRegion
            if Htobb_p4.M() < 90 or Htobb_p4.M() > 150: continue
        elif physRegion == "CRDY":
           # print 'doing ', physRegion
            if Htobb_p4.M() >= 90 and Htobb_p4.M() <= 150: continue
        elif physRegion == "CRDY_1b":
           # print 'doing ', physRegion
            if Htobb_p4.M() < 90 or Htobb_p4.M() > 150: continue
        elif physRegion == "CRDY_0b":
            #print 'doing ', physRegion
            if Htobb_p4.M() < 90 or Htobb_p4.M() > 150: continue
        else:
            #print 'doing ', physRegion
            exit(1)


        histos['cutFlow'].Fill(6, 1)# Htobb mass    

        if passLoose:
            if nLeps > 5: continue  #??????????
        else:
            if nLeps != 2: continue 
        histos['cutFlow'].Fill(7, 1)# 2 leptons


        bazinga('before Zmass raw')  
        
        if physRegion == "SR" and not passLoose:
            #print 'doing ', physRegion
            if tree.V_mass <76 or tree.V_mass > 106 : continue
        elif physRegion == "SR" and passLoose:
            if tree.V_mass <56 or tree.V_mass > 126 : continue
        elif physRegion == "CRTT":
            #print 'doing ', physRegion
            if tree.V_mass >= 76 and tree.V_mass <= 106 : continue
        elif physRegion == "CRDY":
            #print 'doing ', physRegion
            if tree.V_mass <76 or tree.V_mass > 106 : continue
        elif physRegion == "CRDY_1b":
            #print 'doing ', physRegion
            if tree.V_mass <76 or tree.V_mass > 106 : continue
        elif physRegion == "CRDY_0b":
            #print 'doing ', physRegion
            if tree.V_mass <76 or tree.V_mass > 106 : continue     
        else:
            #print 'doing ', physRegion
            exit(1)



        histos['cutFlow'].Fill(8,1) # Dilepton mass
       


        Z_p4=ROOT.TLorentzVector()  
        missing_p4=ROOT.TLorentzVector()  
        hh_tlv = ROOT.TLorentzVector()

        bazinga('get ready to build HH') 
# build HH candidate and draw mass transverse  
        
        Z_p4.SetPtEtaPhiM(tree.V_pt,tree.V_eta,tree.V_phi,tree.V_mass)   
        missing_p4.SetPtEtaPhiM(tree.met_pt,tree.met_eta,tree.met_phi,tree.met_mass)    
        hh_Mt = (Htobb_p4 + Z_p4 + missing_p4).Mt()
        hToZZ_p4 = (Z_p4 + missing_p4)
        visible_p4 = (Z_p4 + Htobb_p4)
        bazinga('before mt_cosine')
        hToZZ_mt_cosine = mt_cosine(Z_p4.Pt(), tree.met_pt, Z_p4.Phi(), tree.met_phi )
        #hToZZ_mt_cosine = mt_cosine(tree.V_pt, tree.met_pt, tree.V_phi, tree.met_phi )
        hh_mt_cosine = mt_cosine(visible_p4.Pt(), tree.met_pt, visible_p4.Phi(), tree.met_phi )
        
        if False: 
            #if True:
            print 'hToZZ_mt_cosine = {0} ==?== hToZZ_p4.Mt() ={1}'.format( hToZZ_mt_cosine, hToZZ_p4.Mt() )
            print 'hh_mt_cosine = {0} ==?== hh_Mt = {1}'.format( hh_mt_cosine, hh_Mt)
            print 'Z_p4.Pt() = {0} == tree.V_pt = {1}'.format(Z_p4.Pt(), tree.V_pt)
            print 'Z_p4.Phi() = {0} == tree.V_phi = {1}'.format(Z_p4.Phi(), tree.V_phi)
            #print 'visible_p4.Pt() = {0} and visible_p4.Phi() = {1}'.format(visible_p4.Pt(), visible_p4.Phi() )
        

        #histos['hh_mt_cosine_long_beforeMETcut'].Fill(hh_mt_cosine, evWgt)
        histos['hh_mt_cosine_beforeMETcut'].Fill(hh_mt_cosine, evWgt)
        histos['hToZZ_mt_cosine_long_beforeMETcut'].Fill(hToZZ_mt_cosine, evWgt)
        histos['hToZZ_mt_cosine_beforeMETcut'].Fill(hToZZ_mt_cosine, evWgt)

        histos['hhMt_beforeMETcut'].Fill(hh_Mt,evWgt)                 
        histos['hhMt_long_beforeMETcut'].Fill(hh_Mt,evWgt)                 
        #print 'btagCSV0_beforeMETcut={0} for fileName={1} with evWgt={2}'.format(bJetsCSV[0], fileName, evWgt)
        bazinga('before bJetCSV')
        histos['btagCSV0_beforeMETcut'].Fill(bJetsCSV[0], evWgt)
        histos['btagCSV1_beforeMETcut'].Fill(bJetsCSV[1], evWgt)
# tree->Scan("tree.Jet_btagCSV[tree.hJCidx[0]]")
        histos['hZZpt_beforeMETcut'].Fill(hToZZ_p4.Pt(),evWgt)                 
        histos['hZZmt_beforeMETcut'].Fill(hToZZ_p4.Mt(),evWgt)                 
        histos['hZZmt_long_beforeMETcut'].Fill(hToZZ_p4.Mt(),evWgt)                 
        histos['metpt_beforeMETcut'].Fill(tree.met_pt, evWgt)  
        histos['zMass_beforeMETcut'].Fill(tree.V_mass, evWgt)
        histos['zHMass_beforeMETcut'].Fill(visible_p4.M(), evWgt)
        histos['zHTransMass_beforeMETcut'].Fill(visible_p4.Mt(), evWgt)

        histos['zPt_beforeMETcut'].Fill(tree.V_pt, evWgt)

        histos['hCSVmass_beforeMETcut'].Fill(Htobb_p4.M(),evWgt)    
        histos['hCSVmass_long_beforeMETcut'].Fill(Htobb_p4.M(),evWgt)
        histos['zMass_long_beforeMETcut'].Fill(tree.V_mass, evWgt)
        histos['hCSVpt_beforeMETcut'].Fill(Htobb_p4.Pt(),evWgt)    
        histos['nleps_beforeMETcut'].Fill(nLeps, evWgt)    #how many good leptons remains to be in the event
        bazinga('bjetsp4')
        if bJetsP4[0].Pt() > bJetsP4[1].Pt():
            histos['bjet0pt_beforeMETcut'] .Fill(bJetsP4[0].Pt() ,evWgt)
            histos['bjet0eta_beforeMETcut'].Fill(bJetsP4[0].Eta(),evWgt)
            histos['bjet1pt_beforeMETcut'] .Fill(bJetsP4[1].Pt() ,evWgt)
            histos['bjet1eta_beforeMETcut'].Fill(bJetsP4[1].Eta(),evWgt)
        else:
            histos['bjet0pt_beforeMETcut'] .Fill(bJetsP4[1].Pt() ,evWgt)
            histos['bjet0eta_beforeMETcut'].Fill(bJetsP4[1].Eta(),evWgt)
            histos['bjet1pt_beforeMETcut'] .Fill(bJetsP4[0].Pt() ,evWgt)
            histos['bjet1eta_beforeMETcut'].Fill(bJetsP4[0].Eta(),evWgt)
        bazinga('again bjets p4')
        for ij in xrange(0,len(bJetsP4)):
            histos['bjetpt_beforeMETcut'].Fill(bJetsP4[ij].Pt(),evWgt)
            histos['bjeteta_beforeMETcut'].Fill(bJetsP4[ij].Eta(),evWgt)
        bazinga('lep p4')
        for ij in xrange(0,len(lepsP4)):
            histos['leppt_beforeMETcut'].Fill(lepsP4[ij].Pt(),evWgt)
            histos['lepeta_beforeMETcut'].Fill(lepsP4[ij].Eta(),evWgt)
                     
        bazinga('before doing leading-subLeading leptons')
        histos['lep0pt_beforeMETcut']	.Fill(lepsP4[0].Pt()	,evWgt)
        histos['lep1pt_beforeMETcut']	.Fill(lepsP4[1].Pt()	,evWgt)
        histos['lep0eta_beforeMETcut']	.Fill(lepsP4[0].Eta()   ,evWgt)
        histos['lep1eta_beforeMETcut']	.Fill(lepsP4[1].Eta()   ,evWgt)
        bazinga('dR vars')
#work with angular variables
        dR_leps= lepsP4[0].DeltaR(lepsP4[1])    
        dR_bjets = bJetsP4[0].DeltaR (bJetsP4[1])
        dR_ZH = Z_p4.DeltaR(Htobb_p4)
        dRList = []
        for l in lepsP4:
            for b in bJetsP4:
                dRList.append( l.DeltaR( b) )
        dR_lb_min = min(float(i) for i in dRList )  if len(dRList) != 0 else -10

        histos['dR_leps_beforeMETcut'].Fill(dR_leps,evWgt)    
        histos['dR_bjets_beforeMETcut'].Fill(dR_bjets,evWgt)    
        histos['dR_ZH_beforeMETcut'].Fill(dR_ZH,evWgt)    
        histos['dR_lb_min_beforeMETcut'].Fill(dR_lb_min,evWgt)    

#============================
        dPhi_leps= lepsP4[0].DeltaPhi(lepsP4[1])
        dPhi_bjets = bJetsP4[0].DeltaPhi (bJetsP4[1])
        dPhi_ZH = Z_p4.DeltaPhi(Htobb_p4)
        dPhiList = []
        for l in lepsP4:
            for b in bJetsP4:
                dPhiList.append( l.DeltaPhi( b) )
        dPhi_lb_min = min(abs(float(i)) for i in dPhiList ) if len(dPhiList) != 0 else -10

        histos['dPhi_leps_beforeMETcut'].Fill(dPhi_leps,evWgt)
        histos['dPhi_bjets_beforeMETcut'].Fill(dPhi_bjets,evWgt)
        histos['dPhi_ZH_beforeMETcut'].Fill(dPhi_ZH,evWgt)
        histos['dPhi_lb_min_beforeMETcut'].Fill(dPhi_lb_min,evWgt)
#============================
        
        dEta_leps= lepsP4[0].Eta() - lepsP4[1].Eta()
	dEta_bjets = bJetsP4[0].Eta() - bJetsP4[1].Eta()
        dEta_ZH =  Z_p4.Eta() - Htobb_p4.Eta() 
        dEtaList = []
        for l in lepsP4:
            for b in bJetsP4:
                dEtaList.append( l.Eta() - b.Eta() )
        dEta_lb_min = min(abs(float(i)) for i in dEtaList )  if len(dEtaList) != 0 else -10

        histos['dEta_leps_beforeMETcut'].Fill(dEta_leps,evWgt)
        histos['dEta_bjets_beforeMETcut'].Fill(dEta_bjets,evWgt)
        histos['dEta_ZH_beforeMETcut'].Fill(dEta_ZH,evWgt)
        histos['dEta_lb_min_beforeMETcut'].Fill(dEta_lb_min,evWgt)

        #calculate S-transverse masses
        mt2maker1 = mt2_bisect.mt2()
        mt2maker2 = mt2_bisect.mt2()
        mt2maker3 = mt2_bisect.mt2()
        mt2maker4 = mt2_bisect.mt2()
        mt2maker5 = mt2_bisect.mt2()
        # use somewhere predifined masses maybe? like H=125, Z=91, Z* = 125-91, etc?? 
        mt2_llmet = mt2(mt2maker1, lepsP4[0], lepsP4[1], missing_p4) #(l1, l2, MET))
        mt2_b1l1b2l2met = mt2(mt2maker2, bJetsP4[0] + lepsP4[0], bJetsP4[1] + lepsP4[1], missing_p4) #(b1+l1, b2+l2, MET)
        mt2_b1l2b2l1met = mt2(mt2maker3, bJetsP4[0] + lepsP4[1], bJetsP4[1] + lepsP4[0], missing_p4) #(b1+l2, b2+l1, MET)
        mt2_bbmet = mt2(mt2maker4, bJetsP4[0], bJetsP4[1], missing_p4) #(b1, b2, MET)
        mt2_ZHmet = mt2(mt2maker5, Z_p4 , Htobb_p4, missing_p4) #(ll, bb, MET)
        min_mt2_blmet = min (mt2_b1l1b2l2met, mt2_b1l2b2l1met)

        histos['mt2_llmet_beforeMETCut'].Fill(min(mt2_llmet, 299), evWgt)
        histos['mt2_b1l1b2l2met_beforeMETCut'].Fill(min(mt2_b1l1b2l2met, 299), evWgt)
        histos['mt2_b1l2b2l1met_beforeMETCut'].Fill(min(mt2_b1l2b2l1met, 299), evWgt)
        histos['mt2_bbmet_beforeMETCut'].Fill(min(mt2_bbmet, 299), evWgt)
        histos['mt2_ZHmet_beforeMETCut'].Fill(mt2_ZHmet, evWgt)
        histos['min_mt2_blmet_beforeMETCut'].Fill(min(min_mt2_blmet, 299), evWgt)
        

        if not passLoose:
            if tree.met_pt < 20: continue    
        else:
            if tree.met_pt < 0: continue
        histos['cutFlow'].Fill(9,1) # met cut   

        histos['hhMt_long'].Fill(hh_Mt,evWgt)                 
        if not passLoose:
            if hh_Mt < 250: continue     #try hh_mt_cosine
        else:
            if hh_Mt < 100: continue  
        histos['cutFlow'].Fill(10,1)# HH_mt cut           
 
        #histos['hh_mt_cosine_long'].Fill(hh_mt_cosine, evWgt)
        histos['hh_mt_cosine'].Fill(hh_mt_cosine, evWgt)
        histos['hToZZ_mt_cosine_long'].Fill(hToZZ_mt_cosine, evWgt)
        histos['hToZZ_mt_cosine'].Fill(hToZZ_mt_cosine, evWgt)



        histos['mt2_llmet'].Fill(min(mt2_llmet, 299), evWgt)
        histos['mt2_b1l1b2l2met'].Fill(min(mt2_b1l1b2l2met, 299), evWgt)
        histos['mt2_b1l2b2l1met'].Fill(min(mt2_b1l2b2l1met, 299), evWgt)
        histos['mt2_bbmet'].Fill(min(mt2_bbmet, 299), evWgt)
        histos['mt2_ZHmet'].Fill(mt2_ZHmet, evWgt)
        histos['min_mt2_blmet'].Fill(min(min_mt2_blmet, 299), evWgt)


        histos['btagCSV0'].Fill(bJetsCSV[0], evWgt)
        histos['btagCSV1'].Fill(bJetsCSV[1], evWgt)
# tree->Scan("tree.Jet_btagCSV[tree.hJCidx[0]]")
        histos['hZZpt'].Fill(hToZZ_p4.Pt(),evWgt)                 
        histos['hZZmt'].Fill(hToZZ_p4.Mt(),evWgt)                 
        histos['hZZmt_long'].Fill(hToZZ_p4.Mt(),evWgt)                 
        histos['metpt'].Fill(tree.met_pt, evWgt)  
        histos['zMass'].Fill(tree.V_mass, evWgt)
        histos['zHMass'].Fill(visible_p4.M(), evWgt)
        histos['zHTransMass'].Fill(visible_p4.Mt(), evWgt)
        
        histos['zPt'].Fill(tree.V_pt, evWgt)
        histos['hhMt'].Fill(hh_Mt,evWgt)                 
        histos['hCSVmass'].Fill(Htobb_p4.M(),evWgt)    
        histos['hCSVmass_long'].Fill(Htobb_p4.M(),evWgt)
        histos['zMass_long'].Fill(tree.V_mass, evWgt)
        histos['hCSVpt'].Fill(Htobb_p4.Pt(),evWgt)    
        histos['nleps'].Fill(nLeps, evWgt)    #how many good leptons remains to be in the event
        if bJetsP4[0].Pt()  > bJetsP4[1].Pt() :        
            histos['bjet0pt'] .Fill(bJetsP4[0].Pt() ,evWgt)
            histos['bjet0eta'].Fill(bJetsP4[0].Eta(),evWgt)
            histos['bjet1pt'] .Fill(bJetsP4[1].Pt() ,evWgt)
            histos['bjet1eta'].Fill(bJetsP4[1].Eta(),evWgt)
            minitree.bpt0 = bJetsP4[0].Pt()
            minitree.beta0 = bJetsP4[0].Eta()
            minitree.bphi0 = bJetsP4[0].Phi()
            minitree.bpt1 = bJetsP4[1].Pt()
            minitree.beta1 = bJetsP4[1].Eta()
            minitree.bphi1 = bJetsP4[1].Phi()
        else:
            histos['bjet0pt'] .Fill(bJetsP4[1].Pt() ,evWgt)
            histos['bjet0eta'].Fill(bJetsP4[1].Eta(),evWgt)
            histos['bjet1pt'] .Fill(bJetsP4[0].Pt() ,evWgt)
            histos['bjet1eta'].Fill(bJetsP4[0].Eta(),evWgt)
            minitree.bpt0 = bJetsP4[1].Pt()
            minitree.beta0 = bJetsP4[1].Eta()
            minitree.bphi0 = bJetsP4[1].Phi()
            minitree.bpt1 = bJetsP4[0].Pt()
            minitree.beta1 = bJetsP4[0].Eta()
            minitree.bphi1 = bJetsP4[0].Phi()
        for ij in xrange(0,len(bJetsP4)):
            histos['bjetpt'].Fill(bJetsP4[ij].Pt(),evWgt)
            histos['bjeteta'].Fill(bJetsP4[ij].Eta(),evWgt)
        
        for ij in xrange(0,len(lepsP4)):
            histos['leppt'].Fill(lepsP4[ij].Pt(),evWgt)
            histos['lepeta'].Fill(lepsP4[ij].Eta(),evWgt)
                     


        bazinga('before doing leading-subLeading leptons')
        histos['lep0pt']	.Fill(lepsP4[0].Pt()	,evWgt)
        histos['lep1pt']	.Fill(lepsP4[1].Pt()	,evWgt)
        histos['lep0eta']	.Fill(lepsP4[0].Eta()   ,evWgt)
        histos['lep1eta']	.Fill(lepsP4[1].Eta()   ,evWgt)
        
        bazinga('before lep for minitree')
        minitree.leppt0 = lepsP4[0].Pt() 
        minitree.lepeta0 = lepsP4[0].Eta() 
        minitree.lepphi0 = lepsP4[0].Phi() 

        minitree.leppt1 = lepsP4[1].Pt()
        minitree.lepeta1 = lepsP4[1].Eta()
        minitree.lepphi1 = lepsP4[1].Phi()
        bazinga('before met for minitree')
        minitree.metpt = tree.met_pt
        minitree.meteta = tree.met_eta
        minitree.metphi = tree.met_phi

        minitree.btag0 = bJetsCSV[0]
        minitree.btag1 = bJetsCSV[1]
        bazinga('before V for minitree')
        minitree.zmass = tree.V_mass
        minitree.zpt0 = tree.V_pt 
        minitree.zeta0 = tree.V_eta
        minitree.zphi0 = tree.V_phi
        bazinga('before hToZZ for minitree')
        minitree.hmass0 = hToZZ_p4.M()
        minitree.hmt0 = hToZZ_p4.Mt()
        minitree.hpt0 = hToZZ_p4.Pt()
        minitree.heta0 = hToZZ_p4.Eta()
        minitree.hphi0 = hToZZ_p4.Phi()
        minitree.hToZZ_mt_cosine = hToZZ_mt_cosine
        bazinga('before Htobb for minitree')
        minitree.hmass1 = Htobb_p4.M()
        minitree.hmt1 = Htobb_p4.Mt()
        minitree.hpt1 = Htobb_p4.Pt()
        minitree.heta1 = Htobb_p4.Eta()
        minitree.hphi1 = Htobb_p4.Phi()
        bazinga('before # for minitree')
        minitree.nbjets = nBJets
        minitree.njets = nJets
        minitree.nloosebjets = nLooseBJets
        minitree.nleps = nLeps
        
        bazinga('before dEta for minitree')
        minitree.dEta_lb_min = dEta_lb_min
        minitree.dEta_ZH = dEta_ZH
        minitree.dEta_bjets = dEta_bjets
        minitree.dEta_leps = dEta_leps
        bazinga('before dR for minitree')
        minitree.dR_lb_min = dR_lb_min
        minitree.dR_ZH = dR_ZH
        minitree.dR_bjets = dR_bjets
        minitree.dR_leps = dR_leps
        bazinga('before dPhi for minitree')
        minitree.dPhi_lb_min = dPhi_lb_min
        minitree.dPhi_ZH = dPhi_ZH
        minitree.dPhi_bjets = dPhi_bjets
        minitree.dPhi_leps = dPhi_leps

        minitree.hhmt = hh_Mt
        minitree.hh_mt_cosine = hh_mt_cosine
 
        minitree.zhmass = visible_p4.M()
        minitree.zhpt = visible_p4.Pt()
        minitree.zheta = visible_p4.Eta()
        minitree.zhphi = visible_p4.Phi()
        bazinga('before mt2 for minitree')
        minitree.mt2_llmet = mt2_llmet
        minitree.mt2_bbmet = mt2_bbmet
        minitree.mt2_b1l1b2l2met = mt2_b1l1b2l2met
        minitree.mt2_b1l2b2l1met = mt2_b1l2b2l1met
        minitree.min_mt2_blmet = min_mt2_blmet
        minitree.mt2_ZHmet = mt2_ZHmet

        # minitree.btagWeightCSV_up_lf = tree.btagWeightCSV_up_lf
        # minitree.btagWeightCSV_up_lfstats1 = tree.btagWeightCSV_up_lfstats1
        # minitree.btagWeightCSV_up_lfstats2 = tree.btagWeightCSV_up_lfstats2
        
        # minitree.btagWeightCSV_up_hf = tree.btagWeightCSV_up_hf
        # minitree.btagWeightCSV_up_hfstats1 = tree.btagWeightCSV_up_hfstats1
        # minitree.btagWeightCSV_up_hfstats2 = tree.btagWeightCSV_up_hfstats2
        
        # minitree.btagWeightCSV_down_lf = tree.btagWeightCSV_down_lf
        # minitree.btagWeightCSV_down_lfstats1 = tree.btagWeightCSV_down_lfstats1
        # minitree.btagWeightCSV_down_lfstats2 = tree.btagWeightCSV_down_lfstats2
        
        # minitree.btagWeightCSV_down_hf = tree.btagWeightCSV_down_hf
        # minitree.btagWeightCSV_down_hfstats1 = tree.btagWeightCSV_down_hfstats1
        # minitree.btagWeightCSV_down_hfstats2 = tree.btagWeightCSV_down_hfstats2

        minitree.bdtOutput = -10
        #minitree.bdtOutput_multiclass = -10
        #minitree.dnnOutput = -10

        minitree.evWgt = evWgt
        minitree.countWeighted = countWeighted 
        bazinga('before xsec for minitree')
        if xsec is None:# or xsec==1:
                #print 'doing Data'
            bazinga('inside IF for xsec')
            bazinga('xsec is '); bazinga(xsec)
            minitree.xsec = 1
            bazinga('v_id is '); bazinga(v_id)
            minitree.genvbosonpdgid = 0
        else:
            bazinga('inside ELSE for xsec')
            bazinga('file is '); bazinga(fIn)
            bazinga('xsec is '); bazinga(xsec)
            minitree.xsec = xsec
            if v_id:
                bazinga('v_id is '); bazinga(v_id)
                minitree.genvbosonpdgid = v_id
            else:
                minitree.genvbosonpdgid = 0
#work with angular variables
        # dR_leps= lepsP4[0].DeltaR(lepsP4[1])    
        # dR_bjets = bJetsP4[0].DeltaR (bJetsP4[1])
        # dR_ZH = Z_p4.DeltaR(Htobb_p4)
        # dRList = []
        # for l in lepsP4:
        #     for b in bJetsP4:
        #         dRList.append( l.DeltaR( b) )
        # dR_lb_min = min(float(i) for i in dRList )  if len(dRList) != 0 else -10
        bazinga('before dR histograms')
        histos['dR_leps'].Fill(dR_leps,evWgt)    
        histos['dR_bjets'].Fill(dR_bjets,evWgt)    
        histos['dR_ZH'].Fill(dR_ZH,evWgt)    
        histos['dR_lb_min'].Fill(dR_lb_min,evWgt)    

#============================
        # dPhi_leps= lepsP4[0].DeltaPhi(lepsP4[1])
        # dPhi_bjets = bJetsP4[0].DeltaPhi (bJetsP4[1])
        # dPhi_ZH = Z_p4.DeltaPhi(Htobb_p4)
        # dPhiList = []
        # for l in lepsP4:
        #     for b in bJetsP4:
        #         dPhiList.append( l.DeltaPhi( b) )
        # dPhi_lb_min = min(abs(float(i)) for i in dPhiList ) if len(dPhiList) != 0 else -10
        bazinga('before dPhi histograms')
        histos['dPhi_leps'].Fill(dPhi_leps,evWgt)
        histos['dPhi_bjets'].Fill(dPhi_bjets,evWgt)
        histos['dPhi_ZH'].Fill(dPhi_ZH,evWgt)
        histos['dPhi_lb_min'].Fill(dPhi_lb_min,evWgt)
#============================
        
        # dEta_leps= lepsP4[0].Eta() - lepsP4[1].Eta()
	# dEta_bjets = bJetsP4[0].Eta() - bJetsP4[1].Eta()
        # dEta_ZH =  Z_p4.Eta() - Htobb_p4.Eta() 
        # dEtaList = []
        # for l in lepsP4:
        #     for b in bJetsP4:
        #         dEtaList.append( l.Eta() - b.Eta() )
        # dEta_lb_min = min(abs(float(i)) for i in dEtaList )  if len(dEtaList) != 0 else -10
        bazinga('before dEta histograms')
        histos['dEta_leps'].Fill(dEta_leps,evWgt)
        histos['dEta_bjets'].Fill(dEta_bjets,evWgt)
        histos['dEta_ZH'].Fill(dEta_ZH,evWgt)
        histos['dEta_lb_min'].Fill(dEta_lb_min,evWgt)


    #histos['cutFlowLogScale'] = copy.deepcopy(histos['cutFlow']) 

    # check if integral has to start from 0 or 1, read ROOT bin enumeration convention?
        nbins = lastEffBin - 1
    #print 'nbins in cutFlow histo', nbins, 
    
        for bin, label in enumerate(binLabels):
        #print '{} entries in zero bin, and {} in the 9th bins'.format(histos['cutFlow'].GetBinContent(0), histos['cutFlow'].GetBinContent(9))
        #print '\n'
        #print 'processing bin {} with content {}'.format((bin+1),  histos['cutFlow'].GetBinContent(bin+1))
            histos['cutFlow'].GetXaxis().SetBinLabel(bin+1,label)
            histos['cutFlowEff'].GetXaxis().SetBinLabel(bin+1,label)

            if histos['cutFlow'].Integral(1, nbins) ==0: #len(binLabels)) == 0:
                print 'ooups, devision by zero may happen, need more events?'
            else:
                #eff = 100* histos['cutFlow'].Integral(bin+1, nbins)/histos['cutFlow'].Integral(1, nbins) #len(binLabels))
                eff_v2 = 100.* histos['cutFlow'].GetBinContent(bin+1)/ histos['cutFlow'].GetBinContent(1)
                #print 'eff is ', eff_v2
                #print 'dividing {} by {} we get eff {}'.format(histos['cutFlow'].GetBinContent(bin+1), histos['cutFlow'].GetBinContent(1), eff_v2)
            #histos['cutFlowEff'].SetBinContent(bin+1, eff)
                histos['cutFlowEff'].SetBinContent(bin+1, eff_v2)
            #print 'eff is ', eff_v2



        bazinga('about to fill minitree')
        if passLoose:
            minitree.fill()
        bazinga('after fill of minitree')
        bazinga('about to close IN file')
                        #all done with this file
        if file_ext == '.root':
            fIn.Close()
        elif file_ext == '.txt':
            pass
            print ''#all is fine, txt file as input'
        else:
            print 'fix me later: may be memory leak due to open "fc"'
        #bazinga('about to fill minitree')
        #minitree.fill()
        #bazinga('after fill of minitree')
    if fIn.IsOpen():
        fIn.Close()
    bazinga('about to cd into the fO file')
    fO.cd()
    if not passLoose:
        for key in histos: histos[key].Write()
    else:
        minitree.write()
    #minitree.vals.reset()
    # print tree contents in CSV format
    
    #minitree.csv()
    #fO.write()
    #fO.close()

    #save histograms to file
    #fOut=ROOT.TFile.Open(outFileURL,'RECREATE')
    #fOut.cd()
    #for key in histos: histos[key].Write()
    bazinga('about to close Out file')
    #fO.write()
    fO.close()
    #fOut.Close()
    

"""
Wrapper to be used when run in parallel
"""
def runSimplestAnPacked(args):
    bazinga ('inside runSimplestAnPacked')
    try:
        print 'len of args is ', len(args)
        print 'args are :'
        print args
        return runSimplestAn(inFileURLorList=args[0],
                             outFileURL=args[1],
                             xsec=args[2], 
                             denominator=args[3],
                             isSignal = args[4], 
                             splitSignal = args[5], 
                             whichChannel = args[6],
                             physRegion = args[7],
                             passLoose = args[8])
    except :
        print 50*'<'
        print "  Problem  (%s) with %s continuing without"%(sys.exc_info()[1],args[0])
        print 50*'<'
        return False


"""
steer the script
"""
#@do_cprofile
def main():

    #configuration
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option('-t', '--type',		 dest='type'  ,		 help='do analysis with cuts or create trees: DoCuts or SaveTrees',	  default=None,		   type='string')
    parser.add_option('-j', '--json',		 dest='json'  ,		 help='json with list of files',	  default=None,		   type='string')
    parser.add_option('-r', '--region',		 dest='region'  ,		 help='region:SR,CRDY,CRTT,CRDY_1b,CRDY_0b',	  default=None,		   type='string')
    parser.add_option('-m', '--mod',		 dest='moduleExt'  ,		 help='module ext for cProfile',	  default=None,	      type='string')
    parser.add_option('-i', '--inDir',		 dest='inDir',		 help='input directory with files',   default=None,		   type='string')
    parser.add_option('-w', '--write2outDir',		 dest='outDir',		 help='output directory',			  default='analysis',  type='string')
    parser.add_option('-n', '--njobs',		 dest='njobs',		 help='# jobs to run in parallel',	  default=0,		   type='int')
    (opt, args) = parser.parse_args()

    #read list of samples
    if len(opt.json) != 0:
        jsonFile = open(opt.json,'r')
        samplesList=json.load(jsonFile,encoding='utf-8').items()
        jsonFile.close()

    #prepare output
    if len(opt.outDir) is None: opt.outDir='./'
    os.system('mkdir -p %s' % opt.outDir) #overwrite if exists
    
    physRegion = opt.region
    passLoose = None

    if 'DoCuts' in opt.type:
        passLoose = False
    elif 'SaveTrees' in opt.type:
        passLoose = True
    else:
        print 'choose "DoCuts or SaveTrees" for "-t" option'
        sys.exit(1)

    bazinga('before processing samplesLIst')
    #create the analysis jobs
    denominator=None #  Tot, Hzz or Hww
    isSignal = False
    splitSignal= None # No, Hzz, Hww
    taskList = []
    if len(opt.json) is not None  and samplesList:
        bazinga('processing samplesLIst')
        for sample, sampleInfo in samplesList: 
            fileWithTrees = '%s/%s.txt' % (opt.inDir,sample) #  add slash? ->  /%s/%s.root' % (opt.inDir,sample)
            print 'sample is', sample
            print fileWithTrees
            print sampleInfo
#with open (fileWithTrees, mode = "rt") as f:
            #   treesList = f.read().split('\n')
                #inFileURL  = '%s/%s.root' % (opt.inDir,sample) #  add slash? ->  /%s/%s.root' % (opt.inDir,sample)
        #if not os.path.isfile(inFileURL): continue
            xsec= sampleInfo[0] if sampleInfo[1]==0 else None		
            
            denominator = sampleInfo[5] if sampleInfo[1]==0 else None
            
            isSignal = sampleInfo[6] if sampleInfo[1]==0 else False

            splitSignal = sampleInfo[7]# if sampleInfo[1]==0 else None
            whichChannel = sampleInfo[8]  # electron or muon channel 
            if splitSignal and 'H' in splitSignal:
                outFileURL = '%s/%s_%s' % (opt.outDir,sample,splitSignal )
            else:
                outFileURL = '%s/%s' % (opt.outDir,sample)
                #taskList.append( (inFileURL,outFileURL,xsec, denominator) )
            typle = (fileWithTrees,outFileURL,xsec, denominator, isSignal, splitSignal, whichChannel, physRegion, passLoose) 
            print typle
            taskList.append( typle )
    else:
        inFileURL  = inGlobalFile
        xsec = None
        print '************* this is debug run*************'
        outFileURL = '%s/%s' % (opt.outDir,"plots")
        taskList.append( (inFileURL,outFileURL,xsec, denominator, isSignal, splitSignal, whichChannel, physRegion, passLoose) )
  
    # take into account this info:
    # http://stackoverflow.com/questions/24728084/why-does-this-implementation-of-multiprocessing-pool-not-work
    #run the analysis jobs
    if opt.njobs == 0:
        print 'use 1 cpu'
        for inFileURL, outFileURL, xsec, denominator, isSignal, splitSignal in taskList:
            runSimplestAn(inFileURL=inFileURL, outFileURL=outFileURL, xsec=xsec, denominator=denominator, isSignal = isSignal, splitSignal=splitSignal, whichChannel=whichChannel, physRegion=physRegion, passLoose=passLoose )
    else:
        print 'use multiprocessing'
        from multiprocessing import Pool, Process
        #from pathos.multiprocessing import ProcessingPool as Pool
        pool = Pool(opt.njobs)
        
#        try:
            #funct= runSimplestAn(inFileURL=inFileURL, outFileURL=outFileURL, xsec=xsec, denominator=denominator)
            # apply runSimplestAn fcn to each object in the taskList with the hepl of map()
            #pool.map(funct,taskList)
        pool.map(runSimplestAnPacked,taskList)
        print 'after pool.map call'
            #p = Process(target=runSimplestAn, args=taskList)
            #p.start()
            #p.join()
        #except Exception as e:
            #except ( TypeError): # attention it is a bad practice, normally one should not touch TypeError 
            #except (cPickle.PicklingError, TypeError) as e: # attention it is a bad practice, normally one should not touch TypeError 
        #    print 50*'<'
        #    print e.__doc__
        #    print e.message
            #print "  Problem  (%s) with %s continuing without"%(sys.exc_info()[1],args[0])
            #print 'Exception is caught: {}'.format(str(e))
            #print 'Exception is caught: {}'.format(str(e)), file=sys.stderr
        #    print 50*'<'
        #    raise 
        #finally:
            #perform clean up here
        #    print '\nthere COULD be a problem with the multiprocessing map, see stack above for exceptions, if any'
                




    #all done here
    print '\nAnalysis results are available in %s' % opt.outDir
    #exit(0)
    


"""
for execution from another script
"""
if __name__ == "__main__":
    #sys.exit(main())
    

    start_time = time.time()
    main()
    end_time = time.time()
    time_taken = end_time - start_time # time_taken is in seconds
    hours, rest = divmod(time_taken,3600)
    minutes, seconds = divmod(rest, 60)
    print "---it took {hours} hours, {minutes} minutes and {seconds:.1f} seconds to run the analysis ---".format (hours=hours, minutes=minutes, seconds=seconds)

    #img = mpimg.imread('cutFlow.png')
    #plt.imshow(img)
    #img = Image.open('cutFlow.png')
    #img.show() 



############
#additions on April 3
#1. met cut > 20 
#2. if debug run->use 1./5 of signal events and 1./25 of BG events
#3. k-factor 1.23 for all 4 DY samples is applied in the JSON file for Xsec number
#4. added various mt2 variables
