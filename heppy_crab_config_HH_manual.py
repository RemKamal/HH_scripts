from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'HH_V25_Oct'
config.General.workArea = 'crab_projects_oct2_1'
config.General.transferLogs=True

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'heppy_crab_fake_pset.py'
config.JobType.scriptExe = 'heppy_crab_script.sh'
import os
#os.system("tar czf python.tar.gz --dereference --directory $CMSSW_BASE python")                                                                                   

os.system("tar czf python.tar.gz --directory $CMSSW_BASE python `find $CMSSW_BASE/src -name python | perl -pe s#$CMSSW_BASE/## `")
#onfig.JobType.sendPythonFolder = True                                                                                                                             
config.JobType.maxMemoryMB = 2500
config.JobType.maxJobRuntimeMin = 2000
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

#config.Data.inputDBS = 'global'
#config.Data.splitting = 'LumiBased'  #for data?
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.totalUnits = -1
config.Data.outLFNDirBase = '/store/user/rkamalie/'
config.Data.publication = True
config.Data.outputDatasetTag = 'VHBB_V25'
#only for data
#config.Data.lumiMask = 'json.txt'


#config.Data.inputDataset = ''
#config.Data.userInputFiles = open('/eos/cms/store/user/rkamalie/BBVV_MINIAOD_650/bbvv_miniaod_650.txt').readlines()
#config.Data.outputPrimaryDataset = 'BBVV_650'

config.Data.outputPrimaryDataset = 'BBVV_260'
config.Data.userInputFiles = open('/afs/cern.ch/work/r/rkamalie/private/July31/v2/CMSSW_8_0_25/src/VHbbAnalysis/Heppy/test/crab/bbvv_miniaod_260.txt').readlines()

#config.Data.outputPrimaryDataset = 'BBVV_650'
#config.Data.userInputFiles = open('/afs/cern.ch/work/r/rkamalie/private/July31/v2/CMSSW_8_0_25/src/VHbbAnalysis/Heppy/test/crab/bbvv_miniaod_650.txt').readlines()
config.General.requestName+= "_"+config.Data.outputPrimaryDataset

config.section_("Site")
config.Site.storageSite = "T2_US_Nebraska"

#below is a hopeless try to deal with 650 and 260 gev bbVV samples
#config.Site.blacklist = ['T2_US_*']
#config.Site.blacklist = ['T2_US_Florida', 'T2_US_UCSD', 'T2_US_MIT', 'T2_US_Wisconsin']
#config.Site.whitelist = ['T2_EE_Estonia']
config.Site.whitelist = ['T2_CH_CERN']
#config.Site.whitelist = ['T2_EE_Estonia', 'T2_DE_DESY', 'T2_IT_Rome']
config.Data.ignoreLocality = False
# when TRUE The parameter Site.whitelist is mandatory and Site.blacklist can also be used and it is respected.
