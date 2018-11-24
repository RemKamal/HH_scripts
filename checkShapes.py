from ROOT import TFile
import ROOT
import glob
import sys
import subprocess
import time
start_time = time.time()

trueRunROOTCP = True

dateOfInterest = 'jan6'
shapeInputs =  glob.glob('*' + dateOfInterest + '/*/*inputs.root')

#fname = 'mm_SR.input.root'
#innerDir = 'mm_SR'
tmpfile  = 'new_mm.root'

shapes_ee = ['ST', 'TT', 'DY', 'ZH', 'VV', 'signal_hww', 'signal_hzz', 'data_obs', 'ST_CMS_eff_e_trackerUp', 'TT_CMS_eff_e_trackerUp', 'DY_CMS_eff_e_trackerUp', 'ZH_CMS_eff_e_trackerUp', 'VV_CMS_eff_e_trackerUp', 'signal_hww_CMS_eff_e_trackerUp', 'signal_hzz_CMS_eff_e_trackerUp', 'ST_CMS_btag_lightUp', 'TT_CMS_btag_lightUp', 'DY_CMS_btag_lightUp', 'ZH_CMS_btag_lightUp', 'VV_CMS_btag_lightUp', 'signal_hww_CMS_btag_lightUp', 'signal_hzz_CMS_btag_lightUp', 'ST_CMS_eff_e_IDUp', 'TT_CMS_eff_e_IDUp', 'DY_CMS_eff_e_IDUp', 'ZH_CMS_eff_e_IDUp', 'VV_CMS_eff_e_IDUp', 'signal_hww_CMS_eff_e_IDUp', 'signal_hzz_CMS_eff_e_IDUp', 'ST_CMS_eff_e_triggerUp', 'TT_CMS_eff_e_triggerUp', 'DY_CMS_eff_e_triggerUp', 'ZH_CMS_eff_e_triggerUp', 'VV_CMS_eff_e_triggerUp', 'signal_hww_CMS_eff_e_triggerUp', 'signal_hzz_CMS_eff_e_triggerUp', 'ST_CMS_btag_heavyUp', 'TT_CMS_btag_heavyUp', 'DY_CMS_btag_heavyUp', 'ZH_CMS_btag_heavyUp', 'VV_CMS_btag_heavyUp', 'signal_hww_CMS_btag_heavyUp', 'signal_hzz_CMS_btag_heavyUp', 'ST_CMS_scale_jUp', 'TT_CMS_scale_jUp', 'DY_CMS_scale_jUp', 'ZH_CMS_scale_jUp', 'VV_CMS_scale_jUp', 'signal_hww_CMS_scale_jUp', 'signal_hzz_CMS_scale_jUp', 'ST_CMS_eff_met_JetEnUp', 'TT_CMS_eff_met_JetEnUp', 'DY_CMS_eff_met_JetEnUp', 'ZH_CMS_eff_met_JetEnUp', 'VV_CMS_eff_met_JetEnUp', 'signal_hww_CMS_eff_met_JetEnUp', 'signal_hzz_CMS_eff_met_JetEnUp', 'ST_CMS_eff_met_JetResUp', 'TT_CMS_eff_met_JetResUp', 'DY_CMS_eff_met_JetResUp', 'ZH_CMS_eff_met_JetResUp', 'VV_CMS_eff_met_JetResUp', 'signal_hww_CMS_eff_met_JetResUp', 'signal_hzz_CMS_eff_met_JetResUp', 'ST_CMS_res_jUp', 'TT_CMS_res_jUp', 'DY_CMS_res_jUp', 'ZH_CMS_res_jUp', 'VV_CMS_res_jUp', 'signal_hww_CMS_res_jUp', 'signal_hzz_CMS_res_jUp', 'ST_CMS_eff_met_UnclusteredEnUp', 'TT_CMS_eff_met_UnclusteredEnUp', 'DY_CMS_eff_met_UnclusteredEnUp', 'ZH_CMS_eff_met_UnclusteredEnUp', 'VV_CMS_eff_met_UnclusteredEnUp', 'signal_hww_CMS_eff_met_UnclusteredEnUp', 'signal_hzz_CMS_eff_met_UnclusteredEnUp', 'ST_CMS_eff_e_trackerDown', 'TT_CMS_eff_e_trackerDown', 'DY_CMS_eff_e_trackerDown', 'ZH_CMS_eff_e_trackerDown', 'VV_CMS_eff_e_trackerDown', 'signal_hww_CMS_eff_e_trackerDown', 'signal_hzz_CMS_eff_e_trackerDown', 'ST_CMS_btag_lightDown', 'TT_CMS_btag_lightDown', 'DY_CMS_btag_lightDown', 'ZH_CMS_btag_lightDown', 'VV_CMS_btag_lightDown', 'signal_hww_CMS_btag_lightDown', 'signal_hzz_CMS_btag_lightDown', 'ST_CMS_eff_e_IDDown', 'TT_CMS_eff_e_IDDown', 'DY_CMS_eff_e_IDDown', 'ZH_CMS_eff_e_IDDown', 'VV_CMS_eff_e_IDDown', 'signal_hww_CMS_eff_e_IDDown', 'signal_hzz_CMS_eff_e_IDDown', 'ST_CMS_btag_heavyDown', 'TT_CMS_btag_heavyDown', 'DY_CMS_btag_heavyDown', 'ZH_CMS_btag_heavyDown', 'VV_CMS_btag_heavyDown', 'signal_hww_CMS_btag_heavyDown', 'signal_hzz_CMS_btag_heavyDown', 'ST_CMS_eff_e_triggerDown', 'TT_CMS_eff_e_triggerDown', 'DY_CMS_eff_e_triggerDown', 'ZH_CMS_eff_e_triggerDown', 'VV_CMS_eff_e_triggerDown', 'signal_hww_CMS_eff_e_triggerDown', 'signal_hzz_CMS_eff_e_triggerDown', 'ST_CMS_scale_jDown', 'TT_CMS_scale_jDown', 'DY_CMS_scale_jDown', 'ZH_CMS_scale_jDown', 'VV_CMS_scale_jDown', 'signal_hww_CMS_scale_jDown', 'signal_hzz_CMS_scale_jDown', 'ST_CMS_eff_met_JetEnDown', 'TT_CMS_eff_met_JetEnDown', 'DY_CMS_eff_met_JetEnDown', 'ZH_CMS_eff_met_JetEnDown', 'VV_CMS_eff_met_JetEnDown', 'signal_hww_CMS_eff_met_JetEnDown', 'signal_hzz_CMS_eff_met_JetEnDown', 'ST_CMS_eff_met_JetResDown', 'TT_CMS_eff_met_JetResDown', 'DY_CMS_eff_met_JetResDown', 'ZH_CMS_eff_met_JetResDown', 'VV_CMS_eff_met_JetResDown', 'signal_hww_CMS_eff_met_JetResDown', 'signal_hzz_CMS_eff_met_JetResDown', 'ST_CMS_eff_met_UnclusteredEnDown', 'TT_CMS_eff_met_UnclusteredEnDown', 'DY_CMS_eff_met_UnclusteredEnDown', 'ZH_CMS_eff_met_UnclusteredEnDown', 'VV_CMS_eff_met_UnclusteredEnDown', 'signal_hww_CMS_eff_met_UnclusteredEnDown', 'signal_hzz_CMS_eff_met_UnclusteredEnDown', 'ST_CMS_res_jDown', 'TT_CMS_res_jDown', 'DY_CMS_res_jDown', 'ZH_CMS_res_jDown', 'VV_CMS_res_jDown', 'signal_hww_CMS_res_jDown', 'signal_hzz_CMS_res_jDown']

