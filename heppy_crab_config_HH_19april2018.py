from WMCore.Configuration import Configuration
config = Configuration()
import time
import os

config.section_("General")
config.General.requestName = 'HH_V25_April'
config.General.workArea = 'crab_projects_19apr2018_1'
config.General.transferLogs=True

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'heppy_crab_fake_pset.py'
config.JobType.scriptExe = 'heppy_crab_script.sh'
import os
#os.system("tar czf python.tar.gz --dereference --directory $CMSSW_BASE python")                                                                                   

print "Local current time :", time.asctime( time.localtime(time.time()) )

#For Unix, the epoch is 1970.
if not os.path.isfile("python.tar.gz") or (os.path.isfile("python.tar.gz") and (time.time() - os.path.getmtime("python.tar.gz") > (1 * 30 * 24 * 60 * 60))): # if the file is more than 1 month old or if does not exist
    print 'ABOUT TO TAR THE directory'
    os.system("tar czf python.tar.gz --directory $CMSSW_BASE python `find $CMSSW_BASE/src -name python | perl -pe s#$CMSSW_BASE/## `")
    print 'AFter the TAR of THE directory'

print "Local current time :", time.asctime( time.localtime(time.time()) )
#onfig.JobType.sendPythonFolder = True                                                                                                                             
config.JobType.maxMemoryMB = 2500
config.JobType.maxJobRuntimeMin = 1000 #2000 before used for previous versions
config.JobType.inputFiles = ['heppy_config.py',
                             'heppy_crab_script.py',
                             'python.tar.gz',
#                             'MVAJetTags_620SLHCX_Phase1And2Upgrade.db',
                             'combined_cmssw.py',
                             '../vhbb.py',
                             '../vhbb_combined.py',
                             '../TMVA_blikelihood_vbf_cmssw76.weights.xml',
                             'TMVAClassification_BDT.weights.xml',
                             'puData.root',
                             'puMC.root',
                             'puDataMinus.root',
                             'puDataPlus.root',
                              'json.txt',
                              '../silver.txt',
                              #"../Zll-spring15.weights.xml",
                              #"../Wln-spring15.weights.xml",
                              #"../Znn-spring15.weights.xml",
                              #"../VBF-spring15.weights.xml",
                              #"../ttbar-spring15.weights.xml",
                              #"../ttbar-fall15.weights.xml",
                              #"../ttbar-fall15_TargetGenOverPt_GenPtCut0.weights.xml",
                              '../ttbar-G25-500k-13d-300t.weights.xml',
                              '../triggerEmulation.root',
			      #'../ttbar-spring16-80X.weights.xml',
                              '../TMVA_blikelihood_vbf_cmssw76_h21trained.weights.xml',
]
#config.JobType.outputFiles = ['tree.root']

config.section_("Data")
config.Data.inputDataset = ''
config.Data.inputDBS = 'global'
#config.Data.splitting = 'LumiBased'  #for data?
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.totalUnits = -1
config.Data.outLFNDirBase = '/store/user/rkamalie/'
config.Data.publication = True
config.Data.outputDatasetTag = 'VHBB_V25'
#only for data
#config.Data.lumiMask = 'json.txt'


config.section_("Site")
config.Site.storageSite = "T2_US_Nebraska"

#use below when need to skip local sites and run somewhere else
#config.Data.ignoreLocality = False 
#config.Site.blacklist = ['T2_US_UCSD', 'T3_*']                                      
#config.Site.whitelist = ['T2_US_MIT', 'T2_US_Purdue', 'T2_US_Wisconsin', 'T2_US_Nebraska', 'T3_UK_SGrid_Oxford', 'T2_EE_Estonia']
# when TRUE The parameter Site.whitelist is mandatory and Site.blacklist can also be used and it is respected.
