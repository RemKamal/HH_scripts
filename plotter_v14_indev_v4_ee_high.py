#!/usr/bin/env python
import pandas as pd
import optparse
import os,sys
import json
import ROOT
import math
import collections, operator
import io
import pprint
pp = pprint.PrettyPrinter(indent=4)
import time

debugMode = True
def bazinga (mes):
    if debugMode:
        print mes



def determMultiples (number):
    number = int(round(number, 0))
    mil, rest = divmod (number, 1000000)
    thous, leftov = divmod (rest, 1000)
    hund, rest = divmod (leftov, 100)
    #print '{0}M {1}k {2}h {3}'.format(mil, thous, hund, rest)
    if mil ==0:
        if thous ==0:
            if hund == 0:
                return '{0}'.format(rest)
            else:
                return '{0}{1}'.format(hund, str(rest))
        else:
            return '{0}.{1}k'.format(thous, str(hund)[0])
    else:
        return '{0}.{1}M'.format(mil, str(thous)[0])



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
        self.plotformats = ['pdf', 'png', 'root']
        self.savelog = False
        self.ratiorange = (0.46,1.54)

    def add(self, h, title, color, isData, isSignal):
        h.SetTitle(title)
        if len(self.name)>5 and not title.startswith('Data'):
            extension = self.name[4:] 
            print 'extension={0}, self.name={1}'.format(extension, self.name)
        else:
            extension = ''

        sampleType = None
        #print '8'*100
        #print 'sampleType is', sampleType
        
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
        elif 'ZZ' in title:
            sampleType = 'signal_hzz'
        elif 'zz' in title:
            sampleType = 'signal_zz'
        elif 'WW' in title:
             sampleType = 'signal_hww'
        elif 'VV' in title:
             sampleType = 'signal_vv'
        else:
            print 'something is wrong with ', title
            sys.exit(1)
        #if sampleType.startswith('sig'):
         #   print 'title is ', title
          #  print 'sampleType is ', sampleType

        #sampleType += extension


        # if len(self.name>5) and sampleType != 'data_obs':
        #     print 'sampleType before', sampleType
        #     sampleType += self.name[5:]
        #     print 'sampleType after', sampleType


     
        if isData:
            try:
                self.dataH.Add(h)
            except:
                self.dataH=h
                self.dataH.SetName(sampleType)#'%s_%s' % (self.dataH.GetName(), sampleType ) )
                print 'self.dataH.GetName() is ', self.dataH.GetName()
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
                self.mc[title].SetName(sampleType)#'%s_%s' % (self.mc[title].GetName(), sampleType ) )
                print 'self.mc[title].GetName is ', self.mc[title].GetName()
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
                self.mcSignal[title].SetName(sampleType)#'%s_%s' % (self.mcSignal[title].GetName(), sampleType ) )
                print 'self.mcSignal[title].GetName is ', self.mcSignal[title].GetName()
                self.mcSignal[title].SetDirectory(0)
                self.mcSignal[title].SetMarkerStyle(1) #20
 #               self.mcSignal[title].SetMarkerSize(0.9)
                self.mcSignal[title].SetMarkerColor(color)
                self.mcSignal[title].SetLineColor(color)
                self.mcSignal[title].SetLineWidth(2)
                #self.mcSignal[title].SetLineStyle(7)

                self.mcSignal[title].SetFillColor(0)
                #uncomment for overlay hists
                #self.mcSignal[title].SetFillStyle(0)
                self._garbageList.append(h)
        else:
            print "problem appearred, exiting..."
            exit(1)



    def finalize(self):
        self.data = convertToPoissonErrorGr(self.dataH)

    def unblindAllowed (self, bdtCut, hist = None):
        print 'in unblindAllowed'
        
        if hist:
            print 'hist.GetName() is ', hist.GetName()
            hist_to_use = hist
        else:
            hist_to_use = self.dataH
            
        bdtBin = hist_to_use.GetXaxis().FindBin(bdtCut)# if 'bdt' in hist_to_use.GetName() else None                                 
        retHist = ROOT.TH1F('bdt_response_allowed', ';BDT response; Events', bdtBin, -1., bdtCut)

        retHist.SetName('data_obs')
        print 'retHist.GetName() is ', retHist.GetName()
        retHist.SetDirectory(0)
        retHist.SetMarkerStyle(20) 
 #               retHist.SetMarkerSize(0.9)                                                                                                  
        retHist.SetMarkerColor(ROOT.kBlack)
        retHist.SetLineColor(ROOT.kBlack)
        retHist.SetLineWidth(2)
        retHist.SetLineStyle(7)
        retHist.SetFillColor(0)
        retHist.SetFillStyle(0)
        retHist.Sumw2()
        retHist.SetDirectory(0)

        for i, binCont in enumerate(hist_to_use):
            retHist.SetBinContent (i, binCont)
            err = hist_to_use.GetBinError (i)
            retHist.SetBinError (i, err)
        return retHist


    def appendTo(self,outUrl, makeDataCards=False, channel2run='', regionType = ''):
        #print 'before opening the file in fcn appendTo'
        outF = ROOT.TFile.Open(outUrl,'UPDATE')
        #print 'after opening the file in fcn appendTo'
        # fix me: Error in <TFile::cd>: Unknown directory xyz
        # which disappears if run the script again
        

        #print '/'*100
        #print 'outUrl is', outUrl
        #print 'self.name is', self.name

        #print 'before making directory in fcn appendTo'

        nameDir = channel2run + '_' + regionType if makeDataCards else self.name
        outF.cd(nameDir)#channel2run + '_' + regionType)#self.name)
        exis= outF.GetDirectory(nameDir)
        #FIX ME Error in <TFile::mkdir>: An object with name mm_SR exists already
        if exis ==0:
            try:
                outDir = outF.mkdir(nameDir)
            #outDir.cd()
            except: #Exception as e:
                print "Oops!", sys.exc_info()[0], "occured."
                if outDir: 
                    outDir.cd()
        else:
            outDir = outF.mkdir(nameDir)
            if outDir:
                outDir.cd()

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
                bazinga('try statement deleting ')
                
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
            #print 'maxY in totalMC is ', maxY
            if maxY < stack.GetMaximum():
                maxY = stack.GetMaximum()
                #print 'maxY in stack is ', maxY
        if self.dataH:
            if maxY<self.dataH.GetMaximum():
                maxY=self.dataH.GetMaximum()
                #print 'maxY in dataH is ', maxY
        
        #print 'maxY is ', maxY
        
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


    def doStack(self, outDir,lumi,noScale=False,saveTeX=False, ratio=False, plotData = True, massPoint=0, bdtCut = 0., regionType = None, channel2run = None, doPostFit=False):
        print 'bdtCut is', bdtCut
        if channel2run is None:
            print 'specify "channel2run", exiting...'
            sys.exit(1)
        
        norm_dict_dy = {'ee': {260: 1.48,
                          270: 1.476,
                          300: 1.468,
                          350: 1.441,
                          400: 1.497,
                          450: 1.509,
                          600: 1.667,
                          650: 1.685,
                          900: 1.742,
                          1000: 1.674},
                   'mm': {260: 1.396,
                          270: 1.41,
                          300: 1.367,
                          350: 1.373,
                          400: 1.378,
                          450: 1.385,
                          600: 1.39,
                          650: 1.383,
                          900: 1.387,
                          1000: 1.385}}

        norm_dict_tt = {'ee': {260: 0.931,
                          270: 0.926,
                          300: 0.948,
                          350: 0.961,
                          400: 0.971,
                          450: 0.98,
                          600: 0.781,
                          650: 0.785,
                          900: 0.805,
                          1000: 0.794},
                   'mm': {260: 1.091,
                          270: 1.08,
                          300: 1.097,
                          350: 1.094,
                          400: 1.094,
                          450: 1.097,
                          600: 0.87,
                          650: 0.867,
                          900: 0.868,
                          1000: 0.868}}

        


        labels = ['ee', 'mm']

        df1 = pd.DataFrame(norm_dict_dy)
        df2 = pd.DataFrame(norm_dict_tt)
        #df1
        #print(df2)
        norm_dict = {'DY': df1, "TT": df2 }
        
        norm_dict_of_df = {k: pd.DataFrame(v) for k,v in norm_dict.items()}
        df = pd.concat(norm_dict_of_df, axis=0)
        names=['Normalization', 'Mass']
        df.index.set_names(names, inplace=True )
        df.columns=labels


        DY_norm  = None
        TT_norm  = None
        
        try:
            DY_norm = df[channel2run]['DY'][massPoint]
            TT_norm = df[channel2run]['TT'][massPoint]
        except KeyError as e:
            print 'ERROR looking for:'
            print e
            sys.exit(1)
        
        if not doPostFit:
            DY_norm = 1
            TT_norm = 1 

        makeVisible = True
        shortTitle = True
        

        plot_part_of_bdt = True if bdtCut > -1 else False
        #print 'plot_part_of_bdt is', plot_part_of_bdt
        #print 'lumi is', lumi 
        #print '*'*500
        print 'for {0} and mass {1}'.format(channel2run, massPoint)
        print '{0}=DY_norm and {1}=TT_norm'.format(DY_norm, TT_norm)
        if len(self.mc)==0:
            print '%s has no MC!' % self.name
            return

        if self.mc.values()[0].InheritsFrom('TH2') :
            print 'Skipping TH2'
            return

        c = ROOT.TCanvas('c','c',500,500)
        c.SetBottomMargin(0.)
        c.SetLeftMargin(0.0)
        c.SetTopMargin(0)
        c.SetRightMargin(0.00)

        #holds the main plot
        c.cd()
        p1 = ROOT.TPad('p1','p1',0.0,0.,1.0,0.99) if not ratio else ROOT.TPad('p1','p1',0.0,0.25,1.0,0.99)
        p1.Draw()
        p1.SetRightMargin(0.07 if not ratio else 0.05)
        p1.SetLeftMargin(0.2 if not ratio else 0.15)
        p1.SetTopMargin(0.05)
