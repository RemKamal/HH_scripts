#!/usr/bin/python

import sys, getopt


def convert(inputfile, outputfile):
    print 'inside convert'
    contents = open(inputfile,"r")
    with open(outputfile, "w") as e:
        for idx, lines in enumerate(contents.readlines()):
            lines = [x for x in lines.split(' ') if x]

            #if 'r' == lines[0]:
             #   lines.insert(3, '+/-')
            #if len(lines) <4: continue    
            #if 'Floating' in lines:
            # f.write(text.replace(search_word, '<span style="color: red">{}</span>'.format(search_word)))
#            if 'Floating' in lines:
 #               lines.insert(0, '<b>')
  #              lines[-1] = 'GblCorr.'
   #             lines += ['</b>\n']
            #lines[0] = '<b><span style="color: red">{}</span>/<b>'.format(lines[0].ljust(30)   )
            #for idx, word in enumerate(lines):
             #   if idx ==0: continue
              #  word = word.ljust(10)
            
            if len(lines) <3 or '--' in lines[0]: continue
            if 'Floating' in lines:
                lines = '\nFloating Parameter'.ljust (30) + 'InitialValue'.ljust(16) + '       FinalValue'.ljust(33)  #+ '\n'
                lines = '<b><span style="color: red">{}</span></b>'.format(lines)
            else:
                if lines[1].startswith('-'):
                    pass
                else:
                    lines[1] = '+' + lines[1]

                if lines[2].startswith('-'):
                    pass
                else:
                    lines[2] = '+' + lines[2]

                
                if 'r' == lines[0]:
                    continue
                    #lines = '<b>{}</b>'.format(lines[0].ljust(29)) + lines[1].ljust(16) + (lines[2] + ' ' + lines[3]).ljust(33)
                else:
                    lines = '<b>{}</b>'.format(lines[0].ljust(29)) + lines[1].ljust(16)+ (lines[2] + ' ' + lines[3] + ' ' + lines[4]).ljust(33)

            lines = '<font size="4">{}</font>'.format(lines)
            lines += '\n' + '-'*31 + '     ' + '-'*14 + '     ' + '-'*30
            print lines


            e.write("<pre>" + lines + "</pre>\n")
            #if lines == 
            continue
            lines = [x.ljust(15) for x in lines]
            lines[0] = lines[0].ljust(20)
            lines = lines[0] + lines[1] + lines[2] + lines[2:4] + lines[4:]
            newstr = ''.join(lines)
            
            print newstr
            if idx ==5: sys.exit(1)
            #lines = ''.join(lines)
            #lines = [x for x in ] ''.join(lines)

            e.write("<pre>" + newstr + "</pre> <br>\n")
            continue
            #sys.exit(1)


            for word in lines:
                word.replace('_', '\_')
            lines = ''.join(lines)
            print lines
            e.write("<pre>" + lines + "</pre> <br>\n")


def main(argv):
    #https://www.tutorialspoint.com/python/python_command_line_arguments.htm
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
        #The second argument is the option definition string for single character options. If one of the options requires an argument, its letter is followed by a colon.
        # it essentially says: h,i:,o:
    except getopt.GetoptError:
        print 'txt2html.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'txt2html.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    print 'Input file is "', inputfile
    print 'Output file is "', outputfile
    convert(inputfile, outputfile)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))


