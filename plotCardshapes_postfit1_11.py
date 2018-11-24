import ROOT
import time, os
import sys
import itertools
import multiprocessing
import math
import glob
from copy import deepcopy
from ROOT import TFile

date = 'nov16_2'
#useTotalBkg = False #TotalBkg vs TotalProcs for totalerr

useTotalBkg = True #TotalBkg vs TotalProcs for totalerr
usesumBGnotTotals = True
reScaleSignalTo = 2 #pb, not 1 pb
putOnlyCombinedSignal = True
legendFontSize = 0.023

useLogY = True
minOfYRange = 2
noChi2Shown = True

drawCutArrow = False



BulkGraviton_or_Radion_directory = "BulkGraviton" if "BulkGrav" in os.getcwd() else "Radion"
particleType = "graviton" if "BulkGrav" in os.getcwd() else "radion"

allow_raw_input = False
do_prefit_or_postfit = 'postfit'
mass = int(os.getcwd().split('_')[-1])
rebin_factor = 2
visualization_mult_factor = 500
do_SR_BDTSideband = False#True
plotData_in_SR = True #if not do_SR_BDTSideband else False

includeAbsentSignal = False
tolerate = 0.01 #extra 0 should be added?!
stack_manually = True

badRoots = [
	'zmass',
	'dR_bjets'
	'hmass0',
	'dR_bjets',
	'dR_leps'
	'hmass1',
	]