#check
        p1.SetBottomMargin(0.15) if not ratio else p1.SetBottomMargin(0.)   


        p1.SetGridx(True)
        self._garbageList.append(p1)
        p1.cd()

        # legend

#        leg = ROOT.TLegend(0.25, 0.86, 0.88, 0.94)  
        leg = ROOT.TLegend(0.23, 0.81-0.02*max(len(self.mc)-2,0), 0.925, 0.94)
      
        leg.SetBorderSize(0)
        leg.SetFillStyle(0)
        leg.SetTextFont(43)
        leg.SetTextSize(12)
        nlegCols = 0

        # masses = [260, 270, 300, 350, 400, 450, 600, 650, 900, 1000]
        # idx = None
        # try:
        #     print massPoint
        #     if massPoint==None:
        #         print 'exiting, specify mass point'; sys.exit(1)
        #     idx = masses.index(massPoint)
        # except ValueError:
        #     print 'requested mass in not in the list of "masses", exiting...'
        #     sys.exit(1)



        outF = ROOT.TFile.Open(outDir + '/' + self.name + '_stacks.root','recreate')
        histDict = {}
        if self.dataH is not None:
            if self.data is None: 
                #bdtBin = self.dataH.GetXaxis().FindBin(bdtCut) if 'bdt' in self.dataH.GetName() else None
                #print 'P'*50
                if 'bdt' in self.name and not plotData:
                    print 'P'*50
                    print 'for {0} bdtCut is {1}'.format(self.name, bdtCut)
                    store_dataH =self.dataH.Clone('store_dataH')
                    print '*'*50
                    print 'self.dataH before unblindAllowed(bdtCut):'
                    #self.dataH.Print()
                    self.dataH = self.unblindAllowed(bdtCut)
                    
                else:
                    pass
                
                self.finalize()
                
                print 'self.data.GetTitle() is ', self.data.GetTitle()
                print 'self.dataH.Integral() is ', self.dataH.Integral()
                print 'self.dataH.GetMaximum() is ', self.dataH.GetMaximum()
                leg.AddEntry( self.data, self.data.GetTitle(),'p')
                #leg.AddEntry( self.dataH, self.dataH.GetTitle(),'l')
                histDict[self.data.GetName()] =  self.data
                histDict[self.dataH.GetName()] =  self.dataH
            nlegCols += 1
        for h in self.mc:
            #if not noScale :
            self.mc[h].Scale(lumi)
            if 'DY' in self.mc[h].GetName():
                pass
                #print '1'*5000
                #print 'before', self.mc[h].Integral()
                self.mc[h].Scale(DY_norm)
                #print self.mc[h].GetName()
                #print 'after', self.mc[h].Integral()
            elif 'TT' in self.mc[h].GetName():
                pass
                #print '2'*5000
                #print 'before', self.mc[h].Integral()
                self.mc[h].Scale(TT_norm)
                #print self.mc[h].GetName()
                #print 'after', self.mc[h].Integral()
            else:
                pass
             
            #print 'self.mc[h].GetTitle() is ', self.mc[h].GetTitle()
            #print 'self.mc[h].Integral() is ', self.mc[h].Integral()
            #print 'self.mc[h].GetMaximum() is ', self.mc[h].GetMaximum()
            leg.AddEntry(self.mc[h], self.mc[h].GetTitle(), 'f')
            nlegCols += 1

            #if 'DY' in self.mc[h].GetName():
             #   continue
            histDict[self.mc[h].GetName()] = self.mc[h]

            #print self.mc[h].GetTitle()
           # if 'DY' in self.mc[h].GetTitle():
            #    self.mc[h].Print('all')                

            
        styleList = [1,1,1]*4
        widthList = [2,2,2]*4
 
        for hS in self.mcSignal:

            self.mcSignal[hS].SetLineStyle(styleList[0])
            self.mcSignal[hS].SetLineWidth(widthList[0])
            print '~/~'*30
            print 'self.mcSignal[hS].GetTitle():', self.mcSignal[hS].GetTitle()
            self.mcSignal[hS].Scale(lumi)
            if 'WW' in self.mcSignal[hS].GetTitle():
                print 'self.mcSignal[hS].GetMaximum() is ', self.mcSignal[hS].GetMaximum()
                signalMultFactor = self.dataH.GetMaximum()/self.mcSignal[hS].GetMaximum() if self.mcSignal[hS].GetMaximum() !=0 else self.dataH.GetMaximum()
                if makeVisible:
                    self.mcSignal[hS].Scale(signalMultFactor)
                #self.mcSignal[hS].Scale(branchingRatios[ww])
                print self.name
                print 'self.mcSignal[hS].GetMaximum() is ', self.mcSignal[hS].GetMaximum()
                print 'for ww mass is {0} and factor is {1}'.format(massPoint, signalMultFactor)
            elif 'zz' in self.mcSignal[hS].GetTitle():
                print 'self.mcSignal[hS].GetMaximum() is ', self.mcSignal[hS].GetMaximum()
                signalMultFactor = self.dataH.GetMaximum()/self.mcSignal[hS].GetMaximum() if self.mcSignal[hS].GetMaximum() !=0 else self.dataH.GetMaximum()
                if makeVisible:
                    self.mcSignal[hS].Scale(signalMultFactor)
                #self.mcSignal[hS].Scale(branchingRatios[zz])
                print self.name
                print 'self.mcSignal[hS].GetMaximum() is ', self.mcSignal[hS].GetMaximum()
                print 'for zz mass is {0} and factor is {1}'.format(massPoint, signalMultFactor)
            elif 'ZZ' in self.mcSignal[hS].GetTitle():
                print 'self.mcSignal[hS].GetMaximum() is ', self.mcSignal[hS].GetMaximum()
                signalMultFactor = self.dataH.GetMaximum()/self.mcSignal[hS].GetMaximum() if self.mcSignal[hS].GetMaximum() !=0 else self.dataH.GetMaximum()
                if makeVisible:
                    self.mcSignal[hS].Scale(signalMultFactor)
                #self.mcSignal[hS].Scale(branchingRatios[zz])
                print self.name
                print 'self.mcSignal[hS].GetMaximum() is ', self.mcSignal[hS].GetMaximum()
                print 'for zz mass is {0} and factor is {1}'.format(massPoint, signalMultFactor)
            elif 'vv' in self.mcSignal[hS].GetTitle():
                print 'self.mcSignal[hS].GetMaximum() is ', self.mcSignal[hS].GetMaximum()
                signalMultFactor = self.dataH.GetMaximum()/self.mcSignal[hS].GetMaximum() if self.mcSignal[hS].GetMaximum() !=0 else self.dataH.GetMaximum()

                if makeVisible:
                    self.mcSignal[hS].Scale(signalMultFactor)
                #self.mcSignal[hS].Scale(branchingRatios[vv])
                print self.name
                print 'self.mcSignal[hS].GetMaximum() is ', self.mcSignal[hS].GetMaximum()
                print 'for vv mass is {0} and factor is {1}'.format(massPoint, signalMultFactor)
            else:
                signalMultFactor = None
                print 'smth is wrong, exiting'
                sys.exit(1)

            print '~/~'*30
            #print '-'*50
            #print 'fact is {0} for {1}'.format(fact, self.name)
            #print '-'*50
            fact = None
            if signalMultFactor: 
                fact = determMultiples(signalMultFactor)
            print 'fact is', fact
            legStr = '{0} x {1}'.format(self.mcSignal[hS].GetTitle(), fact)
            if shortTitle:
                legStr = legStr[7:]
            leg.AddEntry(self.mcSignal[hS], legStr, 'l') #f    
            print 'legStr is', legStr
            #leg.AddEntry(self.mcSignal[hS], self.mcSignal[hS].GetTitle(), 'l')
            nlegCols += 1
            histDict[self.mcSignal[hS].GetName()] = self.mcSignal[hS]

        # Build the stack to plot from all backgrounds
        totalMC = None
        stack = ROOT.THStack('mc','mc')
        clr = None
        for h in self.mc:
            stack.Add(self.mc[h],'hist')
            try:
                #if 'DY' in self.mc[h].GetName() or 'TT' in self.mc[h].GetName():    
                 #   continue    

                clr = self.mc[h].GetLineColor()
                self.mc[h].SetFillColor(clr)
                self.mc[h].SetFillStyle(1001)
                totalMC.Add(self.mc[h])
            except:
                totalMC = self.mc[h].Clone('totalmc')
                self._garbageList.append(totalMC)
                totalMC.SetDirectory(0)


        if totalMC is not None:
            leg.AddEntry(totalMC, "Total stat uncertainty", "f")
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
        frame.GetXaxis().SetTitleOffset(1.3)
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
        #control the size of number on the X axis
        stack.GetXaxis().SetLabelSize(0.037)
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
            elif not plotData and 'bdt' in self.name:   # and plot_part_of_bdt
                print 'plotting plot_part_of_bdt'
                #print 'P'*50
                self.data.Draw('p')#SAME PLC PMC') #('p')      
            else:
                pass
             #if self.dataH is not None : self.dataH.Draw('SAME PLC PMC') #('p')

        for hS in self.mcSignal:
            #print 'name of hist to draw ', self.mcSignal[hS].GetName()
            #  try:
                #clr = self.mcSignal[hS].GetLineColor()
                #self.mcSignal[hS].SetFillColor(clr)
                #self.mcSignal[hS].SetFillStyle(1001)
            self.mcSignal[hS].Draw('SAME HIST C') #PLC PMC') #('p')
            #except:
                #pass

        # THIS is where you control height of the distribution on the canvas (before used maxY*1.3)
        if 'hh' in self.name:
            stack.SetMaximum(maxY*6.5)
        else:
            stack.SetMaximum(maxY*6.5)

        c.Modified()

        leg.Draw()
        txt=ROOT.TLatex()
        txt.SetNDC(True)
        txt.SetTextFont(43)
        txt.SetTextSize(16)
        txt.SetTextAlign(12)
        if lumi<100:
            txt.DrawLatex(0.2,0.972,'#bf{CMS} #it{Preliminary}')
            txt.DrawLatex(0.7,0.972,'%3.1f pb^{-1} (13 TeV)' % (lumi) )
        else:
            txt.DrawLatex(0.2,0.972,'#bf{CMS} #it{Preliminary}')
            txt.DrawLatex(0.7,0.972,'%3.1f fb^{-1} (13 TeV)' % (lumi/1000.) )


  #holds the ratio            
        print '='*50, 'before ratio'
        if ratio:
            print '+'*50, 'inside ratio'
            c.cd()
            p2 = ROOT.TPad('p2','p2',0.0,0.02,1.0,0.25)
            p2.Draw()
