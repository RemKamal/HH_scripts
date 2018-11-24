from ROOT import *
from tdrStyle import *
setTDRStyle()
import subprocess
import json
import os, sys, glob
from array import array
import pprint as pp

trueRun = True
copyHiggsROOTfiles = True
logY = True

date = 'dec17'

doFullHH = True
addTheoryCurve = False

if doFullHH:
    yaxis_title = '95% CL limit on #sigma(pp #rightarrow X, spin-2 #rightarrow hh)) [pb]' #to have a full HH
    mult_limit_by = 1
else:
    yaxis_title = '95% CL limit on #sigma(pp #rightarrow X, spin-2 #rightarrow hh)x BR(hh #rightarrow b#bar{b}VV #rightarrow b#bar{b}ll#nu#nu) [fb]'
    mult_limit_by = 1000.*(0.0012+0.0266) # to have in 'fb' for bbVV
#'#sigma/#sigma_{Theory}'

bbllnunu_BF = (0.0012+0.0266) 

# '/' at the end of the line is VERY important!
dirROOTfiles = 'combinedCards_'#/afs/cern.ch/user/r/rkamalie/workspace/private/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/test/mytest/newCRTT_july9_ZHtests/1pb_noBDTcut_inCRs_Zm15p15_Hm35p25/low_SR_0.5/plots/makeDataCards/'
                       #/afs/cern.ch/user/r/rkamalie/workspace/private/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/test/mytest/june21/low_SR_0.5/plots/makeDataCards/'
dirROOTfiles_high = 'logs_'#/afs/cern.ch/user/r/rkamalie/workspace/private/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/test/mytest/newCRTT_july9_ZHtests/1pb_noBDTcut_inCRs_Zm15p15_Hm35p25/high_SR_0.95/plots/makeDataCards/'
#/afs/cern.ch/user/r/rkamalie/workspace/private/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/test/mytest/june21/high_SR_0.95/plots/makeDataCards/'

masses = [260, 270, 300, 350, 400, 450, 451, 600, 650, 900, 1000]
 
if copyHiggsROOTfiles:
    for mass in masses:
        #dirROOTfiles = dirROOTfiles_low if mass <= 450 else dirROOTfiles_high
        cpCommand = 'cp ' + dirROOTfiles + str(mass) + '_dec17/higgs*Asym*root .'
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
    if int(m) in masses:
        unsortedmass.append(float(m))

unsortedmass.sort()
print 'unsortedmass is', unsortedmass

debugMode = False # for priting with bazinga                                                                                                             
def bazinga (mes):
    if debugMode:
        print mes



for m in unsortedmass:
    
    mass.append(m)

    f = TFile("higgsCombineTest.Asymptotic.mH"+str(m).replace('.0','')+".root","READ")
    t = f.Get("limit")
    #t.Print()

    zeros.append(0.0)
    
    t.GetEntry(2)
    thisexp = t.limit
    bazinga('thisexp expected is {0}'.format(thisexp) )
    exp.append(thisexp)
    if m == 450 or m == 451:
        print 'thisexp expected is {0} for mass={1} using file {2}'.format(thisexp, m, f) 
    
    t.GetEntry(0)
    bazinga('"thisexp-t.limit" m2 is {0}'.format(thisexp-t.limit) )
    exp_m2.append(thisexp-t.limit)

    t.GetEntry(1)
    bazinga('"thisexp-t.limit" m1 is {0}'.format(thisexp-t.limit) )
    exp_m1.append(thisexp-t.limit)

    t.GetEntry(3)
    bazinga('"t.limit-thisexp" p1 is {0}'.format(t.limit-thisexp) )
    exp_p1.append(t.limit-thisexp)

    t.GetEntry(4)
    bazinga('"t.limit-thisexp" p2 is {0}'.format(t.limit-thisexp) )
    exp_p2.append(t.limit-thisexp)

    t.GetEntry(5)
    bazinga('t.limit obs is {0}'.format(t.limit) )
    obs.append(t.limit)



if mult_limit_by > 1.:

    zeros = array('d',[x * mult_limit_by for x in zeros])
    exp_p2 = array('d',[x * mult_limit_by for x in exp_p2])
    exp_p1 = array('d',[x * mult_limit_by for x in exp_p1])
    
    exp = array('d',[x * mult_limit_by for x in exp])
    exp_m1 = array('d',[x * mult_limit_by for x in exp_m1])
    exp_m2 = array('d',[x * mult_limit_by for x in exp_m2])
    obs = array('d',[x * mult_limit_by for x in obs])
    

print 'mass array is', mass

mass_high = mass[-5:]
zeros_high = zeros[-5:]
exp_p2_high = exp_p2[-5:]
exp_p1_high = exp_p1[-5:]

exp_high = exp[-5:]
exp_m1_high =  exp_m1[-5:]
exp_m2_high = exp_m2[-5:]
obs_high = obs[-5:]

mass_high[0] = 450.

