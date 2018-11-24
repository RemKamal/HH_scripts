print 'started'
import sys, getopt
from ROOT import TFile
print 'imported ROOT'
#https://stackoverflow.com/questions/15938532/matplotlib-histogram-and-bin-labels
import matplotlib.pyplot as plt
print 'imported plt'
import numpy as np

#import matplotlib as mpl
from math import floor, ceil
from pprint import pprint as pp

#matplotlib.get_backend()
#%matplotlib notebook
#%pylab inline
#%matplotlib inline

insertDenominator = False
addAnalysisCutsManually = False

printEntriesNotEfficiency = False

printEntriesNotEfficiency = True


add900sample = False
HHtype = ""
muon_iso_tightEle_cut = False
addMETcut = False
skipList = [] #["bbZZ900"]
#channel = "eles"
channel = ""#"muons"
vTypeCorrected = ""#False
prepareCutFlowData = True

cutFlow_list_of_lists = {}

def getCutFlowHistogram(fIn, shortName):
    print 'fIn', fIn
    if shortName in skipList: return
    if fIn == "": return
    if "bbZZ300" in shortName:
        global vTypeCorrected
        vTypeCorrected = True if ("VTC" in fIn or "May25" in fIn or "May3" in fIn) else False
        print 'vTypeCorrected', vTypeCorrected
    f = TFile(fIn)
    if f.IsZombie() or not f.IsOpen() or  f.GetNkeys()==0 : 
        skipList.append(shortName)
        return
    try:
        cutFlowHist = f.Get("cutFlow")
    except:
        skipList.append(shortName)
        return
    if cutFlowHist == None:
        skipList.append(shortName)
        return

    #https://github.com/scikit-hep/root_numpy/blob/master/root_numpy/tests/test_hist.py
    #https://github.com/rootpy/rootpy-tutorials/tree/master/pyroot/official/pyroot
    #https://root.cern/doc/v610/ratioplot_8py_source.html
    #http://www.rootpy.org/auto_examples/plotting/plot_bin_merging.html
    print 'len(cutFlowHist)', len(cutFlowHist)                #13
    print 'cutFlowHist.GetNbinsX()', cutFlowHist.GetNbinsX()  #11
    eff_list = []
    for idx, bin in enumerate(cutFlowHist): 
        # skip under and overflows
        if idx ==0 or idx >= len(cutFlowHist)-1: continue
        print 'bin {} has content {}'.format(idx, bin)
        if printEntriesNotEfficiency:
            eff_list.append(bin)
        else:
            eff_list.append(100.*bin/cutFlowHist.GetBinContent(1))

    #maxEntry = max(eff_list) 

    # inclusiveEles =  naEles + nvEles
    # naEles = tree.Draw("aLeptons_pdgId", "abs(aLeptons_pdgId)==11", "goff") 
    # nvEles = tree.Draw("vLeptons_pdgId", "abs(vLeptons_pdgId)==11", "goff")

    inclusiveEles = None
    inclusiveMuons = None
    #bb ZZ 300
    #naEles=65915, nvEles=51936, nselEles=67831
    #naMuons=40709, nvMuons=73566, nselMuons=87550


    #bb ZZ 900
    #naEles=129733, nvEles=110810, nselEles=146162
    #naMuons=93772, nvMuons=144490, nselMuons=165879
    if 'bbZZ300' in shortName:
        inclusiveEles = 65915 + 51936
        inclusiveMuons = 40709 + 73566
    elif 'bbZZ900' in shortName:
        inclusiveEles = 129733 + 110810
        inclusiveMuons = 93772 + 144490
    else:
        pass

    inclusive = inclusiveEles if channel == "eles" else inclusiveMuons if channel == "muons" else None
    if inclusive == None and insertDenominator:
        print 'check inclusive, exiting...'
        sys.exit(1)


    if insertDenominator:
        eff_list.insert(2, inclusive)
    tree = f.Get("tree")
    analysis_cuts = ""
    muonCuts = "lep0Iso04 < 0.15 && lep1Iso04 < 0.15 && (1.4442 > abs(lepeta0) || abs(lepeta0) > 1.566) && (1.4442 > abs(lepeta1) || abs(lepeta1) > 1.566)" 
    eleCuts = "leppt0 > 25 && lep0Iso03 < 0.06 && lep1Iso03 < 0.06 && (1.4442 > abs(lepeta0) || abs(lepeta0) > 1.566) && (1.4442 > abs(lepeta1) || abs(lepeta1) > 1.566)"
    muonCuts_ele_like = "leppt0 > 25 && lep0Iso04 < 0.06 && lep1Iso04 < 0.06 && (1.4442 > abs(lepeta0) || abs(lepeta0) > 1.566) && (1.4442 > abs(lepeta1) || abs(lepeta1) > 1.566)"

    if "muon" in fIn:
        analysis_cuts = muonCuts 
    else:
        analysis_cuts = eleCuts

    if muon_iso_tightEle_cut:
        analysis_cuts = muonCuts_ele_like


    if addMETcut and 'Glu' in fIn:
        start = fIn.find("M-")
        end = fIn.find("_narrow")
        mass = int(fIn[start+2:end])
        
        if mass <= 300:
            metCut = " && met_pt > 40"
        elif 350 <= mass <= 600:
            metCut = " && met_pt > 75"
        else:
            metCut = " && met_pt > 100"

        analysis_cuts += metCut



    print 'for ', shortName, ' analysis_cuts=', analysis_cuts

    events_analysis_cuts = tree.Draw("leppt0", analysis_cuts, "goff")
    print 'original events_analysis_cuts', events_analysis_cuts
    if printEntriesNotEfficiency:
        pass
    else:
        events_analysis_cuts = 100.0*events_analysis_cuts/cutFlowHist.GetBinContent(1)

    print 'eff of events_analysis_cuts', events_analysis_cuts
    if addAnalysisCutsManually:
        eff_list[-1] = events_analysis_cuts
    
        # if  leptonType == "ee" and entry.leppt0 <=25: continue
        # if  leptonType == "ee" and (entry.lep0Iso03>0.06 or entry.lep1Iso03>0.06): continue
        # if  leptonType == "mm" and (entry.lep0Iso04>0.15 or entry.lep1Iso04>0.15): continue
        # if (1.4442 < abs(entry.lepeta0) < 1.566) or (1.4442 < abs(entry.lepeta1) <1.566): continue



    if eff_list != []:
        print "'{}_eff_list' : {},".format(shortName, eff_list)
        #global cutFlow_list_of_lists
        cutFlow_list_of_lists[shortName] = eff_list
        #makeFigure (eff_list)
    

