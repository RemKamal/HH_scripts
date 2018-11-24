from ROOT import TFile
import ROOT

fname = 'mm_SR.input.root'
innerDir = 'mm_SR'
tmpfile  = 'new_mm.root'


def read3():
    shapes_file = ROOT.TFile.Open(fname)
    print 'tfile path is', shapes_file
    print 'list of keys'
    print 'list of Keys is', ROOT.gDirectory.GetListOfKeys().ls()
    print 'gonna cd'
    print shapes_file.cd(innerDir)
    shapes = ROOT.gDirectory.GetListOfKeys()
    hists = []
    print shapes
        # Since the nominal and varied shapes share the same binning,
        # take any of the histograms found in the shapes file.
    for idx, shape in enumerate(shapes):
        shape = ROOT.gDirectory.Get(shapes[idx].GetName())
        print 'before draw'
        shape.Print()
        hists.append (shape)

    if True:
            #inp = ROOT.TFile.Open(inputfile,'read')
        output = ROOT.TFile.Open(tmpfile,'recreate')
        output.mkdir(innerDir)
        output.cd(innerDir)
        for h in hists:
            h.Write()#key.GetName())
        output.Close()
        
        # obj = ROOT.TObject
        # for key in ROOT.gDirectory.GetListOfKeys():
        #         #inp.cd()
        #     obj = key.ReadObj()
        #         #if obj.GetName() == job.tree:
        #         #   continue
        #     output.cd()
        #     obj.Write(key.GetName())
        # outfile.Close()
        # infile.Close()



#ONLY example 3 is working!!!!!!!!!!!!!!!!!
def read1():
    hnames = []
    tfile = TFile.Open(fname)
    for key in tfile.GetListOfKeys():
        h = key.ReadObj()
        if h.ClassName() == 'TH1F' or h.ClassName() == 'TH2F':
            hnames.append(h.GetName())
    print hnames

def read2():
    tfile = TFile.Open(fname)
    tfile.cd("mm_SR")
    for h in tfile.GetListOfKeys():
        h = h.ReadObj()
        print h.ClassName(), h.GetName()



#read1()
#read2()
read3()
