import subprocess
import io
from shutil import copy2
from subprocess import Popen, PIPE, STDOUT

totalDir = 'analysis_mar25_total'
dirRegions = ['_sr_v3','_crTT_v3','_crDY_v3','_crDY_zerob_v3','_crDY_oneb_v3']
hzzDir = 'analysis_mar25_tot_hzz'
mainWebDir = '~/www/HH_mar30/'
webDir = mainWebDir + 'hzz'
totSignalJson = 'data/test_samples_mar25_total.json'
hzzSignalJson = 'data/test_samples_mar25_tot_hzz.json'
for d in dirRegions:
    inDir = totalDir + d
    outDir = hzzDir + d
    finalWebDir = webDir +d
    region = 'SR' if 'sr' in d else 'CR'
    cpCmd = 'cd ' + inDir + ' && cp ST* DY* *ZH* TT* W* Z* Bulk*300* muo* ../' + outDir + ' && cd - '
    json = hzzSignalJson if 'sr' in d else totSignalJson
    plotCmd = 'python  plotter_v9.py -i ' + outDir + ' -j ' + json + ' -k Stack -r ' + region
    createWebDirs = 'mkdir -p ' + finalWebDir
    movePlotsCmd = 'cp ' + outDir + '/plots/Stack/*png ' + finalWebDir
    makeWebCmd = 'cp /afs/cern.ch/user/r/rkamalie/www/index.php ' + finalWebDir + ' && cp /afs/cern.ch/user/r/rkamalie/www/index.php ' + mainWebDir 
    rmSomePlotsCmd = 'cd ' + finalWebDir + ' && rm cut*png && cd -'
    print cpCmd
    print plotCmd
    print createWebDirs
    print movePlotsCmd
    print makeWebCmd
    print rmSomePlotsCmd

    final = Popen("{0}; {1}; {2}; {3}; {4}; {5}".format(cpCmd, plotCmd, createWebDirs, movePlotsCmd, makeWebCmd, rmSomePlotsCmd), shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    stdout, nothing = final.communicate()
    logFile = 'log'+d
    log = io.open(logFile, 'wb')
    log.write(stdout)
    log.close()
