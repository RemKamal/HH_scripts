import subprocess
import time
import numpy as np
import sys

trueRun = False

if len(sys.argv) > 0:
    readerPythonFile = sys.argv[1]
    if 'py' in readerPythonFile:
        print 'all is fine, using', readerPythonFile
    else:
        print 'wrong input, please use "reader" python file'
        sys.exit(1)
else:
    print 'not specified "readerPythonFile", please use "createHHMTforCombine_reader_v4_1pb_noBR_noBDTcut_inCRs_Zm10p10_Hm35p25.py" or so'

        


start_time = time.time()

for massRegion in ['low', 'high']:
    print 'doing massRegion ', massRegion
    print 
    for physRegion in ['SR', 'CRDY', 'CRTT']:
        print 'processing physRegion ', physRegion
        for bdtCut in [0.5, 0.95]:#-0.9, -0.7, -0.5, -0.3, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.825, 0.85, 0.9, 0.925, 0.95, 0.99]:#np.arange(-0.9, 1.0, 0.1):    #[0.24]:#-0.24, -0.11, 0, 0.11, 0.24]:
            if massRegion == 'low' and bdtCut == 0.95: continue
            if massRegion == 'high' and bdtCut == 0.5: continue

            command = 'python ' + str(readerPythonFile) + ' ./  TMVAClassification250_450_BDT.weights.xml,TMVAClassification500_1000_BDT.weights.xml ' + str(physRegion) + ' ' + str(bdtCut) + ' ' + str(massRegion)  
            print command
            if trueRun:
                subprocess.call(command, shell=True)
            #time.sleep(90)
        print '='*50


end_time = time.time()
time_taken = end_time - start_time # time_taken is in seconds                                                           
                                                                                                                         
hours, rest = divmod(time_taken,3600)
minutes, seconds = divmod(rest, 60)
print
print "---it took {hours} hours, {minutes} minutes and {seconds:.1f} seconds to run the analysis ---".format (hours=hours, minutes=minutes, seconds=seconds) 


