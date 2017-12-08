#!/usr/bin/env python  # start line
# coding:utf-8
import poplib
import re

mail_host = "pop.163.com"
mail_user = "aaron_shen2015"
mail_pass = "shen19870314"

sendmail_user = 'shenwanjiang2013'
sendmail_pass = 'Y0kogawa' 

popClient = poplib.POP3_SSL(mail_host)
popClient.user(sendmail_user)
popClient.pass_(sendmail_pass)
 
numMsgs, mboxSize = popClient.stat()
 
print "Number of messages ", numMsgs
print "Mailbox size", mboxSize
print
 
for id in range (numMsgs):
    for mail in popClient.retr(id+1)[1]:
        if re.search( 'Subject:', mail ):
            print mail
 
    print
popClient.quit()
