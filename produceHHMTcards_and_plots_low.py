import subprocess
import time
import numpy as np

start_time = time.time()
directory = 'analysis_apr23_total_SR_v3/' + '1pb_newCuts_signal_noBDTcut_inCRs/'
masses = [260, 400]#, 270, 300, 350, 400, 450, 600, 650, 900, 1000]
applyBR = True

kinds = [' -k Stack ', ' -k makeDataCards ']

jsonFile = 'toMakeDataCard_samples_1pb_total.json' #'samples_1fb_total.json' if '1' in directory else 'samples_june13_tot_hzz.json'
for massRegion in ['low']:#, 'high']:
    print 'doing massRegion ', massRegion
    print 
    for mass in masses:
        if massRegion == 'low' and mass > 450: continue
        if massRegion == 'high' and mass <=  450: continue
        print 'processing mass ', mass

        for bdtCut in [0.5]:#[-0.9, -0.5,  0, 0.4, 0.5, 0.8, 0.825, 0.85, 0.9, 0.925, 0.95, 0.99]:#[-0.9, -0.7, -0.5, -0.3, 0, 0.2, 0.5, 0.8, 0.9]:#np.arange(-0.9, 1.0, 0.1):   #[-0.24, -0.11, 0., 0.11, 0.24]:
            print 'using bdtCut', str(bdtCut)
            for physRegion in ['SR', 'CRDY', 'CRTT']:              
                print 'working with physRegion ', physRegion
                for kind in kinds:
                    print 'Doing option', kind[4:-1]
                    br = ''
                    if 'make' in kind[4:-1]:
                        br = ' --branchingRatio ' if applyBR else ''
                    
                    print 'br is ', br
                    command = 'python  plotter_v13.py -i ' + directory +  str(massRegion) + '_' + str(physRegion) + '_' + str(bdtCut) + '  -j data/' + jsonFile + kind + ' -r ' + str(physRegion) + ' -m ' + str(mass) + ' -l 35900 -b ' + str(bdtCut) + br
                    print command
                    subprocess.call(command, shell=True)
                    #time.sleep(90)
                    print 
                print '='*50



end_time = time.time()
time_taken = end_time - start_time # time_taken is in seconds                                                           
                                                                                                                         
hours, rest = divmod(time_taken,3600)
minutes, seconds = divmod(rest, 60)
print
print "---it took {hours} hours, {minutes} minutes and {seconds:.1f} seconds to run the analysis ---".format (hours=hours, minutes=minutes, seconds=seconds) 