#     from root_numpy import array2hist, hist2array

# import numpy as np
# from rootpy.plotting import Hist2D
# from rootpy.plotting import Hist
# h = Hist(10, 0, 1, name="some name", title="some title")

# hist = Hist2D(5, 0, 1, 3, 0, 1, type='F')
# array = np.random.randint(0, 10, size=(7, 5))
# array
# array([[6, 7, 8, 3, 4],
#        [8, 9, 7, 6, 2],
#        [2, 3, 4, 5, 2],
#        [7, 6, 5, 7, 3],
#        [2, 0, 5, 6, 8],
#        [0, 0, 6, 5, 2],
#        [2, 2, 1, 5, 4]])
# _ = array2hist(array, hist)
# # dtype matches histogram type (D, F, I, S, C)
# hist2array(hist)
# array([[ 9.,  7.,  6.],
#        [ 3.,  4.,  5.],
#        [ 6.,  5.,  7.],
#        [ 0.,  5.,  6.],
#        [ 0.,  6.,  5.]], dtype=float32)
# # overflow is excluded by default
# hist2array(hist, include_overflow=True)
# array([[ 6.,  7.,  8.,  3.,  4.],
#        [ 8.,  9.,  7.,  6.,  2.],
#        [ 2.,  3.,  4.,  5.,  2.],
#        [ 7.,  6.,  5.,  7.,  3.],
#        [ 2.,  0.,  5.,  6.,  8.],
#        [ 0.,  0.,  6.,  5.,  2.],
#        [ 2.,  2.,  1.,  5.,  4.]], dtype=float32)
# array2 = hist2array(hist, include_overflow=True, copy=False)


