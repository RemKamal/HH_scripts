print 'importing VTC'
from VtypeCorrector import VtypeCorrector
print 'importing ROOT'
import ROOT 
import os
import io

debugMode = True

def bazinga (mes):
    if debugMode:
        print mes

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
    fNewRadionSkim = "/eos/user/i/ikrav/HH_2016data/skimming/GluGluToRadionToHHTo2B2ZTo2L2Nu_M-300_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/skimtree_15_29.root"
    fOldRadionSkim = "/eos/cms/store/group/phys_higgs/cmshzz2l2v/HH_bbZZ/samples_skimmed_april_may2018/GluGluToRadionToHHTo2B2ZTo2L2Nu_M-300_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/skimtree_15_29.root"


    fNewBulkGravitonSkim = "/eos/user/r/rkamalie/CMSSW_8_0_25/src/bbZZ/skimmedSamples/GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-300_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/skimtree_15_29.root"
    fOldBulkGravitonSkim = "/eos/cms/store/group/phys_higgs/cmshzz2l2v/HH_bbZZ/skimmedSamples/signal_new_bbZZ/GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-300_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/skimtree_15_29.root"


    fNewBulkGravitonSkim900 = "/eos/user/r/rkamalie/CMSSW_8_0_25/src/bbZZ/skimmedSamples/GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-900_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/skimtree_15_29.root"
    fOldBulkGravitonSkim900 = "/eos/cms/store/group/phys_higgs/cmshzz2l2v/HH_bbZZ/skimmedSamples/signal_new_bbZZ/GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-900_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/skimtree_15_29.root"

    fS = "/eos/user/r/rkamalie/CMSSW_8_0_25/src/bbZZ/skimmedSamples/GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-300_narrow_13TeV-madgraph/skimtree_0_14.root"
    fDY1 = "/eos/user/r/rkamalie/CMSSW_8_0_25/src/bbZZ/skimmedSamples_v2/DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/skimtree_0_14.root"



    print 'before the loop'
    #for f in [fNewBulkGravitonSkim900, fOldBulkGravitonSkim900]:
    inFileURLorList = "/eos/user/r/rkamalie/CMSSW_8_0_25/src/bbZZ/test/samples20May2018/GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-270_narrow_13TeV-madgraph.txt"
    #"/eos/user/r/rkamalie/CMSSW_8_0_25/src/bbZZ/test/samples20May2018/GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-900_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1.txt"
    splitSignal = "No"
    file_name, file_ext = os.path.splitext(inFileURLorList)
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




#    for f in [fS, fDY1]:
 #       fIn = ROOT.TFile.Open(f) # very important to have OPEN when work with root prefix for Pisa                                                                 print 'fIn', fIn
        #tree_orig = fIn.Get("tree")
        print 'countWeighted', countWeighted
        print 'count', count
        tree_orig = tree
        print 'tree_orig', tree_orig
        vtc = VtypeCorrector(tree_orig, channel='zll')
        #vtc = VtypeCorrector(channel='zll')
        print 'vtc', vtc
        nEvents = tree_orig.GetEntries()
        print 'starting the loop'
    #    for idx, event in enumerate(tree_orig): #.GetEntries():                                                                                                                                                                                                                                                                                                                                                        
        #http://www.ppe.gla.ac.uk/~abuzatu/SUPAROO/PyROOT/Helper/HelperPyRoot.py                                                                                                                                                                                                                                                                                                                                    
        #http://pandora.physics.lsa.umich.edu:3000/projects/panda/wiki/Data_analysis_with_pyroot                                                                                                                                                                                                                                                                                                                    
        #https://wiki.physik.uzh.ch/cms/root:pyroot_ttree                                                                                                                                                                                                                                                                                                                                                           


        #https://root-forum.cern.ch/t/tchain-loadtree-not-giving-a-proper-entry-in-pyroot-5-34/28311/2                                                                                                                                                                                                                                                    
        for idx in xrange(0,int(nEvents)): # tree_orig.GetEntryList()                                                                                                                                                      
            i = idx
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

            #new_vtype = vtc.processEvent(tree_orig)
                new_vtype = vtc.processEvent(i)
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







