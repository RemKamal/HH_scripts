import getopt
import time
from ROOT import TFile
from ROOT import TCanvas
import sys




def extractCanvasFromROOTfile(expSignal0_inputfile, expSignal1_inputfile):
    
   expS0_file = TFile.Open(expSignal0_inputfile)
   expS1_file = TFile.Open(expSignal1_inputfile)


# KEY: TCanvasasdf;1          asdf
# KEY: TCanvasnuisancs;1      nuisances
# KEY: TCanvaspost_fit_errs;1 post_fit_errs
   
   pulls_expS0 = expS0_file.Get('asdf')
   print 'pulls_expS0', pulls_expS0
   
   pulls_expS0.SaveAs('pulls_expS0.pdf')
   #pulls_expS0.Print('/afs/cern.ch/user/r/rkamalie/workspace/private/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/test/mytest/jan5/jan_work/tests/march30_forLimits/copy_combinedCards_300/combinedCards_300/pulls_expS0.png')

   pulls_expS1 = expS1_file.Get('asdf')
   print 'pulls_expS1', pulls_expS1
   
   pulls_expS1.SaveAs('pulls_expS1.pdf')
   #pulls_expS1.Print('pulls_expS1.png')


def main(argv):
   print 'inside the MAIN fnc'
   expSignal0_inputfile = None
   expSignal1_inputfile = None
   try:
      opts, args = getopt.getopt(argv,"hz:o:",["expSignal0=","expSignal1="])
   except getopt.GetoptError:
      print 'test.py -i <expSignal0 file> -o <expSignal1 file>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <expSignal0 file> -o <expSignal1 file>'
         sys.exit()
      elif opt in ("-z", "--expSignal0"):
         expSignal0_inputfile = arg
      elif opt in ("-o", "--expSignal1"):
         expSignal1_inputfile = arg

   if expSignal0_inputfile and expSignal1_inputfile:
       print 'Input expSignal0 file is', expSignal0_inputfile
       print 'Input expSignal1 file is', expSignal1_inputfile
   else:
      print 'no input files are specified, exiting...'
      sys.exit(1)

   start_time = time.time()

   extractCanvasFromROOTfile(expSignal0_inputfile, expSignal1_inputfile)

   end_time = time.time()
   time_taken = end_time - start_time  # time_taken is in seconds                                                                                            
                                      

   hours, rest = divmod(time_taken, 3600)
   minutes, seconds = divmod(rest, 60)


   print
   print 'all done!'
   print "---it took {hours} hours, {minutes} minutes and {seconds:.1f} seconds to run the analysis ---".format(hours=hours,
                                                                                                          minutes=minutes,
                                                                                                          seconds=seconds)
   # raw_input("Press Enter to exit...")                                                                                                                         


if __name__ == "__main__":
   main(sys.argv[1:])