def createPreFitPlot2(ifile, typ=''):
	ROOT.gROOT.SetBatch(True)
	fileName = deepcopy(ifile)

	if typ == None:
		print 'exiting, no plot type is specified!...'
		sys.exit(1)
	elif typ == 'prefit':
		print 'Doing prefit type of plot'
	elif typ == 'postfit':
		print 'Doing postfit type of plot'
	else:
		print 'exiting, no correct plot type is specified!...'
                sys.exit(1)

	print 'create a plot for', ifile

	tmpList = ifile.split('Postfit.')[0].split('_')
	channel, name, region, fitType = tmpList[0], '_'.join(tmpList[1:-2]), tmpList[-2], tmpList[-1]

	#channel, name, region = tmpList[0], '_'.join(tmpList[1:-1]), tmpList[-1]

	
	#name = ifile.split('.input.')[0] #'_'.join((ifile.GetName()).split('_')[:-1])
	print 'name', name#, 'len=', len(name)
	
	#FIX ME later
	do_plotData_in_SR = plotData_in_SR
	print 'do_plotData_in_SR', do_plotData_in_SR
	#tolerance  = 0              #0.001 if ('hh' in name or 'dR' in name or 'zpt' in name) else tolerate
	#tolerance = 0               #0.01 if ('dR_lep' in name and 'SR' not in ifile) else tolerance
	tolerance = tolerate
	
	ROOT.gStyle.SetOptStat(0)

	size = os.stat(ifile).st_size
	ifile = ROOT.TFile(ifile)

	if ifile.IsZombie() or not ifile.IsOpen() or ifile.TestBit(TFile.kRecovered) or ifile.GetNkeys()==0:# or size <= 10000:
		print 'bad file of the type similar to ee/mm_hhMt_SR/CRDY/CRTT_CRs/FullPostfit.root, skipping...'
		return
	innerDir = channel + '_' + region + '_' + typ 

	print 'Dir=', innerDir   #ee_CRDYlow_prefit


	ST = ifile.Get("%s/ST" % innerDir)
	TT = ifile.Get("%s/TT" % innerDir)
	VV = ifile.Get("%s/VV" % innerDir)
	DY = ifile.Get("%s/DY" % innerDir)
	ZH = ifile.Get("%s/ZH" % innerDir)
	HZZ = ifile.Get("%s/signal_hzz" % innerDir)
	HWW = ifile.Get("%s/signal_hww" % innerDir)

	TotalBkg = ifile.Get("%s/TotalBkg" % innerDir)
	TotalProcs = ifile.Get("%s/TotalProcs" % innerDir)
	#TotalSig = ifile.Get("%s/TotalSig" % innerDir)
	data = ifile.Get("%s/data_obs" % innerDir)

	hzz_is_absent = False
	hww_is_absent = False

	totSignal = None

	if HZZ == None or HZZ.GetSumOfWeights() == 0:
		print 'HZZ', HZZ
		#hzz_is_absent = True
		HZZ = ifile.Get("%s/signal_hzz" % innerDir.replace('post', 'pre'))
		if HZZ == None:
			hzz_is_absent = True
			print 'damn hzz is not here' *100



	if HWW == None or HWW.GetSumOfWeights() == 0:
		print 'HWW', HWW
		#hww_is_absent = True
		HWW = ifile.Get("%s/signal_hww" % innerDir.replace('post', 'pre'))
		if HWW == None:
			hww_is_absent = True 
			print 'damn HWW is not here' *100

			
	
	signalExists = False
	if not hzz_is_absent and not hww_is_absent:
		totSignal = HZZ.Clone()
		HZZ.Print("all")
		totSignal.Add(HWW)
		signalExists = True
	elif hww_is_absent and not hzz_is_absent:
		totSignal = HZZ.Clone()
		signalExists = True
	elif hzz_is_absent and not hww_is_absent:
		totSignal = HWW.Clone()
		signalExists = True
	else:
		if "CR" in region:
			pass
		else:
			# if both are absent
			print 'cannot happen, exiting....'
			sys.exit(1)

	if signalExists:
		totSignal.Print("all")
		totSignal.Scale(reScaleSignalTo)

	for h in ST, TT, VV, DY, ZH, HZZ, HWW, data, TotalProcs, TotalBkg, totSignal:
		if h != None:
			if rebin_factor > 1 and 'bdt' in fileName:
			        h.Rebin(rebin_factor)
                                if 'dR_leps' in fileName: 
                                        print
                                        print 'Rebining h=', h
                                        h.Rebin(rebin_factor)
                                else:
                                        pass

        # sumBG = TT.Clone()
	# for h in ST, DY, VV, ZH:
	# 	if h == None: continue
	# 	print 'h=', h
	# 	sumBG.Add(h)
	sumBG = None
	if "SR" in innerDir or "TT" in innerDir:
		sumBG = TT.Clone()
		for h in ST, DY, VV, ZH:
			if h == None: continue
			print 'h=', h
			sumBG.Add(h)
	elif "DY" in innerDir:
		print 'fileName', fileName
		print 'DY=', DY.Print("all")
		sumBG = DY.Clone()
		for h in ST, ZH, VV, TT:
			if h == None: continue
			print 'h=', h
			sumBG.Add(h)
	else:
		print "please check innerDir, exiting..."
		sys.exit(1)

	if sumBG == None:
		print "please check sumBG, exiting..."
		sys.exit(1)

        # sumBG = ZH.Clone()
	# for h in ST, DY, VV, TT:
	# 	if h == None: continue
	# 	print 'h=', h
	# 	sumBG.Add(h)

	copyTotalProcs = TotalProcs   #sumBG #.Clone()
	for idx, bin in enumerate(copyTotalProcs):
		if copyTotalProcs.GetBinContent(idx) < tolerance:
			copyTotalProcs.SetBinContent(idx, 0)
			copyTotalProcs.SetBinError(idx, 0)

	TotalProcs  = copyTotalProcs#.Clone()



        copyTotalBkg = TotalBkg   #sumBG #.Clone()                                                                                              
        for idx, bin in enumerate(copyTotalBkg):
                if copyTotalBkg.GetBinContent(idx) < tolerance:
                        copyTotalBkg.SetBinContent(idx, 0)
                        copyTotalBkg.SetBinError(idx, 0)

        TotalBkg  = copyTotalBkg#.Clone()  
	print 'TotalProcs modified'
	#TotalProcs.Print('all')
	#print 'data', data.Print('all')
	data_clone = data.Clone()
	nbins = data_clone.GetNbinsX()

	for idx, bin in enumerate(data_clone):
		print 'bin in data', bin
		print 'idx', idx
	print 'done with data entries'
	print 'data', data


	data.SetMarkerStyle(20) 
	data.SetMarkerSize(0.8) 
	data.SetLineStyle(1) #7 was used in the plotter 
	data.SetLineWidth(1)

	if TT != None: TT.SetLineColor(ROOT.kRed - 4)
	if VV != None: VV.SetLineColor(ROOT.kSpring + 5)
	if DY != None: DY.SetLineColor(ROOT.kOrange - 2)
	if ST != None: ST.SetLineColor(ROOT.kBlue - 4)
	if ZH != None: ZH.SetLineColor(ROOT.kMagenta - 9)


	if TT != None: TT.SetFillColor(ROOT.kRed - 4)
	if VV != None:  VV.SetFillColor(ROOT.kSpring + 5)
	if DY != None: DY.SetFillColor(ROOT.kOrange - 2)
	if ST != None: ST.SetFillColor(ROOT.kBlue - 4)
	if ZH != None: ZH.SetFillColor(ROOT.kMagenta - 9)
	
	#HZZ.SetFillColor(ROOT.kYellow + 1)
	#HWW.SetFillColor(ROOT.kYellow - 2)
	mult = visualization_mult_factor
        if not hzz_is_absent and not hww_is_absent:
                #print 'HZZ', HZZ                                                                                                                    
                HZZ.SetLineColor(ROOT.kRed - 3)#Azure + 6 )#Blue - 4)                                                                                
                HWW.SetLineColor(ROOT.kTeal - 7 )#Spring + 5)                                                                                        

		if signalExists: 
			#totSignal.SetLineColor(ROOT.kGreen -3)
			totSignal.SetLineColor(ROOT.kViolet -6)
			totSignal.SetLineStyle(7)
                HWW.SetLineStyle(7)
                HZZ.SetLineStyle(7)
                #https://root-forum.cern.ch/t/different-ways-of-normalizing-histograms/15582/6                                                       
                #if 'SR' in ifile.GetName() and                                                                                                      

                if 'SR' in ifile.GetName():
			if "Bulk" in BulkGraviton_or_Radion_directory:
                                if channel == "ee":
                                        if mass <= 260:
                                                mult = 2500
                                        elif mass == 270:
                                                mult = 2500
                                        elif mass == 300:
                                                mult = 200 #2500
                                        elif mass == 350:
                                                mult = 2500
                                        elif mass == 400:
                                                mult = 2500
                                        elif mass == 450:
                                                mult = 10
                                        elif mass == 451:
                                                mult = 10

                                        elif mass == 500:
                                                mult = 10
                                        elif mass == 550:
                                                mult = 10
                                        elif mass == 600:
                                                mult = 10
                                        elif mass == 650:
                                                mult = 10

                                        elif mass == 700:
                                                mult = 10
                                        elif mass == 750:
						mult = 5
                                        elif mass == 800:
                                                mult = 5
                                        elif mass == 900:
                                                mult = 2
                                        elif mass == 1000:
						mult = 10
                                        else:
                                                mult = 5

                                else: ## mm channel     
					if mass <= 260:
                                                mult = 2500
					elif mass == 270:
                                                mult = 2500
					elif mass == 300:
                                                mult = 200 #2500
					elif mass == 350:
                                                mult = 2500
					elif mass == 400:
                                                mult = 2500
					elif mass == 450:
                                                mult = 25
					elif mass == 451:
                                                mult = 25
					elif mass == 500:
						mult = 35
					elif mass == 550:
                                                mult = 35
					elif mass == 650:
                                                mult = 35
					else:
                                                mult = 5

			elif "Radion" in BulkGraviton_or_Radion_directory:
				if channel == "ee":
					if mass <= 260:
						mult = 1000000
					elif mass == 270:
						mult = 25000
					elif mass == 300:
						mult = 200 #10000
					elif mass == 350:
						mult = 5000
					elif mass == 400:
						mult = 10000
					elif mass == 450:
						mult = 150
					elif mass == 451:
						mult = 10
					elif mass == 500:
						mult = 100
					elif mass == 550:
						mult = 50
					elif mass == 600:
                                                mult = 50
					elif mass == 650:
						mult = 20
					else:
						mult = 4
						
				else: ## mm channel
					if mass <=300:
						mult = 200 #10000
					elif mass == 350:
						mult = 400
					elif mass == 400:
						mult = 2000
					elif 450 <= mass < 500:
						mult = 50
					else:   
						mult = 20
			else:
				print 'BulkGraviton or Radion, any other is not possible, exiting...'
				sys.exit(1)
					
		HZZ.Scale(mult)
		HWW.Scale(mult)
		
	if signalExists:
		if 'DY' in region:
			totSignal.Print("all")
			totSignal.Scale(mult)
			print
			print
			totSignal.Print("all")
			#sys.exit(1)
		else:
			totSignal.Scale(mult)

	# visualization_mult_factor = 500 if 'SR' in region else 10000
	# if not hzz_is_absent and not hww_is_absent:
	# 	#print 'HZZ', HZZ
	# 	HZZ.SetLineColor(ROOT.kRed - 3)#Azure + 6 )#Blue - 4)
	# 	HWW.SetLineColor(ROOT.kTeal - 7 )#Spring + 5)

	# 	HWW.SetLineStyle(7)
	# 	HZZ.SetLineStyle(7)
	# 	#https://root-forum.cern.ch/t/different-ways-of-normalizing-histograms/15582/6
	# 	#if 'SR' in ifile.GetName() and int(os.getcwd().split('/')[-1]) > 450:
	# 	mult = visualization_mult_factor 

	if TT != None: TT.SetFillStyle(1001)
	if VV != None: VV.SetFillStyle(1001)
	if DY != None: DY.SetFillStyle(1001)
	if ST != None: ST.SetFillStyle(1001)
	if ZH != None: ZH.SetFillStyle(1001)

	if TT != None: TT.SetLineStyle(1)
	if VV != None: VV.SetLineStyle(1)
	if DY != None: DY.SetLineStyle(1)
	if ST != None: ST.SetLineStyle(1)
	if ZH != None: ZH.SetLineStyle(1)

	if not hzz_is_absent and not hww_is_absent:#includeAbsentSignal:
		HZZ.SetFillStyle(1001)
		HWW.SetFillStyle(1001)
		if signalExists:
			totSignal.SetFillStyle(1001)
		

	#VV.Scale(100)
	#ST.Scale(100)
	#ZH.Scale(100)
 
	stack = ROOT.THStack("stack", "stack")
	# for h in VV, ST, ZH, DY, TT:#bg_hists:
	# 	stack.Add(h)
	
	if stack_manually:
		#for h in VV, ST, ZH, DY, TT:#bg_hists:
		for h in DY, TT, ZH, ST, VV:#bg_hists:
			if h != None:
				stack.Add(h)
	else:
		print 'adding manually'
		if 'DY' in fileName:
			if DY != None:
				stack.Add(DY)
			if TT != None:
				stack.Add(TT)
			if VV != None:
				stack.Add(VV)
			if ST != None:
				stack.Add(ST)
			if ZH != None: 
				stack.Add(ZH)
		else: # CRTT and SR
                        if TT != None:
                                stack.Add(TT)
                        if VV != None:
                                stack.Add(VV)
                        if ST != None:
				stack.Add(ST)
                        if ZH != None: 
				stack.Add(ZH)
			if DY != None:
				stack.Add(DY)
			#if TT != None:
			#	stack.Add(TT)
		

	if useTotalBkg:
		totalerr = TotalBkg.Clone("totalerr")
	else:
		totalerr = TotalProcs.Clone("totalerr")
	if usesumBGnotTotals:
		totalerr = sumBG.Clone("totalerr")
	#https://root-forum.cern.ch/t/set-error-bars-in-thstack-histogram/18523/6
	#https://root.cern.ch/doc/master/classTHStack.html
	#https://root.cern.ch/root/htmldoc/guides/users-guide/Histograms.html

	print '\n'*50
	print 'totalerr.GetMaximum()', totalerr.GetMaximum()
	print 'stack.GetMaximum()', stack.GetMaximum()
	
        #totalerr.Sumw2()
        totalerr.SetFillColor(ROOT.kGray + 3)
        totalerr.SetMarkerSize(0)
        #totalerr.SetLineColor(ROOT.kGray)
	totalerr.SetLineColor(ROOT.kGray + 3)
	totalerr.SetLineWidth(1)

        totalerr.SetFillStyle(3013) #13
	totalerr.SetLineStyle(3)

	canv = ROOT.TCanvas("canv", "canv", 600, 600)
	canv.cd()
	if do_plotData_in_SR:
		canv.SetBottomMargin(0.2) #0.3 to separate two pads
	xmin = int(math.floor(TotalProcs.GetBinCenter(1)))
	xmax = int(math.ceil(TotalProcs.GetBinCenter( TotalProcs.GetNbinsX() )))
	if 'hh' in name:
		xmin, xmax = 150, 1150
		if mass > 450:
			xmin, xmax = 400, 1400			


	print 'xmin', xmin
	print 'xmax', xmax
	#if 'bdt' in ifile:
	#	xmin, xmax = -1.01, 1.01
	
	
	frame = ROOT.TH1F("frame", "", 1, xmin, xmax)
	
	if useLogY:
		canv.SetLogy()

	frame.SetStats(0)
	frame.GetXaxis().SetLabelSize(0)
	#if do_plotData_in_SR:
	frame.GetXaxis().SetTitleOffset(1.15)

	frame.GetYaxis().SetTitleOffset(1.35)
	frame.GetYaxis().SetTitle("Events")
	# frame.GetXaxis().SetTitle("atanhBDT")
	frame.GetYaxis().SetLabelSize(0.04)
	#frame.GetYaxis().SetMoreLogLabels(1)
	
	#ROOT.gStyle.SetNdivisions(999, "y");
	#https://root.cern.ch/doc/master/classTStyle.html#aa8f3cf9d3e427f9c7d5a24df7296cd10
	#frame.GetYaxis().SetRangeUser(TotalProcs.GetMinimum() if TotalProcs.GetMinimum() > 0 else 10, TotalProcs.GetMaximum() * 3.5)
	#frame.GetYaxis().SetRangeUser(10, TotalProcs.GetMaximum() * 3.5)
	#if 'bdt' in name:
	minFactor = minOfYRange if mass <=450 else 0.2
	maxFactor = 6.5 if mass <=450 else 3.5

	frame.GetYaxis().SetRangeUser(minFactor, TotalProcs.GetMaximum() * maxFactor)  

	#else:
	#	frame.GetYaxis().SetRangeUser(, TotalProcs.GetMaximum() * 6.5)#TotalProcs.GetMaximum() * 3.5)
	# if 'bdt' in ifile.GetName() and 'TT' in ifile.GetName():
	# 	frame.GetYaxis().SetRangeUser(10, TotalProcs.GetMaximum() * 1.5)
	# 	#frame.GetYaxis().SetRangeUser(10E-9, TotalProcs.GetMaximum() * 1.5)
	# else:
	# 	frame.GetYaxis().SetRangeUser(10, TotalProcs.GetMaximum() * 1.5)
	# #	print 'doing bdt'*50
	# #frame.GetYaxis().SetRangeUser(1, 150)
	
	


	# frame.GetYaxis().SetRangeUser(10E-03,200)
        if not do_plotData_in_SR:
		frame.GetXaxis().SetLabelSize(0.04)
		frame.GetXaxis().SetTitle(data.GetXaxis().GetTitle())
		

	frame.Draw()
	frame.GetXaxis().SetTitleOffset(1.4)
		
	#canv.Modified() # not sure if needed though
	#canv.Update()

	# for idx, h in enumerate(bg_hists):
	# 	if idx ==0:
	# 		h.Draw('')
	# 	else:
	# 		h.Draw('same')
	stack.Draw("same hist")

	if "SR" in region and "bdt" in fileName and "after" not in fileName:
		ymin, ymax = minOfYRange, TotalProcs.GetMaximum() * maxFactor * 2/16
		bdtCut = None

		if channel == 'mm':
			if mass < 300:
				bdtCut = 0.1
			elif 300 <= mass < 500:
				bdtCut = 0.7
			elif 500 <= mass:
				bdtCut = 0.99
			else:
				print 'cannot happen, exiting'
				sys.exit(1)
		elif channel == 'ee':
			if mass <= 350:
				bdtCut = 0.4
			elif 400 <= mass < 500:
				bdtCut = 0.925
			elif 500 <= mass:
				bdtCut = 0.99
			else:
				print 'cannot happen, exiting'
				sys.exit(1)
		else:
			print 'cannot happen, exiting'
			sys.exit(1)

		if bdtCut == None:
			print 'cannot happen, exiting'
			sys.exit(1)

		latex = ROOT.TLatex()
		latex.SetTextSize(0.025)
		latex.SetTextAlign(13)  ##align at top

		xlabelcut = bdtCut + 0.2
		if drawCutArrow:
			latex.DrawLatex(xlabelcut, ymax-5,"#color[36]{keep}")
		#latex.DrawLatex(xcut - 0.23, ymax,"#color[36]{BDT cut}")


		ar2 = ROOT.TArrow(bdtCut, ymax , bdtCut + 0.3, ymax , 0.03, "|>")
		#                       -1    -1                   -1  
		ar2.SetAngle(40)
		ar2.SetLineColor(36)
		#ar2.SetFillStyle(3008)
		ar2.SetFillColor(36)
		ar2.SetLineWidth(2)
		if drawCutArrow:
			ar2.Draw()

		bdtCutLine = ROOT.TLine(bdtCut, ymin, bdtCut, ymax)
		bdtCutLine.SetLineColor(36)
		bdtCutLine.SetLineWidth(2)
		if drawCutArrow:
			bdtCutLine.Draw()

	ROOT.gPad.RedrawAxis()
		
	if not hzz_is_absent and not putOnlyCombinedSignal:
		HZZ.Draw("same hist")
	if not hww_is_absent and not putOnlyCombinedSignal:
		HWW.Draw("same hist")

	if signalExists:
		totSignal.Draw("same hist")

	if do_plotData_in_SR:
		data.Draw("Psame")

	if usesumBGnotTotals:
        #sumBG.Sumw2()
		sumBG.SetFillColor(ROOT.kGray + 3)
		sumBG.SetMarkerSize(0)
        #sumBG.SetLineColor(ROOT.kGray)
		sumBG.SetLineColor(ROOT.kGray + 3)
		sumBG.SetLineWidth(1)

		sumBG.SetFillStyle(3013) #13
		sumBG.SetLineStyle(3)
		sumBG.Draw("e2 same")
	else: 
		totalerr.Draw("e2 same")
	
	print 'data.Chi2Test TotalProcs:'
	print "Chi2/NDF = ", data.Chi2Test( TotalProcs , "UWCHI2/NDF")
	chi2 = data.Chi2Test( TotalProcs , "UWCHI2/NDF")
	print 'normal chi2', chi2
	#if usesumBGnotTotals:
	#	chi2 = data.Chi2Test( sumBG , "UWCHI2/NDF")
	#	print 'sumBG chi2', chi2
	#print 'data.Chi2Test TotalBkg:'
	#print "Chi2/NDF = ", data.Chi2Test( TotalBkg , "UWCHI2/NDF")
	#chi2 = data.Chi2Test( TotalBkg , "UWCHI2/NDF")

	stack.SetTitle(innerDir)

	leg = ROOT.TLegend(0.5, 0.65, 0.9, 0.87)
	leg.SetNColumns(2)

	leg.SetFillStyle(-1)
	leg.SetBorderSize(0)
	leg.SetTextSize(legendFontSize)


	if signalExists:
		#graviton M=300 GeV [x5000]	
		firstNamePart = "{0}(2 pb)".format(particleType)
		secondNamePart = "M={0} GeV [x{1}]".format(mass, mult)
		leg.AddEntry(totSignal, "#splitline{%s}{%s}" % (firstNamePart, secondNamePart), "L")   
		#leg.AddEntry(totSignal, "#splitline{{0}(2 pb)}{M={1} GeV [x{2}]}".format(particleType, mass, mult), "L")   
		#signal(2pb, {0} GeV) x {1}".format(mass, mult), "L")

	
	#for h in VV, ST, ZH, DY, TT:#bg_hists:
	if VV != None: leg.AddEntry(VV, "Dibosons", "F")
	if ST != None: leg.AddEntry(ST, "Single top", "F")
	if TT != None: leg.AddEntry(TT, "t#bar{t}", "F")
	
	if ZH != None: leg.AddEntry(ZH, "ZH", "F")
	if DY != None: leg.AddEntry(DY, "Drell-Yan", "F")

	


	leg.AddEntry(totalerr, "Total uncertainty", "F")
	#leg.AddEntry(TotalBkg, "TotalBkg", "F")
	#leg.AddEntry(TotalProcs, "TotalProcs", "F")
	leg.SetEntrySeparation(0.5)

	if not hww_is_absent and not putOnlyCombinedSignal:
		leg.AddEntry(HWW, "bbWW x {0}".format(mult), "L")

        if not hzz_is_absent and not putOnlyCombinedSignal:
                leg.AddEntry(HZZ, "bbZZ x {0}".format(mult), "L")


	if do_plotData_in_SR:
		leg.AddEntry(data, "Data", "EPL")

	
	leg.Draw("same")
	if do_plotData_in_SR:
		#https://root-forum.cern.ch/t/axis-labels-overlapped-by-pad/6920/13
		pad2 = ROOT.TPad("pad2", "pad2", 0., 0., 1., 1.)
		pad2.SetTopMargin(0.73)
	#	pad2.SetBottomMargin(0.)
	#	pad2.SetRightMargin(0.)
		pad2.SetFillColor(0)
		pad2.SetFillStyle(0)
		pad2.Draw()
		pad2.cd()

		frame2 = ROOT.TH1F("frame2", "", 1, xmin, xmax)
		frame2.SetMinimum(-0.5)
	#frame2.SetMinimum(0.5)
		frame2.SetMaximum(0.5)
	#frame2.SetMaximum(1.5)
		frame2.GetXaxis().SetTitleOffset(1.3)

		frame2.GetYaxis().SetLabelSize(0.02)
		frame2.GetYaxis().SetTitleSize(0.04)
		frame2.GetXaxis().SetLabelSize(0.04)
		#frame2.GetXaxis().SetTitle(data.GetXaxis().GetTitle())
		if 'hh' in fileName:
			frame2.GetXaxis().SetTitle("#tilde{M}_{T}(HH) [GeV]")
		elif 'bdt' in fileName:
			frame2.GetXaxis().SetTitle("BDT response")
		else:
			pass

		frame2.GetYaxis().SetRangeUser(-0.9, 0.9)

		frame2.SetStats(0)
		frame2.GetYaxis().SetTitle("Data/MC - 1")
	#frame2.GetYaxis().SetTitle("Data/MC")
		frame2.Draw()
	data2 = data.Clone("data2")

	
	mc_total = TotalProcs.Clone('mt_total') if not usesumBGnotTotals else sumBG.Clone('mt_total')#stack.GetStack().Last().Clone("mc_total")
	data2.Add(mc_total, -1)
	data2.Divide(mc_total)
	mc_total_uncUp = TotalProcs.Clone("mc_total_Up") if not usesumBGnotTotals else sumBG.Clone('mt_total')#stack.GetStack().Last().Clone("mc_total")
	mc_total_uncDown = TotalProcs.Clone("mc_total_Down") if not usesumBGnotTotals else sumBG.Clone('mt_total') #stack.GetStack().Last().Clone("mc_total")
	
	
	
	for i in range(0, mc_total_uncUp.GetNbinsX()):
		#error on (data-mc)/mc is equal to error on data/mc, as (data-mc)/mc = data/mc -1 and the constant - 1 has zero error if we propagate it to the error on the different of data/mc and 1
		#error on r = data/mc => delta_r = r * sqrt((delta_data/data)^2 + (delta_mc/mc)^2)
		e = 0.
		#if mc_total.GetBinContent(i + 1) != 0 and mc_total.GetBinContent(i + 1) < tolerance: continue
		#if data.GetBinContent(i + 1) != 0 and data.GetBinContent(i + 1) < tolerance: continue
		if mc_total.GetBinContent(i + 1) > tolerance and data.GetBinContent(i + 1) > tolerance:
			#if mc_total.GetBinContent(i + 1) < 0.000001 or data.GetBinContent(i + 1) < 0.000001:
			#	continue
			r = data.GetBinContent(i + 1)/mc_total.GetBinContent(i + 1)
			delta_data_over_data = data.GetBinError(i + 1) / data.GetBinContent(i + 1)
			delta_mc_over_mc = mc_total.GetBinError(i + 1) / mc_total.GetBinContent(i + 1)
			delta_r = r * math.sqrt(delta_data_over_data**2 + delta_mc_over_mc**2)
			e = delta_r  
		mc_total_uncUp.SetBinContent(i + 1, e)
		#mc_total_uncUp.SetBinError(i + 1, 0)
		mc_total_uncDown.SetBinContent(i + 1, -e)
                #mc_total_uncDown.SetBinError(i + 1, 0)

	# for i in range(0, mc_total_uncUp.GetNbinsX()):
	# 	e = 0.
	# 	if mc_total.GetBinContent(i + 1) != 0:
	# 		e = mc_total.GetBinError(i + 1) / mc_total.GetBinContent(i + 1)
	# 	mc_total_uncUp.SetBinContent(i + 1, e)
	# 	mc_total_uncDown.SetBinContent(i + 1, -e)


	latex2 = ROOT.TLatex()
	latex2.SetNDC()
	latex2.SetTextSize(0.3*canv.GetTopMargin())
	latex2.SetTextFont(42)
	latex2.SetTextAlign(31) # align right                                                  
	latex2.DrawLatex(0.9, 0.91,"35.9 fb^{-1} (13 TeV)")
		#latex2.SetTextSize(0.9*canv.GetTopMargin())
		#latex2.SetTextFont(52)
		#latex2.SetTextAlign(11) # align right                                                  
		
		#latex2.SetTextSize(0.5*canv.GetTopMargin())
		#latex2.SetTextFont(42)
	latex2.SetTextAlign(11)
	latex2.DrawLatex(0.12, 0.91, "#bf{CMS} #it{preliminary}") #"Work in progress")   
	#chi2string = '#chi^{{2}}#lower[0.1]{{/#it{{dof}} = {0:.2f}}}'.format(data.Chi2Test( TotalProcs , "UWCHI2/NDF"))
	chi2string = "#chi^{2}/" + "NDF = {0}".format(round(chi2, 2)) 
	placeChi2 = False if (round(chi2, 2) == 0 or chi2 > 500) or 'pre' in typ  or noChi2Shown else True
	print 'placeChi2', placeChi2
	if (do_plotData_in_SR or 'SR' not in ifile.GetName()) and placeChi2:
		latex2.DrawLatex(0.12, 0.87, chi2string)#"Chi2/NDF = {0}".format(data.Chi2Test( TotalProcs , "UWCHI2/NDF"))) #"Work in progress")   

	regionFullName = ""
	if "SR" == region:
		regionFullName = "Signal region"
	elif "CRTT" == region:
		regionFullName = "Control region t#bar{t}"
	else:
		regionFullName = "Control region Drell-Yan"

	print 'regionFullName', regionFullName
	print 'channel', channel
	latex2.DrawLatex(0.13, 0.87, regionFullName)
	if 'ee' in channel:
		channelFullName = "e^{+}e^{-} channel"
	else:
		channelFullName = "#mu^{+}#mu^{-} channel"
	latex2.DrawLatex(0.13, 0.83, channelFullName)

	# ratiostaterr = TotalProcs.Clone("ratiostaterr")
        # ratiostaterr.Sumw2()
        # ratiostaterr.SetStats(0)
        # ratiostaterr.SetTitle("")
        # ratiostaterr.GetXaxis().SetTitle(xtitle)
        # ratiostaterr.GetYaxis().SetTitle("Data/MC")
        # ratiostaterr.SetMaximum(2.2)
        # ratiostaterr.SetMinimum(0)
        # ratiostaterr.SetMarkerSize(0)
        # ratiostaterr.SetFillColor(kRed)
        # ratiostaterr.SetFillStyle(3013)
        # #ratiostaterr.SetFillStyle(3001)
        # ratiostaterr.GetXaxis().CenterTitle()
        # ratiostaterr.GetXaxis().SetLabelSize(0.12)
        # ratiostaterr.GetXaxis().SetTitleSize(0.14)
        # ratiostaterr.GetXaxis().SetTitleOffset(1.10)
        # ratiostaterr.GetYaxis().CenterTitle()
        # ratiostaterr.GetYaxis().SetLabelSize(0.10)
        # ratiostaterr.GetYaxis().SetTitleSize(0.12)
        # #ratiostaterr.GetYaxis().SetTitleSize(0.10)
        # ratiostaterr.GetYaxis().SetTitleOffset(0.6)
        # ratiostaterr.GetYaxis().SetNdivisions(505)



	#mc_total_uncUp.Scale(5)
	#mc_total_uncDown.Scale(5)

	mc_total_uncUp.SetLineColor(ROOT.kGray + 3)
	mc_total_uncUp.SetLineWidth(1)
	mc_total_uncUp.SetLineStyle(3)
	mc_total_uncUp.SetFillColor(ROOT.kGray + 3)
	mc_total_uncUp.SetFillStyle(3013)
	mc_total_uncDown.SetLineColor(ROOT.kGray + 3)#SetLineColor(ROOT.kGreen)
	mc_total_uncDown.SetLineWidth(1)
	mc_total_uncDown.SetLineStyle(3)
	mc_total_uncDown.SetFillColor(ROOT.kGray + 3)
	mc_total_uncDown.SetFillStyle(3013)
	if do_plotData_in_SR:
		mc_total_uncUp.Draw("HIST SAME")
		mc_total_uncDown.Draw("HIST SAME")
		line = ROOT.TLine(xmin, 0, xmax, 0)
		line.SetLineStyle(3)
		line.Draw("same")
		data2.Draw("PEsame")
	canv.cd()

	
	#ROOT.gPad.RedrawAxis()
	#ROOT.gROOT.ForceStyle()
	
	canv.Modified()
	canv.Update()

	# print "Data yield: ",data.Integral()
	# print "MC yield: ",stack.GetHistogram().Integral()
	# raw_input()
	# canv.SetLogy(True)
	postfit_type = 'CRsPostfit' if 'CRsPostfit' in fileName else 'FullPostfit'

	for ext in [".png", ".pdf", ".C", ".root"]:
		canv.SaveAs("{0}_{1}_plot_{2}_{3}{4}".format(name, innerDir.replace('postfit', postfit_type), date, particleType, ext))
	
	ifile.Close()
	#datafile.Close()
	do_plotData_in_SR = False



