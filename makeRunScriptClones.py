
# -------------------------------------------------------------------------
# | Function          |Copies Metadata|Copies Permissions|Can Specify Buffer|
# -------------------------------------------------------------------------
# | shutil.copy       |      No       |        Yes       |        No        |
# -------------------------------------------------------------------------
# | shutil.copyfile   |      No       |         No       |        No        |
# -------------------------------------------------------------------------
# | shutil.copy2      |     Yes       |        Yes       |        No        |
# -------------------------------------------------------------------------
# | shutil.copyfileobj|      No       |         No       |       Yes        |
# -------------------------------------------------------------------------

import shutil
regionsList = ['minitrees']#'SR', 'CRTT', 'CRDY', 'CRDY_0b', 'CRDY_1b', 'minitrees' ]


version = '16'
trueRun = True
analyzer = 'runSimpleAn_v' + version 
chainFile = 'runTests'

for region in regionsList:
    #region = region + 'test'
    if trueRun:
        shutil.copy2 ( analyzer + '.py', analyzer + '_' + region + '.py'   )    
    if region is not 'minitrees':
        if trueRun:
            shutil.copy2 ( chainFile + '.py', chainFile + '_' + region + '.py'   )
        strToRun = '{}{}{}{}{}{}{}{}{}{}{}'.format('python ', chainFile, '_', region, '.py ', region, ' &> log_', chainFile, '_', region, '.txt &')
    
        print strToRun

