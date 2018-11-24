import subprocess
import time, os, sys
import numpy as np
import glob, re, io
import pickle, itertools
import pprint
pp = pprint.PrettyPrinter(indent=4)
pp = pprint.PrettyPrinter(depth=6)


start_time = time.time()
trueRun = True                     #keep False for debug
run_combine_and_copy_cards = True   #keep False for debug
copy_logs = True
cpLogs = True

# if len(sys.argv) > 0:
#     directo = sys.argv[1]
#     print 'all is fine, using', directo
#     if not directo:
#         print 'wrong input, please use "directory"'
#         sys.exit(1)
# else:
#     print 'not specified "directory", please provide an input'

directo = '.'
masses = [260, 270, 300, 350, 400, 450,         600, 650, 900, 1000]

curDir = os.getcwd()
#fileOfInterest = 'higgsCombineTest.Asymptotic.mH*.root'
#low_CRTT_0.3/plots/makeDataCards/260/

logList = []
date = '_oct19'

if run_combine_and_copy_cards:
    for massRegion in ['low', 'high']:
        print 'doing massRegion ', massRegion
        print 


        for mass in masses:
            if mass <= 450 and massRegion =='low':
                pass
            elif mass > 450 and massRegion =='high':
                pass
            else:
                #print 'skipping, since mass is {0} and massRegion is {1}'.format(mass, massRegion)
                continue
            logList_perMass = []

            
            for bdtCut in [0.5, 0.95]:#[-0.9, -0.7, -0.5, -0.3, -0.1,  0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.825, 0.85, 0.9, 0.925, 0.95, 0.99]: #[-0.9,-0.5,0,0.4,0.5,0.8,0.825,0.85,0.9,0.925,0.95,0.99]:#np.arange(-0.9, 1.0, 0.1): #[0.24]: #-0.24, -0.11, 0, 0.11, 0.24]:
                if bdtCut == 0 or not -1 < bdtCut < 1 or abs(bdtCut) < 0.001: continue 
                # numpy did not create dirs at 0 :(, instead it was created under the name '-2.22044604925e-16'
                if massRegion == 'low' and bdtCut >= 0.95: continue
                if massRegion == 'high' and bdtCut < 0.5: continue


                tmpDir = str(massRegion) + '_' + str(bdtCut) + date + '/' + str(mass) 
                # high_0.95_oct19/650
                if os.path.exists (tmpDir):           
                    print 'change dir to', tmpDir
                    os.chdir(tmpDir)
                print 'tmpDir is', tmpDir 
                logList_perMass.append (directo + '/' + tmpDir + '/log*')
                logList_perMass.append (directo + '/' + tmpDir + '/higgs*')

                # for region in ['CRDY', 'CRTT']:
                #     cp_cards_n_ROOTfiles = 'cp -r ../../../../../' + str(massRegion) + '_' + region + '_' + str(bdtCut) + '/plots/makeDataCards/' +str(mass) + '/test_wo_br/*' + region + '*{txt,root} .' 
                
                #     print cp_cards_n_ROOTfiles
                #     print 'DIRECTORY contains:'; print glob.glob("*R*")
                #tmpDir = str(mass)

            
                

            #cpCommand = 'cp ' + fileOfInterest + ' ' + curDir
            #print cpCommand
                
                    # if trueRun: 
                    #     subprocess.call(cp_cards_n_ROOTfiles, shell=True)
                
                commandJoin = 'combineCards.py SR=dataCard_SR.txt CRDY=dataCard_CRDY.txt CRTT=dataCard_CRTT.txt > comb_' + str(mass) + '.txt'
                commandFit = 'combine -M Asymptotic -t -1 -v 3 --run blind -m ' + str(mass) + ' comb_' + str(mass) + '.txt >& log_comb_M' + str(mass) + '_' + str(bdtCut) + '.txt&' 
                print commandJoin
                print commandFit
            #cpLog = 'cp log* ' + curDir
            #print cpLog

                if trueRun:
                    time.sleep(1)
                    subprocess.call(commandJoin, shell=True)
                    subprocess.call(commandFit, shell=True)
                    time.sleep(20)
                #subprocess.call(cpLog, shell=True)
            
                print 'change dir to', curDir
                os.chdir(curDir)
            print '='*50
            logList.append(logList_perMass)