#check                                                                                           
            p2.SetBottomMargin(0.38)
            p2.SetRightMargin(0.05)
            p2.SetLeftMargin(0.15)
# check                                                                                          
            p2.SetTopMargin(0.04)
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
            ratioframe.GetXaxis().SetTitleSize(0.18)
            ratioframe.GetXaxis().SetTitleOffset(.8)
            #        ratioframe.GetXaxis().SetTitle(xName)                                                   
        #print 'name is ', xName                                                                 
            ratioframe.GetYaxis().CenterTitle()
            
            ratioframe.Draw()
            
        #x.SetTitle(self.mc[0].GetTitle())                                                       


            #print '>'*50, 'before try'
            #print 'self.name is', self.name
            try:
                print 'inside try'
                if 'bdt' in self.name and not plotData:
                    #print 'inside bdt'
                    tmp_ratio_hist=store_dataH.Clone('ratio_hist')
                    #tmp_ratio_hist.Sumw2()
                    #print 'after clone'
                    tmp_ratio_hist.Divide(totalMC)
                    #print 'after divide'
                    ratio_hist = self.unblindAllowed(bdtCut, tmp_ratio_hist)            
                    #print '<>'*50
                    #print 'ratio_hist.GetMaximum() is', ratio_hist.GetMaximum()
                    
                else:
                    ratio_hist=self.dataH.Clone('ratio_hist')
                    ratio_hist.Divide(totalMC)

                ratio_hist.SetDirectory(0)
                self._garbageList.append(ratio_hist)

                gr=ROOT.TGraphAsymmErrors(ratio_hist)
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
        print '='*50, 'before closing file'

        print '='*50, 'after file is closed'
        #save 
   
        for ext in self.plotformats : 
            if self.savelog:
                p1.cd()
                bazinga("before p1.SetLogy()")
                p1.SetLogy()
                c.cd()
                c.Modified()
                c.Update()
                bazinga("after c.Update()")
                if doPostFit:
                    c.SaveAs(os.path.join(outDir, self.name + '_' + regionType + '_' + str(massPoint) + '_log_postFit.'+ext))
                else:
                    bazinga("before SaveAs")
                    c.SaveAs(os.path.join(outDir, self.name + '_' + regionType + '_' + str(massPoint) + '_log.'+ext))
            else:
                if doPostFit:
                    c.SaveAs(os.path.join(outDir, self.name + '_' + regionType + '_' + str(massPoint) + '_postFit.'+ext))
                else: 
                    c.SaveAs(os.path.join(outDir, self.name + '_' + regionType + '_' + str(massPoint) + '.'+ext))

        #print '='*50, 'before save hists'
        outF.cd()
        #print 'I'*50, 'before file name'
        #print 'outF is', outF
        #print 'I'*50, 'after file name'
        for name, hist in histDict.items():
            print 'name is {0} and object is {1}'.format(name, hist)
            hist.Write(name, ROOT.TObject.kOverwrite)
        outF.Close()


        #print '='*50, 'before savetex'
        if saveTeX : self.convertToTeX(outDir=outDir)
        #os.chdir(curDir)
        print '='*50, 'done'



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

        frame.GetXaxis().SetLabelSize(0)
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
    def makeDataCards(self, outDir,lumi,noScale=False,saveTeX=False, regionType=None, massPoint=None, applyBR = True, channel2run = None):
        print 'applyBR is ', applyBR
        
        if channel2run is None:
            print 'specify "channel2run", exiting...'
            sys.exit(1)
        print 'channel2run is', channel2run
        del_zznWW = False
        delVV = False
        delZZ = False
        doBlinding = False # using -t -1 with Higgs combine is doing it automatically: combine -M Asymptotic -t -1 -m NUMBER  comb_400.txt
        #but recommended is --run blind

        dataDict = {}
        printStrings = True
        dataDict[self.dataH.GetName()] = self.dataH
        ndic = dict(self.mc.items() + self.mcSignal.items() + dataDict.items())



        print 'ndic is:'
        pp.pprint(ndic)
        for k, v in ndic.items():
            print k
            print v
            if del_zznWW:
                if '_zz' in k or '_hww' in k:
                    print 'ndic[k] is', ndic[k]
                    del ndic[k]
            if delVV:
                if '_vv' in k:
                    print 'ndic[k] is', ndic[k]
                    del ndic[k]
            if delZZ:
                if '_hzz' in k:
                    print 'ndic[k] is', ndic[k]
                    del ndic[k]

        print 'ndic becomes:'
        pp.pprint(ndic)



        dicRates = collections.defaultdict(str)
        processName = channel2run
        #bbzz
        #masses = [250, 260, 270, 300, 350, 400, 450,       500, 550, 600, 650, 700, 750, 800, 900, 1000]
        #bbvv:     
        masses = [260, 270, 300, 350, 400, 450,             600, 650, 900, 1000]

        idx = None
        try:
            print massPoint
            if massPoint==None: 
                print 'exiting, specify mass point'; sys.exit(1)
            idx = masses.index(massPoint)
        except ValueError:
            print 'requested mass in not in the list of "masses", exiting...'
            sys.exit(1)

            
        #branchingRatios = [0.0444, 0.9556, 1]
        branchingRatios = [0.0012 #HtoZZ                                                                 
                           , 0.0266 #HtoWW                                                               
                           , 0.02787 #HtoVV                                                              
                           ]
        zz = 0
        ww = 1
        vv = 2

        zzFactor = [10000., 15000.,   20000.,  50000.,  50000,    50000, 50000, 
                    50000, 50000., 150000., 500000., 1000000., 4000000., 5000000.,
                    5000000., 5000000.]
        wwFactor = totFactor = [500., 750., 1000., 2500., 5000., 7500., 25000., 50000., 200000., 250000.]
        vvFactor = zzFactor
        lumino = lumi#36000.
        
        zz_signalMultFactor = 1#zzFactor[idx] * 1.
        ww_signalMultFactor = 1#wwFactor[idx] * 1.
        vv_signalMultFactor = 1#vvFactor[idx] * 1.
        zzRate_unscaled = None
        wwRate_unscaled = None
        vvRate_unscaled = None

        DY_norm  =   1.8662
        TT_norm  =   1.0655
        
        fix = False
        zzfix = 6.17449 if fix else 1.
        wwfix = 0.889857/3.35880 if fix else 1.

        dataSubstitution_forSR = 0.
        dataIntegral = 0
        for h in ndic:
            print 'type(h) is ', ndic[h]
            print 'h is', h
            print 'name is', ndic[h].GetName()
            nameEnding_beg = ndic[h].GetName().find('_',5)
            print 'Before any fixes, hist {0} has integral={1}'.format( ndic[h].GetName(), ndic[h].Integral() )
            if '_zz' in ndic[h].GetName():
                zzRate_unscaled = ndic[h].Integral()
                ndic[h].Scale(lumino)#/zz_signalMultFactor)
                if applyBR: 
                    print branchingRatios[zz]
                    ndic[h].Scale(branchingRatios[zz])
                print 'zz unsclaed with mult factor is {0}, after scaling down and applying lumi is {1}'.format(zzRate_unscaled, ndic[h].Integral()) 
                if fix:
                    ndic[h].Scale(zzfix)  
            elif '_hww' in ndic[h].GetName():
                wwRate_unscaled = ndic[h].Integral()
                ndic[h].Scale(lumino)#/ww_signalMultFactor)
                if applyBR: 
                    print branchingRatios[ww]
                    ndic[h].Scale(branchingRatios[ww])
                print 'WW unsclaed with mult factor is {0}, after scaling down and applying lumi is {1}'.format(wwRate_unscaled, ndic[h].Integral())
                if fix:
                    ndic[h].Scale(wwfix)
            elif '_vv' in ndic[h].GetName():
                vvRate_unscaled = ndic[h].Integral()
                ndic[h].Scale(lumino)#/ww_signalMultFactor)                                                                                                
                if applyBR:
                    print branchingRatios[vv]
                    ndic[h].Scale(branchingRatios[vv])
                print 'vv unsclaed with mult factor is {0}, after scaling down and applying lumi is {1}'.format(vvRate_unscaled, ndic[h].Integral())
                if fix:
                    ndic[h].Scale(wwfix)#close to vv?

            elif '_hzz' in ndic[h].GetName():
                ZZRate_unscaled = ndic[h].Integral()
                ndic[h].Scale(lumino)#/vv_signalMultFactor)                                  
                if applyBR:
                    print branchingRatios[zz]
                    ndic[h].Scale(branchingRatios[zz])
                    print 'ZZ unsclaed with mult factor is {0}, after scaling down and applying lumi is {1}'.format(ZZRate_unscaled, ndic[h].Integral())
            else:
                if 'data' not in ndic[h].GetName():# and 'signal' not in ndic[h].GetName():
                    ndic[h].Scale(lumino)
                    # if 'DY' in ndic[h].GetName():
                    #     print '1'*500
                    #     print 'before', ndic[h].Integral()
                    #     ndic[h].Scale(DY_norm)
                    #     print 'after', ndic[h].Integral()
                    # elif 'TT' in ndic[h].GetName():
                    #     print '2'*500
                    #     print 'before', ndic[h].Integral()
                    #     ndic[h].Scale(TT_norm)
                    #     print 'after', ndic[h].Integral()
                    # else:
                    #     pass
                    
                    dataSubstitution_forSR += ndic[h].Integral()
                else:
                    dataIntegral = ndic[h].Integral()

            tmpRate = ndic[h].Integral()
            print 'After fixes, hist {0} has integral={1}'.format( ndic[h].GetName(), tmpRate )
            if 'ZH' in ndic[h].GetName():#[nameEnding_beg+1:]:
                dicRates[ndic[h].GetName()] = [5, round(tmpRate, 2),ndic[h]]
            elif 'VV' in ndic[h].GetName():#[nameEnding_beg+1:]:
                dicRates[ndic[h].GetName()] = [4, round(tmpRate, 2),ndic[h]]
            elif 'ST' in ndic[h].GetName():#[nameEnding_beg+1:]:
                dicRates[ndic[h].GetName()] = [3, round(tmpRate, 2),ndic[h]]
            elif 'DY' in ndic[h].GetName():#[nameEnding_beg+1:]:
                dicRates[ndic[h].GetName()] = [2, round(tmpRate, 2),ndic[h]]
            elif 'TT' in ndic[h].GetName():#[nameEnding_beg+1:]:
                dicRates[ndic[h].GetName()] = [1, round(tmpRate, 2),ndic[h]]
            elif '_hzz' in ndic[h].GetName():#[nameEnding_beg+1:]:
                dicRates[ndic[h].GetName()] = [0, round(tmpRate, 2),ndic[h]]
            elif '_hww' in ndic[h].GetName():#[nameEnding_beg+1:]:
                dicRates[ndic[h].GetName()] = [-1, round(tmpRate, 2),ndic[h]]
            elif '_zz' in ndic[h].GetName():#[nameEnding_beg+1:]:                                                    
                dicRates[ndic[h].GetName()] = [-2, round(tmpRate, 2),ndic[h]]
            elif '_vv' in ndic[h].GetName():#[nameEnding_beg+1:]:                              
                dicRates[ndic[h].GetName()] = [-3, round(tmpRate, 2),ndic[h]]
            elif 'data_obs' in ndic[h].GetName():#[nameEnding_beg+1:]:
                #if regionType == 'SR': ndic[h].Scale(dataSubstitution_forSR/dataIntegral)
                dicRates[ndic[h].GetName()] = [-10, round(tmpRate, 2),ndic[h]]
            else:
                print 'smth went wrong with dataCard'
                sys.exit(1)

        
        ordDict = collections.OrderedDict(sorted(dicRates.items(), key=operator.itemgetter(1)) )
        print 'ordDicts contains:'
        pp.pprint(ordDict) 
        print 'len(ordDict) is', len(ordDict) 
        print
        values = ordDict.get('data_obs')
        if doBlinding:
            if regionType == 'SR':
                print 'Doing SR, thus use dataSubstitution_forSR instead of real data_obs'
                print 'For example, data_obs is {0}, but we would use sum of ALL other MC, which is {1}'.format(values[1], dataSubstitution_forSR)
                ordDict.__setitem__('data_obs', [values[0], round(dataSubstitution_forSR, 2), values[2]])
                ndic['data_obs'].Scale(dataSubstitution_forSR/dataIntegral)
