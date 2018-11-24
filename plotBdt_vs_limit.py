import numpy as np
import matplotlib.pyplot as plt
import pickle

import pprint
pp = pprint.PrettyPrinter(indent=4)
pp = pprint.PrettyPrinter(depth=6)



with open ('limits.txt', 'rb') as fp:
    itemlist = pickle.load(fp)


twosigmaDown = []
onesigmaDown = []
medians = []
onesigmaUp = []
twosigmaUp = []
bdtCuts = []

if itemlist:
    print 'itemlist is :'
    pp.pprint(itemlist)
    #print itemlist
    print 'len(itemlist) is', len(itemlist)
    for item in itemlist:
        lims, mass, bdtCut = item
        twosigmaDown.append(float(lims[-5]))
        onesigmaDown.append(float(lims[-4]))
        medians.append(float(lims[-3]))
        onesigmaUp.append(float(lims[-2]))
        twosigmaUp.append(float(lims[-1]))
        bdtCuts.append(float(bdtCut))


print bdtCuts

# example data
x = np.asarray(bdtCuts)
y = np.asarray(medians)
yerr = np.asarray([onesigmaDown, onesigmaUp])
#yerr = np.asarray()

#asymmetric_error = [lower_error, upper_error]

fig, ax = plt.subplots()
ax.errorbar(x, y, yerr, fmt='o') #, xerr)
plt.show()


plt.savefig('limits_vs_bdt.png')
plt.savefig('limits_vs_bdt.pdf')

# # Create some fake data
# xvalue = np.linspace(1,100,100)
# pop_mean = xvalue
# walker_pos = pop_mean + 10*np.random.randn(100)

# # Do the plot
# fig, ax = plt.subplots()

# # Save the output of 'plot', as we need it later
# lwalker, = ax.plot(xvalue, walker_pos, 'b-')

# # Save output of 'fill_between' (note there's no comma here)
# lsigma = ax.fill_between(xvalue, pop_mean+10, pop_mean-10, color='yellow', alpha=0.5)

# # Save the output of 'plot', as we need it later
# lmean, = ax.plot(xvalue, pop_mean, 'k--')

# # Create the legend, combining the yellow rectangle for the 
# # uncertainty and the 'mean line'  as a single item
# ax.legend([lwalker, (lsigma, lmean)], ["Walker position", "Mean + 1sigma range"], loc=2)

# fig.savefig("legend_example.png")
# plt.show()


