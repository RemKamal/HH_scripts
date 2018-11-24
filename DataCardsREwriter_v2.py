import pprint
import re
import sys, getopt

nChannelsToRemove = 2


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


def processFile(fin, outfileName):
    data = None
    with open(fin) as f:
        data = f.readlines()

    pprint.pprint(data)
    print


    data_out = []
    for indx, l in enumerate(data, start=1):
        print(indx, l)


        if 'DY_norm rateParam' in l:
            l = 'DY_DataDrivenSF rateParam' + l.split('rateParam')[-1]

        if 'TT_norm rateParam' in l:
            l ='TT_DataDrivenSF rateParam' + l.split('rateParam')[-1]


        if 'lumi_13TeV' in l:
            l = 'lumi_13TeV                               lnN   1.026               1.026               -                   -                   1.026               1.026               1.026               \n'


        if 'QCDscale_VH' in l:
            l = 'QCDscale_VH                              lnN   -                   -                   -                   -                   -                   -                   0.969/1.038         \n'

        if 'QCDscale_TT' in l or 'QCDscale_ttbar' in l:
            l = 'QCDscale_ttbar                           lnN   -                   -                   -                   -                   0.947/1.054         -                   -                   \n'
        if 'QCDscale_ST' in l:
            continue
        if 'QCDscale_VV' in l:
            l = 'QCDscale_VV                              lnN   -                   -                   -                   -                   -                   0.938/1.067         -                   \n'
            
        if 'QCDscale_DY' in l:
           #l = 'QCDscale_DY                              lnN   -                   -                   -                   0.996/1.006         -                   -                   -                   \n'
            l = 'QCDscale_DY                              lnN   -                   -                   -                   -                   -                   -                   -                   \n'


        if 'QCDscale_Higgs_HH' in l:
            l = 'QCDscale_ggHH                            lnN   0.94/1.04           0.94/1.04           -                   -                   -                   -                   -                   \n'
          
        if 'CMS_pu' in l:
            l = 'CMS_pu                                   lnN   1.06                1.06                -                   -                   1.06                1.06                1.06                \n'

            

        if 'pdf_qqbar' in l:
            l = 'pdf_qqbar                                lnN   -                   -                   -                   -                   1.01                1.01                1.023               \n'
            
        if 'pdf_gg' in l:
            l = 'pdf_gg                                   lnN   1.18                1.18                -                   -                   -                   -                   -                   \n'

        if indx == 39 and l == '\n':
            l = 'CMS_eff_met_UnclusteredEn                lnN   1.03                1.03                -                   -                   1.03                1.03                1.03                \n'

        if 'eff_met_' in l and 'shape' in l:
            continue

        if 'xsec' in l:
            continue


        line = re.split(r'(\s+)', l)
        line_mod = line


        # line = l.split()
        # print(line)
        if 0:  # 'QCD' in l:
            # print(line)
            line_mod = modify_line(line, [3, 4, 5])
            # print(line_mod)

            for c in l.split():
                pass  # print (c)
        if 0:  # 'lumi' in l:
            # line = l.split()
            # print(line)
            rem_obj = line.pop(3)
            # print(line)
            line.insert(3, '-' + ' ' * (len(rem_obj) - 1))
            line_mod = modify_line(line, [0])
            # print(line_mod)
            # print(line)
            # for c in l.split():
            # print (c)


        print line_mod
        # print line
        # if 'jmax' in line:
        #     nChan = line[2]
        #     line[2] = str(int(nChan) - nChannelsToRemove)
        # print line_mod

        # if ('bin' in l and len(line) > 6) or ('process' in l and "#" not in l) or ('rate' in l and 'norm' not in l):
        #     print
        #     print line, ' len(line)=', len(line)  # , ' len(l)=', len(l)
        #     line_mod = modify_line2(line, [2, 3, 4, 5])
        #     print line_mod, ' len(line_mod)=', len(line_mod)
        #     print

        # elif ('lumi' in l or 'CMS' in l or 'pdf' in l or 'QCD' in l or 'xsec' in l):
        #     print
        #     print line, ' len(line)=', len(line)  # , ' len(l)=', len(l)
        #     line_mod = modify_line2(line, [4, 5, 6, 7])
        #     print line_mod, ' len(line_mod)=', len(line_mod)
        #     print
        # else:
        #     pass

        # print line_mod
        # # data_2 = list(open(fin))

        data_out.append(''.join(line_mod))


    outfile = open(outfileName, 'w')
    # outfile.write("\n".join(data_out))
    for item in data_out:
        # print item
        if item:  # != '\n':
            outfile.write("%s" % item)
    print
    print
    pprint.pprint(data_out)


#https://www.tutorialspoint.com/python/python_command_line_arguments.htm
def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'test.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   print 'Input file is ', inputfile
   print 'Output file is ', outputfile
   processFile(inputfile, outputfile)


if __name__ == "__main__":
   main(sys.argv[1:])















