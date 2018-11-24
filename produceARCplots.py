import sys, getopt
from copy import deepcopy
import glob
from pprint import pprint as pp
from ROOT import TFile, gStyle
import ROOT
import math

use300GeV = None
date = "July8"
channelIn = None
tolerate = 0.01 #extra 0 should be added?!                                      
runBatchMode = True


class HistHolder(object):
    def __init__(self, name, zmass, zpt, met, njets, nbjets, nnonbjets, nloosebjets, hbbpt, hbbmass, detabb, hhmt):
        self.name = name

        self.zmass = zmass
        self.zpt = zpt
        self.met = met

        self.njets = njets
        self.nbjets = nbjets
        self.nnonbjets = nnonbjets
        self.nloosebjets = nloosebjets

        self.hbbpt = hbbpt
        self.hbbmass = hbbmass
        self.detabb = detabb
        self.hhmt = hhmt

    def __getitem__(self, item):
        return getattr(self, item)

    def getFields(self):
        return [self.name, 
                self.zmass, self.zpt, self.met, 
                self.njets, self.nbjets, self.nnonbjets, self.nloosebjets,
                self.hbbpt, self.hbbmass, self.detabb, self.hhmt]





def createPreFitPlot2(hists, typ, fileNameIn, channelIn):
        if runBatchMode: ROOT.gROOT.SetBatch(True)
        rebin_factor = 1
        plotData_in_SR = True
        visualization_mult_factor = 5000
        stack_manually = True
        useTotalBkg = True
        usesumBGnotTotals = True
        mass = 300 if use300GeV else 900

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

	fileName = fileNameIn #deepcopy(ifile)
	print 'create a plot for', fileNameIn

	#tmpList = ifile.split('Postfit.')[0].split('_')
	channel, name, region, fitType = channelIn, fileNameIn, "SR", "prefit" #tmpList[0], '_'.join(tmpList[1:-2]), tmpList[-2], tmpList[-1]
	#channel, name, region = tmpList[0], '_'.join(tmpList[1:-1]), tmpList[-1]

	
	#name = ifile.split('.input.')[0] #'_'.join((ifile.GetName()).split('_')[:-1])
	print 'name', name#, 'len=', len(name)
	
	#FIX ME later
	do_plotData_in_SR = plotData_in_SR
	print 'do_plotData_in_SR', do_plotData_in_SR
	#tolerance  = 0              #0.001 if ('hh' in name or 'dR' in name or 'zpt' in name) else tolerate
	#tolerance = 0               #0.01 if ('dR_lep' in name and 'SR' not in ifile) else tolerance
	tolerance = tolerate
	
	gStyle.SetOptStat(0)
	#ifile = TFile(ifile)

	innerDir = channel + '_' + region + '_' + typ 

	print 'Dir=', innerDir   #ee_CRDYlow_prefit

        DY1 = hists[0]
        DY2 = hists[1]
        DY3 = hists[2]
        DY4 = hists[3]

        DY= DY1.Clone()
        for h in [DY2, DY3, DY4]:
            if h: DY.Add(h)

        ST1 = hists[4]
        ST2 = hists[5]
        ST3 = hists[6]
        ST4 = hists[7]
        ST5 = hists[8]

        ST= ST1.Clone()
        for h in [ST2, ST3, ST4, ST5]:
            if h: ST.Add(h)

        VV1 = hists[9]
        VV2 = hists[10]
        VV3 = hists[11]

        VV= VV1.Clone()
        for h in [VV2, VV3]:
            if h: VV.Add(h)

        TT = hists[12]
        ZH = hists[13]

        HZZ300 = hists[14]
        HWW300 = hists[15]
        HZZ900 = hists[16]
        HWW900 = hists[17]

        if use300GeV:
            HZZ = HZZ300
            HWW = HWW300
        else:
            HZZ= HZZ900
            HWW= HWW900


        data1 = hists[18]
        data2 = hists[19]
        data3 = hists[20]
        data4 = hists[21]
        data5 = hists[22]
        data6 = hists[23]
        data7 = hists[24]
        data8 = hists[25]

        data= data1.Clone()
        for h in [data2, data3, data4, data5, data6, data7, data8]:
            if h: data.Add(h)



	# ST = ifile.Get("%s/ST" % innerDir)
	# TT = ifile.Get("%s/TT" % innerDir)
	# VV = ifile.Get("%s/VV" % innerDir)
	# DY = ifile.Get("%s/DY" % innerDir)
	# ZH = ifile.Get("%s/ZH" % innerDir)
	# HZZ = ifile.Get("%s/signal_hzz" % innerDir)
	# HWW = ifile.Get("%s/signal_hww" % innerDir)

	# TotalBkg = ifile.Get("%s/TotalBkg" % innerDir)
	# TotalProcs = ifile.Get("%s/TotalProcs" % innerDir)
	# #TotalSig = ifile.Get("%s/TotalSig" % innerDir)
	# data = ifile.Get("%s/data_obs" % innerDir)

	hzz_is_absent = False
	hww_is_absent = False

	if HZZ == None or HZZ.GetSumOfWeights() == 0:
		print 'HZZ', HZZ
		#hzz_is_absent = True
		#HZZ = ifile.Get("%s/signal_hzz" % innerDir.replace('post', 'pre'))
		if HZZ == None:
			hzz_is_absent = True
			print 'damn hzz is not here' *100



	if HWW == None or HWW.GetSumOfWeights() == 0:
		print 'HWW', HWW
		#hww_is_absent = True
		#HWW = ifile.Get("%s/signal_hww" % innerDir.replace('post', 'pre'))
		if HWW == None:
			hww_is_absent = True 
			print 'damn HWW is not here' *100


	for h in ST, TT, VV, DY, ZH, HZZ, HWW, data:#, TotalProcs, TotalBkg:
		if h != None:
			if rebin_factor > 1:
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

        sumBG = ZH.Clone()
	for h in ST, DY, VV, TT:
		if h == None: continue
		print 'h=', h
		sumBG.Add(h)

	# copyTotalProcs = sumBG #.Clone()
	# for idx, bin in enumerate(copyTotalProcs):
	# 	if copyTotalProcs.GetBinContent(idx) < tolerance:
	# 		copyTotalProcs.SetBinContent(idx, 0)
	# 		copyTotalProcs.SetBinError(idx, 0)

	# TotalProcs  = copyTotalProcs#.Clone()



        copyTotalBkg = sumBG.Clone()                                                                                              
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

        if not hzz_is_absent and not hww_is_absent:
                #print 'HZZ', HZZ                                                                                                                    
                HZZ.SetLineColor(ROOT.kRed - 3)#Azure + 6 )#Blue - 4)                                                                                
                HWW.SetLineColor(ROOT.kTeal - 7 )#Spring + 5)                                                                                        

                HWW.SetLineStyle(7)
                HWW.SetLineWidth(2)
                HZZ.SetLineStyle(7)
                HZZ.SetLineWidth(2)
                #https://root-forum.cern.ch/t/different-ways-of-normalizing-histograms/15582/6                                                       
                #if 'SR' in ifile.GetName() and                                                                                                      

                if use300GeV:#'SR' in ifile.GetName() and mass >= 450:
                        mult = 2500
                else:
                        mult = 150 #visualization_mult_factor
		HZZ.Scale(mult)
		HWW.Scale(mult)

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
		if True: #'DY' in fileName:
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
		else:
                        
                        if VV != None:
                                stack.Add(VV)
                        if ST != None:
				stack.Add(ST)
                        if ZH != None: 
				stack.Add(ZH)
			if DY != None:
				stack.Add(DY)
			if TT != None:
				stack.Add(TT)
		

	if useTotalBkg:
		totalerr = TotalBkg.Clone("totalerr")
                TotalProcs = TotalBkg
	#else:
	#	totalerr = TotalProcs.Clone("totalerr")
		
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
	if False:
            if 'hhmt_' in name:
                xmin, xmax = 400, 1400

	print 'xmin', xmin
	print 'xmax', xmax
	#if 'bdt' in ifile:
	#	xmin, xmax = -1.01, 1.01
	
	
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
	#if 'bdt' in name:

	minFactor = 2 if mass <=450 else 0.2
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
	#canv.Modified() # not sure if needed though
	#canv.Update()

	# for idx, h in enumerate(bg_hists):
	# 	if idx ==0:
	# 		h.Draw('')
	# 	else:
	# 		h.Draw('same')
	stack.Draw("same hist")
	ROOT.gPad.RedrawAxis()
		
	if not hzz_is_absent:
		HZZ.Draw("same hist")
	if not hww_is_absent:
		HWW.Draw("same hist")


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

	leg = ROOT.TLegend(0.7, 0.7, 0.9, 0.89)
	leg.SetFillStyle(-1)
	leg.SetBorderSize(0)
	if VV != None: leg.AddEntry(VV, "VV", "F")
	if ST != None: leg.AddEntry(ST, "ST", "F")
	if DY != None: leg.AddEntry(DY, "DY", "F")
	if ZH != None: leg.AddEntry(ZH, "ZH", "F")
	if TT != None: leg.AddEntry(TT, "TT", "F")
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
	placeChi2 = False if (round(chi2, 2) == 0 or chi2 > 500) or 'pre' in typ  else True
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
	postfit_type = 'prefit' #'CRsPostfit' if 'CRsPostfit' in fileName else 'FullPostfit'

	for ext in [".png", ".C"]:#, ".pdf", ".C", ".root"]:
		canv.SaveAs("{0}_plot_{1}_{2}{3}".format(name, date, channelIn, ext))
	
        #ifile.Close()
	#datafile.Close()
	do_plotData_in_SR = False



