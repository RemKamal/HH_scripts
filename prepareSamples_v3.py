import os
import subprocess
import re, sys
from pprint import pprint
import traceback


# for data use V25b = re-miniAOD
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# comment out the line below to start outputting log debug info
logging.disable(logging.CRITICAL)


signalSamplePatterns = [
    "GluGluToRadionToHHTo2B2VTo2L2Nu_M",        # bbVV Radion, 16 samples
    "GluGluToRadionToHHTo2B2ZTo2L2Nu_M",        # our Radion, 16 samples

    "GluGluToRadionToHHTo2B2ZTo2L2J_M",         # 2b2j Radion, 14 samples

    "GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M",  # bbVV Graviton, 6 samples
    ]
    
    

debug = True
def bazinga(mes):
    if debug:
        print mes



def createListOfDataAndBackground():
    fileLocation = [
        '/store/user/arizzi/VHBBHeppyV25/' , 
        '/store/user/arizzi/VHBBHeppyV25a/' , 
        '/store/user/arizzi/VHBBHeppyV25b/' , 
        '/store/user/tboccali/Ntuples_v25/', 
        '/eos/cms/store/group/phys_higgs/hbb/ntuples/V25/' 
        ]
    dataList = []
    skipList = ['WJet', 'Wjet', 'NuNu', '1L1Nu', '2Nu', 'LNu', "WH", 'Wplus', 'Wminus', 'Bulk', 'GluHTo','VBFHToBB', 'ZHiggs0', 'bbHToBB', 'QQ', '2Q', 'Single', 'HT-', 'Inf', '0L', 'hbbhbb', '4B', '10to50', 'MET', 'BTagCSV', 'DYJetsToLL_Pt', 'QCD', 'Mtt', 'EWK', 'HToMuMu', 'DYBBJ', 'DYBJ', 'DYJetsTo', 'DYToLL', 'JetHT']
    keepList = []#'Double']
    prefixPisa = 'xrdfs stormgf1.pi.infn.it ls '
    prefixCern = 'ls '  # xrdfs 188.184.38.46 ls '
    bazinga("Inside createListOfDataAndBackground")
    for site in fileLocation:
        prefix = prefixCern if 'group' in site else prefixPisa
        files = str(subprocess.check_output(prefix + site, shell=True))
        for l1 in files.split('\n'):
            #if l1: print 'l"0" is', l1
            
            if not l1:
                continue

            l1 = site + l1 if 'group' in site else l1
            
            if '25' not in l1 or (l1 and any(word in l1 for word in skipList) ):
                continue
#bazinga()
            #print 'l1 is', l1
            
            filesL1 = str(subprocess.check_output(prefix + l1, shell=True))
            for l2 in filesL1.split('\n'):
                if not l2:
                    continue
                #l2 = site + l2 if 'group' in site else l2
                #print 'site is {0}, l2 is {1}'.format(site, l2)
                l2 = l1 + '/' + l2 if 'group' in site else l2
                if site in l2:
                    #print 'l2 is', l2
                    filesL2 = str(subprocess.check_output(prefix + l2, shell=True))
                    for l3 in filesL2.split('\n'):
                        if not l3:
                            continue
                        l3 = l2 + '/' + l3 if 'group' in site else l3
                        # keep only data samples
                        if all(x in l3 for x in [site]):#, keepList[0]]):
                            # logging.debug('l3 is ' + l3)
                            filesL3 = str(subprocess.check_output(prefix + l3, shell=True))
                            #print 'l3 is', l3
                            l = len(filesL3.split('\n')) - 1
                            myStr = l3 + "/:"

                            for count, l4 in enumerate(filesL3.split('\n'), start=1):
                                if l4:
                                    # logging.debug('l4 is ' + l4)
                                    #print 'l4 is ', l4
                                    if count == 1:
                                        myStr += l4[-4:]
                                    if count > 1 and count <= l:
                                        myStr += ',' + l4[-4:]

                            

                            # remove unwanted samples
                            dataList.append(myStr)
                            logging.debug('myStr is ' + myStr)
                            print myStr
                            print
    print 'DataAndBGList length is', len(dataList)
    dataOutFile = open('logOfSamples_DataAndBackground.txt', 'w')
    for item in dataList:
        print>>dataOutFile, item
    bazinga('Done with DataAndBG')



def createListOfSignals(signalPattern):
    signalList = []
    #global fileLocation, l1, l2, l3, l4, myStr

    fileLocation = [
        "."
        #'/eos/user/r/rkamalie/CMSSW_8_0_25/src/bbZZ'
        ]
        
    
    bazinga("Inside createListOfSignals")
    files = os.listdir(os.getcwd())
    #print 'first files=', files
    files = [x for x in files if signalPattern in x and 'txt' not in x]
    #print 'second files='
    #pprint(files)
    print 'len final files=', len(files)
    
    for fil in files: #os.listdir(os.getcwd()):
        if 'txt' not in fil:
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

                                            #print l4
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
    #return
    signalOutFile = open('logOfSamples_Signal_%s.txt' % signalPattern, 'w')
    
    print 'signalList length is', len(signalList)
    for item in signalList:
        #signalOutFile.write("%s\n" % item)   #also works
        print>>signalOutFile, item
    bazinga("Done with signals")






def main():
    """
    Prepares two txt files with the list of data and BG, and signal samples from the location defined in the above 'fileLocation'.

    Args:
        None

    Usage:
        python prepareSamples_v3.py

    Returns:
        Two txt files with a list of samples to use with 'chooseSamples.py'

    """
    
    logging.debug('Start of program.')
    try:
        #createListOfDataAndBackground()
        
        for sp in signalSamplePatterns:
            print 'signalSamplePattern=', sp
            createListOfSignals(sp)

    except Exception as e:
        logging.error(traceback.format_exc())
        # Logs the error appropriately. 
    logging.debug('End of program.\n')


if __name__ == '__main__':
    sys.exit(main())











