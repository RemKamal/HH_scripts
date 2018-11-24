from ROOT import *
from tdrStyle import *
setTDRStyle()
import subprocess
import json
import os, sys, glob
from array import array


trueRun = True
copyHiggsROOTfiles = True
logY = True

date = 'oct31'

doFullHH = True


if doFullHH:
    yaxis_title = '95% CL limit on #sigma(pp #rightarrow BGrav #rightarrow hh)) [pb]' #to have a full HH
    mult_limit_by = 1
else:
    yaxis_title = '95% CL limit on #sigma(pp #rightarrow BGrav #rightarrow hh)x BR(hh #rightarrow b#bar{b}VV #rightarrow b#bar{b}#mu#mu#nu#nu) [fb]'
    mult_limit_by = 1000.*(0.0012+0.0266) # to have in 'fb' for bbVV
#'#sigma/#sigma_{Theory}'


# '/' at the end of the line is VERY important!
dirROOTfiles = 'combinedCards_'#/afs/cern.ch/user/r/rkamalie/workspace/private/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/test/mytest/newCRTT_july9_ZHtests/1pb_noBDTcut_inCRs_Zm15p15_Hm35p25/low_SR_0.5/plots/makeDataCards/'
                       #/afs/cern.ch/user/r/rkamalie/workspace/private/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/test/mytest/june21/low_SR_0.5/plots/makeDataCards/'
dirROOTfiles_high = 'logs_'#/afs/cern.ch/user/r/rkamalie/workspace/private/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/test/mytest/newCRTT_july9_ZHtests/1pb_noBDTcut_inCRs_Zm15p15_Hm35p25/high_SR_0.95/plots/makeDataCards/'
#/afs/cern.ch/user/r/rkamalie/workspace/private/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/test/mytest/june21/high_SR_0.95/plots/makeDataCards/'

masses = [260, 270, 300, 350, 400, 450, 600, 650, 900, 1000]
 
if copyHiggsROOTfiles:
    for mass in masses:
        #dirROOTfiles = dirROOTfiles_low if mass <= 450 else dirROOTfiles_high
        cpCommand = 'cp ' + dirROOTfiles + str(mass) + '/higgs*root .'
        print cpCommand
        if trueRun:
            subprocess.call(cpCommand, shell=True)


#sys.exit(1)
unsortedmass = []

mass = array('d',[])
zeros = array('d',[])
exp_p2 = array('d',[])
exp_p1 = array('d',[])

exp = array('d',[])
exp_m1 = array('d',[])
exp_m2 = array('d',[])
obs = array('d',[])


files=glob.glob("higgsCombineTest.Asymptotic.mH*.root")
print 'files is', files
for afile in files:
    m = afile.split('mH')[1].replace('.root','')    
    unsortedmass.append(float(m))

unsortedmass.sort()
print 'unsortedmass is', unsortedmass

debugMode = True # for priting with bazinga                                                                                                             
def bazinga (mes):
    if debugMode:
        print mes



for m in unsortedmass:
    
    mass.append(m)

    f = TFile("higgsCombineTest.Asymptotic.mH"+str(m).replace('.0','')+".root","READ")
    t = f.Get("limit")
    t.Print()

    zeros.append(0.0)
    
    t.GetEntry(2)
    thisexp = t.limit
    bazinga('thisexp is {0}'.format(thisexp) )
    exp.append(thisexp)
    
    t.GetEntry(0)
    bazinga('"thisexp-t.limit" is {0}'.format(thisexp-t.limit) )
    exp_m2.append(thisexp-t.limit)

    t.GetEntry(1)
    bazinga('"thisexp-t.limit" is {0}'.format(thisexp-t.limit) )
    exp_m1.append(thisexp-t.limit)

    t.GetEntry(3)
    bazinga('"t.limit-thisexp" is {0}'.format(t.limit-thisexp) )
    exp_p1.append(t.limit-thisexp)

    t.GetEntry(4)
    bazinga('"t.limit-thisexp" is {0}'.format(t.limit-thisexp) )
    exp_p2.append(t.limit-thisexp)

    t.GetEntry(5)
    bazinga('t.limit is {0}'.format(t.limit) )
    obs.append(t.limit)



if mult_limit_by > 1.:

    zeros = array('d',[x * mult_limit_by for x in zeros])
    exp_p2 = array('d',[x * mult_limit_by for x in exp_p2])
    exp_p1 = array('d',[x * mult_limit_by for x in exp_p1])
    
    exp = array('d',[x * mult_limit_by for x in exp])
    exp_m1 = array('d',[x * mult_limit_by for x in exp_m1])
    exp_m2 = array('d',[x * mult_limit_by for x in exp_m2])
    obs = array('d',[x * mult_limit_by for x in obs])
    

print 'mass is', mass
print 'zeros is ', zeros
print 'exp_p2 is ', exp_p2
print 'exp_p1 is', exp_p1
print 'exp is', exp
print 'exp_m1 is', exp_m1
print 'exp_m2 is', exp_m2
print 'obs is ', obs

print 'mult_limit_by is', mult_limit_by

f = open('expLimits_HH.txt', 'w')
json.dump(list(exp), f)
f.close()

