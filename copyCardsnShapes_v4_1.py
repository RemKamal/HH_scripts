import subprocess
import time, os
import sys
import itertools
import multiprocessing

#import pdb
#import program2debug
#pdb.run('program2debug.test()')


start_time = time.time()

addShapesForOnlyHHmt = False
trueRun = False
doManuallyLastStep = False

doEles = True
doMuons = False


dest = '/afs/cern.ch/user/r/rkamalie/workspace/private/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/test/mytest/'

whenMade = '1_1_' #  _ at the end is important!                                   
outputDirDate = '_jan1/'


leptonsList = []
if doEles:
    leptonsList.append('eles')
if doMuons:
    leptonsList.append('muons')

dest = dest + outputDirDate[1:] #+ leptType[:-1] 
if not os.path.exists(dest):
    os.makedirs(dest)
pref, postf = 'analysis_jan', '_total_SR_minitrees_inpb_wBR'
dirs = [pref + whenMade + ll + postf + '/' for ll in leptonsList]
print 'dirs = ', dirs

#sys.exit(1)
#os.makedirs (dest, 0755 )
physRegion = ["SR", "CRTT", "CRDY", "CRDYlow", "CRDYhigh", "CRDYoneBin", "CRTToneBin"]
massRegion = ['low', 'high']


masses = [260, 270, 300, 350, 400, 450,        600, 650, 900, 1000]
#masses = [250, 260, 270, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 900, 1000]


firstPass_ee_systUnc = [
    #'nominal',
    'CMS_btag_lightUp', 'CMS_btag_heavyUp',
    #'CMS_eff_m_IDUp', 'CMS_eff_m_ISOUp', 'CMS_eff_m_trackerUp', 'CMS_eff_m_triggerUp',                                                         
    'CMS_eff_e_IDUp', 'CMS_eff_e_trackerUp', 'CMS_eff_e_triggerUp',
    'CMS_eff_met_JetEnUp', 'CMS_eff_met_UnclusteredEnUp', 'CMS_eff_met_JetResUp', 'CMS_scale_jUp', 'CMS_res_jUp',

    'CMS_btag_lightDown', 'CMS_btag_heavyDown',
    #'CMS_eff_m_IDDown', 'CMS_eff_m_ISODown', 'CMS_eff_m_trackerDown', 'CMS_eff_m_triggerDown',                                                \
                                                                                                                                                
    'CMS_eff_e_IDDown', 'CMS_eff_e_trackerDown', 'CMS_eff_e_triggerDown',
    'CMS_eff_met_JetEnDown', 'CMS_eff_met_UnclusteredEnDown',
    'CMS_eff_met_JetResDown', 'CMS_scale_jDown', 'CMS_res_jDown'
    ]




firstPass_mm_systUnc = [
    #'nominal',
    'CMS_btag_lightUp', 'CMS_btag_heavyUp', 'CMS_eff_m_IDUp', 'CMS_eff_m_ISOUp', 'CMS_eff_m_trackerUp', 'CMS_eff_m_triggerUp',
    #'CMS_eff_e_IDUp', 'CMS_eff_e_trackerUp', 'CMS_eff_e_triggerUp',                                                                           \
                                                                                                                                                
    'CMS_eff_met_JetEnUp', 'CMS_eff_met_UnclusteredEnUp', 'CMS_eff_met_JetResUp', 'CMS_scale_jUp', 'CMS_res_jUp',

    'CMS_btag_lightDown', 'CMS_btag_heavyDown', 'CMS_eff_m_IDDown', 'CMS_eff_m_ISODown', 'CMS_eff_m_trackerDown', 'CMS_eff_m_triggerDown',
    #'CMS_eff_e_IDDown', 'CMS_eff_e_trackerDown', 'CMS_eff_e_triggerDown',                                                                     \
                                                                                                                                                
    'CMS_eff_met_JetEnDown', 'CMS_eff_met_UnclusteredEnDown',
    'CMS_eff_met_JetResDown', 'CMS_scale_jDown', 'CMS_res_jDown'
    ]

#secondPass_mm_systUnc = firstPass_mm_systUnc[1:] + firstPass_mm_systUnc[:1]
#secondPass_ee_systUnc = firstPass_ee_systUnc[1:] + firstPass_ee_systUnc[:1]

