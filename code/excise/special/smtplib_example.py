import smtplib
from email.mime.text import MIMEText

#
mail_host = "smtp.163.com"  # 
mail_user = "shenwanjiang2013"  # 
mail_pass = "Y0kogawa"  # 

sender = 'shenwanjiang2013@163.com'  
receivers = ['aaron_shen2015@163.com']  


content = '123456!'
title = 'Python SMTP Mail Test'  # 
message = MIMEText(content, 'plain', 'utf-8')  # 
message['From'] = "{}".format(sender)
message['To'] = ",".join(receivers)
message['Subject'] = title

try:
    smtpObj = smtplib.SMTP_SSL(mail_host, 465)  #
    smtpObj.login(mail_user, mail_pass)  #
    smtpObj.sendmail(sender, receivers, message.as_string())  #
    print("mail has been send successfully.")
except smtplib.SMTPException as e:
    print(e)