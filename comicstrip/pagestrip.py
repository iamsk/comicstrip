import os

from page import page


kw = dict(quiet=False,
          lignore=0,
          rignore=0,
          firstPgRow=0,
          startRow=0,
          gwidth=15,
          fwidth=100,
          fheight=100,
          debug=False,
          pgNum=1,
          contents=False)


def pagestrip(filename, directory):
    os.makedirs(directory)
    kw['infile'] = filename
    prefix = directory if directory.endswith('/') else directory + '/'
    count = page(**kw).save(prefix)
    return count


if __name__ == '__main__':
    filename = '/data/c2f52f696155b570454f5dcd086df2e6.jpg'
    directory = '/pages/c2f52f696155b570454f5dcd086df2e6'
    pagestrip(filename, directory)
