import collections

totFactorsList = wFactorsList = [500, 750, 1000, 2500, 5000, 7500,
                25000, 50000, 200000, 250000]

zFactorsList = [ x*20. for x in wFactorsList ]


massXsecDict = {260: 3.3956,
                270: 2.783,
                300: 1.7849,
                350: 0.82315,
                400: 0.48266,
                450: 0.25302,
                600: 0.07351,
                650: 0.04503,
                900: 0.0098,
                1000: 0.0057}

massXsecDict = collections.OrderedDict(sorted(massXsecDict.items(), key=lambda x: x[0]  ) )


# 2*Htobb * [ HtoWW * ( Wtoe_nu + Wtom_nu + Wtotau_nu)^2 + HtoZZ * 2* (Ztoee + Ztomm + Ztotautau) * ZtoInv ] 
br_HH_bbVV_2b2l2nu = 2* 0.5824 * (0.2154*(0.1086+0.1086+0.1086)*(0.1086+0.1086+0.1086) + 0.02643 *2* ( 0.03363+0.03366+0.03366 )*0.2) #= 0.02787 for 3 flavours 
br_HH_bbWW_2b2l2nu = 2* 0.5824 * (0.2154*(0.1086+0.1086+0.1086)*(0.1086+0.1086+0.1086)) # 0.0266 for 3 flavours
br_HH_bbZZ_2b2l2nu = 2* 0.5824 * ( 0.02643 *2* ( 0.03363+0.03366+0.03366 )*0.2) # 0.0012 for 3 flavours
space = '    '
count = 0
print 'mass     xsec      zFactor/ {w,tot}factor    xsec*zzBR         xsec*wwBR        xsec*totBR'
for massPoint, xsec in massXsecDict.items():

    print massPoint, space, xsec, space, zFactorsList[count], '/', wFactorsList[count], space, xsec*br_HH_bbZZ_2b2l2nu*zFactorsList[count], space, xsec*br_HH_bbWW_2b2l2nu*wFactorsList[count], space, xsec*br_HH_bbVV_2b2l2nu*totFactorsList[count] 
    #print 'count is ', count
    count += 1
    
