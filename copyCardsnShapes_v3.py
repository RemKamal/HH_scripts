import subprocess
import time, os
import sys
import itertools
import multiprocessing

start_time = time.time()
trueRun = True
doManuallyLastStep = True

dest = '/afs/cern.ch/user/r/rkamalie/workspace/private/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/test/mytest/'

whenMade = '29_3_' #  _ at the end is important!                                   
outputDirDate = '_oct31/'



dest = dest + outputDirDate[1:] #+ leptType[:-1] 
pref, postf = 'analysis_oct', '_total_SR_minitrees_inpb_wBR'
dirs = [pref + whenMade + ll + postf + '/' for ll in ['eles', 'muons']]
print 'dirs = ', dirs

#sys.exit(1)
#os.makedirs (dest, 0755 )
physRegion = ['SR', 'CRDY', 'CRTT']
firstPass_ee_systUnc = [
    #'nominal',
    'CMS_eff_b_lfUp', 'CMS_eff_b_hfUp',
    #'CMS_eff_m_IDUp', 'CMS_eff_m_ISOUp', 'CMS_eff_m_trackerUp', 'CMS_eff_m_triggerUp',                                                         
    'CMS_eff_e_IDUp', 'CMS_eff_e_trackerUp', 'CMS_eff_e_triggerUp',
    'CMS_eff_met_JetEnUp', 'CMS_eff_met_UnclusteredEnUp', 'CMS_eff_met_JetResUp', 'CMS_scale_jUp', 'CMS_res_jUp',

    'CMS_eff_b_lfDown', 'CMS_eff_b_hfDown',
    #'CMS_eff_m_IDDown', 'CMS_eff_m_ISODown', 'CMS_eff_m_trackerDown', 'CMS_eff_m_triggerDown',                                                \
                                                                                                                                                
    'CMS_eff_e_IDDown', 'CMS_eff_e_trackerDown', 'CMS_eff_e_triggerDown',
    'CMS_eff_met_JetEnDown', 'CMS_eff_met_UnclusteredEnDown',
    'CMS_eff_met_JetResDown', 'CMS_scale_jDown', 'CMS_res_jDown'
    ]




firstPass_mm_systUnc = [
    #'nominal',
    'CMS_eff_b_lfUp', 'CMS_eff_b_hfUp', 'CMS_eff_m_IDUp', 'CMS_eff_m_ISOUp', 'CMS_eff_m_trackerUp', 'CMS_eff_m_triggerUp',
    #'CMS_eff_e_IDUp', 'CMS_eff_e_trackerUp', 'CMS_eff_e_triggerUp',                                                                           \
                                                                                                                                                
    'CMS_eff_met_JetEnUp', 'CMS_eff_met_UnclusteredEnUp', 'CMS_eff_met_JetResUp', 'CMS_scale_jUp', 'CMS_res_jUp',

    'CMS_eff_b_lfDown', 'CMS_eff_b_hfDown', 'CMS_eff_m_IDDown', 'CMS_eff_m_ISODown', 'CMS_eff_m_trackerDown', 'CMS_eff_m_triggerDown',
    #'CMS_eff_e_IDDown', 'CMS_eff_e_trackerDown', 'CMS_eff_e_triggerDown',                                                                     \
                                                                                                                                                
    'CMS_eff_met_JetEnDown', 'CMS_eff_met_UnclusteredEnDown',
    'CMS_eff_met_JetResDown', 'CMS_scale_jDown', 'CMS_res_jDown'
    ]

#secondPass_mm_systUnc = firstPass_mm_systUnc[1:] + firstPass_mm_systUnc[:1]
#secondPass_ee_systUnc = firstPass_ee_systUnc[1:] + firstPass_ee_systUnc[:1]

mm_bdtCuts = [0.1, 0.7, 0.99]
ee_bdtCuts = [0.4, 0.925, 0.99]


