#!/usr/bin/env python

import optparse
import os, io # f@cking Python 2.X
import sys
import json
import pickle
import ROOT
from subprocess import Popen, PIPE
from functools import partial
import pickle 
import time
from ROOT import TLorentzVector
#from getHHMass_rk import computeHHMass # def computeHHMass(leps, met, bjets)
from operator import itemgetter, attrgetter, methodcaller

# to set CMS Pub style, use personal modified version instead
#sys.path.append('/afs/cern.ch/user/r/rkamalie/workspace/private/tdr-style')
#import tdrstyle
#import copy

# to open image from the directory using Python
#from PIL import Image                                                    
#import matplotlib.pyplot as plt 
#import matplotlib.image as mpimg                     
def createH1():
    h1 = TH1F("h1", ("Two gaussian plots and their ratio; x title; h1 and h2"
                " histograms"), 100, -5, 5)
    h1.SetLineColor(kBlue+1)
    h1.SetLineWidth(2)
    h1.FillRandom("gaus")
    h1.GetYaxis().SetTitleSize(20)
    h1.GetYaxis().SetTitleFont(43)
    h1.GetYaxis().SetTitleOffset(1.55)
    h1.SetStats(0)
    return h1


def createRatio(h1, h2):
    h3 = h1.Clone("h3")
    h3.SetLineColor(kBlack)
    h3.SetMarkerStyle(21)
    h3.SetTitle("")
    h3.SetMinimum(0.8)
    h3.SetMaximum(1.35)
    # Set up plot for markers and errors
    h3.Sumw2()
    h3.SetStats(0)
    h3.Divide(h2)

    # Adjust y-axis settings
    y = h3.GetYaxis()
    y.SetTitle("ratio h1/h2 ")
    y.SetNdivisions(505)
    y.SetTitleSize(20)
    y.SetTitleFont(43)
    y.SetTitleOffset(1.55)
    y.SetLabelFont(43)
    y.SetLabelSize(15)

    # Adjust x-axis settings
    x = h3.GetXaxis()
    x.SetTitleSize(20)
    x.SetTitleFont(43)
    x.SetTitleOffset(4.0)
    x.SetLabelFont(43)
    x.SetLabelSize(15)

    return h3


def createCanvasPads():
    c = TCanvas("c", "canvas", 800, 800)
    # Upper histogram plot is pad1
    pad1 = TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
    pad1.SetBottomMargin(0)  # joins upper and lower plot
    pad1.SetGridx()
    pad1.Draw()
    # Lower ratio plot is pad2
    c.cd()  # returns to main canvas before defining pad2
    pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
    pad2.SetTopMargin(0)  # joins upper and lower plot
    pad2.SetBottomMargin(0.2)
    pad2.SetGridx()
    pad2.Draw()

    return c, pad1, pad2


def saveCanvases(dic):
    ROOT.gStyle.SetOptStat(0)
    
    for k in dic:
        c = ROOT.TCanvas("c", "canvas", 800, 800)
        c.cd()

        dic[k].SetLineColor(ROOT.kBlue+1)
        dic[k].SetLineWidth(2)
        dic[k].GetYaxis().SetTitleSize(20)
        dic[k].GetYaxis().SetTitleFont(43)
        dic[k].GetYaxis().SetTitleOffset(1.55)
        dic[k].SetStats(0)
        #if dic[k].InheritsFrom('TH2'): 
        dic[k].Draw('colz') if dic[k].InheritsFrom('TH2') else dic[k].Draw()
        c.SaveAs(dic[k].GetName()+".png")



debugMode = False # for priting with bazinga
def bazinga (mes):
    if debugMode:
        print mes


