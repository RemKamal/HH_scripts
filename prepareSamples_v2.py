
import os
import subprocess
import re, sys
from pprint import pprint


# for data use V25b = re-miniAOD
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# comment out the line below to start outputting log debug info
logging.disable(logging.CRITICAL)

debug = True
def bazinga(mes):
    if debug:
        print mes



def createListOfData():
    """
    Prepare a list of data samples from the location defined above.

    Args:
        None

    Usage:
        python prepareDataSamples.py > logOfDataSamples.txt

    Returns:
        A list of samples to use with 'chooseBestDataSamples.py'

    """
    fileLocation = ['/store/user/arizzi/VHBBHeppyV25b/']  # , '/store/user/tboccali/Ntuples_v25/', '/store/group/phys_higgs/hbb/ntuples/V25' ]
    dataList = []
    #global skipList, prefixPisa, prefixCern, site, prefix, files, l1, filesL1, l2, filesL2, l3, filesL3, l, myStr, count, l4
    skipList = ['WJet', 'Wjet', 'DYJet', 'NuNu', '1L1Nu', '2Nu', 'LNu', "WH", 'Wplus', 'Wminus', 'Bulk', 'GluHTo',
                'VBFHToBB', 'ZHiggs0', 'bbHToBB', 'ToQQ']
    keepList = ['Double']
    prefixPisa = 'xrdfs stormgf1.pi.infn.it ls '
    prefixCern = 'ls '  # xrdfs 188.184.38.46 ls '
    bazinga("Inside createListOfData")
    for site in fileLocation:
        if 'user' in site:
            pass
            # site = '/eos/cms' + site
        prefix = prefixCern if 'group' in site else prefixPisa
        files = str(subprocess.check_output(prefix + site, shell=True))
        for l1 in files.split('\n'):
            filesL1 = str(subprocess.check_output(prefix + l1, shell=True))
            for l2 in filesL1.split('\n'):
                if site in l2:

                    filesL2 = str(subprocess.check_output(prefix + l2, shell=True))
                    for l3 in filesL2.split('\n'):
                        # keep only data samples
                        if all(x in l3 for x in [site, keepList[0]]):
                            # logging.debug('l3 is ' + l3)
                            filesL3 = str(subprocess.check_output(prefix + l3, shell=True))
                            l = len(filesL3.split('\n')) - 1
                            myStr = l3 + "/:"

                            for count, l4 in enumerate(filesL3.split('\n'), start=1):
                                if l4:
                                    # logging.debug('l4 is ' + l4)
                                    if count == 1:
                                        myStr += l4[-4:]
                                    if count > 1 and count <= l:
                                        myStr += ',' + l4[-4:]
                            logging.debug('myStr is ' + myStr)
                            print myStr
                            dataList.append(myStr)

                            # remove unwanted samples

                            if any(word in myStr for word in skipList):
                                pass
                                # continue
                            else:
                                pass
                                # print myStr
    dataOutFile = open('logOfSamples_Data.txt', 'w')
    for item in dataList:
        print>>dataOutFile, item










def createListOfBackgrounds():
    """
    Prepare a list of BG MCsamples from the location defined above.

    Args:
        None

    Usage:
        python prepareSamples.py > logOfSamples.txt

    Returns:
        A list of samples to use with 'chooseBestSamples.py'

    """

    bgList = []
    #global fileLocation, skipList, prefixPisa, prefixCern, site, prefix, files, l1, filesL1, l2, filesL2, l3, filesL3, l, myStr, count, l4

    fileLocation = ['/store/user/arizzi/VHBBHeppyV25/', '/store/user/tboccali/Ntuples_v25/',
                    '/store/group/phys_higgs/hbb/ntuples/V25']

    skipList = []  # 'WJet', 'Wjet', 'DYJet', 'NuNu', '1L1Nu', '2Nu','LNu', "WH", 'Wplus', 'Wminus' , 'Bulk', 'GluHTo' ,'VBFHToBB', 'ZHiggs0', 'bbHToBB', 'ToQQ']
    prefixPisa = 'xrdfs stormgf1.pi.infn.it ls '
    prefixCern = 'xrdfs 188.184.38.46 ls '
    bazinga("Inside createListOfBackgrounds")
    for site in fileLocation:
        prefix = prefixCern if 'group' in site else prefixPisa
        print 'prefix + site=', prefix, site
        files = str(subprocess.check_output(prefix + site, shell=True))
        for l1 in files.split('\n'):
            filesL1 = str(subprocess.check_output(prefix + l1, shell=True))
            for l2 in filesL1.split('\n'):
                if site in l2:
                    filesL2 = str(subprocess.check_output(prefix + l2, shell=True))
                    for l3 in filesL2.split('\n'):
                        # keep only MC samples
                        if site in l3 and 'Summer16MAv2' in l3:
                            filesL3 = str(subprocess.check_output(prefix + l3, shell=True))
                            l = len(filesL3.split('\n')) - 1
                            myStr = l3 + "/:"
                            for count, l4 in enumerate(filesL3.split('\n'), start=1):
                                if count == 1:
                                    myStr += l4[-4:]
                                if count > 1 and count <= l:
                                    myStr += ',' + l4[-4:]
                            # remove unwanted samples
                            if any(word in myStr for word in skipList):
                                continue
                            else:
                                print myStr
                                bgList.append(myStr)
    bgOutFile = open('logOfSamples_Background.txt', 'w')
    for item in bgList:
        print>>bgOutFile, item













def createListOfSignals():
    signalList = []
    #global fileLocation, l1, l2, l3, l4, myStr

    fileLocation = [
        '/eos/user/r/rkamalie/CMSSW_8_0_25/src/submit2/signal']#samplesForHH/signal']  # /store/user/arizzi/VHBBHeppyV25/', '/store/user/tboccali/Ntuples_v25/', '/store/group/phys_higgs/hbb/ntuples/V25' ]
    bazinga("Inside createListOfSignals")
    for fil in os.listdir(os.getcwd()):
        if 'Glu' in fil and 'txt' not in fil:
            # print 'fil is ', fil
            for l1 in os.listdir(fil):
                # print 'l1 is ', l1
                if l1:
                    for l2 in os.listdir(fil + '/' + l1):
                        if l2:
                            # print l2
                            for l3 in os.listdir(fil + '/' + l1 + '/' + l2):
                                if l3:
                                    printOnce = 0
                                    # print l3
                                    nSamp = 0
                                    for l4 in os.listdir(fil + '/' + l1 + '/' + l2 + '/' + l3):
                                        if l4:

                                            # print l4
                                            myStr = fil + '/' + l1 + '/' + l2 + '/' + l3 + '/' + l4
                                            if 'spr' in myStr: continue
                                            if 'tree' in myStr:
                                                toPlot = fil + '/' + l1 + '/' + l2 + '/:' + l3
                                                if printOnce == 0:
                                                    print toPlot
                                                    signalList.append(toPlot)
                                                printOnce += 1
                                                nSamp += 1

                                    if nSamp != 0:
                                        pass
                                        # print 1, nSamp
    signalOutFile = open('logOfSamples_Signal.txt', 'w')

    print 'signalList length is', len(signalList)
    for item in signalList:
        #signalOutFile.write("%s\n" % item)   #also works
        print>>signalOutFile, item
    bazinga("Done with signals")






def main():
    logging.debug('Start of program.')

    #createListOfSignals()
    
    #not working
    #createListOfBackgrounds()
    createListOfData()

    logging.debug('End of program.\n')





if __name__ == '__main__':
    sys.exit(main())