def createPreFitPlot(ifile, typ=''):
	if typ == '':
		print 'exiting, no plot type is specified!...'
		sys.exit(1)
	print 'create for', ifile
	name = ifile.split('.input.')[0] #'_'.join((ifile.GetName()).split('_')[:-1])
	print 'name', name#, 'len=', len(name)
	
	# ROOT.TH1F.SetDefaultSumw2(ROOT.kTRUE) # For correct uncertainty calculation
	global plotData_in_SR
	bdt_plot = True if 'bdt' in ifile else False
	if 'SR' in ifile and plotData_in_SR:
		do_plotData_in_SR = True
	elif 'SR' not in ifile:
		do_plotData_in_SR = True
	else:
		do_plotData_in_SR = False
	print '~'*500
	print 'do_plotData_in_SR', do_plotData_in_SR
	tolerance  = 0              #0.001 if ('hh' in name or 'dR' in name or 'zpt' in name) else tolerate
	tolerance = 0               #0.01 if ('dR_lep' in name and 'SR' not in ifile) else tolerance
	print 'tolerance=', tolerance
	
	ROOT.gStyle.SetOptStat(0)
	#ifile = ROOT.TFile(sys.argv[1])
	ifile = ROOT.TFile(ifile)
	lk=ifile.GetListOfKeys()
	preFitDir = [x.GetName() for x in lk][0]
	if typ == 'postfit':
		preFitDir = preFitDir.replace('pre', 'post')
	else:
		preFitDir = preFitDir.replace('post', 'pre')
	print 'Dir=', preFitDir   #ee_CRDYlow_prefit
	#name = 
	#print 
	#return #sys.exit(1)
	if typ not in preFitDir:
		print 'wrong pre/post fit dir, please check!..'
		sys.exit(1)

	ST = ifile.Get("%s/ST" % preFitDir)
	TT = ifile.Get("%s/TT" % preFitDir)

	print '-'*50
	print 'TT=', TT
	if TT == None:
		return

	print '-'*50
	VV = ifile.Get("%s/VV" % preFitDir)
	DY = ifile.Get("%s/DY" % preFitDir)
	ZH = ifile.Get("%s/ZH" % preFitDir)
	HZZ = ifile.Get("%s/signal_hzz" % preFitDir)
	HWW = ifile.Get("%s/signal_hww" % preFitDir)
	#TotalBkg = ifile.Get("%s/TotalBkg" % preFitDir)
	#TotalProcs = ifile.Get("%s/TotalProcs" % preFitDir)
	#TotalSig = ifile.Get("%s/TotalSig" % preFitDir)
	data = ifile.Get("%s/data_obs" % preFitDir)
	
	# mc_hists = [
	# 	ST,
	# 	TT,
	# 	VV,
	# 	DY,
	# 	ZH,
	# 	]

	# data_n_total_hists = [
	# 	data,
	# 	TotalBkg,
	# 	TotalProcs,

	# 	]
	hzz_is_absent = False
	hww_is_absent = False

	if HZZ == None:
		print 'HZZ', HZZ
		hzz_is_absent = True

	if HWW == None:
		print 'HWW', HWW
		hww_is_absent = True


	# for h in TT, ST, DY, VV, ZH:
	# 	for idx, bin in enumerate(h):
	# 		if h.GetBinContent(idx) < tolerance:
	# 			h.SetBinContent(idx, 0)
	# 			h.SetBinError(idx, 0)
	
		
	# 	print 'hist is', h
	# 	#h.Print('all')
	     
	sumBG = TT.Clone()
	for h in ST, DY, VV, ZH:
		if h == None: continue
		print 'h=', h
		sumBG.Add(h)

	copyTotalProcs = sumBG #.Clone()
	for idx, bin in enumerate(copyTotalProcs):
		if copyTotalProcs.GetBinContent(idx) < tolerance:
			copyTotalProcs.SetBinContent(idx, 0)
			copyTotalProcs.SetBinError(idx, 0)

	TotalProcs  = copyTotalProcs#.Clone()
	print 'TotalProcs modified'
	#TotalProcs.Print('all')
	#print 'data', data.Print('all')
	data_clone = data.Clone()
	nbins = data_clone.GetNbinsX()
	for idx, bin in enumerate(data_clone):
		print 'bin in data', bin
		print 'idx', idx
	print 'done with data entries'
	print 'data', data
	data.SetMarkerStyle(20) 

	TT.SetLineColor(ROOT.kRed - 4)
	if VV != None: VV.SetLineColor(ROOT.kSpring + 5)
	DY.SetLineColor(ROOT.kOrange - 2)
	ST.SetLineColor(ROOT.kBlue - 4)
	ZH.SetLineColor(ROOT.kMagenta - 9)


	TT.SetFillColor(ROOT.kRed - 4)
	if VV != None:  VV.SetFillColor(ROOT.kSpring + 5)
	DY.SetFillColor(ROOT.kOrange - 2)
	ST.SetFillColor(ROOT.kBlue - 4)
	ZH.SetFillColor(ROOT.kMagenta - 9)
	
	#HZZ.SetFillColor(ROOT.kYellow + 1)
	#HWW.SetFillColor(ROOT.kYellow - 2)
	mass = int(os.getcwd().split('_')[-1])
	if not hzz_is_absent and not hww_is_absent:
		#print 'HZZ', HZZ
		HZZ.SetLineColor(ROOT.kRed - 3)#Azure + 6 )#Blue - 4)
		HWW.SetLineColor(ROOT.kTeal - 7 )#Spring + 5)

		HWW.SetLineStyle(7)
		HZZ.SetLineStyle(7)
		#https://root-forum.cern.ch/t/different-ways-of-normalizing-histograms/15582/6
		#if 'SR' in ifile.GetName() and 

		if 'SR' in ifile.GetName() and mass >= 450:
			mult = 1
		else:
			mult = visualization_mult_factor 
		HZZ.Scale(mult)
		HWW.Scale(mult)

	#hzzClone = HZZ
	#hwwClone = HWW#.Clone()
	#HZZ = hzzClone.Clone()
	#HWW = hwwClone.Clone()
	#zj1b.SetFillColor(398)
	#zj2b.SetLineColor(400)
