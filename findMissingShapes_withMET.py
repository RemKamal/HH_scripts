from itertools import izip_longest
import subprocess
from ROOT import TFile
#import ROOT
import os, sys
import pprint
from glob import glob
from pprint import pprint as pp

debug = True
addMETcuts = True
# shapes = glob('*/')
# shapes = [s for s in shapes if 'shape' in s]
# print 'work with %s shapes, which are:' %  len(shapes)
# pp(shapes)
# print
badList = [



    ]

eleDir = True if 'eles' in os.getcwd() else False if 'muons' in os.getcwd() else None
RadionOrBulkGravitonArea = "Grav" if "Grav" in os.getcwd() else "Radion" if "Radion" in os.getcwd() else None
#eleDir = True
if eleDir == None or RadionOrBulkGravitonArea == None:
    print 'check eleDir or RadionOrBulkGravitonArea, exiting'
    sys.exit(1)
else:
    print 'doing eleDir =', eleDir
    print 'doing RadionOrBulkGravitonArea=', RadionOrBulkGravitonArea


skip1 = 'eff_e' if eleDir == False else 'eff_m_I' # if ele run do not check muons shapes and similarly in opprosite
skip2 = 'eff_e' if eleDir == False else 'eff_m_tr'
if 'eff' not in skip1 or 'eff' not in skip2:
    print 'check skip1/2, exiting'
    sys.exit(1)

print 'skip1 = {0}, skip2 = {1}'.format(skip1, skip2)
dirs = glob('*/*')
dirs = [d for d in dirs if d.startswith('shapes') and skip1 not in d and skip2 not in d]
print 'found {0} dirs'.format(len(dirs))
print 'dirs', dirs
print
count = 1
good_dirs = []
for idx, d in enumerate(dirs, start = 1):
    #print 'idx, d are', idx, ' ', d
    #if d in badList: continue
    if 'eff_met' in d: continue
    if 'CRDYlow' in d or 'CRDYhigh' in d or 'oneBin' in d: continue
    listOfTrees = None
    try:
        if debug:
            pass
        #if '/low_' not in d: continue
        #if 'shapes' not in d: continue
        #if 'trackerDown' in d and 'low' in d: continue
        if 'all' in d or 'good' in d or 'dy' in d or '650sha' in d or '450n' in d: continue
        #if 'shapes_CMS_eff_m_ISODown' in d: continue




        #print 'in try'
        listOfTrees = subprocess.check_output('ls ' + d + '/*shape*root', shell=True).split('\n')[:-1]
    except subprocess.CalledProcessError as e:
        print e    
    print 'count, d are', count, ' ', d
    #if len(listOfTrees)!= 27: 
     #   pass#print '!!!'*500
        #print 'damn it with d=', d

    #print 'listOfTrees =', listOfTrees
    cutoff_low = 36 if "Grav" in RadionOrBulkGravitonArea else 42
    cutoff_high = 42 if "Grav" in RadionOrBulkGravitonArea else 51 # 450 is present here TOO!
    if '/low_' in d and len(listOfTrees) != cutoff_low:
        print 'check dir = {0}'.format(d)
        print 'len(listOfTrees) is', len(listOfTrees), 'exiting'
        badList.append(d)#sys.exit(1)
        
    elif '/high_' in d and len(listOfTrees)!= cutoff_high:
        print 'check dir = {0}'.format(d)
        print 'len(listOfTrees) is', len(listOfTrees), 'exiting'
        badList.append(d)#sys.exit(1)
    else:
        good_dirs.append(d)
        #pass
        #print 'all is fine with dir {0}, which has {1} files'.format(d, len(listOfTrees) )
    
    print '-'*100
    count += 1




