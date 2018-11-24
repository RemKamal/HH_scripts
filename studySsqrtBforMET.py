from ROOT import TFile
from numpy import array, sqrt, divide, ones, inf, isnan, logical_or
import glob
import collections
import os
import sys

#with open ("TT_DY_Gl_samples.txt") as fIn:
 #   samples = fIn.readlines()

TT_regex = "TT_*root"
DY_regex = "DY*Jets*root"
LL2Nu_regex = "G*2B2ZTo2L2Nu*root"
llQQ_regex = "G*2B2ZTo2L2J*root"
bbWW_regex = "G*2B2VTo2L2Nu*root"

masses = [260, 270, 300, 350, 400, 450,    451,    600, 650, 900, 1000]


samples = glob.glob(TT_regex) + glob.glob(DY_regex) + glob.glob(LL2Nu_regex) + glob.glob(llQQ_regex) + glob.glob(bbWW_regex)

# samples = [
#     "TT_TuneCUETP8M2T4_13TeV-powheg-Py8__RunIISummer16MAv2-PUMoriond17_backup_80r2as_2016_TrancheIV_v6-v1_shapes_mm_nominal.root",

#     "DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_shapes_mm_nominal.root",
#     "DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_shapes_mm_nominal.root",
#     "DY3JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_shapes_mm_nominal.root",
#     "DY4JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_shapes_mm_nominal.root",

#     "GluGluToRadionToHHTo2B2VTo2L2Nu_M-250_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_shapes_mm_nominal.root",
#     "GluGluToRadionToHHTo2B2VTo2L2Nu_M-260_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_shapes_mm_nominal.root",
#     "GluGluToRadionToHHTo2B2VTo2L2Nu_M-270_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_shapes_mm_nominal.root",
#     "GluGluToRadionToHHTo2B2VTo2L2Nu_M-300_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_shapes_mm_nominal.root",
#     "GluGluToRadionToHHTo2B2VTo2L2Nu_M-350_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_shapes_mm_nominal.root",
#     "GluGluToRadionToHHTo2B2VTo2L2Nu_M-400_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_shapes_mm_nominal.root",
#     "GluGluToRadionToHHTo2B2VTo2L2Nu_M-450_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_shapes_mm_nominal.root",

#     # "GluGluToRadionToHHTo2B2ZTo2L2J_M-260_narrow_13TeV-madgraph-v2__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_shapes_mm_nominal.root",
#     # "GluGluToRadionToHHTo2B2ZTo2L2J_M-270_narrow_13TeV-madgraph-v2__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_shapes_mm_nominal.root",
#     # "GluGluToRadionToHHTo2B2ZTo2L2J_M-300_narrow_13TeV-madgraph-v2__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_shapes_mm_nominal.root",
#     # "GluGluToRadionToHHTo2B2ZTo2L2J_M-350_narrow_13TeV-madgraph-v2__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_shapes_mm_nominal.root",
#     # "GluGluToRadionToHHTo2B2ZTo2L2J_M-400_narrow_13TeV-madgraph-v2__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_shapes_mm_nominal.root",
#     # "GluGluToRadionToHHTo2B2ZTo2L2J_M-450_narrow_13TeV-madgraph-v2__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_shapes_mm_nominal.root",

#     "GluGluToRadionToHHTo2B2ZTo2L2Nu_M-250_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_shapes_mm_nominal.root",
#     "GluGluToRadionToHHTo2B2ZTo2L2Nu_M-260_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_shapes_mm_nominal.root",
#     "GluGluToRadionToHHTo2B2ZTo2L2Nu_M-270_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_shapes_mm_nominal.root",
#     "GluGluToRadionToHHTo2B2ZTo2L2Nu_M-300_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_shapes_mm_nominal.root",
#     "GluGluToRadionToHHTo2B2ZTo2L2Nu_M-350_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_shapes_mm_nominal.root",
#     "GluGluToRadionToHHTo2B2ZTo2L2Nu_M-400_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_shapes_mm_nominal.root",
#     "GluGluToRadionToHHTo2B2ZTo2L2Nu_M-450_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_shapes_mm_nominal.root"


