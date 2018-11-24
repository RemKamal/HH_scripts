import numpy as np
import matplotlib.pyplot as plt
import pickle
import ROOT 
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

    mass = 0
    workingmass260, workingmass400, workingmass650, workingmass900 = None, None, None, None

    lims260, lims400, lims650, lims900 = [], [], [], []
    onesigmaDown260, medians260, onesigmaUp260, bdtCuts260 = [], [], [], []
    onesigmaDown400, medians400, onesigmaUp400, bdtCuts400 = [], [], [], [] 
    onesigmaDown650, medians650, onesigmaUp650, bdtCuts650 = [], [], [], []
    onesigmaDown900, medians900, onesigmaUp900, bdtCuts900 = [], [], [], []
    
    for item in itemlist:
        lims, mass, bdtCut = item
    #print mass
        mass = int(mass)
        if mass == 260:
            lims260.append (lims)
            if not workingmass260:
                workingmass260 = mass
                #twosigmaDown.append(float(lims[-5]))
            onesigmaDown260.append(float(lims[-4]))
            medians260.append(float(lims[-3]))
            onesigmaUp260.append(float(lims[-2]))
                #twosigmaUp.append(float(lims[-1]))
            bdtCuts260.append(float(bdtCut))

        elif mass == 400:
            lims400.append (lims)
            if not workingmass400:
                workingmass400 = mass
                #twosigmaDown.append(float(lims[-5]))                           
            onesigmaDown400.append(float(lims[-4]))
            medians400.append(float(lims[-3]))
            onesigmaUp400.append(float(lims[-2]))
                #twosigmaUp.append(float(lims[-1]))                              
            bdtCuts400.append(float(bdtCut))
        elif mass == 650:
            lims650.append (lims)
            if not workingmass650:
                workingmass650 = mass
                #twosigmaDown.append(float(lims[-5]))                           
            onesigmaDown650.append(float(lims[-4]))
            medians650.append(float(lims[-3]))
            onesigmaUp650.append(float(lims[-2]))
                #twosigmaUp.append(float(lims[-1]))                        
            bdtCuts650.append(float(bdtCut))
        elif mass == 900:
            lims900.append (lims)
            if not workingmass900:
                workingmass900 = mass
                #twosigmaDown.append(float(lims[-5]))                           
            onesigmaDown900.append(float(lims[-4]))
            medians900.append(float(lims[-3]))
            onesigmaUp900.append(float(lims[-2]))
                #twosigmaUp.append(float(lims[-1]))                                 
            bdtCuts900.append(float(bdtCut))
        else:
            print 'cant happen'

        # workingmass = mass # to keep the mass of interest, 
        # twosigmaDown.append(float(lims[-5]))
        # onesigmaDown.append(float(lims[-4]))
        # medians.append(float(lims[-3]))
        # onesigmaUp.append(float(lims[-2]))
        # twosigmaUp.append(float(lims[-1]))
        # bdtCuts.append(float(bdtCut))


# print    lims260, lims400, lims650, lims900 
# print    '='*50
# print    onesigmaDown260
# print    medians260
# print    onesigmaUp260
# print    bdtCuts260
# print    '-'*50
# print    workingmass400
# print    onesigmaDown400
# print    medians400
# print    onesigmaUp400
# print    bdtCuts400 
# print    '-'*50
# print    workingmass650
# print    onesigmaDown650
# print    medians650
# print    onesigmaUp650
# print    bdtCuts650 
# print    '-'*50
# print    workingmass900
# print    onesigmaDown900
# print    medians900
# print    onesigmaUp900
# print    bdtCuts900 
# print    '-'*50

for m, sido, me, siup, bdt in [ [workingmass260,onesigmaDown260,medians260,onesigmaUp260,bdtCuts260], [workingmass400,onesigmaDown400,medians400,onesigmaUp400,bdtCuts400], [workingmass650,onesigmaDown650,medians650,onesigmaUp650,bdtCuts650], [workingmass900,onesigmaDown900,medians900,onesigmaUp900,bdtCuts900] ]:
    #print m, sido, me, siup, bdt

        x = np.asarray(bdt)
        y = np.asarray(me)
        #yerr = np.asarray([onesigmaDown, onesigmaUp])
        #yerr = np.asarray()
        yerr_p = np.asarray(siup)
        yerr_m = np.asarray(sido)

        #xerr = np.zeros(len(x))
        xerr_p = np.zeros(len(x))
        xerr_m = np.zeros(len(x))

        c1 = ROOT.TCanvas("c1","Graph with asymmetric error bars",200,10,700,500)
        c1.SetFillColor(0)
        c1.SetGrid()
        c1.GetFrame().SetFillColor(21)
        c1.GetFrame().SetBorderSize(12)
        gr = ROOT.TGraphAsymmErrors(len(x), x, y, xerr_m, xerr_p, yerr_m, yerr_p)

        gr.SetTitle('no BR, Xsec = 1pb, mass = {0}GeV'.format(m))
        gr.GetYaxis().SetTitle("'r' from 'Combine'")

        gr.GetXaxis().SetTitle("Cut on BDT value")

        gr.SetMarkerColor(4)
        gr.SetMarkerStyle(21)
        gr.Draw("AP")
        for ext in ['png', 'pdf', 'root']:
            c1.SaveAs('gr_limits_{0}.{1}'.format(m, ext))