def makeEffCutFlowPlot(eff_dict):
    
    #global cutFlow_list_of_lists
    if not eff_dict: eff_dict = cutFlow_list_of_lists #= eff_dict
    #cutFlow_list_of_lists = dict_effs
    #print 'cutFlow_list_of_lists'
    #pp(cutFlow_list_of_lists)
    print 'eff_dict:'
    pp(eff_dict)
    #%matplotlib notebook                                                                                                                                                                                                                                                       
    
#%matplotlib inline                                                                                                         
    if vTypeCorrected != "" and vTypeCorrected == True:
        names = [
            "skimming",
            "splitSignal",
            "VHbb preselection",
            "decayType",
            "trigger",
            ">=b-jets",
            "Hbb mass",
            "2 leptons",
            "Z mass",
            "MET cut",
            "hhMt cut",
            "analysis cuts" #"final bin"
            ]

        names = ['no cut', 'splitSignal', 'inclusive >=2 ee/mm', 'selLeptons pdg ID 11/13', 'mva ID', 'ocsm and leading pt', 'eta gap',
                 'iso cut', 'manual preselection', '0 or 1 vType', 'trigger', '>=2b-jets', 'Hbb loose',  '2leps', 'Z mass loose',
                 'met>0', 'hhMt>100', '90<Hbb<150', '76<Z<106']

        if insertDenominator:
            names.insert(2, 'aLept+vLept')
    else:
        names = [
            "skimming",
            "splitSignal",
            "decayType",
            "trigger",
            ">=b-jets",
            "Hbb mass",
            "2 leptons",
            "Z mass",
            "MET cut",
            "hhMt cut",
            "analysis cuts" #"final bin"                                                                                          
            ]

    print 'names', names
    print 'len(names)', len(names)


    fig, ax = plt.subplots(1) #, figsize=(8,12))
    #plt.rcParams["figure.figsize"] = [9,16]

    # BAD STUFF!!!
    #axes = plt.axes()
    # right stuff FOR THIS TYPE OF PLOT 
    axes = plt.gca()
    
    bbZZ300 = eff_dict.get('bbZZ300', None)
    bbZZ900 = eff_dict.get('bbZZ900', None)

    bbWW900 = eff_dict.get('bbWW900', None)
    bbWW300 = eff_dict.get('bbWW300', None)

    TT = eff_dict.get('TT', None)
    DY1J = eff_dict.get('DY1J', None)
    DY2J = eff_dict.get('DY2J', None)

    maxEntry = None
    width=0.3
    if bbZZ300 == None:
        print 'check bbZZ300, exiting'
        sys.exit(1)
    else:
        print 'bbZZ300', bbZZ300
        maxEntry = max(bbZZ300) 
        if maxEntry == None:
            print 'check maxEntry for bbZZ300, exiting'
            sys.exit(1)
    if 'bbZZ900' not in skipList:
        maxEntry = max(bbZZ900)

    bins = map(lambda x: x-width/2,range(1,len(bbZZ300)+1))
    #bins = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    print 'bins', bins
    print 'len(bins)', len(bins)
    colors = ['blue', 'red', 'green', 'orange', 'brown', 'olive', 'orchid' ]

    for idx, (sampleEff, name) in enumerate(zip([bbZZ300, bbZZ900, bbWW900, bbWW300, TT, DY1J, DY2J], ["bbZZ300", "bbZZ900", "bbWW900", "bbWW300", "TT", "DY1J", "DY2J"])):
        if sampleEff == None:
            continue
        else:
            print 'working with', name
            print 'sampleEff', sampleEff
            print 'len(sampleEff)', len(sampleEff)
            clr = colors[idx]
            print 'color', clr
            ax.plot(bins, sampleEff, lw=2, label=name, color=clr)

    
    # ax.plot(bins, bbZZ300, lw=2, label='bbZZ300', color='blue')                                                                                                                                                                                                               

    # ax.plot(bins, bbZZ900, lw=2, label='bbZZ900', color='red')                                                                                                                                                                                                                
    # ax.plot(bins, bbWW900, lw=2, label='bbWW900', color='green')                                                                                                                                                                                                              
    # ax.plot(bins, bbWW300, lw=2, label='bbWW300', color='orange')                                                                                                                                                                                                             

    # ax.plot(bins, TT, lw=2, label='TT', color='brown')                                                                                                                                                                                                                        
    # ax.plot(bins, DY1J, lw=2, label='DY1J', color='olive')                                                                                                                                                                                                                    
    # ax.plot(bins, DY2J, lw=2, label='DY2J', color='orchid')                                                                                                                                                                                                                   
    #https://matplotlib.org/examples/color/named_colors.html                                                                                                                                                                                                                    


    ax.set_axis_bgcolor('white')


    ax.legend(loc='best')

    axis_font = {'fontname':'Arial', 'size':'13'}


    #ax.set_xlabel('MET cut, GeV', 'size':'10')                 
    ax.set_ylabel('Efficiency, %' if not printEntriesNotEfficiency else 'Events', fontdict=axis_font)                                                                                                                                                                                                                         

    left = floor(bins[0])
    right = ceil (bins[-1])

    axes.set_ylim([0, maxEntry])
    #ax.set_xlim(left, right)
    
    #plt.set_xlim(left, right)
    
    fig = plt.gcf()
    #fig.set_size_inches(18.5, 10.5)
    #fig.savefig('test2png.png', dpi=100)
    #To propagate the size change to an existing gui window add forward=True

    fig.set_size_inches(8, 4, forward=True)


    #axes.yaxis.set_label_coords(-0.1,1.02)                                                                                                                                                                                                                                     
    #axes.yaxis.set_label_coords(-0.1, 100.)
    

    #https://alexpearce.me/2014/04/exponent-label-in-matplotlib/                                                                                                                                                                                                                
    #ax.get_xaxis().set_major_locator(mpl.ticker.MultipleLocator(1.0))
    #ax.set_xticklabels(names,rotation=45, rotation_mode="anchor", ha="right")
    manual_labels = bins #['0.20','0.32','0.50','0.79','1.26','2.00','3.16']
    ax.set_xticks(bins )#[0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5])
    #plt.xticks(ha='left')
    fig.autofmt_xdate()

    #ax.set_xticklabels(names, minor=False)
    ax.set_xticklabels(names,rotation=45, rotation_mode="anchor", ha="right", size=9)
    ax.set_xmargin(1)
    ax.grid()
    plt.savefig('cutFlow{}_{}{}{}{}_{}.png'.format("Events" if printEntriesNotEfficiency else "Efficiency", channel, "_VTC" if vTypeCorrected else "", "_METcut" if addMETcut else "", "_eleCuts" if muon_iso_tightEle_cut else "", HHtype), bbox_inches='tight', dpi=300)
    print 'dict_effs_{}{}{}{}_{}='.format(channel, "_VTC" if vTypeCorrected else "", "_METcut" if addMETcut else "", "_eleCuts" if muon_iso_tightEle_cut else "", HHtype), pp(cutFlow_list_of_lists)
    #plt.show()
    #plt.draw()



