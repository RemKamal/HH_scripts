#!/usr/bin/env python

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

debugFractionOfEvents = 1./10
debugRun = False  # for quick runs with debugFractionOfEvents

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


"""
Perform the analysis on a single file
"""
def runSimplestAn(inFileURLorList, outFileURL, xsec=None, denominator=None, isSignal = False, splitSignal = None, whichChannel = 0):#muons):
    
    bazinga('before list of binLabels')

    binLabels = ['no cut', '1b-jet', '90<Hbb<150',  '2leps', '76<Z<106', 'met>30', 'hhMt>250']
    lastEffBin = 8
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
        'cutFlow'       :ROOT.TH1F('cutFlow', ';; Events', 7, 1, lastEffBin),
        'cutFlowEff'       :ROOT.TH1F('cutFlowEff', ';; Efficiency, %', 7, 1, lastEffBin),
        
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
        'btagCSV0'       :ROOT.TH1F('btagCSV0'	,';Leading b-Jet CSV weight; Events'	    , 40, 0., 1.),
        'btagCSV1'       :ROOT.TH1F('btagCSV1'	,';Subleading b-Jet CSV weight; Events'	    , 40, 0., 1.),
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
        'btagCSV0_beforeMETcut'       :ROOT.TH1F('btagCSV0_beforeMETcut'	,';Leading b-Jet CSV weight; Events'	    , 40, 0., 1.),
        'btagCSV1_beforeMETcut'       :ROOT.TH1F('btagCSV1_beforeMETcut'	,';Subleading b-Jet CSV weight; Events'	    , 40, 0., 1.),
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
        'zMass_long_beforeMETcut'      :ROOT.TH1F('zMass_long_beforeMETcut', ';Z mass [GeV]; Events', 50, 20, 220),
        'zPt_beforeMETcut'      :ROOT.TH1F('zPt_beforeMETcut', ';Z p_{T} [GeV]; Events', 50, 0, 300),

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

    countWeighted = 0
    count = 0
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
                    countWeighted += fIn.Get('CountWeighted').GetBinContent(1)
   #             if isSignal: #fix me
    #                count += fIn.Get('Count').GetBinContent(1)
      #          if isSignal: #fix me
     #               print 'File ',fIn, ' has Count equal to ', count
                    print 'File ',fIn, ' has CountWeighted equal to ', fIn.Get('CountWeighted').GetBinContent(1)
            print '...analysing {0} files in {1} with {2} countWeighted events'.format ( len(listOfFiles), inFileURLorList, countWeighted )
       #     if isSignal:#fix me
        #        print '...analysing {} files in {} with {} Count events'.format ( len(listOfFiles), inFileURLorList, count )
    else:
        print 'something went wrong, bad input file'
        

    if countWeighted is 0:
        print 'Something is wrong with "countWeighted", please check!'
        exit(1)
        
#    if isSignal and  count is 0:
 #       print 'Something is wrong with "count", please check!'
  #      exit(1)
    # tree->GetEntries("abs(GenVbosons_pdgId) ==23")
    # deprecated (genHiggsDecayMode % 10000 == 23")   

   # if denominator == "Tot":  #do nothing: Data or Bkg MC
    #    pass
    #elif denominator == "Hzz":  #HtoZZ MC
     #   count = 24816 
    #elif denominator == "Hww": #HtoWW in MC
     #   count = 562438 # W+ and W-
   # else:
 #    'smth went wrong'
 #       exit(1)

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
                      
        bazinga('before get entry')
        tree.GetEntry(i)

        if whichChannel == 0: #muons
            if tree.Vtype != 0: continue
     
        elif whichChannel == 1: #electrons
            if tree.Vtype != 1: continue
        else:
            print 'wrong channel type, only electron or muon are possible, exiting...'
            exit(1)

        if i%100==0 : 
            print 'isSignal, splitSignal are ', isSignal, splitSignal
            print 'xsec is ', xsec
            print 'evWgt is ', evWgt
            print 'countWeighted is ', countWeighted 
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



        lumino = 36800.
        #generator level weight only for MC

        #print '..xsec is', xsec
        #print 'countWeighted is ', countWeighted
        if xsec!=0 and countWeighted != 0: 
            #fix me proper usage os selLepEff when two leptons are in the event!