#https://github.com/capalmer85/AnalysisTools/blob/5aa23260f2e1f47c59d692c04e7b0144328a358b/StatTools/Jan21/plotCardshapes_postfit_vv.py

	TT.SetFillStyle(1001)
	if VV != None: VV.SetFillStyle(1001)
	DY.SetFillStyle(1001)
	ST.SetFillStyle(1001)
	ZH.SetFillStyle(1001)
	TT.SetLineStyle(1)
	if VV != None: VV.SetLineStyle(1)
	DY.SetLineStyle(1)
	ST.SetLineStyle(1)
	ZH.SetLineStyle(1)

	if not hzz_is_absent and not hww_is_absent:#includeAbsentSignal:
		HZZ.SetFillStyle(1001)
		HWW.SetFillStyle(1001)

		

	#VV.Scale(100)
	#ST.Scale(100)
	#ZH.Scale(100)
 
	stack = ROOT.THStack("stack", "stack")
	# for h in VV, ST, ZH, DY, TT:#bg_hists:
	# 	stack.Add(h)
	
	if stack_manually:
		for h in VV, ST, ZH, DY, TT:#bg_hists:
			if h != None:
				stack.Add(h)
	else:
		print 'adding manually'
		if VV != None:
			stack.Add(VV)
		stack.Add(ST)
		stack.Add(ZH)
		if 'DY' in ifile:
			stack.Add(TT)
			stack.Add(DY)
		else:
			stack.Add(DY)
			stack.Add(TT)



	#if not hww_is_absent:
	#	stack.Add(HWW)
	#if not hzz_is_absent:
	#	stack.Add(HZZ)
	

        #if includeAbsentSignal:
	#	stack.Add(HZZ)
	#	stack.Add(HWW)
	#use this?
	#stack = TotalProcs #????????????????


	totalerr = TotalProcs.Clone("totalerr")
	#totalerr = TotalBkg.Clone("totalerr")
	print '\n'*50
	print 'totalerr.GetMaximum()', totalerr.GetMaximum()
	print 'stack.GetMaximum()', stack.GetMaximum()
	
        #totalerr.Sumw2()
        totalerr.SetFillColor(ROOT.kGray + 3)
        totalerr.SetMarkerSize(0)
        totalerr.SetLineColor(ROOT.kGray)
        totalerr.SetFillStyle(3013)
	totalerr.SetLineStyle(4)

	canv = ROOT.TCanvas("canv", "canv", 600, 600)
	canv.cd()
	if do_plotData_in_SR:
		canv.SetBottomMargin(0.2) #0.3 to separate two pads
	xmin = int(math.floor(TotalProcs.GetBinCenter(1)))
	xmax = int(math.ceil(TotalProcs.GetBinCenter( TotalProcs.GetNbinsX() )))
	print 'xmin', xmin
	print 'xmax', xmax
	#if 'bdt' in ifile:
	#	xmin, xmax = -1.01, 1.01
	if 'hh' in name:
		xmin, xmax, = 400, 1400
	frame = ROOT.TH1F("frame", "", 1, xmin, xmax)
	canv.SetLogy()

	frame.SetStats(0)
	frame.GetXaxis().SetLabelSize(0)
	#if do_plotData_in_SR:
	frame.GetXaxis().SetTitleOffset(1.3)
	#else:
	frame.GetXaxis().SetTitleOffset(1.15)
	frame.GetYaxis().SetTitleOffset(1.3)
	frame.GetYaxis().SetTitle("Events")
	# frame.GetXaxis().SetTitle("atanhBDT")
	frame.GetYaxis().SetLabelSize(0.04)
	#frame.GetYaxis().SetMoreLogLabels(1)
	
	#ROOT.gStyle.SetNdivisions(999, "y");
	#https://root.cern.ch/doc/master/classTStyle.html#aa8f3cf9d3e427f9c7d5a24df7296cd10
	#frame.GetYaxis().SetRangeUser(TotalProcs.GetMinimum() if TotalProcs.GetMinimum() > 0 else 10, TotalProcs.GetMaximum() * 3.5)
	#frame.GetYaxis().SetRangeUser(10, TotalProcs.GetMaximum() * 3.5)
	if bdt_plot:
		frame.GetYaxis().SetRangeUser(1, TotalProcs.GetMaximum() * 6.5)  
	else:
		frame.GetYaxis().SetRangeUser(0.1, TotalProcs.GetMaximum() * 6.5)#TotalProcs.GetMaximum() * 3.5)
	# if 'bdt' in ifile.GetName() and 'TT' in ifile.GetName():
	# 	frame.GetYaxis().SetRangeUser(10, TotalProcs.GetMaximum() * 1.5)
	# 	#frame.GetYaxis().SetRangeUser(10E-9, TotalProcs.GetMaximum() * 1.5)
	# else:
	# 	frame.GetYaxis().SetRangeUser(10, TotalProcs.GetMaximum() * 1.5)
	# #	print 'doing bdt'*50
	# #frame.GetYaxis().SetRangeUser(1, 150)
	
	


	# frame.GetYaxis().SetRangeUser(10E-03,200)
        if not do_plotData_in_SR:
		frame.GetXaxis().SetLabelSize(0.04)
		frame.GetXaxis().SetTitle(data.GetXaxis().GetTitle())


	frame.Draw()
	#canv.Modified() # not sure if needed though
	#canv.Update()

	# for idx, h in enumerate(bg_hists):
	# 	if idx ==0:
	# 		h.Draw('')
	# 	else:
	# 		h.Draw('same')
	stack.Draw("same hist")
	if not hzz_is_absent and not putOnlyCombinedSignal:
		HZZ.Draw("same hist")
	if not hww_is_absent and not putOnlyCombinedSignal:
		HWW.Draw("same hist")


	#stack.Draw()
	#TT.Draw('same')
	#TotalBkg.SetLineColor(ROOT.kOrange)
	#TotalBkg.Draw('same')
	
	TotalProcs.SetLineColor(ROOT.kRed)
	#TotalProcs.Draw('same')

	print 'of', stack
	#stack.Print('all')
	#pad.Modified()
	#pad.Update()
	#canv.Modified() # not sure if needed though
	#canv.Update()
	if do_plotData_in_SR:
		data.Draw("Psame")
	#canv.Modified() # not sure if needed though
	#canv.Update()

	totalerr.Draw("e2 same")
	#canv.Modified() # not sure if needed though
	#canv.Update()
	print 'data.Chi2Test TotalProcs:'
	print "Chi2/NDF = ", data.Chi2Test( TotalProcs , "UWCHI2/NDF")
	#print 'data.Chi2Test TotalBkg:'
        #print "Chi2/NDF = ", data.Chi2Test( TotalBkg , "UWCHI2/NDF")
	#print 'TotalProcs.Chi2Test TotalBkg:'
	#print "Chi2/NDF = ", TotalProcs.Chi2Test(TotalBkg , "WWCHI2/NDF")

	print 'ifile', ifile
	chi2 = data.Chi2Test( TotalProcs , "UWCHI2/NDF")
	# print "Total bkg: ",stack.GetHistogram().GetIntegral()
	# stack.Draw("ep same")
	stack.SetTitle(preFitDir)
	# stack.GetXaxis().SetTitle("Mjj [GeV]")
	
	
