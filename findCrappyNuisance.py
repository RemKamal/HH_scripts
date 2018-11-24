import sys
import subprocess
from multiprocessing import Pool

ee_systUnc = [
    #'nominal',
    #'CMS_btag_lightUp', 'CMS_btag_heavyUp',
    #'CMS_eff_m_IDUp', 'CMS_eff_m_ISOUp', 'CMS_eff_m_trackerUp', 'CMS_eff_m_triggerUp',                                                                                            
    'CMS_eff_e_ID', 'CMS_eff_e_tracker', 'CMS_eff_e_trigger',
    #'CMS_eff_met_JetEn', 'CMS_eff_met_UnclusteredEn', 'CMS_eff_met_JetRes', 'CMS_scale_j', 'CMS_res_j',

    #'CMS_btag_lightDown', 'CMS_btag_heavyDown',
    #'CMS_eff_m_IDDown', 'CMS_eff_m_ISODown', 'CMS_eff_m_trackerDown', 'CMS_eff_m_triggerDown',                                                                                    
    #'CMS_eff_e_IDDown', 'CMS_eff_e_trackerDown', 'CMS_eff_e_triggerDown',
    #'CMS_eff_met_JetEnDown', 'CMS_eff_met_UnclusteredEnDown',
    #'CMS_eff_met_JetResDown', 'CMS_scale_jDown', 'CMS_res_jDown'
    ]




mm_systUnc = [
    #'nominal',
    #'CMS_btag_lightUp', 'CMS_btag_heavyUp', 
    'CMS_eff_m_ID','CMS_eff_m_ISO', 'CMS_eff_m_tracker', 'CMS_eff_m_trigger',
    #'CMS_eff_e_ID', 'CMS_eff_e_tracker', 'CMS_eff_e_trigger',                                                                                                               
    #'CMS_eff_met_JetEnUp', 'CMS_eff_met_UnclusteredEnUp', 'CMS_eff_met_JetResUp', 'CMS_scale_jUp', 'CMS_res_jUp',

    #'CMS_btag_lightDown', 'CMS_btag_heavyDown', 
    #'CMS_eff_m_IDDown', 'CMS_eff_m_ISODown', 'CMS_eff_m_trackerDown', 'CMS_eff_m_triggerDown',
    #'CMS_eff_e_IDDown', 'CMS_eff_e_trackerDown', 'CMS_eff_e_triggerDown',                                                                                                         
    #'CMS_eff_met_JetEnDown', 'CMS_eff_met_UnclusteredEnDown',
    #'CMS_eff_met_JetResDown', 'CMS_scale_jDown', 'CMS_res_jDown'
    ]


common_systUnc = [
    #'nominal',
    'CMS_btag_light', 'CMS_btag_heavy', 
    #'CMS_eff_m_IDUp', 'CMS_eff_m_ISOUp', 'CMS_eff_m_trackerUp', 'CMS_eff_m_triggerUp',
    #'CMS_eff_e_IDUp', 'CMS_eff_e_trackerUp', 'CMS_eff_e_triggerUp',                                                                                                               
    'CMS_eff_met_JetEn', 'CMS_eff_met_UnclusteredEn', 'CMS_eff_met_JetRes', 
    'CMS_scale_j', 'CMS_res_j',

    #'CMS_btag_lightDown', 'CMS_btag_heavyDown', 
    #'CMS_eff_m_IDDown', 'CMS_eff_m_ISODown', 'CMS_eff_m_trackerDown', 'CMS_eff_m_triggerDown',
    #'CMS_eff_e_IDDown', 'CMS_eff_e_trackerDown', 'CMS_eff_e_triggerDown',                                                                                                         
    #'CMS_eff_met_JetEnDown', 'CMS_eff_met_UnclusteredEnDown', 'CMS_eff_met_JetResDown', 
    #'CMS_scale_jDown', 'CMS_res_jDown'
    ]



systList = ee_systUnc + mm_systUnc + common_systUnc

lnNList = ['lumi_13TeV',
           'CMS_pu',
           'pdf_qqbar',
           'pdf_gg',
           'QCDscale_VH',
           'QCDscale_TT',
           'QCDscale_VV',
           'QCDscale_DY',
           'QCDscale_ST',
           'QCDscale_Higgs_HH',
           'xsec_TT',
           'xsec_ST'
           ]

def expectedSignalZero(uncs):
    if len(uncs) > 1:
        logName = 'manyUnc'
    else:
        logName = uncs
    cmd = 'combine -M MaxLikelihoodFit -t -1 --expectSignal 0 -d comb_tot_highCombination_M350.root  --rMin -1000 --rMax 1000 --X-rtd MINIMIZER_analytic -v 3 --freezeParameters ' + uncs + ' >& log_' + logName + '.txt&'
    print 'about to run:'
    print cmd
    subprocess.call(cmd, shell=True)

    


def main():
    p = Pool(4)
    print 'systList:'
    print systList
    print
    #p.map(expectedSignalZero, systList)
    #for syst in systList:
    #expectedSignalZero(syst)
    #expectedSignalZero( ','.join(systList) )
    expectedSignalZero( ','.join(lnNList+systList) )

if __name__ == "__main__":
    sys.exit(main())
