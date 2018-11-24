#!/usr/bin/env python
"""
===================
A simple tree model
===================

This example demonstrates how to define a simple tree model.
"""
print(__doc__)
from rootpy.tree import Tree, TreeModel
from rootpy.tree import IntCol, FloatCol, FloatArrayCol, CharCol, CharArrayCol, IntArrayCol
from rootpy.io import root_open
from random import gauss, choice, sample, randint
from string import ascii_letters
from rootpy.extern.six.moves import range 
from rootpy.plotting import Hist, Hist2D, Hist3D, HistStack, Legend, Canvas

f = root_open("test.root", "recreate")

# define the model
class Event(TreeModel):
    s = CharCol()
    string = CharArrayCol(5)
    x = FloatCol()
    y = FloatCol()
    z = FloatCol()
    f = FloatArrayCol(5)
    num_vals = IntCol()
    # variable-length array
    vals = FloatArrayCol(5, length_name='num_vals')
    
#h_simple = Hist(10, 0, 1, name='my_hist')
h_simple = Hist(11, 1, 12, name='cutFlow', title='Some Data',
                drawstyle='hist',
                legendstyle='F',
                fillstyle='/')

tree = Tree("test", model=Event)

# fill the tree
for i in range(1000):
    tree.s = ord(choice(ascii_letters))
    tree.string = (u''.join(sample(ascii_letters, 4))).encode('ascii')

    tree.x = gauss(.5, 1.)
    if tree.x < 0.5: continue
    h_simple.Fill(1, 1)

    tree.y = gauss(.3, 2.)
    if tree.y < 0.5: continue
    h_simple.Fill(2, 1)

    tree.z = gauss(13., 42.)
    if tree.z < 0.5: continue
    h_simple.Fill(3, 1)

    for j in range(5):
        tree.f[j] = gauss(-2, 5)
    tree.num_vals = i
    for j in range(5):
        tree.vals[j] = j
    if randint(1, 10) < 6: continue
    h_simple.Fill(4, 1)

    if randint(1, 10) < 8: continue
    h_simple.Fill(5, 1)

    tree.fill()

#for key in histos: histos[key].Write()
h_simple.Write()
tree.write()
tree.vals.reset()

# print tree contents in CSV format
tree.csv()

f.close()