# ]


def checkMetForOneMass(mass):

    #print 'samples', samples
    B2V_until_cut = collections.OrderedDict()
    B2Z_until_cut = collections.OrderedDict()
    B2Q_until_cut = collections.OrderedDict()
    TT_until_cut = collections.OrderedDict()
    DY1_until_cut = collections.OrderedDict()
    DY2_until_cut = collections.OrderedDict()
    DY3_until_cut = collections.OrderedDict()
    DY4_until_cut = collections.OrderedDict()

    B2V_after_cut = collections.OrderedDict()
    B2Z_after_cut = collections.OrderedDict()
    B2Q_after_cut = collections.OrderedDict()
    TT_after_cut = collections.OrderedDict()
    DY1_after_cut = collections.OrderedDict()
    DY2_after_cut = collections.OrderedDict()
    DY3_after_cut = collections.OrderedDict()
    DY4_after_cut = collections.OrderedDict()
    
    for s in samples:
        if s != '\n':
            raw_s = "%r"%s
            s_raw = r'%s'%s

        #s = raw_s 
        #s = s_raw


         
            #mass = None 

            # if not os.path.exists(thisMassSample):
            #     print 'please check sample', thisMassSample , '...exiting...'
            #     sys.exit(1)

            if 'Glu' in s:
                tmp_mass = int(s.split("_narrow")[0].split("_M-")[-1])
                if tmp_mass != mass: continue
                
            if not os.path.exists(s):
                print 'please check sample', s , '...exiting...'
                sys.exit(1)

            #print s
            #print 'mass=', mass
            fil = TFile(s)
            met_hist = fil.Get("met_pt")
            integral = met_hist.Integral()
            for cut in range(0, 180, 10):# first_bin, last_bin):
                first_bin = met_hist.FindBin(0) #if cut == 10 else met_hist.FindBin(cut-10)
                cut_bin = met_hist.FindBin(cut)
                last_bin = met_hist.GetNbinsX()
                #print 'cut=', cut
                #print 'met_hist.GetBinLowEdge(cut_bin)+1 for real value of the cut since inclusive', met_hist.GetBinLowEdge(cut_bin+1)
                #print "first_bin={}, cut_bin= {}, last_bin={}".format(first_bin, cut_bin, last_bin, )
                yield_until_cut = met_hist.Integral(first_bin, cut_bin)
                yield_after_cut = met_hist.Integral(cut_bin+1, last_bin)
                #print 'yield_until_cut/integral =', 1.0*yield_until_cut/integral
                #print 'yield_after_cut/integral =', 1.0*yield_after_cut/integral
                #print 'yield_until_cut =', 1.0*yield_until_cut
                #print 'yield_after_cut =', 1.0*yield_after_cut

            
                if 'TT' in s:    
                    TT_until_cut[cut+10] = 1.0*yield_until_cut
                    TT_after_cut[cut+10] = 1.0*yield_after_cut
                elif 'DY1' in s:
                    DY1_until_cut[cut+10] = 1.0*yield_until_cut
                    DY1_after_cut[cut+10] = 1.0*yield_after_cut
                elif 'DY2' in s:
                    DY2_until_cut[cut+10] = 1.0*yield_until_cut
                    DY2_after_cut[cut+10] = 1.0*yield_after_cut
                elif 'DY3' in s:
                    DY3_until_cut[cut+10] = 1.0*yield_until_cut
                    DY3_after_cut[cut+10] = 1.0*yield_after_cut
                elif 'DY4' in s:
                    DY4_until_cut[cut+10] = 1.0*yield_until_cut
                    DY4_after_cut[cut+10] = 1.0*yield_after_cut
                elif '2B2VTo2L2Nu' in s:
                    #if mass in masses_of_interest:
                    B2V_until_cut[cut+10] = 1.0*yield_until_cut
                    B2V_after_cut[cut+10] = 1.0*yield_after_cut
                elif '2B2ZTo2L2Nu' in s:
                    #if mass in masses_of_interest:
                    B2Z_until_cut[cut+10] = 1.0*yield_until_cut
                    B2Z_after_cut[cut+10] = 1.0*yield_after_cut
                elif '2B2ZTo2L2J' in s:
                    #if mass in masses_of_interest:
                    B2Q_until_cut[cut+10] = 1.0*yield_until_cut
                    B2Q_after_cut[cut+10] = 1.0*yield_after_cut
                else:
                    continue

                


