import io
import re
import copy, logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# comment out the line below to start outputting log debug info
logging.disable(logging.CRITICAL)

"""
Remove duplicate samples, for samples with different TuneC... use the one which has 'ext' at the end of the name.

Args:
    None

Usage:
    python chooseBestSamples.py

Returns:
    List of samples w/o obvious duplicates to use with 'createListOfBGFiles_v2.sh'

"""


def chooseBackground():
    global sampleFile, sampleFileOut, sampleNamesOut, f, initialList, inputList, lineL1, nameRe, matchObjL1, lineL2, nameRe2, matchObjL2, sampleName1, sampleName2, len1, len2, fOut, fNamesOut, line, matchObj, niceSampleName
    sampleFile = 'logOfSamples.txt'
    sampleFileOut = 'logOfSamplesUnique.txt'
    sampleNamesOut = 'logOfSamplesNames.txt'
    with io.open(sampleFile, mode='rt') as f:
        initialList = f.read().split('\n')
        inputList = copy.deepcopy(
            initialList)  # necessary, since cannot iterate and remove same time using just one list

        for lineL1 in inputList[:-1]:
            # break
            if lineL1:

                nameRe = re.compile(r'_V25_([A-Za-z0-9_-]*)(Tranche)([A-Za-z0-9_-]*)(/[A-Za-z0-9_-]*)')
                matchObjL1 = nameRe.search(lineL1)
                for lineL2 in inputList[:-2]:
                    if lineL2:
                        nameRe2 = re.compile(r'_V25_([A-Za-z0-9_-]*)(Tranche)([A-Za-z0-9_-]*)(/[A-Za-z0-9_-]*)')

                        matchObjL2 = nameRe2.search(lineL2)
                        sampleName1 = matchObjL1.group(1) + matchObjL1.group(2)
                        sampleName2 = matchObjL2.group(1) + matchObjL2.group(2)
                        # print 'sampleName1 is ', sampleName1
                        # print 'sampleName2 is ', sampleName2

                        len1 = len(matchObjL1.group(1) + matchObjL1.group(2) + matchObjL1.group(3))
                        len2 = len(matchObjL2.group(1) + matchObjL2.group(2) + matchObjL2.group(3))
                        if lineL2 not in initialList:
                            pass
                        if sampleName1 in sampleName2 and len1 < len2:
                            if lineL1 in initialList:
                                initialList.remove(lineL1)

                        elif sampleName2 in sampleName1 and len2 < len1:
                            if lineL2 in initialList:
                                initialList.remove(lineL2)
                        else:
                            pass
    print '\nLen of modified and input lists are: ', (len(initialList) - 1), (len(inputList) - 1)
    with io.open(sampleFileOut, mode='wt') as fOut, io.open(sampleNamesOut, mode='wt') as fNamesOut:
        for line in initialList:
            if line:
                fOut.write(line + '\n')
                nameRe = re.compile(r'_V25_([A-Za-z0-9_-]*)(Tranche)([A-Za-z0-9_-]*)(/[A-Za-z0-9_-]*)')
                matchObj = nameRe.search(line)
                niceSampleName = matchObj.group(1) + matchObj.group(2) + matchObj.group(3)
                fNamesOut.write(niceSampleName + '\n')
                print 'niceSampleName is ', niceSampleName
    print "All done!"






"""
Remove duplicate samples, for samples with different TuneC... use the one which has 'ext' at the end of the name.

Args:
    None

Usage:
    python chooseBestDataSamples.py

Returns:
    List of samples w/o obvious duplicates to use with 'createListOfDataFiles.sh'

"""


