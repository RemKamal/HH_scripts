import sys, getopt
import glob
from pprint import pprint as pp
from ROOT import TFile

skipList = []


def verifyTrees(trees):
    print "="*50
    print 'len(trees)', len(trees)
    for fil in sorted(trees):
        f = TFile(fil)
        if f.IsZombie() or not f.IsOpen() or f.GetNkeys()==0 :
            skipList.append(fil)
            continue
        tree = f.Get("tree")
        print 
        print 'fil', fil
        print 'tree.GetEntries()', tree.GetEntries()
        print
        try:
            cutFlowHist = f.Get("cutFlow")
        except:
            skipList.append(fil)
            continue
        if cutFlowHist == None:
            skipList.append(fil)
            continue

def checkMinitrees(inDir):
    if inDir == None:
        return
    if inDir[-1] == '/':
        inDir = inDir[:-1]
    trees = glob.glob(inDir + '/*root')
    print 'trees:'
    pp(trees)
    if trees == []:
        print 'check trees, exiting....'
        sys.exit(1)
    verifyTrees(trees)



def main(argv):
   inDir = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["inputDir=","ofile="])
   except getopt.GetoptError:
      print 'test.py -i <inDir> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <inDir> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--inputDir"):
         inDir = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   print 'Input file is "', inDir
   if outputfile:
       print 'Output file is "', outputfile
   
   if inDir == "":
       print 'check inDir, exiting....'
       sys.exit(1)
   checkMinitrees(inDir)

if __name__ == "__main__":
    main(sys.argv[1:])
    print 'skipList:'
    pp(sorted(skipList))