#to compare:
ee_low_dirs_to_compare = ['shapes_nominal/low_SR_0.4_met40',
 'shapes_nominal/low_SR_0.4_met75',
 'shapes_nominal/low_SR_0.925_met75',
 'shapes_nominal/low_CRTT_0.4_met40',
 'shapes_nominal/low_CRTT_0.4_met75',
 'shapes_nominal/low_CRTT_0.925_met75',
 'shapes_nominal/low_CRDY_0.4_met40',
 'shapes_nominal/low_CRDY_0.4_met75',
 'shapes_nominal/low_CRDY_0.925_met75',
 'shapes_CMS_eff_e_trackerUp/low_SR_0.4_met40',
 'shapes_CMS_eff_e_trackerUp/low_SR_0.4_met75',
 'shapes_CMS_eff_e_trackerUp/low_SR_0.925_met75',
 'shapes_CMS_eff_e_trackerUp/low_CRTT_0.4_met40',
 'shapes_CMS_eff_e_trackerUp/low_CRTT_0.4_met75',
 'shapes_CMS_eff_e_trackerUp/low_CRTT_0.925_met75',
 'shapes_CMS_eff_e_trackerUp/low_CRDY_0.4_met40',
 'shapes_CMS_eff_e_trackerUp/low_CRDY_0.4_met75',
 'shapes_CMS_eff_e_trackerUp/low_CRDY_0.925_met75',
 'shapes_CMS_eff_e_triggerUp/low_SR_0.4_met40',
 'shapes_CMS_eff_e_triggerUp/low_SR_0.4_met75',
 'shapes_CMS_eff_e_triggerUp/low_SR_0.925_met75',
 'shapes_CMS_eff_e_triggerUp/low_CRTT_0.4_met40',
 'shapes_CMS_eff_e_triggerUp/low_CRTT_0.4_met75',
 'shapes_CMS_eff_e_triggerUp/low_CRTT_0.925_met75',
 'shapes_CMS_eff_e_triggerUp/low_CRDY_0.4_met40',
 'shapes_CMS_eff_e_triggerUp/low_CRDY_0.4_met75',
 'shapes_CMS_eff_e_triggerUp/low_CRDY_0.925_met75',
 'shapes_CMS_btag_heavyUp/low_SR_0.4_met40',
 'shapes_CMS_btag_heavyUp/low_SR_0.4_met75',
 'shapes_CMS_btag_heavyUp/low_SR_0.925_met75',
 'shapes_CMS_btag_heavyUp/low_CRTT_0.4_met40',
 'shapes_CMS_btag_heavyUp/low_CRTT_0.4_met75',
 'shapes_CMS_btag_heavyUp/low_CRTT_0.925_met75',
 'shapes_CMS_btag_heavyUp/low_CRDY_0.4_met40',
 'shapes_CMS_btag_heavyUp/low_CRDY_0.4_met75',
 'shapes_CMS_btag_heavyUp/low_CRDY_0.925_met75',
 'shapes_CMS_scale_jDown/low_SR_0.4_met40',
 'shapes_CMS_scale_jDown/low_SR_0.4_met75',
 'shapes_CMS_scale_jDown/low_SR_0.925_met75',
 'shapes_CMS_scale_jDown/low_CRTT_0.4_met40',
 'shapes_CMS_scale_jDown/low_CRTT_0.4_met75',
 'shapes_CMS_scale_jDown/low_CRTT_0.925_met75',
 'shapes_CMS_scale_jDown/low_CRDY_0.4_met40',
 'shapes_CMS_scale_jDown/low_CRDY_0.4_met75',
 'shapes_CMS_scale_jDown/low_CRDY_0.925_met75',
 'shapes_CMS_eff_e_triggerDown/low_SR_0.4_met40',
 'shapes_CMS_eff_e_triggerDown/low_SR_0.4_met75',
 'shapes_CMS_eff_e_triggerDown/low_SR_0.925_met75',
 'shapes_CMS_eff_e_triggerDown/low_CRTT_0.4_met40',
 'shapes_CMS_eff_e_triggerDown/low_CRTT_0.4_met75',
 'shapes_CMS_eff_e_triggerDown/low_CRTT_0.925_met75',
 'shapes_CMS_eff_e_triggerDown/low_CRDY_0.4_met40',
 'shapes_CMS_eff_e_triggerDown/low_CRDY_0.4_met75',
 'shapes_CMS_eff_e_triggerDown/low_CRDY_0.925_met75',
 'shapes_CMS_eff_e_IDDown/low_SR_0.4_met40',
 'shapes_CMS_eff_e_IDDown/low_SR_0.4_met75',
 'shapes_CMS_eff_e_IDDown/low_SR_0.925_met75',
 'shapes_CMS_eff_e_IDDown/low_CRTT_0.4_met40',
 'shapes_CMS_eff_e_IDDown/low_CRTT_0.4_met75',
 'shapes_CMS_eff_e_IDDown/low_CRTT_0.925_met75',
 'shapes_CMS_eff_e_IDDown/low_CRDY_0.4_met40',
 'shapes_CMS_eff_e_IDDown/low_CRDY_0.4_met75',
 'shapes_CMS_eff_e_IDDown/low_CRDY_0.925_met75',
 'shapes_CMS_res_jUp/low_SR_0.4_met40',
 'shapes_CMS_res_jUp/low_SR_0.4_met75',
 'shapes_CMS_res_jUp/low_SR_0.925_met75',
 'shapes_CMS_res_jUp/low_CRTT_0.4_met40',
 'shapes_CMS_res_jUp/low_CRTT_0.4_met75',
 'shapes_CMS_res_jUp/low_CRTT_0.925_met75',
 'shapes_CMS_res_jUp/low_CRDY_0.4_met40',
 'shapes_CMS_res_jUp/low_CRDY_0.4_met75',
 'shapes_CMS_res_jUp/low_CRDY_0.925_met75',
 'shapes_CMS_eff_e_IDUp/low_SR_0.4_met40',
 'shapes_CMS_eff_e_IDUp/low_SR_0.4_met75',
 'shapes_CMS_eff_e_IDUp/low_SR_0.925_met75',
 'shapes_CMS_eff_e_IDUp/low_CRTT_0.4_met40',
 'shapes_CMS_eff_e_IDUp/low_CRTT_0.4_met75',
 'shapes_CMS_eff_e_IDUp/low_CRTT_0.925_met75',
 'shapes_CMS_eff_e_IDUp/low_CRDY_0.4_met40',
 'shapes_CMS_eff_e_IDUp/low_CRDY_0.4_met75',
 'shapes_CMS_eff_e_IDUp/low_CRDY_0.925_met75',
 'shapes_CMS_res_jDown/low_SR_0.4_met40',
 'shapes_CMS_res_jDown/low_SR_0.4_met75',
 'shapes_CMS_res_jDown/low_SR_0.925_met75',
 'shapes_CMS_res_jDown/low_CRTT_0.4_met40',
 'shapes_CMS_res_jDown/low_CRTT_0.4_met75',
 'shapes_CMS_res_jDown/low_CRTT_0.925_met75',
 'shapes_CMS_res_jDown/low_CRDY_0.4_met40',
 'shapes_CMS_res_jDown/low_CRDY_0.4_met75',
 'shapes_CMS_res_jDown/low_CRDY_0.925_met75',
 'shapes_CMS_btag_lightDown/low_SR_0.4_met40',
 'shapes_CMS_btag_lightDown/low_SR_0.4_met75',
 'shapes_CMS_btag_lightDown/low_SR_0.925_met75',
 'shapes_CMS_btag_lightDown/low_CRTT_0.4_met40',
 'shapes_CMS_btag_lightDown/low_CRTT_0.4_met75',
 'shapes_CMS_btag_lightDown/low_CRTT_0.925_met75',
 'shapes_CMS_btag_lightDown/low_CRDY_0.4_met40',
 'shapes_CMS_btag_lightDown/low_CRDY_0.4_met75',
 'shapes_CMS_btag_lightDown/low_CRDY_0.925_met75',
 'shapes_CMS_scale_jUp/low_SR_0.4_met40',
 'shapes_CMS_scale_jUp/low_SR_0.4_met75',
 'shapes_CMS_scale_jUp/low_SR_0.925_met75',
 'shapes_CMS_scale_jUp/low_CRTT_0.4_met40',
 'shapes_CMS_scale_jUp/low_CRTT_0.4_met75',
 'shapes_CMS_scale_jUp/low_CRTT_0.925_met75',
 'shapes_CMS_scale_jUp/low_CRDY_0.4_met40',
 'shapes_CMS_scale_jUp/low_CRDY_0.4_met75',
 'shapes_CMS_scale_jUp/low_CRDY_0.925_met75',
 'shapes_CMS_btag_heavyDown/low_SR_0.4_met40',
 'shapes_CMS_btag_heavyDown/low_SR_0.4_met75',
 'shapes_CMS_btag_heavyDown/low_SR_0.925_met75',
 'shapes_CMS_btag_heavyDown/low_CRTT_0.4_met40',
 'shapes_CMS_btag_heavyDown/low_CRTT_0.4_met75',
 'shapes_CMS_btag_heavyDown/low_CRTT_0.925_met75',
 'shapes_CMS_btag_heavyDown/low_CRDY_0.4_met40',
 'shapes_CMS_btag_heavyDown/low_CRDY_0.4_met75',
 'shapes_CMS_btag_heavyDown/low_CRDY_0.925_met75',
 'shapes_CMS_btag_lightUp/low_SR_0.4_met40',
 'shapes_CMS_btag_lightUp/low_SR_0.4_met75',
 'shapes_CMS_btag_lightUp/low_SR_0.925_met75',
 'shapes_CMS_btag_lightUp/low_CRTT_0.4_met40',
 'shapes_CMS_btag_lightUp/low_CRTT_0.4_met75',
 'shapes_CMS_btag_lightUp/low_CRTT_0.925_met75',
 'shapes_CMS_btag_lightUp/low_CRDY_0.4_met40',
 'shapes_CMS_btag_lightUp/low_CRDY_0.4_met75',
 'shapes_CMS_btag_lightUp/low_CRDY_0.925_met75',
 'shapes_CMS_eff_e_trackerDown/low_SR_0.4_met40',
 'shapes_CMS_eff_e_trackerDown/low_SR_0.4_met75',
 'shapes_CMS_eff_e_trackerDown/low_SR_0.925_met75',
 'shapes_CMS_eff_e_trackerDown/low_CRTT_0.4_met40',
 'shapes_CMS_eff_e_trackerDown/low_CRTT_0.4_met75',
 'shapes_CMS_eff_e_trackerDown/low_CRTT_0.925_met75',
 'shapes_CMS_eff_e_trackerDown/low_CRDY_0.4_met40',
 'shapes_CMS_eff_e_trackerDown/low_CRDY_0.4_met75',
 'shapes_CMS_eff_e_trackerDown/low_CRDY_0.925_met75']