mm_bdtCuts = [0.1, 0.7, 0.99]
ee_bdtCuts = [0.4, 0.925, 0.99]

bdt_vars = [
    "bdt_response",
    "bdt_response_afterCut",
    "dR_bjets",
    "dR_leps",
    "hhMt",
    "hmass0",
    "hmass1",
    "hmass1_oneBin",
    "hpt0",
    "hpt1",
    "met_pt",
    "zmass",
    "zmass_high",
    "zmass_oneBin",
    "zpt0"
]

def parallCopy(cmd):
    print 'in parallCopy'
    # ('analysis_oct29_3_muons_total_SR_minitrees_inpb_wBR/',  'nominal',  'SR',  0.99,  650)
    start_timxe = time.time()

    directo, systUnc, physRegion, bdtCut, mass, massReg = str(cmd[0]), str(cmd[1]), str(cmd[2]), float(cmd [3]), int(cmd[4]), str(cmd[5])
    inDir = directo + 'shapes_' + systUnc + '/'
    print '*'*100
    print cmd


    if 260 <= mass <= 270:
        if doMuons and bdtCut == 0.1:
            pass
        elif doEles and bdtCut == 0.4:
            pass
        else:
            return
    elif 300 <= mass <= 350:
        if doMuons and bdtCut == 0.7:
            pass
        elif doEles and bdtCut == 0.4:
            pass
        else:
            return
        
    elif 400 <= mass <= 450:
        if doMuons and bdtCut == 0.7:
            pass
        elif doEles and bdtCut == 0.925:
            pass
        else:
            return
        
    elif 600 <= mass <= 1000:
        if doMuons and bdtCut == 0.99:
            pass
        elif doEles and bdtCut == 0.99:
            pass
        else:
            return
        
    else:
        print 'cannott happen'
        sys.exit(1)

    # if (mass == 260 and  bdtCut != 0.1 and doMuons) or (mass == 270 and  bdtCut != 0.925 and doEles): 
    #     return
    # if mass > 450 and bdtCut < 0.99: return #pass#sys.exit(1)
    # if mass < 450 and bdtCut > 0.925: return #sys.exit(1)
    # if (mass == 450 and  bdtCut != 0.7 and doMuons) or (mass == 450 and  bdtCut != 0.925 and doEles): 
    #     #print 'stuck in tricky mass'
    #     return #pass#sys.exit(1)
    print 'after mass cuts'
    #massReg = 'low' if bdtCut < 0.99 else 'high' if bdtCut >= 0.99 else None
    if massReg == None or massReg not in ['low', 'high']: 
        print 'check massReg'
        sys.exit(1)
    leptType = 'mm_' if 'muons' in directo else 'ee_' if 'eles' in directo else None
    if leptType == None or leptType not in ['mm_', 'ee_'] :
        print 'check leptType'
        sys.exit(1)
    cardsdir = inDir + str(massReg) + '_' + str(physRegion) + '_' + str(bdtCut)
    outDir = leptType + str(massReg) + '_' + str(bdtCut) + outputDirDate + str(mass)
    print 'cardsdir={0} and outDir={1}'.format( cardsdir, outDir)
    path = outDir
    if not os.path.exists (outDir):
        print 'creating', outDir
        if trueRun: #os.makedirs (outDir)
            #https://stackoverflow.com/questions/27978889/python-2-6-file-exists-errno-17
            #https://stackoverflow.com/questions/12468022/python-fileexists-error-when-making-directory
            try:
                os.makedirs(path, 0755)
            except OSError as e:
                if e.errno == 17:  # errno.EEXIST
                    os.chmod(path, 0755)

    command1 = 'rsync --exclude "hists_*" ' + cardsdir + '/plots/makeDataCards/' + str(mass) + '/*root ' + outDir
    command2 = 'cp -r ' + cardsdir + '/plots/makeDataCards/' + str(mass) + '/d* ' + outDir

    # command1 = 'cp -r ' +  cardsdir + '/plots/makeDataCards/' + str(mass) + '/' + leptType + '*' + systUnc + '* ' + outDir
    # command2 = 'cp -r ' + cardsdir + '/plots/makeDataCards/' + str(mass) + '/d* ' + outDir

    print 'command1:', command1
    if systUnc == 'nominal':
        print 'command2:', command2
    if trueRun:
        subprocess.call(command1, shell=True)
        if systUnc == 'nominal':
            subprocess.call(command2, shell=True)
            #time.sleep(90)                                                                                                                                                                 
    

    end_time = time.time()
    time_taken = end_time - start_time # time_taken is in seconds                                                                               
    hours, rest = divmod(time_taken,3600)
    minutes, seconds = divmod(rest, 60)
    print
    print "---for 'parallCopy' it took {hours} hours, {minutes} minutes and {seconds:.1f} seconds to run the analysis ---".format (hours=hours, minutes=minutes,seconds=seconds)
    print '='*50


