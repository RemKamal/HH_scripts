from sys import argv
argv.append( '-b-' )
import ROOT
ROOT.gROOT.SetBatch(True)
argv.remove( '-b-' )
from ROOT import TLorentzVector
import math
import os, io
import timeit, time
import sys
sys.path.append('./')
#sys.path.append('../python/')
#from samples import *




def main():
	files_txt = argv[1]
	samp = argv[4]
# samples = samples_V24
	numSampDebug = -1 # to skip last empty element ' '
	dirpath = os.getcwd()
	destpath = dirpath #+ '/' + samp

# sample_to_process = samples[argv[1]]

	print "\nProcessing sample", samp
	print 'Starting job date: ', time.ctime() 
	print 'files-argv1 is ', argv[1]
	print '1st sample is ', argv[2]
	print 'last sample is ', argv[3]
	print 'sample name is ', argv[4]

	print 'dirpath is ', dirpath
	print 'destpath is ', destpath

	exp_str = 'X509_USER_PROXY=/afs/cern.ch/user/r/rkamalie/x509up_u27011'
	#print 'option for "call" is ', exp_str 
    
	#import subprocess
	#subprocess.call(['export', exp_str])



	is_empty = True
	nFiles = 0

	count = 0
	processed = 0
	processedP = 0
	processedN = 0
	countLHEWeightScale = 0
	countLHEWeightPdf = 0
	print 'filex_txt is ', files_txt
	with io.open (files_txt, mode="rt", encoding = "utf-8") as f:
		listOfFiles = f.read().split('\n')[:numSampDebug] # for test purpose limit to 50
		print 'len of list of files is', len(listOfFiles)
		print 'testfile to open, say #0, is ', listOfFiles[0]
		chain = ROOT.TChain("tree")
		
		for ff in xrange(int(argv[2]),int(argv[3])+1):
			if ff < len (listOfFiles):
				fname = listOfFiles[ff] 
				nFiles +=1
			else:
				print 'job splitting has no file, other jobs should be fine'
				continue
			print 'inside xrange over samples, before ROOT.TFile.Open'
			fi = ROOT.TFile.Open(fname)
			if fi==None or fi.IsZombie():
				continue
			is_empty = False
			chain.AddFile(fname)  
			count += fi.Get("Count").GetBinContent(1)
			processed += fi.Get("CountWeighted").GetBinContent(1)
			processedP += fi.Get("CountPosWeight").GetBinContent(1)
			processedN += fi.Get("CountNegWeight").GetBinContent(1)
			countLHEWeightScale += fi.Get("CountWeightedLHEWeightScale").GetBinContent(1)
			countLHEWeightPdf   += fi.Get("CountWeightedLHEWeightPdf").GetBinContent(1)

			fi.Close()
			print "Adding file n.", ff, ": total processed events:", processed


	if is_empty:
		print "Return because no files could be opened"
		exit(1)

	h_count_simple = ROOT.TH1F("Count", "Count", 1, 0, 2)
	h_count_simple.Fill(1, count)

	h_count = ROOT.TH1F("CountWeighted", "CountWeighted", 1, 0, 2)
	h_count.Fill(1, processed)
	
	h_countPos = ROOT.TH1F("CountPosWeight", "CountPosWeight", 1, 0, 2)
	h_countPos.Fill(1, processedP)
	
	h_countNeg = ROOT.TH1F("CountNegWeight", "CountNegWeight", 1, 0, 2)
	h_countNeg.Fill(1, processedN)
	
	h_countLHEWeightScale = ROOT.TH1F("CountWeightedLHEWeightScale", "CountWeightedLHEWeightScale", 1, 0, 2)
        h_countLHEWeightScale.Fill(1, countLHEWeightScale)

	h_countLHEWeightPdf = ROOT.TH1F("CountWeightedLHEWeightPdf", "CountWeightedLHEWeightPdf", 1, 0, 2)
        h_countLHEWeightPdf.Fill(1, countLHEWeightPdf)


	if os.getcwd() != destpath:
		os.chdir(destpath)
   
  
	f = ROOT.TFile(destpath + "/skimtree_"+argv[2]+"_" + argv[3]+ ".root", "RECREATE")


