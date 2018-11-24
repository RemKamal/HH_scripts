import ROOT
import os
import io
import time
import sys
import array
from rootpy.io import root_open
from rootpy.tree import Tree

debugMode = False                                                                                    
debugFractionOfEvents = 1/5
debugRun = False
recomputeVtype = True
                
printClass_V_Objects = False
                                                                               
def bazinga (mes):
    if debugMode:
        print mes

vLeptonsvar = ['pt', 'eta', 'phi', 'mass', 'relIso03', 'relIso04', 'pfRelIso03', 'pfRelIso04']
Vvar = ['pt', 'eta', 'phi', 'mass']
LorentzDic = {'pt':'Pt', 'eta':'Eta', 'phi':'Phi', 'mass':'M'}

class NewVLeptons:

   def __init__(self, pt, eta, phi, mass, relIso03, relIso04, pfRelIso03, pfRelIso04):
       self.pt = pt
       self.eta = eta
       self.phi = phi
       self.mass = mass
       self.relIso03 = relIso03
       self.relIso04 = relIso04
       self.pfRelIso03 = pfRelIso03
       self.pfRelIso04 = pfRelIso04

   def __str__(self):
       return '\n'.join(sorted( ["\t{}: {}".format(key, val) for key, val in self.__dict__.items()] ))


class NewVBoson:

   def __init__(self, pt, eta, phi, mass):
       self.pt = pt
       self.eta = eta
       self.phi = phi
       self.mass = mass

   def __str__(self):
       return '\n'.join(sorted( ["\t{}: {}".format(key, val) for key, val in self.__dict__.items()] ))





fileName = None
countWeighted = 0
count = 0
masses = [260, 270, 300, 350, 400, 450, 600, 650, 900, 1000]

inFileURLorList = "/afs/cern.ch/work/r/rkamalie/private/July31/v2/CMSSW_8_0_25/src/VHbbAnalysis/Heppy/test/samples20May2018/GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-300_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1.txt"








file_name, file_ext = os.path.splitext(inFileURLorList)
if True:
    if file_ext == '.txt':
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
    
                if True:
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
                #print 'File ',fIn, ' has CountWeighted equal to {0} and count to {1}'.format( fIn.Get('CountWeighted').GetBinContent(1), fIn.Get('Count').GetBinContent(1))
        print '...analysing {0} files in {1} with {2} countWeighted and count {3} events'.format ( len(listOfFiles), inFileURLorList, countWeighted, count )


   

totalEntries = tree.GetEntries() * debugFractionOfEvents if debugRun else tree.GetEntries()
print '\nTotal number of entries is ', totalEntries
bazinga('before loop over entries')
start = time.time()

evWgt=1.0
xsec = 1

per_cent = 0
start = 0
fiveJobs = 0
ninFiveJobs = 0

if recomputeVtype:
        #define functions                                                                                                                         
   zEleSelection = lambda x : tree.selLeptons_pt[x] > 15 and tree.selLeptons_eleMVAIdSppring16GenPurp[x] >= 1
   zMuSelection = lambda x : tree.selLeptons_pt[x] > 15 and  tree.selLeptons_looseIdPOG[x] and tree.selLeptons_relIso04[x] < 0.25
     
   zEleSelection_v = lambda x : tree.vLeptons_pt[x] > 15 and tree.vLeptons_eleMVAIdSppring16GenPurp[x] >= 1
   zMuSelection_v = lambda x : tree.vLeptons_pt[x] > 15 and  tree.vLeptons_looseIdPOG[x] and tree.vLeptons_relIso04[x] < 0.25
     
   zEleSelection_a = lambda x : tree.aLeptons_pt[x] > 15 and tree.aLeptons_eleMVAIdSppring16GenPurp[x] >= 1
   zMuSelection_a = lambda x : tree.aLeptons_pt[x] > 15 and  tree.aLeptons_looseIdPOG[x] and tree.aLeptons_relIso04[x] < 0.25
   


binLabels = ['no cut', 'splitSignal', 'VHbb preselection', 'ele or mu channel', 'trigger', '>=2b-jets', 'Hbb mass',  '2leps', 'Z mass', 'met cut','hhMt cut', 'final bin']
lastEffBin = len(binLabels)+1

lastEffBin = 12

