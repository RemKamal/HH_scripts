import subprocess
import time, os, sys
import numpy as np
import glob, re, io
import pickle, itertools
import pprint
pp = pprint.PrettyPrinter(indent=4)
pp = pprint.PrettyPrinter(depth=6)

trueRun = True

date = '_dec17'

start_time = time.time()

#masses = [260, 270, 300, 350, 400, 450,         600, 650, 900, 1000]
masses = [451]
curDir = os.getcwd()


comb_dirs = glob.glob("combinedCards_*0/") + glob.glob("combinedCards_*451/")

#ee_dirs = glob.glob("ee_log*")
print 'DIRECTORY contains:'; 
print comb_dirs
#print ee_dirs

for comb_d in comb_dirs:
    #mm_bdt, ee_bdt = None, None
    print 'comb_d', comb_d
    #if len(mm_d.split('_')) > 3:
    #    mm_bdt, ee_bdt = mm_d.split('_')[3], ee_d.split('_')[3]
    #    print 'mm_bdt = {0}, ee_bdt = {1}'.format(mm_bdt, ee_bdt)
    #    mass = int(mm_d.split('_')[2])
    #else:
    #    mass  = int(mm_d[8:])
    mass  = int(comb_d[14:-1])

    print 'mass is', mass
    if mass not in masses: continue
    

    # ee_extra_if_bdt = ''
    # mm_extra_if_bdt = ''
    # if mm_bdt != None:
    #     ee_extra_if_bdt = '_ee_' + ee_bdt
    #     mm_extra_if_bdt = '_mm_' + mm_bdt
    origDir = 'combinedCards_' + str(mass)
    tmpDir =  'combinedCards_' + str(mass) + date#ee_extra_if_bdt + mm_extra_if_bdt 
    print 'tmpDir =', tmpDir
    if not os.path.exists(tmpDir):
        os.makedirs(tmpDir)

    if os.path.exists (tmpDir):           
        print 'change dir to', tmpDir
        os.chdir(tmpDir)
        print 'tmpDir is', tmpDir 
        # cp_cards_n_ROOTfiles_mm = 'cp -r ../' + mm_d + '/mm* .' 
        # cp_cards_n_ROOTfiles_ee = 'cp -r ../' + ee_d + '/ee* .' 
        # print 'cp_cards_n_ROOTfiles_mm', cp_cards_n_ROOTfiles_mm
        # print 'cp_cards_n_ROOTfiles_ee', cp_cards_n_ROOTfiles_ee
        
        # if trueRun: 
        #     subprocess.call(cp_cards_n_ROOTfiles_mm, shell=True)
        #     subprocess.call(cp_cards_n_ROOTfiles_ee, shell=True)
     

        if mass > 450:
            range_ = ' --rMin -100 --rMax 100 ' 
        else: #use high extremes for low masses
            range_ = ' --rMin -1000 --rMax 1000 ' 
           
        commandCopy = 'cp -r ../' + origDir + '/{mm,ee}_*root . && cp -r ../' + origDir + '/comb*txt .'
        
        commandAddMC = 'echo "" >> combinedCard_{0}.txt && echo "* autoMCStats 0" >> combinedCard_{1}.txt '.format(str(mass),str(mass) )

        #commandFit = 'combine -M Asymptotic -t -1 -v 3 --run blind -m ' + str(mass) + ' combinedCard_' +  str(mass) + '.txt >& log_combined_M' + str(mass) + '.txt&' 
        commandFit = 'combine -M Asymptotic -t -1 -v 3 --run blind  --X-rtd MINIMIZER_analytic -m ' + str(mass) + ' combinedCard_' +  str(mass) + '.txt >& log_combined_M' + str(mass) + '.txt&' 
        commandFit_ML = 'combine -M MaxLikelihoodFit -v 3 --X-rtd MINIMIZER_analytic -m ' + str(mass) + range_ + ' combinedCard_' +  str(mass) + '.txt >& log_combined_M' + str(mass) + '_ML.txt&' 
        print commandCopy
        print commandAddMC
        print commandFit
        print commandFit_ML

        if trueRun:
            time.sleep(1)

            subprocess.call(commandCopy, shell=True)
            subprocess.call(commandAddMC, shell=True)
            subprocess.call(commandFit, shell=True)
            time.sleep(25)
            subprocess.call(commandFit_ML, shell=True)
            time.sleep(15)
            
        print 'change dir to', curDir
        os.chdir(curDir)
        print '='*50
            

#sys.exit(1)



limits = []
print 'DIRECTORY contains:'; print glob.glob("combinedCards*" + "log*")
for root, dirs, files in os.walk('.'):
#     #print 'root={0}, dirs={1}, files={2}'.format(root, dirs, files) 
    if 'combinedCards' not in root: continue # or 'makeDataCards/' not in root: continue
    if 'dec17' not in root: continue # or 'makeDataCards/' not in root: continue

#     #print 'root={0}, dirs={1}'.format(root, dirs) 
    print 'root is ', root
    
# # root is  ./low_SR_-0.9/plots/makeDataCards/260
# # root is  ./low_SR_-0.9/plots/makeDataCards/400
# # root is  ./low_SR_-0.8/plots/makeDataCards/260
# # root is  ./low_SR_-0.8/plots/makeDataCards/400

    for fil in files:
        
        if not fil.endswith('txt') or 'log' not in fil: continue
        if '_ML' in str(root) + '/' +  fil: continue
        if '#' in str(root) + '/' +  fil: continue
        #if leptType not in str(str(root) + '/' + fil): continue
         #if not fil.endswith('txt'): continue
        #if len(str(fil)) > 30: continue
        if  os.path.getsize(str(root) + '/' + fil) < 10000: continue # to skip corrupted/incomplete logs with errors
        print
        print 'For file', fil
        print 'size is:'
        print os.path.getsize(str(root) + '/' + fil)
        with io.open (str(root) + '/' + fil, mode='r') as f:

            print 'Full file name is', str(root) + '/' +  fil
            text = f.read()
            print 'text=', text
            tmp_limits = re.findall(r"r < (\d*\.\d+|\d+)", text)
            #print 'tmp_limits', tmp_limits
            
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

print
print 'limits are:'
pp.pprint(limits)




with io.open('combinedCards_limits.txt', 'wb') as fp:
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