#        for key,value in ordDict.items():
 #           print(key, ":", value)
  #          print 'type(key) is ', type(value[2]) 
        bin = channel2run + '_' + regionType
        print 'bin is', bin
        curDir = os.getcwd()
        if os.path.exists(outDir):
            os.chdir(outDir)
        
        extension = '.input'
        if len(self.name)>5:
            extension += self.name[4:] 
        else:
            pass


        binStr =         'bin                                            '
        processNameStr = 'process                                        '
        processTypeStr = 'process                                        '
        processRateStr = 'rate                                           '
        
        lumiLine       = 'lumi_13TeV                               lnN   '
        puLine         = 'CMS_pu                                   lnN   '
        
        pdf_qqbarLine  = 'pdf_qqbar                                lnN   '
        pdf_ggLine     = 'pdf_gg                                   lnN   '
        vhbb_res_jLine =   'CMS_res_j                                lnN   '
        vhbb_scale_jLine =     'CMS_scale_j                              lnN   '
        vhbb_trigger_METLine = 'CMS_trigger_met                          lnN   '
        if channel2run == 'mm':
            vhbb_eff_mLine =   'CMS_eff_m                                lnN   '
        else:
            vhbb_eff_eLine = 'CMS_eff_e                                lnN   '
        #vhbb_eff_bLine =     'CMS_eff_b                                lnN   '
        QCDscale_VHLine    = 'QCDscale_VH                              lnN   '
        QCDscale_HHLine    = 'QCDscale_Higgs_HH                        lnN   '
        QCDscale_ttbarLine = 'QCDscale_TT                              lnN   '
        QCDscale_VVLine    = 'QCDscale_VV                              lnN   '
        QCDscale_DYLine    = 'QCDscale_DY                              lnN   '
        QCDscale_STLine    = 'QCDscale_ST                              lnN   '
        xsecTT_line =        'xsec_TT                                  lnN   '
        xsecST_line =        'xsec_ST                                  lnN   '
    
        #eff_m_shapeLine = 'vhbb_eff_m                               shape '
        #btag_lf_shapeLine = 'vhbb_btag_lf                            shape '
        #btag_hf_shapeLine = 'vhbb_btag_hf                            shape '
        JEC_shapeLine  =  'CMS_scale_j                            shape   '
        JER_shapeLine  =      'CMS_res_j                              shape   '

        eff_m_ID_shapeLine  =  'CMS_eff_m_ID                           shape   '
        eff_m_ISO_shapeLine  =  'CMS_eff_m_ISO                          shape   '
        eff_m_tracker_shapeLine  =  'CMS_eff_m_tracker                      shape   '
        eff_m_trigger_shapeLine  =  'CMS_eff_m_trigger                      shape   '

        eff_e_ID_shapeLine  =  'CMS_eff_e_ID                           shape   '
        eff_e_tracker_shapeLine  =  'CMS_eff_e_tracker                      shape   '
        eff_e_trigger_shapeLine  =  'CMS_eff_e_trigger                      shape   '

        btag_lf_shapeLine    =  'CMS_btag_light                        shape   '
        btag_hf_shapeLine    =  'CMS_btag_heavy                        shape   '

        eff_met_JE_shapeLine  =  'CMS_eff_met_JetEn                      shape   '
        eff_met_UE_shapeLine  =  'CMS_eff_met_UnclusteredEn              shape   '
        eff_met_JR_shapeLine  =  'CMS_eff_met_JetRes                     shape   '


        qqbarList = ['DY', 'ST', 'VV', 'ZH']
        ggList = ['si', 'TT']#gnal_zz', 'signal_vv', 'signal_ZZ', 'signal_WW', 'TT']
        #ggList = ['signal_vv', 'signal_zz', 'signal_ww', 'TT']

        histObj = 2
        typ = 0
        rate = 1
        padding = 20
        #use extension below?
        outF = ROOT.TFile.Open('hists_' + self.name + '_' + bin + 'input.root','recreate')        
        for h in ordDict:
            if 'data' not in h:
                print 'h is ', h
                print 
                binStr += bin.ljust(padding)
                processNameStr += h.ljust(padding)
                processTypeStr += ('{0}'.format(ordDict[h][typ])).ljust(padding)
                processRateStr += ('{0}'.format(ordDict[h][rate])).ljust(padding)
                
                lumiLine += '1.026'.ljust(padding)
                puLine += '1.06'.ljust(padding)
                if h[:2] in qqbarList:
                    pdf_qqbarLine  += '1.05'.ljust(padding)
                else:
                    pdf_qqbarLine  += '-'.ljust(padding)

                if h[:2] in ggList:
                    pdf_ggLine     += '1.03'.ljust(padding)
                else:
                    pdf_ggLine     += '-'.ljust(padding)

                vhbb_res_jLine += '1.05'.ljust(padding)
                vhbb_scale_jLine += '1.05'.ljust(padding)
                
                #vhbb_trigger_METLine += '1.03'.ljust(padding)
                #vhbb_eff_mLine += '1.03'.ljust(padding)
                #vhbb_eff_bLine += '1.05'.ljust(padding)
                
                # eff_m_shapeLine += '1'.ljust(padding)
                # btag_lf_shapeLine += '1'.ljust(padding)
                # btag_hf_shapeLine += '1'.ljust(padding)
                # JER_shapeLine  +=  '1'.ljust(padding)
                JEC_shapeLine  +=  '1'.ljust(padding)
                JER_shapeLine  +=  '1'.ljust(padding)

                if channel2run =='mm':
                    eff_m_ID_shapeLine  +=  '1'.ljust(padding)
                    eff_m_ISO_shapeLine  +=  '1'.ljust(padding)
                    eff_m_tracker_shapeLine  +=  '1'.ljust(padding)
                    eff_m_trigger_shapeLine  +=  '1'.ljust(padding)
                
                    eff_e_ID_shapeLine  +=  '-'.ljust(padding)
                    eff_e_tracker_shapeLine  +=  '-'.ljust(padding)
                    eff_e_trigger_shapeLine  +=  '-'.ljust(padding)
                else:
                    eff_m_ID_shapeLine  +=  '-'.ljust(padding)
                    eff_m_ISO_shapeLine  +=  '-'.ljust(padding)
                    eff_m_tracker_shapeLine  +=  '-'.ljust(padding)
                    eff_m_trigger_shapeLine  +=  '-'.ljust(padding)

                    eff_e_ID_shapeLine  +=  '1'.ljust(padding)
                    eff_e_tracker_shapeLine  +=  '1'.ljust(padding)
                    eff_e_trigger_shapeLine  +=  '1'.ljust(padding)

                btag_lf_shapeLine  +=  '1'.ljust(padding)
                btag_hf_shapeLine  +=  '1'.ljust(padding)

                eff_met_JE_shapeLine  +=  '1'.ljust(padding)
                eff_met_UE_shapeLine  +=  '1'.ljust(padding)
                eff_met_JR_shapeLine  +=  '1'.ljust(padding)




                if h[:2] in 'ZH':
                    QCDscale_VHLine += '1.04'.ljust(padding)
                else:
                    QCDscale_VHLine += '-'.ljust(padding)

                if h[:2] in 'TT':
                    QCDscale_ttbarLine  += '1.06'.ljust(padding)
                    xsecTT_line +=         '1.053'.ljust(padding)
                else:
                    QCDscale_ttbarLine  += '-'.ljust(padding)
                    xsecTT_line +=         '-'.ljust(padding)

                if h[:2] in 'si' and 'hzz' in h:
                    QCDscale_HHLine += '1.04'.ljust(padding)
                else:
                    QCDscale_HHLine += '-'.ljust(padding)

                if h[:2] in 'ST':
                    QCDscale_STLine  += '1.06'.ljust(padding)
                    xsecST_line +=         '1.072'.ljust(padding)
                else:
                    QCDscale_STLine  += '-'.ljust(padding)
                    xsecST_line +=         '-'.ljust(padding)

                if h[:2] in 'VV':
                    QCDscale_VVLine += '1.04'.ljust(padding)
                else:
                    QCDscale_VVLine += '-'.ljust(padding)

                if h[:2] in 'DY':
                    QCDscale_DYLine +='1.06'.ljust(padding)
                else:
                    QCDscale_DYLine +='-'.ljust(padding)

            (ordDict[h])[histObj].Write(h, ROOT.TObject.kOverwrite)
       
        outF.Close()

        strDY = 'DY'
        strTT = 'TT'
        strCR = 'CR'
        strSR = 'SR'
        rateParam = 'rateParam'
        space = ' '
        normStr = '_norm'
        one = '1'
        #rateParam0 = 'SR'
        #rateParam1 = 'CRDY'
        #rateParam2 = 'CRTT'
        systParamLineDY = strDY + normStr + space + rateParam + space + bin + space + strDY + space + one
        systParamLineTT = strTT + normStr + space + rateParam + space + bin + space + strTT + space + one
           
        #if 'hhMt' in self.name:
         #   pass
        if True:
        #encoding='utf-8'
            with io.open ('dataCard_' + regionType + '_' + self.name + '.txt', mode = 'wb') as fOut:
                fOut.write('#  DataCard for ' + regionType + ' \n')
                
                #fOut.write('# Data_obs is {0}, but we would use sum of ALL other MC, which is {1}\n'.format(values[1], dataSubstitution_forSR))
                
                fOut.write('#  For ' + str(massPoint) + 'GeV signal mass point\n')
                fOut.write('#  "{0}" variable\n'.format(self.name))
                fOut.write('#  Draft of the HHtobbZZto2b2l2nu datacard\n')
                fOut.write('#-----------------------------------------------------------------------------------\n')
            #fOut.write('imax 1 number of channels, switch to two when add EGamma data?\njmax {0} number of MC samples minus one\nkmax * number of nuisance parameters (sources of systematical uncertainties)\n'.format(   len(ordDict) -2  ))# -1 for data_obs, -1 for each signal sample
                fOut.write('imax 1 number of channels\njmax {0} number of mc samples minus one\nkmax * number of nuisance parameters (sources of systematic uncertainties)\n'.format(   len(ordDict) -2  ))# -1 for data_obs, -1 for each signal sample
                fOut.write('#-----------------------------------------------------------------------------------\n')
                fOut.write('#  syntax:\n')
                fOut.write('#  shapes  _process_  _channel_   _file_    _histogram-name_      _histogram-name-for-systematics_\n')
                fOut.write('#  or\n')
                #fOut.write('#  shapes * * ' + bin + '_Mt.root $CHANNEL/$PROCESS $CHANNEL/$PROCESS_$SYSTEMATIC\n')
                fOut.write('#  shapes * * ' + bin + '.input.root $CHANNEL/$PROCESS $CHANNEL/$PROCESS_$SYSTEMATIC\n')
                #fOut.write('shapes * * ' + bin + '_Mt.root $PROCESS $PROCESS_$SYSTEMATIC\n')
                fOut.write('shapes * * ' + bin + '.input.root {0}/$PROCESS {1}/$PROCESS_$SYSTEMATIC\n'.format(bin, bin))
                fOut.write('#-----------------------------------------------------------------------------------\n')
            #fOut.write('# so far we have just one channel, in which we observe N events in data (yield, or Integral() \n')
                fOut.write('bin {0}_{1}\n'.format(channel2run, regionType))
                fOut.write('observation {0}\n'.format((ordDict['data_obs'])[rate]))
                fOut.write("#  rate is obtained using hhMt->Integral()\n")# of root -l muon2016data.root from:\n")
            #fOut.write('#~/workspace/private/feb22HH/CMSSW_8_0_25/src/VHbbAnalysis/Heppy/test/analysis_apr01_tot_hzz_CRDY_v5 and similar for other regions!\n')
                fOut.write('#-----------------------------------------------------------------------------------\n')
            #fOut.write('# zz rate is {0}/{1} times "fixme" factor {2}\n'.format(zzRate_unscaled, zz_signalMultFactor, zzfix))
            #fOut.write('# ww rate is {0}/{1} times "fixme" factor {2}\n'.format(wwRate_unscaled, ww_signalMultFactor, wwfix))
                
                fOut.write(binStr)
                fOut.write('\n')
            #fOut.write('process      {0}\n'.format(processNameStr))
                fOut.write(processNameStr)
                fOut.write('\n')
                fOut.write(processTypeStr)
                fOut.write('\n')
            #fOut.write('process      {0}\n'.format(processRateStr))
            #fOut.write('rate         {0}\n'.format(processTypeStr))
                fOut.write(processRateStr)
                fOut.write('\n')
                fOut.write('#-----------------------------------------------------------------------------------\n')
                #fOut.write('#  lnN SYSTEMATICS \n')
                fOut.write('#  SYSTEMATICS goes below\n')
                fOut.write('#  syntax: name rateParam bin process initial_value [min,max]\n')
                fOut.write('\n')
            #if 'TT' in regionType:
            #   fOut.write(systParamLineTT)
            #  fOut.write('\n')
