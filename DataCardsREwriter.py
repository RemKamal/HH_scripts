import pprint

fin = "ee_350_noSignal_dataCard_CRTT_hhMt.txt"
outfileName = "test.txt"
data = None
with open (fin) as f:
    data = f.readlines()

pprint.pprint( data )
print
print

nChannelsToRemove = 2


import re
def modify_line(lineIn, idxs):
    for idx in idxs:
        if idx >= len(lineIn):
            continue
        rem_obj = lineIn.pop(idx)
    #print(line)
        lineIn.insert(idx, '-' + ' '* (len(rem_obj) - 1))
    return lineIn


def modify_line2(lineIn, idxs):
    line_to_return = []
    for idx, obj in enumerate(lineIn):
        if idx in idxs:
            print 'skipping idx=', idx, ' obj=', obj
            continue
        else:
            line_to_return.append(obj)
    return line_to_return
        
data_out = []
for indx, l in enumerate(data, start=1):
    print (indx, l)
    line = re.split(r'(\s+)', l) 
    #line = l.split()
    #print(line)
    if 0:#'QCD' in l:
        #print(line)
        line_mod = modify_line(line, [3,4,5])
        #print(line_mod)

        for c in l.split():
            pass #print (c)
    if 0:#'lumi' in l:
        #line = l.split()
        #print(line)
        rem_obj = line.pop(3)
        #print(line)
        line.insert(3, '-' + ' '* (len(rem_obj) - 1))
        line_mod = modify_line(line, [0])
        #print(line_mod)
        #print(line)
        #for c in l.split():
            #print (c)
    line_mod = line

    #print line
    if 'jmax' in line:
        nChan = line[2]
        line[2] = str( int(nChan) - nChannelsToRemove )
    print line_mod

    if ('bin' in l and len(line) > 6) or ('process' in l and "#" not in l) or ('rate' in l and 'norm' not in l):
        print
        print line, ' len(line)=', len(line)#, ' len(l)=', len(l)
        line_mod = modify_line2(line, [2, 3, 4, 5])
        print line_mod, ' len(line_mod)=', len(line_mod)
        print 

    elif ('lumi' in l or 'CMS' in l or 'pdf' in l or 'QCD' in l or 'xsec' in l):
        print
        print line, ' len(line)=', len(line)#, ' len(l)=', len(l)
        line_mod = modify_line2(line, [4, 5, 6, 7])
        print line_mod, ' len(line_mod)=', len(line_mod)
        print 
    else:
        pass

    print line_mod
#data_2 = list(open(fin))

    data_out.append(''.join(line_mod))

outfile = open(outfileName, 'w')    
#outfile.write("\n".join(data_out))
for item in data_out:
    #print item
    if item :#!= '\n':
        outfile.write("%s" % item)

print
print
pprint.pprint(data_out)