# fig, ax = plt.subplots()
# ax.errorbar(x, y, yerr, fmt='o') #, xerr)
# plt.show()


# plt.savefig('limits_vs_bdt.png')
# plt.savefig('limits_vs_bdt.pdf')


# def PlotDataPoints(config,pars):
#     """Collect the data points/UL and generate a TGraph for the points
#     and a list of TArrow for the UL. All is SED format"""
  
#     #Preparation + declaration of arrays
#     arrows = []
#     NEbin = int(config['Ebin']['NumEnergyBins'])
#     lEmax = np.log10(float(config['energy']['emax']))
#     lEmin = np.log10(float(config['energy']['emin']))
#     Epoint = np.zeros(NEbin)
#     EpointErrp = np.zeros(NEbin)
#     EpointErrm = np.zeros(NEbin)
#     Fluxpoint = np.zeros(NEbin)
#     FluxpointErrp = np.zeros(NEbin)
#     FluxpointErrm = np.zeros(NEbin)
#     ener = np.logspace(lEmin, lEmax, NEbin + 1)
  
#     print "Save Ebin results in ",pars.PlotName+".Ebin.dat"
#     dumpfile = open(pars.PlotName+".Ebin.dat",'w')
#     dumpfile.write("# Energy (MeV)\tEmin (MeV)\tEmax (MeV)\tE**2. dN/dE (erg.cm-2s-1)\tGaussianError\tMinosNegativeError\tMinosPositiveError\n")
  
#     from enrico.constants import EbinPath
#     for i in xrange(NEbin):#Loop over the energy bins
#         E = int(pow(10, (np.log10(ener[i + 1]) + np.log10(ener[i])) / 2))
#         filename = (config['out'] + '/'+EbinPath+str(NEbin)+'/' + config['target']['name'] +
#                     "_" + str(i) + ".conf")
#         try:#read the config file of each data points
#             CurConf = get_config(filename)
#             print "Reading ",filename
#             results = utils.ReadResult(CurConf)
#         except:
#             print "cannot read the Results of energy ", E
#             continue
#         #fill the energy arrays
#         Epoint[i] = E
#         EpointErrm[i] = E - results.get("Emin")
#         EpointErrp[i] = results.get("Emax") - E
#         dprefactor = 0
  
#         #Compute the flux or the UL (in SED format)
#         if results.has_key('Ulvalue'):
#             PrefUl = utils.Prefactor(results.get("Ulvalue"),results.get("Index"),
#                                     results.get("Emin"),results.get("Emax"),E)
#             Fluxpoint[i] = MEV_TO_ERG  * PrefUl * Epoint[i] ** 2
#             arrows.append(ROOT.TArrow(Epoint[i], Fluxpoint[i], Epoint[i],
#                                      Fluxpoint[i] * 0.5, 0.02, "|>"))
#         else : #Not an UL : compute points + errors
#             Fluxpoint[i] = MEV_TO_ERG  * results.get("Prefactor") * Epoint[i] ** 2
#             dprefactor = results.get("dPrefactor")
#             try:
#                 down = abs(results.get("dPrefactor-"))
#                 up = results.get("dPrefactor+")
#                 if down==0 or  up ==0 :
#                   raise RuntimeError("cannot get Error value")
#                 FluxpointErrp[i] = MEV_TO_ERG  * up * Epoint[i] ** 2
#                 FluxpointErrm[i] = MEV_TO_ERG  * down * Epoint[i] ** 2
#             except:
#                 try:
#                     err = MEV_TO_ERG  * dprefactor * Epoint[i] ** 2
#                     FluxpointErrp[i] = err
#                     FluxpointErrm[i] = err
#                 except:
#                     pass
#         print "Energy = ",Epoint[i]
#         print "E**2. dN/dE = ",Fluxpoint[i]," + ",FluxpointErrp[i]," - ",FluxpointErrm[i]
  
#         #Save the data point in a ascii file
#         dumpfile.write(str(Epoint[i])+"\t"+str(results.get("Emin"))+"\t"+str( results.get("Emax"))+"\t"+str(Fluxpoint[i])+"\t"+str( MEV_TO_ERG  * dprefactor * Epoint[i] ** 2)+"\t"+str(FluxpointErrm[i])+"\t"+str(FluxpointErrp[i])+"\n")
#     #create a TGraph for the points
#     tgpoint = ROOT.TGraphAsymmErrors(NEbin, Epoint, Fluxpoint, EpointErrm,
#                                      EpointErrp, FluxpointErrm, FluxpointErrp)
#     tgpoint.SetMarkerStyle(20)
#     dumpfile.close()
#     return tgpoint, arrows






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


