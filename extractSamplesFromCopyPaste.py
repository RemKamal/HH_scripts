import re
import io
from datetime import date
today = date.today().strftime("%B%d")

copyPasteFile = 'copyPaste.txt'

with io.open (copyPasteFile, mode ='tr') as f:
    text = f.read()
    

#print (text)
sampleRegex = re.compile (r'(/[A-Za-z0-9_/-]*)')
extractedSampleList = sampleRegex.findall(text)

outputFile = "datasets_HH_" + today + ".txt"
with io.open (outputFile, mode ='w') as f:
    for line in extractedSampleList:
        f.write("%s\n" % line)


print ("\nFile with samples '{}' is created.".format ( outputFile) )
