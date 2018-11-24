import subprocess
import time

start_time = time.time()

for massRegion in ['low', 'high']:
    print 'doing massRegion ', massRegion
    print 
    for physRegion in ['SR', 'CRDY', 'CRTT']:
        print 'processing physRegion ', physRegion
        for bdtCut in [-0.24, -0.11, 0, 0.11, 0.24]:
            
            command = 'python createHHMTforCombine_reader_v2.py ../minitreesMay29/  TMVAClassification260_450_BDT.weights.xml,TMVAClassification600_1000_BDT.weights.xml ' + str(physRegion) + ' ' + str(bdtCut) + ' ' + str(massRegion)  
            print command
        
            subprocess.call(command, shell=True)
            #time.sleep(90)
        print '='*50


end_time = time.time()
time_taken = end_time - start_time # time_taken is in seconds                                                           
                                                                                                                         
hours, rest = divmod(time_taken,3600)
minutes, seconds = divmod(rest, 60)
print
print "---it took {hours} hours, {minutes} minutes and {seconds:.1f} seconds to run the analysis ---".format (hours=hours, minutes=minutes, seconds=seconds) 


