#!/usr/bin/env python

import optparse
import os,sys
import json
import ROOT
import math
import collections, operator
import io

debugMode = False
def bazinga (mes):
    if debugMode:
        print mes


"""
A wrapper to store data and MC histograms for comparison
"""
class Plot(object):

    def __init__(self,name):
        self.name = name
        self.mc = {}
        self.mcSignal = {}
        self.dataH = None
        self.data = None
        self._garbageList = []
        self.plotformats = ['pdf','png', 'root']
        self.savelog = False
        self.ratiorange = (0.46,1.54)

    def add(self, h, title, color, isData, isSignal):
        h.SetTitle(title)
        sampleType = None

        if title.startswith('t'):
            sampleType = 'TT'
        elif title.startswith('Single'):
            sampleType = 'ST'
        elif title.startswith('Diboson'):
            sampleType = 'VV'
        elif title.startswith('ZH'):
            sampleType = 'ZH'
        elif title.startswith('DY'):
            sampleType = 'DY'
        elif title.startswith('Data'):
            sampleType = 'data_obs'
        elif title.startswith('wwBGrav'):
            sampleType = 'signal_ww'
        elif title.startswith('zzBGrav'):
            sampleType = 'signal_zz'
        else:
            print 'something is wrong with ', title
            sys.exit(1)
        #if sampleType.startswith('sig'):
         #   print 'title is ', title
          #  print 'sampleType is ', sampleType

        if isData:
            try:
                self.dataH.Add(h)
            except:
                self.dataH=h
                self.dataH.SetName('%s_%s' % (self.dataH.GetName(), sampleType ) )
                self.dataH.SetDirectory(0)
                self.dataH.SetMarkerStyle(20) #20
 #               self.dataH.SetMarkerSize(0.9)
                self.dataH.SetMarkerColor(color)
                self.dataH.SetLineColor(ROOT.kBlack)
                self.dataH.SetLineWidth(2)
                self.dataH.SetLineStyle(7)

                self.dataH.SetFillColor(0)
                self.dataH.SetFillStyle(0)
                self._garbageList.append(h)

        elif not isData and not isSignal:
            
            try:
                self.mc[title].Add(h)
            except:
                self.mc[title]=h
                self.mc[title].SetName('%s_%s' % (self.mc[title].GetName(), sampleType ) )
                self.mc[title].SetDirectory(0)
                self.mc[title].SetMarkerStyle(1)
                self.mc[title].SetMarkerColor(color)
                self.mc[title].SetLineColor(color) #ROOT.kBlack)
                self.mc[title].SetLineWidth(2) #1
                #self.mc[title].SetFillColor(color)
                #self.mc[title].SetFillStyle(1001)
                self._garbageList.append(h)

                
        elif not isData and isSignal:

            try:
                self.mcSignal[title].Add(h)
            except:
                self.mcSignal[title]=h
                self.mcSignal[title].SetName('%s_%s' % (self.mcSignal[title].GetName(), sampleType ) )
                self.mcSignal[title].SetDirectory(0)
                self.mcSignal[title].SetMarkerStyle(1) #20
 #               self.mcSignal[title].SetMarkerSize(0.9)
                self.mcSignal[title].SetMarkerColor(color)
                self.mcSignal[title].SetLineColor(color)
                self.mcSignal[title].SetLineWidth(2)
                self.mcSignal[title].SetLineStyle(7)

                self.mcSignal[title].SetFillColor(0)
                #uncomment for overlay hists
                #self.mcSignal[title].SetFillStyle(0)
                self._garbageList.append(h)
        else:
            print "problem appearred, exiting..."
            exit(1)


    def finalize(self):
        self.data = convertToPoissonErrorGr(self.dataH)

    def appendTo(self,outUrl):
        #print 'before opening the file in fcn appendTo'
        outF = ROOT.TFile.Open(outUrl,'UPDATE')
        #print 'after opening the file in fcn appendTo'
        # fix me: Error in <TFile::cd>: Unknown directory xyz
        # which disappears if run the script again
        if not outF.cd(self.name):
            print 'before making directory in fcn appendTo'
            outDir = outF.mkdir(self.name)
            outDir.cd()
        #print 'before loop over mc in appendTo'
        for m in self.mc :
            self.mc[m].Write(self.mc[m].GetName(), ROOT.TObject.kOverwrite)

        for mS in self.mcSignal :
            self.mcSignal[mS].Write(self.mcSignal[mS].GetName(), ROOT.TObject.kOverwrite)

        if self.dataH :
            self.dataH.Write(self.dataH.GetName(), ROOT.TObject.kOverwrite)
        if self.data:
            self.data.Write(self.data.GetName(), ROOT.TObject.kOverwrite)
        outF.Close()

    def reset(self):
        for ob in self._garbageList:
            try:
                bazinga('before deleting object  ')
                print ob
                ob.Delete()
                bazinga('stuck in try statement deleting ')
                
            except:
                bazinga ('silently pass')
                pass


    def simpleStackNoRatio(self, outDir,lumi,noScale=False,saveTeX=False):
        print 'I am here'
        hs = ROOT.THStack("hs","Stacked 1D histograms")
#        hTot = ROOT.TH1F ("hTot","total hist")
        hTot = None
        dummyName = None

        # for k, v in self.mc.items():
        #     # Display key and value.
        #     print(k, v)

        binmax = 0 #h.GetMaximumBin()

        for count, h in enumerate( self.mc, start = 1):
            self.mc[h].Sumw2()
            if count ==1:
                hTot = self.mc[h].Clone('hTot')
                print 'error with only 1 hist', hTot.GetBinError( hTot.GetMaximumBin() )

            clr = self.mc[h].GetLineColor()
            self.mc[h].SetFillColor(clr)
            
            hs.Add(self.mc[h])
#            entr = hTot.GetEntries()
            
            if count != 1:
                hTot.Add(self.mc[h])

            print 'iteration ', count, ' number of events in hTot is ',  hTot.GetEntries()

            

        print 'Before draw hTot has , iteration ', hTot.GetEntries()
        print 'error with all hist', hTot.GetBinError( hTot.GetMaximumBin() )
#        hTot.SetFillStyle(3001)
        #hTot.SetFillColorAlpha(10, 0.05) #very transparent
        print 'color of tot is ', hTot.GetFillColor()
 #       hTot.SetMarkerStyle(1)
  #      hTot.SetMarkerColor(0)


        hTot.SetFillColor(ROOT.kGray +3)
        hTot.SetMarkerSize(0)
        hTot.SetFillStyle(3013)
        #hTot.SetFillStyle(3001)

        c = ROOT.TCanvas("c","stacked hists",10,10,700,700)
        c.Divide(2,2)
        # in top left pad, draw the stack with defaults
        
        # for bin in xrange(1, hTot.GetXaxis().GetNbins() +1 ):
        #     nBins = hTot.GetXaxis().GetNbins()
        #     error = hTot.GetBinError(bin)
        #     binValue = hTot.GetBinContent(bin)
        #     print "nBins, bin, binValue, unc are ", nBins, bin, binValue, error
        #     hTot.SetBinContent(bin, error)

        c.cd(1)
        hs.Draw('e1')
        #in top right pad, draw the stack in non-stack mode
        #and errors option
        
        c.cd(2)