def parallCopy(cmd):
    # ('analysis_oct29_3_muons_total_SR_minitrees_inpb_wBR/',  'nominal',  'SR',  0.99,  650)
    start_timxe = time.time()

    directo, systUnc, physRegion, bdtCut, mass = str(cmd[0]), str(cmd[1]), str(cmd[2]), float(cmd [3]), int(cmd[4])
    inDir = directo + 'shapes_' + systUnc + '/'
    print '*'*100
    if mass <= 450 and bdtCut > 0.925: exit(1)
    if mass  > 450 and bdtCut < 0.99: exit(1)
    massRegion = 'low' if bdtCut < 0.99 else 'high' if bdtCut >= 0.99 else None
    if massRegion == None or massRegion not in ['low', 'high']: 
        print 'check massRegion'
        sys.exit(1)
    leptType = 'mm_' if 'muons' in directo else 'ee_' if 'eles' in directo else None
    if leptType == None or leptType not in ['mm_', 'ee_'] :
        print 'check leptType'
        sys.exit(1)
    cardsdir = inDir + str(massRegion) + '_' + str(physRegion) + '_' + str(bdtCut)
    outDir = leptType + str(massRegion) + '_' + str(bdtCut) + outputDirDate + str(mass)
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
    command1 = 'cp -r ' +  cardsdir + '/plots/makeDataCards/' + str(mass) + '/' + leptType + '*' + systUnc + '* ' + outDir
    command2 = 'cp -r ' + cardsdir + '/plots/makeDataCards/' + str(mass) + '/d* ' + outDir
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
    print "---it took {hours} hours, {minutes} minutes and {seconds:.1f} seconds to run the analysis ---".format (hours=hours, minutes=minutes,seconds=seconds)
    print '='*50


def parallAddShapes(cmd):
    # ('analysis_oct29_3_muons_total_SR_minitrees_inpb_wBR/',  'nominal',  'SR',  0.99,  650)                                                                                                                                                              
    start_time = time.time()

    directo, systUnc, physRegion, bdtCut, mass = str(cmd[0]), str(cmd[1]), str(cmd[2]), float(cmd [3]), int(cmd[4])
    inDir = directo + 'shapes_' + systUnc + '/'
    print '*'*100
    if mass <= 450 and bdtCut > 0.925: exit(1)
    if mass  > 450 and bdtCut < 0.99: exit(1)
    massRegion = 'low' if bdtCut < 0.99 else 'high' if bdtCut >= 0.99 else None
    if massRegion == None or massRegion not in ['low', 'high']:
        print 'check massRegion'
        sys.exit(1)
    leptType = 'mm_' if 'muons' in directo else 'ee_' if 'eles' in directo else None
    if leptType == None or leptType not in ['mm_', 'ee_'] :
        print 'check leptType'
        sys.exit(1)



    cardsdir = inDir + str(massRegion) + '_' + str(physRegion) + '_' + str(bdtCut)
    outDir = leptType + str(massRegion) + '_' + str(bdtCut) + outputDirDate + str(mass)
    print 'cardsdir={0} and outDir={1}'.format( cardsdir, outDir)

    command3 = 'cp ' + outDir + '/' + leptType + str(physRegion) + '_' + systUnc + '.input.root ' + outDir + '/' + leptType  + str(physRegion) + '.input.root'
    command4 = 'rootcp ' + outDir + '/' + leptType + str(physRegion) + '_' + systUnc + '.input.root:' + leptType + str(physRegion) + '/*' + systUnc + ' ' + outDir + '/' + leptType + str(physRegion) +  '.input.root:' + leptType + str(physRegion)
    #  2175  rootcp mm_SR_JECUp.input.root:mm_SR/*JECUp mm_SR_JECDown.input.root:mm_SR/*JECDown mm_SR.input.root:mm_SR

    print 
    if systUnc == 'nominal':
        print 'command3 is', command3
    #mm_CRDY_CMS_eff_b_lfUp.input.root
    if systUnc != 'nominal':
        print 'command4 is', command4
    if trueRun and systUnc == 'nominal':
        #                        pass
        subprocess.call(command3, shell=True)
        #time.sleep(1)
    if trueRun and systUnc != 'nominal': 
        subprocess.call(command4, shell=True)
        #time.sleep(1)
    print '='*50


    end_time = time.time()
    time_taken = end_time - start_time # time_taken is in seconds                                                                                                                                                                                          
    hours, rest = divmod(time_taken,3600)
    minutes, seconds = divmod(rest, 60)
    print
    print "---it took {hours} hours, {minutes} minutes and {seconds:.1f} seconds to run the analysis ---".format (hours=hours, minutes=minutes,seconds=seconds)
    print '='*50