# print "Total data: ",data.Integral()
	# bkg.Draw("hist")
	# bkg.Draw("ep same")
	# stackvv.Draw("hist same")
	# stackvv.Draw("ep same")
	# TT.Draw("HISTsame")
	leg = ROOT.TLegend(0.7, 0.7, 0.9, 0.89)
	leg.SetFillStyle(-1)
	leg.SetBorderSize(0)
	leg.AddEntry(VV, "VV", "F")
	leg.AddEntry(ST, "ST", "F")
	leg.AddEntry(DY, "DY", "F")
	leg.AddEntry(ZH, "ZH", "F")
	leg.AddEntry(TT, "TT", "F")
	leg.AddEntry(totalerr, "Total uncertainty", "F")
	#leg.AddEntry(TotalBkg, "TotalBkg", "F")
	#leg.AddEntry(TotalProcs, "TotalProcs", "F")


	if not hww_is_absent and not hzz_is_absent:
		leg.AddEntry(HZZ, "bbZZ x {0}".format(mult), "L")
		leg.AddEntry(HWW, "bbWW x {0}".format(mult), "L")
	if do_plotData_in_SR:
		leg.AddEntry(data, "Data", "EPL")
	leg.Draw("same")
	if do_plotData_in_SR:
		#https://root-forum.cern.ch/t/axis-labels-overlapped-by-pad/6920/13
		pad2 = ROOT.TPad("pad2", "pad2", 0., 0., 1., 1.)
		pad2.SetTopMargin(0.73)
	#	pad2.SetBottomMargin(0.)
	#	pad2.SetRightMargin(0.)
		pad2.SetFillColor(0)
		pad2.SetFillStyle(0)
		pad2.Draw()
		pad2.cd()

		frame2 = ROOT.TH1F("frame2", "", 1, xmin, xmax)
		frame2.SetMinimum(-0.5)
	#frame2.SetMinimum(0.5)
		frame2.SetMaximum(0.5)
	#frame2.SetMaximum(1.5)
		frame2.GetYaxis().SetLabelSize(0.02)
		frame2.GetYaxis().SetTitleSize(0.04)
		frame2.GetXaxis().SetLabelSize(0.04)
		frame2.GetXaxis().SetTitle(data.GetXaxis().GetTitle())
	

		frame2.SetStats(0)
		frame2.GetYaxis().SetTitle("Data/MC - 1")
	#frame2.GetYaxis().SetTitle("Data/MC")
		frame2.Draw()
	data2 = data.Clone("data2")

	
	mc_total = TotalProcs.Clone('mt_total') #stack.GetStack().Last().Clone("mc_total")
	data2.Add(mc_total, -1)
	data2.Divide(mc_total)
	mc_total_uncUp = TotalProcs.Clone("mc_total_Up") #stack.GetStack().Last().Clone("mc_total")
	mc_total_uncDown = TotalProcs.Clone("mc_total_Down") #stack.GetStack().Last().Clone("mc_total")
	
	
	
	for i in range(0, mc_total_uncUp.GetNbinsX()):
		#error on (data-mc)/mc is equal to error on data/mc, as (data-mc)/mc = data/mc -1 and the constant - 1 has zero error if we propagate it to the error on the different of data/mc and 1
		#error on r = data/mc => delta_r = r * sqrt((delta_data/data)^2 + (delta_mc/mc)^2)
		e = 0.
		#if mc_total.GetBinContent(i + 1) != 0 and mc_total.GetBinContent(i + 1) < tolerance: continue
		#if data.GetBinContent(i + 1) != 0 and data.GetBinContent(i + 1) < tolerance: continue
		if mc_total.GetBinContent(i + 1) > tolerance and data.GetBinContent(i + 1) > tolerance:
			#if mc_total.GetBinContent(i + 1) < 0.000001 or data.GetBinContent(i + 1) < 0.000001:
			#	continue
			r = data.GetBinContent(i + 1)/mc_total.GetBinContent(i + 1)
			delta_data_over_data = data.GetBinError(i + 1) / data.GetBinContent(i + 1)
			delta_mc_over_mc = mc_total.GetBinError(i + 1) / mc_total.GetBinContent(i + 1)
			delta_r = r * math.sqrt(delta_data_over_data**2 + delta_mc_over_mc**2)
			e = delta_r  
		mc_total_uncUp.SetBinContent(i + 1, e)
		#mc_total_uncUp.SetBinError(i + 1, 0)
		mc_total_uncDown.SetBinContent(i + 1, -e)
                #mc_total_uncDown.SetBinError(i + 1, 0)

	# for i in range(0, mc_total_uncUp.GetNbinsX()):
	# 	e = 0.
	# 	if mc_total.GetBinContent(i + 1) != 0:
	# 		e = mc_total.GetBinError(i + 1) / mc_total.GetBinContent(i + 1)
	# 	mc_total_uncUp.SetBinContent(i + 1, e)
	# 	mc_total_uncDown.SetBinContent(i + 1, -e)


	latex2 = ROOT.TLatex()
	latex2.SetNDC()
	latex2.SetTextSize(0.3*canv.GetTopMargin())
	latex2.SetTextFont(42)
	latex2.SetTextAlign(31) # align right                                                  
	latex2.DrawLatex(0.9, 0.91,"35.9 fb^{-1} (13 TeV)")
		#latex2.SetTextSize(0.9*canv.GetTopMargin())
		#latex2.SetTextFont(52)
		#latex2.SetTextAlign(11) # align right                                                  
		
		#latex2.SetTextSize(0.5*canv.GetTopMargin())
		#latex2.SetTextFont(42)
	latex2.SetTextAlign(11)
	latex2.DrawLatex(0.12, 0.91, "CMS preliminary") #"Work in progress")   
	#chi2string = '#chi^{{2}}#lower[0.1]{{/#it{{dof}} = {0:.2f}}}'.format(data.Chi2Test( TotalProcs , "UWCHI2/NDF"))
	chi2string = "#chi^{2}/" + "NDF = {0}".format(round(chi2, 2)) 
	placeChi2 = False if (round(chi2, 2) == 0 or chi2 > 500)  else True
	print 'placeChi2', placeChi2
	if (do_plotData_in_SR or 'SR' not in ifile.GetName()) and placeChi2:
		latex2.DrawLatex(0.12, 0.87, chi2string)#"Chi2/NDF = {0}".format(data.Chi2Test( TotalProcs , "UWCHI2/NDF"))) #"Work in progress")   


	# ratiostaterr = TotalProcs.Clone("ratiostaterr")
        # ratiostaterr.Sumw2()
        # ratiostaterr.SetStats(0)
        # ratiostaterr.SetTitle("")
        # ratiostaterr.GetXaxis().SetTitle(xtitle)
        # ratiostaterr.GetYaxis().SetTitle("Data/MC")
        # ratiostaterr.SetMaximum(2.2)
        # ratiostaterr.SetMinimum(0)
        # ratiostaterr.SetMarkerSize(0)
        # ratiostaterr.SetFillColor(kRed)
        # ratiostaterr.SetFillStyle(3013)
        # #ratiostaterr.SetFillStyle(3001)
        # ratiostaterr.GetXaxis().CenterTitle()
        # ratiostaterr.GetXaxis().SetLabelSize(0.12)
        # ratiostaterr.GetXaxis().SetTitleSize(0.14)
        # ratiostaterr.GetXaxis().SetTitleOffset(1.10)
        # ratiostaterr.GetYaxis().CenterTitle()
        # ratiostaterr.GetYaxis().SetLabelSize(0.10)
        # ratiostaterr.GetYaxis().SetTitleSize(0.12)
        # #ratiostaterr.GetYaxis().SetTitleSize(0.10)
        # ratiostaterr.GetYaxis().SetTitleOffset(0.6)
        # ratiostaterr.GetYaxis().SetNdivisions(505)



	#mc_total_uncUp.Scale(5)
	#mc_total_uncDown.Scale(5)

	mc_total_uncUp.SetLineColor(ROOT.kGray + 3)
	mc_total_uncUp.SetLineWidth(1)
	mc_total_uncUp.SetFillColor(ROOT.kGray + 3)
	mc_total_uncUp.SetFillStyle(3004)
	mc_total_uncDown.SetLineColor(ROOT.kGray + 3)#SetLineColor(ROOT.kGreen)
	mc_total_uncDown.SetLineWidth(1)
	mc_total_uncDown.SetFillColor(ROOT.kGray + 3)
	mc_total_uncDown.SetFillStyle(3004)
	if do_plotData_in_SR:
		mc_total_uncUp.Draw("HIST SAME")
		mc_total_uncDown.Draw("HIST SAME")
		line = ROOT.TLine(xmin, 0, xmax, 0)
		line.SetLineStyle(3)
		line.Draw("same")
		data2.Draw("PEsame")
	canv.cd()
	canv.Modified()
	canv.Update()
	ROOT.gROOT.ForceStyle()
	ROOT.gPad.RedrawAxis()

	# print "Data yield: ",data.Integral()
	# print "MC yield: ",stack.GetHistogram().Integral()
	# raw_input()
	# canv.SetLogy(True)
	postfit_type = 'CRsPostfit' if 'CRsPostfit' in fileName else 'FullPostfit'

	for ext in [".png"]:#, ".pdf", ".C", ".root"]:
		canv.SaveAs("{0}_{1}_plot_{2}{3}".format(name, postfit_type, date, ext))
	
	ifile.Close()
	#datafile.Close()
	do_plotData_in_SR = False