#        ROOT.gPad.SetGrid()
#        hs.Draw("nostack,e1p")
        hTot.Draw('e2')
#in bottom left, draw in stack mode with "lego1" option
        
        c.cd(3)
        # ROOT.gPad.SetFrameFillColor(17)
        # ROOT.gPad.SetTheta(3.77)
        # ROOT.gPad.SetPhi(2.9)
        # hs.Draw("lego1")
        hTot.Draw('e3')
    
        c.cd(4)
        #dummy, repeat

        hs.Draw('hist')
        hTot.Draw('e2 same')


        c.cd()
        c.Modified()
        c.Update()
    
        #save
        for ext in self.plotformats : c.SaveAs(os.path.join(outDir, self.name+'.'+ext))
        if self.savelog:
            p1.cd()
            p1.SetLogy()
            c.cd()
            c.Modified()
            c.Update()
            for ext in self.plotformats : c.SaveAs(os.path.join(outDir, self.name+'_log.'+ext))

        if saveTeX : self.convertToTeX(outDir=outDir)



    def doStackNoRatio(self, outDir,lumi,noScale=False,saveTeX=False):

        if len(self.mc)==0:
            print '%s has no MC!' % self.name
            return

        if self.mc.values()[0].InheritsFrom('TH2') :
            print 'Skipping TH2'
            return

        c = ROOT.TCanvas('c','c',500,500)
        c.SetBottomMargin(0.0)
        c.SetLeftMargin(0.0)
        c.SetTopMargin(0)
        c.SetRightMargin(0.00)

        #holds the main plot
        c.cd()
        p1 = ROOT.TPad('p1','p1',0.0,0.,1.0,0.99)
        p1.Draw()
        p1.SetRightMargin(0.1)
        p1.SetLeftMargin(0.2)
        p1.SetTopMargin(0.05)
#check
        p1.SetBottomMargin(0.15)   


        p1.SetGridx(True)
        self._garbageList.append(p1)
        p1.cd()

        # legend
#        leg = ROOT.TLegend(0.26, 0.87-0.02*max(len(self.mc)-2,0), 0.92, 0.94)        
        leg = ROOT.TLegend(0.25, 0.86, 0.88, 0.94)        
        leg.SetBorderSize(0)
        leg.SetFillStyle(0)
        leg.SetTextFont(43)
        leg.SetTextSize(12)
        nlegCols = 0

        if self.dataH is not None:
            if self.data is None: 
                self.finalize()
                leg.AddEntry( self.data, self.data.GetTitle(),'p')
                #leg.AddEntry( self.dataH, self.dataH.GetTitle(),'l')
            nlegCols += 1
        for h in self.mc:
            #if not noScale : self.mc[h].Scale(lumi)
            leg.AddEntry(self.mc[h], self.mc[h].GetTitle(), 'f')
            nlegCols += 1

        for hS in self.mcSignal:
            #if not noScale : self.msSignal[h].Scale(lumi)
            leg.AddEntry(self.mcSignal[hS], self.mcSignal[hS].GetTitle(), 'l')
            nlegCols += 1


        # Build the stack to plot from all backgrounds
        totalMC = None
        stack = ROOT.THStack('mc','mc')
        clr = None
        for h in self.mc:
            stack.Add(self.mc[h],'hist')
            try:
                clr = self.mc[h].GetLineColor()
                self.mc[h].SetFillColor(clr)
                self.mc[h].SetFillStyle(1001)
                totalMC.Add(self.mc[h])
            except:
                totalMC = self.mc[h].Clone('totalmc')
                self._garbageList.append(totalMC)
                totalMC.SetDirectory(0)


        if totalMC is not None:
            leg.AddEntry(totalMC, "Total stat unc", "f")
            nlegCols += 1
            
        if nlegCols ==0 :
            print '%s is empty'%self.name
            return
        leg.SetNColumns(2) #ROOT.TMath.Min(nlegCols/2,3))


        frame = totalMC.Clone('frame') if totalMC is not None else self.dataH.Clone('frame')

    
        frame.SetDirectory(0)
        frame.Reset('ICE')
        self._garbageList.append(frame)
        frame.GetYaxis().SetTitleSize(0.045)
        frame.GetYaxis().SetLabelSize(0.04)
        #frame.GetYaxis().SetNoExponent()
        frame.GetYaxis().SetTitleOffset(1.3)

        frame.GetXaxis().SetLabelSize(0.045)
        frame.GetXaxis().SetTitleSize(0.04)
        frame.GetXaxis().SetTitleOffset(1.2)
#        frame.GetYaxis().SetNdivisions(512)
        

        xName = frame.GetXaxis().GetTitle()
        yName = frame.GetYaxis().GetTitle()
#        frame.Draw('')  #check here


        if totalMC:
            maxY = totalMC.GetMaximum() 
            print 'maxY in totalMC is ', maxY
            if maxY < stack.GetMaximum():
                maxY = stack.GetMaximum()
                print 'maxY in stack is ', maxY
        if self.dataH:
            if maxY<self.dataH.GetMaximum():
                maxY=self.dataH.GetMaximum()
                print 'maxY in dataH is ', maxY
        
        print 'maxY is ', maxY
        
        # binmax = totalMC.GetMaximumBin()
        # lastBin = totalMC.FindLastBinAbove (binmax, 1)
        # x = totalMC.GetXaxis().GetBinCenter(lastBin)
        # xBins = totalMC.GetXaxis().GetNbins()
        # ROOT.gPad.DrawFrame(0.0, 0.1, x*1.1, maxY*1.3); 
        frame.GetYaxis().SetRangeUser(0.1,maxY*2.5)
        totalMC.GetYaxis().SetRangeUser(0.1,maxY*1.5)
        c.Modified()

        stack.Draw('hist')
  
        stack.GetYaxis().SetRangeUser(0.1,maxY*2)
        frame.GetYaxis().SetRangeUser(0.1,maxY*2.5)
        totalMC.GetYaxis().SetRangeUser(0.1,maxY*1.5)
        c.Modified()


        stack.GetXaxis().SetTitle(xName)
        stack.GetYaxis().SetTitle(yName)
        stack.GetYaxis().SetTitleOffset(1.4)
        stack.GetYaxis().SetTitleSize(0.045)
        stack.GetXaxis().SetLabelSize(0.045)
        stack.GetXaxis().SetTitleSize(0.04)
        stack.GetXaxis().SetTitleOffset(1.2)

       
        totalMC.SetFillColor(ROOT.kGray +3)
        totalMC.SetLineColor(ROOT.kGray)
        totalMC.SetMarkerSize(0)
        totalMC.SetFillStyle(3013)
           
        if totalMC is not None   :
            pass
            frame.Draw('hist same')  
            totalMC.Draw('e2 same') 

        #if self.data is not None : self.data.Draw('SAME PLC PMC') #('p')
        if self.dataH is not None : self.dataH.Draw('SAME PLC PMC') #('p')

        for hS in self.mcSignal:
            print 'name of hist to draw ', self.mcSignal[hS].GetName()
            #  try:
                #clr = self.mcSignal[hS].GetLineColor()
                #self.mcSignal[hS].SetFillColor(clr)
                #self.mcSignal[hS].SetFillStyle(1001)
            self.mcSignal[hS].Draw('SAME PLC PMC') #('p')
            #except:
                #pass


        stack.SetMaximum(maxY*1.3)
        c.Modified()

        leg.Draw()
        txt=ROOT.TLatex()
        txt.SetNDC(True)
        txt.SetTextFont(43)
        txt.SetTextSize(16)
        txt.SetTextAlign(12)
        if lumi<100:
            txt.DrawLatex(0.42,0.972,'#bf{CMS} #it{Preliminary} %3.1f pb^{-1} (13 TeV)' % (lumi) )
        else:
            txt.DrawLatex(0.42,0.972,'#bf{CMS} #it{Preliminary} %3.1f fb^{-1} (13 TeV)' % (lumi/1000.) )

        #all done
        c.cd()
        c.Modified()
        c.Update()

        #save
        for ext in self.plotformats : c.SaveAs(os.path.join(outDir, self.name+'.'+ext))
        if self.savelog:
            p1.cd()
            p1.SetLogy()
            c.cd()
            c.Modified()
            c.Update()
            for ext in self.plotformats : c.SaveAs(os.path.join(outDir, self.name+'_log.'+ext))

        if saveTeX : self.convertToTeX(outDir=outDir)