#elif 'DY' in regionType:
#               fOut.write(systParamLineDY)
#              fOut.write('\n')
   #         elif 'SR' in regionType:
                fOut.write(systParamLineDY)
                fOut.write('\n')
                fOut.write(systParamLineTT)
                fOut.write('\n')
                fOut.write('\n')
                fOut.write(lumiLine)
                fOut.write('\n')
                fOut.write(puLine)
                fOut.write('\n')
                fOut.write(pdf_qqbarLine)
                fOut.write('\n')
                fOut.write(pdf_ggLine)
                fOut.write('\n')
                #fOut.write(vhbb_res_jLine)
                #fOut.write('\n')
                #fOut.write(vhbb_scale_jLine)
                #fOut.write('\n')
                #fOut.write(vhbb_trigger_METLine)
                #fOut.write('\n')
                #if channel2run =='mm':
                 #   fOut.write(vhbb_eff_mLine)
                #else:
                 #   fOut.write(vhbb_eff_eLine)
                #fOut.write('\n')
                #fOut.write(vhbb_eff_bLine)
                #fOut.write('\n')
                fOut.write(QCDscale_VHLine)
                fOut.write('\n')
                fOut.write(QCDscale_ttbarLine)
                fOut.write('\n')
                fOut.write(QCDscale_VVLine)
                fOut.write('\n')
                fOut.write(QCDscale_DYLine)
                fOut.write('\n')
                fOut.write(QCDscale_STLine)
                fOut.write('\n')
                fOut.write(QCDscale_HHLine)
                fOut.write('\n')
                fOut.write('\n')
                fOut.write(xsecTT_line)
                fOut.write('\n')
                fOut.write(xsecST_line)
                fOut.write('\n')
                fOut.write('\n')
                fOut.write(JEC_shapeLine)
                fOut.write('\n')
                fOut.write(JER_shapeLine)
                fOut.write('\n')
                fOut.write(eff_m_ID_shapeLine)
                fOut.write('\n')
                fOut.write(eff_m_ISO_shapeLine)
                fOut.write('\n')
                fOut.write(eff_m_tracker_shapeLine)
                fOut.write('\n')
                fOut.write(eff_m_trigger_shapeLine)
                fOut.write('\n')
                fOut.write(eff_e_ID_shapeLine)
                fOut.write('\n')
                fOut.write(eff_e_tracker_shapeLine)
                fOut.write('\n')
                fOut.write(eff_e_trigger_shapeLine)
                fOut.write('\n')
                fOut.write(btag_lf_shapeLine)
                fOut.write('\n')
                fOut.write(btag_hf_shapeLine)
                fOut.write('\n')
                fOut.write(eff_met_JE_shapeLine)
                fOut.write('\n')
                fOut.write(eff_met_UE_shapeLine)
                fOut.write('\n')
                fOut.write(eff_met_JR_shapeLine)
                fOut.write('\n')
                fOut.write('\n')
                
            if printStrings:
                print 'Doing {0} GeV datacard with {1}'.format(massPoint, self.name)
                print 'observation is    {0}'.format((ordDict['data_obs'])[rate])
                print 'binStr is         ', binStr
                print 'processNameStr is ', processNameStr
                print 'processTypeStr is ', processTypeStr
                print 'processRateStr is ', processRateStr
                print 'lumiLine is       ', lumiLine
        os.chdir(curDir)



