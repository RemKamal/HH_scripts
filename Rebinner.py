from ROOT import TFile, TH1F
import sys
import itertools

inputFile = "hhMt_ee_SR.input.root"

channel = 'ee' if 'ee' in inputFile else 'mm' if 'mm' in inputFile else None
if channel == None:
    print 'please check inputFile, exiting...'
    sys.exit(1)

tolerance = 0.3

class Rebinner(object):
    tolerance = 0.3
    def __init__(self, DY, TT, data, bins):
        """
        :type bins: an array of low bin edges
        """
        self.DY = DY
        self.TT = TT
        self.data = data
        self.bins = bins
 



fIn = TFile.Open(inputFile)
print 'fIn.ls()', fIn.ls()
fIn.cd('{}_SR'.format(channel))
print 'fIn.ls()', fIn.ls()

DYshape = fIn.Get('{}_SR/DY'.format(channel))
TTshape = fIn.Get('{}_SR/TT'.format(channel))
Datashape = fIn.Get('{}_SR/data_obs'.format(channel))


for hist in [DYshape, TTshape, Datashape]:
    hist.Print("all")
    #for idx, bin in hist:

buildData , buildDY, buildTT = 0, 0, 0

binUpperEdge = [Datashape.GetBinLowEdge(1)] 
nbins=Datashape.GetNbinsX()
for idx, (dy, tt, data) in enumerate(itertools.izip(DYshape, TTshape, Datashape), start =1):


    #print '{idx}, {dy}, {tt}, {data}'.format_map(vars())
    #startBuildingBins = True
    lowEdge = Datashape.GetBinLowEdge(idx)
    print '{idx}, {dy}, {tt}, {data}, {lowEdge}'.format(**locals()) # expansion of variables returned by locals()
    if True:#startBuildingBins:
        buildData += data
        buildDY += dy
        buildTT += tt

    ratio = 1.0*buildData/(buildDY + buildTT) if (buildDY + buildTT) !=0 else 0
    
    if abs(ratio - 1) < tolerance:
        print 'ratio is', ratio
        print 'idx', idx
        buildData , buildDY, buildTT = 0, 0, 0
        binUpperEdge.append(Datashape.GetBinCenter(idx) + Datashape.GetXaxis().GetBinWidth(idx)/2)
    else:
        continue
        #xbins_list = [shape.GetBinLowEdge(1)]
        #xbins_list += [600, 800, 1000, shape.GetBinCenter(nbins) + shape.GetXaxis().GetBinWidth(nbins)/2]
if binUpperEdge[-1] != Datashape.GetBinCenter(nbins+1) + Datashape.GetXaxis().GetBinWidth(nbins+1)/2:
    binUpperEdge.append( Datashape.GetBinCenter(nbins+1) + Datashape.GetXaxis().GetBinWidth(nbins+1)/2)

print 'binUpperEdge', binUpperEdge 
print 'done'
