from itertools import izip_longest
import subprocess
from ROOT import TFile
#import ROOT
import os, sys
import pprint
from glob import glob
from pprint import pprint as pp

debug = True

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

print 'good_dirs='
pp(good_dirs)

items, chunk = good_dirs, 12
mydirs=list(izip_longest(*[iter(items)]*chunk))
print 'mydirs'
pp(mydirs)

low_dirs = [x for x in good_dirs if "/low_" in x]
print 'low_dirs: ',  len(low_dirs)
pp(low_dirs)

high_dirs = [x for x in good_dirs if "/high_" in x]
#print 'high_dirs'
#pp(high_dirs)
bdtCuts = [0.4, 0.925, 0.99] if eleDir else [0.1,0.7,0.99]
good_high_dirs = [x for x in high_dirs if float(x.split('_')[-1]) in bdtCuts]
print 'good_high_dirs: ', len(good_high_dirs)
pp(good_high_dirs)


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
