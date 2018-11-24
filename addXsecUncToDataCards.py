from ROOT import TFile
import ROOT
import glob
import re
import subprocess
import time, os
import sys
import itertools
import multiprocessing
import glob
import shutil
import getopt
from copy import deepcopy
from array import array


onlyHHMTandBDT = True
CRDY_type = "CRDY"
#test_dc_name = 'copy_xsec_'
test_dc_name = 'copy_'
trueRun = True

channel = glob.glob("hh*eff_e_*")
if channel != [] and channel != None:
    channel = 'ee'  # comb_*")[0].split('_')[1]                                                                                                                               
else:
    channel = 'mm'



variables = [
    "bdt_response",
    "bdt_response_afterCut",
    "dR_bjets",
    "dR_leps",
    "hhMt",
    "hmass0",
    "hmass1",
    #"hmass1_oneBin",                                                                                                                                                                                                                                    
    "hpt0",
    "hpt1",
    "met_pt",
    "zmass",
    "zmass_high",
    #"zmass_oneBin",                                                                                                                                                                                                                                     
    "zpt0"
]



def copyAndCombineCards(varbl):
    print 'working with', varbl

    if onlyHHMTandBDT and not ('hh' in varbl or 'bdt' in varbl): return
   
    templ_dataCard  = 'dataCard_%s_%s.txt'
    datacards = []
    for reg in "SR", "CRTT", CRDY_type:
        datacards.append(templ_dataCard % (reg, varbl))

    # back up initial data cards                                                                                                                                                                                                                         
    for dc in datacards:

        new_dc = test_dc_name + dc
        shutil.copyfile(dc, new_dc)

    modifyDatacard(varbl, datacards)

    if 'hhMt' in varbl:
        comb_CRDYnCRTT = "combineCards.py " + test_dc_name + "dataCard_" + CRDY_type + "_hhMt.txt " + test_dc_name + "dataCard_CRTT_hhMt.txt > " + test_dc_name + "dataCard_" + CRDY_type + "nTT_hhMt.txt"
        comb_CRsnSR = "combineCards.py CRDY=" + test_dc_name + "dataCard_" + CRDY_type + "_hhMt.txt SR=" + test_dc_name + "dataCard_SR_hhMt.txt CRTT=" + test_dc_name + "dataCard_CRTT_hhMt.txt > " + test_dc_name + "dataCard_all_hhMt.txt && cp " + test_dc_name + "dataCard_all_hhMt.txt dataCard_hhMt_" + channel + ".txt"
        print
    # combine cards for various regions for HHMT only                                                                                                                                                                                                    

        for cmd in comb_CRDYnCRTT, comb_CRsnSR:
            print 'cmd=', cmd
            if trueRun: subprocess.call(cmd, shell=True)

    all_dc = glob.glob(test_dc_name + '*' + varbl + '*.txt')
    # add BBB uncertainty to data cards                                                                                                                                                                                                                  
    for dc in all_dc:  # [0:1]:                                                                                                                                                                                                                          
        print 'processing', dc
        cmd = 'echo "" >> ' + dc + ' && echo "* autoMCStats 0" >> ' + dc
        print 'cmd', cmd
        if trueRun: subprocess.call(cmd, shell=True)



def modifyDatacard(var, datacards):
    if onlyHHMTandBDT and not ('hh' in var or 'bdt' in var): return

    print 'working with', var
    #templ_dataCard  = 'dataCard_%s_%s.txt'                                                                                                                    
    mod_datacards = deepcopy(datacards)
    mod_datacards= [test_dc_name + x for x in mod_datacards]
    #for reg in "SR", "CRTT", CRDY_type:                                                                                                                       
     #   datacards.append(templ_dataCard % (reg, var))                                                                                                         

    for dc in mod_datacards:
        # back up initial data cards, they will be used by other functions later, below we rewrite old once                                                    
        #new_dc = dc[:-4] + '_original.txt'                                                                                                                    
        #shutil.copyfile(dc, new_dc)                                                                                                                           

        cmd = 'python  DataCardsREwriter_v3.py  -i ' + dc  + ' -o ' + dc
        print 'cmd=', cmd
        subprocess.call(cmd, shell=True)







def main(argv):
   inputfile = None
   outputfile = None
   rebin = None
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile=", "rebin="])
   except getopt.GetoptError:
      print 'test.py -i <inputfile> -o <outputfile> --rebin <rebinNumber>'
      #print 'opts=', opts                                                                                                                                                                                                                               
      #print 'args', args                                                                                                                                                                                                                                
      sys.exit(0)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("--rebin"):
         rebin = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg

   if inputfile and outputfile:
       print 'Input file is "', inputfile
       print 'Output file is "', outputfile

   start_time = time.time()
                                                                          
   for var in variables:
       print 'processing var=', var

       if onlyHHMTandBDT and not ('hh' in var or 'bdt' in var): continue

       print 'after processing var=', var
       print
       copyAndCombineCards(var)


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