# weights are correct and full, only common lumi is not included, since the same for all!
# signal is normalised to 1pn xsec

    #print 'cuts=', B2V_until_cut.keys()
    
    # print 'B2V_until_cut_%s=' % str(mass) , (B2V_until_cut.values())
    # print 'B2Z_until_cut_%s=' % str(mass) , (B2Z_until_cut.values()) 
    # print 'B2Q_until_cut_%s=' % str(mass) , (B2Q_until_cut.values()) 
    # print 'TT_until_cut_%s=' % str(mass) ,  (TT_until_cut.values()) 
    # print 'DY1_until_cut_%s=' % str(mass) , (DY1_until_cut.values())
    # print 'DY2_until_cut_%s=' % str(mass) , (DY2_until_cut.values())
    # print 'DY3_until_cut_%s=' % str(mass) , (DY3_until_cut.values())
    # print 'DY4_until_cut_%s=' % str(mass) , (DY4_until_cut.values())
    
    # print 'B2V_after_cut_%s=' % str(mass) , (B2V_after_cut.values())
    # print 'B2Z_after_cut_%s=' % str(mass) , (B2Z_after_cut.values()) 
    # print 'B2Q_after_cut_%s=' % str(mass) , (B2Q_after_cut.values()) 
    # print 'TT_after_cut_%s=' % str(mass) ,  (TT_after_cut.values()) 
    # print 'DY1_after_cut_%s=' % str(mass) , (DY1_after_cut.values())
    # print 'DY2_after_cut_%s=' % str(mass) , (DY2_after_cut.values())
    # print 'DY3_after_cut_%s=' % str(mass) , (DY3_after_cut.values())
    # print 'DY4_after_cut_%s=' % str(mass) , (DY4_after_cut.values())

    
    before_cut = array([
        array(B2V_until_cut.values()), array(B2Z_until_cut.values()), 
        array(B2Q_until_cut.values()), 
        array(TT_until_cut.values()), array(DY1_until_cut.values()), array(DY2_until_cut.values()), array(DY3_until_cut.values()), array(DY4_until_cut.values())
        ])
    after_cut = array([
        array(B2V_after_cut.values()), array(B2Z_after_cut.values()),
        array(B2Q_after_cut.values()),
        array(TT_after_cut.values()), array(DY1_after_cut.values()), array(DY2_after_cut.values()), array(DY3_after_cut.values()), array(DY4_after_cut.values())
        ])

    return before_cut, after_cut



