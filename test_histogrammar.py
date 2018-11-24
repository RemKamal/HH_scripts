import time
import ROOT
tcanvas = ROOT.TCanvas("TCanvasName", "TCanvasTitle", 800, 300)



sigInputFile = ROOT.TFile("BulkGraviton_M900_Hzz_minitree.root")


from histogrammar import *

histogram = Bin(100, 0, 1000, lambda x: x)    # I'll explain this "lambda x: x" in a moment

startTime = time.time()
for event in sigInputFile.tree:
    if event.hhmt > 100:
        histogram.fill(event.hhmt)
endTime = time.time()

print "This took", endTime - startTime, "seconds."
