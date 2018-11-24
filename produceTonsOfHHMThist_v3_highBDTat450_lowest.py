import subprocess
import time
import numpy as np
import sys
import multiprocessing
from pprint import pprint as pp

trueRun = True
onlyNominalRun = False
debugRun = False

if len(sys.argv) > 0:
    readerPythonFile = sys.argv[1]
    if 'py' in readerPythonFile:
        print 'all is fine, using', readerPythonFile
    else:
        print 'wrong input, please use "reader" python file'
        sys.exit(1)
else:
    print 'not specified "readerPythonFile", please use "createHHMTforCombine_reader_v4_1pb_noBR_noBDTcut_inCRs_Zm10p10_Hm35p25.py" or so'


if len(sys.argv) > 1:
    mRegion = sys.argv[2]
    if 'low' in mRegion or 'high' in mRegion:
        print 'all is fine, using', mRegion
    else:
        print 'wrong input, please use right mass region'
        sys.exit(1)
else:
    print 'not specified mass region: low or high, exiting...'
    sys.exit(1)


if len(sys.argv) > 2:
    leptType = sys.argv[3]
    if 'mm' in leptType or 'ee' in leptType:
        print 'all is fine, using', leptType
    else:
        print 'wrong input, please use right leptType: mm or ee'
        sys.exit(1)
else:
    print 'not specified leptType: mm or ee'
    sys.exit(1)

ee_systUnc = [
    'nominal', 
    'CMS_eff_b_lightUp', 'CMS_eff_b_heavyUp', 
    #'CMS_eff_m_IDUp', 'CMS_eff_m_ISOUp', 'CMS_eff_m_trackerUp', 'CMS_eff_m_triggerUp', 
    'CMS_eff_e_IDUp', 'CMS_eff_e_trackerUp', 'CMS_eff_e_triggerUp', 
    'CMS_eff_met_JetEnUp', 'CMS_eff_met_UnclusteredEnUp', 'CMS_eff_met_JetResUp', 'CMS_scale_jUp', 'CMS_res_jUp',
    
    'CMS_eff_b_lightDown', 'CMS_eff_b_heavyDown', 
    #'CMS_eff_m_IDDown', 'CMS_eff_m_ISODown', 'CMS_eff_m_trackerDown', 'CMS_eff_m_triggerDown', 
    'CMS_eff_e_IDDown', 'CMS_eff_e_trackerDown', 'CMS_eff_e_triggerDown', 
    'CMS_eff_met_JetEnDown', 'CMS_eff_met_UnclusteredEnDown', 
    'CMS_eff_met_JetResDown', 'CMS_scale_jDown', 'CMS_res_jDown'
    ]
    



mm_systUnc = [
    'nominal', 
    'CMS_eff_b_lightUp', 'CMS_eff_b_heavyUp', 'CMS_eff_m_IDUp', 'CMS_eff_m_ISOUp', 'CMS_eff_m_trackerUp', 'CMS_eff_m_triggerUp', 
    #'CMS_eff_e_IDUp', 'CMS_eff_e_trackerUp', 'CMS_eff_e_triggerUp', 
    'CMS_eff_met_JetEnUp', 'CMS_eff_met_UnclusteredEnUp', 'CMS_eff_met_JetResUp', 'CMS_scale_jUp', 'CMS_res_jUp',
    
    'CMS_eff_b_lightDown', 'CMS_eff_b_heavyDown', 'CMS_eff_m_IDDown', 'CMS_eff_m_ISODown', 'CMS_eff_m_trackerDown', 'CMS_eff_m_triggerDown', 
    #'CMS_eff_e_IDDown', 'CMS_eff_e_trackerDown', 'CMS_eff_e_triggerDown', 
    'CMS_eff_met_JetEnDown', 'CMS_eff_met_UnclusteredEnDown', 
    'CMS_eff_met_JetResDown', 'CMS_scale_jDown', 'CMS_res_jDown'
    ]

if debugRun:
    mm_systUnc = ee_systUnc = [
        'nominal', 
        'CMS_eff_b_lightUp', 'CMS_eff_b_heavyUp', 
        'CMS_eff_b_lightDown', 'CMS_eff_b_heavyDown',
        ]


if leptType == 'mm':
#for bdtCut in [0.1, 0.7, 0.99]:  # muons based on oct27 study               
    bdtCuts = [0.1]
    #bdtCuts = [0.99]
    systUnc = mm_systUnc
elif leptType == 'ee':
#[0.4, 0.925, 0.99]: # electrons based on oct27 study  
    bdtCuts = [0.4]
    #bdtCuts = [0.99]
    systUnc = ee_systUnc
else:
    print 'wrong bdtCuts, exiting...'
    sys.exit(1)
 
if onlyNominalRun:
    systUnc = ['nominal']

def parallCall(cmd):
    command, syst = cmd[0], cmd[1]
    print 'using multiprocessing.cpu_count() = {0}'.format(multiprocessing.cpu_count() )
    print command, syst
    if trueRun:
        subprocess.call(command+syst, shell=True)



start_time = time.time()

for massRegion in [mRegion]:
                     
    print 'doing massRegion ', massRegion
    print 
    for physRegion in ['SR', 'CRDY', 'CRTT']:
        print 'processing physRegion ', physRegion
        for bdtCut in bdtCuts:#[0.4, 0.925, 0.99]: # electrons based on oct27 study
            #for bdtCut in [0.1, 0.7, 0.99]:  # muons based on oct27 study

#-0.9, -0.7, -0.5, -0.3, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.825, 0.85, 0.9, 0.925, 0.95, 0.99]:#np.arange(-0.9, 1.0, 0.1):    #[0.24]:#-0.24, -0.11, 0, 0.11, 0.24]:
       #     if massRegion == 'low' and bdtCut > 0.925: continue
            #if massRegion == 'high' and bdtCut != 0.7: continue

            command = 'python ' + str(readerPythonFile) + ' ./  TMVAClassification250_450_BDT.weights.xml,TMVAClassification500_1000_BDT.weights.xml ' + str(physRegion) + ' ' + str(bdtCut) + ' ' + str(massRegion) + ' ' 
            typ = tuple([command, x] for x in systUnc )
            pool = multiprocessing.Pool(32)#16
            pool.map(parallCall, typ )


            #time.sleep(90)
            print
        print '='*50
        




end_time = time.time()
time_taken = end_time - start_time # time_taken is in seconds                                                           

hours, rest = divmod(time_taken,3600)
minutes, seconds = divmod(rest, 60)
print
print "---it took {hours} hours, {minutes} minutes and {seconds:.1f} seconds to run the analysis ---".format (hours=hours, minutes=minutes, seconds=seconds) 


