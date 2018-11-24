#!/usr/bin/env python
"""
======================================
Copy a tree while overwriting branches
======================================

This is an example showing how to copy a tree while overwriting one or more of
its branches with new values.
"""

from rootpy.tree import Tree, TreeModel, FloatCol, IntCol
from rootpy.io import root_open
from ROOT import TMVA
import sys
args_are_given = len(sys.argv) > 1
#print sys.argv[0] # script name itself                                                                                                                          
#print sys.argv[1] # 1st passed argument, file with samples
#print sys.argv[2] # 2nd passed argument, comma separated list of xml trainings

if args_are_given:
    dirWithSamples = sys.argv[1] 
    print '"dirWithSamples" in a wrong format'
    
    list_of_diff_mvas = list() if len(sys.argv) < 2 else [str(x) if 'xml' in x else None for x in sys.argv[2].split(',')]
    if None in list_of_diff_mvas:
        print '"mvaXml" files should be xml format, please check.' 
        sys.exit(1)
    print 'list_of_diff_mvas is ', list_of_diff_mvas
else:
    print '"dirWithSamples" or "mvaXml" files are not specified, please follow the syntax W/O spaces for XMLs: python fillMvaBranchOfTrees.py "dirWithSamples" "mvaXml1,mvaXml2,mvaXml3"'
    sys.exit(1)


print 'all is fine'



TMVA.Tools.Instance()
reader = TMVA.Reader( "!Color:!Silent" )
for mva in list_of_diff_mvas:
    reader.BookMVA( mav[-15:-11] if mva[-15:-11] == 'BDT' else None, mva )


h1 = ROOT.TH1D("h1","Classifier Output on Background Events",100,-1.0,1.0)
h2 = ROOT.TH1D("h2","Classifier Output on Signal Events",100,-1.0,1.0)

samplesList = []
for root, dirs, files in os.walk(dirWithSamples):
    for name in files:
        if 'tree.root' in name:
            samplesList.append (name)



for sample in samplesList:
    if sample:
        # first open the file and load tree
        f = root_open(sample, "read")
        tree = Tree("tree") #, model=Event)
        
        """
        This section below takes the input tree and copies it while overwriting a
        branch with new values.
        """

        # Now we want to copy the tree above into a new file while overwriting a branch
        # First create a new file to save the new tree in:
        f_copy = root_open(sample[:-5] + "_withMva.root", "recreate")
        
        # You may not know the entire model of the original tree but only the branches
        # you intend to overwrite, so I am not specifying the model=Event below as an
        # example of how to deal with this in general:
        tree_copy = Tree("tree")
        
        # Here we specify the buffer for the new tree to use. We use the same buffer as
        # the original tree. This creates all the same branches in the new tree but
        # their addresses point to the same memory used by the original tree.
        tree_copy.set_buffer(tree._buffer, create_branches=True)

        # Now loop over the original tree and fill the new tree
        for entry in tree:
            # Overwrite a branch value. This changes the value that will be written to
            # the new tree but leaves the value unchanged in the original tree on disk.
            entry.bdtOutput = reader.EvaluateMVA("BDT")
            entry.bdtOutput_multiclass = reader.EvaluateMVA("BDTG")
            entry.dnnOutput = reader.EvaluateMVA("DNN")
            # "entry" is actually the buffer, which is shared between both trees.
            tree_copy.Fill()

    
        # tree_copy is now a copy of tree where the "mva" branches have been overwritten with new values
        tree_copy.Write()
        f_copy.Close()
        f.Close()
