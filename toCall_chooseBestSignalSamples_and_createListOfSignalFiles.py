from os import listdir, system
from os.path import isfile, join

mainScript = "createListOfSignalFiles.py"

prefix_of_interest = "logOfSamples_Signal_"
path = "."



files_of_interest = [f for f in listdir(path) if isfile(join(path, f)) and prefix_of_interest in join(path, f)]
print "Number of files_of_interest=", len(files_of_interest) 
print "files_of_interest=", files_of_interest 
#logOfSamples_Signal_GluGluToRadionToHHTo2B2ZTo2L2Nu_M.txt


for idx, f in enumerate(files_of_interest):
    #if idx > 0:
     #   break
    cmd1 = "python chooseBestSignalSamples.py -i %s" % f
    print "cmd1=", cmd1
    system(cmd1)

    name = f.split("Signal_")[-1].split("_M")[0]
    print "name=", name
    #USAGE:  sh createListOfSignalFiles.sh <logOfSignalSamplesUnique> <logOfSignalSamplesNames>  <nameOfSignal>                    
    cmd2 = "sh createListOfSignalFiles.sh %s %s %s" % (f.replace("Samples", "SamplesUnique"), f.replace("Samples", "SamplesNames"), name) 
    print "cmd2=", cmd2
    system(cmd2)
    print '-'*20
