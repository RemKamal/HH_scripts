import subprocess
import time, os
import sys

start_time = time.time()
trueRun = True

#analysis_oct16_2_muons_total_SR_minitrees_inpb_wBR/shapes_JECDown/low_CRTT_0.5/plots/makeDataCards/260
#analysis_oct16_2_muons_total_SR_minitrees_inpb_wBR/shapes_JECDown/high_CRTT_0.95/plots/makeDataCards/1000

dest = '/afs/cern.ch/user/r/rkamalie/workspace/private/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/test/mytest/oct19_2017'

directo = 'analysis_oct16_2_muons_total_SR_minitrees_inpb_wBR/'



# inDir = None
# if len(sys.argv) > 1:
#     inDir = sys.argv[1]#'analysis_apr23_total_SR_v3/'
# else:# or not inDir:
#     print 'syntax: python copyCardsnShapes....py <indir/>, indir is not provided, specify location of low/high dirs, exiting...'
#     sys.exit(1)

# if not inDir or '/' not in inDir:
#     print 'syntax: python copyCardsnShapes....py <indir/>, indir has to have "/" at the end, exiting...'
#     sys.exit(1)

# print inDir
masses = [260, 270, 300, 350, 400, 450, 600, 650, 900, 1000]
#masses = [250, 260, 270, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 900, 1000]

date = '_oct19/'


for massRegion in ['low', 'high']:
    
    print 'doing massRegion ', massRegion
    print 



    ################### IMPORTANT to keep NOMINAL the FIRST!!!!!!!!!!!!!!!!!!!!!!
    for systUnc in ['nominal', 'JECUp', 'JECDown']:#, 'JERUp', 'JERDown', 'eff_mUp', 'eff_mDown', 'eff_b_lfUp', 'eff_b_lfDown', 'eff_b_hfUp', 'eff_b_hfDown' ]:    
        inDir = directo + 'shapes_' + systUnc + '/'


        for physRegion in ['SR', 'CRDY', 'CRTT']:
            print 'processing physRegion ', physRegion
            for bdtCut in [0.5, 0.95]: #-0.24, -0.11, 0, 0.11, 0.24]:
                for mass in masses:
                    if mass <= 450 and massRegion =='low':
                        if bdtCut == 0.95: continue
                    elif mass > 450 and massRegion =='high':
                        if bdtCut == 0.5: continue
                    else:
                        #print 'skipping, since mass is {0} and massRegion is {1}'.format(mass, massRegion)
                        continue

                # if mass == 'low' and bdtCut == 0.95: continue
                # if mass == 'high' and bdtCut == 0.5: continue


                    cardsdir = str(massRegion) + '_' + str(physRegion) + '_' + str(bdtCut)
                    outDir = str(massRegion) + '_' + str(bdtCut) + date + str(mass)
                    print 'cardsdir={0} and outDir={1}'.format( cardsdir, outDir)
                    if not os.path.exists (outDir):
                        print 'creating', outDir
                        os.makedirs (outDir)
                    command1 = 'cp -r ' + inDir + cardsdir + '/plots/makeDataCards/' + str(mass) + '/m*' + systUnc + '* ' + outDir 
                    command2 = 'cp -r ' + inDir + cardsdir + '/plots/makeDataCards/' + str(mass) + '/d* ' + outDir 
                    #command3 = 'cp ' + outDir + '/mm_' + str(physRegion) + '_' + systUnc + '.input.root ' + outDir + '/mm_' + str(physRegion) + '.input.root'


                    print command1
                    if systUnc == 'nominal': 
                        print command2
                    #print '>'*80
                    #print 'command3 is', command3
                    if trueRun:
                        subprocess.call(command1, shell=True)
                        if systUnc == 'nominal': 
                            subprocess.call(command2, shell=True)
            #time.sleep(90)
            print '='*50
        #cpCommand = 'cp -r ' + str(massRegion) + '_*' + date + ' ' + dest  
        #print cpCommand
        print 
        #if trueRun:
         #   subprocess.call(cpCommand, shell=True)


print 
print '~/~'*200
print


for massRegion in ['low', 'high']:
    
    print 'doing massRegion ', massRegion
    print 



    ################### IMPORTANT to keep NOMINAL the FIRST!!!!!!!!!!!!!!!!!!!!!!
    for systUnc in ['nominal', 'JECUp', 'JECDown']:#, 'JERUp', 'JERDown', 'eff_mUp', 'eff_mDown', 'eff_b_lfUp', 'eff_b_lfDown', 'eff_b_hfUp', 'eff_b_hfDown' ]:    
        inDir = directo + 'shapes_' + systUnc + '/'


        for physRegion in ['SR', 'CRDY', 'CRTT']:
            print 'processing physRegion ', physRegion
            for bdtCut in [0.5, 0.95]: #-0.24, -0.11, 0, 0.11, 0.24]:
                for mass in masses:
                    if mass <= 450 and massRegion =='low':
                        if bdtCut == 0.95: continue
                    elif mass > 450 and massRegion =='high':
                        if bdtCut == 0.5: continue
                    else:
                        #print 'skipping, since mass is {0} and massRegion is {1}'.format(mass, massRegion)
                        continue

                # if mass == 'low' and bdtCut == 0.95: continue
                # if mass == 'high' and bdtCut == 0.5: continue


                    cardsdir = str(massRegion) + '_' + str(physRegion) + '_' + str(bdtCut)
                    outDir = str(massRegion) + '_' + str(bdtCut) + date + str(mass)
                    print 'cardsdir={0} and outDir={1}'.format( cardsdir, outDir)
                    if not os.path.exists (outDir):
                        print 'creating', outDir
                        os.makedirs (outDir)
                    #command1 = 'cp -r ' + inDir + cardsdir + '/plots/makeDataCards/' + str(mass) + '/m*' + systUnc + '* ' + outDir 
                    #command2 = 'cp -r ' + inDir + cardsdir + '/plots/makeDataCards/' + str(mass) + '/d* ' + outDir 
                    command3 = 'cp ' + outDir + '/mm_' + str(physRegion) + '_' + systUnc + '.input.root ' + outDir + '/mm_' + str(physRegion) + '.input.root'
                    command4 = 'rootcp ' + outDir + '/mm_' + str(physRegion) + '_' + systUnc + '.input.root:mm_' + str(physRegion) + '/*' + systUnc + ' ' + outDir + '/mm_' + str(physRegion) +  '.input.root:mm_' + str(physRegion)
                      #  2175  rootcp mm_SR_JECUp.input.root:mm_SR/*JECUp mm_SR_JECDown.input.root:mm_SR/*JECDown mm_SR.input.root:mm_SR

                    #print command1
                    #if systUnc == 'nominal': 
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
            #time.sleep(90)
            print '='*50
    cpCommand = 'cp -r ' + str(massRegion) + '_*' + date + ' ' + dest  
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