#===========================
    def overlayHists(self, outDir,lumi,noScale=False,saveTeX=False, massPoint=0):
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
            styleList = [1,1,1]*4
            widthList = [2,2,2]*4
            self.mcSignal[h].SetLineStyle(1)    
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
    #print 'grpois.Print() is:'
    #grpois.Print() 
    #print 
    for i in xrange(0,grpois.GetN()+1) :
        if i >= grpois.GetN(): continue
        N = grpois.GetY()[i]
        if N<200 :
            if N <= 0: 
                grpois.SetPoint(i, -10,-10)
                #continue
            L = 0
            if N>0 : L = ROOT.Math.gamma_quantile(alpha/2,N,1.)
            U = ROOT.Math.gamma_quantile_c(alpha/2,N+1,1)
            grpois.SetPointEYlow(i, N-L)
            grpois.SetPointEYhigh(i, U-N)
        else:
            grpois.SetPointEYlow(i, math.sqrt(N))
            grpois.SetPointEYhigh(i,math.sqrt(N))
    return grpois


# def convertToPoissonErrorGr(h):

#     htype=h.ClassName()
#     if htype.find('TH1')<0 : return None
#     bazinga ('in the convert fcn')
#     #check https://twiki.cern.ch/twiki/bin/view/CMS/PoissonErrorBars
#     alpha = 1 - 0.6827;
#     mygr = ROOT.TGraphAsymmErrors(h);


