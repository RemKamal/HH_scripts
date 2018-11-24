#!/usr/bin/envevw python

from rootpy.tree import Tree, TreeModel
from rootpy.tree import IntCol, FloatCol, FloatArrayCol, IntArrayCol
from rootpy.io import root_open
import inspect

from LeptonSF import LeptonSF
import sys

#reload(sys)
#sys.setdefaultencoding('utf-8')


import optparse
import os, io # f@cking Python 2.X

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
import itertools

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
fullDebug = False
debugFractionOfEvents = 1./5 #*1./5 additionally for BG

if fullDebug:
    debugRun = True # for quick runs with debugFractionOfEvents
    debugMode = True # for priting with bazinga
else:
    #set manually
    debugRun = False # for quick runs with debugFractionOfEvents                                               
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


def computeSF(weight_SF, weight):
    '''Combines SF of each leg to compute final event SF'''
    weight_SF[0] = (weight[0][0]*weight[1][0])
    weight_SF[1] = ( (weight[0][0]-weight[0][1])*(weight[1][0]-weight[1][1]) )
    weight_SF[2] = ( (weight[0][0]+weight[0][1])*(weight[1][0]+weight[1][1]) )

def computeSF_leg(leg, weight):
    #leg is the leg index, can be 0 or 1
    eff_leg = [1.,0.,0.]
    eff_leg[0] = (weight[leg][0])
    eff_leg[1] = weight[leg][0]-weight[leg][1]
    eff_leg[2] = weight[leg][0]+weight[leg][1]
    return eff_leg

def getLumiAvrgSF(weightLum1, lum1, weightLum2, lum2, weight_SF):
    ##Take SF for two different run categorie and makes lumi average'''
    #print 'weightLum1[0] is', weightLum1[0]
    #print 'weightLum1[1] is', weightLum1[1]
    #print 'weightLum1[2] is', weightLum1[2]
    #print 'weightLum2[0] is', weightLum2[0]
    #print 'weightLum2[1] is', weightLum2[1]
    #print 'weightLum2[2] is', weightLum2[2]

    weight_SF[0] = weightLum1[0]*lum1+weightLum2[0]*lum2
    weight_SF[1] = weightLum1[1]*lum1+weightLum2[1]*lum2
    weight_SF[2] = weightLum1[2]*lum1+weightLum2[2]*lum2

def computeEventSF_fromleg(effleg1, effleg2):
    #returns event efficiency and relative uncertainty
    eff_event = [1.,0.]
    eff_event[0] = ((effleg1[0][0]**2*effleg2[1][0] + effleg1[1][0]**2*effleg2[0][0])/(effleg1[0][0] + effleg1[1][0]))
    #relative uncertainty down
    uncert_down = (abs(((effleg1[0][1]**2*effleg2[1][1] + effleg1[1][1]**2*effleg2[0][1])/(effleg1[0][1] + effleg1[1][1])) - eff_event[0])/eff_event[0])
    #relative uncertainty up
    uncert_up = (abs(((effleg1[0][2]**2*effleg2[1][2] + effleg1[1][2]**2*effleg2[0][2])/(effleg1[0][2] + effleg1[1][2])) - eff_event[0])/eff_event[0])
    eff_event[1]  = (uncert_down+uncert_up)/2.
    return eff_event


def computeEvenSF_DZ(eff):
    eff_event = [1.,0.]
    eff_event[0] = ((eff[0][0]**2 + eff[1][0]**2)/(eff[0][0] + eff[1][0]))
    #relative uncertainty down
    uncert_down = (((eff[0][1]**2 + eff[1][1]**2)/(eff[0][1] + eff[1][1])) - eff_event[0])/eff_event[0]
    #relative uncertainty up
    uncert_up = (((eff[0][2]**2 + eff[1][2]**2)/(eff[0][2] + eff[1][2])) - eff_event[0])/eff_event[0]
    eff_event[1]  = (uncert_down+uncert_up)/2.
    return eff_event



