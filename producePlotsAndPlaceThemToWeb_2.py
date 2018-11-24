import subprocess
import io
from shutil import copy2
from subprocess import Popen, PIPE, STDOUT

trueRun = True
removeCutFlowEffPlot = True
version = '_v1'
date = 'apr18'
publishDate = 'apr20'
totalDir = 'analysis_' + date + '_total'
dirRegions = [ x+version for x in ['_SR', '_CRTT', '_CRDY', '_CRDY_1b', '_CRDY_0b'] ]
hzzDir = 'analysis_' + date + '_tot_hzz'
mainWebDir = '~/www/HH_' + publishDate + '/'
webDir = mainWebDir + 'hzz'
totSignalJson = 'data/test_samples_' + date + '_total.json'
hzzSignalJson = 'data/test_samples_' + date + '_tot_hzz.json'

jsonToPlot = 'data/toPlot_samples_' + date + '_total.json'
for d in dirRegions:
    print 'd is ', d
    inDir = totalDir + d
    outDir = hzzDir + d
    finalWebDir = webDir +d
    region = 'SR' if 'SR' in d else 'CR'
    cpCmd = 'cd ' + inDir + ' && cp ST* DY* *ZH* TT* W* Z* Bulk*{270,450,1000}* muo* ../' + outDir 
    #json = hzzSignalJson if 'sr' in d else totSignalJson
    json = jsonToPlot
    plotCmd = 'cd ../ && python  plotter_v10.py -i ' + outDir + ' -j ' + json + ' -k Stack -r ' + region
    createWebDirs = 'mkdir -p ' + finalWebDir
    movePlotsCmd = 'cp ' + outDir + '/plots/Stack/*png ' + finalWebDir
    makeWebCmd = 'cp /afs/cern.ch/user/r/rkamalie/www/index.php ' + finalWebDir + ' && cp /afs/cern.ch/user/r/rkamalie/www/index.php ' + mainWebDir 
    rmSomePlotsCmd = 'cd ' + finalWebDir 
    if removeCutFlowEffPlot:
        rmSomePlotsCmd += ' && rm cutFlowEff*png ' 
    rmSomePlotsCmd += ' && cd -'

    print cpCmd
    print plotCmd
    print createWebDirs
    print movePlotsCmd
    print makeWebCmd
    print rmSomePlotsCmd

    if trueRun:
        print 'about to start Popen'
        final = Popen("{0}; {1}; {2}; {3}; {4}; {5}".format(cpCmd, plotCmd, createWebDirs, movePlotsCmd, makeWebCmd, rmSomePlotsCmd), shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        stdout, nothing = final.communicate()
        logFile = 'log'+d
        log = io.open(logFile, 'wb')
        log.write(stdout)
        log.close()
    
    print '=\='*50
