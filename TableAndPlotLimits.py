from ROOT import *
from tdrStyle import *
setTDRStyle()
import subprocess
import json
import os, sys, glob, time
from array import array
import pprint as pp
import numpy as np
import re, io
import pickle, itertools
import pprint
pp = pprint.PrettyPrinter(indent=4)
pp = pprint.PrettyPrinter(depth=6)

trueRun = True
readStoredLimits = False

date = 'apr23'
curDir = os.getcwd()


copyHiggsROOTfiles = False
logY = True
masses = [260, 270, 300, 350, 400, 450,      451,       600, 650, 900, 1000]


#doFullHH = False 
doFullHH = True

addTheoryCurve = True

debugMode = False
def bazinga(mes):
    if debugMode:
        print mes


def plotLimit():
    bbllnunu_BF = (0.0012 + 0.0266)
    #https://stackoverflow.com/questions/13188476/get-the-nth-element-from-the-inner-list-of-a-list-of-lists-in-python
    if doFullHH:
        yaxis_title = '95% CL limit on #sigma(pp #rightarrow X, spin-2 #rightarrow hh)) [pb]'  # to have a full HH in pb
        mult_limit_by = 1
    else:
        yaxis_title = '95% CL limit on #sigma(pp #rightarrow X, spin-2 #rightarrow hh)x BR(hh #rightarrow b#bar{b}VV #rightarrow b#bar{b}ll#nu#nu) [fb]'
        mult_limit_by = 1000. * (bbllnunu_BF)  # to have in 'fb' for bbVV
    # '#sigma/#sigma_{Theory}'

    # '/' at the end of the line is VERY important!
    dirROOTfiles = 'combinedCards_'  # /afs/cern.ch/user/r/rkamalie/workspace/private/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/test/mytest/newCRTT_july9_ZHtests/1pb_noBDTcut_inCRs_Zm15p15_Hm35p25/low_SR_0.5/plots/makeDataCards/'
    # /afs/cern.ch/user/r/rkamalie/workspace/private/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/test/mytest/june21/low_SR_0.5/plots/makeDataCards/'
    #dirROOTfiles_high = 'logs_'  # /afs/cern.ch/user/r/rkamalie/workspace/private/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/test/mytest/newCRTT_july9_ZHtests/1pb_noBDTcut_inCRs_Zm15p15_Hm35p25/high_SR_0.95/plots/makeDataCards/'
    # /afs/cern.ch/user/r/rkamalie/workspace/private/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/test/mytest/june21/high_SR_0.95/plots/makeDataCards/'
    if copyHiggsROOTfiles:
        for mass in masses:
            # dirROOTfiles = dirROOTfiles_low if mass <= 450 else dirROOTfiles_high
            cpCommand = 'cp ' + dirROOTfiles + str(mass) + '/higgs*Asym*root .'
            print cpCommand
            if trueRun:
                subprocess.call(cpCommand, shell=True)

    # sys.exit(1)
    
         #To read it back:                                                                                                                                       
    if readStoredLimits:              
                with open ('combinedCards_limits.txt', 'rb') as fp:                                                                                           
                    itemlist = pickle.load(fp)                                                                                                                                            
                print 'itemlist'
                pprint.pprint(itemlist)

        


    unsortedmass = []
    mass = array('d', [])
    zeros = array('d', [])
    exp_p2 = array('d', [])
    exp_p1 = array('d', [])
    exp = array('d', [])
    exp_m1 = array('d', [])
    exp_m2 = array('d', [])
    obs = array('d', [])
    files = glob.glob("higgsCombineTest.Asymptotic.mH*.root")
    print 'files is', files
    for afile in files:
        m = afile.split('mH')[1].replace('.root', '')
        if int(m) in masses:
            unsortedmass.append(float(m))
    unsortedmass.sort()
    print 'unsortedmass is', unsortedmass
    debugMode = False  # for priting with bazinga


    for m in unsortedmass:

        mass.append(m)

        f = TFile("higgsCombineTest.Asymptotic.mH" + str(m).replace('.0', '') + ".root", "READ")
        t = f.Get("limit")
        # t.Print()

        zeros.append(0.0)

        t.GetEntry(2)
        thisexp = t.limit
        bazinga('thisexp expected is {0}'.format(thisexp))
        exp.append(thisexp)
        if m == 450 or m == 451:
            print 'thisexp expected is {0} for mass={1} using file {2}'.format(thisexp, m, f)

        t.GetEntry(0)
        bazinga('"thisexp-t.limit" m2 is {0}'.format(thisexp - t.limit))
        exp_m2.append(thisexp - t.limit)

        t.GetEntry(1)
        bazinga('"thisexp-t.limit" m1 is {0}'.format(thisexp - t.limit))
        exp_m1.append(thisexp - t.limit)

        t.GetEntry(3)
        bazinga('"t.limit-thisexp" p1 is {0}'.format(t.limit - thisexp))
        exp_p1.append(t.limit - thisexp)

        t.GetEntry(4)
        bazinga('"t.limit-thisexp" p2 is {0}'.format(t.limit - thisexp))
        exp_p2.append(t.limit - thisexp)

        t.GetEntry(5)
        bazinga('t.limit obs is {0}'.format(t.limit))
        obs.append(t.limit)






    if mult_limit_by > 1.:
        zeros = array('d', [x * mult_limit_by for x in zeros])
        exp_p2 = array('d', [x * mult_limit_by for x in exp_p2])
        exp_p1 = array('d', [x * mult_limit_by for x in exp_p1])

        exp = array('d', [x * mult_limit_by for x in exp])
        exp_m1 = array('d', [x * mult_limit_by for x in exp_m1])
        exp_m2 = array('d', [x * mult_limit_by for x in exp_m2])
        obs = array('d', [x * mult_limit_by for x in obs])
    print 'mass array is', mass
    mass_high = mass[-5:]
    zeros_high = zeros[-5:]
    exp_p2_high = exp_p2[-5:]
    exp_p1_high = exp_p1[-5:]
    exp_high = exp[-5:]
    exp_m1_high = exp_m1[-5:]
    exp_m2_high = exp_m2[-5:]
    obs_high = obs[-5:]
    print mass_high
    mass_high[0] = 450.
    mass_low = mass[:6]
    zeros_low = zeros[:6]
    exp_p2_low = exp_p2[:6]
    exp_p1_low = exp_p1[:6]
    exp_low = exp[:6]
    exp_m1_low = exp_m1[:6]
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
    print '*' * 100
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
    v_mass = TVectorD(len(mass), mass)
    v_zeros = TVectorD(len(zeros), zeros)
    v_exp_p2 = TVectorD(len(exp_p2), exp_p2)
    v_exp_p1 = TVectorD(len(exp_p1), exp_p1)
    v_exp = TVectorD(len(exp), exp)
    v_exp_m1 = TVectorD(len(exp_m1), exp_m1)
    v_exp_m2 = TVectorD(len(exp_m2), exp_m2)
    v_obs = TVectorD(len(obs), obs)
    v_mass_high = TVectorD(len(mass_high), mass_high)
    v_zeros_high = TVectorD(len(zeros_high), zeros_high)
    v_exp_p2_high = TVectorD(len(exp_p2_high), exp_p2_high)
    v_exp_p1_high = TVectorD(len(exp_p1_high), exp_p1_high)
    v_exp_high = TVectorD(len(exp_high), exp_high)
    v_exp_m1_high = TVectorD(len(exp_m1_high), exp_m1_high)
    v_exp_m2_high = TVectorD(len(exp_m2_high), exp_m2_high)
    v_obs_high = TVectorD(len(obs_high), obs_high)
    v_mass_low = TVectorD(len(mass_low), mass_low)
    v_zeros_low = TVectorD(len(zeros_low), zeros_low)
    v_exp_p2_low = TVectorD(len(exp_p2_low), exp_p2_low)
    v_exp_p1_low = TVectorD(len(exp_p1_low), exp_p1_low)
    v_exp_low = TVectorD(len(exp_low), exp_low)
    v_exp_m1_low = TVectorD(len(exp_m1_low), exp_m1_low)
    v_exp_m2_low = TVectorD(len(exp_m2_low), exp_m2_low)
    v_obs_low = TVectorD(len(obs_low), obs_low)


    arr_mass_low = np.array(mass_low[:-1], dtype = "float64")
    arr_zeros_low = np.array(zeros_low[:-1], dtype = "float64")
    arr_exp_p2_low = np.array(exp_p2_low[:-1], dtype = "float64")
    arr_exp_p1_low = np.array(exp_p1_low[:-1], dtype = "float64")
    arr_exp_low = np.array(exp_low[:-1], dtype = "float64")
    arr_exp_m1_low = np.array(exp_m1_low[:-1], dtype = "float64")
    arr_exp_m2_low = np.array(exp_m2_low[:-1], dtype = "float64")
    arr_obs_low = np.array(obs_low[:-1], dtype = "float64")









    c = TCanvas("c", "c", 800, 800)
    c.SetGridx()
    c.SetGridy()
    c.SetRightMargin(0.06)
    c.SetLeftMargin(0.2)
    if logY:
        c.SetLogy()
    dummy = TH1D("dummy", "dummy", 1, 250, 1050)
    dummy.SetBinContent(1, 0.0)
    dummy.GetXaxis().SetTitle('m_{X, spin-2} [GeV]')
    dummy.GetYaxis().SetTitle(yaxis_title)
    dummy.GetYaxis().CenterTitle()
    dummy.SetLineColor(0)
    dummy.SetLineWidth(0)
    dummy.SetFillColor(0)
    # HAVE TO HAVE non-zero value if logY is USED!!!!!!!!!!!
    minVal = 20 if not doFullHH else 1 if doFullHH else 0  # to exit
    if minVal == 0 and logY:
        print
        'check minVal'
        sys.exit(1)
    dummy.SetMinimum(minVal)
    histMax = dummy.GetMaximum()
    maxValue = 40000 if not doFullHH else 900 if doFullHH  else 0
    #if not addTheoryCurve:
    #    maxValue = 22000 if not doFullHH else 1700 if doFullHH  else 0
    if minVal == 0 or maxValue == 0:
        print
        'check min/max Val'
        sys.exit(1)
    dummy.SetMaximum(maxValue)
    # dummy.GetYaxis().SetTitleSize(0.04)
    dummy.GetYaxis().SetLabelSize(0.035)
    dummy.GetXaxis().SetLabelSize(0.03)
    dummy.SetTitleSize(0.03, "Y");
    dummy.SetTitleSize(0.04, "X");
    dummy.SetTitleOffset(2.45, "Y")
    dummy.Draw()
    # h->SetXTitle("x axis label");  h->SetYTitle("y axis label");
    # h->SetTitleSize( 0.08, "X" ); h->SetTitleOffset(0.01, "X");
    # h->SetTitleSize( 0.08, "Y" ); h->SetTitleOffset(0.01, "Y");
    # h->SetLabelSize( 0.08, "X" ); h->SetLabelOffset(0.01, "X");
    # h->SetLabelSize( 0.08, "Y" ); h->SetLabelOffset(0.01, "Y");
    low_gr_exp2 = TGraphAsymmErrors(v_mass_low, v_exp_low, v_zeros_low, v_zeros_low, v_exp_m2_low, v_exp_p2_low)
    low_gr_exp2.SetLineColor(kYellow)
    low_gr_exp2.SetFillColor(kYellow)
    low_gr_exp2.Draw("e3same")
    low_gr_exp1 = TGraphAsymmErrors(v_mass_low, v_exp_low, v_zeros_low, v_zeros_low, v_exp_m1_low, v_exp_p1_low)
    low_gr_exp1.SetLineColor(kGreen)
    low_gr_exp1.SetFillColor(kGreen)
    low_gr_exp1.Draw("e3same")
    low_gr_exp = TGraphAsymmErrors(v_mass_low, v_exp_low, v_zeros_low, v_zeros_low, v_zeros_low, v_zeros_low)
    low_gr_exp.SetLineColor(1)
    low_gr_exp.SetLineWidth(2)
    low_gr_exp.SetLineStyle(2)
    low_gr_exp.Draw("Lsame")
    high_gr_exp2 = TGraphAsymmErrors(v_mass_high, v_exp_high, v_zeros_high, v_zeros_high, v_exp_m2_high, v_exp_p2_high)
    high_gr_exp2.SetLineColor(kYellow)
    high_gr_exp2.SetFillColor(kYellow)
    high_gr_exp2.Draw("e3same")
    high_gr_exp1 = TGraphAsymmErrors(v_mass_high, v_exp_high, v_zeros_high, v_zeros_high, v_exp_m1_high, v_exp_p1_high)
    high_gr_exp1.SetLineColor(kGreen)
    high_gr_exp1.SetFillColor(kGreen)
    high_gr_exp1.Draw("e3same")
    high_gr_exp = TGraphAsymmErrors(v_mass_high, v_exp_high, v_zeros_high, v_zeros_high, v_zeros_high, v_zeros_high)
    high_gr_exp.SetLineColor(1)
    high_gr_exp.SetLineWidth(2)
    high_gr_exp.SetLineStyle(2)
    high_gr_exp.Draw("Lsame")

    # uncomment after unblinding
    print 'len(arr_mass_low)', len(arr_mass_low)
    
    gr_obs_low_p = TGraphAsymmErrors(len(arr_mass_low), arr_mass_low,arr_obs_low,arr_zeros_low,arr_zeros_low,arr_zeros_low,arr_zeros_low)
    gr_obs_low_p.SetMarkerStyle(20)
    #gr_obs_low_p.SetLineColor(1)
    #gr_obs_low_p.SetLineWidth(2)
    gr_obs_low_p.Draw("Psame") #gr_obs_low.Draw("CPsame")

    gr_obs_low_l = TGraphAsymmErrors(v_mass_low,v_obs_low,v_zeros_low,v_zeros_low,v_zeros_low,v_zeros_low)
    gr_obs_low_l.SetLineColor(1)
    gr_obs_low_l.SetLineWidth(2)
    gr_obs_low_l.Draw("Lsame") #gr_obs_low.Draw("CPsame")



    gr_obs_high = TGraphAsymmErrors(v_mass_high,v_obs_high,v_zeros_high,v_zeros_high,v_zeros_high,v_zeros_high)
    gr_obs_high.SetLineColor(1)
    gr_obs_high.SetLineWidth(2)
    gr_obs_high.SetMarkerStyle(20)
    gr_obs_high.Draw("PLsame") #gr_obs_high.Draw("CPsame")

    # if doFullHH:
    #     bbllnunu_BF = 1
    # else:
    #     bbllnunu_BF *= 1000
    # bbzz_wed_mass_xsec_dict = {k:(v*bbllnunu_BF) for k,v in wed_mass_xsec_dict.items()}
    # print 'bbzz_wed_mass_xsec_dict:'
    # pp.pprint(bbzz_wed_mass_xsec_dict)
    # wed_masses = [k for k,v in wed_mass_xsec_dict.items()]
    # bbzz_wed_xsecs = [v for k,v in wed_mass_xsec_dict.items()]


    # mass  RS1                             Bulk
    # 200   0.                              0.
    # 260   7.875333606243e-6               0.0002385051312151215
    # 300   0.0002609363907507743           0.00898207634989881

    # 400   0.0014748453016228675           0.05676631040764654
    # 500   0.002474422167974112            0.08267362069350354
    # 600   0.0031442653849825413           0.09194919121683677

    # 700   0.0035917787224510177           0.09563559916637383
    # 750   0.003759423688146883            0.09662970788334772
    # 800   0.0038997130095538993           0.09732659343012394

    # 900   0.004118727164348575            0.09819829119075223
    # 1000  0.00427930100894505             0.09869019214731996


    rs1_XtoHH = [ 0., 7.875333606243e-6, 0.0002609363907507743,
                  0.0014748453016228675, 0.002474422167974112, 0.0031442653849825413,
                  0.0035917787224510177, 0.003759423688146883, 0.0038997130095538993,
                  0.004118727164348575, 0.00427930100894505]
    #https://github.com/CrossSectionsLHC/WED/blob/master/KKGraviton_RS1/Decay_long.txt

    bulk_XtoHH = [0. , 0.0002385051312151215, 0.00898207634989881, 
                  0.05676631040764654, 0.08267362069350354, 0.09194919121683677, 
                  0.09563559916637383, 0.09662970788334772, 0.09732659343012394, 
                  0.09819829119075223, 0.09869019214731996]
    #https://github.com/CrossSectionsLHC/WED/blob/master/KKGraviton_Bulk/Decay_long.txt

    wed_masses = [200, 260, 300, 400, 500, 600, 700, 750, 800, 900, 1000]
    # https://github.com/CrossSectionsLHC/WED/blob/master/KKGraviton_RS1/GF_NLO_13TeV_ktilda_0p1.txt
    rs1_wed_xsecs = [39275.98, 14445.39, 8033.67, 2481.79, 937.05, 415.62, 205.6, 146.43, 105.82, 60.5, 36.13]
    rs1_wed_xsecs = [x * mult_limit_by for x in rs1_wed_xsecs]
    # https://github.com/CrossSectionsLHC/WED/blob/master/KKGraviton_Bulk/GF_NLO_13TeV_ktilda_0p1.txt
    bulk_wed_xsecs = [11.4356, 3.3956, 1.7849, 0.4827, 0.1752, 0.0735, 0.035, 0.0249, 0.0182, 0.0098, 0.0057]
    bulk_wed_xsecs = [x * mult_limit_by for x in bulk_wed_xsecs]
    
    total_rs1 = [x*y for x, y in zip(rs1_XtoHH, rs1_wed_xsecs)]
    total_bulk = [x*y for x, y in zip(bulk_XtoHH, bulk_wed_xsecs)]
    print 'wed_masses:'
    pp.pprint(wed_masses)

    print
    print 'total_rs1:'
    pp.pprint(total_rs1)
    print
    print 'total_bulk:'
    pp.pprint(total_bulk)

    nPoints = len(wed_masses)
    tgr_RS1 = ROOT.TGraph(nPoints, array('f', wed_masses), array('f', total_rs1))
    tgr_RS1.SetLineColor(2)
    tgr_RS1.SetLineWidth(2)

    if addTheoryCurve:
        tgr_RS1.Draw("C")
        #https://root.cern.ch/doc/master/classTGraphPainter.html#GP01

    tgr_Bulk = ROOT.TGraph(nPoints, array('f', wed_masses), array('f', total_bulk))
    tgr_Bulk.SetLineColor(4)
    tgr_Bulk.SetLineWidth(2)

    if addTheoryCurve:
        pass
        #tgr_Bulk.Draw("Lsame")

    # tgr.SetLineColor(2)
    # tgr.SetMarkerColor(2)
    # tgr.SetMarkerStyle(20)
    # tgr.Draw("pz")
    latex2 = TLatex()
    latex2.SetNDC()
    latex2.SetTextSize(0.5 * c.GetTopMargin())
    latex2.SetTextFont(42)
    latex2.SetTextAlign(11)
    latex2.DrawLatex(0.2, 0.95, "CMS preliminary")  # "Work in progress")
    # latex2.DrawLatex(0.3, 0.85, "CMS")
    legend = TLegend(.60, .70, .90, .90)
    legend.AddEntry(gr_obs_low_p , "Observed 95% CL", "lp")
    legend.AddEntry(low_gr_exp, "Expected 95% CL", "l")
    legend.AddEntry(low_gr_exp1, "#pm 1#sigma", "f")
    legend.AddEntry(low_gr_exp2, "#pm 2#sigma", "f")
    if addTheoryCurve:
        legend.AddEntry(tgr_RS1, "RS1 KK-graviton", "l");
        #legend.AddEntry(tgr_Bulk, "Bulk KK-graviton", "l");
    legend.SetShadowColor(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)
    legend.Draw("same")
    gPad.RedrawAxis()
    for ext in ['.pdf']:#, '.pdf', '.root']:
        name = 'limitHH_' if doFullHH else 'limitbbZZ_'
        c.SaveAs(name + date + ext)
    raw_input("Press Enter to continue...")