shapes_mm = ['ST', 'TT', 'DY', 'ZH', 'VV', 'signal_hww', 'signal_hzz', 'data_obs', 'ST_CMS_btag_heavyUp', 'TT_CMS_btag_heavyUp', 'DY_CMS_btag_heavyUp', 'ZH_CMS_btag_heavyUp', 'VV_CMS_btag_heavyUp', 'signal_hww_CMS_btag_heavyUp', 'signal_hzz_CMS_btag_heavyUp', 'ST_CMS_eff_m_trackerUp', 'TT_CMS_eff_m_trackerUp', 'DY_CMS_eff_m_trackerUp', 'ZH_CMS_eff_m_trackerUp', 'VV_CMS_eff_m_trackerUp', 'signal_hww_CMS_eff_m_trackerUp', 'signal_hzz_CMS_eff_m_trackerUp', 'ST_CMS_eff_m_IDUp', 'TT_CMS_eff_m_IDUp', 'DY_CMS_eff_m_IDUp', 'ZH_CMS_eff_m_IDUp', 'VV_CMS_eff_m_IDUp', 'signal_hww_CMS_eff_m_IDUp', 'signal_hzz_CMS_eff_m_IDUp', 'ST_CMS_btag_lightUp', 'TT_CMS_btag_lightUp', 'DY_CMS_btag_lightUp', 'ZH_CMS_btag_lightUp', 'VV_CMS_btag_lightUp', 'signal_hww_CMS_btag_lightUp', 'signal_hzz_CMS_btag_lightUp', 'ST_CMS_eff_m_triggerUp', 'TT_CMS_eff_m_triggerUp', 'DY_CMS_eff_m_triggerUp', 'ZH_CMS_eff_m_triggerUp', 'VV_CMS_eff_m_triggerUp', 'signal_hww_CMS_eff_m_triggerUp', 'signal_hzz_CMS_eff_m_triggerUp', 'ST_CMS_eff_m_ISOUp', 'TT_CMS_eff_m_ISOUp', 'DY_CMS_eff_m_ISOUp', 'ZH_CMS_eff_m_ISOUp', 'VV_CMS_eff_m_ISOUp', 'signal_hww_CMS_eff_m_ISOUp', 'signal_hzz_CMS_eff_m_ISOUp', 'ST_CMS_res_jUp', 'TT_CMS_res_jUp', 'DY_CMS_res_jUp', 'ZH_CMS_res_jUp', 'VV_CMS_res_jUp', 'signal_hww_CMS_res_jUp', 'signal_hzz_CMS_res_jUp', 'ST_CMS_eff_met_JetResUp', 'TT_CMS_eff_met_JetResUp', 'DY_CMS_eff_met_JetResUp', 'ZH_CMS_eff_met_JetResUp', 'VV_CMS_eff_met_JetResUp', 'signal_hww_CMS_eff_met_JetResUp', 'signal_hzz_CMS_eff_met_JetResUp', 'ST_CMS_eff_met_JetEnUp', 'TT_CMS_eff_met_JetEnUp', 'DY_CMS_eff_met_JetEnUp', 'ZH_CMS_eff_met_JetEnUp', 'VV_CMS_eff_met_JetEnUp', 'signal_hww_CMS_eff_met_JetEnUp', 'signal_hzz_CMS_eff_met_JetEnUp', 'ST_CMS_eff_met_UnclusteredEnUp', 'TT_CMS_eff_met_UnclusteredEnUp', 'DY_CMS_eff_met_UnclusteredEnUp', 'ZH_CMS_eff_met_UnclusteredEnUp', 'VV_CMS_eff_met_UnclusteredEnUp', 'signal_hww_CMS_eff_met_UnclusteredEnUp', 'signal_hzz_CMS_eff_met_UnclusteredEnUp', 'ST_CMS_scale_jUp', 'TT_CMS_scale_jUp', 'DY_CMS_scale_jUp', 'ZH_CMS_scale_jUp', 'VV_CMS_scale_jUp', 'signal_hww_CMS_scale_jUp', 'signal_hzz_CMS_scale_jUp', 'ST_CMS_btag_heavyDown', 'TT_CMS_btag_heavyDown', 'DY_CMS_btag_heavyDown', 'ZH_CMS_btag_heavyDown', 'VV_CMS_btag_heavyDown', 'signal_hww_CMS_btag_heavyDown', 'signal_hzz_CMS_btag_heavyDown', 'ST_CMS_eff_m_trackerDown', 'TT_CMS_eff_m_trackerDown', 'DY_CMS_eff_m_trackerDown', 'ZH_CMS_eff_m_trackerDown', 'VV_CMS_eff_m_trackerDown', 'signal_hww_CMS_eff_m_trackerDown', 'signal_hzz_CMS_eff_m_trackerDown', 'ST_CMS_btag_lightDown', 'TT_CMS_btag_lightDown', 'DY_CMS_btag_lightDown', 'ZH_CMS_btag_lightDown', 'VV_CMS_btag_lightDown', 'signal_hww_CMS_btag_lightDown', 'signal_hzz_CMS_btag_lightDown', 'ST_CMS_eff_m_IDDown', 'TT_CMS_eff_m_IDDown', 'DY_CMS_eff_m_IDDown', 'ZH_CMS_eff_m_IDDown', 'VV_CMS_eff_m_IDDown', 'signal_hww_CMS_eff_m_IDDown', 'signal_hzz_CMS_eff_m_IDDown', 'ST_CMS_eff_m_ISODown', 'TT_CMS_eff_m_ISODown', 'DY_CMS_eff_m_ISODown', 'ZH_CMS_eff_m_ISODown', 'VV_CMS_eff_m_ISODown', 'signal_hww_CMS_eff_m_ISODown', 'signal_hzz_CMS_eff_m_ISODown', 'ST_CMS_eff_m_triggerDown', 'TT_CMS_eff_m_triggerDown', 'DY_CMS_eff_m_triggerDown', 'ZH_CMS_eff_m_triggerDown', 'VV_CMS_eff_m_triggerDown', 'signal_hww_CMS_eff_m_triggerDown', 'signal_hzz_CMS_eff_m_triggerDown', 'ST_CMS_res_jDown', 'TT_CMS_res_jDown', 'DY_CMS_res_jDown', 'ZH_CMS_res_jDown', 'VV_CMS_res_jDown', 'signal_hww_CMS_res_jDown', 'signal_hzz_CMS_res_jDown', 'ST_CMS_eff_met_JetEnDown', 'TT_CMS_eff_met_JetEnDown', 'DY_CMS_eff_met_JetEnDown', 'ZH_CMS_eff_met_JetEnDown', 'VV_CMS_eff_met_JetEnDown', 'signal_hww_CMS_eff_met_JetEnDown', 'signal_hzz_CMS_eff_met_JetEnDown', 'ST_CMS_eff_met_JetResDown', 'TT_CMS_eff_met_JetResDown', 'DY_CMS_eff_met_JetResDown', 'ZH_CMS_eff_met_JetResDown', 'VV_CMS_eff_met_JetResDown', 'signal_hww_CMS_eff_met_JetResDown', 'signal_hzz_CMS_eff_met_JetResDown', 'ST_CMS_eff_met_UnclusteredEnDown', 'TT_CMS_eff_met_UnclusteredEnDown', 'DY_CMS_eff_met_UnclusteredEnDown', 'ZH_CMS_eff_met_UnclusteredEnDown', 'VV_CMS_eff_met_UnclusteredEnDown', 'signal_hww_CMS_eff_met_UnclusteredEnDown', 'signal_hzz_CMS_eff_met_UnclusteredEnDown', 'ST_CMS_scale_jDown', 'TT_CMS_scale_jDown', 'DY_CMS_scale_jDown', 'ZH_CMS_scale_jDown', 'VV_CMS_scale_jDown', 'signal_hww_CMS_scale_jDown', 'signal_hzz_CMS_scale_jDown']

