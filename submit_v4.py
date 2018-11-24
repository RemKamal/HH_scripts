#!/usr/bin/env python

from sys import argv
import commands
import time
import re
import os
import io
import string
from os import listdir
from os.path import isfile, join
from string import digits, translate

import FWCore.ParameterSet.Config as cms

import sys
#sys.path.append('./')
numSampForDebug = -1 # to skip the last empty element ' ' 
step = 15 # number of samples per job to process with bsub
files_txt = argv[1]
samp = argv[2]

dirpath = os.getcwd()
destpath = dirpath + '/' + samp
parentdir = '../'

run = 'run_tree_skimmer_v2'

# usage python submit_v3_test.py ../comb_listOf_TT_Tune_trees.txt TT_Tune
################################################################################

def submit(sample, first, last, postfix=0):
    print "Running: submit.py "+run
    print 'current pwd is ', os.getcwd()
    #print 'sample name is ', sample
    
    # sampleNoDigits = sample[-10:].translate( digits)
    # print 'no digits version', sampleNoDigits

    # sampleNoDigits = sample[:-10] + sampleNoDigits
    # print 'new no digits version', sampleNoDigits

    # s_end = re.sub('[0-9]+', '', sample[-10:])
    # sample = sample[:-10] + s_end
    # sample = sample.replace("/tree_.root", "")
    
    #print 'new sample name is ', sample
    
    scriptName = 'job_'+samp +'_'+str(first)+'_'+str(last)+'.sh'
    jobName    = 'job_'+samp +'_'+str(first)+'_'+str(last)
    
    
    # if run=="run_tree_skimmer":
    #     outName = "tree_"+str(postfix)
    # print 'outName is ', outName
    if os.getcwd() == dirpath:
        if not os.path.exists(samp):
            os.makedirs(samp)
            print '************************creating a dir ', samp

    if os.getcwd() != destpath:
        os.chdir(destpath)
    print 'dirpath is ', dirpath
    print 'current pwd is ', os.getcwd()
    print 'should be equal to destpath, which is ', destpath
   
    # pretty_scriptName = scriptName[:]
    # pretty_jobName = jobName[:]
    # for ch in [':', '/']:
    #     pretty_scriptName = pretty_scriptName.replace(ch, "_")
    #     pretty_jobName = pretty_jobName.replace(ch, "_")

    with io.open( (destpath+'/'+scriptName), mode='wb') as f:
    #f = open(pretty_scriptName, mode='w')  
     #   print 'pretty scriptName is ', pretty_scriptName
        f.write('#!/bin/bash\n\n')
        cwd = os.getcwd()
        print 'inside with of submit', cwd
        f.write('cd ' + destpath+ '\n')
        
        #    f.write('cd /mnt/t3nfs01/data01/shome/bianchi/TTH-76X-heppy/CMSSW/src/TTH/MEIntegratorStandalone/test/macros\n')                                                                                
        #   f.write('source /swshare/psit3/etc/profile.d/cms_ui_env.sh\n')                                                                                                                                  
        f.write('source /cvmfs/cms.cern.ch/cmsset_default.sh\n')
        f.write('eval `scramv1 runtime -sh`\n')
        #f.write('cmsenv\n')
        f.write('\n')
        
        f.write('export X509_USER_PROXY=/afs/cern.ch/user/r/rkamalie/x509up_u27011\n')
    # maybe cd to inner dir
        #     f.write('export X509_USER_PROXY=/afs/cern.ch/user/r/rkamalie/workspace/private/Jan2017/CMSSW_8_0_21/src/VHbbAnalysis/Heppy/test/SkimNtuple/ samp   x509up_u27011\n')
    
        
        f.write('\n')    
        f.write('python ' +parentdir + run+ '.py ' +parentdir +files_txt+ ' '+str(first)+' '+str(last)+' ' +samp+ '\n')

    #    if run=="run_tree_skimmer":
    # f.write('mkdir '+samp+'\n')
        #        f.write('mv /scratch/$USER/'+sample+'/'+outName+'.root ./'+sample+'/'+'\n')    
        #    else:
        #        f.write('mv /scratch/$USER/'+outName+'.root ./'+'\n')    
        
        f.close()
        #
        #
        # where import, never rely on WITH statement, do it explicitly!
        #
        #
        os.system('chmod +x '+destpath+ '/'+scriptName) # vs chmod 755
        
    #    submitToQueue = 'bsub -q 8nh -G CMS_CERN01_YODA -J testXbb -u pippo123'+jobName+' '+scriptName
        
        submitToQueue =  'bsub -q 8nh -J '+jobName+ ' -u dummy12345@gmail.com < ' +destpath+'/'+scriptName              
        print 'submitToQueue is', submitToQueue
        os.system(submitToQueue)
        time.sleep( 2.0 )
        
        print "@@@@@ END JOB @@@@@@@@@@@@@@@"
    

##########################################

def main():
    print 'trying to open the file'
    with io.open (files_txt, mode="rt", encoding = "utf-8") as f:
        listOfFiles = f.read().split('\n')[:numSampForDebug] # for test purpose limit to 50
    
    print 'file was opened'
    if samp not in listOfFiles[0]:
        print 'An error happened, list of samples and sample name do NOT coincide, please check. See top of the script for the hint.'
        exit(1)
    
    listOfNum =[n for n in range(0, len(listOfFiles), step)] 
    last = first = 0
    for num, fil in zip (listOfNum, listOfFiles):
        first = num
        last = num + (step-1)
        #print 'file is {}, first job is {}, last job is {} are '.format (fil, first, last)
        submit( fil, first, last)
        



"""                                                                                                                                                         
for execution from another script                                                                                                                           
"""
if __name__ == "__main__":
    #sys.exit(main())                                                      
    main()
 
