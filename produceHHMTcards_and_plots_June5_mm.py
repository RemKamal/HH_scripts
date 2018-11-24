import subprocess
import time
import numpy as np
import sys
import multiprocessing

start_time = time.time()

cardsOnly = True
plotsOnly = False
doPostFit = False
trueRun = True
nominalOnly = False
applyBR = False

debugMode = False

regions = ["SR", "CRTT", "CRDY"] #, "CRDYlow", "CRDYhigh", "CRDYoneBin", "CRTToneBin"]              
pref, postf = 'analysis_May', '_total_SR_minitrees_inpb_wBR'
#whenMade = '16_btagMedium_' #  _ at the end is important!

masses = [250, 260, 270, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 900, 1000]
#masses = [270, 300, 350, 400, 450]

metCuts = [40, 75, 100]

whenMade = '25_{}_'
if len(sys.argv) > 1:
    version_of_JSON_for_plotting = int(sys.argv[1])
    print 'all is fine, using', version_of_JSON_for_plotting
else:
    
    print 'not specified "version_of_JSON_for_plotting", please specify which version_of_JSON_for_plotting of json to use, default must be "3" (THREE for datacards), and 2 when runSimple*'
    sys.exit(1)

if len(sys.argv) > 2:
    leptType = str(sys.argv[2])
    print 'all is fine, using', leptType 
else:

    print 'not specified "leptType", please specify which version_of_JSON_for_plotting of json to use'
    sys.exit(1)

if leptType not in ['eles', 'muons']:
    print 'wrong leptType, use "eles" or "muons"'
    sys.exit(1)


if len(sys.argv) > 3:
    massR = str(sys.argv[3])
    if massR in ['low', 'high']:
        print 'all is fine, processing mass region =>', massR
    else: 
        print 'wrongly specified "massR"'
        sys.exit(1)
else:
    print 'not specified "massR", please specify which one to use'
    sys.exit(1)


if len(sys.argv) > 4:
    plotter = str(sys.argv[4])
    if 'plotter_v14_indev_v' in plotter:
        print 'all is fine'
    else:
        print 'wrongly specified plotter'
        sys.exit(1)
else:
    print 'not specified "pltter*", please specify which one to use'
    sys.exit(1)

if len(sys.argv) > 5:
    HHtype = str(sys.argv[5])
    if 'BGrav' in HHtype or "Radion" in HHtype:
        print 'all is fine'
    else:
        print 'wrongly specified HHtype, exiting'
        sys.exit(1)
else:
    print 'not specified HHtype, please specify which one to use'
    sys.exit(1)




whenMade += HHtype
# if not directo:
#     print 'wrong input, please use "directory"'
#     sys.exit(1)


# dir with low and high regions, not inside of them!
#directory = 'analysis_oct16_2_muons_total_SR_minitrees_inpb_wBR/shapes/'
#analysis_oct18_1_muons_total_SR_minitrees_inpb_wBR/'
#print 'directory is', directory

common_syst = [
    'nominal',
    'CMS_btag_lightUp', 'CMS_btag_heavyUp',
    #'CMS_eff_met_JetEnUp', 'CMS_eff_met_UnclusteredEnUp', 'CMS_eff_met_JetResUp', 
    'CMS_scale_jUp', 'CMS_res_jUp',
    'CMS_btag_lightDown', 'CMS_btag_heavyDown',
    #'CMS_eff_met_JetEnDown', 'CMS_eff_met_UnclusteredEnDown', 'CMS_eff_met_JetResDown', 
    'CMS_scale_jDown', 'CMS_res_jDown'
    
    ]

ee_systUnc = [
    #'nominal',
    #'CMS_btag_lightUp', 'CMS_btag_heavyUp',
    'CMS_eff_e_IDUp', 'CMS_eff_e_trackerUp', 'CMS_eff_e_triggerUp',
    #'CMS_eff_met_JetEnUp', 'CMS_eff_met_UnclusteredEnUp', 'CMS_eff_met_JetResUp', 'CMS_scale_jUp', 'CMS_res_jUp',

    #'CMS_btag_lightDown', 'CMS_btag_heavyDown',
    'CMS_eff_e_IDDown', 'CMS_eff_e_trackerDown', 'CMS_eff_e_triggerDown',
    #'CMS_eff_met_JetEnDown', 'CMS_eff_met_UnclusteredEnDown', 'CMS_eff_met_JetResDown', 'CMS_scale_jDown', 'CMS_res_jDown'
    ]