def parallAddShapes(cmd):
    print 'in parallAddShapes'
    # ('analysis_oct29_3_muons_total_SR_minitrees_inpb_wBR/',  'nominal',  'SR',  0.99,  650)                                                                                                                                                              
    start_time = time.time()

    directo, systUnc, physRegion, bdtCut, mass, massReg = str(cmd[0]), str(cmd[1]), str(cmd[2]), float(cmd [3]), int(cmd[4]), str(cmd[5])

    var = 'hhMt'
    if not addShapesForOnlyHHmt:
        var = str(cmd[6])

    var += '_'
    inDir = directo + 'shapes_' + systUnc + '/'
    print '*'*100


    if 260 <= mass <= 270:
        if doMuons and bdtCut == 0.1:
            pass
        elif doEles and bdtCut == 0.4:
            pass
        else:
            return
    elif 300 <= mass <= 350:
        if doMuons and bdtCut == 0.7:
            pass
        elif doEles and bdtCut == 0.4:
            pass
        else:
            return
        
    elif 400 <= mass <= 450:
        if doMuons and bdtCut == 0.7:
            pass
        elif doEles and bdtCut == 0.925:
            pass
        else:
            return
        
    elif 600 <= mass <= 1000:
        if doMuons and bdtCut == 0.99:
            pass
        elif doEles and bdtCut == 0.99:
            pass
        else:
            return
        
    else:
        print 'cannott happen'
        sys.exit(1)

    # if mass > 450 and bdtCut < 0.99: return #sys.exit(1)
    # if mass < 450 and bdtCut > 0.925: return #sys.exit(1)
    # if (mass == 450 and  bdtCut != 0.7 and doMuons) or (mass == 450 and  bdtCut != 0.925 and doEles):
    #     #print 'stuck in tricky mass'
    #     return #pass#sys.exit(1)

    # if mass <= 450 and bdtCut > 0.925: exit(1)
    # if mass  > 450 and bdtCut < 0.99: exit(1)
    #massReg = 'low' if bdtCut < 0.99 else 'high' if bdtCut >= 0.99 else None
    if massReg == None or massReg not in ['low', 'high']:
        print 'check massReg'
        sys.exit(1)
    leptType = 'mm_' if 'muons' in directo else 'ee_' if 'eles' in directo else None
    if leptType == None or leptType not in ['mm_', 'ee_'] :
        print 'check leptType'
        sys.exit(1)



    cardsdir = inDir + str(massReg) + '_' + str(physRegion) + '_' + str(bdtCut)
    outDir = leptType + str(massReg) + '_' + str(bdtCut) + outputDirDate + str(mass)
    print 'cardsdir={0} and outDir={1}'.format( cardsdir, outDir)
    
    
    # command3 = 'cp ' + outDir + '/' + leptType + str(physRegion) + '_' + systUnc + '.input.root ' + outDir + '/' + leptType  + str(physRegion) + '.input.root'
    # if systUnc == 'nominal':
    #     print 'command3 is', command3
    # if trueRun and systUnc == 'nominal':
    #     #                        pass
    #     subprocess.call(command3, shell=True)
    #     #time.sleep(1)



    command4 = 'rootcp ' + outDir + '/' + var + systUnc + '_' + leptType + str(physRegion) + '.input.root:' + leptType + str(physRegion) + '/*' + systUnc + ' ' + outDir + '/' + var + systUnc + '_' + leptType + str(physRegion) +  '.input.root:' + leptType + str(physRegion)
    #command4 = 'rootcp ' + outDir + '/' + var + leptType + str(physRegion) + '_' + systUnc + '.input.root:' + leptType + str(physRegion) + '/*' + systUnc + ' ' + outDir + '/' + var + leptType + str(physRegion) +  '.input.root:' + leptType + str(physRegion)
    #  2175  rootcp mm_SR_JECUp.input.root:mm_SR/*JECUp mm_SR_JECDown.input.root:mm_SR/*JECDown mm_SR.input.root:mm_SR

    print 
    #mm_CRDY_CMS_btag_lightUp.input.root
    if systUnc != 'nominal':
        print 'command4 is', command4
    if trueRun and systUnc != 'nominal': 
        subprocess.call(command4, shell=True)
        #time.sleep(1)
    print '='*50


    end_time = time.time()
    time_taken = end_time - start_time # time_taken is in seconds                                                                                                                                                                                          
    hours, rest = divmod(time_taken,3600)
    minutes, seconds = divmod(rest, 60)
    print
    print "---For 'parallAddShapes' it took {hours} hours, {minutes} minutes and {seconds:.1f} seconds to run the analysis ---".format (hours=hours, minutes=minutes,seconds=seconds)
    print '='*50






