import subprocess
import getopt
import time
import sys
import os
import shlex
from math import sqrt
trueRun = True
import glob

def runMLNorms():
   runMLNormsCmd = 'python /afs/cern.ch/work/r/rkamalie/private/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/test/mlfitNormsToText.py fitDiagnostics_all.root  -u >& log_MLNorms.txt'
   print 'runMLNormsCmd=', runMLNormsCmd
   if trueRun: subprocess.call(runMLNormsCmd, shell=True)


def getNorms(inputfile=''):
   if inputfile:
      print 'inputfile=', inputfile
   getPostfitNorms = False
   if inputfile:
      getPostfitNorms = True
      inputfile = inputfile
   else:
      inputfile = 'log_MLNorms.txt'

   text = []
   log_files = glob.glob('log*PostFitShapesFromWorkspace*Full*txt')
   if log_files != [] and '_ee_' not in log_files[0] and getPostfitNorms:
      inputfile = inputfile.replace('_ee_', '_mm_')
      #print 'inputfile', inputfile
 
   if os.path.exists(inputfile):
      #print 'reading', inputfile
      with open(inputfile, 'r') as f:
         text = f.readlines()
   else:
      return
   if text == []:
      print 'empty text, exiting...'
      sys.exit(1)

   for idx, line in enumerate(text):
      if getPostfitNorms:
         tmp_list = shlex.split(line)
         channelAndRegion = inputfile.split('PostFitShapesFromWorkspace_')[-1].split('_hhMt')[0]
         #print 'channelAndRegion', channelAndRegion
         #print 'tmp_list', tmp_list
         if  tmp_list != [] and channelAndRegion == tmp_list[0] and len(tmp_list) == 3:
            print tmp_list

      else:
         if idx > 0 :
            #print(shlex.split(line))
            results = calcNormalizationSF(shlex.split(line))
            print results

def calcNormalizationSF(line):
   prefitValue = float(line[2]) 
   prefitUnc   = float(line[4])
   # s+b fit
   postfitValue = float(line[5])
   postfitUnc   = float(line[7])

   ratio = round(postfitValue/prefitValue, 2)
   # error propagation for ratio
   #dR/R = sqrt (  (dNum/Num)^2 + (dDen/Den)^2  )
   dR = round (ratio * sqrt( (prefitUnc/prefitValue)**2 + (postfitUnc/postfitValue)**2 ), 2)
   return (line[0], line[1], ratio, '+/-', dR)


   


def main(argv):
   inputfile = None
   outputfile = None
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
      print 'all is fine here'
   except getopt.GetoptError:
      print 'test.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg

   if inputfile or outputfile:
       print 'Input file is', inputfile
       print 'Output file is', outputfile
   
   if opts == []:
      print 'proceding with no options specified'
   start_time = time.time()

   

   runMLNorms()
   getNorms()
   print 
   
   #notice it relised that log is present below. It should be produced by putTogetherHists_makePostfitRoots_v2.py
   inputfile = inputfile if inputfile else 'log_PostFitShapesFromWorkspace_ee_CRDY_hhMt_FullPostfit.txt'
   #getNorms(inputfile) #PostFitShapesFromWorkspace
   logs = [inputfile, inputfile.replace('CRDY', 'CRTT'), inputfile.replace('CRDY', 'SR')]
   
   for fil in logs:
      #print 'processing', fil
      getNorms(fil)
      print 


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


