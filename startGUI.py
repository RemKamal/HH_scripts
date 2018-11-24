import ROOT
import sys


args_are_given = len(sys.argv) > 1
#print sys.argv[0] # script name itself                                                                                                                     
#print sys.argv[1] # 1st passed argument, TMVA file, e.g.  TMVAOutput_250_450_biClass_2017Oct17_19-02.root                                                                                                


#prefix = 'dataset/weights/'
if args_are_given:
    fileIn = sys.argv[1] #)ROOT.TString ( 
    print 'fileIn is ', fileIn
    doMLCL = True if 'multi' in fileIn else False if 'bi' in fileIn else None

if doMLCL:
    ROOT.TMVA.TMVAMultiClassGui(fileIn)
else:
    if 'bi' in fileIn:
        ROOT.TMVA.TMVAGui(fileIn)
    else:
        print 'check input file, exiting'
        sys.exit(1)

raw_input('Press Enter to exit')
