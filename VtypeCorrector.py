#!/usr/bin/env python
import ROOT
import numpy as np
import array
import sys

class VtypeCorrector(object):
    now_mm_old_yy = []
    now_ee_old_xx = []
    other_Vtypes = []
    after_other_Vtypes = []

    def __init__(self, tree=None, channel='all'):
        self.channel = channel
        self.lastEntry = -1
        self.nEntries = -1
        self.n_vtype_unchanged = 0
        self.n_vtype0_original = 0
        self.n_vtype1_original = 0
        self.n_ee_reassigned = 0
        self.n_mm_reassigned = 0
        self.n_vtype_changed = 0
        self.n_vtype_events_skipped = 0
        self.branchBuffers = {}
        self.branches = []
        self.tree = None
        ### new branches for Vtype correction ###
        self.branchBuffers['Vtype_new'] = array.array('f', [0])
        self.branches.append({'name': 'Vtype_new', 'formula': self.getBranch, 'arguments': 'Vtype_new'})

        self.vLeptonsvar = ['pt', 'eta', 'phi', 'mass', 'relIso03', 'relIso04']
        for var in self.vLeptonsvar:
            branchName = 'vLeptons_new_%s'%var
            self.branchBuffers[branchName] = np.zeros(21, dtype=np.float32)
            self.branches.append({'name': branchName, 'formula': self.getVectorBranch, 'arguments': {'branch': branchName, 'length':2}, 'length': 2})

        ##define Vleptons branch
        self.Vvar = ['pt', 'eta', 'phi', 'mass']
        self.LorentzDic = {'pt':'Pt', 'eta':'Eta', 'phi':'Phi', 'mass':'M'}
        for var in self.Vvar:
            branchName = 'V_new_%s'%var
            self.branchBuffers[branchName] = np.zeros(21, dtype=np.float32)
            self.branches.append({'name': branchName, 'formula': self.getBranch, 'arguments': branchName})

        if tree:
           self.tree = tree
           self.nEntries = tree.GetEntries()
         
        #self.setTree(tree)
        #self.zEleSelection = lambda x : tree.selLeptons_pt[x] > 15 and tree.selLeptons_eleMVAIdSppring16GenPurp[x] >= 1
        #self.zMuSelection = lambda x : tree.selLeptons_pt[x] > 15 and  tree.selLeptons_looseIdPOG[x] and tree.selLeptons_relIso04[x] < 0.25
        

        self.zEleSelection = lambda x : tree.selLeptons_pt[x] > 15 and tree.selLeptons_eleMVAIdSppring16GenPurp[x] >= 1 and tree.selLeptons_pfRelIso04[x] < 0.25 #and ( 1.4442 > abs(tree.selLeptons_eta[x]) or 1.566 < abs(tree.selLeptons_eta[x]) ) #not (1.4442 < abs(tree.selLeptons_eta[x])  < 1.566)
        self.zMuSelection  = lambda x : tree.selLeptons_pt[x] > 15 and  tree.selLeptons_looseIdPOG[x] and tree.selLeptons_pfRelIso04[x] < 0.25 #and ( 1.4442 > abs(tree.selLeptons_eta[x]) or 1.566 < abs(tree.selLeptons_eta[x]) ) #not (1.4442 < abs(tree.selLeptons_eta[x])  < 1.566)
        
        #??tree.selLeptons_relIso04[x]


    # recompute Vtype, return false to skip the event if Vtype does not match channel
    def processEvent(self, idx):
    #def processEvent(self, event):
        #tree=event
        
        Vtype_new_ = -10
        isGoodEvent = True
        currentEntry = idx #
        #currentEntry = event.GetReadEntry()

        #self.zEleSelection = lambda x : tree.selLeptons_pt[x] > 15 and tree.selLeptons_eleMVAIdSppring16GenPurp[x] >= 1 and tree.selLeptons_pfRelIso04[x] < 0.25 #and ( 1.4442 > abs(tree.selLeptons_eta[x]) or 1.566 < abs(tree.selLeptons_eta[x]) ) #not (1.4442 < abs(tree.selLeptons_eta[x])  < 1.566)
        #self.zMuSelection  = lambda x : tree.selLeptons_pt[x] > 15 and  tree.selLeptons_looseIdPOG[x] and tree.selLeptons_pfRelIso04[x] < 0.25 #and ( 1.4442 > abs(tree.selLeptons_eta[x]) or 1.566 < abs(tree.selLeptons_eta[x]) ) #not (1.4442 < abs(tree.selLeptons_eta[x])  < 1.566)

        if currentEntry%500==0: 
            print 'currentEntry', currentEntry
            print 'self.nEntries'

        print 'currentEntry', currentEntry

        if currentEntry != self.lastEntry and currentEntry < self.nEntries:
            # do processing
            tree=self.tree #event
            event = self.tree

            
            #Variable to store Vtype and leptons info
            Vtype_new_ = -1
            self.branchBuffers['V_new_mass'][0] = -1

            vLeptons_new = []
            #get all the lepton index
            lep_index = range(len(event.selLeptons_pt))

            #vTypeSim = event.VtypeSim
            vType = event.Vtype #[i for i in  lep_index  if event.Vtype ==0]
            #print 'vType', vType
            if vType == 0:
                #print 'tree.selLeptons_pfRelIso04[0]', tree.selLeptons_pfRelIso04[0]
                #print 'tree.selLeptons_pfRelIso04[1]', tree.selLeptons_pfRelIso04[1]
                #print 'tree.selLeptons_eta[0]', tree.selLeptons_eta[0]
                #print 'tree.selLeptons_eta[1]', tree.selLeptons_eta[1]
                self.n_vtype0_original += 1
            elif vType == 1:
                self.n_vtype1_original += 1
            else:
                VtypeCorrector.other_Vtypes.append(vType)

            selectedElectrons = [i for i in  lep_index if abs(event.selLeptons_pdgId[i]) == 11]
            selectedMuons = [i for i in lep_index if abs(event.selLeptons_pdgId[i]) == 13]

            zElectrons = [x for x in selectedElectrons if self.zEleSelection(x)]
            zMuons = [x for x in selectedMuons if self.zMuSelection(x)]

            zMuons.sort(key=lambda x:event.selLeptons_pt[x], reverse=True)
            zElectrons.sort(key=lambda x:event.selLeptons_pt[x], reverse=True)
            

            
            #Zll case. Recompute lepton branches
            if len(zMuons) >=  2 :
                #if tree.Vtype == 0:
                self.n_mm_reassigned += 1
                if vType !=0:
                    #VtypeCorrector.now_mm_old_yy.append((vType, vTypeSim))
                    VtypeCorrector.now_mm_old_yy.append(vType)
                if tree.selLeptons_pt[zMuons[0]] > 20:
                    for i in zMuons[1:]:
                        if  tree.selLeptons_charge[zMuons[0]]*tree.selLeptons_charge[i] < 0:
                            Vtype_new_ = 0
                            for var in self.vLeptonsvar:
                                self.branchBuffers['vLeptons_new_'+var][0] = getattr(tree,'selLeptons_%s'%var)[0]
                                self.branchBuffers['vLeptons_new_'+var][1] = getattr(tree,'selLeptons_%s'%var)[i]
                            break
            elif len(zElectrons) >=  2 :
                #if tree.Vtype == 1:
                self.n_ee_reassigned += 1
                if vType != 1:
                    #VtypeCorrector.now_ee_old_xx.append((vType, vTypeSim))
                    VtypeCorrector.now_ee_old_xx.append(vType)
                if tree.selLeptons_pt[zElectrons[0]] > 20:
                #if tree.selLeptons_pt[zElectrons[0]] > 25:
                    for i in zElectrons[1:]:
                        if  tree.selLeptons_charge[zElectrons[0]]*tree.selLeptons_charge[i] < 0:
                            Vtype_new_ = 1
                            for var in self.vLeptonsvar:
                                self.branchBuffers['vLeptons_new_'+var][0] = getattr(tree,'selLeptons_%s'%var)[0]
                                self.branchBuffers['vLeptons_new_'+var][1] = getattr(tree,'selLeptons_%s'%var)[i]
                            break
            else:
                VtypeCorrector.after_other_Vtypes.append(vType)

                if tree.Vtype == 0 or tree.Vtype == 1:
                    print '@ERROR: This is impossible, the new ele cut should be looser...'
                    print 'selected mu/e:',selectedMuons, selectedElectrons, ' z mu:', zMuons, ' z e:', zElectrons
                    sys.exit(1)
                #Wlv case. Recompute lepton branches
                if tree.Vtype == 2 or tree.Vtype == 3:
                    Vtype_new_ = tree.Vtype
                    for var in self.vLeptonsvar:
                        self.branchBuffers['vLeptons_new_'+var][0] = getattr(tree,'vLeptons_%s'%var)[0]
                #to handle misassigned Vtype 4 or -1 because of additional electron cut
                elif (tree.Vtype == 4 or tree.Vtype == -1) and len(zElectrons) + len(zMuons) > 0:
                    Vtype_new_ = 5
                #to handle misassigned Vtype 5 because of additional electron cut
                elif tree.Vtype == 5 and len(zElectrons) + len(zMuons) == 0:
                    if tree.met_pt < 80:
                        Vtype_new_ = -1
                    else:
                        Vtype_new_ = 4
                #if none of the exception above happen, it is save to copy the Vtype
                else:
                    Vtype_new_ = tree.Vtype

            # skip event, if vtype_new doesn't correspond to channel
            if self.channel.lower() == 'zll': 
                if Vtype_new_ != 0 and Vtype_new_ != 1:
                    self.n_vtype_events_skipped += 1
                    isGoodEvent = False
            elif self.channel.lower() == 'wlv':
                if Vtype_new_ != 2 and Vtype_new_ != 3:
                    self.n_vtype_events_skipped += 1
                    isGoodEvent = False
            elif self.channel.lower() == 'zvv':
                if (Vtype_new_ != 2 and Vtype_new_ != 3 and Vtype_new_ != 4) or tree.V_pt < 170:
                    self.n_vtype_events_skipped += 1
                    isGoodEvent = False

            if isGoodEvent:
                if Vtype_new_ == tree.Vtype:
                    self.n_vtype_unchanged += 1
                else:
                    self.n_vtype_changed += 1

            V = ROOT.TLorentzVector()

            #Recompute combined lepton variables for Zll
            if Vtype_new_ == 0 or Vtype_new_ == 1:
                lep1 = ROOT.TLorentzVector()
                lep2 = ROOT.TLorentzVector()
                lep1.SetPtEtaPhiM(self.branchBuffers['vLeptons_new_pt'][0], self.branchBuffers['vLeptons_new_eta'][0], self.branchBuffers['vLeptons_new_phi'][0], self.branchBuffers['vLeptons_new_mass'][0])
                lep2.SetPtEtaPhiM(self.branchBuffers['vLeptons_new_pt'][1], self.branchBuffers['vLeptons_new_eta'][1], self.branchBuffers['vLeptons_new_phi'][1], self.branchBuffers['vLeptons_new_mass'][1])
                V = lep1+lep2
                for var in self.Vvar:
                    self.branchBuffers['V_new_'+var][0] = getattr(V, self.LorentzDic[var])()
            #Use "old" lepton variables for Wlv and Zvv. i.e. only Vtype -> Vtype_new change, other _new variables are copy
            else:
                for var in self.Vvar:
                    self.branchBuffers['V_new_'+var][0] = getattr(tree,'V_%s'%var)

            self.branchBuffers['Vtype_new'][0] = Vtype_new_

            # mark current entry as processed
            self.lastEntry = currentEntry
        return Vtype_new_ #isGoodEvent

    def getBranch(self, event, arguments=None):
        self.processEvent(event)
        if arguments:
            return self.branchBuffers[arguments][0]

    def getVectorBranch(self, event, arguments=None, destinationArray=None):
        self.processEvent(event)
        # TODO: avoid this additional copy step
        for i in range(arguments['length']):
            destinationArray[i] =  self.branchBuffers[arguments['branch']][i]
    
    def getBranches(self):
        return self.branches

    def printStatistics(self):
        print 'Vtype correction statistics:' 
        print ' #skipped:', self.n_vtype_events_skipped
        print ' #unchanged:', self.n_vtype_unchanged
        print ' #changed:', self.n_vtype_changed
        print 'self.n_mm_reassigned', self.n_mm_reassigned
        print 'self.n_ee_reassigned', self.n_ee_reassigned
        print 'self.n_vtype0_original', self.n_vtype0_original
        print 'self.n_vtype1_original', self.n_vtype1_original


