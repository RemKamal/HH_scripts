import re, os
import subprocess
cmdJobs = 'ls job*'
cmdTrees = 'ls skim*'

jobNumbers = []
treeNumbers = []
missedTrees = []
for mainDir, folders, files in os.walk("."):
   if mainDir == ".":
      listOfJobs = subprocess.check_output(cmdJobs, shell=True).split('\n')[:-1]    
      listOfTrees = subprocess.check_output(cmdTrees, shell=True).split('\n')[:-1]        
      print 'len(listOfJobs) is ', len(listOfJobs) 
      print 'len(listOfTrees) is ', len(listOfTrees) 

      for fil in listOfTrees:
         if fil:
            #print fil
            nameRe = re.compile(r'(([0-9]*)_([0-9]*)).root')
            mo = nameRe.search(fil)
            treeNumbers.append(int(mo.group(2)))

      for job in listOfJobs:
         if job:
            nameRe = re.compile(r'(([0-9]*)_([0-9]*)).sh')
            mo = nameRe.search(job)
            jobNumbers.append(int(mo.group(2)))
            if int(mo.group(2)) not in treeNumbers:
               missedTrees.append (int(mo.group(2)))
               print job

print ','.join(str(x) for x in missedTrees)
print 'jobNumbers is ', sorted(jobNumbers)
print 'jobreeNumbers is ', sorted(treeNumbers)