baddirs = []


def read3(fname):
    print '>',
    #mm_low_0.7_jan5/450/bdt_response_afterCut_mm_CRDY.input.root
    shapes_file = ROOT.TFile.Open(fname)
    # print 'tfile path is', shapes_file
    # print 'list of keys'
    # print 'list of Keys is', ROOT.gDirectory.GetListOfKeys().ls()
    # print 'gonna cd'

    idx2 = fname.find('inputs.root')
    suff = '_mm_' if 'mm' in fname else '_ee_'

    idx1 = fname.find(suff)
    innerDir = fname[idx1+1: idx2-1]

    shapes_file.cd(innerDir)
    shapes = ROOT.gDirectory.GetListOfKeys()
    hists = []
    shapeNames = []
    #print shapes
     
        # Since the nominal and varied shapes share the same binning,
        # take any of the histograms found in the shapes file.
    #print 'len(shapes) = ', len(shapes) 
    for idx, shape in enumerate(shapes):
        shape = ROOT.gDirectory.Get(shapes[idx].GetName())
        #print 'before draw'
        #shape.Print()
        shapeNames.append(shapes[idx].GetName())
        hists.append (shape)
        
    if ('mm' in fname and len(hists) != 162) or ('ee' in fname and len(hists) != 148):
        #if '1000' in fname and 'CRDY' in fname:
         #   return

        print
        print 'wrong N of shapes in {0} is {1}'.format(len(hists), fname)
        #print 'shapes_{0} = '.format(str(idx))
        #print shapeNames
        print set(shapeNames).symmetric_difference(set(shapes_ee) if 'ee' in fname else set(shapes_mm))
        missingSyst = list (set(shapeNames).symmetric_difference(set(shapes_ee) if 'ee' in fname else set(shapes_mm)))
        #print missingSyst
        STsyst = [i for i in missingSyst if i.startswith('ST')]
        systUnc = STsyst[0][3:]
        pref = 'analysis_jan1_1_{0}_total_SR_minitrees_inpb_wBR/shapes_{1}/'.format('eles' if 'ee' in fname else 'muons', systUnc)
        srcFile = fname.split(innerDir)[0] + systUnc + '_' + innerDir + '.input.root'
        print srcFile
        commandROOTCP = 'rootcp ' + srcFile + ':' + innerDir +  '/*' + systUnc + ' ' + fname + ':' + innerDir

        print commandROOTCP
        if trueRunROOTCP:
            subprocess.call(commandROOTCP, shell=True)
        print ' '*100


    return

    if False:
            #inp = ROOT.TFile.Open(inputfile,'read')
        output = ROOT.TFile.Open(tmpfile,'recreate')
        output.mkdir(innerDir)
        output.cd(innerDir)
        for h in hists:
            h.Write()#key.GetName())
        output.Close()
        
        # obj = ROOT.TObject
        # for key in ROOT.gDirectory.GetListOfKeys():
        #         #inp.cd()
        #     obj = key.ReadObj()
        #         #if obj.GetName() == job.tree:
        #         #   continue
        #     output.cd()
        #     obj.Write(key.GetName())
        # outfile.Close()
        # infile.Close()



#ONLY example 3 is working!!!!!!!!!!!!!!!!!
def read1():
    hnames = []
    tfile = TFile.Open(fname)
    for key in tfile.GetListOfKeys():
        h = key.ReadObj()
        if h.ClassName() == 'TH1F' or h.ClassName() == 'TH2F':
            hnames.append(h.GetName())
    print hnames

def read2():
    tfile = TFile.Open(fname)
    tfile.cd("mm_SR")
    for h in tfile.GetListOfKeys():
        h = h.ReadObj()
        print h.ClassName(), h.GetName()



#read1()
#read2()
#read3()



#print shapeInputs


#sys.exit(1)
for rootFile in shapeInputs:
    #mm_low_0.7_jan5/450/bdt_response_afterCut_mm_CRDY.input.root
    read3(rootFile)




end_time = time.time()
time_taken = end_time - start_time # time_taken is in seconds                                                                                

hours, rest = divmod(time_taken,3600)
minutes, seconds = divmod(rest, 60)
print
print 'all done!'
print "---it took {hours} hours, {minutes} minutes and {seconds:.1f} seconds to run the analysis ---".format (hours=hours, minutes=minutes, seconds=seconds)

