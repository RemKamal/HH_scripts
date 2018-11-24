import subprocess
import time, os
import numpy as np

start_time = time.time()

masses = [260]#, 270, 300, 350, 400, 450, 600, 650, 900, 1000]

curDir = os.getcwd()
fileOfInterest = 'higgsCombineTest.Asymptotic.mH*.root'

for massRegion in ['low']:#, 'high']:
    print 'doing massRegion ', massRegion
    print 
    for bdtCut in np.arange(-0.1, .8, 0.8): #[0.24]: #-0.24, -0.11, 0, 0.11, 0.24]:
        for mass in masses:
            if mass <= 450 and massRegion =='low':
                pass
            elif mass > 450 and massRegion =='high':
                pass
            else:
                print 'skipping, since mass is {0} and massRegion is {1}'.format(mass, massRegion)
                continue
            
            #print curDir
            #tmpDir = curDir + '/' + str(massRegion) + '_' + str(bdtCut) + date + str(mass)
            #tmpDir = curDir + date + str(mass)
            tmpDir = str(mass)
            print 'tmpDir is', tmpDir
            
            
            if os.path.exists (tmpDir):
                print 'change dir to', tmpDir
                os.chdir(tmpDir)
                
            print 'in the directory', os.getcwd()
            commandJoin = 'combineCards.py SR=dataCard_SR.txt CRDY=dataCard_CRDY.txt CRTT=dataCard_CRTT.txt > comb_' + str(mass) + '.txt'
            commandFit = 'combine -M Asymptotic -t -1 -m ' + str(mass) + ' comb_' + str(mass) + '.txt' 
            print commandJoin
            print commandFit
            cpCommand = 'cp ' + fileOfInterest + ' ' + curDir
            print cpCommand
        
            subprocess.call(commandJoin, shell=True)
            subprocess.call(commandFit, shell=True)
            subprocess.call(cpCommand, shell=True)

            print 'change dir to', curDir
            os.chdir(curDir)
    print '='*50


end_time = time.time()
time_taken = end_time - start_time # time_taken is in seconds                                                           
                                                                                                                         
hours, rest = divmod(time_taken,3600)
minutes, seconds = divmod(rest, 60)
print
print "---it took {hours} hours, {minutes} minutes and {seconds:.1f} seconds to run the analysis ---".format (hours=hours, minutes=minutes, seconds=seconds) 