masses = [260, 270, 300, 350, 400, 450,        600, 650, 900, 1000]
#masses = [250, 260, 270, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 900, 1000]



nomin_ee_low = [dirs[:1], ['nominal'], physRegion, ee_bdtCuts[:2], masses[:6]]
nomin_ee_high = [dirs[:1], ['nominal'], physRegion, ee_bdtCuts[2:], masses[6:]]

nomin_mm_low = [dirs[1:], ['nominal'], physRegion, mm_bdtCuts[:2], masses[:6]]
nomin_mm_high = [dirs[1:], ['nominal'], physRegion, mm_bdtCuts[2:], masses[6:]]


nomin_ee_low_params = list(itertools.product(*nomin_ee_low))
nomin_ee_high_params = list(itertools.product(*nomin_ee_high))

nomin_mm_low_params = list(itertools.product(*nomin_mm_low))
nomin_mm_high_params = list(itertools.product(*nomin_mm_high))



# ee_low = [dirs[:1], firstPass_ee_systUnc, physRegion, ee_bdtCuts[:2], masses[:6]]
# ee_high = [dirs[:1], firstPass_ee_systUnc, physRegion, ee_bdtCuts[2:], masses[6:]]

# mm_low = [dirs[1:], firstPass_mm_systUnc, physRegion, mm_bdtCuts[:2], masses[:6]]
# mm_high = [dirs[1:], firstPass_mm_systUnc, physRegion, mm_bdtCuts[2:], masses[6:]]


# ee_low_params = list(itertools.product(*ee_low))
# ee_high_params = list(itertools.product(*ee_high))

# mm_low_params = list(itertools.product(*mm_low))
# mm_high_params = list(itertools.product(*mm_high))




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



pool = multiprocessing.Pool(16)#32                                                                                              

    ################### IMPORTANT to keep NOMINAL the FIRST in the syst list!!!!!!!!!!!!!!!!!!!!!!
pool.map(parallCopy, nomin_ee_low_params )
pool.map(parallCopy, nomin_mm_low_params )
pool.map(parallCopy, nomin_ee_high_params )
pool.map(parallCopy, nomin_mm_high_params )


# pool.map(parallCopy, ee_low_params )
# pool.map(parallCopy, mm_low_params )
# pool.map(parallCopy, ee_high_params )
# pool.map(parallCopy, mm_high_params )



print 
print '~/~'*2000
print


# pool.map(parallAddShapes, nomin_ee_low_params )
# pool.map(parallAddShapes, nomin_mm_low_params )
# pool.map(parallAddShapes, nomin_ee_high_params )
# pool.map(parallAddShapes, nomin_mm_high_params )


pool = multiprocessing.Pool(1)#!!!!!!!!!!!!!!  not 32, nor 16
if doManuallyLastStep:
    pass
#runCmd3n4manually()
else:
    pool.map(parallAddShapes, ee_low_params )
    pool.map(parallAddShapes, mm_low_params )
    pool.map(parallAddShapes, ee_high_params )
    pool.map(parallAddShapes, mm_high_params )
    

#sys.exit(1)

print
print '=/='*2000
print


cpCommand = 'cp -r ' + '{mm,ee}'  + '_*' + outputDirDate[:-1] + ' ' + dest  
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
print "---it took {hours} hours, {minutes} minutes and {seconds:.1f} seconds to run the analysis ---".format (hours=hours, minutes=minutes, seconds=seconds) 