def chooseData():
    global sampleFile, sampleFileOut, sampleNamesOut, f, initialList, inputList, lineL1, nameRe, matchObjL1, lineL2, nameRe2, matchObjL2, sampleName1, sampleName2, len1, len2, fOut, fNamesOut, line, matchObj, niceSampleName
    sampleFile = 'logOfDataSamples.txt'
    sampleFileOut = 'logOfDataSamplesUnique.txt'
    sampleNamesOut = 'logOfDataSamplesNames.txt'
    with io.open(sampleFile, mode='rt') as f:
        initialList = f.read().split('\n')
        inputList = copy.deepcopy(
            initialList)  # necessary, since cannot iterate and remove same time using just one list

        for lineL1 in inputList[:-1]:
            # break
            if lineL1:

                nameRe = re.compile(r'V25b_([A-Za-z0-9_-]*)(/[A-Za-z0-9_-]*)')
                matchObjL1 = nameRe.search(lineL1)
                for lineL2 in inputList[:-2]:
                    if lineL2:

                        nameRe2 = re.compile(r'V25b_([A-Za-z0-9_-]*)(/[A-Za-z0-9_-]*)')
                        matchObjL2 = nameRe2.search(lineL2)
                        sampleName1 = matchObjL1.group(1)
                        sampleName2 = matchObjL2.group(1)
                        len1 = len(matchObjL1.group())
                        len2 = len(matchObjL2.group())
                        print 'sampleName1 is ', sampleName1
                        print 'sampleName2 is ', sampleName2
                        if lineL2 not in initialList:
                            pass
                        if sampleName1 in sampleName2 and len1 < len2:
                            if lineL1 in initialList:
                                initialList.remove(lineL1)

                        elif sampleName2 in sampleName1 and len2 < len1:
                            if lineL2 in initialList:
                                initialList.remove(lineL2)
                        else:
                            pass
    print '\nLen of modified and input lists are: ', (len(initialList) - 1), (len(inputList) - 1)
    with io.open(sampleFileOut, mode='wt') as fOut, io.open(sampleNamesOut, mode='wt') as fNamesOut:
        for line in initialList:
            if line:
                fOut.write(line + '\n')
                nameRe = re.compile(r'V25b_([A-Za-z0-9_-]*)(/[A-Za-z0-9_-]*)')
                matchObj = nameRe.search(line)
                niceSampleName = matchObj.group(1)
                print niceSampleName
                fNamesOut.write(niceSampleName + '\n')
    print "All done!"






"""
Remove duplicate samples, for samples with different TuneC... use the one which has 'ext' at the end of the name.

Args:
    None

Usage:
    python chooseBestSamples.py

Returns:
    List of samples w/o obvious duplicates to use with 'createListOfBGFiles_v2.sh'

"""



def chooseSignal():
    sampleFile = 'logOfSignalSamples.txt'
    sampleFileOut = 'logOfSignalSamplesUnique.txt'
    sampleNamesOut = 'logOfSignalSamplesNames.txt'
    global f, initialList, inputList, lineL1, nameRe, matchObjL1, lineL2, nameRe2, matchObjL2, sampleName1, sampleName2, len1, len2, fOut, fNamesOut, line, matchObj, niceSampleName
    with io.open(sampleFile, mode='rt') as f:
        initialList = f.read().split('\n')
        inputList = copy.deepcopy(
            initialList)  # necessary, since cannot iterate and remove same time using just one list

        for lineL1 in inputList[:-1]:
            # break
            if lineL1:
                logging.debug('lineL1 is ' + lineL1)
                nameRe = re.compile(r'(_Glu([A-Za-z0-9_-]*)(/[A-Za-z0-9_-]*))')
                matchObjL1 = nameRe.search(lineL1)
                for lineL2 in inputList[:-2]:
                    if lineL2:
                        logging.debug('lineL2 is ' + lineL2)

                        nameRe2 = re.compile(r'(_Glu([A-Za-z0-9_-]*)(/[A-Za-z0-9_-]*))')
                        matchObjL2 = nameRe2.search(lineL2)

                        sampleName1 = 'Glu' + matchObjL1.group(2)
                        sampleName2 = 'Glu' + matchObjL2.group(2)
                        logging.debug('sampleName1 is ' + sampleName1)
                        logging.debug('sampleName2 is ' + sampleName2)

                        len1 = len(matchObjL1.group())
                        len2 = len(matchObjL2.group())

                        if sampleName1 in sampleName2 and len1 < len2:
                            if lineL1 in initialList:
                                initialList.remove(lineL1)

                        elif sampleName2 in sampleName1 and len2 < len1:
                            if lineL2 in initialList:
                                initialList.remove(lineL2)
                        else:
                            pass
    print '\nLen of modified and input lists are: ', (len(initialList) - 1), (len(inputList) - 1)
    with io.open(sampleFileOut, mode='wt') as fOut, io.open(sampleNamesOut, mode='wt') as fNamesOut:
        for line in initialList:
            if line:
                fOut.write(line + '\n')
                nameRe = re.compile(r'(_Glu([A-Za-z0-9_-]*)(/[A-Za-z0-9_-]*))')
                matchObj = nameRe.search(line)
                niceSampleName = matchObj.group(2)
                logging.debug('matchObj.group(1) is ' + matchObj.group(1))
                logging.debug('matchObj.group() is ' + matchObj.group())
                logging.debug('matchObj.group(2) is ' + matchObj.group(2))

                logging.debug('niceSampleName is ' + niceSampleName)
                fNamesOut.write('Glu' + niceSampleName + '\n')




def main():
    logging.debug('Start of program.')

    chooseSignal()
    chooseData()
    chooseBackground()

    logging.debug('End of program.\n')





if __name__ == '__main__':
    sys.exit(main())



