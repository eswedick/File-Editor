#!/usr/bin/python

import sys
import getopt
import re


def main(argv):
    inputfile, outputfile = getargs(argv)   # handles parsing parameters

    try:
        processfile(inputfile, outputfile)
    except UnboundLocalError:
        print('No file specified.')


def processfile(file, outfile):
    matches = []

    out = open(outfile, 'w+')
    with open(file) as infile:
        for line in infile.readlines():
            matches = processline(line, file, matches)

    for string in matches:
        if string is not None:
            out.write(string)

    out.close()
    infile.close()


def processline(line, file, matches):    # processes line and returns lines to insert

    fields = re.split(r'\t+', line)
    search(line, file, fields, matches)     # search for desired fieds

    return matches


def search(currentline, file, fields, matches):
    strings = [fields[1]]                     # list of strings to match

    if test(fields):
        if getnext(currentline, file) not in matches:   # if detail has not been added
            matches.append(currentline)                 # add header
            matches.append(getnext(currentline, file))  # add detail

        with open(file) as infile:                      # find any details matching therapist
            for line in infile.readlines():
                newline = re.split(r'\t+', line)
                if test(newline[0]):
                    hasMatch = any(string in newline for string in strings)
                    if hasMatch and (getnext(line, file) not in matches):
                        print(line)
                        matches.append(getnext(line, file))  #append other details


def getnext(searchline, file):
    found = False
    with open(file) as infile:
        for line in infile.readlines():
            if searchline == line:
                found = True
            else:
                if found:
                    return line     # return detail
                    break


def test(fields):
    if fields[0] == 'H':  # checks line type
        return True
    else:
        return False


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


