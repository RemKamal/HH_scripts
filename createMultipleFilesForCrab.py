from multiprocessing import Pool
import sys
import glob
import subprocess

trueRun = False# True
inputFile = "2L2J_radion.txt" #'signalSamples_15april2018_remaining.txt'

def createFiles(inputFile):
    text = []
    with open(inputFile, "r") as fIn:
        text = fIn.readlines()

        print 'len(text)=', len(text)
        for i in range(0, len(text), 2):
            print i
            print text[i]
    
            f = open("2L2J_signal_remaining_%s.txt" % i, "w")
            f.write(text[i])
            if i < len(text)-1:
                f.write(text[i+1])
            f.close()


 
def crabIt(fil):
    cmd = "sh launchall_HH.sh %s" % fil
    print cmd
    if trueRun:
        subprocess.call(cmd, shell=True)

def fileNumber(fil):
    print 'fil=', fil
    number = int(fil.split('_')[-1].split('.txt')[0]) # E.g.: 'signal_remaining_24.txt'
    return number

def main():
    createFiles(inputFile)

    inFiles = glob.glob("2L2J_signal_remaining_*txt")
    inFiles.sort(key=fileNumber)#, reverse=...)
    #https://www.programiz.com/python-programming/methods/list/sort
    print inFiles
    print 'len(inFiles)=', len(inFiles)

    only16files = inFiles#[:-1]
    # the last one want to try manually

    #for fil in inFiles:
     #   print fileNumber(fil)

    pool = Pool(processes=16)
    pool.map(crabIt, only16files)
    

 
if __name__ == '__main__':
    sys.exit(main())
