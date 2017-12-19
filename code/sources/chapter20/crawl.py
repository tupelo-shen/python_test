#! /usr/bin/env python
# -*- coding: UTF-8 -*-

'''
Advanced Web Client: a Web Crawler
'''

from sys        import argv
from os         import makedirs, unlink, sep
from os.path    import dirname, exists, isdir, splitext
from string     import replace, find, lower
from htmllib    import HTMLParser
from urllib     import urlretrieve
from urlparse   import urlparse, urljoin
from formatter  import DumbWriter, AbstractFormatter
from cStringIO  import StringIO

# download Web pages
class Retriever(object):
    def __init__(self, url):
        self.url = url
        self.file = self.filename(url)

    def filename(self, url, deffile='index.html'):
        parsedurl = urlparse(url, 'https:', 0) ## parse path
        path = parsedurl[1] + parsedurl[2]
        ext = splitext(path)

        if ext[1] == '': # no file, use default
            if path[-1] == '/':
                path += deffile
            else:
                path += '/' + deffile
        ldir = dirname(path) # local

        # os-indep. path separator 
        if sep != '/': 
            ldir = replace(ldir, '/', sep)

         # create archive dir if nec.
        if not isdir(ldir):
            if exists(ldir): 
                unlink(ldir)
            makedirs(ldir)

        return path

    # download Web page
    def download(self):
        try:
            retval = urlretrieve(self.url, self.file)
        except IOError:
            retval = ('*** ERROR: invalid URL "%s"' % self.url,)
        return retval

    # parse HTML, save links
    def parseAndGetLinks(self):
        self.parser = HTMLParser(AbstractFormatter(DumbWriter(StringIO())))
        self.parser.feed(open(self.file).read())
        self.parser.close()
        return self.parser.anchorlist

# manage entire crawling process
class Crawler(object):
    count = 0 # static downloaded page counter
    def __init__(self, url):
        self.q = [url]
        self.seen = []
        self.dom = urlparse(url)[1]

    def getPage(self, url):
        r = Retriever(url)
        retval = r.download()
        # error situation, do not parse
        if retval[0] == '*': 
            print retval, '... skipping parse'
            return
        Crawler.count += 1
        print '\n(', Crawler.count, ')'
        print 'URL:', url       
        print 'FILE:', retval[0]
        self.seen.append(url)

        # get and process links
        links = r.parseAndGetLinks()
        for eachLink in links:
            if eachLink[:4] != 'http' and find(eachLink, '://') == -1:
                eachLink = urljoin(url, eachLink)
                print '* ', eachLink
            if find(lower(eachLink), 'mailto:') != -1:
                print '... discarded, mailto link'
                continue
            if eachLink not in self.seen:
                if find(eachLink, self.dom) == -1:
                    print '... discarded, not in domain'
                else:
                    if eachLink not in self.q:
                        self.q.append(eachLink)
                        print '... new, added to Q'
                    else:
                        print '... discarded, already in Q'
            else:
                print '... discarded, already processed'

    # process links in queue
    def go(self):
        while self.q:
            url = self.q.pop()
            self.getPage(url)

def main():
    if len(argv) > 1:
        url = argv[1]
    else:
        try:
            url = raw_input('Enter starting URL:')
        except(KeyboardInterrupt, EOFError):
            url = ''
    if not url:
        return
    robot = Crawler(url)
    robot.go()

if __name__ == '__main__':
    main()