ee_good_high_dirs_to_compare = ['shapes_nominal/high_SR_0.925_met75',
 'shapes_nominal/high_SR_0.99_met75',
 'shapes_nominal/high_SR_0.99_met100',
 'shapes_nominal/high_CRTT_0.925_met75',
 'shapes_nominal/high_CRTT_0.99_met75',
 'shapes_nominal/high_CRTT_0.99_met100',
 'shapes_nominal/high_CRDY_0.925_met75',
 'shapes_nominal/high_CRDY_0.99_met75',
 'shapes_nominal/high_CRDY_0.99_met100',
 'shapes_CMS_eff_e_trackerUp/high_SR_0.925_met75',
 'shapes_CMS_eff_e_trackerUp/high_SR_0.99_met75',
 'shapes_CMS_eff_e_trackerUp/high_SR_0.99_met100',
 'shapes_CMS_eff_e_trackerUp/high_CRTT_0.925_met75',
 'shapes_CMS_eff_e_trackerUp/high_CRTT_0.99_met75',
 'shapes_CMS_eff_e_trackerUp/high_CRTT_0.99_met100',
 'shapes_CMS_eff_e_trackerUp/high_CRDY_0.925_met75',
 'shapes_CMS_eff_e_trackerUp/high_CRDY_0.99_met75',
 'shapes_CMS_eff_e_trackerUp/high_CRDY_0.99_met100',
 'shapes_CMS_eff_e_triggerUp/high_SR_0.925_met75',
 'shapes_CMS_eff_e_triggerUp/high_SR_0.99_met75',
 'shapes_CMS_eff_e_triggerUp/high_SR_0.99_met100',
 'shapes_CMS_eff_e_triggerUp/high_CRTT_0.925_met75',
 'shapes_CMS_eff_e_triggerUp/high_CRTT_0.99_met75',
 'shapes_CMS_eff_e_triggerUp/high_CRTT_0.99_met100',
 'shapes_CMS_eff_e_triggerUp/high_CRDY_0.925_met75',
 'shapes_CMS_eff_e_triggerUp/high_CRDY_0.99_met75',
 'shapes_CMS_eff_e_triggerUp/high_CRDY_0.99_met100',
 'shapes_CMS_btag_heavyUp/high_SR_0.925_met75',
 'shapes_CMS_btag_heavyUp/high_SR_0.99_met75',
 'shapes_CMS_btag_heavyUp/high_SR_0.99_met100',
 'shapes_CMS_btag_heavyUp/high_CRTT_0.925_met75',
 'shapes_CMS_btag_heavyUp/high_CRTT_0.99_met75',
 'shapes_CMS_btag_heavyUp/high_CRTT_0.99_met100',
 'shapes_CMS_btag_heavyUp/high_CRDY_0.925_met75',
 'shapes_CMS_btag_heavyUp/high_CRDY_0.99_met75',
 'shapes_CMS_btag_heavyUp/high_CRDY_0.99_met100',
 'shapes_CMS_scale_jDown/high_SR_0.925_met75',
 'shapes_CMS_scale_jDown/high_SR_0.99_met75',
 'shapes_CMS_scale_jDown/high_SR_0.99_met100',
 'shapes_CMS_scale_jDown/high_CRTT_0.925_met75',
 'shapes_CMS_scale_jDown/high_CRTT_0.99_met75',
 'shapes_CMS_scale_jDown/high_CRTT_0.99_met100',
 'shapes_CMS_scale_jDown/high_CRDY_0.925_met75',
 'shapes_CMS_scale_jDown/high_CRDY_0.99_met75',
 'shapes_CMS_scale_jDown/high_CRDY_0.99_met100',
 'shapes_CMS_eff_e_triggerDown/high_SR_0.925_met75',
 'shapes_CMS_eff_e_triggerDown/high_SR_0.99_met75',
 'shapes_CMS_eff_e_triggerDown/high_SR_0.99_met100',
 'shapes_CMS_eff_e_triggerDown/high_CRTT_0.925_met75',
 'shapes_CMS_eff_e_triggerDown/high_CRTT_0.99_met75',
 'shapes_CMS_eff_e_triggerDown/high_CRTT_0.99_met100',
 'shapes_CMS_eff_e_triggerDown/high_CRDY_0.925_met75',
 'shapes_CMS_eff_e_triggerDown/high_CRDY_0.99_met75',
 'shapes_CMS_eff_e_triggerDown/high_CRDY_0.99_met100',
 'shapes_CMS_eff_e_IDDown/high_SR_0.925_met75',
 'shapes_CMS_eff_e_IDDown/high_SR_0.99_met75',
 'shapes_CMS_eff_e_IDDown/high_SR_0.99_met100',
 'shapes_CMS_eff_e_IDDown/high_CRTT_0.925_met75',
 'shapes_CMS_eff_e_IDDown/high_CRTT_0.99_met75',
 'shapes_CMS_eff_e_IDDown/high_CRTT_0.99_met100',
 'shapes_CMS_eff_e_IDDown/high_CRDY_0.925_met75',
 'shapes_CMS_eff_e_IDDown/high_CRDY_0.99_met75',
 'shapes_CMS_eff_e_IDDown/high_CRDY_0.99_met100',
 'shapes_CMS_res_jUp/high_SR_0.925_met75',
 'shapes_CMS_res_jUp/high_SR_0.99_met75',
 'shapes_CMS_res_jUp/high_SR_0.99_met100',
 'shapes_CMS_res_jUp/high_CRTT_0.925_met75',
 'shapes_CMS_res_jUp/high_CRTT_0.99_met75',
 'shapes_CMS_res_jUp/high_CRTT_0.99_met100',
 'shapes_CMS_res_jUp/high_CRDY_0.925_met75',
 'shapes_CMS_res_jUp/high_CRDY_0.99_met75',
 'shapes_CMS_res_jUp/high_CRDY_0.99_met100',
 'shapes_CMS_eff_e_IDUp/high_SR_0.925_met75',
 'shapes_CMS_eff_e_IDUp/high_SR_0.99_met75',
 'shapes_CMS_eff_e_IDUp/high_SR_0.99_met100',
 'shapes_CMS_eff_e_IDUp/high_CRTT_0.925_met75',
 'shapes_CMS_eff_e_IDUp/high_CRTT_0.99_met75',
 'shapes_CMS_eff_e_IDUp/high_CRTT_0.99_met100',
 'shapes_CMS_eff_e_IDUp/high_CRDY_0.925_met75',
 'shapes_CMS_eff_e_IDUp/high_CRDY_0.99_met75',
 'shapes_CMS_eff_e_IDUp/high_CRDY_0.99_met100',
 'shapes_CMS_res_jDown/high_SR_0.925_met75',
 'shapes_CMS_res_jDown/high_SR_0.99_met75',
 'shapes_CMS_res_jDown/high_SR_0.99_met100',
 'shapes_CMS_res_jDown/high_CRTT_0.925_met75',
 'shapes_CMS_res_jDown/high_CRTT_0.99_met75',
 'shapes_CMS_res_jDown/high_CRTT_0.99_met100',
 'shapes_CMS_res_jDown/high_CRDY_0.925_met75',
 'shapes_CMS_res_jDown/high_CRDY_0.99_met75',
 'shapes_CMS_res_jDown/high_CRDY_0.99_met100',
 'shapes_CMS_btag_lightDown/high_SR_0.925_met75',
 'shapes_CMS_btag_lightDown/high_SR_0.99_met75',
 'shapes_CMS_btag_lightDown/high_SR_0.99_met100',
 'shapes_CMS_btag_lightDown/high_CRTT_0.925_met75',
 'shapes_CMS_btag_lightDown/high_CRTT_0.99_met75',
 'shapes_CMS_btag_lightDown/high_CRTT_0.99_met100',
 'shapes_CMS_btag_lightDown/high_CRDY_0.925_met75',
 'shapes_CMS_btag_lightDown/high_CRDY_0.99_met75',
 'shapes_CMS_btag_lightDown/high_CRDY_0.99_met100',
 'shapes_CMS_scale_jUp/high_SR_0.925_met75',
 'shapes_CMS_scale_jUp/high_SR_0.99_met75',
 'shapes_CMS_scale_jUp/high_SR_0.99_met100',
 'shapes_CMS_scale_jUp/high_CRTT_0.925_met75',
 'shapes_CMS_scale_jUp/high_CRTT_0.99_met75',
 'shapes_CMS_scale_jUp/high_CRTT_0.99_met100',
 'shapes_CMS_scale_jUp/high_CRDY_0.925_met75',
 'shapes_CMS_scale_jUp/high_CRDY_0.99_met75',
 'shapes_CMS_scale_jUp/high_CRDY_0.99_met100',
 'shapes_CMS_btag_heavyDown/high_SR_0.925_met75',
 'shapes_CMS_btag_heavyDown/high_SR_0.99_met75',
 'shapes_CMS_btag_heavyDown/high_SR_0.99_met100',
 'shapes_CMS_btag_heavyDown/high_CRTT_0.925_met75',
 'shapes_CMS_btag_heavyDown/high_CRTT_0.99_met75',
 'shapes_CMS_btag_heavyDown/high_CRTT_0.99_met100',
 'shapes_CMS_btag_heavyDown/high_CRDY_0.925_met75',
 'shapes_CMS_btag_heavyDown/high_CRDY_0.99_met75',
 'shapes_CMS_btag_heavyDown/high_CRDY_0.99_met100',
 'shapes_CMS_btag_lightUp/high_SR_0.925_met75',
 'shapes_CMS_btag_lightUp/high_SR_0.99_met75',
 'shapes_CMS_btag_lightUp/high_SR_0.99_met100',
 'shapes_CMS_btag_lightUp/high_CRTT_0.925_met75',
 'shapes_CMS_btag_lightUp/high_CRTT_0.99_met75',
 'shapes_CMS_btag_lightUp/high_CRTT_0.99_met100',
 'shapes_CMS_btag_lightUp/high_CRDY_0.925_met75',
 'shapes_CMS_btag_lightUp/high_CRDY_0.99_met75',
 'shapes_CMS_btag_lightUp/high_CRDY_0.99_met100',
 'shapes_CMS_eff_e_trackerDown/high_SR_0.925_met75',
 'shapes_CMS_eff_e_trackerDown/high_SR_0.99_met75',
 'shapes_CMS_eff_e_trackerDown/high_SR_0.99_met100',
 'shapes_CMS_eff_e_trackerDown/high_CRTT_0.925_met75',
 'shapes_CMS_eff_e_trackerDown/high_CRTT_0.99_met75',
 'shapes_CMS_eff_e_trackerDown/high_CRTT_0.99_met100',
 'shapes_CMS_eff_e_trackerDown/high_CRDY_0.925_met75',
 'shapes_CMS_eff_e_trackerDown/high_CRDY_0.99_met75',
 'shapes_CMS_eff_e_trackerDown/high_CRDY_0.99_met100']

