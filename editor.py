#!/usr/bin/python
#python
import sys
import getopt
import re


def main(argv):
    inputfile = ''
    inputfile, outputfile = getargs(argv)   # handles parsing parameters

    #try:
        #input = open(inputfile, 'r+')
    #except (FileNotFoundError):
        #print("Could not find input file.")

    try:
        processfile(inputfile, outputfile)
        #input.close()
    except UnboundLocalError:
        print('No file specified.')


def processfile(file, outfile):
    matches = []

    out = open(outfile, 'w+')
    with open(file) as infile:
        for line in infile.readlines():
            matches = processline(line, file, matches)

    for string in matches:
        out.write(string)

    out.close()
    infile.close()


def processline(line, file, matches):    # processes line and returns lines to insert

    fields = re.split(r'\t+', line)
    search(line, file, fields, matches)     # search for desired fieds

    return matches


def search(currentline, file, fields, matches):
    strings =[fields[1], fields[2]]                     # list of strings to match
    with open(file) as infile:
        for line in infile.readlines():
            hasMatch = any(string in line for string in strings)
            if hasMatch and (line not in matches):
                print(line)
                matches.append(line)
            elif line != currentline:
                if test(fields):
                    matches.append(line)


def test(fields):
    #if(fields[0] != H):  #checks that the line is a detail
    return True
    #else:
    #    return False


def getargs(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('editor.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('editor.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    return inputfile, outputfile

if __name__ == "__main__":
   main(sys.argv[1:])