#////////////////////////


    def doStack(self, outDir,lumi,noScale=False,saveTeX=False, ratio=False, plotData = True):

        if len(self.mc)==0:
            print '%s has no MC!' % self.name
            return

        if self.mc.values()[0].InheritsFrom('TH2') :
            print 'Skipping TH2'
            return

        c = ROOT.TCanvas('c','c',500,500)
        c.SetBottomMargin(0.0)
        c.SetLeftMargin(0.0)
        c.SetTopMargin(0)
        c.SetRightMargin(0.00)

        #holds the main plot
        c.cd()
        p1 = ROOT.TPad('p1','p1',0.0,0.,1.0,0.99) if not ratio else ROOT.TPad('p1','p1',0.0,0.25,1.0,0.99)
        p1.Draw()
        p1.SetRightMargin(0.1 if not ratio else 0.05)
        p1.SetLeftMargin(0.2 if not ratio else 0.15)
        p1.SetTopMargin(0.05)
#check
        p1.SetBottomMargin(0.15) if not ratio else p1.SetBottomMargin(0.)   


        p1.SetGridx(True)
        self._garbageList.append(p1)
        p1.cd()

        # legend

#        leg = ROOT.TLegend(0.25, 0.86, 0.88, 0.94)  
        leg = ROOT.TLegend(0.3, 0.85-0.02*max(len(self.mc)-2,0), 0.92, 0.93)
      
        leg.SetBorderSize(0)
        leg.SetFillStyle(0)
        leg.SetTextFont(43)
        leg.SetTextSize(11)
        nlegCols = 0

        if self.dataH is not None:
            if self.data is None: 
                self.finalize()
                leg.AddEntry( self.data, self.data.GetTitle(),'p')
                #leg.AddEntry( self.dataH, self.dataH.GetTitle(),'l')
            nlegCols += 1
        for h in self.mc:
            #if not noScale : self.mc[h].Scale(lumi)
            leg.AddEntry(self.mc[h], self.mc[h].GetTitle(), 'f')
            nlegCols += 1

        for hS in self.mcSignal:
            #if not noScale : self.msSignal[h].Scale(lumi)
            leg.AddEntry(self.mcSignal[hS], self.mcSignal[hS].GetTitle(), 'l')
            nlegCols += 1


        # Build the stack to plot from all backgrounds
        totalMC = None
        stack = ROOT.THStack('mc','mc')
        clr = None
        for h in self.mc:
            stack.Add(self.mc[h],'hist')
            try:
                clr = self.mc[h].GetLineColor()
                self.mc[h].SetFillColor(clr)
                self.mc[h].SetFillStyle(1001)
                totalMC.Add(self.mc[h])
            except:
                totalMC = self.mc[h].Clone('totalmc')
                self._garbageList.append(totalMC)
                totalMC.SetDirectory(0)


        if totalMC is not None:
            leg.AddEntry(totalMC, "Total stat unc", "f")
            nlegCols += 1
            
        if nlegCols ==0 :
            print '%s is empty'%self.name
            return
        leg.SetNColumns(2) #ROOT.TMath.Min(nlegCols/2,3))


        frame = totalMC.Clone('frame') if totalMC is not None else self.dataH.Clone('frame')

    
        frame.SetDirectory(0)
        frame.Reset('ICE')
        self._garbageList.append(frame)
        frame.GetYaxis().SetTitleSize(0.045)
        frame.GetYaxis().SetLabelSize(0.04)
        #frame.GetYaxis().SetNoExponent()
        frame.GetYaxis().SetTitleOffset(1.3)

        frame.GetXaxis().SetLabelSize(0.045)
        frame.GetXaxis().SetTitleSize(0.04)
        frame.GetXaxis().SetTitleOffset(1.2)
#        frame.GetYaxis().SetNdivisions(512)
        

        xName = frame.GetXaxis().GetTitle()
        yName = frame.GetYaxis().GetTitle()
#        frame.Draw('')  #check here


        if totalMC:
            maxY = totalMC.GetMaximum() 
            print 'maxY in totalMC is ', maxY
            if maxY < stack.GetMaximum():
                maxY = stack.GetMaximum()
                print 'maxY in stack is ', maxY
        if self.dataH:
            if maxY<self.dataH.GetMaximum():
                maxY=self.dataH.GetMaximum()
                print 'maxY in dataH is ', maxY
        
        print 'maxY is ', maxY
        
        # binmax = totalMC.GetMaximumBin()
        # lastBin = totalMC.FindLastBinAbove (binmax, 1)
        # x = totalMC.GetXaxis().GetBinCenter(lastBin)
        # xBins = totalMC.GetXaxis().GetNbins()
        # ROOT.gPad.DrawFrame(0.0, 0.1, x*1.1, maxY*1.3); 
        frame.GetYaxis().SetRangeUser(0.1,maxY*2.5)
        totalMC.GetYaxis().SetRangeUser(0.1,maxY*1.5)
        c.Modified()

        stack.Draw('hist')
  
        stack.GetYaxis().SetRangeUser(0.1,maxY*2)
        frame.GetYaxis().SetRangeUser(0.1,maxY*2.5)
        totalMC.GetYaxis().SetRangeUser(0.1,maxY*1.5)
        c.Modified()


        stack.GetXaxis().SetTitle(xName)
        stack.GetYaxis().SetTitle(yName)
        stack.GetYaxis().SetTitleOffset(1.4)
        stack.GetYaxis().SetTitleSize(0.045)
        stack.GetXaxis().SetLabelSize(0.045)
        stack.GetXaxis().SetTitleSize(0.04)
        stack.GetXaxis().SetTitleOffset(1.2)

       
        totalMC.SetFillColor(ROOT.kGray +3)
        totalMC.SetLineColor(ROOT.kGray)
        totalMC.SetMarkerSize(0)
        totalMC.SetFillStyle(3013)
           
        if totalMC is not None   :
            pass
            frame.Draw('hist same')  
            totalMC.Draw('e2 same') 

        if self.data is not None : 
            if plotData:
                #'h' not in self.dataH.GetName():
                #print 'name is {} and type is {}'.format ( name, type(name) )
                self.data.Draw('p')#SAME PLC PMC') #('p')
        #if self.dataH is not None : self.dataH.Draw('SAME PLC PMC') #('p')

        for hS in self.mcSignal:
            print 'name of hist to draw ', self.mcSignal[hS].GetName()
            #  try:
                #clr = self.mcSignal[hS].GetLineColor()
                #self.mcSignal[hS].SetFillColor(clr)
                #self.mcSignal[hS].SetFillStyle(1001)
            self.mcSignal[hS].Draw('SAME PLC PMC') #('p')
            #except:
                #pass


        stack.SetMaximum(maxY*1.3)
        c.Modified()

        leg.Draw()
        txt=ROOT.TLatex()
        txt.SetNDC(True)
        txt.SetTextFont(43)
        txt.SetTextSize(16)
        txt.SetTextAlign(12)
        if lumi<100:
            txt.DrawLatex(0.42,0.972,'#bf{CMS} #it{Preliminary} %3.1f pb^{-1} (13 TeV)' % (lumi) )
        else:
            txt.DrawLatex(0.42,0.972,'#bf{CMS} #it{Preliminary} %3.1f fb^{-1} (13 TeV)' % (lumi/1000.) )


  #holds the ratio            
        print '='*50, 'before ratio'
        if ratio:
            print '+'*50, 'inside ratio'
            c.cd()
            p2 = ROOT.TPad('p2','p2',0.0,0.05,1.0,0.25)
            p2.Draw()