def makeFigure(data):
    
    np.random.seed(42)
    #data = np.random.rand(5)
    #names = ['A:GBC_1233','C:WERT_423','A:LYD_342','B:SFS_23','D:KDE_2342']
    names = [
        "skimming",
        "splitSignal",
        "decayType",
        "trigger",
        ">=b-jets",
        "Hbb mass",
        "2 leptons",
        "Z mass",
        "MET cut",
        "hhMt cut",
        "final bin"
        ]
     
    print 'before ax'
    ax = plt.subplot(111)
    width=0.3
    bins = map(lambda x: x-width/2,range(1,len(data)+1))
    print 'before bar'
    ax.bar(bins,data,width=width)
    ax.set_xticks(map(lambda x: x, range(1,len(data)+1)))
#ax.set_xticklabels(names,rotation=45)
    plt.ylabel('Efficiency, %', position=(0., 1.), va='top', ha='right')
    axes = plt.axes()

    #axes.yaxis.set_label_coords(-0.1,1.02)
    axes.yaxis.set_label_coords(-0.1, 1.)
    #https://alexpearce.me/2014/04/exponent-label-in-matplotlib/
    ax.set_xticklabels(names,rotation=45, rotation_mode="anchor", ha="right")
    print 'after set_'
#plt.show()
# save the figure as a bytes string in the svg format.
#from io import BytesIO
#f = BytesIO()
    print 'before saving'