mass_low = mass[:6]
zeros_low = zeros[:6]
exp_p2_low = exp_p2[:6]
exp_p1_low = exp_p1[:6]

exp_low = exp[:6]
exp_m1_low =  exp_m1[:6]
exp_m2_low = exp_m2[:6]
obs_low = obs[:6]



print 'high mass is', mass_high
print 'high zeros is ', zeros_high
print 'high exp_p2 is ', exp_p2_high
print 'high exp_p1 is', exp_p1_high
print 'high exp is', exp_high
print 'high exp_m1 is', exp_m1_high
print 'high exp_m2 is', exp_m2_high
print 'high obs is ', obs_high


print 'low mass is', mass_low
print 'low zeros is ', zeros_low
print 'low exp_p2 is ', exp_p2_low
print 'low exp_p1 is', exp_p1_low
print 'low exp is', exp_low
print 'low exp_m1 is', exp_m1_low
print 'low exp_m2 is', exp_m2_low
print 'low obs is ', obs_low

print '*'*100

print 'mass is', mass
print 'zeros is ', zeros
print 'exp_p2 is ', exp_p2
print 'exp_p1 is', exp_p1
print 'exp is', exp
print 'exp_m1 is', exp_m1
print 'exp_m2 is', exp_m2
print 'obs is ', obs

print 'mult_limit_by is', mult_limit_by

f = open('expLimits_HH_low.txt' if doFullHH else 'expLimits_bbZZ_low.txt', 'w')
json.dump(list(exp_low), f)
f.close()

f = open('expLimits_HH_high.txt' if doFullHH else 'expLimits_bbZZ_high.txt', 'w')
json.dump(list(exp_high), f)
f.close()


v_mass = TVectorD(len(mass),mass)
v_zeros = TVectorD(len(zeros),zeros)
v_exp_p2 = TVectorD(len(exp_p2),exp_p2)
v_exp_p1 = TVectorD(len(exp_p1),exp_p1)
v_exp = TVectorD(len(exp),exp)
v_exp_m1 = TVectorD(len(exp_m1),exp_m1)
v_exp_m2 = TVectorD(len(exp_m2),exp_m2)
v_obs = TVectorD(len(obs),obs)



v_mass_high = TVectorD(len(mass_high),mass_high)
v_zeros_high = TVectorD(len(zeros_high),zeros_high)
v_exp_p2_high = TVectorD(len(exp_p2_high),exp_p2_high)
v_exp_p1_high = TVectorD(len(exp_p1_high),exp_p1_high)
v_exp_high = TVectorD(len(exp_high),exp_high)
v_exp_m1_high = TVectorD(len(exp_m1_high),exp_m1_high)
v_exp_m2_high = TVectorD(len(exp_m2_high),exp_m2_high)
v_obs_high = TVectorD(len(obs_high),obs_high)


v_mass_low = TVectorD(len(mass_low),mass_low)
v_zeros_low = TVectorD(len(zeros_low),zeros_low)
v_exp_p2_low = TVectorD(len(exp_p2_low),exp_p2_low)
v_exp_p1_low = TVectorD(len(exp_p1_low),exp_p1_low)
v_exp_low = TVectorD(len(exp_low),exp_low)
v_exp_m1_low = TVectorD(len(exp_m1_low),exp_m1_low)
v_exp_m2_low = TVectorD(len(exp_m2_low),exp_m2_low)
v_obs_low = TVectorD(len(obs_low),obs_low)


c = TCanvas("c","c",800, 800)
c.SetGridx()
c.SetGridy()

c.SetRightMargin(0.06)
c.SetLeftMargin(0.2)

if logY:
     c.SetLogy()

dummy = TH1D("dummy","dummy", 1, 250,1050)
dummy.SetBinContent(1,0.0)
dummy.GetXaxis().SetTitle('m_{X, spin-2} [GeV]')   
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

maxValue = 1100000 if not doFullHH else 40000 if doFullHH  else 0
if not addTheoryCurve:
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


low_gr_exp2 = TGraphAsymmErrors(v_mass_low,v_exp_low,v_zeros_low,v_zeros_low,v_exp_m2_low,v_exp_p2_low)
low_gr_exp2.SetLineColor(kYellow)
low_gr_exp2.SetFillColor(kYellow)
low_gr_exp2.Draw("e3same")

low_gr_exp1 = TGraphAsymmErrors(v_mass_low,v_exp_low,v_zeros_low,v_zeros_low,v_exp_m1_low,v_exp_p1_low)
low_gr_exp1.SetLineColor(kGreen)
low_gr_exp1.SetFillColor(kGreen)
low_gr_exp1.Draw("e3same")

low_gr_exp = TGraphAsymmErrors(v_mass_low,v_exp_low,v_zeros_low,v_zeros_low,v_zeros_low,v_zeros_low)
low_gr_exp.SetLineColor(1)
low_gr_exp.SetLineWidth(2)
low_gr_exp.SetLineStyle(2)
low_gr_exp.Draw("Lsame")