def runCmd3n4manually():
    #NEED fix for directo, bdtcuts, etc
    for massRegion in ['low', 'high']:

        print
        'doing massRegion ', massRegion
        print

        ################### IMPORTANT to keep NOMINAL the FIRST!!!!!!!!!!!!!!!!!!!!!!                                                                                                                                                                                                                                     
        for systUnc in ['nominal', 'JECUp', 'JECDown']:                                                                                                                                                         
            inDir = directo + 'shapes_' + systUnc + '/'

            for physRegion in ['SR', 'CRDY', 'CRTT']:
                print 'processing physRegion ', physRegion
                for bdtCut in [0.5, 0.95]:  # -0.24, -0.11, 0, 0.11, 0.24]:                                                                                                                                                                                                                                                 
                    for mass in masses:
                        if mass <= 450 and massRegion == 'low':
                            if bdtCut == 0.95: continue
                        elif mass > 450 and massRegion == 'high':
                            if bdtCut == 0.5: continue
                        else:
                            # print 'skipping, since mass is {0} and massRegion is {1}'.format(mass, massRegion)                                                                                                                                                                                                           
                            continue

                            # if mass == 'low' and bdtCut == 0.95: continue                                                                                                                                                                                                                                                       
                            # if mass == 'high' and bdtCut == 0.5: continue                                                                                                                                                                                                                                                       

                        cardsdir = str(massRegion) + '_' + str(physRegion) + '_' + str(bdtCut)
                        outDir = str(massRegion) + '_' + str(bdtCut) + outputDirDate + str(mass)
                        print 'cardsdir={0} and outDir={1}'.format(cardsdir, outDir)
                        if not os.path.exists(outDir):
                            print 'creating', outDir
                            os.makedirs(outDir)
                        # command1 = 'cp -r ' + inDir + cardsdir + '/plots/makeDataCards/' + str(mass) + '/m*' + systUnc + '* ' + outDir                                                                                                                                                                                   
                        # command2 = 'cp -r ' + inDir + cardsdir + '/plots/makeDataCards/' + str(mass) + '/d* ' + outDir                                                                                                                                                                                                   
                        command3 = 'cp ' + outDir + '/mm_' + str(
                            physRegion) + '_' + systUnc + '.input.root ' + outDir + '/mm_' + str(
                            physRegion) + '.input.root'
                        command4 = 'rootcp ' + outDir + '/mm_' + str(
                            physRegion) + '_' + systUnc + '.input.root:mm_' + str(
                            physRegion) + '/*' + systUnc + ' ' + outDir + '/mm_' + str(
                            physRegion) + '.input.root:mm_' + str(physRegion)
                        #  2175  rootcp mm_SR_JECUp.input.root:mm_SR/*JECUp mm_SR_JECDown.input.root:mm_SR/*JECDown mm_SR.input.root:mm_SR                                                                                                                                                                              

                        # print command1                                                                                                                                                                                                                                                                                   
                        # if systUnc == 'nominal':                                                                                                                                                                                                                                                                         
                        #   print command2                                                                                                                                                                                                                                                                               
                        print
                        if systUnc == 'nominal':
                            print 'command3 is', command3
                        if systUnc != 'nominal':
                            print 'command4 is', command4
                        if trueRun and systUnc == 'nominal':
                            #                        pass                                                                                                                                                                                                                                                                                         
                            subprocess.call(command3, shell=True)
                        if trueRun and systUnc != 'nominal':
                            subprocess.call(command4, shell=True)
                # time.sleep(90)                                                                                                                                                                                                                                                                                           
                print '=' * 50
        cpCommand = 'cp -r ' + str(massRegion) + '_*' + outputDirDate + ' ' + dest
        print cpCommand
        print
        print
        if trueRun:
            subprocess.call(cpCommand, shell=True)
 