def calcSsqrtB(before_cut_rates, after_cut_rates):
    
    #print 'before_cut_rates', before_cut_rates
    #print 'after_cut_rates', after_cut_rates
    before_cut_rates, after_cut_rates = 35900 * before_cut_rates, 35900 * after_cut_rates
    #print 'after lumi'
    #print 'before_cut_rates', before_cut_rates
    #print 'after_cut_rates', after_cut_rates
    
    ourSignal_before_cut = before_cut_rates[0:2].sum(axis=0)
    qqSignal_before_cut = before_cut_rates[2]
    bgTotal_before_cut = before_cut_rates[3:].sum(axis=0)
    #bgTotal_before_cut[bgTotal_before_cut == inf] = 0
    
    #bgTotal_before_cut = 0.000000000000000000001 + bgTotal_before_cut
    #print 'ourSignal_before_cut', ourSignal_before_cut.tolist()
    #print 'qqSignal_before_cut', qqSignal_before_cut.tolist()
    #print 'bgTotal_before_cut', bgTotal_before_cut.tolist()
    #print 'sqrt(bgTotal_before_cut)', sqrt(bgTotal_before_cut)
    ourSsqrtB_before_cut = divide(ourSignal_before_cut, sqrt(bgTotal_before_cut))
    ourSsqrtB_before_cut[logical_or(ourSsqrtB_before_cut == inf, isnan(ourSsqrtB_before_cut) )] = 0
    print 'ourSsqrtB_before_cut=', ourSsqrtB_before_cut.tolist()

    qqSsqrtB_before_cut = divide(qqSignal_before_cut, sqrt(bgTotal_before_cut))
    qqSsqrtB_before_cut[logical_or(qqSsqrtB_before_cut == inf , isnan(qqSsqrtB_before_cut) )] = 0
    print 'qqSsqrtB_before_cut=', qqSsqrtB_before_cut.tolist()

    #print "=="*50
    ourSignal_after_cut = after_cut_rates[0:2].sum(axis=0)
    qqSignal_after_cut = after_cut_rates[2]
    bgTotal_after_cut = after_cut_rates[3:].sum(axis=0)
    #bgTotal_after_cut[bgTotal_after_cut == inf] = 0
    #bgTotal_after_cut = 0.000000000000000000001 + bgTotal_after_cut
    #print 'ourSignal_after_cut', ourSignal_after_cut.tolist()
    #print 'qqSignal_after_cut', qqSignal_after_cut.tolist()
    #print 'bgTotal_after_cut', bgTotal_after_cut.tolist()
    #print 'sqrt(bgTotal_after_cut)', sqrt(bgTotal_after_cut)
    ourSsqrtB_after_cut = divide(ourSignal_after_cut, sqrt(bgTotal_after_cut))
    ourSsqrtB_after_cut[logical_or( ourSsqrtB_after_cut == inf, isnan(ourSsqrtB_after_cut) )] = 0
    print 'ourSsqrtB_after_cut=', ourSsqrtB_after_cut.tolist()

    qqSsqrtB_after_cut = divide(qqSignal_after_cut, sqrt(bgTotal_after_cut))
    qqSsqrtB_after_cut[logical_or(qqSsqrtB_after_cut == inf , isnan(qqSsqrtB_after_cut) )] = 0
    print 'qqSsqrtB_after_cut=', qqSsqrtB_after_cut.tolist()


if __name__ == "__main__":
    bdtCut = float(os.getcwd().split('/')[-1].split('_')[-1])
    print 'bdtCut=', bdtCut
    leptType = "muons" if "muons" in os.getcwd() else "eles" if "eles" in os.getcwd() else None
    print 'leptType=', leptType
    if not bdtCut in [0.1, 0.4, 0.7, 0.925, 0.99] or leptType == None:
        print 'check bdtCut or leptType, exiting...'
        sys.exit(1)
    
    for mass in masses:
        if leptType == 'muons':
            if mass < 300 and bdtCut == 0.1:
                pass
            elif 300 <= mass < 600 and bdtCut == 0.7:
                pass
            elif 600 <= mass and bdtCut == 0.99:
                pass
            else:
                continue
        elif leptType == 'eles':
            if mass <= 350 and bdtCut == 0.4:
                pass
            elif 400 <= mass < 600 and bdtCut == 0.925:
                pass
            elif 600 <= mass and bdtCut == 0.99:
                pass
            else:
                continue
        else:
            print
            'cannot happen, exiting'
            sys.exit(1)
        

        thisMassSample = glob.glob("Glu*" + str(mass) + "*root")
        if thisMassSample != []:
            thisMassSample = thisMassSample[0]
        else:
            continue

        rates_before, rates_after = checkMetForOneMass(mass)
        if mass == 450 and "high_SR" in os.getcwd():
            print 'mass=', 451
        else:
            print 'mass=', mass
        channel = "\mu\mu" if "muons" in leptType else "ee"
        print """channelNmass = r"$%s$ channel, {} GeV". format(mass)""" % channel
        calcSsqrtB(rates_before, rates_after)
        print """makeMETplot(ourSsqrtB_before_cut, qqSsqrtB_before_cut, ourSsqrtB_after_cut, qqSsqrtB_after_cut, channelNmass)"""
        print
    print '=/='*100
