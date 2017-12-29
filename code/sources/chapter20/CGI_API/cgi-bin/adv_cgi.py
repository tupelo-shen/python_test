#!/usr/bin/env python

from cgi import FieldStorage
from os import environ
from cStringIO import StringIO
from urllib import quote, unquote
from string import capwords, strip, split, join

class AdvCgi(object):
    """docstring for AdvCgi"""
    header = 'Content-Type: text/html\n\n'
    url = '/cgi-bin/adv_cgi.py'
    formhtml = '''<HTML><HEAD><TITLE>
    Advanced CGI Demo</TITLE></HEAD>
    <BODY><H2>Advanced CGI Demo Form</H2>
    <FORM METHOD=post ACTION="%s" ENCTYPE="multipart/form-data">
    <H3>My Cookie Setting</H3>
    <LI> <CODE><B>CPPuser = %s</B></CODE>
    <H3>Enter cookie value<BR>
    <INPUT NAME=cookie value="%s"> (<I>optional</I>)</H3>
    <H3>Enter your name<BR>
    <INPUT NAME=person VALUE="%s"> (<I>required</I>)</H3>
    <H3>What languages can you program in?
    (<I>at least one required</I>)</H3>
    %s
    <H3>Enter file to upload</H3>
    <INPUT TYPE=file NAME=upfile VALUE="%s" SIZE=45>
    <P><INPUT TYPE=submit>
    </FORM></BODY></HTML>'''
    langSet = ('Python', 'PERL', 'Java', 'C++', 'PHP','C', 'JavaScript')
    langItem = '<INPUT TYPE=checkbox NAME=lang VALUE="%s"%s> %s\n'

    def getCPPCookies(self): # read cookies from client
        if environ.has_key('HTTP_COOKIE'):
            for eachCookie in map(strip, split(environ['HTTP_COOKIE'], ';')):
                if len(eachCookie) > 6 and eachCookie[:3] == 'CPP':
                    tag = eachCookie[3:7]
                    try:
                        self.cookies[tag] = eval(unquote(eachCookie[8:])) 
                    except(NameError, SyntaxError):
                        self.cookies[tag] = unquote(eachCookie[8:])
                else:
                    self.cookies['info'] = self.cookies['user'] = ''

                if self.cookies['info'] != '':
                    self.who, langStr, self.fn = split(self.cookies['info'], ':')
                    self.langs = split(langStr, ',')
                else:
                    self.who = self.fn = ' '
                    self.langs = ['Python']


    def showForm(self): # show fill-out form
        self.getCPPCookies()
        langStr = ''
        for eachLang in AdvCGI.langSet:
            if eachLang in self.langs:
                langStr += AdvCGI.langItem % \
                (eachLang, ' CHECKED', eachLang)
            else:
                langStr += AdvCGI.langItem % \
                (eachLang, '', eachLang)

            if not self.cookies.has_key('user') or \
                self.cookies['user'] == '':
                cookStatus = '<I>(cookie has not been set yet)</I>'
                userCook = ''
            else:
                userCook = cookStatus = self.cookies['user']

            print AdvCGI.header + AdvCGI.formhtml % (AdvCGI.url,cookStatus, userCook, self.who, langStr, self.fn)

    errhtml = '''<HTML><HEAD><TITLE>
    Advanced CGI Demo</TITLE></HEAD>
    <BODY><H3>ERROR</H3>
    <B>%s</B><P>
    <FORM><INPUT TYPE=button VALUE=Back
    ONCLICK="window.history.back()"></FORM>
    </BODY></HTML>'''
def showError(self):
    print AdvCGI.header + AdvCGI.errhtml % (self.error)

reshtml = '''<HTML><HEAD><TITLE>
Advanced CGI Demo</TITLE></HEAD>
<BODY><H2>Your Uploaded Data</H2>
<H3>Your cookie value is: <B>%s</B></H3>
<H3>Your name is: <B>%s</B></H3>
<H3>You can program in the following languages:</H3>
<UL>%s</UL>
<H3>Your uploaded file...<BR>
Name: <I>%s</I><BR>
Contents:</H3>
<PRE>%s</PRE>
Click <A HREF="%s"><B>here</B></A> to return to form.
</BODY></HTML>'''

def setCPPCookies(self):# tell client to store cookies
    for eachCookie in self.cookies.keys():
        print 'Set-Cookie: CPP%s=%s; path=/' % (eachCookie, quote(self.cookies[eachCookie]))

def doResults(self):# display results page
    MAXBYTES = 1024
    langlist = ''
    for eachLang in self.langs:
        langlist = langlist + '<LI>%s<BR>' % eachLang

    filedata = ''
    while len(filedata) < MAXBYTES:# read file chunks 
120 data = self.fp.readline()
121 if data == '': break
122 filedata += data
123 else: # truncate if too long
124 filedata += \
125 '... <B><I>(file truncated due to size)</I></B>'
126 self.fp.close()
127 if filedata == '':
128 filedata = \
129 <B><I>(file upload error or file not given)</I></B>'
130 filename = self.fn

132 if not self.cookies.has_key('user') or \
133 self.cookies['user'] == '':
134 cookStatus = '<I>(cookie has not been set yet)</I>'
135 userCook = ''
136 else:
137 userCook = cookStatus = self.cookies['user']

139 self.cookies['info'] = join([self.who, \
140 join(self.langs, ','), filename], ':')
141 self.setCPPCookies()
142 print AdvCGI.header + AdvCGI.reshtml % \
143 (cookStatus, self.who, langlist,
144 filename, filedata, AdvCGI.url)

def go(self): # determine which page to return
    self.cookies = {}
    self.error = ''
    form = FieldStorage()
    if form.keys() == []:
        self.showForm()
        return

    if form.has_key('person'):
        self.who = capwords(strip(form['person'].value))
        if self.who == '':
            self.error = 'Your name is required. (blank)'
        else:
            self.error = 'Your name is required. (missing)'

    if form.has_key('cookie'):
        self.cookies['user'] = unquote(strip(form['cookie'].value))
    else:
        self.cookies['user'] = ''

    self.langs = []
    if form.has_key('lang'):
        langdata = form['lang']
        if type(langdata) == type([]):
            for eachLang in langdata:
                self.langs.append(eachLang.value)
        else:
            self.langs.append(langdata.value)
    else:
        self.error = 'At least one language required.'

    if form.has_key('upfile'):
        upfile = form["upfile"]
        self.fn = upfile.filename or ''
        if upfile.file:
            self.fp = upfile.file
        else:
        self.fp = StringIO('(no data)')
    else:
        self.fp = StringIO('(no file)')
        self.fn = ''

    if not self.error:
        self.doResults()
    else:
        self.showError()

if __name__ == '__main__':
    page = AdvCGI()
    page.go()   