#     if not bdtBin:
#         from array import array
#         x, y = array( 'd' ), array( 'd' )
#         X = mygr.GetX()
#         Y = mygr.GetY()
#         count = 0
#         xarr = []
#         yarr = []
#         print 'name is ', h.GetName()
        
#         print 'bdtBin is', bdtBin
#         print 'b'*50
#         for i in xrange( 0, mygr.GetN()+1 ):
#         #if i==0:
#             print '1'*50
#             print 'mygr.GetN() is ', mygr.GetN()
#             print count
#             if i >= mygr.GetN(): continue
#             if bdtBin:
#                 if i < bdtBin:
#                     x.append( X[i] )
#                     y.append( Y[i])
#             else:
#                 x.append( X[i] )
#                 y.append( Y[i])
        
#             count += 1
        
#             print(' i %i %f %f ' % (i,X[i],Y[i]))
#     # const Int_t n = 10;
#     # Double_t x[n]   = {-0.22, 0.05, 0.25, 0.35, 0.5, 0.61,0.7,0.85,0.89,0.95};
#     # Double_t y[n]   = {1,2.9,5.6,7.4,9,9.6,8.7,6.3,4.5,1};
#     # Double_t exl[n] = {.05,.1,.07,.07,.04,.05,.06,.07,.08,.05};
#     # Double_t eyl[n] = {.8,.7,.6,.5,.4,.4,.5,.6,.7,.8};
#     # Double_t exh[n] = {.02,.08,.05,.05,.03,.03,.04,.05,.06,.03};
#     # Double_t eyh[n] = {.6,.5,.4,.3,.2,.2,.3,.4,.5,.6};
#     # gr = new TGraphAsymmErrors(n,x,y,exl,exh,eyl,eyh);
#             print count
#             print x
#             print y
#     #grpois = ROOT.TGraph(len(xarr), array('d', xarr), array('d', yarr))

#             grpois = ROOT.TGraphAsymmErrors( count, x, y )
#             grpois.SetTitle( mygr.GetTitle())
#             print 'grpois.GetN() is ', grpois.GetN()

#     else:
#         grpois.ROOT.TGraphAsymmErrors(mygr)

#     for i in xrange(0,grpois.GetN()+1) :
#         if i >= grpois.GetN(): continue
#         if i==0:
#             print 'O'*50
#             print 'grpois.GetN() is ', grpois.GetN()
#         #print '"i" is', i
#         print 'Inside grpois, bin {0} has content{1}'.format(i, grpois.GetY()[i])

#         N = grpois.GetY()[i]
#         #print 'N={0} at i={1}'.format(N, i)
#         if N<200 :
#             L = 0
#             if N>0 : L = ROOT.Math.gamma_quantile(alpha/2,N,1.)
#             U = ROOT.Math.gamma_quantile_c(alpha/2,N+1,1)
#             grpois.SetPointEYlow(i, N-L)
#             grpois.SetPointEYhigh(i, U-N)
#         else:
#             grpois.SetPointEYlow(i, math.sqrt(N))
#             grpois.SetPointEYhigh(i,math.sqrt(N))
    