def createPostFitPlot(ifile):
	print 'create for', ifile
	# ROOT.TH1F.SetDefaultSumw2(ROOT.kTRUE) # For correct uncertainty calculation
	global plotData_in_SR
	bdt_plot = True if 'bdt' in ifile else False
	if 'SR' in ifile and plotData_in_SR:
		plotData_in_SR = True
	elif 'SR' not in ifile:
		plotData_in_SR = True
	else:
		plotData_in_SR = False
	print '~'*500
	print 'plotData_in_SR', plotData_in_SR
	ROOT.gStyle.SetOptStat(0)
	#ifile = ROOT.TFile(sys.argv[1])
	ifile = ROOT.TFile(ifile)
	lk=ifile.GetListOfKeys()
	postFitDir = [x.GetName() for x in lk if 'post' in x.GetName()][0]
	#print postFitDir
	name = '_'.join((ifile.GetName()).split('_')[:-1])
	#name = 
	print 'name', name#, 'len=', len(name)
	#print 
	#return #sys.exit(1)

        tolerance  = 0.001 if ('hh' in name or 'dR' in name or 'zpt' in name) else tolerate
        tolerance = 0.01 if ('dR_lep' in name and 'SR' not in ifile) else tolerance
        print 'tolerance=', tolerance


	ST = ifile.Get("%s/ST" % postFitDir)
	TT = ifile.Get("%s/TT" % postFitDir)
	VV = ifile.Get("%s/VV" % postFitDir)
	DY = ifile.Get("%s/DY" % postFitDir)
	ZH = ifile.Get("%s/ZH" % postFitDir)
	HZZ = ifile.Get("%s/signal_hzz" % postFitDir)
	HWW = ifile.Get("%s/signal_hww" % postFitDir)
	TotalBkg = ifile.Get("%s/TotalBkg" % postFitDir)
	TotalProcs = ifile.Get("%s/TotalProcs" % postFitDir)
	TotalSig = ifile.Get("%s/TotalSig" % postFitDir)
	data = ifile.Get("%s/data_obs" % postFitDir)
	
	# mc_hists = [
	# 	ST,
	# 	TT,
	# 	VV,
	# 	DY,
	# 	ZH,
	# 	]

	# data_n_total_hists = [
	# 	data,
	# 	TotalBkg,
	# 	TotalProcs,

	# 	]
	hzz_is_absent = False
	hww_is_absent = False

	if HZZ == None:
		print 'HZZ', HZZ
		hzz_is_absent = True

	if HWW == None:
		print 'HWW', HWW
		hww_is_absent = True

	#all_hists = mc_hists + [data_n_total_hists]

	#bg_hists = mc_hists #[x.Clone() for x in mc_hists] #deepcopy(mc_hists)

	#if includeAbsentSignal:
	#	hzz_is_absent = False
	#	hww_is_absent = False
	#all_hists.append(TotalSig)
				
	
	#dummy_hzz = ST.Clone('signal_hzz')
	#dummy_hww = ST.Clone('signal_hww')
	# noHZZ, noHWW = False, False
	# if HZZ == None: #.InheritsFrom('TH1'):
	# 	noHZZ = True
	# 	#if includeAbsentSignal:
	# 	#	dummy_hzz.Reset('M')
	# 	#	HZZ = dummy_hzz

	# if HWW == None: #.InheritsFrom('TH1'):
	# 	noHWW = True
	# 	#if includeAbsentSignal:
	# 	#	dummy_hww.Reset('M')
	# 	#	HWW = dummy_hww
	# signal_hists = []
	# if not hzz_is_absent:
	# 	#all_hists.append(HZZ)
	# 	signal_hists.append(HZZ)
	# if not hww_is_absent:
	# 	#all_hists.append(HWW)
	# 	signal_hists.append(HWW)


	for h in TT, ST, DY, VV, ZH:
		for idx, bin in enumerate(h):
			if h.GetBinContent(idx) < tolerance:
				h.SetBinContent(idx, 0)
				h.SetBinError(idx, 0)
	
		
		print 'hist is', h
		h.Print('all')
		
	
	# postFitDir = 'CRTT' if 'CRTT' in ifile else 'CRDY'
	# ST = ifile.Get("shapes_fit_s/%s/ST" % postFitDir)
	# TT = ifile.Get("shapes_fit_s/%s/TT" % postFitDir)
	# VV = ifile.Get("shapes_fit_s/%s/VV" % postFitDir)
	# DY = ifile.Get("shapes_fit_s/%s/DY" % postFitDir)
	# ZH = ifile.Get("shapes_fit_s/%s/ZH" % postFitDir)
	# HZZ = ifile.Get("shapes_fit_s/%s/signal_hzz" % postFitDir)
	# debug = "shapes_fit_s/%s/signal_hzz" % postFitDir
	# print 'debug', debug
	# HWW = ifile.Get("shapes_fit_s/%s/signal_hww" % postFitDir)
	
	# TotalBkg = ifile.Get("shapes_fit_s/%s/TotalBkg" % postFitDir)
	# TotalProcs = ifile.Get("shapes_fit_s/%s/TotalProcs" % postFitDir)
	# TotalSig = ifile.Get("shapes_fit_s/%s/TotalSig" % postFitDir)
	copyTotalProcs = TotalProcs.Clone()
	for idx, bin in enumerate(copyTotalProcs):
		if copyTotalProcs.GetBinContent(idx) < tolerance:
			copyTotalProcs.SetBinContent(idx, 0)
			copyTotalProcs.SetBinError(idx, 0)

	TotalProcs = copyTotalProcs#.Clone()
	print 'TotalProcs modified'
	TotalProcs.Print('all')
	print 'data', data.Print('all')
	data_clone = data.Clone()
	nbins = data_clone.GetNbinsX()
	for idx, bin in enumerate(data_clone):
		print 'bin in data', bin
		print 'idx', idx
	print 'done with data entries'
	# TotalBkg = ifile.Get("shapes_fit_s/%s/total_background" % postFitDir)
	# TotalProcs = ifile.Get("shapes_fit_s/%s/total" % postFitDir)
	# TotalSig = ifile.Get("shapes_fit_s/%s/total_signal" % postFitDir)

	# datafile = 'hmass1_ee_CRDY.input.root'
	# data = ifile.Get("shapes_fit_s/%s/data" % postFitDir)
	