v_mass = TVectorD(len(mass),mass)
v_zeros = TVectorD(len(zeros),zeros)
v_exp_p2 = TVectorD(len(exp_p2),exp_p2)
v_exp_p1 = TVectorD(len(exp_p1),exp_p1)
v_exp = TVectorD(len(exp),exp)
v_exp_m1 = TVectorD(len(exp_m1),exp_m1)
v_exp_m2 = TVectorD(len(exp_m2),exp_m2)
v_obs = TVectorD(len(obs),obs)

c = TCanvas("c","c",800, 800)
c.SetGridx()
c.SetGridy()

c.SetRightMargin(0.06)
c.SetLeftMargin(0.2)

if logY:
     c.SetLogy()

dummy = TH1D("dummy","dummy", 1, 250,1050)
dummy.SetBinContent(1,0.0)
dummy.GetXaxis().SetTitle('m(BulkGraviton) [GeV]')   
dummy.GetYaxis().SetTitle(yaxis_title)   
dummy.GetYaxis().CenterTitle()   
dummy.SetLineColor(0)
dummy.SetLineWidth(0)
dummy.SetFillColor(0)
#HAVE TO HAVE non-zero value if logY is USED!!!!!!!!!!!
minVal = 20 if not doFullHH else 1 if doFullHH else 0 # to exit

if minVal ==0 and logY:
    print 'check minVal'
    sys.exit(1)
dummy.SetMinimum(minVal)
histMax = dummy.GetMaximum()

maxValue = 22000 if not doFullHH else 1700 if doFullHH  else 0

if minVal ==0 or maxValue ==0:
    print 'check min/max Val'
    sys.exit(1)

dummy.SetMaximum(maxValue)
#dummy.GetYaxis().SetTitleSize(0.04)
dummy.GetYaxis().SetLabelSize(0.035)
dummy.GetXaxis().SetLabelSize(0.03)
dummy.SetTitleSize( 0.03, "Y" ); 
dummy.SetTitleSize( 0.04, "X" ); 
dummy.SetTitleOffset(2.45, "Y") 
dummy.Draw()


  # h->SetXTitle("x axis label");  h->SetYTitle("y axis label");
  # h->SetTitleSize( 0.08, "X" ); h->SetTitleOffset(0.01, "X");
  # h->SetTitleSize( 0.08, "Y" ); h->SetTitleOffset(0.01, "Y");
  # h->SetLabelSize( 0.08, "X" ); h->SetLabelOffset(0.01, "X");
  # h->SetLabelSize( 0.08, "Y" ); h->SetLabelOffset(0.01, "Y");


gr_exp2 = TGraphAsymmErrors(v_mass,v_exp,v_zeros,v_zeros,v_exp_m2,v_exp_p2)
gr_exp2.SetLineColor(kYellow)
gr_exp2.SetFillColor(kYellow)
gr_exp2.Draw("e3same")

gr_exp1 = TGraphAsymmErrors(v_mass,v_exp,v_zeros,v_zeros,v_exp_m1,v_exp_p1)
gr_exp1.SetLineColor(kGreen)
gr_exp1.SetFillColor(kGreen)
gr_exp1.Draw("e3same")

gr_exp = TGraphAsymmErrors(v_mass,v_exp,v_zeros,v_zeros,v_zeros,v_zeros)
gr_exp.SetLineColor(1)
gr_exp.SetLineWidth(2)
gr_exp.SetLineStyle(2)
gr_exp.Draw("Lsame")

#uncomment after unblinding

# gr_obs = TGraphAsymmErrors(v_mass,v_obs,v_zeros,v_zeros,v_zeros,v_zeros)
# gr_obs.SetLineColor(1)
# gr_obs.SetLineWidth(2)
# gr_obs.Draw("CPsame")

latex2 = TLatex()
latex2.SetNDC()
latex2.SetTextSize(0.5*c.GetTopMargin())
latex2.SetTextFont(42)
latex2.SetTextAlign(31) # align right
latex2.DrawLatex(0.92, 0.95,"35.9 fb^{-1} (13 TeV)")
latex2.SetTextSize(0.9*c.GetTopMargin())
latex2.SetTextFont(52)
latex2.SetTextAlign(11) # align right

latex2.SetTextSize(0.5*c.GetTopMargin())
latex2.SetTextFont(42)
latex2.SetTextAlign(11)
latex2.DrawLatex(0.3, 0.8, "CMS preliminary") #"Work in progress")
#latex2.DrawLatex(0.3, 0.85, "CMS")


legend = TLegend(.60,.70,.90,.90)
#legend.AddEntry(gr_obs , "Observed 95% CL", "l")
legend.AddEntry(gr_exp , "Expected 95% CL", "l")
legend.AddEntry(gr_exp1 , "#pm 1#sigma", "f")
legend.AddEntry(gr_exp2 , "#pm 2#sigma", "f")
legend.SetShadowColor(0)
legend.SetFillColor(0)
legend.SetLineColor(0)            
legend.Draw("same")
                                                            
gPad.RedrawAxis()

for ext in ['.png', '.pdf', '.root']:
    c.SaveAs("limit_" + date + ext)

raw_input("Press Enter to continue...")