#     return grpois


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
    parser.add_option(      '--doPostFit',   dest='doPostFit' ,  help='produce PostFit plots',          default=False,   action='store_true')
    parser.add_option(      '--saveTeX',     dest='saveTeX' ,    help='save as tex file as well',       default=False,   action='store_true')
    parser.add_option(      '--rebin',       dest='rebin',       help='rebin param factor',             default=1,       type=int)
    parser.add_option('-l', '--lumi',        dest='lumi' ,       help='lumi to print out',              default=1,       type=float)
    parser.add_option('-b', '--bdtCut',      dest='bdtCut' ,     help='bdtCut value',                   default=-1,      type=float)
    parser.add_option(      '--only',        dest='only',        help='plot only these (csv)',          default='',      type='string')
    parser.add_option('-k', '--kind',        dest='kind'  ,      help='kind of plot: "Stack", "OverlayHists" or "makeDataCards"',default=None,   type='string')
    parser.add_option('-r', '--region',      dest='region',      help='SR(no Data for Higgs lots) or CRXY with data',default=None,   type='string')
    #parser.add_option('--fzz', '--zzfactor',   dest='zzfactor',    help='factor xN with which ZZ signal is multiplied',default=1,   type=int)
    #parser.add_option('--fww', '--wwfactor',   dest='wwfactor',    help='factor xN with which WW signal is multiplied',default=1,   type=int)
    parser.add_option('-m', '--massPoint',        dest='massPoint' ,       help='Signal massPoint value',              default=None,    type=int)
    parser.add_option(      '--branchingRatio',        dest='branchingRatio',        help='apply branching ratios',          action='store_true', default=False) #if you add to the arguments --branchingRatio, then it is True, if you omit, then it defaults to false, this is how "action='store_true'" works
    parser.add_option('', '--channel2run',               dest='channel2run',             help='channel to run:0=muons, 1=eles',   default=0,               type='int')
    parser.add_option('', '--systUnc',      dest='systUnc',      help='type of shape systematics',default=None,   type='string')
    (opt, args) = parser.parse_args()
    
    applyBR = opt.branchingRatio
    bdtCut = opt.bdtCut
    #print 'bdtCut passed is', bdtCut

    do_hzz_hbb_fix = False
    doPostFit = opt.doPostFit
    #read list of samples
    jsonFile = open(opt.json,'r')
    samplesList=json.load(jsonFile,encoding='utf-8').items()
    jsonFile.close()
    #print 'opt.lumi is ', opt.lumi 
    onlyList=opt.only.split(',')

    massPoint = opt.massPoint  
    if massPoint is None or massPoint ==0:
        print 'please specify massPoint, exiting..'
        sys.exit(1)
        
    channel2run = 'mm' if opt.channel2run == 0 else "ee" if opt.channel2run == 1 else "" 
    systUnc = opt.systUnc
    #print 'systUnc is', systUnc

    extraName = 'shapes_' + channel2run + '_' + systUnc
    #print '~'*100
    #print 'extraName is', extraName
    #read plots 
    plots={}
    for tag,sample in samplesList: 
        
        if 'Bulk' in tag and str(massPoint) not in tag: continue
        
        fIn=ROOT.TFile.Open('%s/%s_%s.root' % ( opt.inDir, tag, extraName) )
        print 'opening %s/%s_%s.root' % ( opt.inDir, tag, extraName)
        try:
            for tkey in fIn.GetListOfKeys():
                key=tkey.GetName()
                #print
                #print '+'*500

                
                #if 'sf' in key: continue
                print 'key is', key                
                if 'makeDataCards' in opt.kind:
                    if 'h' in key or 'z' in key or 'met' in key or 'dR' in key or ('bdt' in key): 
                        pass
                        #print 'key is ', key
                        # print 'massPoint type is', type(massPoint)
                        # print 'tag type is', type(tag)
                
                    else:
                        continue

                keep=False
                for tag in onlyList: 
                    if tag in key: keep=True
                if not keep: continue
                obj=fIn.Get(key)
                if channel2run == 'mm' and 'iso03' in obj.GetName() or channel2run == 'ee' and 'iso04' in obj.GetName():
                    continue
                #if obj.IsEmpty():
                 #   if channel2run == 'mm' and 'iso04' in obj.GetName() or channel2run == 'ee' and 'iso03' in obj.GetName():
                  #      bazinga("empty iso hist {0}".format(obj))
                   #     continue
                if not obj.InheritsFrom('TH1') : continue
                #print 'obj.GetXaxis().GetTitle()', obj.GetXaxis().GetTitle()
                obj_x_title = obj.GetXaxis().GetTitle()
                if do_hzz_hbb_fix and 'Hbb mass' in obj_x_title or 'HZZ mass' in obj_x_title:
                    hbb_title = 'Hbb mass [GeV]'
                    hzz_title = 'HZZ mass [GeV]'
                    if obj_x_title == hbb_title:
                        obj.GetXaxis().SetTitle(hzz_title)
                    elif obj_x_title == hzz_title:
                        obj.GetXaxis().SetTitle(hbb_title)
                    else:
                        print 'cannot happen, exiting'
                        sys.exit(1)
                #print 'new obj.GetXaxis().GetTitle()', obj.GetXaxis().GetTitle()
                #print '-'*500
                if not key in plots : 
                    #print 'processing ', fIn
                    plots[key]=Plot(key)
                if opt.rebin>1:  obj.Rebin(opt.rebin)
                bazinga('add "Plot" to dict of plots')
                bazinga('title is {0} and it is signal?{1}'.format(sample[3], sample[6]))
    #            plots[key].add(h=obj,title=sample[3],color=sample[4],isData=sample[1])
                plots[key].add(h=obj,title=sample[3],color=sample[4],isData=sample[1], isSignal=sample[6])
                print 'successfully added plot'
        except:
            print 'Skipping %s'%tag

    #show plots
    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gROOT.SetBatch(True)

    if opt.kind:
        outDir=opt.inDir+'/plots/' + str(opt.kind) + '/' + str(massPoint) #+ '/test_wo_br' #+ '/testWithBR/'
        os.system('mkdir -p %s' % outDir)
  
    dataOrNot = True if 'CR' in opt.region  else False
    regionType = opt.region
    #print regionType
    
    #zzFactor = opt.zzfactor
    #wwFactor = opt.wwfactor
    for p in plots : 
        plotName = plots[p].name
        if 'bdt' in plotName: opt.saveLog = True

        print 'plotName is', plotName
        #CHECK ME HERE!
        opt.saveLog = True
        if opt.saveLog    : plots[p].savelog=True
        #print 'p is ', p
        #print 'type of p is ', type(p)
        #print 'p name is ', plots[p].name

        if not opt.silent :
            
            if 'Stack' in opt.kind and 'cutFlow' not in plotName:# == 'Stack' or 'StackNoRatio':
#                if 'h' in plotName:
 #                   plots[p].doStack(outDir=outDir,lumi=opt.lumi,saveTeX=opt.saveTeX, ratio = dataOrNot, plotData = dataOrNot)
  #              else:
                #print 'will do "Stack"'
                if 'bdt' not in plotName:
                    plots[p].doStack(outDir=outDir,lumi=opt.lumi,saveTeX=opt.saveTeX, ratio=dataOrNot, plotData = dataOrNot, massPoint=massPoint, bdtCut=bdtCut, regionType=regionType, doPostFit=doPostFit, channel2run=channel2run)
                else:#if 'bdt' in plotName:
                    plots[p].doStack(outDir=outDir,lumi=opt.lumi,saveTeX=opt.saveTeX, ratio=True, plotData = dataOrNot, massPoint=massPoint, bdtCut=bdtCut, regionType=regionType, doPostFit=doPostFit, channel2run=channel2run)
                #else:
                    #plots[p].doStack(outDir=outDir,lumi=opt.lumi,saveTeX=opt.saveTeX, ratio=True, plotData = True, massPoint=massPoint, bdtCut=bdtCut, regionType=regionType)
                    #   pass
            

            elif 'Stack' in opt.kind and 'cutFlow' in plotName:
                print 'will do "OverlayHists" because it is cutFlow!'
                plots[p].overlayHists(outDir=outDir,lumi=opt.lumi,saveTeX=opt.saveTeX, massPoint=massPoint)

            elif 'OverlayHists' in opt.kind:# == 'OverlayHists':
                print 'will do "OverlayHists"'
                plots[p].overlayHists(outDir=outDir,lumi=opt.lumi,saveTeX=opt.saveTeX, massPoint=massPoint)
            elif 'makeDataCards' in opt.kind:

                    print 'will do "makeDataCards"'
                    plots[p].makeDataCards(outDir=outDir,lumi=opt.lumi,saveTeX=opt.saveTeX, regionType=regionType, massPoint=massPoint, applyBR=applyBR, channel2run=channel2run)
            else:
                print "\nwrong kind of plot is specified, please use '-k Stack', '-k StackNoRatio' or '-k OverlayHists' or '-r makeDataCards'"
                sys.exit(1) # vs exit(1)

        bazinga ('after call to overlayHists')
        if 'makeDataCards' in opt.kind:
            plots[p].appendTo(outDir+'/{0}_{1}.input.root'.format(plotName, channel2run+ '_' + regionType + '_' + systUnc), makeDataCards=True, channel2run = channel2run, regionType=regionType)
        else:
            plots[p].appendTo(outDir+'/plotter{0}.root'.format('_postFit' if doPostFit else ''))
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