def dealWithSingleHists(histograms):
    print 
    for h in histograms:
        print h


def combineAlikeHistograms(inPut):
    
    print 'inPut'
    #pp(inPut)
    for k, v in inPut.items():
        print k
        print v.__dict__
        print 
    
    DYs = [v for k,v in inPut.items() if "DY" in k]
    STs = [v for k,v in inPut.items() if "ST" in k]
    VVs = [v for k,v in inPut.items() if ("WW" in k or "ZZ" in k or "WZ" in k)]
    datas = [v for k,v in inPut.items() if "Run" in k]
    signals = [v for k,v in inPut.items() if "2L2Nu" in k]

    B2VTo2L2Nu_M_900 = inPut['B2VTo2L2Nu_M_900']
    B2ZTo2L2Nu_M_300 = inPut['B2ZTo2L2Nu_M_300']
    B2VTo2L2Nu_M_300 = inPut['B2VTo2L2Nu_M_300']
    B2ZTo2L2Nu_M_900 = inPut['B2ZTo2L2Nu_M_900']

    TTbar = inPut['TT']
    ZHiggs = inPut['ZH']

    print 'B2ZTo2L2Nu_M_900', B2ZTo2L2Nu_M_900

    print 'signals', signals

    for _ in signals:
        pp(_.__dict__)


    for idx, plotType in enumerate(['zmass', 'zpt', 'met',
                'njets', 'nbjets', 'nnonbjets', 'nloosebjets',
                'hbbpt', 'hbbmass', 'detabb', 'hhmt']):
        #if idx > 0 : return

        DY_a = DYs[0][plotType]
        DY_b = DYs[1][plotType]
        DY_c = DYs[2][plotType]
        DY_d = DYs[3][plotType]

        print 'DY_a', DY_a


        VTo2L2Nu_M_900 = B2VTo2L2Nu_M_900[plotType]
        ZTo2L2Nu_M_300 = B2ZTo2L2Nu_M_300[plotType]
        VTo2L2Nu_M_300 = B2VTo2L2Nu_M_300[plotType]
        ZTo2L2Nu_M_900 = B2ZTo2L2Nu_M_900[plotType]

        TT = TTbar[plotType]
        ZH = ZHiggs[plotType]

        print 'VTo2L2Nu_M_900', VTo2L2Nu_M_900


        ST_a = STs[0][plotType]
        ST_b = STs[1][plotType]
        ST_c = STs[2][plotType]
        ST_d = STs[3][plotType]
        ST_e = STs[4][plotType]


        VV_a = VVs[0][plotType]
        VV_b = VVs[1][plotType]
        VV_c = VVs[2][plotType]



        data_a = datas[0][plotType]
        data_b = datas[1][plotType]
        data_c = datas[2][plotType]
        data_d = datas[3][plotType]
        data_e = datas[4][plotType]
        data_f = datas[5][plotType]
        data_g = datas[6][plotType]
        data_h = datas[7][plotType]
        
        for i in range(len(DY_a)):
            #if i > 2: return

            print 'DY_a[0]', DY_a[0]
            print 'DY_a[1]', DY_a[1]
            fileNameIn = DY_a[i].GetName()
            histsMC = [
                DY_a[i], DY_b[i], DY_c[i], DY_d[i],
                ST_a[i], ST_b[i], ST_c[i], ST_d[i], ST_e[i], 
                VV_a[i], VV_b[i], VV_c[i],
                TT[i], 
                ZH[i]
                ]
            histsSignal = [
                ZTo2L2Nu_M_300[i],
                VTo2L2Nu_M_300[i],
                ZTo2L2Nu_M_900[i],
                VTo2L2Nu_M_900[i]
                ]
            histsData = [
                data_a[i], data_b[i], data_c[i], data_d[i], 
                data_e[i], data_f[i], data_g[i], data_h[i]
                ]

            hists = histsMC + histsSignal + histsData
            #dealWithSingleHists(hists)
            typ = "prefit"

            #channelIn = "ee" if "eles" in inDir else "mm" if "muons" in inDir else None
            if channelIn == None:
                print 'please check channelIn, exiting...'
                sys.exit(1)
            createPreFitPlot2(hists, typ, fileNameIn, channelIn)









