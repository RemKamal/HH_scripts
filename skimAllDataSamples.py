import re, io
import subprocess

fullRun = True

sampleRe = re.compile(r'comb_listOf_([A-Za-z0-9_-]*)_trees(\w*)')
files_txt = '../dataSamplesFinal.txt' if fullRun else '../dataSamplesFinal_rest_5o5.txt'
with io.open(files_txt, mode="rt", encoding="utf-8") as f:
    listOfFiles = f.read().split('\n')[:-1]

for fil in listOfFiles:
    matchObj = sampleRe.search(fil)
    sampleName = matchObj.group(1)
    if sampleName not in fil:
        print 'An error happened, list of samples and sample name do NOT coincide, please check. See top of the script for the hint.'
        exit(1)
    print ' file is ', fil
    print 'sample name is ', sampleName
    subprocess.call("python submit_v3_test_data.py ../" + fil + " " + sampleName, shell=True)

        