#check                                                                                           
            p2.SetBottomMargin(0.2)
            p2.SetRightMargin(0.05)
            p2.SetLeftMargin(0.15)
# check                                                                                          
            p2.SetTopMargin(0.00)
            p2.SetGridx(True)
            p2.SetGridy(True)
            self._garbageList.append(p2)
            p2.cd()
            ratioframe=frame.Clone('ratioframe')
            ratioframe.Reset('ICE')
            ratioframe.GetYaxis().SetTitle('Data/MC')
            ratioframe.GetYaxis().SetRangeUser(self.ratiorange[0], self.ratiorange[1])
            self._garbageList.append(frame) #?ratioframe                                             
            ratioframe.GetYaxis().SetNdivisions(5)
            ratioframe.GetYaxis().SetLabelSize(0.16)
            ratioframe.GetYaxis().SetTitleSize(0.16)
            ratioframe.GetYaxis().SetTitleOffset(.35) #0.25                                          
#check                                                                                           
            ratioframe.GetXaxis().SetLabelSize(0.16)
            ratioframe.GetXaxis().SetTitleSize(0.19)
            ratioframe.GetXaxis().SetTitleOffset(.9)
            #        ratioframe.GetXaxis().SetTitle(xName)                                                   
        #print 'name is ', xName                                                                 
            ratioframe.GetYaxis().CenterTitle()
            
            ratioframe.Draw()
            
        #x.SetTitle(self.mc[0].GetTitle())                                                       


            print '>'*50, 'before try'

            try:
                ratio=self.dataH.Clone('ratio')
                ratio.SetDirectory(0)
                self._garbageList.append(ratio)
                ratio.Divide(totalMC)
                gr=ROOT.TGraphAsymmErrors(ratio)
                # gr.SetMarkerStyle(self.data.GetMarkerStyle())
                # gr.SetMarkerSize(self.data.GetMarkerSize())
                # gr.SetMarkerColor(self.data.GetMarkerColor())
                # gr.SetLineColor(self.data.GetLineColor())
                # gr.SetLineWidth(self.data.GetLineWidth())
                gr.Draw('p')
            except:
                pass



        #all done
        c.cd()
        c.Modified()
        c.Update()

        #save
        for ext in self.plotformats : c.SaveAs(os.path.join(outDir, self.name+'.'+ext))
        if self.savelog:
            p1.cd()
            p1.SetLogy()
            c.cd()
            c.Modified()
            c.Update()
            for ext in self.plotformats : c.SaveAs(os.path.join(outDir, self.name+'_log.'+ext))

        if saveTeX : self.convertToTeX(outDir=outDir)





#///////////////////////


    def showStack(self, outDir,lumi,noScale=False,saveTeX=False):

        if len(self.mc)==0:
            print '%s has no MC!' % self.name
            return

        if self.mc.values()[0].InheritsFrom('TH2') :
            print 'Skipping TH2'
            return

        c = ROOT.TCanvas('c','c',500,500)
        c.SetBottomMargin(0.0)
        c.SetLeftMargin(0.0)
        c.SetTopMargin(0)
        c.SetRightMargin(0.00)

        #holds the main plot
        c.cd()
        p1 = ROOT.TPad('p1','p1',0.0,0.25,1.0,0.99)
        p1.Draw()
        p1.SetRightMargin(0.05)
        p1.SetLeftMargin(0.15)
        p1.SetTopMargin(0.05)