pp.pprint(logList) 
if run_combine_and_copy_cards: time.sleep(15)


if copy_logs:
    print '\/'*50
    for log_per_mass, mass in itertools.izip_longest(logList, masses):
        print 'log_per_mass is ', log_per_mass
        logPath = 'logs_' + str(mass) #+ '_' + directo #+ '_' + str(log_per_mass.split('_')[-1]) 
        if mass and not os.path.exists(logPath):
            os.makedirs(logPath)
        print 'logPath is ', logPath
        print 'before loop over log_per_mass'
        for log in log_per_mass:
            print 'log is', log
            #if len(str(log)) > 30: continue
            #if mass <= 450 and '_0.9' in log: continue # bdt at +0.9 exists only for high mass region
            #cpLog = 'cp -r ../' + str(log) + ' ' + logPath
            cpLog = 'cp -r ' + str(log) + ' ' + logPath
            print 'cpLog is', cpLog
            print '*'*50
            print
            if cpLogs:
                subprocess.call(cpLog, shell=True)



limits = []
print 'DIRECTORY contains:'; print glob.glob("log*")
for root, dirs, files in os.walk('.'):
#     #print 'root={0}, dirs={1}, files={2}'.format(root, dirs, files) 
    if 'logs' not in root: continue # or 'makeDataCards/' not in root: continue

#     #print 'root={0}, dirs={1}'.format(root, dirs) 
    print 'root is ', root

# # root is  ./low_SR_-0.9/plots/makeDataCards/260
# # root is  ./low_SR_-0.9/plots/makeDataCards/400
# # root is  ./low_SR_-0.8/plots/makeDataCards/260
# # root is  ./low_SR_-0.8/plots/makeDataCards/400

    for fil in files:
        if not fil.endswith('txt') or 'log' not in fil: continue
         #if not fil.endswith('txt'): continue
        #if len(str(fil)) > 30: continue
        if  os.path.getsize(str(root) + '/' + fil) < 10000: continue # to skip corrupted/incomplete logs with errors
        print 'file is', fil
        print os.path.getsize(str(root) + '/' + fil)
        with io.open (str(root) + '/' + fil, mode='r') as f:

            print 'file is', str(root) + '/' +  fil
            text = f.read()
            tmp_limits = re.findall(r"r < (\d*\.\d+|\d+)", text)
            #['0xxx', '0.0755', '0.1009', '0.1411', '0.1990', '0.2700']
            # obs       2.5%      16%       50%      84%      97.5%
            limits.append( (tmp_limits[-5:], fil.split('_')[2][1:], fil.split('_')[-1][:-4]) )

            #         ONLY expected limits        mass              bdt cut value
            
            #  Example:                           
            # Expected  2.5%: r < 0.0755   -2 sigma
            # Expected 16.0%: r < 0.1009   -1 sigma
            # Expected 50.0%: r < 0.1411    limit
            # Expected 84.0%: r < 0.1990   +1 sigma
            # Expected 97.5%: r < 0.2700   +2 sigma


pp.pprint(limits)




#with io.open ('limits.txt', mode='w') as f:
if len(directo) > 3:
    directo = '_' + directo
else:
    directo = ''
with io.open('limits' + directo +'.txt', 'wb') as fp:
    pickle.dump(limits, fp)

# #To read it back:
# with open ('limits.txt', 'rb') as fp:
#     itemlist = pickle.load(fp)




end_time = time.time()
time_taken = end_time - start_time # time_taken is in seconds                                                           
                                                                                                                         
hours, rest = divmod(time_taken,3600)
minutes, seconds = divmod(rest, 60)
print
print "---it took {hours} hours, {minutes} minutes and {seconds:.1f} seconds to run the analysis ---".format (hours=hours, minutes=minutes, seconds=seconds) 