mm_systUnc = [
    #'nominal',
    #'CMS_btag_lightUp', 'CMS_btag_heavyUp', 
    'CMS_eff_m_IDUp', 'CMS_eff_m_ISOUp', 'CMS_eff_m_trackerUp', 'CMS_eff_m_triggerUp',
    #'CMS_eff_met_JetEnUp', 'CMS_eff_met_UnclusteredEnUp', 'CMS_eff_met_JetResUp', 'CMS_scale_jUp', 'CMS_res_jUp',

    #'CMS_btag_lightDown', 'CMS_btag_heavyDown', 
    'CMS_eff_m_IDDown', 'CMS_eff_m_ISODown', 'CMS_eff_m_trackerDown', 'CMS_eff_m_triggerDown',
    #'CMS_eff_met_JetEnDown', 'CMS_eff_met_UnclusteredEnDown', 'CMS_eff_met_JetResDown', 'CMS_scale_jDown', 'CMS_res_jDown'
    ]

ee_systUnc = common_syst + ee_systUnc
mm_systUnc = common_syst + mm_systUnc


if leptType == 'muons':
    #directo = pref + whenMade + leptType + postf
#for bdtCut in [0.1, 0.7, 0.99]:  # muons based on oct27 study                                         
    bdtCuts = [0.1, 0.7, 0.99]
    systUnc = mm_systUnc

elif leptType == 'eles':
    #directo = pref + whenMade + leptType + postf
#[0.4, 0.925, 0.99]: # electrons based on oct27 study                                                         
    bdtCuts = [0.4, 0.925, 0.99]
    systUnc = ee_systUnc
else:
    print 'wrong directo, exiting.'
    sys.exit(1)
directo = pref + whenMade.format(leptType) + postf
#analysis_May25_{}_BGrav_eles_total_SR_minitrees_inpb_wBR
#analysis_May25_eles_BGrav_total_SR_minitrees_inpb_wBR

print 'working with', directo
#sys.exit(1)


    
if nominalOnly:
    systUnc = ['nominal']
if not directo.endswith('/'):
    directo += '/'

print directo

if debugMode:
    systUnc = ["CMS_btag_heavyUp"]
    regions = ["CRTT"]
    masses = [600]
    metCuts = [100]
    bdtCuts = [0.99]


def parallCall(cmd):
    start_time = time.time()

    command, syst = cmd[0], cmd[1]
    print '*'*100
    print command
    print syst
    directory = directo + 'shapes_' + syst + '/'
    print 'using multiprocessing.cpu_count() = {0}'.format(multiprocessing.cpu_count() )
    command = 'python  ' + plotter + ' -i ' + directory + command 
    print command
    print syst
    #time.sleep(3)
    if trueRun:
        subprocess.call(command+syst, shell=True)

    end_time = time.time()
    time_taken = end_time - start_time # time_taken is in seconds          
    hours, rest = divmod(time_taken,3600)
    minutes, seconds = divmod(rest, 60)
    print
    print "---it took {hours} hours, {minutes} minutes and {seconds:.1f} seconds to run the analysis ---".format (hours=hours, minutes=minutes, seconds=seconds)





#sys.exit(1)


kinds = [' -k Stack ', ' -k makeDataCards ']
if plotsOnly:
    kinds = [' -k Stack ']
if cardsOnly:
    kinds = [' -k makeDataCards ']

jsonFile = 'new_toMakeDataCard_samples_1pb_{}_{}.json'.format(leptType, HHtype)
#jsonFile = 'toMakeDataCard_samples_1pb_bbZZ_{0}_with_bbVV_v{1}.json'.format(leptType, version_of_JSON_for_plotting)
print 'will use jsonFile', jsonFile
 #'samples_1fb_total.json' if '1' in directory else 'samples_june13_tot_hzz.json'
