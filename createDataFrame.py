import io, sys
import pprint
pp = pprint.PrettyPrinter(indent=4)
from collections import OrderedDict
import json
import pandas as pd

args_are_given = len(sys.argv) > 1
#print sys.argv[0] # script name itself                                                                    
#print sys.argv[1] # 1st passed argument, comma separated list of logs                             

if args_are_given:
    list_of_diff_ranks = list() if len(sys.argv) < 2 else [str(x) if 'txt' in x else None for x in sys.argv[1].split(',')]
    if None in list_of_diff_ranks:
        print '"logTxt" files should be txt format, please check.'
        sys.exit(1)
else:
    print '"logTxt" files are not specified.'
    sys.exit(1)


for fil in list_of_diff_ranks:
    mylist = []
    with io.open(fil, "rt") as f:
        for lis in f:
            mylist.append (lis)

    mydict = OrderedDict()

#pp.pprint(mylist)
# for l in mylist:
#     newl = l.split(':')
#     print 'length of is '
#     print len(newl)
#     print newl[0]
#     print newl[1]
    
    for index,l in enumerate(mylist):
        newl = l.split(':')
        if index == 1:
            pass
        else:
            mydict[newl[1]] = [newl[2], newl[3].split('\n')[0]]


    msg1 = (
        'import pandas as pd{sep}'
        'df = pd.DataFrame({sep}'
        ).format(sep="\n")
    msg2 = (
        '){sep}'
        'md = df.T{sep}'
        'md.columns = ["Rank", "Importance"]{sep}'
        'md.iloc[:{lines}]{sep}').format(sep="\n", lines=len(mydict)-1)

    print 'len(mydict) is ', len(mydict)
    print '='*50
    print '#for file:', fil    
    print(msg1)
    print(json.dumps(mydict))#, indent=2))#4
    print(msg2)
    print 
#take output to jupyter and place in variable mydict:
#mydict = 
#df = pd.DataFrame(mydict)
#md = df.T
#md.columns = ['Rank', 'Importance']
#md.iloc[:14]