if doEles and doMuons:
    nomin_ee_low = [dirs[:1], ['nominal'], physRegion, ee_bdtCuts[:2], masses[:6], massRegion[:1]]
    nomin_ee_high = [dirs[:1], ['nominal'], physRegion, ee_bdtCuts[1:], masses[5:], massRegion[1:]]
    
    nomin_mm_low = [dirs[1:], ['nominal'], physRegion, mm_bdtCuts[:2], masses[:6], massRegion[:1]]
    nomin_mm_high = [dirs[1:], ['nominal'], physRegion, mm_bdtCuts[1:], masses[5:], massRegion[1:]]

    ee_low = [dirs[:1], firstPass_ee_systUnc, physRegion, ee_bdtCuts[:2], masses[:6], massRegion[:1]]
    ee_high = [dirs[:1], firstPass_ee_systUnc, physRegion, ee_bdtCuts[1:], masses[5:], massRegion[1:]]

    mm_low = [dirs[1:], firstPass_mm_systUnc, physRegion, mm_bdtCuts[:2], masses[:6], massRegion[:1]]
    mm_high = [dirs[1:], firstPass_mm_systUnc, physRegion, mm_bdtCuts[1:], masses[5:], massRegion[1:]]



else:
    #if only one element in the dirs, take it with ':1'
    nomin_ee_low = [dirs[:1], ['nominal'], physRegion, ee_bdtCuts[:2], masses[:6], massRegion[:1]]
    nomin_ee_high = [dirs[:1], ['nominal'], physRegion, ee_bdtCuts[1:], masses[5:], massRegion[1:]]

    nomin_mm_low = [dirs[:1], ['nominal'], physRegion, mm_bdtCuts[:2], masses[:6], massRegion[:1]]
    nomin_mm_high = [dirs[:1], ['nominal'], physRegion, mm_bdtCuts[1:], masses[5:], massRegion[1:]]

    ee_low = [dirs[:1], firstPass_ee_systUnc, physRegion, ee_bdtCuts[:2], masses[:6], massRegion[:1]]
    ee_high = [dirs[:1], firstPass_ee_systUnc, physRegion, ee_bdtCuts[1:], masses[5:], massRegion[1:]]

    mm_low = [dirs[:1], firstPass_mm_systUnc, physRegion, mm_bdtCuts[:2], masses[:6], massRegion[:1]]
    mm_high = [dirs[:1], firstPass_mm_systUnc, physRegion, mm_bdtCuts[1:], masses[5:], massRegion[1:]]




if doEles:
    nomin_ee_low_params = list(itertools.product(*nomin_ee_low))
    nomin_ee_high_params = list(itertools.product(*nomin_ee_high))
    ee_low_params = list(itertools.product(*ee_low))
    ee_high_params = list(itertools.product(*ee_high))

if doMuons:
    nomin_mm_low_params = list(itertools.product(*nomin_mm_low))
    nomin_mm_high_params = list(itertools.product(*nomin_mm_high))
    mm_low_params = list(itertools.product(*mm_low))
    mm_high_params = list(itertools.product(*mm_high))


nomin_ee_low_withBdt = nomin_ee_low + [bdt_vars]
nomin_ee_high_withBdt = nomin_ee_high + [bdt_vars]

nomin_mm_low_withBdt = nomin_mm_low + [bdt_vars]
nomin_mm_high_withBdt = nomin_mm_high + [bdt_vars]