# 	TH1 h; // the histogram (you should set the number of bins, the title etc)
# auto nPoints = graph.GetN(); // number of points in your TGraph
# for(int i=0; i < nPoints; ++i) {
#    double x,y;
#    graph.GetPoint(i, x, y);
#    h->Fill(x,y); // ?

	# data.Print()
	# nbins=DY.GetNbinsX()
	# data_hist = ROOT.TH1F("data_hist","data_hist",nbins,DY.GetBinLowEdge(1),DY.GetBinCenter(nbins)+DY.GetXaxis().GetBinWidth(nbins)/2)
	# for ibin in range(1,data_hist.GetNbinsX()+1):
	# 	x, y = ROOT.Double(0), ROOT.Double(0)
	# 	data.GetPoint(ibin, x, y)
	# 	print 'x=', x, 'y=', y
	# 	print 
	# 	err = data.GetErrorX(ibin)
	# 	data_hist.Fill (x, y)
	# 	data_hist.SetBinError(int(x), int(y), err)

	# data_hist.Print('aa')
	# data = data_hist
	
		

	# data = ROOT.TGraphErrors()
	# for ibin in range(1,data_hist.GetNbinsX()+1):
	#  data.SetPoint(ibin, ibin-0.5, data_hist.GetBinContent(ibin))
	#  data.SetPointError(ibin,0.5, data_hist.GetBinError(ibin))
	#nbins = DY.GetNbinsX()

	#data = ROOT.TH1F("data_hist", "data_hist", nbins, DY.GetBinLowEdge(1),
	#		 DY.GetBinCenter(nbins) + DY.GetXaxis().GetBinWidth(nbins) / 2)
	#for ibin in range(1, data_hist.GetNbinsX() + 1):
	#	data.SetBinContent(ibin, data_hist.GetBinContent(ibin))
	#	data.SetBinError(ibin, data_hist.GetBinError(ibin))
	
	print 'data', data
	data.SetMarkerStyle(20) 

	#if data.InheritsFrom('TH1'): #ROOT.TH1.Class()):   #'TH1'):#else pass
	#	data.SetMarkerStyle(20)

	# TT.SetLineColor(ROOT.kRed - 4)
	# VV.SetLineColor(ROOT.kYellow - 2)
	# DY.SetLineColor(ROOT.kOrange - 2)
	# ST.SetLineColor(ROOT.kYellow + 1)
	# ZH.SetLineColor(ROOT.kMagenta - 9)


	TT.SetLineColor(ROOT.kRed - 4)
	VV.SetLineColor(ROOT.kSpring + 5)
	DY.SetLineColor(ROOT.kOrange - 2)
	ST.SetLineColor(ROOT.kBlue - 4)
	ZH.SetLineColor(ROOT.kMagenta - 9)


	TT.SetFillColor(ROOT.kRed - 4)
	VV.SetFillColor(ROOT.kSpring + 5)
	DY.SetFillColor(ROOT.kOrange - 2)
	ST.SetFillColor(ROOT.kBlue - 4)
	ZH.SetFillColor(ROOT.kMagenta - 9)
	
	#HZZ.SetFillColor(ROOT.kYellow + 1)
	#HWW.SetFillColor(ROOT.kYellow - 2)
	if not hzz_is_absent and not hww_is_absent:
		print 'HZZ', HZZ
		HZZ.SetLineColor(ROOT.kAzure + 6 )#Blue - 4)
		HWW.SetLineColor(ROOT.kTeal - 3 )#Spring + 5)

		HWW.SetLineStyle(7)
		HZZ.SetLineStyle(9)
		#https://root-forum.cern.ch/t/different-ways-of-normalizing-histograms/15582/6
		if 'SR' in ifile.GetName() and int(os.getcwd().split('/')[-1]) > 450:
			mult = 1
		else:
			mult = visualization_mult_factor 
		HZZ.Scale(mult)
		HWW.Scale(mult)

	#hzzClone = HZZ
	#hwwClone = HWW#.Clone()
	#HZZ = hzzClone.Clone()
	#HWW = hwwClone.Clone()
	#zj1b.SetFillColor(398)
	#zj2b.SetLineColor(400)
#https://github.com/capalmer85/AnalysisTools/blob/5aa23260f2e1f47c59d692c04e7b0144328a358b/StatTools/Jan21/plotCardshapes_postfit_vv.py

	TT.SetFillStyle(1001)
	VV.SetFillStyle(1001)
	DY.SetFillStyle(1001)
	ST.SetFillStyle(1001)
	ZH.SetFillStyle(1001)
	TT.SetLineStyle(1)
	VV.SetLineStyle(1)
	DY.SetLineStyle(1)
	ST.SetLineStyle(1)
	ZH.SetLineStyle(1)

	if not hzz_is_absent and not hww_is_absent:#includeAbsentSignal:
		HZZ.SetFillStyle(1001)
		HWW.SetFillStyle(1001)

      
	stack = ROOT.THStack("stack", "stack")
	# for h in VV, ST, ZH, DY, TT:#bg_hists:
	# 	stack.Add(h)
	
	if stack_manually:
		for h in VV, ST, ZH, DY, TT:#bg_hists:
			stack.Add(h)
	else:
		print 'adding manually'
		stack.Add(VV)
		stack.Add(ST)
		stack.Add(ZH)
		if 'DY' in ifile:
			stack.Add(TT)
			stack.Add(DY)
		else:
			stack.Add(DY)
			stack.Add(TT)

		

	#VV.Scale(100)
	#ST.Scale(100)
	#ZH.Scale(100)

	#FIXME add or not??
	#if not hww_is_absent:
	#	stack.Add(HWW)
	#if not hzz_is_absent:
	#	stack.Add(HZZ)



	#if includeAbsentSignal:
	#	stack.Add(HZZ)
	#	stack.Add(HWW)
	#use this?
	#stack = TotalProcs #????????????????


	totalerr = TotalProcs.Clone("totalerr")
	#totalerr = TotalBkg.Clone("totalerr")

        #totalerr.Sumw2()
        totalerr.SetFillColor(ROOT.kGray + 3)
        totalerr.SetMarkerSize(0)
        totalerr.SetLineColor(ROOT.kGray)
        totalerr.SetFillStyle(3013)
	totalerr.SetLineStyle(4)

	canv = ROOT.TCanvas("canv", "canv", 600, 600)
	canv.cd()
	if plotData_in_SR:
		canv.SetBottomMargin(0.2) #0.3 to separate two pads
	xmin = int(math.floor(TotalProcs.GetBinCenter(1)))
	xmax = int(math.ceil(TotalProcs.GetBinCenter( TotalProcs.GetNbinsX() )))
	print 'xmin', xmin
	print 'xmax', xmax
	#if 'bdt' in ifile:
	#	xmin, xmax = -1.01, 1.01
	
	frame = ROOT.TH1F("frame", "", 1, xmin, xmax)
	canv.SetLogy()

	frame.SetStats(0)
	frame.GetXaxis().SetLabelSize(0)
	#if plotData_in_SR:
	frame.GetXaxis().SetTitleOffset(1.3)
	#else:
	frame.GetXaxis().SetTitleOffset(1.15)
	frame.GetYaxis().SetTitleOffset(1.3)
	frame.GetYaxis().SetTitle("Events")
	# frame.GetXaxis().SetTitle("atanhBDT")
	frame.GetYaxis().SetLabelSize(0.04)
	#frame.GetYaxis().SetMoreLogLabels(1)
	
	#ROOT.gStyle.SetNdivisions(999, "y");
	#https://root.cern.ch/doc/master/classTStyle.html#aa8f3cf9d3e427f9c7d5a24df7296cd10
	#frame.GetYaxis().SetRangeUser(TotalProcs.GetMinimum() if TotalProcs.GetMinimum() > 0 else 10, TotalProcs.GetMaximum() * 3.5)
	#frame.GetYaxis().SetRangeUser(10, TotalProcs.GetMaximum() * 3.5)
	if bdt_plot:
		frame.GetYaxis().SetRangeUser(1, TotalProcs.GetMaximum() * 6.5)  
	else:
		frame.GetYaxis().SetRangeUser(0.1, TotalProcs.GetMaximum() * 6.5)#TotalProcs.GetMaximum() * 3.5)
	# if 'bdt' in ifile.GetName() and 'TT' in ifile.GetName():
	# 	frame.GetYaxis().SetRangeUser(10, TotalProcs.GetMaximum() * 1.5)
	# 	#frame.GetYaxis().SetRangeUser(10E-9, TotalProcs.GetMaximum() * 1.5)
	# else:
	# 	frame.GetYaxis().SetRangeUser(10, TotalProcs.GetMaximum() * 1.5)
	# #	print 'doing bdt'*50
	# #frame.GetYaxis().SetRangeUser(1, 150)
	
	


	# frame.GetYaxis().SetRangeUser(10E-03,200)
        if not plotData_in_SR:
		frame.GetXaxis().SetLabelSize(0.04)
		frame.GetXaxis().SetTitle(data.GetXaxis().GetTitle())


	frame.Draw()
	#canv.Modified() # not sure if needed though
	#canv.Update()

	# for idx, h in enumerate(bg_hists):
	# 	if idx ==0:
	# 		h.Draw('')
	# 	else:
	# 		h.Draw('same')
	stack.Draw("same hist")



	#stack.Draw()
	#TT.Draw('same')
	TotalBkg.SetLineColor(ROOT.kOrange)
	#TotalBkg.Draw('same')
	
	TotalProcs.SetLineColor(ROOT.kRed)
	#TotalProcs.Draw('same')

	print 'of', stack
	stack.Print('all')
	#pad.Modified()
	#pad.Update()
	#canv.Modified() # not sure if needed though
	#canv.Update()
	if plotData_in_SR:
		data.Draw("Psame")
	#canv.Modified() # not sure if needed though
	#canv.Update()

	totalerr.Draw("e2 same")
	#canv.Modified() # not sure if needed though
	#canv.Update()
	print 'data.Chi2Test TotalProcs:'
	print "Chi2/NDF = ", data.Chi2Test( TotalProcs , "UWCHI2/NDF")
	print 'data.Chi2Test TotalBkg:'
        print "Chi2/NDF = ", data.Chi2Test( TotalBkg , "UWCHI2/NDF")
	print 'TotalProcs.Chi2Test TotalBkg:'
	print "Chi2/NDF = ", TotalProcs.Chi2Test(TotalBkg , "WWCHI2/NDF")

	print 'ifile', ifile
	chi2 = data.Chi2Test( TotalProcs , "UWCHI2/NDF")
	# print "Total bkg: ",stack.GetHistogram().GetIntegral()
	# stack.Draw("ep same")
	stack.SetTitle(postFitDir)
	# stack.GetXaxis().SetTitle("Mjj [GeV]")
	
	