#chain.SetBranchStatus("*", True)


	if "EG" in samp or "Muon" in samp:
		pass  #no gen or pu info in data
	else:
		chain.SetBranchStatus("gen*", True)
		chain.SetBranchStatus("GenV*", True)
		chain.SetBranchStatus("GenJ*", True)
		chain.SetBranchStatus("pu*", True) ### check
		chain.SetBranchStatus("nGen*", True)



	chain.SetBranchStatus("HLT*")
	chain.SetBranchStatus("nPVs", True)
	chain.SetBranchStatus("evt", True)
	chain.SetBranchStatus("Jet*", True)
	chain.SetBranchStatus("nJet*", True)
	chain.SetBranchStatus("LHE*", True)
	chain.SetBranchStatus("HC*", True)
	chain.SetBranchStatus("hJ*", True)
	chain.SetBranchStatus("aJ*", True)
	chain.SetBranchStatus("btagW*", True)
	chain.SetBranchStatus("met*", True)
	
	chain.SetBranchStatus("sel*", True)
	chain.SetBranchStatus("V*", True)
	chain.SetBranchStatus("v*", True)
	chain.SetBranchStatus("nselLept*", True)
	chain.SetBranchStatus("nvL*", True)
#chain.SetBranchStatus("Gen*", True)

#cut_string = "(HLT_BIT_HLT_DoubleJetsC100_DoubleBTagCSV0p85_DoublePFJetsC160_v | HLT_BIT_HLT_DoubleJetsC100_DoubleBTagCSV0p9_DoublePFJetsC100MaxDeta1p6_v) & (TMath::Abs(Jet_eta[hJCidx[0]]-Jet_eta[hJCidx[1]])<1.6 & Jet_pt[hJCidx[0]]>200 & Jet_pt[hJCidx[1]]>200 & TMath::Abs(Jet_eta[hJCidx[0]])<2.4 & TMath::Abs(Jet_eta[hJCidx[1]])<2.4)"
#cut_string = "(HLT_BIT_HLT_DoubleJetsC100_DoubleBTagCSV0p85_DoublePFJetsC160_v | HLT_BIT_HLT_DoubleJetsC100_DoubleBTagCSV0p9_DoublePFJetsC100MaxDeta1p6_v) & (TMath::Abs(Jet_eta[hJCidx[0]]-Jet_eta[hJCidx[1]])<2.0 & Jet_pt[hJCidx[0]]>150 & Jet_pt[hJCidx[1]]>150 & TMath::Abs(Jet_eta[hJCidx[0]])<2.4 & TMath::Abs(Jet_eta[hJCidx[1]])<2.4)"
#cut_string = "min(mhtJet30,met_pt)>100 && json && Sum$(vLeptons_pt>30)>=1 && (Vtype==2 || Vtype==3)"
#cut_string = "json && (Vtype>=2) && met_pt>170 && H_pt>170 && min(Jet_btagCSV[hJidx[0]], Jet_btagCSV[hJidx[1]])>0.46"
#cut_string = "V_pt>100 && json && vLeptons_pt[0]>30 && (Vtype==2 || Vtype==3)"

	cut_string = "V_mass>50 && json && (Vtype==0 || Vtype==1) && Jet_pt[hJCidx[0]]>30 && Jet_pt[hJCidx[1]]>30 && TMath::Abs(Jet_eta[hJCidx[0]])<2.4 && TMath::Abs(Jet_eta[hJCidx[1]])<2.4"

	print "Cut string: ", cut_string
	print "Copying tree with ", chain.GetEntries(), " entries..."
	tree = chain.CopyTree(cut_string, "")
	print "Copied ", tree.GetEntries(), " entries satisfying the cut condition"
	print 'Successfully Processed {0} files out of requested {1}'.format(nFiles, (int(argv[3])+1-int(argv[2])) )
	print "Writing to file..."
	f.cd()
	tree.Write("", ROOT.TObject.kOverwrite)
	h_count_simple.Write("", ROOT.TObject.kOverwrite)
	h_count.Write("", ROOT.TObject.kOverwrite)
	h_countPos.Write("", ROOT.TObject.kOverwrite)
	h_countNeg.Write("", ROOT.TObject.kOverwrite)
	h_countLHEWeightScale.Write("", ROOT.TObject.kOverwrite)
        h_countLHEWeightPdf.Write("", ROOT.TObject.kOverwrite)

	f.Close()
	print "Done!"


if __name__ == "__main__":
	# *
	#for execution from the command line, for example, from the TT_Tune directory, one would use these lines:
	#x = timeit.repeat("main()", setup="from __main__ import main",repeat = 1,number = 1)
	#y = (sum(x)/len(x))*1 # here, multiply by 'number' used above
#print (x)
#print (len(x))
	#print("it took {:.6} seconds".format(str(y)) )
	
	# with this command:
	# python ../run_tree_skimmer.py ../../comb_listOf_TT_Tune_trees.txt 10 11 TT_Tune
	# *
	main()
	