mm_low_dirs_to_compare = ['shapes_CMS_btag_heavyDown/low_CRDY_0.1_met40',
 'shapes_CMS_btag_heavyDown/low_CRDY_0.7_met40',
 'shapes_CMS_btag_heavyDown/low_CRDY_0.7_met75',
 'shapes_CMS_btag_heavyDown/low_CRTT_0.1_met40',
 'shapes_CMS_btag_heavyDown/low_CRTT_0.7_met40',
 'shapes_CMS_btag_heavyDown/low_CRTT_0.7_met75',
 'shapes_CMS_btag_heavyDown/low_SR_0.1_met40',
 'shapes_CMS_btag_heavyDown/low_SR_0.7_met40',
 'shapes_CMS_btag_heavyDown/low_SR_0.7_met75',

 'shapes_CMS_btag_heavyUp/low_CRDY_0.1_met40',
 'shapes_CMS_btag_heavyUp/low_CRDY_0.7_met40',
 'shapes_CMS_btag_heavyUp/low_CRDY_0.7_met75',
 'shapes_CMS_btag_heavyUp/low_CRTT_0.1_met40',
 'shapes_CMS_btag_heavyUp/low_CRTT_0.7_met40',
 'shapes_CMS_btag_heavyUp/low_CRTT_0.7_met75',
 'shapes_CMS_btag_heavyUp/low_SR_0.1_met40',
 'shapes_CMS_btag_heavyUp/low_SR_0.7_met40',
 'shapes_CMS_btag_heavyUp/low_SR_0.7_met75',

 'shapes_CMS_btag_lightDown/low_CRDY_0.1_met40',
 'shapes_CMS_btag_lightDown/low_CRDY_0.7_met40',
 'shapes_CMS_btag_lightDown/low_CRDY_0.7_met75',
 'shapes_CMS_btag_lightDown/low_CRTT_0.1_met40',
 'shapes_CMS_btag_lightDown/low_CRTT_0.7_met40',
 'shapes_CMS_btag_lightDown/low_CRTT_0.7_met75',
 'shapes_CMS_btag_lightDown/low_SR_0.1_met40',
 'shapes_CMS_btag_lightDown/low_SR_0.7_met40',
 'shapes_CMS_btag_lightDown/low_SR_0.7_met75',

 'shapes_CMS_btag_lightUp/low_CRDY_0.1_met40',
 'shapes_CMS_btag_lightUp/low_CRDY_0.7_met40',
 'shapes_CMS_btag_lightUp/low_CRDY_0.7_met75',
 'shapes_CMS_btag_lightUp/low_CRTT_0.1_met40',
 'shapes_CMS_btag_lightUp/low_CRTT_0.7_met40',
 'shapes_CMS_btag_lightUp/low_CRTT_0.7_met75',
 'shapes_CMS_btag_lightUp/low_SR_0.1_met40',
 'shapes_CMS_btag_lightUp/low_SR_0.7_met40',
 'shapes_CMS_btag_lightUp/low_SR_0.7_met75',

 'shapes_CMS_eff_m_IDDown/low_CRDY_0.1_met40',
 'shapes_CMS_eff_m_IDDown/low_CRDY_0.7_met40',
 'shapes_CMS_eff_m_IDDown/low_CRDY_0.7_met75',
 'shapes_CMS_eff_m_IDDown/low_CRTT_0.1_met40',
 'shapes_CMS_eff_m_IDDown/low_CRTT_0.7_met40',
 'shapes_CMS_eff_m_IDDown/low_CRTT_0.7_met75',
 'shapes_CMS_eff_m_IDDown/low_SR_0.1_met40',
 'shapes_CMS_eff_m_IDDown/low_SR_0.7_met40',
 'shapes_CMS_eff_m_IDDown/low_SR_0.7_met75',

 'shapes_CMS_eff_m_IDUp/low_CRDY_0.1_met40',
 'shapes_CMS_eff_m_IDUp/low_CRDY_0.7_met40',
 'shapes_CMS_eff_m_IDUp/low_CRDY_0.7_met75',
 'shapes_CMS_eff_m_IDUp/low_CRTT_0.1_met40',
 'shapes_CMS_eff_m_IDUp/low_CRTT_0.7_met40',
 'shapes_CMS_eff_m_IDUp/low_CRTT_0.7_met75',
 'shapes_CMS_eff_m_IDUp/low_SR_0.1_met40',
 'shapes_CMS_eff_m_IDUp/low_SR_0.7_met40',
 'shapes_CMS_eff_m_IDUp/low_SR_0.7_met75',

 'shapes_CMS_eff_m_ISODown/low_CRDY_0.1_met40',
 'shapes_CMS_eff_m_ISODown/low_CRDY_0.7_met40',
 'shapes_CMS_eff_m_ISODown/low_CRDY_0.7_met75',
 'shapes_CMS_eff_m_ISODown/low_CRTT_0.1_met40',
 'shapes_CMS_eff_m_ISODown/low_CRTT_0.7_met40',
 'shapes_CMS_eff_m_ISODown/low_CRTT_0.7_met75',
 'shapes_CMS_eff_m_ISODown/low_SR_0.1_met40',
 'shapes_CMS_eff_m_ISODown/low_SR_0.7_met40',
 'shapes_CMS_eff_m_ISODown/low_SR_0.7_met75',

 'shapes_CMS_eff_m_ISOUp/low_CRDY_0.1_met40',
 'shapes_CMS_eff_m_ISOUp/low_CRDY_0.7_met40',
 'shapes_CMS_eff_m_ISOUp/low_CRDY_0.7_met75',
 'shapes_CMS_eff_m_ISOUp/low_CRTT_0.1_met40',
 'shapes_CMS_eff_m_ISOUp/low_CRTT_0.7_met40',
 'shapes_CMS_eff_m_ISOUp/low_CRTT_0.7_met75',
 'shapes_CMS_eff_m_ISOUp/low_SR_0.1_met40',
 'shapes_CMS_eff_m_ISOUp/low_SR_0.7_met40',
 'shapes_CMS_eff_m_ISOUp/low_SR_0.7_met75',

 'shapes_CMS_eff_m_trackerDown/low_CRDY_0.1_met40',
 'shapes_CMS_eff_m_trackerDown/low_CRDY_0.7_met40',
 'shapes_CMS_eff_m_trackerDown/low_CRDY_0.7_met75',
 'shapes_CMS_eff_m_trackerDown/low_CRTT_0.1_met40',
 'shapes_CMS_eff_m_trackerDown/low_CRTT_0.7_met40',
 'shapes_CMS_eff_m_trackerDown/low_CRTT_0.7_met75',
 'shapes_CMS_eff_m_trackerDown/low_SR_0.1_met40',
 'shapes_CMS_eff_m_trackerDown/low_SR_0.7_met40',
 'shapes_CMS_eff_m_trackerDown/low_SR_0.7_met75',

 'shapes_CMS_eff_m_trackerUp/low_CRDY_0.1_met40',
 'shapes_CMS_eff_m_trackerUp/low_CRDY_0.7_met40',
 'shapes_CMS_eff_m_trackerUp/low_CRDY_0.7_met75',
 'shapes_CMS_eff_m_trackerUp/low_CRTT_0.1_met40',
 'shapes_CMS_eff_m_trackerUp/low_CRTT_0.7_met40',
 'shapes_CMS_eff_m_trackerUp/low_CRTT_0.7_met75',
 'shapes_CMS_eff_m_trackerUp/low_SR_0.1_met40',
 'shapes_CMS_eff_m_trackerUp/low_SR_0.7_met40',
 'shapes_CMS_eff_m_trackerUp/low_SR_0.7_met75',

 'shapes_CMS_eff_m_triggerDown/low_CRDY_0.1_met40',
 'shapes_CMS_eff_m_triggerDown/low_CRDY_0.7_met40',
 'shapes_CMS_eff_m_triggerDown/low_CRDY_0.7_met75',
 'shapes_CMS_eff_m_triggerDown/low_CRTT_0.1_met40',
 'shapes_CMS_eff_m_triggerDown/low_CRTT_0.7_met40',
 'shapes_CMS_eff_m_triggerDown/low_CRTT_0.7_met75',
 'shapes_CMS_eff_m_triggerDown/low_SR_0.1_met40',
 'shapes_CMS_eff_m_triggerDown/low_SR_0.7_met40',
 'shapes_CMS_eff_m_triggerDown/low_SR_0.7_met75',

 'shapes_CMS_eff_m_triggerUp/low_CRDY_0.1_met40',
 'shapes_CMS_eff_m_triggerUp/low_CRDY_0.7_met40',
 'shapes_CMS_eff_m_triggerUp/low_CRDY_0.7_met75',
 'shapes_CMS_eff_m_triggerUp/low_CRTT_0.1_met40',
 'shapes_CMS_eff_m_triggerUp/low_CRTT_0.7_met40',
 'shapes_CMS_eff_m_triggerUp/low_CRTT_0.7_met75',
 'shapes_CMS_eff_m_triggerUp/low_SR_0.1_met40',
 'shapes_CMS_eff_m_triggerUp/low_SR_0.7_met40',
 'shapes_CMS_eff_m_triggerUp/low_SR_0.7_met75',

 'shapes_CMS_res_jDown/low_CRDY_0.1_met40',
 'shapes_CMS_res_jDown/low_CRDY_0.7_met40',
 'shapes_CMS_res_jDown/low_CRDY_0.7_met75',
 'shapes_CMS_res_jDown/low_CRTT_0.1_met40',
 'shapes_CMS_res_jDown/low_CRTT_0.7_met40',
 'shapes_CMS_res_jDown/low_CRTT_0.7_met75',
 'shapes_CMS_res_jDown/low_SR_0.1_met40',
 'shapes_CMS_res_jDown/low_SR_0.7_met40',
 'shapes_CMS_res_jDown/low_SR_0.7_met75',

 'shapes_CMS_res_jUp/low_CRDY_0.1_met40',
 'shapes_CMS_res_jUp/low_CRDY_0.7_met40',
 'shapes_CMS_res_jUp/low_CRDY_0.7_met75',
 'shapes_CMS_res_jUp/low_CRTT_0.1_met40',
 'shapes_CMS_res_jUp/low_CRTT_0.7_met40',
 'shapes_CMS_res_jUp/low_CRTT_0.7_met75',
 'shapes_CMS_res_jUp/low_SR_0.1_met40',
 'shapes_CMS_res_jUp/low_SR_0.7_met40',
 'shapes_CMS_res_jUp/low_SR_0.7_met75',

 'shapes_CMS_scale_jDown/low_CRDY_0.1_met40',
 'shapes_CMS_scale_jDown/low_CRDY_0.7_met40',
 'shapes_CMS_scale_jDown/low_CRDY_0.7_met75',
 'shapes_CMS_scale_jDown/low_CRTT_0.1_met40',
 'shapes_CMS_scale_jDown/low_CRTT_0.7_met40',
 'shapes_CMS_scale_jDown/low_CRTT_0.7_met75',
 'shapes_CMS_scale_jDown/low_SR_0.1_met40',
 'shapes_CMS_scale_jDown/low_SR_0.7_met40',
 'shapes_CMS_scale_jDown/low_SR_0.7_met75',

 'shapes_CMS_scale_jUp/low_CRDY_0.1_met40',
 'shapes_CMS_scale_jUp/low_CRDY_0.7_met40',
 'shapes_CMS_scale_jUp/low_CRDY_0.7_met75',
 'shapes_CMS_scale_jUp/low_CRTT_0.1_met40',
 'shapes_CMS_scale_jUp/low_CRTT_0.7_met40',
 'shapes_CMS_scale_jUp/low_CRTT_0.7_met75',
 'shapes_CMS_scale_jUp/low_SR_0.1_met40',
 'shapes_CMS_scale_jUp/low_SR_0.7_met40',
 'shapes_CMS_scale_jUp/low_SR_0.7_met75',

 'shapes_nominal/low_CRDY_0.1_met40',
 'shapes_nominal/low_CRDY_0.7_met40',
 'shapes_nominal/low_CRDY_0.7_met75',
 'shapes_nominal/low_CRTT_0.1_met40',
 'shapes_nominal/low_CRTT_0.7_met40',
 'shapes_nominal/low_CRTT_0.7_met75',
 'shapes_nominal/low_SR_0.1_met40',
 'shapes_nominal/low_SR_0.7_met40',
 'shapes_nominal/low_SR_0.7_met75']