def plot(rootFile, outFileURL):
    histos={

        'genZMass'      :ROOT.TH1F('genZMass', ';gen Z mass [GeV]; Events', 30, 40, 100),
        'recoZMass'      :ROOT.TH1F('recoZMass', ';reco Z mass [GeV]; Events', 30, 40, 100),
        'invisibleMt'      :ROOT.TH1F('invisibleMt', ';invisible transverse mass [GeV]; Events', 75, 0, 500),
        'genVSrecoZMass'      :ROOT.TH2F('genVSrecoZMass', ';gen Z mass [GeV]; reco Z mass [GeV]', 30, 40, 100, 30, 40, 100),
        # x, y, weight
        #histos['genVSrecoZMass'].Fill(firstGenZBoson_p4.M(), Z_p4.M(), evWgt)



        }
    bazinga('after histos')
    for key in histos:
        histos[key].Sumw2()
        histos[key].SetDirectory(0)

    print 'rootFile is ', rootFile
    fIn = ROOT.TFile.Open(rootFile)

    tree=fIn.Get('tree')
     
    totalEntries = tree.GetEntries() 
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
                      
        bazinga('before get entry')
        tree.GetEntry(i)
        if tree.GenVbosons_pdgId != 23 and tree.nGenVbosons < 2: continue

        if i%100==0 : 
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





        firstGenZBoson_p4 = ROOT.TLorentzVector()
        Z_p4=ROOT.TLorentzVector()  
        missing_p4=ROOT.TLorentzVector()  


        bazinga('get ready to build HH') 

        for i in xrange(0, len(tree.GenVbosons_pt)):
            if i==0:
                firstGenZBoson_p4.SetPtEtaPhiM(tree.GenVbosons_pt[i],tree.GenVbosons_eta[i],tree.GenVbosons_phi[i],tree.GenVbosons_mass[i])   
            else:
                continue

        Z_p4.SetPtEtaPhiM(tree.V_pt,tree.V_eta,tree.V_phi,tree.V_mass)   
        missing_p4.SetPtEtaPhiM(tree.met_pt,tree.met_eta,tree.met_phi,tree.met_mass)    
        
        histos['genZMass'].Fill(firstGenZBoson_p4.M(), evWgt)
        histos['recoZMass'].Fill(Z_p4.M(), evWgt)
        histos['invisibleMt'].Fill(missing_p4.Mt(), evWgt)
        histos['genVSrecoZMass'].Fill(firstGenZBoson_p4.M(), Z_p4.M(), evWgt)




    saveCanvases(histos)
    # h3 = createRatio(h1, h2)
    # c, pad1, pad2 = createCanvasPads()
    # pad1.cd()
    # h1.Draw()
    # h2.Draw("same")
    # h1.GetYaxis().SetLabelSize(0.0)
    # axis = TGaxis(-5, 20, -5, 220, 20, 220, 510, "")
    # axis.SetLabelFont(43)
    # axis.SetLabelSize(15)
    # axis.Draw()
    # pad2.cd()
    # h3.Draw("ep")
    # from ROOT import gROOT 
    # gROOT.GetListOfCanvases().Draw()


#save histograms to file
    fOut=ROOT.TFile.Open(outFileURL,'RECREATE')
    for key in histos: histos[key].Write()
    bazinga('about to close Out file')
    fOut.Close()
    


def main():

    #configuration
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option('-i', '--input',		 dest='input',		 help='inputfile',   default=None,		   type='string')
    parser.add_option('-o', '--outDir',		 dest='outDir',		 help='output directory',			  default='zBosonPlots',  type='string')
   
    (opt, args) = parser.parse_args()

    fileWithTree = '%s' % (opt.input)
    
    #prepare output
    if len(opt.outDir) is None: opt.outDir='./'
    os.system('mkdir -p %s' % opt.outDir) #overwrite if exists
    fileout = '%s/zPlots.root' % (opt.outDir)

    plot(fileWithTree, fileout)
    print '\nAnalysis results are available in %s' % opt.outDir
    #exit(0)
    


"""
for execution from another script
"""
if __name__ == "__main__":

    start_time = time.time()
    main()
    end_time = time.time()
    time_taken = end_time - start_time # time_taken is in seconds
    hours, rest = divmod(time_taken,3600)
    minutes, seconds = divmod(rest, 60)
    print "---it took {hours} hours, {minutes} minutes and {seconds:.1f} seconds to run the analysis ---".format (hours=hours, minutes=minutes, seconds=seconds)

