import zipfile
import fnmatch

from page import page


class comic(object):
    """A comic book - a cbz or a cbr file"""

    PROCESS_BOOK = 0
    PROCESS_PAGE = 1

    keys = ["infile", "prefix", "firstPg", "firstPgRow", "startRow", "lignore", "rignore",
            "filePat", "fileList", "quiet", "gwidth", "debug", "fwidth", "fheight"]
    pgkeys = ["startRow", "lignore", "rignore", "infile", "quiet", "debug", "fwidth", "fheight"]

    def __init__(self, **kw):
        """Initialize a comic book (cbz) file.
        Permitted arguments
        infile:
            Name of the comic book to process. Only cbz files are supported at the moment.
        prefix:
            Output file prefix. Each output fill will be of the form prefixNNN
        firstPg:
            The name of the first page to start analyzing from.
        firstPgRow:
            The first page might start with a title first. We need to skip over this to
            get to the actual rows
        lignore, rignore:
            Sometimes scanned pages are not at the edges. lignore, rignore tell us
            how many left/right columns to ignore when searching for rows
        filePat:
            File names in the archive that match this pattern will be processed. The pattern is
            a glob expression. If both fileList and filePat are specified, fileList is used, if
            neither are specified then the file pattern "*.jpg" is used.
        fileList:
            File names in the archive that are in this list will be processed. If both fileList
            and filePat are specified, fileList is used, if neither are specified then the file
            pattern "*.jpg" is used.
        gwidth:
            Minimum width (and height) of the gutter.
        fwidth, fheight:
            Minimum width (height resp) of a frame.
        quiet:
            Don't print any progress messages.
        debug:
            Enable debug prints"""
        object.__init__(self)
        [self.__setattr__(k, kw[k]) for k in comic.keys]
        self.counter = 0 # used when writing output
        try:
            self.zfile = zipfile.ZipFile(kw["infile"])
        except:
            # is probably a single page image instead of a comic book
            self.actionType = comic.PROCESS_PAGE
        else:
            self.actionType = comic.PROCESS_BOOK

    def processBook(self):
        if len(self.fileList) == 0:
            self.fileList = fnmatch.filter(self.zfile.namelist(), self.filePat)
            self.fileList.remove(self.firstPg)
        kw = dict([(k, object.__getattribute__(self, k)) for k in comic.pgkeys])
        kw["pgNum"] = 1
        kw["contents"] = True
        if self.firstPg:
            # process the start page separately
            buf = self.zfile.read(self.firstPg)
            kw["startRow"] = self.firstPgRow
            kw["infile"] = buf
            pg = page(**kw)
            self.counter = pg.save(self.prefix, self.counter)
            kw["pgNum"] += 1

        # for other pages, startRow = startRow
        kw["startRow"] = self.startRow
        for fname in self.fileList:
            buf = self.zfile.read(fname)
            kw["infile"] = buf
            pg = page(**kw)
            self.counter = pg.save(self.prefix, self.counter)
            kw["pgNum"] += 1

    def processPg(self):
        kw = dict([(k, object.__getattribute__(self, k)) for k in comic.pgkeys])
        kw["pgNum"] = 1
        kw["contents"] = False
        page(**kw).save(self.prefix, self.counter)

    def process(self):
        if self.actionType == comic.PROCESS_BOOK:
            self.processBook()
        else:
            self.processPg()
        print