mm_good_high_dirs_to_compare = ['shapes_CMS_btag_heavyDown/high_CRDY_0.7_met75',
 'shapes_CMS_btag_heavyDown/high_CRDY_0.99_met100',
 'shapes_CMS_btag_heavyDown/high_CRDY_0.99_met75',
 'shapes_CMS_btag_heavyDown/high_CRTT_0.7_met75',
 'shapes_CMS_btag_heavyDown/high_CRTT_0.99_met100',
 'shapes_CMS_btag_heavyDown/high_CRTT_0.99_met75',
 'shapes_CMS_btag_heavyDown/high_SR_0.7_met75',
 'shapes_CMS_btag_heavyDown/high_SR_0.99_met100',
 'shapes_CMS_btag_heavyDown/high_SR_0.99_met75',

 'shapes_CMS_btag_heavyUp/high_CRDY_0.7_met75',
 'shapes_CMS_btag_heavyUp/high_CRDY_0.99_met100',
 'shapes_CMS_btag_heavyUp/high_CRDY_0.99_met75',
 'shapes_CMS_btag_heavyUp/high_CRTT_0.7_met75',
 'shapes_CMS_btag_heavyUp/high_CRTT_0.99_met100',
 'shapes_CMS_btag_heavyUp/high_CRTT_0.99_met75',
 'shapes_CMS_btag_heavyUp/high_SR_0.7_met75',
 'shapes_CMS_btag_heavyUp/high_SR_0.99_met100',
 'shapes_CMS_btag_heavyUp/high_SR_0.99_met75',

 'shapes_CMS_btag_lightDown/high_CRDY_0.7_met75',
 'shapes_CMS_btag_lightDown/high_CRDY_0.99_met100',
 'shapes_CMS_btag_lightDown/high_CRDY_0.99_met75',
 'shapes_CMS_btag_lightDown/high_CRTT_0.7_met75',
 'shapes_CMS_btag_lightDown/high_CRTT_0.99_met100',
 'shapes_CMS_btag_lightDown/high_CRTT_0.99_met75',
 'shapes_CMS_btag_lightDown/high_SR_0.7_met75',
 'shapes_CMS_btag_lightDown/high_SR_0.99_met100',
 'shapes_CMS_btag_lightDown/high_SR_0.99_met75',

 'shapes_CMS_btag_lightUp/high_CRDY_0.7_met75',
 'shapes_CMS_btag_lightUp/high_CRDY_0.99_met100',
 'shapes_CMS_btag_lightUp/high_CRDY_0.99_met75',
 'shapes_CMS_btag_lightUp/high_CRTT_0.7_met75',
 'shapes_CMS_btag_lightUp/high_CRTT_0.99_met100',
 'shapes_CMS_btag_lightUp/high_CRTT_0.99_met75',
 'shapes_CMS_btag_lightUp/high_SR_0.7_met75',
 'shapes_CMS_btag_lightUp/high_SR_0.99_met100',
 'shapes_CMS_btag_lightUp/high_SR_0.99_met75',

 'shapes_CMS_eff_m_IDDown/high_CRDY_0.7_met75',
 'shapes_CMS_eff_m_IDDown/high_CRDY_0.99_met100',
 'shapes_CMS_eff_m_IDDown/high_CRDY_0.99_met75',
 'shapes_CMS_eff_m_IDDown/high_CRTT_0.7_met75',
 'shapes_CMS_eff_m_IDDown/high_CRTT_0.99_met100',
 'shapes_CMS_eff_m_IDDown/high_CRTT_0.99_met75',
 'shapes_CMS_eff_m_IDDown/high_SR_0.7_met75',
 'shapes_CMS_eff_m_IDDown/high_SR_0.99_met100',
 'shapes_CMS_eff_m_IDDown/high_SR_0.99_met75',

 'shapes_CMS_eff_m_IDUp/high_CRDY_0.7_met75',
 'shapes_CMS_eff_m_IDUp/high_CRDY_0.99_met100',
 'shapes_CMS_eff_m_IDUp/high_CRDY_0.99_met75',
 'shapes_CMS_eff_m_IDUp/high_CRTT_0.7_met75',
 'shapes_CMS_eff_m_IDUp/high_CRTT_0.99_met100',
 'shapes_CMS_eff_m_IDUp/high_CRTT_0.99_met75',
 'shapes_CMS_eff_m_IDUp/high_SR_0.7_met75',
 'shapes_CMS_eff_m_IDUp/high_SR_0.99_met100',
 'shapes_CMS_eff_m_IDUp/high_SR_0.99_met75',

 'shapes_CMS_eff_m_ISODown/high_CRDY_0.7_met75',
 'shapes_CMS_eff_m_ISODown/high_CRDY_0.99_met100',
 'shapes_CMS_eff_m_ISODown/high_CRDY_0.99_met75',
 'shapes_CMS_eff_m_ISODown/high_CRTT_0.7_met75',
 'shapes_CMS_eff_m_ISODown/high_CRTT_0.99_met100',
 'shapes_CMS_eff_m_ISODown/high_CRTT_0.99_met75',
 'shapes_CMS_eff_m_ISODown/high_SR_0.7_met75',
 'shapes_CMS_eff_m_ISODown/high_SR_0.99_met100',
 'shapes_CMS_eff_m_ISODown/high_SR_0.99_met75',

 'shapes_CMS_eff_m_ISOUp/high_CRDY_0.7_met75',
 'shapes_CMS_eff_m_ISOUp/high_CRDY_0.99_met100',
 'shapes_CMS_eff_m_ISOUp/high_CRDY_0.99_met75',
 'shapes_CMS_eff_m_ISOUp/high_CRTT_0.7_met75',
 'shapes_CMS_eff_m_ISOUp/high_CRTT_0.99_met100',
 'shapes_CMS_eff_m_ISOUp/high_CRTT_0.99_met75',
 'shapes_CMS_eff_m_ISOUp/high_SR_0.7_met75',
 'shapes_CMS_eff_m_ISOUp/high_SR_0.99_met100',
 'shapes_CMS_eff_m_ISOUp/high_SR_0.99_met75',

 'shapes_CMS_eff_m_trackerDown/high_CRDY_0.7_met75',
 'shapes_CMS_eff_m_trackerDown/high_CRDY_0.99_met100',
 'shapes_CMS_eff_m_trackerDown/high_CRDY_0.99_met75',
 'shapes_CMS_eff_m_trackerDown/high_CRTT_0.7_met75',
 'shapes_CMS_eff_m_trackerDown/high_CRTT_0.99_met100',
 'shapes_CMS_eff_m_trackerDown/high_CRTT_0.99_met75',
 'shapes_CMS_eff_m_trackerDown/high_SR_0.7_met75',
 'shapes_CMS_eff_m_trackerDown/high_SR_0.99_met100',
 'shapes_CMS_eff_m_trackerDown/high_SR_0.99_met75',


 'shapes_CMS_eff_m_trackerUp/high_CRDY_0.7_met75',
 'shapes_CMS_eff_m_trackerUp/high_CRDY_0.99_met100',
 'shapes_CMS_eff_m_trackerUp/high_CRDY_0.99_met75',
 'shapes_CMS_eff_m_trackerUp/high_CRTT_0.7_met75',
 'shapes_CMS_eff_m_trackerUp/high_CRTT_0.99_met100',
 'shapes_CMS_eff_m_trackerUp/high_CRTT_0.99_met75',
 'shapes_CMS_eff_m_trackerUp/high_SR_0.7_met75',
 'shapes_CMS_eff_m_trackerUp/high_SR_0.99_met100',
 'shapes_CMS_eff_m_trackerUp/high_SR_0.99_met75',

 'shapes_CMS_eff_m_triggerDown/high_CRDY_0.7_met75',
 'shapes_CMS_eff_m_triggerDown/high_CRDY_0.99_met100',
 'shapes_CMS_eff_m_triggerDown/high_CRDY_0.99_met75',
 'shapes_CMS_eff_m_triggerDown/high_CRTT_0.7_met75',
 'shapes_CMS_eff_m_triggerDown/high_CRTT_0.99_met100',
 'shapes_CMS_eff_m_triggerDown/high_CRTT_0.99_met75',
 'shapes_CMS_eff_m_triggerDown/high_SR_0.7_met75',
 'shapes_CMS_eff_m_triggerDown/high_SR_0.99_met100',
 'shapes_CMS_eff_m_triggerDown/high_SR_0.99_met75',

 'shapes_CMS_eff_m_triggerUp/high_CRDY_0.7_met75',
 'shapes_CMS_eff_m_triggerUp/high_CRDY_0.99_met100',
 'shapes_CMS_eff_m_triggerUp/high_CRDY_0.99_met75',
 'shapes_CMS_eff_m_triggerUp/high_CRTT_0.7_met75',
 'shapes_CMS_eff_m_triggerUp/high_CRTT_0.99_met100',
 'shapes_CMS_eff_m_triggerUp/high_CRTT_0.99_met75',
 'shapes_CMS_eff_m_triggerUp/high_SR_0.7_met75',
 'shapes_CMS_eff_m_triggerUp/high_SR_0.99_met100',
 'shapes_CMS_eff_m_triggerUp/high_SR_0.99_met75',

 'shapes_CMS_res_jDown/high_CRDY_0.7_met75',
 'shapes_CMS_res_jDown/high_CRDY_0.99_met100',
 'shapes_CMS_res_jDown/high_CRDY_0.99_met75',
 'shapes_CMS_res_jDown/high_CRTT_0.7_met75',
 'shapes_CMS_res_jDown/high_CRTT_0.99_met100',
 'shapes_CMS_res_jDown/high_CRTT_0.99_met75',
 'shapes_CMS_res_jDown/high_SR_0.7_met75',
 'shapes_CMS_res_jDown/high_SR_0.99_met100',
 'shapes_CMS_res_jDown/high_SR_0.99_met75',

 'shapes_CMS_res_jUp/high_CRDY_0.7_met75',
 'shapes_CMS_res_jUp/high_CRDY_0.99_met100',
 'shapes_CMS_res_jUp/high_CRDY_0.99_met75',
 'shapes_CMS_res_jUp/high_CRTT_0.7_met75',
 'shapes_CMS_res_jUp/high_CRTT_0.99_met100',
 'shapes_CMS_res_jUp/high_CRTT_0.99_met75',
 'shapes_CMS_res_jUp/high_SR_0.7_met75',
 'shapes_CMS_res_jUp/high_SR_0.99_met100',
 'shapes_CMS_res_jUp/high_SR_0.99_met75',

 'shapes_CMS_scale_jDown/high_CRDY_0.7_met75',
 'shapes_CMS_scale_jDown/high_CRDY_0.99_met100',
 'shapes_CMS_scale_jDown/high_CRDY_0.99_met75',
 'shapes_CMS_scale_jDown/high_CRTT_0.7_met75',
 'shapes_CMS_scale_jDown/high_CRTT_0.99_met100',
 'shapes_CMS_scale_jDown/high_CRTT_0.99_met75',
 'shapes_CMS_scale_jDown/high_SR_0.7_met75',
 'shapes_CMS_scale_jDown/high_SR_0.99_met100',
 'shapes_CMS_scale_jDown/high_SR_0.99_met75',

 'shapes_CMS_scale_jUp/high_CRDY_0.7_met75',
 'shapes_CMS_scale_jUp/high_CRDY_0.99_met100',
 'shapes_CMS_scale_jUp/high_CRDY_0.99_met75',
 'shapes_CMS_scale_jUp/high_CRTT_0.7_met75',
 'shapes_CMS_scale_jUp/high_CRTT_0.99_met100',
 'shapes_CMS_scale_jUp/high_CRTT_0.99_met75',
 'shapes_CMS_scale_jUp/high_SR_0.7_met75',
 'shapes_CMS_scale_jUp/high_SR_0.99_met100',
 'shapes_CMS_scale_jUp/high_SR_0.99_met75',

 'shapes_nominal/high_CRDY_0.7_met75',
 'shapes_nominal/high_CRDY_0.99_met100',
 'shapes_nominal/high_CRDY_0.99_met75',
 'shapes_nominal/high_CRTT_0.7_met75',
 'shapes_nominal/high_CRTT_0.99_met100',
 'shapes_nominal/high_CRTT_0.99_met75',
 'shapes_nominal/high_SR_0.7_met75',
 'shapes_nominal/high_SR_0.99_met100',
 'shapes_nominal/high_SR_0.99_met75']



