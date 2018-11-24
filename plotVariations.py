import ROOT
import sys
#from ROOT import TColor

modifyShapes = False
drawPlots = True
savePlots = True
createRootFiles = True
signal_mult_factor = 50000
inpFiles = [
 
    "hhMt_ee_CRDY.input.root",
    #"hhMt_ee_CRTT.input.root",
    #"hhMt_ee_SR.input.root",
    #"hhMt_mm_CRDY.input.root",
    #"hhMt_mm_CRTT.input.root",
    #"hhMt_mm_SR.input.root"
]

systUnderStudy = [
    'CMS_eff_met_UnclusteredEn',
    #'CMS_scale_j',
    #'CMS_res_j',
    #'CMS_eff_met_JetEn',
    #'CMS_btag_heavy',
    #'CMS_btag_light',
    
    #'CMS_pu'

    ]


#systName = 'CMS_eff_met_UnclusteredEn'


processes = ['ST', 'TT', 'DY', 'ZH', 'VV', 'signal_hzz', 'signal_hww']
#processes = ['TT']


def drawNplot(hists, canvName):
    
    ROOT.gStyle.SetOptStat(0)
    
    c = ROOT.TCanvas()
    leg = ROOT.TLegend(.45, .6, .73, .73)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetTextFont(42)
    leg.SetTextSize(0.035)

    if drawPlots:
        for idx, h in enumerate(hists):
            if idx == 0:
                h.Draw()
            else:
                print 'working with', h.GetName()
                if h:
                    h.Draw("same")
            if h:
                leg.AddEntry(h, h.GetName(), "L")
            c.Modified()
            c.Update()

    if drawPlots:
        leg.Draw()

    t = ROOT.TLatex()
    t.SetTextFont(22)
    t.SetTextColor(1)
    t.SetTextSize(0.04)
    t.SetTextAlign(12)
            # t.DrawLatex( .1, .9, 'CMS Preliminary')
    if drawPlots:
        t.DrawLatexNDC(.1, .92, 'CMS Preliminary')

            # unnecessary?
            # c.Draw()



        
            # print canvName
    outputName = canvName[:-4].replace('.', '_')
    for format in ['.png', '.pdf', '.root', '.C']:
        if savePlots:
            c.SaveAs(outputName + format)
        else:
            pass