#            evWgt = tree.bTagWeight* 
            #print 'evWgt = ', evWgt 
            evWgt = xsec * (lumino / countWeighted) * tree.Jet_btagWeightCSV[tree.hJCidx[0]] * tree.Jet_btagWeightCSV[tree.hJCidx[1]]
                  #json is applied at skimming level

           # if  denominator !=0 and count !=0:
            #    evWgt = xsec * lumino * tree.puWeight * ROOT.TMath.Sign(1, tree.genWeight) / count
                #print 'evWgt here = ', evWgt  
        #if tree.genWeight>0 : evWgt *= tree.genWeight
        
        bazinga('before v_id')
        v_id = None
        if xsec is None or xsec==1.:
            pass
        #print 'doing Data'
        else:  # below is a hack to avoid segm. viol.
            for index in xrange ( 0, len (tree.GenVbosons_pdgId) ):
                v_id = abs ( int ( float(tree.GenVbosons_pdgId[0]) ) )
##########vs     
         #   if len(tree.GenVbosons_pdgId) != 0:
          #      v_id = abs ( tree.GenVbosons_pdgId[0]) 
        
        # if v_id is not None:
        #     print 'All is fine, v_id is ', v_id
        # else:
        #     print '************************what the heck is this variable about?'
        # if v_id is None:
        #     print '*************************************'
        #     print '*************************************'
        #print 'v_id is ', v_id
        #print 'splitSignal is ', splitSignal     

        if tree.Vtype == 1: #Int_t OR of ['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*', 'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v*']*
            #if not tree.HLT_ttH_DL_elel: continue
            if not tree.HLT_BIT_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v: continue  
        elif tree.Vtype == 0:
            if not tree.HLT_ttH_DL_mumu: continue #Int_t OR of ['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v*', 'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v*']*
        else:
            continue
            #pass

        if splitSignal == "No":
            #print 'all is fine, go further'
            pass
          
        elif splitSignal == "Hzz":
            #print 'in the Hzz'
            if not v_id == 23:
                #print 'before Hzz skip'
                continue    # limit to HtoZZ
        elif splitSignal == "Hww":
            #print '\nin the Hww'
            #print 'v_id is ', v_id
            if not v_id == 24:
                #print 'before Hww skip'
                continue    # limit to HtoWW
        else:
            print 'smth went wrong splitting the signal'
            print 'v_id is ', v_id 
            print 'splitSignal is ', splitSignal

        #print 'Here event weight is ', evWgt
        #if not (tree.Vtype ==0 or tree.Vtype==1): continue # limit to Ztoee or Ztomm                                

        # if len(tree.Jet_btagCSV)>1:
        #     evWgt *= tree.Jet_btagCSV[tree.hJCidx[0]] * tree.Jet_btagCSV[tree.hJCidx[1]] 
        #     print '0 and 1st element of btagCSV',  tree.Jet_btagCSV[tree.hJCidx[0]] , tree.Jet_btagCSV[tree.hJCidx[1]] 

        # if tree.selLeptons_Eff_HLT_RunD4p3[0]:
        #     print 'len of selLepEff and 0th element', len(tree.selLeptons_Eff_HLT_RunD4p3), tree.selLeptons_Eff_HLT_RunD4p3[0]
        #     if tree.selLeptons_Eff_HLT_RunD4p3[1]:
        #         print '......1st element of selLepEff', tree.selLeptons_Eff_HLT_RunD4p3 [1]
        #    evWgt *= tree.selLeptons_Eff_HLT_RunD4p3[0] * tree.selLeptons_Eff_HLT_RunD4p3[1]
            #fix me, do combinatorics for selLepEff
        #print 'while now event weight is ', evWgt
        
        #histos['cutFlow'].Fill(2,1)    # after Ztoll cut and 


        nJets = nBJets = nLooseBJets = 0
        jetsP4 = []
        bJetsP4 = []
        looseBJetsListOfTuples = []
        bazinga('before loop for jets')
        # independent loop over jets in the event
        for ij in xrange(0,tree.nJet):

            #get the kinematics and select the jet
            jp4=ROOT.TLorentzVector()
            jp4.SetPtEtaPhiM(tree.Jet_pt[ij],tree.Jet_eta[ij],tree.Jet_phi[ij],tree.Jet_mass[ij])
            if jp4.Pt()<30 or ROOT.TMath.Abs(jp4.Eta())>2.4 : continue
            jetsP4.append(jp4)

            #count selected jet
            nJets +=1

            #save P4 for b-tagged jet
            if tree.Jet_btagCSV[ij]>= 0.8: # CSV WP Medium, Spring
                nBJets += 1
                bJetsP4.append(jp4)
            elif 0.2 < tree.Jet_btagCSV[ij] < 0.8:
                nLooseBJets += 1
                looseBJetsListOfTuples.append((jp4,tree.Jet_btagCSV[ij]))
            else:
                continue #pass
        
                
        looseBJetsListOfTuples_tmp = sorted(looseBJetsListOfTuples, key=itemgetter(1), reverse = True)
        looseBJetsP4_sortedByCsv = map(itemgetter(0), looseBJetsListOfTuples_tmp )
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
                    print 'emu is ', emu
                    print 'lp4.Pt() is equal to ', lp4.Pt() 
                    print 'while tree.vLeptons_pt is ', tree.vLeptons_pt[emu]
                    #if lp4.Pt()<15: 
                    continue

    
            lepsP4.append(lp4)
            nLeps += 1
        
        #print 'nLeps is ', nLeps
        if nLeps != nvLeps:
                print 'nLeps is {0}, while nvLeps is {1}.'.format ( nLeps, nvLeps )
            #apply WPs from EG POG
            #nGoodLep +=1


        histos['cutFlow'].Fill(1,1) # no cut         
        bazinga('before njets_raw Fill')

        # fill raw histograms, before any cuts are applied
        # for ANY jet
        histos['njets_raw'].Fill(tree.nJet, evWgt)
        histos['nbjets_raw'].Fill(nBJets, evWgt) # how many remain to be 'good'=loose  b-jets 
        histos['metpt_raw'].Fill(tree.met_pt, evWgt)
        histos['nleps_raw'].Fill(nLeps, evWgt)



        # start HH selection 
        #*******************

        bazinga('asked for one b-jet for DY CR')
        if nBJets =! 1: continue    

        histos['cutFlow'].Fill(2, 1)    



        Htobb_p4=ROOT.TLorentzVector()	

        if nBJets==0 and nLooseBJets>=2:
            Htobb_p4 = looseBJetsP4_sortedByCsv[0] + looseBJetsP4_sortedByCsv[1]
        elif nBJets==1 and nLooseBJets>=1:
            Htobb_p4 = bJetsP4[0] + looseBJetsP4_sortedByCsv[0]
        elif nBJets >=2:
            Htobb_p4.SetPtEtaPhiM(tree.HCSV_pt,tree.HCSV_eta,tree.HCSV_phi,tree.HCSV_mass) 
        else:
            continue #pass

        #bazinga('HH selection begins')
        if Htobb_p4.M() < 90 or Htobb_p4.M() > 150: continue 
        histos['cutFlow'].Fill(3, 1)    


        if nLeps != 2: continue 
        histos['cutFlow'].Fill(4, 1)    


        bazinga('before Zmass raw')  
