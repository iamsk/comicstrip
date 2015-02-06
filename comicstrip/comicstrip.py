#!/usr/bin/env python
#
# Comicstrip - extract individual frames from a comic book/strip
#
# Copyright 2009 David Koo
#
# This program is free software: you can redistribute it and/or modify it under the terms of
# the GNU Affero General Public License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>.
#

from optparse import OptionParser

from comic import comic

_version = "0.1"


def getargs(parser):
    (options, args) = parser.parse_args()
    kw = {}
    kw["infile"] = options.infile
    if kw["infile"] is None:
        raise ValueError, "Input File Not Specified"
    kw["prefix"] = options.prefix
    kw["firstPg"] = options.firstPg
    kw["firstPgRow"] = options.firstPgRow
    kw["startRow"] = options.startRow
    kw["lignore"] = options.lignore
    kw["rignore"] = options.rignore
    kw["filePat"] = options.filePat
    kw["quiet"] = options.quiet
    kw["gwidth"] = options.gwidth
    kw["fwidth"] = options.fwidth
    kw["fheight"] = options.fheight
    kw["debug"] = options.debug
    kw["fileList"] = args
    return kw


parser = OptionParser(usage="%prog [options] [pgfile1, pgfile2, ...]",
                      version="%%prog %s" % (_version),
                      description="Split a comic page into individual frames")
parser.add_option("-q", "--quiet", action="store_true", dest="quiet",
                  help="Don't print progress messages to stdout [default:%default]")
parser.add_option("-d", "--debug", dest="debug", action="store_true",
                  help="Enable debug prints [default:%default]")
parser.add_option("-f", "--file", dest="infile", type="string", metavar="FILE",
                  help="Name of the input file")

parser.add_option("", "--prefix", dest="prefix",
                  help="Prefix for output files")
parser.add_option("", "--left-ignore", type="int", dest="lignore", metavar="PIXELS",
                  help="How much of the left margin to ignore when detecting rows [default:%default]")
parser.add_option("", "--right-ignore", type="int", dest="rignore", metavar="PIXELS",
                  help="How much of the right margin to ignore when detecting rows [default:%default]")
parser.add_option("", "--firstpage", dest="firstPg", type="string", metavar="PGFILENAME",
                  help="Name of the title page in comic archive file")
parser.add_option("", "--firstpg-row", type="int", dest="firstPgRow", metavar="PIXELS",
                  help="From which line of the first page should the processing start [default:%default]")
parser.add_option("", "--startrow", type="int", dest="startRow", metavar="PIXELS",
                  help="From which line of the each page (other than the first page) should the processing start [default:%default]")
parser.add_option("", "--glob", dest="filePat", metavar="GLOB",
                  help="A glob expression to select files to be processed from the book. (Not required if a file list is provided.)")
parser.add_option("", "--gutter-width", dest="gwidth", metavar="WIDTH",
                  help="Minimum width of the gutter [default:%default]")
parser.add_option("", "--min-width", dest="fwidth", metavar="WIDTH", type="int",
                  help="Minimum width of a frame [default:%default]")
parser.add_option("", "--min-height", dest="fheight", metavar="HEIGHT", type="int",
                  help="Minimum height of a frame [default:%default]")

parser.set_defaults(quiet=False,
                    prefix="cstrip-",
                    lignore=0,
                    rignore=0,
                    firstPgRow=0,
                    startRow=0,
                    gwidth=15,
                    fwidth=100,
                    fheight=100,
                    debug=False)

kw = getargs(parser)
book = comic(**kw)
book.process()