def makeplots(systName):

    for fil in inpFiles:
        totalHistsprinted = False
        for process in processes:
            #if 'TT' not in process: continue
            f_input_shapes_TH1 = ROOT.TFile(fil)
            f_input_shapes_TH1.ls()
            region = f_input_shapes_TH1.GetName()[8:-11]
            typ = f_input_shapes_TH1.GetName()[5:7]
            innerDirName = typ + '_' + region
            syst = process + '_' + systName
            print "name=%s, process=%s, region=%s, typ=%s, innerDirName=%s, syst=%s" % (f_input_shapes_TH1.GetName(), process, region, typ, innerDirName, syst)
            f_input_shapes_TH1.cd(innerDirName)
            # print '8'*50
            #f_input_shapes_TH1.ls()
            # print 'syst is', syst
            shapes = ROOT.gDirectory.GetListOfKeys()
            # print 'shapes are', shapes
            hists = []
            for idx, shape in enumerate(shapes):
                shape = ROOT.gDirectory.Get(shapes[idx].GetName())
                # print 'before draw'
                #shape.Print()
                # print shape.GetName()
                # print shape.GetTitle()
                shape.SetTitle('')
                hists.append(shape)

            clones = [x.Clone() for x in hists]
            
            BGhists = [x.Clone() for x in hists if 'sig' not in x.GetName() and 'data' not in x.GetName() and '_' not in x.GetName()]
            BGhistsUp = [x.Clone() for x in hists if 'sig' not in x.GetName() and 'data' not in x.GetName() and 'Up' in x.GetName()]
            BGhistsDown = [x.Clone() for x in hists if 'sig' not in x.GetName() and 'data' not in x.GetName() and 'Down' in x.GetName()]
            
            SIGhists = [x.Clone() for x in hists if 'sig' in x.GetName() and 'data' not in x.GetName() and 'hww_' not in x.GetName() and 'hzz_' not in x.GetName()]
            SIGhistsUp = [x.Clone() for x in hists if 'sig' in x.GetName() and 'data' not in x.GetName() and ('hww_' in x.GetName() or 'hzz_' in x.GetName()) and 'Up' in x.GetName()]
            SIGhistsDown = [x.Clone() for x in hists if 'sig' in x.GetName() and 'data' not in x.GetName() and ('hww_' in x.GetName() or 'hzz_' in x.GetName()) and 'Down' in x.GetName()]
            
            print '~'*100
            for x in BGhists, BGhistsUp, BGhistsDown, SIGhists, SIGhistsUp, SIGhistsDown:
                print x
            print '~'*100
            #print 'BGhists', BGhists
            #print 'sighists', sighists
            #BGhist_first = BGhists[0] 
            #sighist_first = sighists[0]
 

            
            





            #print 'clones', clones
            #clones = [x.SetDirectory(0) for x in clones]

            #print 'clones', clones
            TThists = [x for x in hists if x.GetName() == 'TT_CMS_eff_met_UnclusteredEnUp' ]# and 'UnclusteredUp' in x.GetName()]
            print TThists
            if len(TThists) > 0: print TThists[0].GetBinContent(34)
            #print 'hists', hists
            #print '7'*500
            #print hists
            #sys.exit(1)
            
            h_background = filter(lambda x: x.GetName() == process, clones)
            print 'h_background=', h_background
            if h_background == []:
                continue
            h_background = filter(lambda x: x.GetName() == process, clones)[0]
            # print 'h_background is', h_background
            h_background.SetLineColor(1)

            h_background_alphaUp = filter(lambda x: x.GetName() == syst + "Up", clones)[0]
            h_background_alphaUp.SetLineColor(2)

            h_background_alphaDown = filter(lambda x: x.GetName() == syst + "Down", clones)[0]
            h_background_alphaDown.SetLineColor(4)
            print '*'*100
            print 'integrals for h_background_alphaDown, h_background, h_background_alphaUp', h_background_alphaDown.Integral(), h_background.Integral(), h_background_alphaUp.Integral()






            
            totBGh, totBGhUp, totBGDown, totSIGh, totSIGhUp, totSIGhDown  = None, None, None, None, None, None
            print 'totBGh, totBGhUp, totBGDown, totSIGh, totSIGhUp, totSIGhDown', totBGh, totBGhUp, totBGDown, totSIGh, totSIGhUp, totSIGhDown
            print 'BGhists', BGhistsDown
            for idx, (h, hd, hu) in enumerate(zip(BGhists, BGhistsDown, BGhistsUp)):
                print 'doing BG'
                print hd
                print 'systName', systName
                print 'hd.GetName()', hd.GetName()
                if systName not in hd.GetName(): continue # or systName not in hu.GetName(): continue
                if not totalHistsprinted:
                    print ''*1000
                    print 'inside if'
                    print h.Integral(), h
                    print hu.Integral(), hu
                    print hd.Integral(), hd
                if totBGh == None:
                    totBGh = h
                    totBGh.SetLineColor(ROOT.kBlack)
                    totBGhUp = hu
                    totBGhUp.SetLineColor(ROOT.kGray)
                    totBGDown = hd
                    totBGDown.SetLineColor(ROOT.kBrownCyan)
                    totBGh.SetName('total BG')
                    totBGhUp.SetName('total BG Up')
                    totBGDown.SetName('total BG Down')
                else:
                    totBGh.Add(h)
                    totBGhUp.Add(hu)
                    totBGDown.Add(hd)