#        histos['zMass_raw'].Fill(tree.V_mass, evWgt)  
        if tree.V_mass <76 or tree.V_mass > 106 : continue     
        histos['cutFlow'].Fill(5,1) 
       


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


        histos['hhMt_long_beforeMETcut'].Fill(hh_Mt,evWgt)                 

        histos['btagCSV0_beforeMETcut'].Fill(tree.Jet_btagCSV[tree.hJCidx[0]])
        histos['btagCSV1_beforeMETcut'].Fill(tree.Jet_btagCSV[tree.hJCidx[1]])
# tree->Scan("tree.Jet_btagCSV[tree.hJCidx[0]]")
        histos['hZZpt_beforeMETcut'].Fill(hToZZ_p4.Pt(),evWgt)                 
        histos['hZZmt_beforeMETcut'].Fill(hToZZ_p4.Mt(),evWgt)                 
        histos['hZZmt_long_beforeMETcut'].Fill(hToZZ_p4.Mt(),evWgt)                 
        histos['metpt_beforeMETcut'].Fill(tree.met_pt, evWgt)  
        histos['zMass_beforeMETcut'].Fill(tree.V_mass, evWgt)
        histos['zHMass_beforeMETcut'].Fill(visible_p4.M(), evWgt)

        histos['zPt_beforeMETcut'].Fill(tree.V_pt, evWgt)
        histos['hhMt_beforeMETcut'].Fill(hh_Mt,evWgt)                 
        histos['hCSVmass_beforeMETcut'].Fill(Htobb_p4.M(),evWgt)    
        histos['hCSVmass_long_beforeMETcut'].Fill(Htobb_p4.M(),evWgt)
        histos['zMass_long_beforeMETcut'].Fill(tree.V_mass, evWgt)
        histos['hCSVpt_beforeMETcut'].Fill(Htobb_p4.Pt(),evWgt)    
        histos['nleps_beforeMETcut'].Fill(nLeps, evWgt)    #how many good leptons remains to be in the event
        histos['bjet0pt_beforeMETcut'] .Fill(bJetsP4[0].Pt() ,evWgt)
        histos['bjet0eta_beforeMETcut'].Fill(bJetsP4[0].Eta(),evWgt)
        histos['bjet1pt_beforeMETcut'] .Fill(bJetsP4[1].Pt() ,evWgt)
        histos['bjet1eta_beforeMETcut'].Fill(bJetsP4[1].Eta(),evWgt)
        
        for ij in xrange(0,len(bJetsP4)):
            histos['bjetpt_beforeMETcut'].Fill(bJetsP4[ij].Pt(),evWgt)
            histos['bjeteta_beforeMETcut'].Fill(bJetsP4[ij].Eta(),evWgt)
        
        for ij in xrange(0,len(lepsP4)):
            histos['leppt_beforeMETcut'].Fill(lepsP4[ij].Pt(),evWgt)
            histos['lepeta_beforeMETcut'].Fill(lepsP4[ij].Eta(),evWgt)
                     
        bazinga('before doing leading-subLeading leptons')
        histos['lep0pt_beforeMETcut']	.Fill(lepsP4[0].Pt()	,evWgt)
        histos['lep1pt_beforeMETcut']	.Fill(lepsP4[1].Pt()	,evWgt)
        histos['lep0eta_beforeMETcut']	.Fill(lepsP4[0].Eta()   ,evWgt)
        histos['lep1eta_beforeMETcut']	.Fill(lepsP4[1].Eta()   ,evWgt)
    
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








        if tree.met_pt < 30: continue    
        histos['cutFlow'].Fill(6,1)   

        histos['hhMt_long'].Fill(hh_Mt,evWgt)                 
        if hh_Mt < 250: continue     
        histos['cutFlow'].Fill(7,1)           
        

        histos['btagCSV0'].Fill(tree.Jet_btagCSV[tree.hJCidx[0]])
        histos['btagCSV1'].Fill(tree.Jet_btagCSV[tree.hJCidx[1]])