#plt.savefig(f, format="svg")
    plt.savefig('cutEff.png', bbox_inches='tight', dpi=400)



if __name__ == "__main__":
    argv = sys.argv[1:]

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
    print 'Input file is "', inDir
    if outputfile:
        print 'Output file is "', outputfile

    if inDir == "":
        print 'check inDir, exiting....'
        sys.exit(1)
    #global channel
    if "eles" in inDir:
        channel = "eles"
    else:
        channel = "muons"

#oldFileWithCutFlow = "/afs/cern.ch/work/r/rkamalie/private/July31/v2/CMSSW_8_0_25/src/VHbbAnalysis/Heppy/test/analysis_May14_muons_BGrav_total_SR_minitrees_inpb_wBR/GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-900_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root"
#     bbZZ300 = "/eos/user/r/rkamalie/CMSSW_8_0_25/src/bbZZ/skimmedSamples/GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-300_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/skimtree_15_29.root"
#     bbZZ900 = "/eos/user/r/rkamalie/CMSSW_8_0_25/src/bbZZ/skimmedSamples/GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-900_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/skimtree_15_29.root"

#     bbWW900 = "/eos/user/r/rkamalie/CMSSW_8_0_25/src/bbZZ/skimmedSamples/GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-900_narrow_13TeV-madgraph/skimtree_0_14.root"
#     bbWW300 = "/eos/user/r/rkamalie/CMSSW_8_0_25/src/bbZZ/skimmedSamples/GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-300_narrow_13TeV-madgraph/skimtree_0_14.root"

#     TT = "/eos/user/r/rkamalie/CMSSW_8_0_25/src/bbZZ/skimmedSamples_v2/TT_TuneCUETP8M2T4_13TeV-powheg-Py8__RunIISummer16MAv2-PUMoriond17_backup_80r2as_2016_TrancheIV_v6-v1/skimtree_540_554.root"
#     DY1J = "/eos/user/r/rkamalie/CMSSW_8_0_25/src/bbZZ/skimmedSamples/DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/skimtree_1005_1019.root"
#     DY2J = "/eos/user/r/rkamalie/CMSSW_8_0_25/src/bbZZ/skimmedSamples/DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/skimtree_375_389.root"

# #==============================

#     bbZZ300 = ""
#     bbZZ900 = ""

#     bbWW900 = ""
#     bbWW300 = ""

#     TT = ""
#     DY1J = ""
#     DY2J = ""


# #==============================

#     # BULK GRAVITON AND MUONS!!!!!!!!!!! Old skims
#     bbZZ300 = "/afs/cern.ch/work/r/rkamalie/private/July31/v2/CMSSW_8_0_25/src/VHbbAnalysis/Heppy/test/analysis_May14_{}_BGrav_total_SR_minitrees_inpb_wBR/GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-300_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root".format(channel)
#     bbZZ900 = "/afs/cern.ch/work/r/rkamalie/private/July31/v2/CMSSW_8_0_25/src/VHbbAnalysis/Heppy/test/analysis_May14_{}_BGrav_total_SR_minitrees_inpb_wBR/GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-900_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root".format(channel)