SFjsons = {
    #
    #Muon#########################
    #
    #ID and ISO
    'json/V25/muon_ID_BCDEFv2.json' : ['MC_NUM_LooseID_DEN_genTracks_PAR_pt_eta', 'abseta_pt_ratio'],
    'json/V25/muon_ID_GHv2.json' : ['MC_NUM_LooseID_DEN_genTracks_PAR_pt_eta', 'abseta_pt_ratio'],
    'json/V25/muon_ISO_BCDEFv2.json' : ['LooseISO_LooseID_pt_eta', 'abseta_pt_ratio'],
    'json/V25/muon_ISO_GHv2.json' : ['LooseISO_LooseID_pt_eta', 'abseta_pt_ratio'],
    #Tracker
    'json/V25/trk_SF_RunBCDEF.json' : ['Graph', 'ratio_eff_eta3_dr030e030_corr'],
    'json/V25/trk_SF_RunGH.json' : ['Graph', 'ratio_eff_eta3_dr030e030_corr'],
    #Trigg
    #BCDEFG
    'json/V25/Data_EfficienciesAndSF_doublehlt_perleg_RunBCDEFG_leg8.json' : ['MC_NUM_hlt_Mu17_Mu8_OR_TkMu8_leg8_DEN_LooseIDnISO_PAR_pt_eta', 'abseta_pt_DATA'],
    'json/V25/Data_EfficienciesAndSF_doublehlt_perleg_RunBCDEFG_leg17.json' : ['MC_NUM_hlt_Mu17Mu8_leg17_DEN_LooseIDnISO_PAR_pt_eta', 'abseta_pt_DATA'],
    'json/V25/MC_EfficienciesAndSF_doublehlt_perleg_RunBCDEFG_leg8.json' : ['MC_NUM_hlt_Mu17_Mu8_OR_TkMu8_leg8_DEN_LooseIDnISO_PAR_pt_eta', 'abseta_pt_MC'],
    'json/V25/MC_EfficienciesAndSF_doublehlt_perleg_RunBCDEFG_leg17.json' : ['MC_NUM_hlt_Mu17Mu8_leg17_DEN_LooseIDnISO_PAR_pt_eta', 'abseta_pt_MC'],
    #H
    #no DZ
    'json/V25/Data_EfficienciesAndSF_doublehlt_perleg_RunH_leg8.json' : ['MC_NUM_hlt_Mu17_Mu8_OR_TkMu8_leg8_DEN_LooseIDnISO_PAR_pt_eta', 'abseta_pt_DATA'],
    'json/V25/Data_EfficienciesAndSF_doublehlt_perleg_RunH_leg17.json' : ['MC_NUM_hlt_Mu17Mu8_leg17_DEN_LooseIDnISO_PAR_pt_eta', 'abseta_pt_DATA'],
    'json/V25/MC_EfficienciesAndSF_doublehlt_perleg_RunH_leg8.json' : ['MC_NUM_hlt_Mu17_Mu8_OR_TkMu8_leg8_DEN_LooseIDnISO_PAR_pt_eta', 'abseta_pt_MC'],
    'json/V25/MC_EfficienciesAndSF_doublehlt_perleg_RunH_leg17.json' : ['MC_NUM_hlt_Mu17Mu8_leg17_DEN_LooseIDnISO_PAR_pt_eta', 'abseta_pt_MC'],
    #with DZ
    'json/V25/DATA_EfficienciesAndSF_dZ_numH.json' : ['MC_NUM_dZ_DEN_hlt_Mu17_Mu8_OR_TkMu8_loose_PAR_eta1_eta2', 'tag_abseta_abseta_DATA'],
    'json/V25/MC_EfficienciesAndSF_dZ_numH.json' : ['MC_NUM_dZ_DEN_hlt_Mu17_Mu8_OR_TkMu8_loose_PAR_eta1_eta2', 'tag_abseta_abseta_MC'],
    #
    #Electron #####################
    #
    #ID and ISO
    'json/V25/EIDISO_ZH_out.json' : ['EIDISO_ZH', 'eta_pt_ratio'],
    #Tracker
    'json/V25/ScaleFactor_etracker_80x.json' : ['ScaleFactor_tracker_80x', 'eta_pt_ratio'],
    #Trigg
    'json/V25/DiEleLeg1AfterIDISO_out.json' : ['DiEleLeg1AfterIDISO', 'eta_pt_ratio'],
    'json/V25/DiEleLeg2AfterIDISO_out.json' : ['DiEleLeg2AfterIDISO', 'eta_pt_ratio']
    }




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
    btagDiscr0 = FloatCol()
    bpt0 = FloatCol()
    beta0 = FloatCol()
    bphi0 = FloatCol()
    bmass0 = FloatCol()

    leppt0 = FloatCol()
    lepeta0 = FloatCol()
    lepphi0 = FloatCol()
    lepmass0 = FloatCol()

    btagDiscr1 = FloatCol()
    bpt1 = FloatCol()
    beta1 = FloatCol()
    bphi1 = FloatCol()
    bmass1 = FloatCol()

    leppt1 = FloatCol()
    lepeta1 = FloatCol()
    lepphi1 = FloatCol()
    lepmass1 = FloatCol()

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

    Jet_btagWeightCMVAV2lead = FloatCol()
    Jet_btagWeightCMVAV2sublead = FloatCol()
    # metpt = FloatCol()
    # meteta = FloatCol()
    # metphi = FloatCol()

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


    met_sig = FloatCol()
    met_covXX = FloatCol()
    met_covXY = FloatCol()
    met_covYY = FloatCol()
    met_rawpt = FloatCol()
    metPuppi_pt = FloatCol()
    metPuppi_phi = FloatCol()
    metPuppi_rawpt = FloatCol()
    metType1p2_pt = FloatCol()
    met_shifted_UnclusteredEnUp_pt = FloatCol()
    met_shifted_UnclusteredEnUp_phi = FloatCol()
    met_shifted_UnclusteredEnUp_sumEt = FloatCol()
    met_shifted_UnclusteredEnDown_pt = FloatCol()
    met_shifted_UnclusteredEnDown_phi = FloatCol()
    met_shifted_UnclusteredEnDown_sumEt = FloatCol()
    met_shifted_JetResUp_pt = FloatCol()
    met_shifted_JetResUp_phi = FloatCol()
    met_shifted_JetResUp_sumEt = FloatCol()
    met_pt = FloatCol()
    met_eta = FloatCol()
    met_phi = FloatCol()
    met_mass = FloatCol()
    met_sumEt = FloatCol()
    met_rawPt = FloatCol()
    met_rawPhi = FloatCol()
    met_rawSumEt = FloatCol()
    met_genPt = FloatCol()
    met_genPhi = FloatCol()
    met_genEta = FloatCol()
    met_shifted_JetEnUp_pt = FloatCol()
    met_shifted_JetEnUp_phi = FloatCol()
    met_shifted_JetEnUp_sumEt = FloatCol()
    met_shifted_JetEnDown_pt = FloatCol()
    met_shifted_JetEnDown_phi = FloatCol()
    met_shifted_JetEnDown_sumEt = FloatCol()
    met_shifted_MuonEnUp_pt = FloatCol()
    met_shifted_MuonEnUp_phi = FloatCol()
    met_shifted_MuonEnUp_sumEt = FloatCol()
    met_shifted_MuonEnDown_pt = FloatCol()
    met_shifted_MuonEnDown_phi = FloatCol()
    met_shifted_MuonEnDown_sumEt = FloatCol()
    met_shifted_ElectronEnUp_pt = FloatCol()
    met_shifted_ElectronEnUp_phi = FloatCol()
    met_shifted_ElectronEnUp_sumEt = FloatCol()
    met_shifted_ElectronEnDown_pt = FloatCol()
    met_shifted_ElectronEnDown_phi = FloatCol()
    met_shifted_ElectronEnDown_sumEt = FloatCol()
    met_shifted_TauEnUp_pt = FloatCol()
    met_shifted_TauEnUp_phi = FloatCol()
    met_shifted_TauEnUp_sumEt = FloatCol()
    met_shifted_TauEnDown_pt = FloatCol()
    met_shifted_TauEnDown_phi = FloatCol()
    met_shifted_TauEnDown_sumEt = FloatCol()
    met_shifted_JetResDown_pt = FloatCol()
    met_shifted_JetResDown_phi = FloatCol()
    met_shifted_JetResDown_sumEt = FloatCol()

    Jet_hadronFlavour = IntArrayCol(40)

    weight_SF_TRK = FloatArrayCol(3)
    weight_SF_LooseID = FloatArrayCol(3)
    weight_SF_LooseIDnISO = FloatArrayCol(3)
    weight_SF_LooseISO = FloatArrayCol(3)
    weight_SF_Dilep = FloatArrayCol(3)


    Jet_btagCMVAV2 = FloatArrayCol(40)
    Jet_btagCMVAV2L_SF = FloatArrayCol(40)
    Jet_btagCMVAV2L_SF_up = FloatArrayCol(40)
    Jet_btagCMVAV2L_SF_down = FloatArrayCol(40)
    Jet_btagCMVAV2M_SF = FloatArrayCol(40)
    Jet_btagCMVAV2M_SF_up = FloatArrayCol(40)
    Jet_btagCMVAV2M_SF_down = FloatArrayCol(40)
    Jet_btagCMVAV2T_SF = FloatArrayCol(40)
    Jet_btagCMVAV2T_SF_up = FloatArrayCol(40)
    Jet_btagCMVAV2T_SF_down = FloatArrayCol(40)
    Jet_btagWeightCMVAV2 = FloatArrayCol(40)
    Jet_btagWeightCMVAV2_up_jes = FloatArrayCol(40)
    Jet_btagWeightCMVAV2_down_jes = FloatArrayCol(40)
    Jet_btagWeightCMVAV2_up_lf = FloatArrayCol(40)
    Jet_btagWeightCMVAV2_down_lf = FloatArrayCol(40)
    Jet_btagWeightCMVAV2_up_hf = FloatArrayCol(40)
    Jet_btagWeightCMVAV2_down_hf = FloatArrayCol(40)
    Jet_btagWeightCMVAV2_up_hfstats1 = FloatArrayCol(40)
    Jet_btagWeightCMVAV2_down_hfstats1 = FloatArrayCol(40)
    Jet_btagWeightCMVAV2_up_hfstats2 = FloatArrayCol(40)
    Jet_btagWeightCMVAV2_down_hfstats2 = FloatArrayCol(40)
    Jet_btagWeightCMVAV2_up_lfstats1 = FloatArrayCol(40)
    Jet_btagWeightCMVAV2_down_lfstats1 = FloatArrayCol(40)
    Jet_btagWeightCMVAV2_up_lfstats2 = FloatArrayCol(40)
    Jet_btagWeightCMVAV2_down_lfstats2 = FloatArrayCol(40)
    Jet_btagWeightCMVAV2_up_cferr1 = FloatArrayCol(40)
    Jet_btagWeightCMVAV2_down_cferr1 = FloatArrayCol(40)
    Jet_btagWeightCMVAV2_up_cferr2 = FloatArrayCol(40)
    Jet_btagWeightCMVAV2_down_cferr2 = FloatArrayCol(40)

    Jet_pt = FloatArrayCol(40)
    Jet_eta = FloatArrayCol(40)
    Jet_phi = FloatArrayCol(40)
    Jet_mass = FloatArrayCol(40)
    
    vLeptons_pt = FloatArrayCol(40)
    vLeptons_eta = FloatArrayCol(40)
    vLeptons_phi = FloatArrayCol(40)
    vLeptons_mass = FloatArrayCol(40)
    

    Jet_corr_JECUp = FloatArrayCol(40)
    Jet_corr_JECDown = FloatArrayCol(40)
    Jet_corr = FloatArrayCol(40)
    Jet_corr_JERUp = FloatArrayCol(40)
    Jet_corr_JERDown = FloatArrayCol(40)
    Jet_corr_JER = FloatArrayCol(40)
    Jet_corr_AbsoluteStatUp = FloatArrayCol(40)
    Jet_corr_AbsoluteStatDown = FloatArrayCol(40)
    Jet_corr_AbsoluteScaleUp = FloatArrayCol(40)
    Jet_corr_AbsoluteScaleDown = FloatArrayCol(40)
    Jet_corr_AbsoluteFlavMapUp = FloatArrayCol(40)
    Jet_corr_AbsoluteFlavMapDown = FloatArrayCol(40)
    Jet_corr_AbsoluteMPFBiasUp = FloatArrayCol(40)
    Jet_corr_AbsoluteMPFBiasDown = FloatArrayCol(40)
    Jet_corr_FragmentationUp = FloatArrayCol(40)
    Jet_corr_FragmentationDown = FloatArrayCol(40)
    Jet_corr_SinglePionECALUp = FloatArrayCol(40)
    Jet_corr_SinglePionECALDown = FloatArrayCol(40)
    Jet_corr_SinglePionHCALUp = FloatArrayCol(40)
    Jet_corr_SinglePionHCALDown = FloatArrayCol(40)
    Jet_corr_FlavorQCDUp = FloatArrayCol(40)
    Jet_corr_FlavorQCDDown = FloatArrayCol(40)
    Jet_corr_TimePtEtaUp = FloatArrayCol(40)
    Jet_corr_TimePtEtaDown = FloatArrayCol(40)
    Jet_corr_RelativeJEREC1Up = FloatArrayCol(40)
    Jet_corr_RelativeJEREC1Down = FloatArrayCol(40)
    Jet_corr_RelativeJEREC2Up = FloatArrayCol(40)
    Jet_corr_RelativeJEREC2Down = FloatArrayCol(40)
    Jet_corr_RelativeJERHFUp = FloatArrayCol(40)
    Jet_corr_RelativeJERHFDown = FloatArrayCol(40)
    Jet_corr_RelativePtBBUp = FloatArrayCol(40)
    Jet_corr_RelativePtBBDown = FloatArrayCol(40)
    Jet_corr_RelativePtEC1Up = FloatArrayCol(40)
    Jet_corr_RelativePtEC1Down = FloatArrayCol(40)
    Jet_corr_RelativePtEC2Up = FloatArrayCol(40)
    Jet_corr_RelativePtEC2Down = FloatArrayCol(40)
    Jet_corr_RelativePtHFUp = FloatArrayCol(40)
    Jet_corr_RelativePtHFDown = FloatArrayCol(40)
    Jet_corr_RelativeBalUp = FloatArrayCol(40)
    Jet_corr_RelativeBalDown = FloatArrayCol(40)
    Jet_corr_RelativeFSRUp = FloatArrayCol(40)
    Jet_corr_RelativeFSRDown = FloatArrayCol(40)
    Jet_corr_RelativeStatFSRUp = FloatArrayCol(40)
    Jet_corr_RelativeStatFSRDown = FloatArrayCol(40)
    Jet_corr_RelativeStatECUp = FloatArrayCol(40)
    Jet_corr_RelativeStatECDown = FloatArrayCol(40)
    Jet_corr_RelativeStatHFUp = FloatArrayCol(40)
    Jet_corr_RelativeStatHFDown = FloatArrayCol(40)
    Jet_corr_PileUpDataMCUp = FloatArrayCol(40)
    Jet_corr_PileUpDataMCDown = FloatArrayCol(40)
    Jet_corr_PileUpPtRefUp = FloatArrayCol(40)
    Jet_corr_PileUpPtRefDown = FloatArrayCol(40)
    Jet_corr_PileUpPtBBUp = FloatArrayCol(40)
    Jet_corr_PileUpPtBBDown = FloatArrayCol(40)
    Jet_corr_PileUpPtEC1Up = FloatArrayCol(40)
    Jet_corr_PileUpPtEC1Down = FloatArrayCol(40)
    Jet_corr_PileUpPtEC2Up = FloatArrayCol(40)
    Jet_corr_PileUpPtEC2Down = FloatArrayCol(40)
    Jet_corr_PileUpPtHFUp = FloatArrayCol(40)
    Jet_corr_PileUpPtHFDown = FloatArrayCol(40)
    Jet_corr_PileUpMuZeroUp = FloatArrayCol(40)
    Jet_corr_PileUpMuZeroDown = FloatArrayCol(40)
    Jet_corr_PileUpEnvelopeUp = FloatArrayCol(40)
    Jet_corr_PileUpEnvelopeDown = FloatArrayCol(40)
    Jet_corr_SubTotalPileUpUp = FloatArrayCol(40)
    Jet_corr_SubTotalPileUpDown = FloatArrayCol(40)
    Jet_corr_SubTotalRelativeUp = FloatArrayCol(40)
    Jet_corr_SubTotalRelativeDown = FloatArrayCol(40)
    Jet_corr_SubTotalPtUp = FloatArrayCol(40)
    Jet_corr_SubTotalPtDown = FloatArrayCol(40)
    Jet_corr_SubTotalScaleUp = FloatArrayCol(40)
    Jet_corr_SubTotalScaleDown = FloatArrayCol(40)
    Jet_corr_SubTotalAbsoluteUp = FloatArrayCol(40)
    Jet_corr_SubTotalAbsoluteDown = FloatArrayCol(40)
    Jet_corr_SubTotalMCUp = FloatArrayCol(40)
    Jet_corr_SubTotalMCDown = FloatArrayCol(40)
    Jet_corr_TotalUp = FloatArrayCol(40)
    Jet_corr_TotalDown = FloatArrayCol(40)
    Jet_corr_TotalNoFlavorUp = FloatArrayCol(40)
    Jet_corr_TotalNoFlavorDown = FloatArrayCol(40)
    Jet_corr_TotalNoTimeUp = FloatArrayCol(40)
    Jet_corr_TotalNoTimeDown = FloatArrayCol(40)
    Jet_corr_TotalNoFlavorNoTimeUp = FloatArrayCol(40)
    Jet_corr_TotalNoFlavorNoTimeDown = FloatArrayCol(40)
    Jet_corr_FlavorZJetUp = FloatArrayCol(40)
    Jet_corr_FlavorZJetDown = FloatArrayCol(40)
    Jet_corr_FlavorPhotonJetUp = FloatArrayCol(40)
    Jet_corr_FlavorPhotonJetDown = FloatArrayCol(40)
    Jet_corr_FlavorPureGluonUp = FloatArrayCol(40)
    Jet_corr_FlavorPureGluonDown = FloatArrayCol(40)
    Jet_corr_FlavorPureQuarkUp = FloatArrayCol(40)
    Jet_corr_FlavorPureQuarkDown = FloatArrayCol(40)
    Jet_corr_FlavorPureCharmUp = FloatArrayCol(40)
    Jet_corr_FlavorPureCharmDown = FloatArrayCol(40)
    Jet_corr_FlavorPureBottomUp = FloatArrayCol(40)
    Jet_corr_FlavorPureBottomDown = FloatArrayCol(40)
    Jet_corr_TimeRunBCDUp = FloatArrayCol(40)
    Jet_corr_TimeRunBCDDown = FloatArrayCol(40)
    Jet_corr_TimeRunEFUp = FloatArrayCol(40)
    Jet_corr_TimeRunEFDown = FloatArrayCol(40)
    Jet_corr_TimeRunGUp = FloatArrayCol(40)
    Jet_corr_TimeRunGDown = FloatArrayCol(40)
    Jet_corr_TimeRunHUp = FloatArrayCol(40)
    Jet_corr_TimeRunHDown = FloatArrayCol(40)
    Jet_corr_CorrelationGroupMPFInSituUp = FloatArrayCol(40)
    Jet_corr_CorrelationGroupMPFInSituDown = FloatArrayCol(40)
    Jet_corr_CorrelationGroupIntercalibrationUp = FloatArrayCol(40)
    Jet_corr_CorrelationGroupIntercalibrationDown = FloatArrayCol(40)
    Jet_corr_CorrelationGroupbJESUp = FloatArrayCol(40)
    Jet_corr_CorrelationGroupbJESDown = FloatArrayCol(40)
    Jet_corr_CorrelationGroupFlavorUp = FloatArrayCol(40)
    Jet_corr_CorrelationGroupFlavorDown = FloatArrayCol(40)
    Jet_corr_CorrelationGroupUncorrelatedUp = FloatArrayCol(40)
    Jet_corr_CorrelationGroupUncorrelatedDown = FloatArrayCol(40)

    hJCMVAV2idx = IntArrayCol(40)   
    hJidx = IntArrayCol(40)   
    
    puWeight = FloatCol()
    puWeightUp = FloatCol()
    puWeightDown = FloatCol()
    genWeight= FloatCol()


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
        'btagCMVAV20'       :ROOT.TH1F('btagCMVAV20'	,';Leading b-Jet CMVAV2 SF; Events'	    , 60, 0.4, 1.),
        'btagCMVAV21'       :ROOT.TH1F('btagCMVAV21'	,';Subleading b-Jet CMVAV2 SF; Events'	    , 60, 0.4, 1.),
        'lep0pt'	:ROOT.TH1F('lep0pt'		,';Leading Lepton p_{T} [GeV]; Events'		, 25, 0., 250.),
        'lep1pt'	:ROOT.TH1F('lep1pt'		,';Subleading Lepton p_{T} [GeV]; Events'	, 20, 0., 200.),
        'lep0eta'	:ROOT.TH1F('lep0eta'	,';Leading Lepton #eta ; Events'		    , 20, -2.4, 2.4),
        'lep1eta'	:ROOT.TH1F('lep1eta'	,';Subleading Lepton #eta ; Events'	        , 20, -2.4, 2.4),
        'hCMVAV2mass'      :ROOT.TH1F('hCMVAV2mass', ';HCMVAV2 mass [GeV]; Events', 40, 85, 165),
        'hCMVAV2mass_long'      :ROOT.TH1F('hCMVAV2mass_long', ';HCMVAV2 mass [GeV]; Events', 45, 30, 220),
        'hCMVAV2pt'      :ROOT.TH1F('hCMVAV2pt', ';HCMVAV2 p_{T} [GeV]; Events', 50, 0, 400),
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
        'btagCMVAV20_beforeMETcut'       :ROOT.TH1F('btagCMVAV20_beforeMETcut'	,';Leading b-Jet CMVAV2 SF; Events'	    , 60, 0.4, 1.),
        'btagCMVAV21_beforeMETcut'       :ROOT.TH1F('btagCMVAV21_beforeMETcut'	,';Subleading b-Jet CMVAV2 SFt; Events'	    , 60, 0.4, 1.),
        'lep0pt_beforeMETcut'	:ROOT.TH1F('lep0pt_beforeMETcut'		,';Leading Lepton p_{T} [GeV]; Events'		, 25, 0., 250.),
        'lep1pt_beforeMETcut'	:ROOT.TH1F('lep1pt_beforeMETcut'		,';Subleading Lepton p_{T} [GeV]; Events'	, 20, 0., 200.),
        'lep0eta_beforeMETcut'	:ROOT.TH1F('lep0eta_beforeMETcut'	,';Leading Lepton #eta ; Events'		    , 20, -2.4, 2.4),
        'lep1eta_beforeMETcut'	:ROOT.TH1F('lep1eta_beforeMETcut'	,';Subleading Lepton #eta ; Events'	        , 20, -2.4, 2.4),
        'hCMVAV2mass_beforeMETcut'      :ROOT.TH1F('hCMVAV2mass_beforeMETcut', ';HCMVAV2 mass [GeV]; Events', 40, 85, 165),
        'hCMVAV2mass_long_beforeMETcut'      :ROOT.TH1F('hCMVAV2mass_long_beforeMETcut', ';HCMVAV2 mass [GeV]; Events', 45, 30, 220),
        'hCMVAV2pt_beforeMETcut'      :ROOT.TH1F('hCMVAV2pt_beforeMETcut', ';HCMVAV2 p_{T} [GeV]; Events', 50, 0, 400),
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


    ml =['met_sig', 'met_covXX', 'met_covXY', 'met_covYY', 'met_rawpt', 'metPuppi_pt', 'metPuppi_phi', 'metPuppi_rawpt', 'metType1p2_pt', 'met_shifted_UnclusteredEnUp_pt', 'met_shifted_UnclusteredEnUp_phi', 'met_shifted_UnclusteredEnUp_sumEt', 'met_shifted_UnclusteredEnDown_pt', 'met_shifted_UnclusteredEnDown_phi', 'met_shifted_UnclusteredEnDown_sumEt', 'met_shifted_JetResUp_pt', 'met_shifted_JetResUp_phi', 'met_shifted_JetResUp_sumEt', 'met_pt', 'met_eta', 'met_phi', 'met_mass', 'met_sumEt', 'met_rawPt', 'met_rawPhi', 'met_rawSumEt', 'met_genPt', 'met_genPhi', 'met_genEta', 'met_shifted_JetEnUp_pt', 'met_shifted_JetEnUp_phi', 'met_shifted_JetEnUp_sumEt', 'met_shifted_JetEnDown_pt', 'met_shifted_JetEnDown_phi', 'met_shifted_JetEnDown_sumEt', 'met_shifted_MuonEnUp_pt', 'met_shifted_MuonEnUp_phi', 'met_shifted_MuonEnUp_sumEt', 'met_shifted_MuonEnDown_pt', 'met_shifted_MuonEnDown_phi', 'met_shifted_MuonEnDown_sumEt', 'met_shifted_ElectronEnUp_pt', 'met_shifted_ElectronEnUp_phi', 'met_shifted_ElectronEnUp_sumEt', 'met_shifted_ElectronEnDown_pt', 'met_shifted_ElectronEnDown_phi', 'met_shifted_ElectronEnDown_sumEt', 'met_shifted_TauEnUp_pt', 'met_shifted_TauEnUp_phi', 'met_shifted_TauEnUp_sumEt', 'met_shifted_TauEnDown_pt', 'met_shifted_TauEnDown_phi', 'met_shifted_TauEnDown_sumEt', 'met_shifted_JetResDown_pt', 'met_shifted_JetResDown_phi', 'met_shifted_JetResDown_sumEt']

    bl = ['Jet_btagCMVAV2', 'Jet_btagCMVAV2L_SF', 'Jet_btagCMVAV2L_SF_up', 'Jet_btagCMVAV2L_SF_down', 'Jet_btagCMVAV2M_SF', 'Jet_btagCMVAV2M_SF_up', 'Jet_btagCMVAV2M_SF_down', 'Jet_btagCMVAV2T_SF', 'Jet_btagCMVAV2T_SF_up', 'Jet_btagCMVAV2T_SF_down', 'Jet_btagWeightCMVAV2', 'Jet_btagWeightCMVAV2_up_jes', 'Jet_btagWeightCMVAV2_down_jes', 'Jet_btagWeightCMVAV2_up_lf', 'Jet_btagWeightCMVAV2_down_lf', 'Jet_btagWeightCMVAV2_up_hf', 'Jet_btagWeightCMVAV2_down_hf', 'Jet_btagWeightCMVAV2_up_hfstats1', 'Jet_btagWeightCMVAV2_down_hfstats1', 'Jet_btagWeightCMVAV2_up_hfstats2', 'Jet_btagWeightCMVAV2_down_hfstats2', 'Jet_btagWeightCMVAV2_up_lfstats1', 'Jet_btagWeightCMVAV2_down_lfstats1', 'Jet_btagWeightCMVAV2_up_lfstats2', 'Jet_btagWeightCMVAV2_down_lfstats2', 'Jet_btagWeightCMVAV2_up_cferr1', 'Jet_btagWeightCMVAV2_down_cferr1', 'Jet_btagWeightCMVAV2_up_cferr2', 'Jet_btagWeightCMVAV2_down_cferr2']

    cl = ['Jet_corr_JECUp', 'Jet_corr_JECDown', 'Jet_corr', 'Jet_corr_JERUp', 'Jet_corr_JERDown', 'Jet_corr_JER', 'Jet_corr_AbsoluteStatUp', 'Jet_corr_AbsoluteStatDown', 'Jet_corr_AbsoluteScaleUp', 'Jet_corr_AbsoluteScaleDown', 'Jet_corr_AbsoluteFlavMapUp', 'Jet_corr_AbsoluteFlavMapDown', 'Jet_corr_AbsoluteMPFBiasUp', 'Jet_corr_AbsoluteMPFBiasDown', 'Jet_corr_FragmentationUp', 'Jet_corr_FragmentationDown', 'Jet_corr_SinglePionECALUp', 'Jet_corr_SinglePionECALDown', 'Jet_corr_SinglePionHCALUp', 'Jet_corr_SinglePionHCALDown', 'Jet_corr_FlavorQCDUp', 'Jet_corr_FlavorQCDDown', 'Jet_corr_TimePtEtaUp', 'Jet_corr_TimePtEtaDown', 'Jet_corr_RelativeJEREC1Up', 'Jet_corr_RelativeJEREC1Down', 'Jet_corr_RelativeJEREC2Up', 'Jet_corr_RelativeJEREC2Down', 'Jet_corr_RelativeJERHFUp', 'Jet_corr_RelativeJERHFDown', 'Jet_corr_RelativePtBBUp', 'Jet_corr_RelativePtBBDown', 'Jet_corr_RelativePtEC1Up', 'Jet_corr_RelativePtEC1Down', 'Jet_corr_RelativePtEC2Up', 'Jet_corr_RelativePtEC2Down', 'Jet_corr_RelativePtHFUp', 'Jet_corr_RelativePtHFDown', 'Jet_corr_RelativeBalUp', 'Jet_corr_RelativeBalDown', 'Jet_corr_RelativeFSRUp', 'Jet_corr_RelativeFSRDown', 'Jet_corr_RelativeStatFSRUp', 'Jet_corr_RelativeStatFSRDown', 'Jet_corr_RelativeStatECUp', 'Jet_corr_RelativeStatECDown', 'Jet_corr_RelativeStatHFUp', 'Jet_corr_RelativeStatHFDown', 'Jet_corr_PileUpDataMCUp', 'Jet_corr_PileUpDataMCDown', 'Jet_corr_PileUpPtRefUp', 'Jet_corr_PileUpPtRefDown', 'Jet_corr_PileUpPtBBUp', 'Jet_corr_PileUpPtBBDown', 'Jet_corr_PileUpPtEC1Up', 'Jet_corr_PileUpPtEC1Down', 'Jet_corr_PileUpPtEC2Up', 'Jet_corr_PileUpPtEC2Down', 'Jet_corr_PileUpPtHFUp', 'Jet_corr_PileUpPtHFDown', 'Jet_corr_PileUpMuZeroUp', 'Jet_corr_PileUpMuZeroDown', 'Jet_corr_PileUpEnvelopeUp', 'Jet_corr_PileUpEnvelopeDown', 'Jet_corr_SubTotalPileUpUp', 'Jet_corr_SubTotalPileUpDown', 'Jet_corr_SubTotalRelativeUp', 'Jet_corr_SubTotalRelativeDown', 'Jet_corr_SubTotalPtUp', 'Jet_corr_SubTotalPtDown', 'Jet_corr_SubTotalScaleUp', 'Jet_corr_SubTotalScaleDown', 'Jet_corr_SubTotalAbsoluteUp', 'Jet_corr_SubTotalAbsoluteDown', 'Jet_corr_SubTotalMCUp', 'Jet_corr_SubTotalMCDown', 'Jet_corr_TotalUp', 'Jet_corr_TotalDown', 'Jet_corr_TotalNoFlavorUp', 'Jet_corr_TotalNoFlavorDown', 'Jet_corr_TotalNoTimeUp', 'Jet_corr_TotalNoTimeDown', 'Jet_corr_TotalNoFlavorNoTimeUp', 'Jet_corr_TotalNoFlavorNoTimeDown', 'Jet_corr_FlavorZJetUp', 'Jet_corr_FlavorZJetDown', 'Jet_corr_FlavorPhotonJetUp', 'Jet_corr_FlavorPhotonJetDown', 'Jet_corr_FlavorPureGluonUp', 'Jet_corr_FlavorPureGluonDown', 'Jet_corr_FlavorPureQuarkUp', 'Jet_corr_FlavorPureQuarkDown', 'Jet_corr_FlavorPureCharmUp', 'Jet_corr_FlavorPureCharmDown', 'Jet_corr_FlavorPureBottomUp', 'Jet_corr_FlavorPureBottomDown', 'Jet_corr_TimeRunBCDUp', 'Jet_corr_TimeRunBCDDown', 'Jet_corr_TimeRunEFUp', 'Jet_corr_TimeRunEFDown', 'Jet_corr_TimeRunGUp', 'Jet_corr_TimeRunGDown', 'Jet_corr_TimeRunHUp', 'Jet_corr_TimeRunHDown', 'Jet_corr_CorrelationGroupMPFInSituUp', 'Jet_corr_CorrelationGroupMPFInSituDown', 'Jet_corr_CorrelationGroupIntercalibrationUp', 'Jet_corr_CorrelationGroupIntercalibrationDown', 'Jet_corr_CorrelationGroupbJESUp', 'Jet_corr_CorrelationGroupbJESDown', 'Jet_corr_CorrelationGroupFlavorUp', 'Jet_corr_CorrelationGroupFlavorDown', 'Jet_corr_CorrelationGroupUncorrelatedUp', 'Jet_corr_CorrelationGroupUncorrelatedDown']



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
        print '\n', ch, fc, tree
        #print inFileURLorList
        print 'tree.GetEntries() is', tree.GetEntries()
        with io.open (inFileURLorList, mode = 'rt', encoding='utf-8') as f:
            #print f
            listOfFiles = list (f.read().split('\n') )[:-1]
            # loop over root files in the list taken from .txt file
            
            for f in xrange (len(listOfFiles) ):
                print
                print 'processing root file', f, ' for ', inFileURLorList
                fIn=ROOT.TFile.Open(listOfFiles[f])
                if fIn.IsZombie() or not fIn.IsOpen():    
                    print 'error occurred while reading the file, it happens with EOS, rerun.'
                    exit(1)
                else:
                    fileName = fIn.GetName()
                    print 'doing = {0}'.format(fIn)
                    print 'fileNAME is ', fileName
                    #countWeighted += fIn.Get('CountWeighted').GetBinContent(1)
                    #count += fIn.Get('Count').GetBinContent(1)
                    if 'GluGlu' in fileName and 'H' in splitSignal:
                        print 'doing signal HWW or hzz', fileName
                        bazinga('splitSignal is {0}'.format(splitSignal))
                        hToZZ = 1.* tree.Draw("tree.genHiggsDecayMode"," tree.genHiggsDecayMode%1000==23", "goff")
                        hToWW = 1.* tree.Draw("tree.genHiggsDecayMode"," tree.genHiggsDecayMode%1000==24", "goff")
                        hToWWplusCrap = 1.* tree.Draw("tree.genHiggsDecayMode"," tree.genHiggsDecayMode%1000!=23", "goff")
                        hToVV = max(1.* tree.GetEntries(), hToWWplusCrap + hToZZ)
                        bazinga('hToZZ, hToWW, hToWWplusCrap, hToVV are {0} {1} {2} {3}'.format(hToZZ, hToWW, hToWWplusCrap, hToVV))
                        if abs(1.* tree.GetEntries() - (hToWWplusCrap + hToZZ) ) > 10:
                            print 'smth is wrong with the denominator, exiting'
                            sys.exit(1)
                        HtoZZfactor = hToZZ / hToVV
                        HtoWWfactor = hToWWplusCrap / hToVV
                        bazinga('HtoZZfactor, HtoWWfactor are {0} {1}'.format(HtoZZfactor, HtoWWfactor))
            
                        if 'Hzz' in splitSignal:
                            bazinga('in hzz with splitSignal, countWeighted, count, HtoZZfactor, fIn {0} {1} {2} {3} {4}'.format(splitSignal, countWeighted, count, HtoZZfactor, fIn))
                            countWeighted += HtoZZfactor * fIn.Get('CountWeighted').GetBinContent(1)
                            count += HtoZZfactor * fIn.Get('Count').GetBinContent(1)
                        elif 'Hww' in splitSignal:
                            bazinga('in hww with splitSignal, countWeighted, count, HtoZZfactor, fIn {0} {1} {2} {3} {4}'.format(splitSignal, countWeighted, count, HtoWWfactor, fIn))
                            countWeighted += HtoWWfactor * fIn.Get('CountWeighted').GetBinContent(1)
                            count += HtoWWfactor * fIn.Get('Count').GetBinContent(1)
                        elif 'No' in splitSignal:
                            bazinga('in hzz with splitSignal, countWeighted, count, "NO"factor?, fIn {0} {1} {2} {3} {4}'.format(splitSignal, countWeighted, count, HtoZZfactor, fIn))
                            countWeighted += fIn.Get('CountWeighted').GetBinContent(1)
                            count += fIn.Get('Count').GetBinContent(1)
                        else:  
                            print 'cannt happen'
                            sys.exit(1)
                        bazinga('fIn, countWeighted, count are {0} {1} {2}'.format (fIn, countWeighted, count) )
                    else:
                        print 'doing full sample= {0}'.format(fIn)
                        print 'FileName is ', fileName
                        countWeighted += fIn.Get('CountWeighted').GetBinContent(1)
                        count += fIn.Get('Count').GetBinContent(1)
                        bazinga('countWeighted, count are {0} {1} '.format (countWeighted, count) )
                        bazinga('fIn is {0}'.format (str(fIn)) )
                        
                    #             if isSignal: #fix me
    #                count += fIn.Get('Count').GetBinContent(1)
      #          if isSignal: #fix me
     #               print 'File ',fIn, ' has Count equal to ', count
                    print 'File ',fIn, ' has CountWeighted equal to {0} and count to {1}'.format( fIn.Get('CountWeighted').GetBinContent(1), fIn.Get('Count').GetBinContent(1))
                print 
                print 'done with file ', f, ' of ', inFileURLorList
              
            print 
            print '...analysing {0} files in {1} with {2} countWeighted and count {3} events'.format ( len(listOfFiles), inFileURLorList, countWeighted, count )

    if round(countWeighted, 2) ==0:
        countWeighted = count
 
    else:
        print 'something went wrong, bad input file'
        
    if fileName == None:
        print 'filename is None, exiting...'
        exit(1)

    if 'Double' in fileName:
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
        # use 1/25 of BG and 1/5 of signal events when debugging
        branchingRatio = 1
    else:
        if 'Hzz' in splitSignal or '2B2Z' in fileName:
            branchingRatio = branchingRatios[zz]
        elif 'Hww' in splitSignal:
            branchingRatio = branchingRatios[ww]
        else:
            branchingRatio = branchingRatios[vv]
        xsec *= branchingRatio  # 1pb * BR


    if not branchingRatio:
        print 'smth is wrong with branchingRatio, exiting...'
        sys.exit(1)

    if debugRun:
        countWeighted *= debugFractionOfEvents
        count *= debugFractionOfEvents


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
        #print 'event %s' % i
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
            #as in vhbb AN

        elif tree.Vtype == 0:
            #if not tree.HLT_ttH_DL_mumu: continue 