def limitsTable():
    limits = []
    # print ee_dirs
    for fil in glob.glob('combinedCards_*/log_comb_tot_*txt'):
        # mm_bdt, ee_bdt = None, None
        print 'fil', fil
        # if len(mm_d.split('_')) > 3:
        #    mm_bdt, ee_bdt = mm_d.split('_')[3], ee_d.split('_')[3]
        #    print 'mm_bdt = {0}, ee_bdt = {1}'.format(mm_bdt, ee_bdt)
        #    mass = int(mm_d.split('_')[2])
        # else:
        #    mass  = int(mm_d[8:])
        mass = int(fil.split('/')[0].split('_')[1])

        print 'mass is', mass
        if mass not in masses: continue

        if '_ML' in fil or '#' in fil: continue

        if os.path.getsize(fil) < 10000: 
            print 'bad log file, check it, exiting..'
            sys.exit(1)
            continue  # to skip corrupted/incomplete logs with errors
            
        print
        print
        'For file', fil
        print 'size is:'
        print os.path.getsize(fil)
        with io.open(fil, mode='r') as f:
            print'Full file name is', fil
            text = f.read()
            #print 'text=', text
            tmp_limits = re.findall(r"r < (\d*\.\d+|\d+)", text)
            print 'tmp_limits', tmp_limits

                # ['0xxx', '0.0755', '0.1009', '0.1411', '0.1990', '0.2700']
                # obs       2.5%      16%       50%      84%      97.5%
            limits.append((tmp_limits[-5:], mass)) #fil.split('_')[2][1:], fil.split('_')[-1][:-4]))

                #         ONLY expected limits        mass              bdt cut value

                #  Example:
                # Expected  2.5%: r < 0.0755   -2 sigma
                # Expected 16.0%: r < 0.1009   -1 sigma
                # Expected 50.0%: r < 0.1411    limit
                # Expected 84.0%: r < 0.1990   +1 sigma
                # Expected 97.5%: r < 0.2700   +2 sigma

    print
    print 'limits are:'
    limits = sorted(limits, key=lambda x: x[1])
    pp.pprint(limits)
    with io.open('combinedCards_limits.txt', 'wb') as fp:
        pickle.dump(limits, fp)

    # #To read it back:
    # with open ('limits.txt', 'rb') as fp:
    #     itemlist = pickle.load(fp)






def main():
    print 'starting '
    start_time = time.time()



    #limitsTable()
    plotLimit()


    end_time = time.time()
    time_taken = end_time - start_time # time_taken is in seconds

    hours, rest = divmod(time_taken,3600)
    minutes, seconds = divmod(rest, 60)
    print
    print "---it took {hours} hours, {minutes} minutes and {seconds:.1f} seconds to run the analysis ---".format (hours=hours, minutes=minutes, seconds=seconds)





if __name__ == '__main__':
    sys.exit(main())