#check
        p1.SetBottomMargin(0.)   


        p1.SetGridx(True)
        self._garbageList.append(p1)
        p1.cd()

        # legend
        leg = ROOT.TLegend(0.42, 0.85-0.02*max(len(self.mc)-2,0), 0.98, 0.93)        
        #leg = ROOT.TLegend(0.2, 0.8-0.02*max(len(self.mc)-2,0), 0.9, 0.925)        
        leg.SetBorderSize(0)
        leg.SetFillStyle(0)
        leg.SetTextFont(43)
        leg.SetTextSize(13)
        nlegCols = 0

        if self.dataH is not None:
            if self.data is None: self.finalize()
            leg.AddEntry( self.data, self.data.GetTitle(),'p')
            nlegCols += 1
        for h in self.mc:
            #if not noScale : self.mc[h].Scale(lumi)
            leg.AddEntry(self.mc[h], self.mc[h].GetTitle(), 'f')
            nlegCols += 1
        for hS in self.mcSignal:
            #if not noScale : self.mc[h].Scale(lumi)                                                                                 
            leg.AddEntry(self.mcSignal[hS], self.mcSignal[hS].GetTitle(), 'l')
            nlegCols += 1

        if nlegCols ==0 :
            print '%s is empty'%self.name
            return
        leg.SetNColumns(ROOT.TMath.Min(nlegCols/2,3))

        # Build the stack to plot from all backgrounds
        totalMC = None
        stack = ROOT.THStack('mc','mc')
        clr = None
        for h in self.mc:
            stack.Add(self.mc[h],'hist')
            try:
                clr = self.mc[h].GetLineColor()
                self.mc[h].SetFillColor(clr)
                self.mc[h].SetFillStyle(1001)
                totalMC.Add(self.mc[h])
            except:
                totalMC = self.mc[h].Clone('totalmc')
                self._garbageList.append(totalMC)
                totalMC.SetDirectory(0)

        # for h in self.mcSignal:
        #     stack.Add(self.mcSignal[h],'hist')
        #     try:
        #         clr = self.mcSignal[h].GetLineColor()
        #         self.mcSignal[h].SetFillColor(clr)
        #         self.mcSignal[h].SetFillStyle(1001)
        #         totalMC.Add(self.mcSignal[h])
        #     except:
        #         totalMC = self.mcSignal[h].Clone('totalmc')
        #         self._garbageList.append(totalMC)
        #         totalMC.SetDirectory(0)

     

        frame = totalMC.Clone('frame') if totalMC is not None else self.dataH.Clone('frame')
        frame.Reset('ICE')
        if totalMC:
            maxY = totalMC.GetMaximum() 
        if self.dataH:
            if maxY<self.dataH.GetMaximum():
                maxY=self.dataH.GetMaximum()
        frame.GetYaxis().SetRangeUser(0.1,maxY*1.3)
        frame.SetDirectory(0)
        frame.Reset('ICE')
        self._garbageList.append(frame)
        frame.GetYaxis().SetTitleSize(0.045)
        frame.GetYaxis().SetLabelSize(0.04)
        #frame.GetYaxis().SetNoExponent()
        frame.GetYaxis().SetTitleOffset(1.3)

        frame.GetXaxis().SetLabelSize(0.)
        frame.GetXaxis().SetTitleSize(0.)
        frame.GetXaxis().SetTitleOffset(0.)

        xName = frame.GetXaxis().GetTitle()
        frame.Draw()
        

        if totalMC is not None   : stack.Draw('hist same')
        if self.data is not None : self.data.Draw('p')
        
        for count, h in enumerate(self.mcSignal, start=0):
            bazinga ('about to draw MC')
            #self.mcSignal[h].Print('all')                                                                                                 
            if count == 0:
                # print 'hist {} contains {} entries'.format( self.mcSignal[h].GetName(),     self.mcSignal[h].GetEntries() )                    
                # print 'hist sum of W is {}, and integral is {}'.format( self.mcSignal[h].GetSumOfWeights(),     self.mcSignal[h].Integral() )  
                # print 'count is ', count                                                                                           

                #c.cd()                                                                                                              
                self.mcSignal[h].Draw('hist same')
                #c.Modified()                                                                                                        
                #c.Update()                                                                                                          
            else:

                print 'count is ', count
                self.mcSignal[h].Draw("same hist") #("same L")                                                                             
                print 'hist sum of W is {}, and integral is {}'.format( self.mcSignal[h].GetSumOfWeights(),     self.mcSignal[h].Integral() )
                #print 'hist {} contains {} entries'.format( self.mcSignal[h].GetName(),     self.mcSignal[h].GetEntries() )                     

        bazinga ('after the call to draw MC')

     
        leg.Draw()
        txt=ROOT.TLatex()
        txt.SetNDC(True)
        txt.SetTextFont(43)
        txt.SetTextSize(16)
        txt.SetTextAlign(12)
        if lumi<100:
            txt.DrawLatex(0.47,0.972,'#bf{CMS} #it{Preliminary} %3.1f pb^{-1} (13 TeV)' % (lumi) )
        else:
            txt.DrawLatex(0.47,0.972,'#bf{CMS} #it{Preliminary} %3.1f fb^{-1} (13 TeV)' % (lumi/1000.) )

        #holds the ratio
        c.cd()
        p2 = ROOT.TPad('p2','p2',0.0,0.05,1.0,0.25)
        p2.Draw()
#check
        p2.SetBottomMargin(0.2)
        p2.SetRightMargin(0.05)
        p2.SetLeftMargin(0.15)
# check
        p2.SetTopMargin(0.00)
        p2.SetGridx(True)
        p2.SetGridy(True)
        self._garbageList.append(p2)
        p2.cd()
        ratioframe=frame.Clone('ratioframe')
        ratioframe.GetYaxis().SetTitle('Data/MC')
        ratioframe.GetYaxis().SetRangeUser(self.ratiorange[0], self.ratiorange[1])
        self._garbageList.append(frame) #?ratioframe
        ratioframe.GetYaxis().SetNdivisions(5)
        ratioframe.GetYaxis().SetLabelSize(0.16)        
        ratioframe.GetYaxis().SetTitleSize(0.16)
        ratioframe.GetYaxis().SetTitleOffset(1.3) #0.25
#check
        ratioframe.GetXaxis().SetLabelSize(0.16)
        ratioframe.GetXaxis().SetTitleSize(0.19)
        ratioframe.GetXaxis().SetTitleOffset(.9)
#        ratioframe.GetXaxis().SetTitle(xName)
        #print 'name is ', xName
        ratioframe.GetYaxis().CenterTitle()

        ratioframe.Draw()
        
        #x.SetTitle(self.mc[0].GetTitle())
        


        try:
            ratio=self.dataH.Clone('ratio')
            ratio.SetDirectory(0)
            self._garbageList.append(ratio)
            ratio.Divide(totalMC)
            gr=ROOT.TGraphAsymmErrors(ratio)
            gr.SetMarkerStyle(self.data.GetMarkerStyle())
            gr.SetMarkerSize(self.data.GetMarkerSize())
            gr.SetMarkerColor(self.data.GetMarkerColor())
            gr.SetLineColor(self.data.GetLineColor())
            gr.SetLineWidth(self.data.GetLineWidth())
            gr.Draw('p')
        except:
            pass

        #all done
        c.cd()
        c.Modified()
        c.Update()

        #save
        for ext in self.plotformats : c.SaveAs(os.path.join(outDir, self.name+'.'+ext))
        if self.savelog:
            p1.cd()
            p1.SetLogy()
            c.cd()
            c.Modified()
            c.Update()
            for ext in self.plotformats : c.SaveAs(os.path.join(outDir, self.name+'_log.'+ext))

        if saveTeX : self.convertToTeX(outDir=outDir)


#//////////////////////////
    def makeDataCards(self, outDir,lumi,noScale=False,saveTeX=False):
        dataDict = {}
        dataDict[self.dataH.GetName()] = self.dataH
        ndic = dict(self.mc.items() + self.mcSignal.items() + dataDict.items())
        dicRates = collections.defaultdict(str)
#        dataCardHistList = []
        processName = 'hh'
        signalMultFactor = 2000.
        processRateStr = ''
        for h in ndic:
            print 'type(h) is ', ndic[h]
            nameEnding_beg = ndic[h].GetName().find('_',5)
            print 'hist {0} has integral={1}'.format( ndic[h].GetName(), ndic[h].Integral() )
            if 'sig' in ndic[h].GetName():
                ndic[h].Scale(1./2000)
            tmpRate = ndic[h].Integral()

            if 'ZH' in ndic[h].GetName()[nameEnding_beg+1:]:
                dicRates[ndic[h].GetName()[nameEnding_beg+1:]] = [5, round(tmpRate, 2),ndic[h]]
            elif 'VV' in ndic[h].GetName()[nameEnding_beg+1:]:
                dicRates[ndic[h].GetName()[nameEnding_beg+1:]] = [4, round(tmpRate, 2),ndic[h]]
            elif 'ST' in ndic[h].GetName()[nameEnding_beg+1:]:
                dicRates[ndic[h].GetName()[nameEnding_beg+1:]] = [3, round(tmpRate, 2),ndic[h]]
            elif 'DY' in ndic[h].GetName()[nameEnding_beg+1:]:
                dicRates[ndic[h].GetName()[nameEnding_beg+1:]] = [2, round(tmpRate, 2),ndic[h]]
            elif 'TT' in ndic[h].GetName()[nameEnding_beg+1:]:
                dicRates[ndic[h].GetName()[nameEnding_beg+1:]] = [1, round(tmpRate, 2),ndic[h]]
            elif 'signal_ww' in ndic[h].GetName()[nameEnding_beg+1:]:
                dicRates[ndic[h].GetName()[nameEnding_beg+1:]] = [0, round(tmpRate, 2),ndic[h]]
            elif 'signal_zz' in ndic[h].GetName()[nameEnding_beg+1:]:
                dicRates[ndic[h].GetName()[nameEnding_beg+1:]] = [-1, round(tmpRate, 2),ndic[h]]
            elif 'data_obs' in ndic[h].GetName()[nameEnding_beg+1:]:
                dicRates[ndic[h].GetName()[nameEnding_beg+1:]] = [-10, round(tmpRate, 2),ndic[h]]
            else:
                print 'smth went wrong with dataCard'
                sys.exit(1)

        ordDict = collections.OrderedDict(sorted(dicRates.items(), key=operator.itemgetter(1)) )
        print 'ordDicts contains:'
        for key,value in ordDict.items():
            print(key, ":", value)
            print 'type(key) is ', type(value[2]) 