if __name__ == "__main__":
    fDY2 = "root://stormgf1.pi.infn.it:1094//store/user/arizzi/VHBBHeppyV25/DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V25_DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/170206_152714/0000/tree_233.root"
    fS300 = "/eos/cms/store/user/rkamalie/GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-300_narrow_13TeV-madgraph/tree_11.root"

    fS900 = "/eos/cms/store/user/rkamalie/GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-900_narrow_13TeV-madgraph/tree_14.root"
    fTT = "/eos/user/r/rkamalie/CMSSW_8_0_25/src/bbZZ/skimmedSamples/TT_TuneCUETP8M2T4_13TeV-powheg-Py8__RunIISummer16MAv2-PUMoriond17_backup_80r2as_2016_TrancheIV_v6-v1/skimtree_1365_1379.root"
    fDEG = "root://stormgf1.pi.infn.it:1094//store/user/arizzi/VHBBHeppyV25b/DoubleEG/VHBB_HEPPY_V25b_DoubleEG__Run2016B-03Feb2017_ver2-v2/170301_131914/0002/tree_2067.root"
    
    f = fDY2
    f = fS900
    #f = fS300
    #f = fTT
    #f = fDEG
    fIn = ROOT.TFile.Open(f) # very important to have OPEN when work with root prefix for Pisa
    print 'fIn', fIn
    tree_orig = fIn.Get("tree")



    print 'tree_orig', tree_orig
    vtc = VtypeCorrector(tree_orig, channel='zll')
    print 'vtc', vtc
    nEvents = tree_orig.GetEntries()
    print 'starting the loop'