#            sys.exit(1)
            for idx, (h, hd, hu) in enumerate(zip(SIGhists, SIGhistsDown, SIGhistsUp)):
                print 'doing signal'
                print hd
                if systName not in hd.GetName(): continue
                if totSIGh == None:
                    totSIGh = h
                    totSIGh.SetLineColor(ROOT.kBlue)
                    totSIGhUp = hu
                    totSIGhUp.SetLineColor(ROOT.kRed)
                    totSIGhDown = hd
                    totSIGhDown.SetLineColor(ROOT.kMagenta)

                    totSIGh.Scale(signal_mult_factor)
                    totSIGh.SetName('total SIG x {0}'.format(signal_mult_factor)) 
                    totSIGhDown.Scale(signal_mult_factor)
                    totSIGhDown.SetName('total SIG Down x {0}'.format(signal_mult_factor)) 
                    totSIGhUp.Scale(signal_mult_factor)
                    totSIGhUp.SetName('total SIG Up x {0}'.format(signal_mult_factor)) 
                else:
                    totSIGh.Add(h)
                    totSIGhUp.Add(hu)
                    totSIGhDown.Add(hd)


            print 'totBGh, totBGhUp, totBGDown, totSIGh, totSIGhUp, totSIGhDown', totBGh, totBGhUp, totBGDown, totSIGh, totSIGhUp, totSIGhDown


            for idx, (binDown, binNom, binUp) in enumerate(zip(h_background_alphaDown, h_background, h_background_alphaUp)):
                #content_binDown = 
                #content_binNom  =
                #content_binUp   =
                #print 'binDown={0}, binNom={1}, binUp={2}'.format(binDown, binNom, binUp)
                minBinValue, maxBinValue = min([binDown, binNom, binUp]), max([binDown, binNom, binUp])
                binDownErr, binNomErr, binUpErr = h_background_alphaDown.GetBinError(idx), h_background.GetBinError(idx), h_background_alphaUp.GetBinError(idx)

                #deal with (from top to bottom) +~- or -~+ cases, which are just asymmetric, do not address onesided cases here
                weight = h_background.GetBinContent(idx)/h_background.GetEntries() if h_background.GetEntries() != 0 else 0
                if weight==0:
                    continue
                fixIsMade = False
                

    #if modifyShapes:
                # if binDown <= binNom <= binUp: #correct sequence
                #     pos_diff = binUp - binNom
                #     neg_diff = binNom - binDown
                #     print 'fixing the asymetric error in case +~-'
                #     print 'binUp={0}, binNom={1}, binDown={2}'.format(binUp, binNom, binDown)
                #     if pos_diff > neg_diff: #e.g. up=7, nom=4, down=3 
                #         h_background_alphaDown.SetBinContent(idx, binNom - pos_diff if binNom - pos_diff > 0 else 0)#weight)
                #     else:
                #         h_background_alphaUp.SetBinContent(idx, binNom + neg_diff)
                #     fixIsMade= True
                        
                # elif binDown >= binNom >= binUp:
                #     upper_diff = binDown - binNom 
                #     lower_diff = binNom - binUp
                #     print 'the asymetric error FIX in case -~+'
                #     print 'binDown={0}, binNom={1}, binUp={2}'.format(binDown, binNom, binUp)
                #     if upper_diff > lower_diff:
                #         h_background_alphaUp.SetBinContent(idx, binNom - upper_diff if binNom - upper_diff >0 else 0)#weight)
                #     else:
                #         h_background_alphaDown.SetBinContent(idx, binNom + lower_diff)
                #     fixIsMade= True

                # #address here the case of both up and down are below, ~-+ or ~+-, more specifically, first work on the 'worst'?-> ~-+
                # if binNom >= binDown >= binUp: 
                #     pos_diff = binNom - binUp
                #     neg_diff = binNom - binDown
                #     h_background_alphaUp.SetBinContent(idx, binNom + neg_diff)
                #     fixIsMade= True

                # #now work on the case ~+-
                # if binNom >= binUp >= binDown:
                #     pos_diff = binNom - binUp
                #     neg_diff = binNom - binDown
                #     h_background_alphaUp.SetBinContent(idx, binNom + neg_diff)
                #     fixIsMade= True



                # #address here the case of both up and down are above, +-~ or -+~, more specifically, first work on the 'worst'?-> -+~
                # if binDown >= binUp >= binNom:
                #     pos_diff = binUp - binNom 
                #     neg_diff = binDown - binNom
                #     h_background_alphaDown.SetBinContent(idx, binNom - pos_diff if binNom - pos_diff > 0 else 0)
                #     fixIsMade= True

                # #now work on the the case +-~ 
                # if binUp >= binDown >= binNom:
                #     pos_diff = binUp - binNom
                #     neg_diff = binDown - binNom
                #     h_background_alphaDown.SetBinContent(idx, binNom - pos_diff if binNom - pos_diff > 0 else 0)
                #     fixIsMade= True


                if fixIsMade == True:
                    print 'after modification of bins'
                    print 'bin number={0}, bin position={1}'.format(idx, h_background.GetBinCenter(idx))
                    print 'cont in low={0}, cont in nom={1}, cont in up={2}'.format(h_background_alphaDown.GetBinContent(idx), h_background.GetBinContent(idx), h_background_alphaUp.GetBinContent(idx)  )
                    print

                if idx == 34:
                    pass
                    print 'in the loop'
                    print h_background_alphaUp.GetBinContent(idx)
                        
            #just in case???
            for h in clones:
                if h.GetName() == h_background.GetName():
                    h = h_background
                elif h.GetName() == h_background_alphaDown.GetName():
                    h = h_background_alphaDown
                elif h.GetName() == h_background_alphaUp.GetName():
                    h = h_background_alphaUp
                else:
                    pass

            modifiedTThists = [x for x in clones if x.GetName() == 'TT_CMS_eff_met_UnclusteredEnUp' ]# and 'UnclusteredUp' in x.GetName()]                           
            print modifiedTThists
            if len(modifiedTThists) > 0: print modifiedTThists[0].GetBinContent(34)

            if createRootFiles:
            #inp = ROOT.TFile.Open(inputfile,'read')                                                                       
                output = ROOT.TFile.Open(f_input_shapes_TH1.GetName()[:-5] + '_copy.root','recreate')
                output.mkdir(innerDirName)
                output.cd(innerDirName)
                for h in clones:
                    h.Write()#key.GetName())                                                                                       
                output.Close()
                #   output_tree.GetCurrentFile().Write()?????

            canvName = f_input_shapes_TH1.GetName()[:-4] + syst + '.png'
            listofhists = [h_background_alphaDown, h_background, h_background_alphaUp]
            drawNplot(listofhists, canvName)

            if not totalHistsprinted:
                print 'totBGDown.Integral(), totBGh.Integral(), totBGhUp.Integral()', totBGDown.Integral(), totBGh.Integral(), totBGhUp.Integral()
                drawNplot([totBGh, totBGhUp, totBGDown, totSIGh, totSIGhUp, totSIGhDown], 'total_' + canvName)
                totalHistsprinted = True
            
            i = 1
            print 'saving canvas #', i
            print "for hist = %s, central = %s, alpha up = %g, alpha down = %g" % (
            h_background.GetName(), h_background.Integral(), h_background_alphaUp.Integral(),
            h_background_alphaDown.Integral())
            i += 1




def main():
    for systName in systUnderStudy:
        print "doing %s" % systName
        makeplots(systName)

if __name__ == '__main__':
    sys.exit(main())

# f_shapes_TH1 = ROOT.TFile("simple-shapes-TH1.root","READ")
# w_shapes_TH1 = f_shapes_TH1.Get("w")
# w_shapes_TH1.Print()


# shapeBkg = w_shapes_TH1.pdf("shapeBkg_bin1_background_morph")
# th1x = w_shapes_TH1.var("CMS_th1x")
# plot_th1x = th1x.frame()
# alpha = w_shapes_TH1.var("alpha")
# alpha.setVal(0.0)
# shapeBkg.plotOn(plot_th1x,ROOT.RooFit.LineColor(1))
# alpha.setVal(0.5)
# shapeBkg.plotOn(plot_th1x,ROOT.RooFit.LineColor(3))
# alpha.setVal(1.0)
# shapeBkg.plotOn(plot_th1x,ROOT.RooFit.LineColor(2))
# alpha.setVal(2.0)
# shapeBkg.plotOn(plot_th1x,ROOT.RooFit.LineColor(6))

# c2 = ROOT.TCanvas()
# plot_th1x.Draw()
# c2.Draw()


