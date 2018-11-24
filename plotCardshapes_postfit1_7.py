import ROOT
import time, os
import sys
import itertools
import multiprocessing
import math
import glob
from copy import deepcopy


#for the plot name
date = 'feb23'
allow_raw_input = True
plotData_in_SR = False
includeAbsentSignal = False
tolerate = 0.000001 #extra 0 should be added?!
stack_manually = False
visualization_mult_factor = 2000 #if int(os.getcwd().split('/')[-1]) < 450 else 1
badRoots = [
	'zmass',
	'dR_bjets'
	'hmass0',
	'dR_bjets',
	'dR_leps'
	'hmass1',
	]

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
	tolerance  = tolerate if 'bdt' not in ifile else 0.09
	
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
	copyTotalProcs = TotalProcs #.Clone()
	for idx, bin in enumerate(copyTotalProcs):
		if copyTotalProcs.GetBinContent(idx) < tolerance:
			copyTotalProcs.SetBinContent(idx, 0)
			copyTotalProcs.SetBinError(idx, 0)

	TotalProcs = copyTotalProcs#.Clone()
	print 'TotalProcs modified'
	TotalProcs.Print('all')
	print 'data', data.Print('all')
	data_clone = data#.Clone()
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

	if not hww_is_absent:
		stack.Add(HWW)
	if not hzz_is_absent:
		stack.Add(HZZ)
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
	
	files = [
		#'hmass1_CRDY_postfit.root',
		#'hmass1_ee_CRDY_postfit.root',
		#'fitDiagnostics.root',
		#'ee_hmass0_CRDY_postfit_3.root'
		]

	files = glob.glob('*postfit.root')
	
	for fil in files:
		#if 'bdt' not in fil: continue
		#if 'TT'  not in fil: continue
		#if 'SR' not in fil: continue
		if 'plot.' in fil: continue
		if 'after' in fil: continue
		print
		print 'processing', fil
		# if any(x in fil for x in badRoots):
		# 	print 'any(x in fil for x in badRoots)', any(x in fil for x in badRoots)
		# 	continue
		# else:
		# 	if 'DY' in fil and 'zpt' in fil:
		# 		#'hmass0' not in fil and 'leps' not in fil:
		createPostFitPlot(fil)
		if allow_raw_input:
			raw_input ("press a key to continue making plots...")


	end_time = time.time()
	time_taken = end_time - start_time # time_taken is in seconds

	hours, rest = divmod(time_taken,3600)
	minutes, seconds = divmod(rest, 60)
	print
	print 'all done!'
	print "---it took {hours} hours, {minutes} minutes and {seconds:.1f} seconds to run the analysis ---".format (hours=hours, minutes=minutes, seconds=seconds)
	raw_input("Press Enter to exit...")


if __name__ == '__main__':
	sys.exit(main())