# tree->Scan("tree.Jet_btagCSV[tree.hJCidx[0]]")
        histos['hZZpt'].Fill(hToZZ_p4.Pt(),evWgt)                 
        histos['hZZmt'].Fill(hToZZ_p4.Mt(),evWgt)                 
        histos['hZZmt_long'].Fill(hToZZ_p4.Mt(),evWgt)                 
        histos['metpt'].Fill(tree.met_pt, evWgt)  
        histos['zMass'].Fill(tree.V_mass, evWgt)
        histos['zHMass'].Fill(visible_p4.M(), evWgt)

        histos['zPt'].Fill(tree.V_pt, evWgt)
        histos['hhMt'].Fill(hh_Mt,evWgt)                 
        histos['hCSVmass'].Fill(Htobb_p4.M(),evWgt)    
        histos['hCSVmass_long'].Fill(Htobb_p4.M(),evWgt)
        histos['zMass_long'].Fill(tree.V_mass, evWgt)
        histos['hCSVpt'].Fill(Htobb_p4.Pt(),evWgt)    
        histos['nleps'].Fill(nLeps, evWgt)    #how many good leptons remains to be in the event
        histos['bjet0pt'] .Fill(bJetsP4[0].Pt() ,evWgt)
        histos['bjet0eta'].Fill(bJetsP4[0].Eta(),evWgt)
        histos['bjet1pt'] .Fill(bJetsP4[1].Pt() ,evWgt)
        histos['bjet1eta'].Fill(bJetsP4[1].Eta(),evWgt)
        
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
    