outFileURL = 'bbZZ300' if '300' in inFileURLorList else 'bbZZ900'
fO = root_open(outFileURL + '_minitree.root', "recreate")
minitree = Tree("tree", model=Event)

histos={
    'cutFlow'       :ROOT.TH1F('cutFlow', ';; Events', lastEffBin-1, 1, lastEffBin)
    }

for key in histos:
    histos[key].Sumw2()
    histos[key].SetDirectory(0)




if True:
    for i in xrange(0,int(totalEntries)):
        print 'event %s' % i                                                                                                                                                                                     
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

        if v_id != None:
           print 'v_id', v_id


        histos['cutFlow'].Fill(2,1) # splitSignal

        lepsP4 = []
        Vtype_new_ = None

        if recomputeVtype:
            bazinga('create objects of new classes')
            newVLeptons = NewVLeptons(-1,-1,-1,-1,-1,-1, -1, -1)
            newVBoson   = NewVBoson(-1,-1,-1,-1)



        if True:#(whichChannel == 0 or whichChannel ==1 ):# and recomputeVtype:                                                                                                                               

                    #Variable to store Vtype and leptons info                                                                                                                                                     
           if True:

               if i%1000 ==0:
                   naEles = tree.Draw("aLeptons_pdgId", "abs(aLeptons_pdgId)==11", "goff")
                   nvEles = tree.Draw("vLeptons_pdgId", "abs(vLeptons_pdgId)==11", "goff")
                   nselEles = tree.Draw("selLeptons_pdgId", "abs(selLeptons_pdgId)==11", "goff")
                   print 'naEles={}, nvEles={}, nselEles={}'.format(naEles, nvEles, nselEles)

                   naMuons = tree.Draw("aLeptons_pdgId", "abs(aLeptons_pdgId)==13", "goff")
                   nvMuons = tree.Draw("vLeptons_pdgId", "abs(vLeptons_pdgId)==13", "goff")
                   nselMuons = tree.Draw("selLeptons_pdgId", "abs(selLeptons_pdgId)==13", "goff")
                   print 'naMuons={}, nvMuons={}, nselMuons={}'.format(naMuons, nvMuons, nselMuons)

            #vLeptons_new = []                                                                                                                                                                                    
                    #get all the lepton index                                                                                       
                selLeps = tree.selLeptons_pt
                #print 'selLeps', selLeps
                #print 'type(selLeps)', type(selLeps)
                listSelLeps = list(selLeps)
                #print 'listSelLeps', listSelLeps 
                #https://github.com/alexsparrow/PhysicsUtils/blob/master/python/alex_phys/sweetanal/trees.py
                #http://www.hep.caltech.edu/~piti/doc/rootextension.rootextension-pysrc.html
                #ROOT.PyFloatBuffer

                vLeps = tree.vLeptons_pt
                #print 'vLeps', vLeps
                aLeps = tree.aLeptons_pt
                #print 'aLeps', aLeps

                lep_index = range(len(tree.selLeptons_pt))
                lep_index_a = range(len(tree.aLeptons_pt))
                lep_index_v = range(len(tree.vLeptons_pt))
                #find indexes of those leptons which are "good" leptons                                             
                


                                                                                              
                selectedElectrons = [i for i in  lep_index if abs(tree.selLeptons_pdgId[i]) == 11]
                selectedMuons = [i for i in lep_index if abs(tree.selLeptons_pdgId[i]) == 13]

                vElectrons = [i for i in  lep_index_v if abs(tree.vLeptons_pdgId[i]) == 11]
                vMuons = [i for i in lep_index_v if abs(tree.vLeptons_pdgId[i]) == 13]

                aElectrons = [i for i in  lep_index_a if abs(tree.aLeptons_pdgId[i]) == 11]
                aMuons = [i for i in lep_index_a if abs(tree.aLeptons_pdgId[i]) == 13]


                zElectrons = [x for x in selectedElectrons if zEleSelection(x)]
                zMuons = [x for x in selectedMuons if zMuSelection(x)]

                zElectrons_v = [x for x in vElectrons if zEleSelection_v(x)]
                zMuons_v = [x for x in vMuons if zMuSelection_v(x)]

                zElectrons_a = [x for x in aElectrons if zEleSelection_a(x)]
                zMuons_a = [x for x in aMuons if zMuSelection_a(x)]
                


                #sort indexes by the pt of the selLeptons that can be found under those indexes                                                                                                                   
                zMuons.sort(key=lambda x:tree.selLeptons_pt[x], reverse=True)
                zElectrons.sort(key=lambda x:tree.selLeptons_pt[x], reverse=True)
                print '*'*50
                bazinga('zMuons={}'.format(zMuons))
                bazinga('zElectrons={}'.format(zElectrons))

                zMuons_v.sort(key=lambda x:tree.vLeptons_pt[x], reverse=True)
                zElectrons_v.sort(key=lambda x:tree.vLeptons_pt[x], reverse=True)
                bazinga('zMuons_v={}'.format(zMuons_v))
                bazinga('zElectrons_v={}'.format(zElectrons_v))

                zMuons_a.sort(key=lambda x:tree.aLeptons_pt[x], reverse=True)
                zElectrons_a.sort(key=lambda x:tree.aLeptons_pt[x], reverse=True)
                bazinga('zMuons_a={}'.format(zMuons_a))
                bazinga('zElectrons_a={}'.format(zElectrons_a))

                #if (zMuons_a != [] or zElectrons_a != []) and (zMuons==[] or zElectrons ==[]):
                # if (zMuons_a == [0, 1] and zMuons_v == []) or (zElectrons_a == [0, 1] and zElectrons_v == []):
                #     print 'some aLepton passed'
                #     sys.exit(1)


                # if len(zMuons) >=  2 or len(zElectrons) >=  2:
                #     for i in range(len(tree.selLeptons_mass)):
                #         bazinga('tree.selLeptons_mass[i]={}'.format(tree.selLeptons_mass[i]))

                histos['cutFlow'].Fill(3,1) #zMuons/zEles

                if len(zMuons) >=  2:
                    if tree.selLeptons_pt[zMuons[0]] > 20:
                        for i in zMuons[1:]:
                            if  tree.selLeptons_charge[zMuons[0]]*tree.selLeptons_charge[i] < 0:
                                Vtype_new_ = 0
                                for var in vLeptonsvar:
                                    tmp_var_0 = getattr(tree,'selLeptons_%s'%var)[0]
                                    tmp_var_i = getattr(tree,'selLeptons_%s'%var)[i]
                                    new_arr = array.array('f', [tmp_var_0, tmp_var_i])
                                    if printClass_V_Objects:
                                        print 'inside zMuons'
                                        print 'var=', var
                                        print 'tmp_var_0', tmp_var_0
                                        print 'tmp_var_i', tmp_var_i
                                        print 'new_arr', new_arr
                                    setattr(newVLeptons, var, new_arr)
                                break #fill outer loop once for 0th and 1st leptons                                                                                                                               
                elif len(zElectrons) >=  2 :
                    if tree.selLeptons_pt[zElectrons[0]] > 20:
                        for i in zElectrons[1:]:
                            if  tree.selLeptons_charge[zElectrons[0]]*tree.selLeptons_charge[i] < 0:
                                Vtype_new_ = 1
                                for var in vLeptonsvar:
                                    tmp_var_0 = getattr(tree,'selLeptons_%s'%var)[0]
                                    tmp_var_i = getattr(tree,'selLeptons_%s'%var)[i] #can use 1 here?!                                                                                                            
                                    new_arr = array.array('f', [tmp_var_0, tmp_var_i])
                                    if printClass_V_Objects:
                                        print 'inside zElectrons'
                                        print 'var=', var
                                        print 'tmp_var_0', tmp_var_0
                                        print 'tmp_var_i', tmp_var_i
                                        print 'new_arr', new_arr
                                    setattr(newVLeptons, var, new_arr)
                                break #fill outer loop once for 0th and 1st leptons   

                else:
                    #no leptons found, continue                                                                                                                                                                   
                    continue
                if printClass_V_Objects:
                    print 'newVLeptons', newVLeptons

                histos['cutFlow'].Fill(4,1) #construct newVLeptons

                if Vtype_new_ == 1:
                    if not tree.HLT_BIT_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v: continue
                elif Vtype_new_ == 0:
                    if not (tree.HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v or tree.HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v or tree.HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v or tree.HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v): continue
                else:
                    continue
                histos['cutFlow'].Fill(5,1) #trigger 
                

        #time to store hist
        histos['cutFlow'].Write()
        minitree.write()