#Int_t OR of ['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v*', 'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v*']*
        
            if not (tree.HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v or tree.HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v or tree.HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v or tree.HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v): continue
            #as in vhbb AN AN2015_168_v12.pdf
            # OR HLT Mu17 TrkIsoVVL Mu8 TrkIsoVVL v* 
            # OR HLT Mu17 TrkIsoVVL TkMu8 TrkIsoVVL v* 
            # OR HLT Mu17 TrkIsoVVL Mu8 TrkIsoVVL DZ v* 
            # OR HLT Mu17 TrkIsoVVL TkMu8 TrkIsoVVL DZ v*
        else:
            continue
            #pass
        histos['cutFlow'].Fill(4,1) #trigger
        
        bazinga('after triggers')

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
            if tree.Jet_btagCMVAV2[ij]>= -0.5884: 
            #pfCombinedMVAV2BJetTagsCombinedMVA v2cMVAv2L -0.5884 cMVAv2_Moriond17_B_H.csv Mistag SFs for light jets are also available for separate periods, see details below hereto be used only in ttbar jet pT regime, new WP!!!
                # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation80XReReco
             #   print 'inside >=0.8'
                nBJets += 1
                bjp4 = jp4
                bJetsListOfTuples.append(( bjp4,tree.Jet_btagCMVAV2[ij]) )
            elif -0.4 < tree.Jet_btagCMVAV2[ij] and tree.Jet_btagCMVAV2[ij] < -0.5884: 
                # -0.4 is totally random 

                nLooseBJets += 1
                lbjp4 = jp4
                looseBJetsListOfTuples.append( (lbjp4,tree.Jet_btagCMVAV2[ij]) )
            else:
                continue #pass
        

        
        #bJetsP4 = []
        #sortedByCMVAV2
        bJetsListOfTuples_tmp = sorted(bJetsListOfTuples, key=itemgetter(1), reverse = True)
        bJetsP4 = map(itemgetter(0), bJetsListOfTuples_tmp )
        bJetsCMVAV2 = map(itemgetter(1), bJetsListOfTuples_tmp )

        looseBJetsListOfTuples_tmp = sorted(looseBJetsListOfTuples, key=itemgetter(1), reverse = True)
        looseBJetsP4_sortedByCMVAV2 = map(itemgetter(0), looseBJetsListOfTuples_tmp )
        looseBJetsCMVAV2 = map(itemgetter(1), looseBJetsListOfTuples_tmp )
        
        # print '*'*1000
        # print 'nBJets is ', nBJets 
        # print 'bJetsCMVAV2:'
        # for el in bJetsCMVAV2:
        #     print el
        # print 'loose cmvav2'
        # for e in looseBJetsCMVAV2:
        #     print e
        # print 'hj...'
        # print tree.Jet_btagCMVAV2[tree.hJCMVAV2idx[0]] 
        # print tree.Jet_btagCMVAV2[tree.hJCMVAV2idx[1]]

        # print 'hjold...'
        # print tree.Jet_btagCMVAV2[tree.hJidx[0]]
        # print tree.Jet_btagCMVAV2[tree.hJidx[1]]
        if xsec is None:
            minitree.Jet_btagWeightCMVAV2lead = -10
            minitree.Jet_btagWeightCMVAV2sublead = -10
        else:
            minitree.Jet_btagWeightCMVAV2lead = tree.Jet_btagWeightCMVAV2[tree.hJCMVAV2idx[0]]      
            minitree.Jet_btagWeightCMVAV2sublead = tree.Jet_btagWeightCMVAV2[tree.hJCMVAV2idx[1]]         

        
        minitree.Jet_pt = tree.Jet_pt
        minitree.Jet_eta = tree.Jet_eta
        minitree.Jet_phi = tree.Jet_phi
        minitree.Jet_mass = tree.Jet_mass 


        minitree.vLeptons_pt = tree.vLeptons_pt
        minitree.vLeptons_eta = tree.vLeptons_eta
        minitree.vLeptons_phi = tree.vLeptons_phi
        minitree.vLeptons_mass = tree.vLeptons_mass 

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
            # if emu==0:
            #     if lp4.Pt()<20:
            #         print 'emu is ', emu
            #         print 'lp4.Pt() is equal to ', lp4.Pt() 
            #         print 'while tree.vLeptons_pt is ', tree.vLeptons_pt[emu]
            #     #if lp4.Pt()<20:
            #         continue #attention, Eta is limited to 2.4
            # else:
            #     if lp4.Pt()<15:
            #         #print 'emu is ', emu
            #         #print 'lp4.Pt() is equal to ', lp4.Pt() 
            #         #print 'while tree.vLeptons_pt is ', tree.vLeptons_pt[emu]
            #         #if lp4.Pt()<15: 
            #         continue

    
            lepsP4.append(lp4)
            nLeps += 1
        
        #print 'nLeps is ', nLeps
        if len(lepsP4) != nvLeps:
            print 'nLeps is {0}, while nvLeps is {1}.'.format ( nLeps, nvLeps )
            sys.exit(1)



        lept1, lept2 = ROOT.TLorentzVector(), ROOT.TLorentzVector()
        lepidx1 = 0#tree.lepidxCMVAV2idx[0]
        lepidx2 = 1#tree.lepidxCMVAV2idx[1]
        lept1.SetPtEtaPhiM(tree.vLeptons_pt[lepidx1],tree.vLeptons_eta[lepidx1],tree.vLeptons_phi[lepidx1],tree.vLeptons_mass[lepidx1])
        lept2.SetPtEtaPhiM(tree.vLeptons_pt[lepidx2],tree.vLeptons_eta[lepidx2],tree.vLeptons_phi[lepidx2],tree.vLeptons_mass[lepidx2])

        #print 'leptons'; print '^'*1000
        # lept1.Print(); lept2.Print()
        # print 'lepsP4:'

        # for idx,l in enumerate(lepsP4):
        #     print '{0}, {1}'.format(idx, str(lepsP4[idx].Print))
        # print '1st lep'
        # if lepsP4[0]: lepsP4[0].Print; 
        # print '2nd lep'
        # lepsP4[1].Print()
        if lepsP4[0] != lept1 or lepsP4[1] !=lept2:
            print 'bad lep'
            sys.exit(1)
        else:
            pass
            #print 'all is awesome'; print '*'*500

        #histos['cutFlow'].Fill(1,1) # no cut         
        bazinga('before njets_raw Fill')



        lumino = 1.       #36800.
        if xsec and countWeighted != 0: 
            if 'GluGlu' in fileName:
                pass#print 'For {0} BR is {1}'.format(fileName, branchingRatio)

            evWgt = xsec * (lumino / countWeighted) 
                # if 'Hzz' in splitSignal or '2B2Z' in fileName:
                #     evWgt *= branchingRatio# * zzFactors[massIdx]
                # elif 'Hww' in splitSignal:
                #     evWgt *= branchingRatio# * wwFactors[massIdx]
                # else:
                #     evWgt *= branchingRatio# * wwFactors[massIdx] #use same factor for total sample
            
            if nBJets > 0:
                evWgt *= 1#bJetsCMVAV2[0]
                if nBJets >1 and 'b' not in physRegion:
                    evWgt *= 1#bJetsCMVAV2[1]
                    #fix me


                        
                    #apply only one btag CMVAV2 SF if it is CR DY with 0 or 1 b-jets

        # fill raw histograms, before any cuts are applied
        # for ANY jet
        histos['njets_raw'].Fill(tree.nJet, evWgt)
        histos['nbjets_raw'].Fill(nBJets, evWgt) # how many remain to be 'good'=loose  b-jets 
        histos['metpt_raw'].Fill(tree.met_pt, evWgt)
        histos['nleps_raw'].Fill(nLeps, evWgt)



        # start HH selection 
        #*******************

        bazinga('asked for b-jets')
        bazinga('nBJets is {0}'.format(nBJets))
        if physRegion == "SR" and not passLoose:
            #print 'doing ', physRegion
            if nBJets < 2 : continue  
        elif physRegion == "SR" and passLoose:
            if nBJets < 2 : continue  #CHANGED
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



        #use this!!
        bj1, bj2 = ROOT.TLorentzVector(), ROOT.TLorentzVector()
        hj1 = tree.hJCMVAV2idx[0]
        hj2 = tree.hJCMVAV2idx[1]
        bj1.SetPtEtaPhiM(tree.Jet_pt[hj1],tree.Jet_eta[hj1],tree.Jet_phi[hj1],tree.Jet_mass[hj1])
        bj2.SetPtEtaPhiM(tree.Jet_pt[hj2],tree.Jet_eta[hj2],tree.Jet_phi[hj2],tree.Jet_mass[hj2])
        
        # print '+'*1000
        # bJetsP4[0].Print() 
        # bJetsP4[1].Print()
        # bj1.Print()
        # bj2.Print()
        #bJetsP4 = [bj1, bj2]
        
        tmpBJet = bJetsP4 + looseBJetsP4_sortedByCMVAV2
        #bJetsP4 = tmpBJet[:2]


        
        Htobb_p4=ROOT.TLorentzVector()	

        bazinga('nbjets and loose jet are: ')
        
        if nBJets==0 and nLooseBJets>=2:
            bazinga('inside 0 bjets')
            Htobb_p4 = looseBJetsP4_sortedByCMVAV2[0] + looseBJetsP4_sortedByCMVAV2[1]
        elif nBJets==1 and nLooseBJets>=1:
            Htobb_p4 = bJetsP4[0] + looseBJetsP4_sortedByCMVAV2[0]
            bazinga('inside 1 bjets')
            
        elif nBJets >=2:
            Htobb_p4 = bJetsP4[0] + bJetsP4[1]
            #both are the same
            #Htobb_p4.SetPtEtaPhiM(tree.HCMVAV2_pt,tree.HCMVAV2_eta,tree.HCMVAV2_phi,tree.HCMVAV2_mass) 
        else:
            #print 'in the continue...'
            continue #pass

        #print '8'*10000
        #print 'nBJets and loose:'
        bazinga (nBJets)
        bazinga(nLooseBJets)
        # print 'len(bJetsP4) is ', len(bJetsP4)
        # print 'bJetsP4: ', bJetsP4
        # print 'len(looseBJetsP4_sortedByCsv) is ', len(looseBJetsP4_sortedByCsv)
        # print 'looseBJetsP4_sortedByCsv ', looseBJetsP4_sortedByCsv
       # print 'after tmpt, bJetsP4 is ', bJetsP4
        tmpBJetsCMVAV2 = bJetsCMVAV2 + looseBJetsCMVAV2
        #print 'tmpBJetsCMVAV2 is ', tmpBJetsCMVAV2

        #bJetsCMVAV2 = tmpBJetsCMVAV2[:2]
        #print 'after tmp, bJetsCMVAV2 is ', bJetsCMVAV2

        bazinga('before Htobb.M')
        bazinga('Htobb_p4.M() is {0}'.format(Htobb_p4.M()) )
        if physRegion == "SR" and not passLoose:
         #   print 'doing ', physRegion
            if Htobb_p4.M() < 90 or Htobb_p4.M() > 150: continue 
        elif physRegion == "SR" and passLoose:
            bazinga('in passloose Htobb_p4.M() is {0}'.format(Htobb_p4.M()) )
            if Htobb_p4.M() < 20: #75 or Htobb_p4.M() > 175: 
                continue
            #if Htobb_p4.M() < 75: continue# or Htobb_p4.M() > 175: continue
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
            #if nLeps > 2: continue  #??????????
        #else:
            #print 'nLeps is', nLeps
            if nLeps != 2: continue 
        histos['cutFlow'].Fill(7, 1)# 2 leptons


        bazinga('before Zmass raw')  
        bazinga('tree.V_mass is {0}'.format(tree.V_mass) )
        if physRegion == "SR" and not passLoose:
            #print 'doing ', physRegion
            if tree.V_mass <76 or tree.V_mass > 106 : continue
        elif physRegion == "SR" and passLoose:
            bazinga('in passLoose with tree.V_mass is {0}'.format(tree.V_mass) )
            #if tree.V_mass < 76: continue# or tree.V_mass > 126 : continue   #CHANGED
            if tree.V_mass < 76:# or tree.V_mass > 126 : 
                continue   #CHANGED
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
            print 'smth is wrong, when doing ', physRegion
            sys.exit(1)


        bazinga ('before TLVs')
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
        #print 'btagCMVAV20_beforeMETcut={0} for fileName={1} with evWgt={2}'.format(bJetsCMVAV2[0], fileName, evWgt)
        bazinga('before bJetCMVAV2')
        histos['btagCMVAV20_beforeMETcut'].Fill(bJetsCMVAV2[0], evWgt)
        histos['btagCMVAV21_beforeMETcut'].Fill(bJetsCMVAV2[1], evWgt)
