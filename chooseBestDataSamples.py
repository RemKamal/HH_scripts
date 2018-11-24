import io
import re
import copy

sampleFile = 'logOfDataSamples.txt'
sampleFileOut = 'logOfDataSamplesUnique.txt'
sampleNamesOut = 'logOfDataSamplesNames.txt'
"""
Remove duplicate samples, for samples with different TuneC... use the one which has 'ext' at the end of the name.

Args:
    None

Usage:
    python chooseBestDataSamples.py

Returns:
    List of samples w/o obvious duplicates to use with 'createListOfDataFiles.sh'

"""



with io.open (sampleFile, mode = 'rt') as f:
    initialList = f.read().split('\n')
    inputList = copy.deepcopy(initialList) # necessary, since cannot iterate and remove same time using just one list
    
    for lineL1 in inputList[:-1]:
        #break
        if lineL1:
            
            nameRe = re.compile(r'V25b_([A-Za-z0-9_-]*)(/[A-Za-z0-9_-]*)')
            matchObjL1 =  nameRe.search(lineL1)
            for lineL2 in inputList[:-2]:
                if lineL2:

                    nameRe2 = re.compile(r'V25b_([A-Za-z0-9_-]*)(/[A-Za-z0-9_-]*)')
                    matchObjL2 =  nameRe2.search(lineL2)
                    sampleName1 =  matchObjL1.group(1)
                    sampleName2 =  matchObjL2.group(1)
                    len1 = len (matchObjL1.group()) 
                    len2 = len (matchObjL2.group()) 
                    print 'sampleName1 is ', sampleName1
                    print 'sampleName2 is ', sampleName2
                    if lineL2 not in initialList:
                        pass
                    if sampleName1 in sampleName2 and len1 < len2:
                        if lineL1 in initialList:
                            initialList.remove(lineL1)
                        
                    elif  sampleName2 in sampleName1 and len2 < len1:
                        if lineL2 in initialList:
                            initialList.remove(lineL2)
                    else:
                        pass 
                    

print '\nLen of modified and input lists are: ',  (len(initialList )-1), (len(inputList)-1)
with io.open (sampleFileOut, mode = 'wt') as fOut, io.open (sampleNamesOut, mode = 'wt') as fNamesOut:
    for line in initialList:
        if line:
            
            fOut.write(line + '\n')
            nameRe = re.compile(r'V25b_([A-Za-z0-9_-]*)(/[A-Za-z0-9_-]*)')
            matchObj =  nameRe.search(line)
            niceSampleName = matchObj.group(1)
            print niceSampleName
            fNamesOut.write(niceSampleName + '\n')

print "All done!"
