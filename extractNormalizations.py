import subprocess
import time, os, sys
import numpy as np
import glob, re, io
import pickle, itertools
import pprint
pp = pprint.PrettyPrinter(indent=4)
pp = pprint.PrettyPrinter(depth=6)

trueRun = True

date = '_oct31'

start_time = time.time()

masses = [260, 270, 300, 350, 400, 450,         600, 650, 900, 1000]

curDir = os.getcwd()


logs = glob.glob("*/log*")
logs = [l for l in logs if '_ML' in l]

dict_dy = {'ee' :{}, 'mm': {}}
dict_tt = {'ee' :{}, 'mm': {}}

outside = ['DY']*10 + ['TT']*10
inside = masses * 2

for l in logs:
    print 'processing', l
    typ = l.split('_')[0]
    mass = int(l.split('_')[2][:3]) 
    if mass ==100: mass = 1000


#    if 'mm' in typ: continue
    
    command_DY = 'tail -50 ' + l + ' | grep "norm" | head -1'        
    command_TT = 'tail -50 ' + l + ' | grep "norm" | tail -1'
    #print command_DY
    #print command_TT

    if trueRun:
        time.sleep(1)
        tt_norm = subprocess.check_output(command_TT, shell=True)
        dy_norm = subprocess.check_output(command_DY, shell=True)

        
    tt_norm = tt_norm.split(' ')
    tt_norm = filter(lambda X: len(X)>0, tt_norm)[2]
    tt_norm = round(float(tt_norm), 3)
    #tt_norm_err = filter(lambda X: len(X)>0, tt_norm)[3]
    dy_norm = dy_norm.split(' ')
    dy_norm = filter(lambda X: len(X)>0, dy_norm)[2]
    dy_norm = round(float(dy_norm), 3)
    #dy_norm_err = filter(lambda X: len(X)>0, dy_norm)[3]


    print 'tt_norm', tt_norm
    print 'dy_norm', dy_norm
    dict_dy[typ][mass] = dy_norm
    dict_tt[typ][mass] = tt_norm

print 'dict_dy = '; pp.pprint(dict_dy)
print 
print 'dict_tt = '; pp.pprint(dict_tt)


sys.exit(1)

for mm_d, ee_d in zip(mm_dirs, ee_dirs):
    

    mass  = int(mm_d[8:])
    print 'mass is', mass
    if mass not in masses: continue
    
    tmpDir =  'combinedCards_' + str(mass) 
    if not os.path.exists(tmpDir):
        os.makedirs(tmpDir)

    if os.path.exists (tmpDir):           
        print 'change dir to', tmpDir
        os.chdir(tmpDir)
        print 'tmpDir is', tmpDir 
        cp_cards_n_ROOTfiles_mm = 'cp -r ../' + mm_d + '/mm* .' 
        cp_cards_n_ROOTfiles_ee = 'cp -r ../' + ee_d + '/ee* .' 
        print 'cp_cards_n_ROOTfiles_mm', cp_cards_n_ROOTfiles_mm
        print 'cp_cards_n_ROOTfiles_ee', cp_cards_n_ROOTfiles_ee
        
        if trueRun: 
            subprocess.call(cp_cards_n_ROOTfiles_mm, shell=True)
            subprocess.call(cp_cards_n_ROOTfiles_ee, shell=True)
                
        commandJoin = 'combineCards.py ee_comb_' + str(mass) + '.txt mm_comb_' + str(mass) + '.txt > combinedCard_' + str(mass) + '.txt'
        commandFit = 'combine -M Asymptotic -t -1 -v 3 --run blind -m ' + str(mass) + ' combinedCard_' +  str(mass) + '.txt >& log_combined_M' + str(mass) + '.txt&' 
        print commandJoin
        print commandFit
          
        if trueRun:
            time.sleep(1)
            subprocess.call(commandJoin, shell=True)
            subprocess.call(commandFit, shell=True)
            time.sleep(15)
                #subprocess.call(cpLog, shell=True)
            
        print 'change dir to', curDir
        os.chdir(curDir)
        print '='*50
            

#sys.exit(1)



limits = []
print 'DIRECTORY contains:'; print glob.glob("combinedCards*" + "log*")
for root, dirs, files in os.walk('.'):
#     #print 'root={0}, dirs={1}, files={2}'.format(root, dirs, files) 
    if 'combinedCards' not in root: continue # or 'makeDataCards/' not in root: continue

#     #print 'root={0}, dirs={1}'.format(root, dirs) 
    print 'root is ', root

# # root is  ./low_SR_-0.9/plots/makeDataCards/260
# # root is  ./low_SR_-0.9/plots/makeDataCards/400
# # root is  ./low_SR_-0.8/plots/makeDataCards/260
# # root is  ./low_SR_-0.8/plots/makeDataCards/400

    for fil in files:

        if not fil.endswith('txt') or 'log' not in fil: continue
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



