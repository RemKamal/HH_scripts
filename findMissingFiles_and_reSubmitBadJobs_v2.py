import re, os, sys
import subprocess
from glob import glob
#from sets import Set
import pprint as pp
from operator import itemgetter
#import ROOT
from ROOT import TFile

baddirs = []
totalResubDirs = []
skipList = [] #'hadd_part2']
curDir = os.getcwd()
sampleNamesList = []
keepList = [] #'DY3J', 'DY4J', 'ZH_H']
printSampleNames = True
doSignal = True

trueRun = True

def reSubmit(tup):
    
    bd, idxList = tup[0], tup[1]
    #bdirs = list(map(itemgetter(0), baddirs))
    #bindexes = list(map(itemgetter(1), baddirs))
    #print 'bdirs are:', bdirs
    #print 'bindexes are:', bindexes

    for root, dirs, files in os.walk("."):
        #print 'root is', root[2:] +'/'

        if not root or 'LSF' in root or root[2:] +'/' != bd:
            continue
        else:
            #print 'root is', root[2:] + '/'
            root_dir_set = set(dirs)
            bad_dir_set = set()
            for fil in files:
                if 'job' in fil and fil.endswith(".sh"):
                    
                    nameRe = re.compile(r'(([0-9]*)_([0-9]*)).sh')
                    mo = nameRe.search(fil)
                    if int(mo.group(2)) not in idxList:  continue
                    fil = bd + fil
                    cmd = 'bsub -q 8nh -J ' + fil[:-3] + ' -u dummy12345@gmail.com < ' + fil
                    os.system('chmod +x ' + fil)
                    print
                    print 'Command to run is', cmd
                    if trueRun:
                        os.system(cmd)
        
    print '$'*50




def findMissinsFiles():
    dirs = glob('*/')
    ndirs = 0
    #print dirs
    nbadsamples = 0
    dirs = list(filter(lambda x: x[:4] in keepList, dirs)) if keepList else dirs
    print dirs
    for d in dirs:
        if any(x in d for x in  skipList): continue
        # mainDir, folders, files in os.walk("."):
        if d and 'LSF' not in d:  # mainDir == ".":
            if 'signal' in d: continue
            #if doSignal and 'Glu' not in d: continue
            
            print 'Analysing dir', d
            ndirs += 1
            jobNumbers = []
            treeNumbers = []
            missedTrees = []
            fileList = []

            try:
                listOfJobs = subprocess.check_output('ls ' + d + 'job*', shell=True).split('\n')[:-1]
            except subprocess.CalledProcessError as e:
                # print e
                print 'Use "skimAllSamples.py" and modify the "txt" file to have those samples in'
                str(e)
                baddirs.append(d)
                totalResubDirs.append(d)
                nbadsamples += 1
                # print e.args
                continue

            try:
                listOfTrees = subprocess.check_output('ls ' + d + 'skim*', shell=True).split('\n')[:-1]
            except subprocess.CalledProcessError as e:
                # print e
                print 'no trees found, call this sample with all {0}jobs'.format(len(listOfJobs))
                print 'd is {0} and listOfJobs is {1}'.format(d, listOfJobs)
                for job in listOfJobs:
                    if job:
                    # print job                                                                                         
                        nameRe = re.compile(r'(([0-9]*)_([0-9]*)).sh')
                        mo = nameRe.search(job)
                        jobNumbers.append(int(mo.group(2)))

                reSubmit((d, sorted(jobNumbers)))
                str(e)
                # print e.args
                baddirs.append(d)
                nbadsamples += 1
                # print e.args
                continue

            # print 'Inside {0}'.format(d)
            # print 'len(listOfJobs) is ', len(listOfJobs)
            # print 'len(listOfTrees) is ', len(listOfTrees)
            # print 'listOfJobs is', listOfJobs
            # print 'listOfTrees is', listOfTrees
            print
            
            for job in listOfJobs:
                if job:
                    # print job
                    nameRe = re.compile(r'(([0-9]*)_([0-9]*)).sh')
                    mo = nameRe.search(job)
                    jobNumbers.append(int(mo.group(2)))

            for fil in listOfTrees:
                if fil:
                    if 'good.root' in fil: continue
                    print 'fil=', fil
                    nameRe = re.compile(r'(([0-9]*)_([0-9]*)).root')
                    mo = nameRe.search(fil)
                    print 'mo=', mo
                    size = os.stat(fil).st_size

                    #print size
                    if size <= 1000:
                        print 50*'*||*'
                        print size
                        print 'file {0} has size <= 1000b, skip to be able to resubmit'.format(fil)
                        continue
                    else:
                        try: 
                            root_f = TFile.Open(fil)
                            if root_f.IsZombie() or not root_f.IsOpen() or root_f.TestBit(TFile.kRecovered) or root_f.GetNkeys()==0 :
                                print 'zombie file {0}'.format(fil)
                                continue

                            else:
                                countWeighted=root_f.Get('CountWeighted')

                                if countWeighted == None:# or (countWeighted != None and countWeighted.GetBinContent(1) ==0):
                                    print 'file {0} has no countWeighted histogram, skip to resubmit'.format(fil)
                                    continue
                                else:
                                    print 'countWeighted', countWeighted
                                    #print 'countWeighted.GetBinContent(1)', countWeighted.GetBinContent(1)


                        except Exception as e:
                            print 'bad file {0}'.format(fil)
                            print e
                            continue
                        #print 'adding file {0}'.format(fil)
                        treeNumbers.append(int(mo.group(2)))
                        fileList.append(fil)

            jobSet = set(jobNumbers)
            treeSet = set(treeNumbers)

            sym_dif_set = jobSet.symmetric_difference(treeSet)
            if sym_dif_set:
                baddirs.append(d)
                nbadsamples += 1
                print 'For the directory below those are the missing jobNumbers:'
                print d, ','.join((str(x) for x in sorted(sym_dif_set)))
                reSubmit((d, list(sorted(sym_dif_set))))
                print
            else:
                if not printSampleNames: continue
                name = curDir + '/' + d
                #print 'name is', name
                sampleNamesList.append(d)
                with open (name[:-1] + '.txt', mode='wt') as fO:
                    print 'd is:'
                    print d[:-1]
                    #print 'curDir is', curDir
                    for f in fileList:
                        #print 'f is ', f
                        fO.write(curDir+"/%s\n" % f)

    print
    print '{0} baddirs are found:'.format(len(baddirs), baddirs)
    pp.pprint(baddirs)
    print
    print '{0} totalResubDirs are found:'.format(len(totalResubDirs), totalResubDirs)
    pp.pprint(totalResubDirs)
    print 'Use "skimAllSamples.py" and modify the "txt" file to have those samples'
    for j in totalResubDirs:
        prefix = './comb_listOf_' 
        postfix = '_trees.txt'
        print prefix+j[:-1]+postfix
    if printSampleNames:
        print 'Good (no problems) sampleNamesList contains {0} directories:'. format(len(sampleNamesList))
        pp.pprint(sampleNamesList)


def main():
    print 'starting "find" fcn'
    findMissinsFiles()
    print 'done!'


if __name__ == '__main__':
    sys.exit(main())