high_gr_exp2 = TGraphAsymmErrors(v_mass_high,v_exp_high,v_zeros_high,v_zeros_high,v_exp_m2_high,v_exp_p2_high)
high_gr_exp2.SetLineColor(kYellow)
high_gr_exp2.SetFillColor(kYellow)
high_gr_exp2.Draw("e3same")

high_gr_exp1 = TGraphAsymmErrors(v_mass_high,v_exp_high,v_zeros_high,v_zeros_high,v_exp_m1_high,v_exp_p1_high)
high_gr_exp1.SetLineColor(kGreen)
high_gr_exp1.SetFillColor(kGreen)
high_gr_exp1.Draw("e3same")

high_gr_exp = TGraphAsymmErrors(v_mass_high,v_exp_high,v_zeros_high,v_zeros_high,v_zeros_high,v_zeros_high)
high_gr_exp.SetLineColor(1)
high_gr_exp.SetLineWidth(2)
high_gr_exp.SetLineStyle(2)
high_gr_exp.Draw("Lsame")

#uncomment after unblinding

# gr_obs = TGraphAsymmErrors(v_mass,v_obs,v_zeros,v_zeros,v_zeros,v_zeros)
# gr_obs.SetLineColor(1)
# gr_obs.SetLineWidth(2)
# gr_obs.Draw("CPsame")





# if doFullHH: 
#     bbllnunu_BF = 1
# else:
#     bbllnunu_BF *= 1000

# bbzz_wed_mass_xsec_dict = {k:(v*bbllnunu_BF) for k,v in wed_mass_xsec_dict.items()}
# print 'bbzz_wed_mass_xsec_dict:'
# pp.pprint(bbzz_wed_mass_xsec_dict)

# wed_masses = [k for k,v in wed_mass_xsec_dict.items()]
# bbzz_wed_xsecs = [v for k,v in wed_mass_xsec_dict.items()]
wed_masses = [200, 260, 300, 400, 500, 600, 700, 750, 800, 900, 1000]

#https://github.com/CrossSectionsLHC/WED/blob/master/KKGraviton_RS1/GF_NLO_13TeV_ktilda_0p1.txt
rs1_wed_xsecs = [39275.98, 14445.39, 8033.67, 2481.79, 937.05, 415.62, 205.6, 146.43, 105.82, 60.5, 36.13]
rs1_wed_xsecs = [x*mult_limit_by for x in rs1_wed_xsecs]

#https://github.com/CrossSectionsLHC/WED/blob/master/KKGraviton_Bulk/GF_NLO_13TeV_ktilda_0p1.txt
bulk_wed_xsecs = [11.4356, 3.3956, 1.7849, 0.4827, 0.1752, 0.0735, 0.035, 0.0249, 0.0182, 0.0098, 0.0057]
bulk_wed_xsecs = [x*mult_limit_by for x in bulk_wed_xsecs]



print 'wed_masses:'
pp.pprint(wed_masses)
print
print 'rs1_wed_xsecs:'
pp.pprint(rs1_wed_xsecs)
print
print 'bulk_wed_xsecs:'
pp.pprint(bulk_wed_xsecs)

nPoints = len(wed_masses)
tgr_RS1 = ROOT.TGraph(nPoints, array('f', wed_masses), array('f', rs1_wed_xsecs) )

tgr_RS1.SetLineColor(2)
tgr_RS1.SetLineWidth(2)
if addTheoryCurve:
    tgr_RS1.Draw("Lsame")

tgr_Bulk = ROOT.TGraph(nPoints, array('f', wed_masses), array('f', bulk_wed_xsecs) )

tgr_Bulk.SetLineColor(4)
tgr_Bulk.SetLineWidth(2)
if addTheoryCurve:
    tgr_Bulk.Draw("Lsame")

# tgr.SetLineColor(2)
# tgr.SetMarkerColor(2)
# tgr.SetMarkerStyle(20)
# tgr.Draw("pz")



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
latex2.DrawLatex(0.2, 0.95, "CMS preliminary") #"Work in progress")
#latex2.DrawLatex(0.3, 0.85, "CMS")


legend = TLegend(.60,.70,.90,.90)
#legend.AddEntry(gr_obs , "Observed 95% CL", "l")
legend.AddEntry(low_gr_exp , "Expected 95% CL", "l")
legend.AddEntry(low_gr_exp1 , "#pm 1#sigma", "f")
legend.AddEntry(low_gr_exp2 , "#pm 2#sigma", "f")
if addTheoryCurve:
    legend.AddEntry(tgr_RS1, "RS1 KK-graviton","l");
    legend.AddEntry(tgr_Bulk, "Bulk KK-graviton","l");

legend.SetShadowColor(0)
legend.SetFillColor(0)
legend.SetLineColor(0)            
legend.Draw("same")
                                                            
gPad.RedrawAxis()

for ext in ['.png', '.pdf', '.root']:
    name = 'limitHH_' if doFullHH else 'limitbbZZ_'
    c.SaveAs(name + date + ext)

raw_input("Press Enter to continue...")
