import io
import re
import copy
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

#comment out the line below to start outputting log debug info
logging.disable(logging.CRITICAL)



import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str,
                    help="input txt file")
#parser.add_argument("-o", "--output", type=str,
 #                   help="output txt file")

args = parser.parse_args()
if not args:
    sys.exit(1)
else:
    print 'args=', args


sampleFile = args.input #'logOfSignalSamples.txt'
sampleFileOut = sampleFile.replace("Samples", "SamplesUnique")  #'logOfSignalSamplesUnique.txt'
sampleNamesOut =  sampleFile.replace("Samples", "SamplesNames") #'logOfSignalSamplesNames.txt'
"""
Remove duplicate samples, for samples with different TuneC... use the one which has 'ext' at the end of the name.

Args:
    None

Usage:
    python chooseBestSamples.py

Returns:
    List of samples w/o obvious duplicates to use with 'createListOfBGFiles_v2.sh'

"""

logging.debug('Start of program.')


with io.open (sampleFile, mode = 'rt') as f:
    initialList = f.read().split('\n')
    inputList = copy.deepcopy(initialList) # necessary, since cannot iterate and remove same time using just one list
    
    for lineL1 in inputList[:-1]:
        #break
        if lineL1:
            logging.debug('lineL1 is ' + lineL1)
            nameRe = re.compile(r'(_Glu([A-Za-z0-9_-]*)(/[A-Za-z0-9_-]*))')
            matchObjL1 =  nameRe.search(lineL1)
            for lineL2 in inputList[:-2]:
                if lineL2:
                    logging.debug('lineL2 is ' + lineL2)

                    nameRe2 = re.compile(r'(_Glu([A-Za-z0-9_-]*)(/[A-Za-z0-9_-]*))')
                    matchObjL2 =  nameRe2.search(lineL2)

                    sampleName1 =  'Glu' + matchObjL1.group(2)
                    sampleName2 =  'Glu' + matchObjL2.group(2)
                    logging.debug('sampleName1 is ' + sampleName1 )
                    logging.debug('sampleName2 is ' + sampleName2 )

                    len1 = len (matchObjL1.group()) 
                    len2 = len (matchObjL2.group()) 
                    
                    if sampleName1 in sampleName2 and len1 < len2:
                        if lineL1 in initialList:
                            initialList.remove(lineL1)
                        
                    elif  sampleName2 in sampleName1 and len2 < len1:
                        if lineL2 in initialList:
                            initialList.remove(lineL2)
                    else:
                        pass 
                    

print '\nLen of modified and input lists are: ',  (len(initialList )-1), (len(inputList)-1)
#with io.open (sampleFileOut, mode = 'wt') as fOut, io.open (sampleNamesOut, mode = 'wt') as fNamesOut:
with open (sampleFileOut, mode = 'wt') as fOut, open (sampleNamesOut, mode = 'wt') as fNamesOut:
    for line in initialList:
        if line:
            
            fOut.write(line + '\n')
            nameRe = re.compile(r'(_Glu([A-Za-z0-9_-]*)(/[A-Za-z0-9_-]*))')
            matchObj =  nameRe.search(line)
            niceSampleName = matchObj.group(2)
            logging.debug('matchObj.group(1) is ' + matchObj.group(1))
            logging.debug('matchObj.group() is ' + matchObj.group())
            logging.debug('matchObj.group(2) is ' + matchObj.group(2))

            logging.debug('niceSampleName is ' + niceSampleName )
            fNamesOut.write('Glu' + niceSampleName + '\n')


logging.debug('End of program.\n')