#        print 'ordDict is ', ordDict
#        for i in dicRates.items():
 #           print i
        curDir = os.getcwd()
        if os.path.exists(outDir):
            os.chdir(outDir)
        outF = ROOT.TFile.Open(processName + '.root','recreate')

        processNameStr = ''
        for h in ordDict:
            #listValues = ordDict[h]
            if 'data' not in h:
                processNameStr += '  {}  '.format(h)
            (ordDict[h])[2].Write(h, ROOT.TObject.kOverwrite)
        outF.Close()
        print 'processNameStr is ', processNameStr
      #   with io.open (processName + '_dataCard.txt', mode = 'wb') as fOut:
#             fOut.write('#  DataCard for DY CR\n')
#             fOut.write('#  Consider for now only 300GeV signal mass point\n')
#             fOut.write('#  "hhMt_long" variable\n')
#             fOut.write('#  First draft of the HHtobbZZto2b2l2nu datacard\n')
#             fOut.write('#-----------------------------------------------------------------------------------')
#             fOut.write('imax 1 number of channels, switck to two when add EGamma data?\n
# jmax 6 number of mc samples minus one\n
# kmax * number of nuisance parameters (sources of systematical uncertainties)\n')
#             fOut.write('#-----------------------------------------------------------------------------------')
#             fOut.write('#syntax:\n')
#             fOut.write('# shapes  _process_  _channel_   _file_    _histogram-name_      _histogram-name-for-systematics_\n')
#             fOut.write('\n')
#             fOut.write('#shapes * * hh_mt.input_13TeV.root $CHANNEL/$PROCESS $CHANNEL/$PROCESS_$SYSTEMATIC\n')
#             fOut.write('shapes * * hh_mt.input_13TeV.root $PROCESS $PROCESS_$SYSTEMATIC\n')
#             fOut.write('#-----------------------------------------------------------------------------------')
#             fOut.write('# so far we have just one channel, in which we observe N events in data (yield, or Integral() \n')
#             fOut.write('bin hh\n')
#             fOut.write('observation {0} {1}\n'.format(ndic['data_obs'], str("#hhMt_long->Integral() of ~/workspace/private/feb22HH/CMSSW_8_0_25/src/VHbbAnalysis/Heppy/test/analysis_apr01_tot_hzz_CRDY_v5$ root -l muon2016data.root")))
#             fOut.write('#-----------------------------------------------------------------------------------')
#             binStr = '  hh  '*7  
#             fOut.write('bin          {0}\n'.format(binStr))
#             fOut.write('process      {0}\n'.format(processNameStr))
#             fOut.write('process      {0}\n'.format(processRateStr))
#             fOut.write('#  \n')
#             fOut.write('#  \n')


        os.chdir(curDir)



#===========================
    def overlayHists(self, outDir,lumi,noScale=False,saveTeX=False, plotData = False ):
        print 'in overlayHists'
        if len(self.mc)==0:
            print '%s has no MC!' % self.name
            #return

        if self.mc:
            if self.mc.values()[0].InheritsFrom('TH2') :
                print 'Skipping TH2'
                return
        bazinga ('create canvas')
        c = ROOT.TCanvas('c','c',500,500)
        # c.SetBottomMargin(0.0)
        # c.SetLeftMargin(0.0)
        # c.SetTopMargin(0)
        # c.SetRightMargin(0.00)

        #holds the main plot
        c.cd()
        
        #p1 = ROOT.TPad('p1','p1',0.0,0.85,1.0,0.0)
        #p1.Draw()
        # p1.SetRightMargin(0.05)
        # p1.SetLeftMargin(0.12)
        # p1.SetTopMargin(0.01)
        # p1.SetBottomMargin(0.12)
        # p1.SetGridx(True)
        # self._garbageList.append(p1)
        # p1.cd()

        c.SetRightMargin(0.05)
        c.SetLeftMargin(0.12)
        c.SetTopMargin(0.01)
        c.SetBottomMargin(0.12)
        c.SetGridx(True)
#        self._garbageList.append(p1)
 #       p1.cd()

        # legend
        bazinga ('create legend')
        leg = ROOT.TLegend(0.2, 0.8, 0.95, 0.98) #-0.02*max(len(self.mc)-2,0), 0.95, 0.95)        
        leg.SetBorderSize(0)
        leg.SetFillStyle(0)
        leg.SetTextFont(43)
        leg.SetTextSize(10)
        nlegCols = 0

        norm = 1.0
        # fix me regarding dataH when will be using data
        if self.dataH is not None:
            bazinga ('in if dataH')
            if self.data is None: pass #self.finalize()
            name = self.dataH.GetName()
            print 'name is {} and type is {}'.format ( name, type(name) )
            if 'cutFlow' not in name: 
                if self.dataH.GetSumOfWeights() != 0:
                    self.dataH.Scale(norm/self.dataH.GetSumOfWeights(), "")
            else: 
                print 'cutFlow* hist, skipping...'
                