print 'good_dirs='
pp(good_dirs)

items, chunk = good_dirs, 12
if addMETcuts: chunk = 18
mydirs=list(izip_longest(*[iter(items)]*chunk))
print 'mydirs'
pp(sorted(mydirs))

low_dirs = [x for x in good_dirs if "/low_" in x]
print 'low_dirs: ',  len(low_dirs)
pp(sorted(low_dirs))

high_dirs = [x for x in good_dirs if "/high_" in x]
#print 'high_dirs'
#pp(high_dirs)
bdtCuts = [0.4, 0.925, 0.99] if eleDir else [0.1,0.7,0.99]
good_high_dirs = [x for x in high_dirs if float(x.split('_')[-2]) in bdtCuts]
print 'good_high_dirs: ', len(good_high_dirs)
pp(sorted(good_high_dirs))


if "Grav" in RadionOrBulkGravitonArea:
    if not addMETcuts:
        pass
    else:
        if eleDir:
            if len(low_dirs) != 90:
                print 'check low_dirs'
            elif len(good_high_dirs)!=90:
                print 'check good_high_dirs'
            else:
                pass
        else:
            if len(low_dirs) != 102:
                print 'check low_dirs'
            elif len(good_high_dirs)!=102:
                print 'check good_high_dirs'
            else:
                pass