#    for idx, event in enumerate(tree_orig): #.GetEntries():
        #http://www.ppe.gla.ac.uk/~abuzatu/SUPAROO/PyROOT/Helper/HelperPyRoot.py
        #http://pandora.physics.lsa.umich.edu:3000/projects/panda/wiki/Data_analysis_with_pyroot
        #https://wiki.physik.uzh.ch/cms/root:pyroot_ttree
    #http://scikit-hep.org/root_numpy/auto_examples/core/plot_bootstrap.html
    #https://pythonhosted.org/root2matplot/
        #https://root-forum.cern.ch/t/tchain-loadtree-not-giving-a-proper-entry-in-pyroot-5-34/28311/2
    #http://scikit-hep.org/root_numpy/reference/generated/root_numpy.array2hist.html

    for idx in xrange(0,int(nEvents)): # tree_orig.GetEntryList()
     #   idx = i
        tree_orig.GetEntry(idx)
        
        if idx%200 ==0:
            print 'doing idx', idx
        #if idx > 200: break
        #for entry in sample.tree:
        #print 'event.met_pt', event.met_pt
        #print vtc.getBranch(event)
        #vtc.getVectorBranch(event)
        #print vtc.getBranches()
        #print vtc.processEvent(event)

        new_vtype = vtc.processEvent(idx)
        print 'new_vtype', new_vtype
    vtc.printStatistics()
    print 'nEvents', nEvents
    print 'now_mm_old_yy', VtypeCorrector.now_mm_old_yy
    print 'now_ee_old_xx', VtypeCorrector.now_ee_old_xx 
    print 'composition of changes for ee:'
    for idx in [-2, -1, 0, 1, 2, 3, 4, 5, 6]:
        #print 'from old status {} to now ee happened {} times'.format(idx, [x[0] for x in  VtypeCorrector.now_ee_old_xx].count(idx))  
        print 'from old status {} to now ee happened {} times'.format(idx, VtypeCorrector.now_ee_old_xx.count(idx))  


    print 
    for idx in [-2, -1, 0, 1, 2, 3, 4, 5, 6]:
        print 'initial status {} happened {} times'.format(idx, VtypeCorrector.other_Vtypes.count(idx))  

    print 
    for idx in [-2, -1, 0, 1, 2, 3, 4, 5, 6]:
        print 'initial status {} happened {} times'.format(idx, VtypeCorrector.after_other_Vtypes.count(idx))  