#            leg.AddEntry( self.data, self.data.GetTitle(),'p')
            if plotData:
                leg.AddEntry( self.dataH, self.dataH.GetTitle(),'lp')
            nlegCols += 1
        
        for h in self.mc:
            bazinga ('in for loop over h')
            #should this line be used?
            #if not noScale : self.mc[h].Scale(lumi)
            name = self.mc[h].GetName()
            print '\nname is {} and type is {}'.format ( name, type(name) )
            if 'cutFlow' not in name:
                print 'this is not a cutFlow, can normalize'
                if self.mc[h].GetSumOfWeights() != 0:
                    self.mc[h].Scale(norm/self.mc[h].GetSumOfWeights(), "") #"width") 
            else: 
                print 'cutFlow* hist, skipping...'
                print 'name is {}'.format(self.mc[h].GetName())
                #firstBin = self.mc[h]..GetBinContent(1)
                #if firstBin > 100:
                    #self.mc[h].Scale(firstBin/100.)
            leg.AddEntry(self.mc[h], self.mc[h].GetTitle(), 'lp') #f
            nlegCols += 1

        for h in self.mcSignal:
            name = self.mcSignal[h].GetName()
            if 'cutFlow' not in name:
                if self.mcSignal[h].GetSumOfWeights() != 0:
                    self.mcSignal[h].Scale(norm/self.mcSignal[h].GetSumOfWeights(), "")
            else:
                print 'cutFlow* hist, skipping...'
                print 'name is {}'.format(self.mcSignal[h].GetName())
            leg.AddEntry(self.mcSignal[h], self.mcSignal[h].GetTitle(), 'lp') #f                                       
            nlegCols += 1

        if nlegCols ==0 :
            print '%s is empty'%self.name
            return
        leg.SetNColumns(3)#ROOT.TMath.Min(nlegCols/2,3))

        
        # Build the stack to plot from all backgrounds
        #bgHists = None
        # fix me regarding dataH when will be using data
        maxY = 0
        if self.dataH:
            maxY=self.dataH.GetMaximum()
            bazinga ('set maxY for dataH')

        for h in self.mc:
            if maxY<self.mc[h].GetMaximum():
                maxY=self.mc[h].GetMaximum()
                bazinga ('maxY in MC regime')
                print 'maxY is ', maxY

 
        for h in self.mcSignal:
            if maxY<self.mcSignal[h].GetMaximum():
                maxY=self.mcSignal[h].GetMaximum()
                bazinga ('maxY in MC Signal regime')
                print 'maxY is ', maxY



        bazinga ('about to draw data')
        if self.dataH and 'cutFlow' not in self.dataH.GetName(): 
            if plotData:
                self.dataH.Draw('hist') #self.dataH.Draw()
            
        #c, pad1, pad2 = createCanvasPads()
        #pad1.cd()
    
        #self.mc[0].Draw('hist')
        for count, h in enumerate(self.mc, start=0):
            bazinga ('about to draw MC')
            #self.mc[h].Print('all')
            if count == 0:
                # print 'hist {} contains {} entries'.format( self.mc[h].GetName(),     self.mc[h].GetEntries() )
                # print 'hist sum of W is {}, and integral is {}'.format( self.mc[h].GetSumOfWeights(),     self.mc[h].Integral() )
                # print 'count is ', count
                
                #c.cd()
                self.mc[h].Draw('hist same')
                #c.Modified()
                #c.Update()
            else:
                
                print 'count is ', count

                self.mc[h].Draw("same hist") #("same L") 
                print 'hist sum of W is {}, and integral is {}'.format( self.mc[h].GetSumOfWeights(),     self.mc[h].Integral() )
                #print 'hist {} contains {} entries'.format( self.mcSignal[h].GetName(),     self.mcSignal[h].GetEntries() )

            bazinga ('after the call to draw MC')
        
        for count, h in enumerate(self.mcSignal, start=0):
            bazinga ('about to draw MC')
            #self.mcSignal[h].Print('all')                                                                                            
            #styleList = [1,2,9]*4
            styleList = [2,2,2]*4
            widthList = [2,2,3]*4
            self.mcSignal[h].SetLineStyle(styleList[count])    
            self.mcSignal[h].SetLineWidth(widthList[count])
            if count == 0:
                # print 'hist {} contains {} entries'.format( self.mcSignal[h].GetName(),     self.mcSignal[h].GetEntries() )       
                # print 'hist sum of W is {}, and integral is {}'.format( self.mcSignal[h].GetSumOfWeights(),     self.mcSignal[h].\Integral() )                                                                                                            
                # print 'count is ', count                                                                              

                #c.cd()                                                                                                 



                self.mcSignal[h].Draw('hist same')
                #c.Modified()                                                                                           
                #c.Update()                                                                                             
            else:

                print 'count is ', count
                self.mcSignal[h].Draw("same hist") #("same L")                                                                
                print 'hist sum of W is {}, and integral is {}'.format( self.mcSignal[h].GetSumOfWeights(),     self.mcSignal[h].Integral() )
                #print 'hist {} contains {} entries'.format( self.mcSignal[h].GetName(),     self.mcSignal[h].GetEntries() )        

            bazinga ('after the call to draw MC')



        bazinga ('prettify dataH')
        if self.dataH:
            self.dataH.GetYaxis().SetRangeUser(0.1,maxY*1.3)
        #?
            self.dataH.SetDirectory(0)
            #? self.dataH.Reset('ICE')
        #?
        #self._garbageList.append(self.dataH)
            self.dataH.GetYaxis().SetTitleSize(0.045)
            self.dataH.GetYaxis().SetLabelSize(0.04)
            self.dataH.GetYaxis().SetNoExponent()
        #self.dataH.Draw()
            self.dataH.GetYaxis().SetTitleOffset(1.3)
        bazinga ('prettify mc[h]')
        if len(self.mc) != 0:
            for count, h in enumerate(self.mc, start=1):   # default is zero
                self.mc[h].SetDirectory(0)
                while count < 2:
                    self.mc[h].GetYaxis().SetRangeUser(0.,maxY*1.3)
                    bazinga ('inside while')
                    # self.mc[h].Reset('ICE')
                    # be VERY careful with option RESET!
                    #
                    self.mc[h].GetYaxis().SetTitleSize(0.045)
                    self.mc[h].GetYaxis().SetLabelSize(0.04)
                    self.mc[h].GetYaxis().SetNoExponent()
                    self.mc[h].GetYaxis().SetTitleOffset(1.3)
                    count +=1 # otherwise inf while loop
        # #self._garbageList.append(self.mc[h])            
        
        #if totalMC is not None   : stack.Draw('hist same')
        #if self.data is not None : self.data.Draw('p')
        bazinga ('draw leg')
        leg.Draw()
        txt=ROOT.TLatex()
        txt.SetNDC(True)
        txt.SetTextFont(43)
        txt.SetTextSize(16)
        txt.SetTextAlign(12)

            
        bazinga ('cd to canvas')
        #all done
        c.cd()
        c.Modified()
        c.Update()
        bazinga ('just updated the canvas')
        ROOT.gROOT.GetListOfCanvases().Draw()
    
        #save
        for ext in self.plotformats : c.SaveAs(os.path.join(outDir, self.name+'.'+ext))
        # if self.savelog:
        #     p1.cd()
        #     p1.SetLogy()
        #     c.cd()
        #     c.Modified()
        #     c.Update()
        #     for ext in self.plotformats : c.SaveAs(os.path.join(outDir, self.name+'_log.'+ext))
        bazinga ('just saved the plots')
        if saveTeX : self.convertToTeX(outDir=outDir)
        bazinga ('all done with fcn overlayHists')


    def convertToTeX(self, outDir):
        if len(self.mc)==0:
            print '%s is empty' % self.name
            return

        f = open(outDir+'/'+self.name+'.dat','w')
        f.write('------------------------------------------\n')
        f.write("Process".ljust(20),)
        f.write("Events after each cut\n")
        f.write('------------------------------------------\n')

        tot ={}
        err = {}
        f.write(' '.ljust(20),)
        try:
            for xbin in xrange(1,self.mc.values()[0].GetXaxis().GetNbins()+1):
                pcut=self.mc.values()[0].GetXaxis().GetBinLabel(xbin)
                f.write(pcut.ljust(40),)
                tot[xbin]=0
                err[xbin]=0
        except:
            pass
        f.write('\n')
        f.write('------------------------------------------\n')

        for pname in self.mc:
            h = self.mc[pname]
            f.write(pname.ljust(20),)

            for xbin in xrange(1,h.GetXaxis().GetNbins()+1):
                itot=h.GetBinContent(xbin)
                ierr=h.GetBinError(xbin)
                pval=' & %3.1f $\\pm$ %3.1f' % (itot,ierr)
                f.write(pval.ljust(40),)
                tot[xbin] = tot[xbin]+itot
                err[xbin] = err[xbin]+ierr*ierr
            f.write('\n')

        f.write('------------------------------------------\n')
        f.write('Total'.ljust(20),)
        for xbin in tot:
            pval=' & %3.1f $\\pm$ %3.1f' % (tot[xbin],math.sqrt(err[xbin]))
            f.write(pval.ljust(40),)
        f.write('\n')

        if self.dataH is None: return
        f.write('------------------------------------------\n')
        f.write('Data'.ljust(20),)
        for xbin in xrange(1,self.dataH.GetXaxis().GetNbins()+1):
            itot=self.dataH.GetBinContent(xbin)
            pval=' & %d'%itot
            f.write(pval.ljust(40))
        f.write('\n')
        f.write('------------------------------------------\n')
        f.close()