# tree->Scan("tree.Jet_btagCMVAV2[tree.hJCidx[0]]")
        histos['hZZpt_beforeMETcut'].Fill(hToZZ_p4.Pt(),evWgt)                 
        histos['hZZmt_beforeMETcut'].Fill(hToZZ_p4.Mt(),evWgt)                 
        histos['hZZmt_long_beforeMETcut'].Fill(hToZZ_p4.Mt(),evWgt)                 
        histos['metpt_beforeMETcut'].Fill(tree.met_pt, evWgt)  
        histos['zMass_beforeMETcut'].Fill(tree.V_mass, evWgt)
        histos['zHMass_beforeMETcut'].Fill(visible_p4.M(), evWgt)
        histos['zHTransMass_beforeMETcut'].Fill(visible_p4.Mt(), evWgt)

        histos['zPt_beforeMETcut'].Fill(tree.V_pt, evWgt)

        histos['hCMVAV2mass_beforeMETcut'].Fill(Htobb_p4.M(),evWgt)    
        histos['hCMVAV2mass_long_beforeMETcut'].Fill(Htobb_p4.M(),evWgt)
        histos['zMass_long_beforeMETcut'].Fill(tree.V_mass, evWgt)
        histos['hCMVAV2pt_beforeMETcut'].Fill(Htobb_p4.Pt(),evWgt)    
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


        histos['btagCMVAV20'].Fill(bJetsCMVAV2[0], evWgt)
        histos['btagCMVAV21'].Fill(bJetsCMVAV2[1], evWgt)
