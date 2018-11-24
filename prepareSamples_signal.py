import os
import subprocess
import re
from pprint import pprint
fileLocation = ['/eos/user/r/rkamalie/samplesForHH/signal']#/store/user/arizzi/VHBBHeppyV25/', '/store/user/tboccali/Ntuples_v25/', '/store/group/phys_higgs/hbb/ntuples/V25' ]

for fil in os.listdir(os.getcwd()):
    if 'Glu' in fil:
        #print 'fil is ', fil
        for l1 in os.listdir(fil):
            #print 'l1 is ', l1 
            if l1:
                for l2 in os.listdir(fil + '/' + l1):
                    if l2:
                        #print l2
                        for l3 in os.listdir(fil + '/' + l1 + '/' + l2):
                            if l3:
                                printOnce = 0
                                #print l3
                                nSamp=0
                                for l4 in os.listdir(fil + '/' + l1 + '/' + l2 + '/' + l3):
                                    if l4:      
                                        
                                        #print l4
                                        myStr = fil + '/' + l1 + '/' + l2 + '/' + l3 + '/' + l4
                                        if 'spr' in myStr: continue
                                        if 'tree' in  myStr:
                                            toPlot = fil + '/' + l1 + '/' + l2 + '/:' + l3
                                            if printOnce ==0:
                                                print toPlot
                                            printOnce += 1
                                            nSamp += 1 
                                
                                if nSamp!=0:
                                    pass
                                    #print 1, nSamp
                                        