#jsonFile = 'toMakeDataCard_samples_1pb_bbZZ_muons_with_bbVV_v2.json' #'samples_1fb_total.json' if '1' in directory else 'samples_june13_tot_hzz.json'
#jsonFile = 'toMakeDataCard_samples_1pb_bbZZ_muons_with_bbVV_v4.json' #'samples_1fb_total.json' if '1' in directory else 'samples_june13_tot_hzz.json'
#jsonFile = 'toMakeDataCard_samples_1pb_bbZZ_muons_with_bbVV_v5.json' #'samples_1fb_total.json' if '1' in directory else 'samples_june13_tot_hzz.json'
#jsonFile = 'toMakeDataCard_samples_1pb_bbZZ_muons_with_bbVV_v6.json' #'samples_1fb_total.json' if '1' in directory else 'samples_june13_tot_hzz.json'

#sys.exit(1)

leptonType = '0' if 'muons' == leptType else '1' if 'eles' == leptType else None


doPostFit = '' if not doPostFit else ' --doPostFit True '

if leptonType is None:
    print 'check leptonType'
    sys.exit(1)

for massRegion in [massR]:#'low',
    print 'doing massRegion ', massRegion
    print 

#for systUnc in ['nominal']:#, 'JECUp', 'JECDown']:#, 'JERUp', 'JERDown', 'eff_mUp', 'eff_mDown', 'btag_lightUp', 'btag_lightDown', 'btag_heavyUp', 'btag_heavyDown' ]:    
    for mass in masses:
        if massRegion == 'low' and mass > 450: continue
        if massRegion == 'high' and mass <  450: continue
        print 'processing mass ', mass
        
        for bdtCut in bdtCuts:#-0.9, -0.7, -0.5, -0.3, -0.1,  0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.825, 0.85, 0.9, 0.925, 0.95, 0.99]:#[0.5]:#[-0.9, -0.5,  0, 0.4, 0.5, 0.8, 0.825, 0.85, 0.9, 0.925, 0.95, 0.99]:#[-0.9, -0.7, -0.5, -0.3, 0, 0.2, 0.5, 0.8, 0.9]:#np.arange(-0.9, 1.0, 0.1):   #[-0.24, -0.11, 0., 0.11, 0.24]:
            if mass > 450 and bdtCut < 0.99: continue
            if (mass ==  450 and bdtCut != 0.7 and 'muons' in leptType) or (mass == 450 and bdtCut != 0.925 and 'eles' in leptType): continue
            if mass < 450 and bdtCut > 0.925: continue

            print 'using bdtCut', str(bdtCut)
            
            for physRegion in regions:#["SR"]:#, "CRTT", "CRDY", "CRDYlow", "CRDYhigh", "CRDYoneBin", "CRTToneBin"]:              
                print 'working with physRegion ', physRegion
                for kind in kinds:
                    print 'Doing option', kind[4:-1]
                    br = ''
                    if 'make' in kind[4:-1]:
                        br = ' --branchingRatio ' if applyBR else ''
                    
                    print 'br is ', br

                    for metcut in metCuts:
                        if metcut == 40 and massRegion == 'high':
                            continue
                        elif metcut == 100 and massRegion == 'low':
                            continue
                        else:
                            pass

                        if leptType == 'eles':
                            if metcut != 75 and bdtCut == 0.925: continue
                        elif leptType == 'muons':
                            if metcut != 40 and bdtCut == 0.1: continue
                            if metcut == 100 and bdtCut == 0.7: continue
                        else:
                            print 'check leptType, this cannot happen, exiting....'
                            sys.exit(1)


                        command = str(massRegion) + '_' + str(physRegion) + '_' + str(bdtCut) + '_met' + str(metcut) + '  -j data/' + jsonFile + kind + ' -r ' + str(physRegion) + ' -m ' + str(mass) + ' -l 35900 -b ' + str(bdtCut) + br + ' --channel2run ' + leptonType + doPostFit + ' --systUnc '
                        print 'command in main script', command
                        typ = tuple([command, x] for x in systUnc )
                        pool = multiprocessing.Pool(4)#32     
                        print 'before map'
                        pool.map(parallCall, typ )
                    #if trueRun:
                     #   subprocess.call(command, shell=True)

                        print 'after map'
                        print
                print '='*50 



end_time = time.time()
time_taken = end_time - start_time # time_taken is in seconds                                                           
                                                                                                                         
hours, rest = divmod(time_taken,3600)
minutes, seconds = divmod(rest, 60)
print
print "---it took {hours} hours, {minutes} minutes and {seconds:.1f} seconds to run the analysis ---".format (hours=hours, minutes=minutes, seconds=seconds) 