elif "Radion" in RadionOrBulkGravitonArea:
    if not addMETcuts:
        pass
    else:
        if eleDir:
            if len(low_dirs) != 135:
                print 'check low_dirs'
                print set(low_dirs).symmetric_difference(set(ee_low_dirs_to_compare))
            elif len(good_high_dirs)!=135:
                print 'check good_high_dirs'
                print set(good_high_dirs).symmetric_difference(set(ee_good_high_dirs_to_compare))
            else:
                pass
        else:
            if len(low_dirs) != 153:
                print 'check low_dirs'
                print set(low_dirs).symmetric_difference(set(mm_low_dirs_to_compare))
            elif len(good_high_dirs)!=153:
                print 'check good_high_dirs'
                print set(good_high_dirs).symmetric_difference(set(mm_good_high_dirs_to_compare))
            else:
                pass

else:
    print 'smth is from with RadionOrBulkGravitonArea, exiting...'
    sys.exit(1)


print
print 'badList:', len(badList)
pp(badList)
# allFiles = set(listOfTrees)
# badFilesList = []




# for fil in listOfTrees:
#     if fil:
#         print 'working with', fil
#         try:
#             print 'IN THE TRY'
#             root_f = TFile.Open(fil)
#             tree=root_f.Get('tree')
#             size = os.stat(fil).st_size
#             if root_f.IsZombie() or not root_f.IsOpen() or root_f.TestBit(TFile.kRecovered) or size <= 1000 or not tree:
#                 print 'ZOMBIE file {0}'.format(fil)
#                 badFilesList.append(fil)
#         except Exception as e:
#             print 'IN THE EXCEPTION'
#             print 'file {0} has size {1}.'.format(fil, size)
#             print e
#             badFilesList.append(fil)

#         print
#         print

# badFiles = set (badFilesList)
# goodFiles = allFiles.symmetric_difference(badFiles)
# print '{0} goodFiles are:'.format(len(goodFiles)) 
# pprint.pprint(goodFiles)


# print 'badFiles:'
# pprint.pprint(badFiles) 