def pickHistogram(key, hists):
    return_list =  [h for h in hists if key in h.GetName()]
    return return_list[0] if return_list != [] else None

def separateHists(key, hists, extra = "placeHolder"):
    return [h for h in hists if key in h.GetName() and extra not in h.GetName() and "_"+h.GetName().split("_")[1] in ["_preselection", "_trigger", "_zmass", "_2bjets", "_hbb", "_hhmt", "_met"]]

    
def collectHists(inDir):
    print 'inDir', inDir
    files = glob.glob(inDir + "/*root")
    #print 'files', files
    storage = {}
    for f in files:
        fin = TFile(f)
        names_k_v = {(h.GetClassName(), h.GetName()) for h in fin.GetListOfKeys()}
        names = [v for k, v in names_k_v if k == "TH1F"]
        print 'names', names
        hists = [fin.Get(n) for n in names]
        print 'hists', hists
        zmass = separateHists("zmass_", hists)
        zpt = separateHists("zpt_", hists)
        met = separateHists("met_", hists)
        njets = separateHists("njets_", hists)
        nbjets = separateHists("nbjets_", hists, "non")
        nnonbjets = separateHists("nnonbjets_", hists)
        nloosebjets = separateHists("nloosebjets_", hists)
        hbbpt = separateHists("hbbpt_", hists)
        hbbmass = separateHists("hbbmass_", hists)
        detabb = separateHists("detabb_", hists)
        hhmt = separateHists("hhmtt_", hists)
        print 'zmass', zmass
        print 
        print 'working with', f
        if "TT" in f:
            obj = tt_HistHolder = HistHolder("TT", zmass, zpt, met, njets, nbjets, nnonbjets, nloosebjets, hbbpt, hbbmass, detabb, hhmt)
            #pp(tt_HistHolder.__dict__)
            
        elif "DY1" in f:
            obj = dy1_HistHolder = HistHolder("DY1", zmass, zpt, met, njets, nbjets, nnonbjets, nloosebjets, hbbpt, hbbmass, detabb, hhmt)
        elif "DY2" in f:
            obj = dy2_HistHolder = HistHolder("DY2", zmass, zpt, met, njets, nbjets, nnonbjets, nloosebjets, hbbpt, hbbmass, detabb, hhmt)
        elif "DY3" in f:
            obj = dy3_HistHolder = HistHolder("DY3", zmass, zpt, met, njets, nbjets, nnonbjets, nloosebjets, hbbpt, hbbmass, detabb, hhmt)
        elif "DY4" in f:
            obj = dy4_HistHolder = HistHolder("DY4", zmass, zpt, met, njets, nbjets, nnonbjets, nloosebjets, hbbpt, hbbmass, detabb, hhmt)

        elif "ZZ" in f:
            obj = zz_HistHolder = HistHolder("ZZ", zmass, zpt, met, njets, nbjets, nnonbjets, nloosebjets, hbbpt, hbbmass, detabb, hhmt)
        elif "WZ" in f:
            obj = wz_HistHolder = HistHolder("WZ", zmass, zpt, met, njets, nbjets, nnonbjets, nloosebjets, hbbpt, hbbmass, detabb, hhmt)
        elif "WW" in f:
            obj = ww_HistHolder = HistHolder("WW", zmass, zpt, met, njets, nbjets, nnonbjets, nloosebjets, hbbpt, hbbmass, detabb, hhmt)

        elif "ZH" in f:
            obj = zh_HistHolder = HistHolder("ZH", zmass, zpt, met, njets, nbjets, nnonbjets, nloosebjets, hbbpt, hbbmass, detabb, hhmt)

        elif "ST_s-channel" in f:
            obj = ST_s_channel_HistHolder = HistHolder("ST_s_channel", zmass, zpt, met, njets, nbjets, nnonbjets, nloosebjets, hbbpt, hbbmass, detabb, hhmt)
        elif "ST_tW_top" in f:
            obj = ST_tW_top_HistHolder = HistHolder("ST_tW_top", zmass, zpt, met, njets, nbjets, nnonbjets, nloosebjets, hbbpt, hbbmass, detabb, hhmt)
        elif "ST_tW_antitop" in f:
            obj = ST_tW_antitop_HistHolder = HistHolder("ST_tW_antitop", zmass, zpt, met, njets, nbjets, nnonbjets, nloosebjets, hbbpt, hbbmass, detabb, hhmt)
        elif "ST_t-channel_antitop" in f:
            obj = ST_t_channel_antitop_HistHolder = HistHolder("ST_t_channel_antitop", zmass, zpt, met, njets, nbjets, nnonbjets, nloosebjets, hbbpt, hbbmass, detabb, hhmt)
        elif "ST_t-channel_top" in f:
            obj = ST_t_channel_top_HistHolder = HistHolder("ST_t_channel_top", zmass, zpt, met, njets, nbjets, nnonbjets, nloosebjets, hbbpt, hbbmass, detabb, hhmt)

        elif "2B2ZTo2L2Nu_M-300" in f:
            obj = B2ZTo2L2Nu_M_300_HistHolder = HistHolder("B2ZTo2L2Nu_M_300", zmass, zpt, met, njets, nbjets, nnonbjets, nloosebjets, hbbpt, hbbmass, detabb, hhmt)
        elif "2B2VTo2L2Nu_M-300" in f:
            obj = B2VTo2L2Nu_M_300_HistHolder = HistHolder("B2VTo2L2Nu_M_300", zmass, zpt, met, njets, nbjets, nnonbjets, nloosebjets, hbbpt, hbbmass, detabb, hhmt)
            
        elif "2B2ZTo2L2Nu_M-900" in f:
            obj = B2ZTo2L2Nu_M_900_HistHolder = HistHolder("B2ZTo2L2Nu_M_900", zmass, zpt, met, njets, nbjets, nnonbjets, nloosebjets, hbbpt, hbbmass, detabb, hhmt)
        elif "2B2VTo2L2Nu_M-900" in f:
            obj = B2VTo2L2Nu_M_900_HistHolder = HistHolder("B2VTo2L2Nu_M_900", zmass, zpt, met, njets, nbjets, nnonbjets, nloosebjets, hbbpt, hbbmass, detabb, hhmt)


        elif "Run2016B" in f:
            obj = Run2016B_HistHolder = HistHolder("Run2016B", zmass, zpt, met, njets, nbjets, nnonbjets, nloosebjets, hbbpt, hbbmass, detabb, hhmt)            
        elif "Run2016C" in f:
            obj = Run2016C_HistHolder = HistHolder("Run2016C", zmass, zpt, met, njets, nbjets, nnonbjets, nloosebjets, hbbpt, hbbmass, detabb, hhmt)
        elif "Run2016D" in f:
            obj = Run2016D_HistHolder = HistHolder("Run2016D", zmass, zpt, met, njets, nbjets, nnonbjets, nloosebjets, hbbpt, hbbmass, detabb, hhmt)
        elif "Run2016E" in f:
            obj = Run2016E_HistHolder = HistHolder("Run2016E", zmass, zpt, met, njets, nbjets, nnonbjets, nloosebjets, hbbpt, hbbmass, detabb, hhmt)
        elif "Run2016F" in f:
            obj = Run2016F_HistHolder = HistHolder("Run2016F", zmass, zpt, met, njets, nbjets, nnonbjets, nloosebjets, hbbpt, hbbmass, detabb, hhmt)
        elif "Run2016G" in f:
            obj = Run2016G_HistHolder = HistHolder("Run2016G", zmass, zpt, met, njets, nbjets, nnonbjets, nloosebjets, hbbpt, hbbmass, detabb, hhmt)
        elif "Run2016H" in f and "ver2" in f:
            obj = Run2016H_ver2_HistHolder = HistHolder("Run2016H_ver2", zmass, zpt, met, njets, nbjets, nnonbjets, nloosebjets, hbbpt, hbbmass, detabb, hhmt)
        elif "Run2016H" in f and "ver3" in f:
            obj = Run2016H_ver3_HistHolder = HistHolder("Run2016H_ver3", zmass, zpt, met, njets, nbjets, nnonbjets, nloosebjets, hbbpt, hbbmass, detabb, hhmt)


        else:
            obj = None
            
        if obj != None:
            #pp(obj.__dict__)
            storage[obj.name] = deepcopy(obj)
            #print 'zmass', obj.zmass

    #pp(B2ZTo2L2Nu_M_300_HistHolder.__dict__)
    #pp(obj.__dict__)
    print 
    for k,v in storage.items():
        print k
        if "900" in k:
            trig_hist = pickHistogram("_trigger", v.zmass)
            print trig_hist
        if v.zmass[0] == None:
            print v.zmass

    print
    combineAlikeHistograms(storage)    
    return storage





def main(argv):
   inDir = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["inputDir=","ofile="])
   except getopt.GetoptError:
      print 'test.py -i <inDir> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <inDir> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--inputDir"):
         inDir = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   print 'Input file is ', inDir
   if outputfile:
       print 'Output file is "', outputfile

   if inDir == "":
       print 'check inDir, exiting....'
       sys.exit(1)

   global use300GeV
   if '40' in inDir:
       use300GeV = True
   elif '100' in inDir:
       use300GeV = False
   else:
       print 'exiting, please check 40 or 100 met cut is used, so the program knows to use 300 or 900 gev signal...'
       sys.exit(1)

   global channelIn
   channelIn = "ee" if"eles" in inDir else "mm" if "muons" in inDir else None

   collectHists(inDir)

if __name__ == "__main__":
    main(sys.argv[1:])
    #print 'skipList:'
    #pp(sorted(skipList))