ee_low_withBdt = ee_low + [bdt_vars]
ee_high_withBdt = ee_high + [bdt_vars]

mm_low_withBdt = mm_low  + [bdt_vars]
mm_high_withBdt = mm_high + [bdt_vars]

if doEles:
    nomin_ee_low_params_withBdt = list(itertools.product(*nomin_ee_low_withBdt))
    nomin_ee_high_params_withBdt = list(itertools.product(*nomin_ee_high_withBdt))
    ee_low_params_withBdt = list(itertools.product(*ee_low_withBdt))
    ee_high_params_withBdt = list(itertools.product(*ee_high_withBdt))

if doMuons:
    nomin_mm_low_params_withBdt = list(itertools.product(*nomin_mm_low_withBdt))
    nomin_mm_high_params_withBdt = list(itertools.product(*nomin_mm_high_withBdt))
    mm_low_params_withBdt = list(itertools.product(*mm_low_withBdt))
    mm_high_params_withBdt = list(itertools.product(*mm_high_withBdt))




pool = multiprocessing.Pool(16)  #32                                                                                              
print ' ' *1000

#print nomin_ee_low_params
print 
#print ee_low_params
    ################### IMPORTANT to keep NOMINAL the FIRST in the syst list!!!!!!!!!!!!!!!!!!!!!!
print 'before map for eles'
if doEles:
    print 'before ee nominal pass'
    try:
        pool.map(parallCopy, nomin_ee_low_params )
    except Exception as e:
        print 'error = ', e

    print
    print 'before ee nominal pass for high'
    pool.map(parallCopy, nomin_ee_high_params )

#sys.exit(1)

#if True:
    print 'before ee all non nominal pass'
    #print 'ee_low_params:', ee_low_params
    pool.map(parallCopy, ee_low_params )
    pool.map(parallCopy, ee_high_params )

    print 'before ee nominal add shapes pass'
    #pool.map(parallAddShapes, nomin_ee_low_params )                                                                   
    #pool.map(parallAddShapes, nomin_ee_high_params )                                                                  

print 'before map for muons'
if doMuons:
    pool.map(parallCopy, nomin_mm_low_params )
    pool.map(parallCopy, nomin_mm_high_params )
    pool.map(parallCopy, mm_low_params )
    pool.map(parallCopy, mm_high_params )
    #pool.map(parallAddShapes, nomin_mm_low_params )                                                                   
    #pool.map(parallAddShapes, nomin_mm_high_params )                                                                  


print '  '*1000
#print ee_low_params_withBdt
print 
print '~/~'*2000
print 'before last step'

pool = multiprocessing.Pool(16)#!!!!!!!!!!!!!!  not 32, nor 16
if doManuallyLastStep:
    pass
#runCmd3n4manually()
else:
    if doEles:
        pool.map(parallAddShapes, ee_low_params_withBdt )
        pool.map(parallAddShapes, ee_high_params_withBdt )
    if doMuons:
        pool.map(parallAddShapes, mm_low_params_withBdt )
        pool.map(parallAddShapes, mm_high_params_withBdt )
    
    # if doEles:
    #     pool.map(parallAddShapes, ee_low_params )
    #     pool.map(parallAddShapes, ee_high_params )
    # if doMuons:
    #     pool.map(parallAddShapes, mm_low_params )
    #     pool.map(parallAddShapes, mm_high_params )
    

#sys.exit(1)

print
print '=/='*2000
print 'about to copy and be done'

nameLep = '{mm,ee}' if doEles and doMuons else 'ee' if doEles else 'mm' if doMuons else None

if nameLep is None:
    sys.exit(1)
print 'nameLep', nameLep

cpCommand = 'cp -r ' + nameLep  + '_*' + outputDirDate[:-1] + ' ' + dest  
print cpCommand
print 
print 
if trueRun:
    subprocess.call(cpCommand, shell=True)





end_time = time.time()
time_taken = end_time - start_time # time_taken is in seconds                                                           
                                                                                                                         
hours, rest = divmod(time_taken,3600)
minutes, seconds = divmod(rest, 60)
print
print 'all done!'
print "---it took {hours} hours, {minutes} minutes and {seconds:.1f} seconds to run the analysis ---".format (hours=hours, minutes=minutes, seconds=seconds) 


