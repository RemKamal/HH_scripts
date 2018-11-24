import os
import re
from sys import argv

imput = len(argv) > 1 
print argv[0] # script name itself
#print argv[1] # 1st passed argument

print 'len(argv) is ', len(argv)
lostList = list() if len(argv) < 2 else [int(x) for x in argv[1].split(',')]
print lostList



jobsList = []
problematicDir = True if len (lostList) > 0 else False

for root, dirs, files in os.walk("."):
    for fil in files:
        if 'job' in fil and fil.endswith(".sh"):
            jobsList.append(fil)
            #print fil[:-3]


#job_DoubleEG__Run2016B-03Feb2017_ver2-v2_825_839.sh
#nameRe = re.compile(r'_V25_([A-Za-z0-9_-]*)(Tranche)([A-Za-z0-9_-]*)(/[A-Za-z0-9_-]*)')
nameRe = re.compile(r'(([0-9]*)_([0-9]*)).sh')
for i, job in enumerate(jobsList):
    #if i ==0:
     #   print len(jobsList)
    if problematicDir:
        mo = nameRe.search(job)
    #print 'mo.group() is ', mo.group()             => 825_839.sh 
    #print 'mo.group(1) is ', mo.group(1)           => 825_839
    #print 'mo.group(2) is ', mo.group(2)           => 825
    #print 'mo.group(3) is ', mo.group(3)           => 839
    #if any(num in job for num in listOfNumbers): continue
        #if int(mo.group(2)) < 1619: continue
        if int(mo.group(2)) not in lostList:  continue
    #print 'i and job are ', i, job
    cmd = 'bsub -q 8nh -J '+job[:-3]+ ' -u dummy12345@gmail.com < ' + job
    
    os.system('chmod +x ' + job )
    os.system (cmd)
    #print cmd