"""
converts a histogram to a graph with Poisson error bars
"""
def convertToPoissonErrorGr(h):

    htype=h.ClassName()
    if htype.find('TH1')<0 : return None
    bazinga ('in the convert fcn')
    #check https://twiki.cern.ch/twiki/bin/view/CMS/PoissonErrorBars
    alpha = 1 - 0.6827;
    grpois = ROOT.TGraphAsymmErrors(h);
    for i in xrange(0,grpois.GetN()+1) :
        N = grpois.GetY()[i]
        if N<200 :
            L = 0
            if N>0 : L = ROOT.Math.gamma_quantile(alpha/2,N,1.)
            U = ROOT.Math.gamma_quantile_c(alpha/2,N+1,1)
            grpois.SetPointEYlow(i, N-L)
            grpois.SetPointEYhigh(i, U-N)
        else:
            grpois.SetPointEYlow(i, math.sqrt(N))
            grpois.SetPointEYhigh(i,math.sqrt(N))
    return grpois


"""
steer the script
"""
def main():

    #configuration
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option('-j', '--json',        dest='json'  ,      help='json with list of files',        default=None,    type='string')
    parser.add_option('-i', '--inDir',       dest='inDir' ,      help='input directory',                default=None,    type='string')
    parser.add_option(      '--saveLog',     dest='saveLog' ,    help='save log versions of the plots', default=False,   action='store_true')
    parser.add_option(      '--silent',      dest='silent' ,     help='only dump to ROOT file',         default=False,   action='store_true')
    parser.add_option(      '--saveTeX',     dest='saveTeX' ,    help='save as tex file as well',       default=False,   action='store_true')
    parser.add_option(      '--rebin',       dest='rebin',       help='rebin factor',                   default=1,       type=int)
    parser.add_option('-l', '--lumi',        dest='lumi' ,       help='lumi to print out',              default=36300,    type=float)
    parser.add_option(      '--only',        dest='only',        help='plot only these (csv)',          default='',      type='string')
    parser.add_option('-k', '--kind',        dest='kind'  ,      help='kind of plot: "Stack" or "OverlayHists"',default=None,   type='string')
    parser.add_option('-r', '--region',      dest='region',      help='SR(no Data for Higgs lots) or CR with data',default=None,   type='string')

    (opt, args) = parser.parse_args()

    #read list of samples
    jsonFile = open(opt.json,'r')
    samplesList=json.load(jsonFile,encoding='utf-8').items()
    jsonFile.close()

    onlyList=opt.only.split(',')

  
    
    #read plots 
    plots={}
    for tag,sample in samplesList: 
        fIn=ROOT.TFile.Open('%s/%s.root' % ( opt.inDir, tag) )
        print 'opening %s/%s.root' % ( opt.inDir, tag)
        try:
            for tkey in fIn.GetListOfKeys():
                key=tkey.GetName()
                if 'makeDataCards' in opt.kind:
                    if 'hhMt_long' in key: 
                        #print 'key is ', key
                        if 'before' in key: 
                            continue
                    else:
                        continue

                keep=False
                for tag in onlyList: 
                    if tag in key: keep=True
                if not keep: continue
                obj=fIn.Get(key)
                if not obj.InheritsFrom('TH1') : continue
                if not key in plots : 
                    #print 'processing ', fIn
                    plots[key]=Plot(key)
                if opt.rebin>1:  obj.Rebin(opt.rebin)
    #            plots[key].add(h=obj,title=sample[3],color=sample[4],isData=sample[1])
                plots[key].add(h=obj,title=sample[3],color=sample[4],isData=sample[1], isSignal=sample[6])
        except:
            print 'Skipping %s'%tag

    #show plots
    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gROOT.SetBatch(True)
    outDir=opt.inDir+'/plots/' + str(opt.kind)
    os.system('mkdir -p %s' % outDir)
  
    dataOrNot = True if opt.region == 'CR' else False
    
    for p in plots : 
        if opt.saveLog    : plots[p].savelog=True
        #print 'p is ', p
        #print 'type of p is ', type(p)
        #print 'p name is ', plots[p].name
        plotName = plots[p].name
        if not opt.silent :
            
            if 'Stack' in opt.kind and 'cutFlow' not in plotName:# == 'Stack' or 'StackNoRatio':
#                if 'h' in plotName:
 #                   plots[p].doStack(outDir=outDir,lumi=opt.lumi,saveTeX=opt.saveTeX, ratio = dataOrNot, plotData = dataOrNot)
  #              else:
                print 'will do "Stack"'
                plots[p].doStack(outDir=outDir,lumi=opt.lumi,saveTeX=opt.saveTeX, ratio=dataOrNot, plotData = dataOrNot)
            
            elif 'Stack' in opt.kind and 'cutFlow' in plotName:
                print 'will do "OverlayHists" because it is cutFlow!'
                plots[p].overlayHists(outDir=outDir,lumi=opt.lumi,saveTeX=opt.saveTeX, plotData = dataOrNot)

            elif 'OverlayHists' in opt.kind:# == 'OverlayHists':

                #if 'cutFlow' in plotName:
                print 'will do "OverlayHists"'
                plots[p].overlayHists(outDir=outDir,lumi=opt.lumi,saveTeX=opt.saveTeX, plotData = dataOrNot)
            elif 'makeDataCards' in opt.kind:

                    print 'will do "makeDataCards"'
                    plots[p].makeDataCards(outDir=outDir,lumi=opt.lumi,saveTeX=opt.saveTeX)            
            else:
                print "\nwrong kind of plot is specified, please use '-k Stack', '-k StackNoRatio' or '-k OverlayHists' or '-r makeDataCards'"
                sys.exit(1) # vs exit(1)

        bazinga ('after call to overlayHists')
        plots[p].appendTo(outDir+'/plotter.root')
        bazinga ('after call to appendTo')
        #print 'the type of plots[p] is ', type(plots[p])
        #uncomment it when run for stack, fix me
        plots[p].reset()
        bazinga ('after call to reset')

    print '-'*50
    print 'Plots and summary ROOT file can be found in %s' % outDir
    print '-'*50

        
"""
for execution from another script
"""
if __name__ == "__main__":
    sys.exit(main())