#     bbWW900 = "/afs/cern.ch/work/r/rkamalie/private/July31/v2/CMSSW_8_0_25/src/VHbbAnalysis/Heppy/test/analysis_May14_{}_BGrav_total_SR_minitrees_inpb_wBR/GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-300_narrow_13TeV-madgraph_HWW_minitree.root".format(channel)
#     bbWW300 = "/afs/cern.ch/work/r/rkamalie/private/July31/v2/CMSSW_8_0_25/src/VHbbAnalysis/Heppy/test/analysis_May14_{}_BGrav_total_SR_minitrees_inpb_wBR/GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-900_narrow_13TeV-madgraph_HWW_minitree.root".format(channel)

#     TT = "/afs/cern.ch/work/r/rkamalie/private/July31/v2/CMSSW_8_0_25/src/VHbbAnalysis/Heppy/test/analysis_May14_{}_BGrav_total_SR_minitrees_inpb_wBR/TT_TuneCUETP8M2T4_13TeV-powheg-Py8__RunIISummer16MAv2-PUMoriond17_backup_80r2as_2016_TrancheIV_v6-v1_minitree.root".format(channel)
#     DY1J = "/afs/cern.ch/work/r/rkamalie/private/July31/v2/CMSSW_8_0_25/src/VHbbAnalysis/Heppy/test/analysis_May14_{}_BGrav_total_SR_minitrees_inpb_wBR/DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root".format(channel)
#     DY2J = "/afs/cern.ch/work/r/rkamalie/private/July31/v2/CMSSW_8_0_25/src/VHbbAnalysis/Heppy/test/analysis_May14_{}_BGrav_total_SR_minitrees_inpb_wBR/DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root".format(channel)


    inDir.replace("muons", "{leptons}")
    inDir.replace("eles", "{leptons}")
    print 'inDir', inDir
    
    HHtype = "Radion" if "Radion" in inDir else "BulkGraviton" 
    print 'HHtype', HHtype
    if True:#processNewCorrectedFiles:
        #"analysis_May23_2_VTC_eles_BGrav_total_SR_minitrees_inpb_wBR"
        bbZZ300 = inDir.format(leptons=channel) + "/GluGluTo{hh}ToHHTo2B2ZTo2L2Nu_M-300_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root".format(hh=HHtype)
        print 'bbZZ300', bbZZ300
        bbZZ900 = inDir.format(leptons=channel) + "/GluGluTo{hh}ToHHTo2B2ZTo2L2Nu_M-900_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root".format(hh=HHtype)
                                                    #/GluGluTo{hh}ToHHTo2B2VTo2L2Nu_M-300_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root
        bbWW900 = inDir.format(leptons=channel) 
        bbWW900 += "/GluGluTo{hh}ToHHTo2B2VTo2L2Nu_M-300_narrow_13TeV-madgraph_minitree.root".format(hh=HHtype) if HHtype == "BulkGraviton" else "/GluGluTo{hh}ToHHTo2B2VTo2L2Nu_M-300_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root".format(hh=HHtype)
        bbWW300 = inDir.format(leptons=channel) 
        bbWW300 += "/GluGluTo{hh}ToHHTo2B2VTo2L2Nu_M-900_narrow_13TeV-madgraph_minitree.root".format(hh=HHtype) if HHtype == "BulkGraviton" else "/GluGluTo{hh}ToHHTo2B2VTo2L2Nu_M-900_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMorio\
nd17_80r2as_2016_TrancheIV_v6-v1_minitree.root".format(hh=HHtype)

        TT = inDir + "/TT_TuneCUETP8M2T4_13TeV-powheg-Py8__RunIISummer16MAv2-PUMoriond17_backup_80r2as_2016_TrancheIV_v6-v1_minitree.root".format(channel)
        DY1J = inDir + "/DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root".format(channel)
        DY2J = inDir + "/DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root".format(channel)

    # else:
    #     bbZZ300 = "analysis_May23_2_{}_BGrav_total_SR_minitrees_inpb_wBR/GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-300_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root".format(channel)
    #     bbZZ900 = "analysis_May23_2_{}_BGrav_total_SR_minitrees_inpb_wBR/GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-900_narrow_13TeV-madgraph__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root".format(channel)

    #     bbWW900 = "analysis_May23_2_{}_BGrav_total_SR_minitrees_inpb_wBR/GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-300_narrow_13TeV-madgraph_minitree.root".format(channel)
    #     bbWW300 = "analysis_May23_2_{}_BGrav_total_SR_minitrees_inpb_wBR/GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-900_narrow_13TeV-madgraph_minitree.root".format(channel)

    #     TT = "analysis_May23_2_{}_BGrav_total_SR_minitrees_inpb_wBR/TT_TuneCUETP8M2T4_13TeV-powheg-Py8__RunIISummer16MAv2-PUMoriond17_backup_80r2as_2016_TrancheIV_v6-v1_minitree.root".format(channel)
    #     DY1J = "analysis_May23_2_{}_BGrav_total_SR_minitrees_inpb_wBR/DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root".format(channel)
    #     DY2J = "analysis_May23_2_{}_BGrav_total_SR_minitrees_inpb_wBR/DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1_minitree.root".format(channel)





    #tree->Draw("leppt0", "leppt0>25 && lep0Iso03 < 0.06 && lep1Iso03 < 0.06 && (abs(lepeta0)<1.5)", "goff")

    if prepareCutFlowData:    
        for f, name in zip([bbZZ300, bbZZ900, bbWW900, bbWW300, TT, DY1J, DY2J], ["bbZZ300", "bbZZ900", "bbWW900", "bbWW300", "TT", "DY1J", "DY2J"]):
            getCutFlowHistogram(f, name)
        makeEffCutFlowPlot(cutFlow_list_of_lists)
    else: # if this data is ready and pasted below, then use it
        dict_effs = {
            'bbZZ300' : [100.0, 100.0, 65.70395335678614, 62.01136559324953, 23.11249969248936, 23.11249969248936, 23.11249969248936, 19.54783635513789, 19.54783635513789, 19.54783635513789, 19.54783635513789],
            'bbZZ900' : [100.0, 100.0, 65.07951737868503, 61.01129794430185, 26.38105975197294, 26.38105975197294, 26.38105975197294, 21.81510710259301, 21.81510710259301, 21.81510710259301, 21.81510710259301],
            
            'bbWW900' : [100.0, 76.30156472261736, 51.180654338549076, 48.193456614509245, 17.780938833570413, 17.780938833570413, 17.780938833570413, 0.5405405405405406, 0.5405405405405406, 0.5405405405405406, 0.5405405405405406],
            
            'bbWW300' : [100.0, 77.77698712018785, 51.51213264071728, 47.92570981285135, 20.486728812353235, 20.486728812353235, 20.486728812353235, 0.74717142247207, 0.74717142247207, 0.74717142247207, 0.74717142247207],
            
            'DY1J' :[100.0, 100.0, 66.90181826819159, 62.347240531585136, 0.28028170686808945, 0.2790940725169535, 0.2790940725169535, 0.2648424603033218, 0.2648424603033218, 0.2648424603033218, 0.2648424603033218],
            
            'DY2J' : [100.0, 100.0, 66.55185610409491, 62.12593549347281, 0.585480716077731, 0.5853478334821618, 0.5853478334821618, 0.5624920270442658, 0.5624920270442658, 0.5624920270442658, 0.5624920270442658]

            }
        makeEffCutFlowPlot(dict_effs)

