#! /usr/bin/python

from sys import argv
import zlib
import os

USAGE = "usage: ./FancyName.py file_to_rename"


class PlanetaryNameGenerator:
    """Class that generates names like those of names of planets"""
    prefixes = ["alpha", "beta",  "gamma",   "delta", "epsilon", "zeta",
                "eta",   "theta", "iota",    "kappa", "lambda",  "omicron",
                "sigma", "tau",   "upsilon", "phi",   "chi",     "psi",
                "omega"]  # 19 prefixes
    endings = ["a", "ae", "us", "ii", "um", "a"]  # 6 endings
    digraphs = [
            "la",  "ve",  "ta",  "re",  "or",  "za",  "us",  "ac"
            "te",  "ce",  "at",  "a",   "e",   "o",   "le",  "fa",
            "he",  "na",  "ar",  "to",  "oi",  "ne",  "no",  "ba",
            "bo",  "ha",  "ve",  "va",  "ax",  "is",  "or",  "in",
            "mo",  "on",  "cra", "ud",  "sa",  "tu",  "ju",  "pi",
            "mi",  "gu",  "it",  "ob",  "os",  "ut",  "ne",  "as",
            "en",  "ky",  "tha", "um",  "ka",  "qt",  "zi",  "ou",
            "ga",  "dro", "dre", "pha", "phi", "sha", "she", "fo",
            "cre", "tri", "ro",  "sta", "stu", "de",  "gi",  "pe",
            "the", "thi", "thy", "lo",  "ol",  "clu", "cla", "dze",
            "di",  "so",  "ti",  "es",  "ed",  "bi",  "po",  "ni",
            "ex",  "ad",  "un",  "pho", "ci",  "ge",  "se",  "co"
        ]  # should be 96 of them
    midvowels = ["", "kk", "ll", "xx", "rr"]
    #midconsonnants = "yr" # we will just pass it whenever we encounter doubling of any kind of consonnant

    def __init__(self, filename=None):
        self.randomName = ''
        if not (filename is None):
            self.fileCRC = crc(filename)  # No error catching yet
            self.randomName = self.ConstructNameFromCRC()

    def __call__(self, filename=None):
        if not (filename is None):
            self.fileCRC = crc(filename)  # No error catching yet
            self.randomName = self.ConstructNameFromCRC()
        return self.randomName

    def ConstructNameFromCRC(self):
        bar = self.fileCRC
        prefix = ''

        # Append prefix
        bar, pos = divmod(bar, len(self.prefixes))
        prefix += self.prefixes[pos]

        # Choose ending
        bar, pos = divmod(bar, len(self.endings))
        if (pos == 0 and bar == 0):
            ending = "vanitate"  # because it is really exceptional case
        else:
            ending = self.endings[pos]

        # Construct main word
        nameFiller = ''
        while not (bar == 0 and pos == 0):
            bar, pos = divmod(bar, len(self.digraphs))
            # Place fillers between double letters
            if self.digraphs[pos][:1] == nameFiller[-1:]:
                if nameFiller[:-1] not in ('a', 'e', 'i', 'o', 'u', 'y'):
                    nameFiller += 'yr'
            if self.digraphs[pos][:1] in ('a', 'e', 'i', 'o', 'u', 'y') and nameFiller[-1:] in ('a', 'e', 'i', 'o', 'u', 'y'):
                nameFiller += self.midvowels[pos % len(self.midvowels)]
            nameFiller += self.digraphs[pos]

        #Compose all together
        return '_'.join([prefix, nameFiller+ending])

#Independent function to calculate
def crc(filename):
    prev = 0
    for eachLine in open(filename, "rb"):
        prev = zlib.crc32(eachLine, prev)
    return prev & 0xFFFFFFFFL  # "%X" % (prev & 0xFFFFFFFF) #In case you need traditional CRC, this is how it is returned

if __name__ == '__main__':
    if len(argv) > 1:
        fname = os.path.normpath(argv[1])
        #Try renaming the file to fancyName
        if os.path.isfile(fname):
            giveMeNewFancyName = PlanetaryNameGenerator()
            fancyName = giveMeNewFancyName(fname)

            oldname = os.path.basename(fname)  # contains extension
            oldname = os.path.splitext(oldname)[0]  # no extension

            print "Renaming %s to %s:" % (oldname, fancyName)
            os.rename(fname, fname.replace(oldname, fancyName))
        elif os.path.isdir(fname):
            confirmation = raw_input("Are you sure you want to mass rename files in folder '%s'?\r\n> " % fname)
            if confirmation.lower() in ('yes', 'y', 'affirmative', 'gogogo'):
                genFancyName = PlanetaryNameGenerator()
                for filename in os.listdir(fname):
                    filename = os.path.join(fname, filename)
                    if os.path.isfile(filename):
                        oldname = os.path.splitext(os.path.basename(filename))[0]  # no extension
                        fancyName = genFancyName(filename)
                        print "Renaming %s to %s" % (oldname, fancyName)
                        os.rename(filename, filename.replace(oldname, fancyName))
    else:
        print USAGE