# print "Total data: ",data.Integral()
	# bkg.Draw("hist")
	# bkg.Draw("ep same")
	# stackvv.Draw("hist same")
	# stackvv.Draw("ep same")
	# TT.Draw("HISTsame")
	leg = ROOT.TLegend(0.7, 0.7, 0.9, 0.89)
	leg.SetFillStyle(-1)
	leg.SetBorderSize(0)
	leg.AddEntry(VV, "VV", "F")
	leg.AddEntry(ST, "ST", "F")
	leg.AddEntry(DY, "DY", "F")
	leg.AddEntry(ZH, "ZH", "F")
	leg.AddEntry(TT, "TT", "F")
	leg.AddEntry(totalerr, "Total uncertainty", "F")
	#leg.AddEntry(TotalBkg, "TotalBkg", "F")
	#leg.AddEntry(TotalProcs, "TotalProcs", "F")


	if not hww_is_absent and not hzz_is_absent:
		leg.AddEntry(HZZ, "bbZZ x {0}".format(mult), "L")
		leg.AddEntry(HWW, "bbWW x {0}".format(mult), "L")
	if plotData_in_SR:
		leg.AddEntry(data, "Data", "EPL")
	leg.Draw("same")
	if plotData_in_SR:
		#https://root-forum.cern.ch/t/axis-labels-overlapped-by-pad/6920/13
		pad2 = ROOT.TPad("pad2", "pad2", 0., 0., 1., 1.)
		pad2.SetTopMargin(0.73)
	#	pad2.SetBottomMargin(0.)
	#	pad2.SetRightMargin(0.)
		pad2.SetFillColor(0)
		pad2.SetFillStyle(0)
		pad2.Draw()
		pad2.cd()

		frame2 = ROOT.TH1F("frame2", "", 1, xmin, xmax)
		frame2.SetMinimum(-0.5)
	#frame2.SetMinimum(0.5)
		frame2.SetMaximum(0.5)
	#frame2.SetMaximum(1.5)
		frame2.GetYaxis().SetLabelSize(0.02)
		frame2.GetYaxis().SetTitleSize(0.04)
		frame2.GetXaxis().SetLabelSize(0.04)
		frame2.GetXaxis().SetTitle(data.GetXaxis().GetTitle())
	

		frame2.SetStats(0)
		frame2.GetYaxis().SetTitle("Data/MC - 1")
	#frame2.GetYaxis().SetTitle("Data/MC")
		frame2.Draw()
	data2 = data.Clone("data2")

	
	mc_total = TotalProcs.Clone('mt_total') #stack.GetStack().Last().Clone("mc_total")
	data2.Add(mc_total, -1)
	data2.Divide(mc_total)
	mc_total_uncUp = TotalProcs.Clone("mc_total_Up") #stack.GetStack().Last().Clone("mc_total")
	mc_total_uncDown = TotalProcs.Clone("mc_total_Down") #stack.GetStack().Last().Clone("mc_total")
	
	
	
	for i in range(0, mc_total_uncUp.GetNbinsX()):
		#error on (data-mc)/mc is equal to error on data/mc, as (data-mc)/mc = data/mc -1 and the constant - 1 has zero error if we propagate it to the error on the different of data/mc and 1
		#error on r = data/mc => delta_r = r * sqrt((delta_data/data)^2 + (delta_mc/mc)^2)
		e = 0.
		#if mc_total.GetBinContent(i + 1) != 0 and mc_total.GetBinContent(i + 1) < tolerance: continue
		#if data.GetBinContent(i + 1) != 0 and data.GetBinContent(i + 1) < tolerance: continue
		if mc_total.GetBinContent(i + 1) > tolerance and data.GetBinContent(i + 1) > tolerance:
			#if mc_total.GetBinContent(i + 1) < 0.000001 or data.GetBinContent(i + 1) < 0.000001:
			#	continue
			r = data.GetBinContent(i + 1)/mc_total.GetBinContent(i + 1)
			delta_data_over_data = data.GetBinError(i + 1) / data.GetBinContent(i + 1)
			delta_mc_over_mc = mc_total.GetBinError(i + 1) / mc_total.GetBinContent(i + 1)
			delta_r = r * math.sqrt(delta_data_over_data**2 + delta_mc_over_mc**2)
			e = delta_r  
		mc_total_uncUp.SetBinContent(i + 1, e)
		#mc_total_uncUp.SetBinError(i + 1, 0)
		mc_total_uncDown.SetBinContent(i + 1, -e)
                #mc_total_uncDown.SetBinError(i + 1, 0)

	# for i in range(0, mc_total_uncUp.GetNbinsX()):
	# 	e = 0.
	# 	if mc_total.GetBinContent(i + 1) != 0:
	# 		e = mc_total.GetBinError(i + 1) / mc_total.GetBinContent(i + 1)
	# 	mc_total_uncUp.SetBinContent(i + 1, e)
	# 	mc_total_uncDown.SetBinContent(i + 1, -e)


	latex2 = ROOT.TLatex()
	latex2.SetNDC()
	latex2.SetTextSize(0.3*canv.GetTopMargin())
	latex2.SetTextFont(42)
	latex2.SetTextAlign(31) # align right                                                  
	latex2.DrawLatex(0.9, 0.91,"35.9 fb^{-1} (13 TeV)")
		#latex2.SetTextSize(0.9*canv.GetTopMargin())
		#latex2.SetTextFont(52)
		#latex2.SetTextAlign(11) # align right                                                  
		
		#latex2.SetTextSize(0.5*canv.GetTopMargin())
		#latex2.SetTextFont(42)
	latex2.SetTextAlign(11)
	latex2.DrawLatex(0.12, 0.91, "CMS preliminary") #"Work in progress")   
	#chi2string = '#chi^{{2}}#lower[0.1]{{/#it{{dof}} = {0:.2f}}}'.format(data.Chi2Test( TotalProcs , "UWCHI2/NDF"))
	chi2string = "#chi^{2}/" + "NDF = {0}".format(round(chi2, 2)) 
	if plotData_in_SR or 'SR' not in ifile.GetName():
		latex2.DrawLatex(0.12, 0.87, chi2string)#"Chi2/NDF = {0}".format(data.Chi2Test( TotalProcs , "UWCHI2/NDF"))) #"Work in progress")   


	# ratiostaterr = TotalProcs.Clone("ratiostaterr")
        # ratiostaterr.Sumw2()
        # ratiostaterr.SetStats(0)
        # ratiostaterr.SetTitle("")
        # ratiostaterr.GetXaxis().SetTitle(xtitle)
        # ratiostaterr.GetYaxis().SetTitle("Data/MC")
        # ratiostaterr.SetMaximum(2.2)
        # ratiostaterr.SetMinimum(0)
        # ratiostaterr.SetMarkerSize(0)
        # ratiostaterr.SetFillColor(kRed)
        # ratiostaterr.SetFillStyle(3013)
        # #ratiostaterr.SetFillStyle(3001)
        # ratiostaterr.GetXaxis().CenterTitle()
        # ratiostaterr.GetXaxis().SetLabelSize(0.12)
        # ratiostaterr.GetXaxis().SetTitleSize(0.14)
        # ratiostaterr.GetXaxis().SetTitleOffset(1.10)
        # ratiostaterr.GetYaxis().CenterTitle()
        # ratiostaterr.GetYaxis().SetLabelSize(0.10)
        # ratiostaterr.GetYaxis().SetTitleSize(0.12)
        # #ratiostaterr.GetYaxis().SetTitleSize(0.10)
        # ratiostaterr.GetYaxis().SetTitleOffset(0.6)
        # ratiostaterr.GetYaxis().SetNdivisions(505)



	#mc_total_uncUp.Scale(5)
	#mc_total_uncDown.Scale(5)

	mc_total_uncUp.SetLineColor(ROOT.kGray + 3)
	mc_total_uncUp.SetLineWidth(1)
	mc_total_uncUp.SetFillColor(ROOT.kGray + 3)
	mc_total_uncUp.SetFillStyle(3004)
	mc_total_uncDown.SetLineColor(ROOT.kGray + 3)#SetLineColor(ROOT.kGreen)
	mc_total_uncDown.SetLineWidth(1)
	mc_total_uncDown.SetFillColor(ROOT.kGray + 3)
	mc_total_uncDown.SetFillStyle(3004)
	if plotData_in_SR:
		mc_total_uncUp.Draw("HIST SAME")
		mc_total_uncDown.Draw("HIST SAME")
		line = ROOT.TLine(xmin, 0, xmax, 0)
		line.SetLineStyle(3)
		line.Draw("same")
		data2.Draw("PEsame")
	canv.cd()
	canv.Modified()
	canv.Update()
	ROOT.gROOT.ForceStyle()
	ROOT.gPad.RedrawAxis()

	# print "Data yield: ",data.Integral()
	# print "MC yield: ",stack.GetHistogram().Integral()
	# raw_input()
	# canv.SetLogy(True)
	for ext in [".png", ".pdf", ".C", ".root"]:
		canv.SaveAs("{0}_postfit_plot_{1}{2}".format(name, date, ext))
	
	ifile.Close()
	#datafile.Close()
	plotData_in_SR = False


def main():
	print 'starting '
	start_time = time.time()

	files_post = glob.glob('*Postfit.root')
	#files_pre = glob.glob('*.input.root')
	
	#files_of_interest = files_pre + files_post
	files_of_interest = files_post #if 'post' in do_prefit_or_postfit else files_pre

	CRDYfiles = [x for x in files_of_interest if 'CRDY' in x and not ('CMS' in x or 'nominal' in x) ]
	CRTTfiles = [x for x in files_of_interest if 'CRTT' in x and not ('CMS' in x or 'nominal' in x) ]
	SRfiles = [x for x in files_of_interest if 'SR' in x and not ('CMS' in x or 'nominal' in x) ]
	
	print 'CRDYfiles=', CRDYfiles
	print 
	print 'CRTTfiles=', CRTTfiles
	print
	print 'SRfiles=', SRfiles
	print

	
	#files = SRfiles + CRDYfiles + CRTTfiles
	files = CRDYfiles + CRTTfiles +  SRfiles


	
#	files = [		"ee_hhMt_CRDY.postfit.root"         ]
		#'hmass1_CRDY_postfit.root',
		#'hmass1_ee_CRDY_postfit.root',
		#'fitDiagnostics.root',
		#'ee_hmass0_CRDY_postfit_3.root'

	print 'files=', files	
	for fil in files:
		if 'hh' in fil or 'bdt' in fil: pass
		else: 
			continue

		#if 'hh' not in fil: continue
		#if 'ee_zmass_high'  in fil: continue
		#if not do_SR_BDTSideband:
		#if 'CRDY' not in fil: continue
		#if 'CRs' in fil: continue

		if 'plot.' in fil: continue
		#if 'after' in fil: continue
		print
		print 'processing', fil
		# if any(x in fil for x in badRoots):
		# 	print 'any(x in fil for x in badRoots)', any(x in fil for x in badRoots)
		# 	continue
		# else:
		# 	if 'DY' in fil and 'zpt' in fil:
		# 		#'hmass0' not in fil and 'leps' not in fil:
		
                #if 'post' in fil:
		for plotType in "prefit", "postfit":
			createPreFitPlot2(fil, plotType) #do_prefit_or_postfit)        
		#createPostFitPlot(fil)
		
#elif '.input.' in fil:
		#	createPreFitPlot(fil, 'prefit')

		if allow_raw_input:
			raw_input ("press a key to continue making plots...")


	end_time = time.time()
	time_taken = end_time - start_time # time_taken is in seconds

	hours, rest = divmod(time_taken,3600)
	minutes, seconds = divmod(rest, 60)
	print
	print 'all done!'
	print "---it took {hours} hours, {minutes} minutes and {seconds:.1f} seconds to run the analysis ---".format (hours=hours, minutes=minutes, seconds=seconds)
	if allow_raw_input:
		raw_input("Press Enter to exit...")


if __name__ == '__main__':
	sys.exit(main())