#work with angular variables
        # dR_leps= lepsP4[0].DeltaR(lepsP4[1])    
        # dR_bjets = bJetsP4[0].DeltaR (bJetsP4[1])
        # dR_ZH = Z_p4.DeltaR(Htobb_p4)
        # dRList = []
        # for l in lepsP4:
        #     for b in bJetsP4:
        #         dRList.append( l.DeltaR( b) )
        # dR_lb_min = min(float(i) for i in dRList )  if len(dRList) != 0 else -10

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

        histos['dEta_leps'].Fill(dEta_leps,evWgt)
        histos['dEta_bjets'].Fill(dEta_bjets,evWgt)
        histos['dEta_ZH'].Fill(dEta_ZH,evWgt)
        histos['dEta_lb_min'].Fill(dEta_lb_min,evWgt)


    #histos['cutFlowLogScale'] = copy.deepcopy(histos['cutFlow']) 

    # check if integral has to start from 0 or 1, read ROOT bin enumeration convention?
        nbins =  histos['cutFlow'].GetXaxis().FindBin(lastEffBin) - histos['cutFlow'].GetXaxis().FindBin(1)
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
                eff = 100* histos['cutFlow'].Integral(bin+1, nbins)/histos['cutFlow'].Integral(1, nbins) #len(binLabels))
                eff_v2 = 100* histos['cutFlow'].GetBinContent(bin+1)/ histos['cutFlow'].GetBinContent(1)
            #print 'dividing {} by {} we get eff {}'.format(histos['cutFlow'].GetBinContent(bin+1), histos['cutFlow'].GetBinContent(1), eff_v2)
            #histos['cutFlowEff'].SetBinContent(bin+1, eff)
                histos['cutFlowEff'].SetBinContent(bin+1, eff_v2)
            #print 'eff is ', eff_v2



        bazinga('about to close IN file')
                        #all done with this file
        if file_ext == '.root':
            fIn.Close()
        elif file_ext == '.txt':
            pass
            print ''#all is fine, txt file as input'
        else:
            print 'fix me later: may be memory leak due to open "fc"'

    #save histograms to file
    fOut=ROOT.TFile.Open(outFileURL,'RECREATE')
    for key in histos: histos[key].Write()
    bazinga('about to close Out file')
    fOut.Close()
    

"""
Wrapper to be used when run in parallel
"""
def runSimplestAnPacked(args):

    try:
        return runSimplestAn(inFileURLorList=args[0],
                             outFileURL=args[1],
                             xsec=args[2], 
                             denominator=args[3],
                             isSignal = args[4], 
                             splitSignal = args[5], 
                             whichChannel = args[6])
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
    parser.add_option('-j', '--json',		 dest='json'  ,		 help='json with list of files',	  default=None,		   type='string')
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
            #print fileWithTrees
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
                outFileURL = '%s/%s_%s.root' % (opt.outDir,sample,splitSignal )
            else:
                outFileURL = '%s/%s.root' % (opt.outDir,sample)
                #taskList.append( (inFileURL,outFileURL,xsec, denominator) )
            taskList.append( (fileWithTrees,outFileURL,xsec, denominator, isSignal, splitSignal, whichChannel) )
    else:
        inFileURL  = inGlobalFile
        xsec = None
        print '************* this is debug run*************'
        outFileURL = '%s/%s.root' % (opt.outDir,"plots")
        taskList.append( (inFileURL,outFileURL,xsec, denominator, isSignal, splitSignal, whichChannel) )
  
    # take into account this info:
    # http://stackoverflow.com/questions/24728084/why-does-this-implementation-of-multiprocessing-pool-not-work
    #run the analysis jobs
    if opt.njobs == 0:
        for inFileURL, outFileURL, xsec, denominator, isSignal, splitSignal in taskList:
            runSimplestAn(inFileURL=inFileURL, outFileURL=outFileURL, xsec=xsec, denominator=denominator, isSignal = isSignal, splitSignal=splitSignal, whichChannel=whichChannel )
    else:
        from multiprocessing import Pool, Process
        #from pathos.multiprocessing import ProcessingPool as Pool
        pool = Pool(opt.njobs)
        
#        try:
            #funct= runSimplestAn(inFileURL=inFileURL, outFileURL=outFileURL, xsec=xsec, denominator=denominator)
            # apply runSimplestAn fcn to each object in the taskList with the hepl of map()
            #pool.map(funct,taskList)
        pool.map(runSimplestAnPacked,taskList)
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