# tree->Scan("tree.Jet_btagCMVAV2[tree.hJCidx[0]]")
        histos['hZZpt'].Fill(hToZZ_p4.Pt(),evWgt)                 
        histos['hZZmt'].Fill(hToZZ_p4.Mt(),evWgt)                 
        histos['hZZmt_long'].Fill(hToZZ_p4.Mt(),evWgt)                 
        histos['metpt'].Fill(tree.met_pt, evWgt)  
        histos['zMass'].Fill(tree.V_mass, evWgt)
        histos['zHMass'].Fill(visible_p4.M(), evWgt)
        histos['zHTransMass'].Fill(visible_p4.Mt(), evWgt)
        
        histos['zPt'].Fill(tree.V_pt, evWgt)
        histos['hhMt'].Fill(hh_Mt,evWgt)                 
        histos['hCMVAV2mass'].Fill(Htobb_p4.M(),evWgt)    
        histos['hCMVAV2mass_long'].Fill(Htobb_p4.M(),evWgt)
        histos['zMass_long'].Fill(tree.V_mass, evWgt)
        histos['hCMVAV2pt'].Fill(Htobb_p4.Pt(),evWgt)    
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
        #minitree.metpt = tree.met_pt
        #minitree.meteta = tree.met_eta
        #minitree.metphi = tree.met_phi
        #print 'bJetsCMVAV2[0]', bJetsCMVAV2[0]
        #print 'bJetsCMVAV2[1]', bJetsCMVAV2[1]
        minitree.btagDiscr0 = bJetsCMVAV2[0]
        minitree.btagDiscr1 = bJetsCMVAV2[1]
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
        bazinga('before met for minitree')

        #print 'hJCMVAV2idx value {} and type {}'.format( tree.hJCMVAV2idx, type(tree.hJCMVAV2idx)) 
        #print 'hJidx value {} and type {}'.format( tree.hJidx, type(tree.hJidx)) 
        minitree.hJCMVAV2idx = tree.hJCMVAV2idx
        minitree.hJidx = tree.hJidx
        bazinga('after hJ')
        bazinga('xsec is %s' % xsec)
        if xsec is None:
            
            minitree.puWeight = 1
            minitree.puWeightUp = 1
            minitree.puWeightDown = 1
            minitree.genWeight= 1
            bazinga('before minitree.Jet_hadronFlavour')
            if tree.nJet:
                minitree.Jet_hadronFlavour = [-10]*tree.nJet
            else:
                minitree.Jet_hadronFlavour = [-10]*40
            bazinga('been in data minitree')

        else:
            minitree.puWeight = tree.puWeight
            minitree.puWeightUp = tree.puWeightUp
            minitree.puWeightDown = tree.puWeightDown
            minitree.genWeight= tree.genWeight
            bazinga('before minitree.Jet_hadronFlavour')
            #print 'tree.Jet_hadronFlavour:'
            #print tree.Jet_hadronFlavour
            #print 'tree.nJet:'
            #print tree.nJet
            #if tree.Jet_hadronFlavour:
            minitree.Jet_hadronFlavour = tree.Jet_hadronFlavour 
            #else:
             #   if tree.nJet:
              #      minitree.Jet_hadronFlavour = [-10]*tree.nJet
                #else:
               #     pass
                 #   minitree.Jet_hadronFlavour = [-10]*30
            bazinga('been in MC  minitree')

        bazinga('before mets')
        for el in ml: #['L_SF', 'M_SF', 'T_SF']:    
            #print
            #print el
            #ALL met is in DATA
            value = getattr(tree, el, -10)
            #print 'after get'                                                                       
            #print 'value {} and type {}'.format( value, type(value))                                        
            setattr(minitree, el, value)
            #print 'after set'  
            try:
                newval = getattr(minitree, el)
                #print newval
                #print type(newval)
            except AttributeError as e:
                print e

        bazinga('before corrs')
        for indx, ct in enumerate(cl): #['L_SF', 'M_SF', 'T_SF']:                                            
            #only Jet_corr_JECUp and Jet_corr_JECDown are in DATA
            #print
            #print ct
            value = [-10]*tree.nJet
            if xsec:
                value = getattr(tree, ct, -100)
            elif xsec is None and (ct == 'Jet_corr_JECUp' or ct =='Jet_corr_JECDown)') :
                #print 'doing data for ', ct
                #print 'fileName is', fileName 
                value = getattr(tree, ct, -100)
            else:
                pass

            #print 'after get'
            #print 'element {} of the list has value {} and type {}'.format(indx, value, type(value))
            setattr(minitree, ct, value)
            #print 'after set'
            try:
                newval = getattr(minitree, ct)
                #print newval
                #print type(newval)
            except AttributeError as e:
                print e

        bazinga('before btags')
        for ix, bt in enumerate(bl): #['L_SF', 'M_SF', 'T_SF']:                                    
            #not present in DATA, except Jet_btagCMVAV2
            #print
            #print bt
            value = [-10]*tree.nJet
            if xsec:
                value = getattr(tree, bt, -100)
            elif xsec is None and bt == 'Jet_btagCMVAV2':
                #print 'doing data for ', bt
                #print 'fileName is', fileName
                value = getattr(tree, bt, -100)
            else:
                pass
            #print 'after get'
            #print 'element {} of the list has value {} and type {}'.format(ix, value, type(value))
            setattr(minitree, bt, value)
            #print 'after set'
            try:
                newval = getattr(minitree, bt)
                #print newval
                #print type(newval)
            except AttributeError as e:
                print e

                

        minitree.bdtOutput = -10
        #minitree.bdtOutput_multiclass = -10
        #minitree.dnnOutput = -10

        #ID(will be 1 for electron)
        weight_SF_LooseID= array.array('f',[0]*3)
        weight_SF_LooseID[0], weight_SF_LooseID[1], weight_SF_LooseID[2] = 1,0,0
            #ISO (will be 1 for electron)
        weight_SF_LooseISO = array.array('f',[0]*3)
        weight_SF_LooseISO[0], weight_SF_LooseISO[1], weight_SF_LooseISO[2] = 1,0,0
            #ID and ISO
        weight_SF_LooseIDnISO = array.array('f',[0]*3)
        weight_SF_LooseIDnISO[0], weight_SF_LooseIDnISO[1], weight_SF_LooseIDnISO[2] = 1,0,0
            #Split MVAID sys in barrel or endcap
            #Barrel
        weight_SF_LooseIDnISO_B = array.array('f',[0]*2)
        weight_SF_LooseIDnISO_B[0], weight_SF_LooseIDnISO_B[1] = 0,0
            #Endcap
        weight_SF_LooseIDnISO_E = array.array('f',[0]*2)
        weight_SF_LooseIDnISO_E[0], weight_SF_LooseIDnISO_E[1] = 0,0
            #Tracker
        weight_SF_TRK= array.array('f',[0]*3)
        weight_SF_TRK[0], weight_SF_TRK[1], weight_SF_TRK[2] = 1,0,0
            #Lepton (contains all the SF)
        weight_SF_Lepton = array.array('f',[0]*3)
        weight_SF_Lepton[0],  weight_SF_Lepton[1],  weight_SF_Lepton[2] = 1,0,0
            #double electron Trig
        eTrigSFWeight_doubleEle80x = array.array('f',[0]*3)
        eTrigSFWeight_doubleEle80x[0], eTrigSFWeight_doubleEle80x[1], eTrigSFWeight_doubleEle80x[2] = 1,0,0
            #double muon Trig
        muTrigSFWeight_doublemu= array.array('f',[0]*3)
        muTrigSFWeight_doublemu[0], muTrigSFWeight_doublemu[1], muTrigSFWeight_doublemu[2] = 1,0,0

        
        muID_BCDEF = [1.,0.,0.]
        muID_GH = [1.,0.,0.]
        muISO_BCDEF = [1.,0.,0.]
        muISO_GH = [1.,0.,0.]
        muTRK_BCDEF= [1.0,0.,0.]
        muTRK_GH = [1.0,0.,0.]
        #btagSF = [1.,0.,0.]
                    #for muon trigger
                     #Run BCDEFG
        effDataBCDEFG_leg8 = []
        effDataBCDEFG_leg17= []
        effMCBCDEFG_leg8= []
        effMCBCDEFG_leg17 = []
                     #Run H
        effDataH_leg8 = []
        effDataH_leg17 = []
        effMCH_leg8 = []
        effMCH_leg17 = []
                     #Run H dZ
        effDataH_DZ= []
        effMCH_DZ= []
        #for ele trigger
        eff1, eff1Up, eff1Down = 0, 0, 0
        eff2, eff2Up, eff2Down = 0, 0, 0

        SF_trig_Dilep = 1, 0, 0
        bazinga('before looping over jsons')
        for j, name in SFjsons.iteritems():
            #print j
            
            weight = []
            lepCorr = LeptonSF(j , name[0], name[1])
            #2-D binned SF
            if not j.find('trk_SF_Run') != -1 and not j.find('EfficienciesAndSF_dZ_numH') != -1:
                weight.append(lepCorr.get_2D(lepsP4[0].Pt(), lepsP4[0].Eta()) )
                weight.append(lepCorr.get_2D(lepsP4[1].Pt(), lepsP4[1].Eta()) )
            elif not j.find('trk_SF_Run') != -1 and j.find('EfficienciesAndSF_dZ_numH') != -1:
                weight.append(lepCorr.get_2D(lepsP4[0].Eta(), lepsP4[1].Eta() ) )
                weight.append(lepCorr.get_2D(lepsP4[1].Eta(), lepsP4[0].Eta() ) )
                        #1-D binned SF
            else:
                weight.append(lepCorr.get_1D(lepsP4[0].Eta()))
                weight.append(lepCorr.get_1D(lepsP4[1].Eta()))

            
            if tree.Vtype == 0: #whichChannel ==0
                bazinga('will use jsons for muons')
                #print 'doing muons'
                #IDISO
                if j.find('muon_ID_BCDEF') != -1:
                    computeSF(muID_BCDEF, weight)
                elif j.find('muon_ID_GH') != -1:
                    computeSF(muID_GH, weight)
                elif j.find('muon_ISO_BCDEF') != -1:
                    computeSF(muISO_BCDEF, weight)
                elif j.find('muon_ISO_GH') != -1:
                    computeSF(muISO_GH, weight)
                #TRK
                elif j.find('trk_SF_RunBCDEF') != -1:
                    computeSF(muTRK_BCDEF, weight)
                elif j.find('trk_SF_RunGH') != -1:
                    computeSF(muTRK_GH, weight)
                #TRIG
                elif j.find('EfficienciesAndSF_doublehlt_perleg') != -1:
                    #print 'doing doubke leg'
                #BCDEFG
                    if  j.find('Data_EfficienciesAndSF_doublehlt_perleg_RunBCDEFG_leg8') != -1:
                                    #compute the efficiency for both legs
                        effDataBCDEFG_leg8.append(computeSF_leg(0, weight))
                        effDataBCDEFG_leg8.append(computeSF_leg(1, weight))
                    elif j.find('Data_EfficienciesAndSF_doublehlt_perleg_RunBCDEFG_leg17') != -1:
                        effDataBCDEFG_leg17.append(computeSF_leg(0, weight))
                        effDataBCDEFG_leg17.append(computeSF_leg(1, weight))
                    elif j.find('MC_EfficienciesAndSF_doublehlt_perleg_RunBCDEFG_leg8') != -1:
                        effMCBCDEFG_leg8.append(computeSF_leg(0, weight))
                        effMCBCDEFG_leg8.append(computeSF_leg(1, weight))
                    elif j.find('MC_EfficienciesAndSF_doublehlt_perleg_RunBCDEFG_leg17') != -1:
                        effMCBCDEFG_leg17.append(computeSF_leg(0, weight))
                        effMCBCDEFG_leg17.append(computeSF_leg(1, weight))
                                    #H
                    elif j.find('Data_EfficienciesAndSF_doublehlt_perleg_RunH_leg8') != -1:
                        effDataH_leg8.append(computeSF_leg(0, weight))
                        effDataH_leg8.append(computeSF_leg(1, weight))
                    elif j.find('Data_EfficienciesAndSF_doublehlt_perleg_RunH_leg17') != -1:
                        effDataH_leg17.append(computeSF_leg(0, weight))
                        effDataH_leg17.append(computeSF_leg(1, weight))
                    elif j.find('MC_EfficienciesAndSF_doublehlt_perleg_RunH_leg8') != -1:
                        effMCH_leg8.append(computeSF_leg(0, weight))
                        effMCH_leg8.append(computeSF_leg(1, weight))
                    elif j.find('MC_EfficienciesAndSF_doublehlt_perleg_RunH_leg17') != -1:
                        effMCH_leg17.append(computeSF_leg(0, weight))
                        effMCH_leg17.append(computeSF_leg(1, weight))
                                    #H dZ only
                elif j.find('DATA_EfficienciesAndSF_dZ_numH') != -1:
                        effDataH_DZ.append(computeSF_leg(0, weight))
                        effDataH_DZ.append(computeSF_leg(1, weight))
                        #print 'effDataH_DZ is ', effDataH_DZ
                        #print '0'*5000
                elif j.find('MC_EfficienciesAndSF_dZ_numH') != -1:
                        effMCH_DZ.append(computeSF_leg(0, weight))
                        effMCH_DZ.append(computeSF_leg(1, weight))
                        #print 'effMCH_DZ is', effMCH_DZ
                        #print '0'*5000

            elif tree.Vtype == 1: #whichChannel ==1
                bazinga('will use jsons for eles')
                #IDISO
                if j.find('EIDISO_ZH_out') != -1:
                    computeSF(weight_SF_LooseIDnISO, weight)
                    #computeSF_region(weight_SF_LooseIDnISO_B, weight_SF_LooseIDnISO_E, tree.vLeptons_new_eta[0], tree.vLeptons_new_eta[1], 1.566)
                            #TRK
                elif j.find('ScaleFactor_etracker_80x') != -1:
                    computeSF(weight_SF_TRK, weight)
                            #TRIG
                elif j.find('DiEleLeg1AfterIDISO_out') != -1:
                    eff1 = weight[0][0]
                    eff1Up = (weight[0][0]+weight[0][1])
                    eff1Down = (weight[0][0]-weight[0][1])
                elif j.find('DiEleLeg2AfterIDISO_out') != -1:
                    eff2 = weight[1][0]
                    eff2Up = (weight[1][0]+weight[1][1])
                    eff2Down = (weight[1][0]-weight[1][1])
        print 
        #if not effDataH_leg8:
         #   print 'exiting...'
          #  sys.exit(1)
        
        # print 'weight is', weight
        # for a,b in weight:
        #     if a not in [1.0, 0.0] or b not in [1.0, 0.0]:
        #         print '*'*500
        #         print a
        #         print b
        #     else:
        #         print 'boring'
                              
        # print 'muID_BCDEF is', muID_BCDEF
        
        # bazinga('before mu ID ISO TRK')
        # print muID_BCDEF, muID_GH, muISO_BCDEF, muISO_GH, muTRK_BCDEF, muTRK_GH
        # bazinga('before eff bc...')
        # print effDataBCDEFG_leg8 
        # print effDataBCDEFG_leg17
        # print effMCBCDEFG_leg8
        # print effMCBCDEFG_leg17
        #              #Run H                                                                                                                               
        # bazinga('before H')
        # print effDataH_leg8 
        # print effDataH_leg17 
        # print effMCH_leg8 
        # print effMCH_leg17 
        #              #Run H dZ                                                                                                                              
        # bazinga('before dz')
        # print effDataH_DZ
        # print effMCH_DZ


                            #Fill muon triggers

        if tree.Vtype == 0:
                #print 'muTRK_BCDEF is', muTRK_BCDEF
                #print 'muTRK_GH is', muTRK_GH
                #print 'muID_BCDEF is', muID_BCDEF
                #print 'muID_GH is', muID_GH
                #print 'muISO_BCDEF is', muISO_BCDEF
                #print 'muISO_GH is', muISO_GH

                #Tracker
            getLumiAvrgSF(muTRK_BCDEF,(20.1/36.4),muTRK_GH,(16.3/36.4),weight_SF_TRK)
            #print weight_SF_TRK
                #ID and ISO
            getLumiAvrgSF(muID_BCDEF,(20.1/36.4),muID_GH,(16.3/36.4),weight_SF_LooseID)
            #print weight_SF_LooseID
            getLumiAvrgSF(muISO_BCDEF,(20.1/36.4),muISO_GH,(16.3/36.4),weight_SF_LooseISO)
            #print weight_SF_LooseISO

            weight_SF_LooseIDnISO[0] = weight_SF_LooseID[0]*weight_SF_LooseISO[0]
            weight_SF_LooseIDnISO[1] = weight_SF_LooseID[1]*weight_SF_LooseISO[1]
            weight_SF_LooseIDnISO[2] = weight_SF_LooseID[2]*weight_SF_LooseISO[2]
            #print weight_SF_LooseIDnISO
                #Trigger
                    #BCDEFG no DZ
            EffData_BCDEFG = [1.0,0.]
            EffMC_BCDEFG = [1.0,0.]
            SF_BCDEFG = [1.0,0.,0.]
            bazinga('before compute fromleg')
            EffData_BCDEFG = computeEventSF_fromleg(effDataBCDEFG_leg8,effDataBCDEFG_leg17)
            EffMC_BCDEFG = computeEventSF_fromleg(effMCBCDEFG_leg8,effMCBCDEFG_leg17)
            bazinga('EffData_BCDEFG is {0}'.format(EffData_BCDEFG))
            bazinga('EffMC_BCDEFG is {0}'.format(EffMC_BCDEFG))

            SF_BCDEFG[0] =  (EffData_BCDEFG[0]/EffMC_BCDEFG[0])
            SF_BCDEFG[1] = (1-sqroot(EffData_BCDEFG[1]**2+ EffMC_BCDEFG[1]**2))*SF_BCDEFG[0]
            SF_BCDEFG[2] = (1+sqroot(EffData_BCDEFG[1]**2+ EffMC_BCDEFG[1]**2))*SF_BCDEFG[0]
            bazinga('after SF_BCDEFG = {0}'.format(SF_BCDEFG))
                    #H no DZ
            EffData_H = [1.0,0.]
            EffMC_H = [1.0,0.]
            SF_H = [1.0,0.,0.]
            EffData_H = computeEventSF_fromleg(effDataH_leg8,effDataH_leg17)
            EffMC_H = computeEventSF_fromleg(effMCH_leg8,effMCH_leg17)
            SF_H[0] =  (EffData_H[0]/EffMC_H[0])
            SF_H[1] = (1-sqroot(EffData_H[1]**2+ EffMC_H[1]**2))*SF_H[0]
            SF_H[2] = (1+sqroot(EffData_H[1]**2+ EffMC_H[1]**2))*SF_H[0]
            bazinga('after SF_H = {0}'.format(SF_H))
                    #H DZ SF
            EffData_DZ = [1.0,0.]
            EffMC_DZ = [1.0,0.]
            SF_DZ = [1.0,0.,0.]
            bazinga('effDataH_DZ %s' % effDataH_DZ)
            bazinga('effMCH_DZ %s' % effMCH_DZ)
            EffData_DZ = computeEvenSF_DZ(effDataH_DZ)
            EffMC_DZ = computeEvenSF_DZ(effMCH_DZ)
            bazinga('after EffData_DZ = {0}'.format(EffData_DZ))
            bazinga('after EffMC_DZ={0}'.format(EffMC_DZ))
            #bazinga('after '.format())
            SF_DZ[0] = (EffData_DZ[0]/EffMC_DZ[0])
            SF_DZ[1] = (1-sqroot(EffData_DZ[1]**2+ EffMC_DZ[1]**2))*SF_DZ[0]
            SF_DZ[2] = (1+sqroot(EffData_DZ[1]**2+ EffMC_DZ[1]**2))*SF_DZ[0]
            bazinga('SF_DZ is {0}'.format(SF_DZ) )
                #print 'List of all the double trigger SF + uncert'
                #print 'SF_BCDEFG:', SF_BCDEFG[0], '+', SF_BCDEFG[1], '-', SF_BCDEFG[2]
                #print 'SF_H:', SF_H[0], '+', SF_H[1], '-', SF_H[2]
                #print 'SF_DZ:', SF_DZ[0], '+', SF_DZ[1], '-', SF_DZ[2]
                #Final weight
            bazinga('calc muTrigSFWeight_doublemu')
            muTrigSFWeight_doublemu[0] = (27.221/35.827)*SF_BCDEFG[0] + (8.606/35.827)*SF_H[0]*SF_DZ[0]
            muTrigSFWeight_doublemu[1] = (27.221/35.827)*SF_BCDEFG[1] + (8.606/35.827)*SF_H[1]*SF_DZ[1]
            muTrigSFWeight_doublemu[2] = (27.221/35.827)*SF_BCDEFG[2] + (8.606/35.827)*SF_H[2]*SF_DZ[2]
            SF_trig_Dilep = muTrigSFWeight_doublemu[0], muTrigSFWeight_doublemu[1], muTrigSFWeight_doublemu[2]

                #Final weight

                #OLD
                #Trigger
                #    #BCDEFG no DZ
                #EffData_BCDEFG = ((effDataBCDEFG_leg8[0]**2*effDataBCDEFG_leg17[1] + effDataBCDEFG_leg8[1]**2*effDataBCDEFG_leg17[0])/(effDataBCDEFG_leg8[0] + effDataBCDEFG_leg8[1]))
                #EffMC_BCDEFG = ((effMCBCDEFG_leg8[0]**2*effMCBCDEFG_leg17[1] + effMCBCDEFG_leg8[1]**2*effMCBCDEFG_leg17[0])/(effMCBCDEFG_leg8[0] + effMCBCDEFG_leg8[1]))
                #SF_BCDEFG = EffData_BCDEFG/EffMC_BCDEFG
                #    #H no DZ
                #EffData_H = ((effDataH_leg8[0]**2*effDataH_leg17[1] + effDataH_leg8[1]**2*effDataH_leg17[0])/(effDataH_leg8[0] + effDataH_leg8[1]))
                #EffMC_H = ((effMCH_leg8[0]**2*effMCH_leg17[1] + effMCH_leg8[1]**2*effMCH_leg17[0])/(effMCH_leg8[0] + effMCH_leg8[1]))
                #SF_H = EffData_H/EffMC_H
                #    #H DZ SF
                #EffData_DZ = ((effDataH_DZ[0]**2 + effDataH_DZ[1]**2)/(effDataH_DZ[0] + effDataH_DZ[1]))
                #EffMC_DZ = ((effMCH_DZ[0]**2 + effMCH_DZ[1]**2)/(effMCH_DZ[0] + effMCH_DZ[1]))
                #EffMC_SF = EffData_DZ/EffMC_DZ
                ##Final weight

            
        if tree.Vtype == 1:
            bazinga('calc eTrigSFWeight_doubleEle80x')
            eTrigSFWeight_doubleEle80x[0]     = eff1*(1-eff2)*eff1 + eff2*(1-eff1)*eff2 + eff1*eff1*eff2*eff2
            eTrigSFWeight_doubleEle80x[1] = eff1Down*(1-eff2Down)*eff1Down + eff2Down*(1-eff1Down)*eff2Down + eff1Down*eff1Down*eff2Down*eff2Down
            eTrigSFWeight_doubleEle80x[2]   = eff1Up*(1-eff2Up)*eff1Up + eff2Up*(1-eff1Up)*eff2Up + eff1Up*eff1Up*eff2Up*eff2Up
                #
            SF_trig_Dilep = eTrigSFWeight_doubleEle80x[0], eTrigSFWeight_doubleEle80x[1], eTrigSFWeight_doubleEle80x[2]
                #comput total weight
                #
        #weight_SF_Lepton[0] = weight_SF_TRK[0]*weight_SF_LooseIDnISO[0]
        #weight_SF_Lepton[1] = weight_SF_TRK[1]*weight_SF_LooseIDnISO[1]
        #weight_SF_Lepton[2] = weight_SF_TRK[2]*weight_SF_LooseIDnISO[2]
        bazinga('calc final SFs')
        if xsec is None:# or xsec==1:
            minitree.weight_SF_LooseIDnISO = 1, 0, 0
            minitree.weight_SF_TRK = 1, 0, 0
            minitree.weight_SF_LooseID = 1, 0, 0
            minitree.weight_SF_LooseISO = 1, 0, 0
            minitree.weight_SF_Dilep = 1, 0, 0
        else:
            minitree.weight_SF_LooseIDnISO = (weight_SF_LooseIDnISO[0], weight_SF_LooseIDnISO[1], weight_SF_LooseIDnISO[2])
            minitree.weight_SF_TRK = (weight_SF_TRK[0], weight_SF_TRK[1], weight_SF_TRK[2])
            minitree.weight_SF_LooseID = (weight_SF_LooseID[0], weight_SF_LooseID[1], weight_SF_LooseID[2])
            minitree.weight_SF_LooseISO = (weight_SF_LooseISO[0], weight_SF_LooseISO[1], weight_SF_LooseISO[2])
            minitree.weight_SF_Dilep = SF_trig_Dilep
        #(muTrigSFWeight_doublemu[0], muTrigSFWeight_doublemu[1], muTrigSFWeight_doublemu[2]) if tree.Vtype == 0 else (eTrigSFWeight_doubleEle80x[0], eTrigSFWeight_doubleEle80x[1], eTrigSFWeight_doubleEle80x[2]) if tree.Vtype == 1 else None
        # print 'sfssss'
        # print minitree.weight_SF_TRK; #print type(minitree.weight_SF_TRK)
        # print minitree.weight_SF_Dilep; #print type(minitree.weight_SF_Dilep)
        # print minitree.weight_SF_LooseIDnISO
        # print minitree.weight_SF_LooseID
        # print minitree.weight_SF_LooseISO


        minitree.evWgt = evWgt
        minitree.countWeighted = countWeighted 

        bazinga('before xsec for minitree')
        if xsec is None:# or xsec==1:
                #print 'doing Data'
            bazinga('inside IF for xsec')
            bazinga('xsec is '); bazinga(xsec)
            minitree.xsec = 1
            bazinga('v_id is '); bazinga(v_id)
            minitree.genvbosonpdgid = -100
        else:
            bazinga('inside ELSE for xsec')
            bazinga('file is '); bazinga(fIn)
            bazinga('xsec is '); bazinga(xsec)
            minitree.xsec = xsec
            if v_id:
                bazinga('v_id is '); bazinga(v_id)
                minitree.genvbosonpdgid = v_id
            else:
                minitree.genvbosonpdgid = -100
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
            #print 'all is fine, txt file was an input'
        else:
            print 'fix me later: may be memory leak due to open "fc"'
        #bazinga('about to fill minitree')
        #minitree.fill()
        #bazinga('after fill of minitree')
    bazinga('done with entries')
    if fIn.IsOpen():
        fIn.Close()
    bazinga('about to cd into the fO file')
    fO.cd()
    print 'after cd into the fO file'
    if not passLoose:
        for key in histos: histos[key].Write()
    else:
        print 'in the outpur minitree storing {0} events for {1}'.format(minitree.GetEntries(), outFileURL + outFileName)
        minitree.write()
    #minitree.vals.reset()
    # print tree contents in CMVAV2 format
    
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
    parser.add_option('', '--channel2run',		 dest='channel2run',		 help='channel to run:0=muons, 1=eles',	  default=0,		   type='int')
    (opt, args) = parser.parse_args()

    #read list of samples
    if len(opt.json) != 0:
        jsonFile = open(opt.json,'r')
        samplesList=json.load(jsonFile,encoding='utf-8').items()
        jsonFile.close()

    #prepare output
    if len(opt.outDir) is None: opt.outDir='./'
    os.system('mkdir -p %s' % opt.outDir) #overwrite if exists
    
    channel2run = opt.channel2run
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
        print '-'*50
        print 'samplesList is', samplesList
        print '-'*50
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
            if channel2run != whichChannel:
                print 'error in whichChannel, exiting'
                sys.exit(1)
#            if splitSignal and 'H' in splitSignal:
 #               outFileURL = '%s/%s_%s' % (opt.outDir,sample,splitSignal )
  #          else:
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
        print
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
