import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
   
def send_email(mailID,title,body='',attachment=''):
    '''
    :param mailID: to address
    :param title: subject of the email
    :param body: body of the email
    :param attachement: name of attachment file
    :result: None
    '''
    fromaddr = "emotiondetection123@gmail.com"
    toaddr = mailID 
    # instance of MIMEMultipart 
    msg = MIMEMultipart() 
    # storing the senders email address   
    msg['From'] = fromaddr 
    # storing the receivers email address  
    msg['To'] = mailID
    # storing the subject  
    msg['Subject'] = title
    # string to store the body of the mail 
    body = body
    # attach the body with the msg instance 
    msg.attach(MIMEText(body, 'plain')) 
    # open the file to be sent  
    if attachment != '':
        attach = open(attachment, "rb") 
        # instance of MIMEBase and named as p 
        p = MIMEBase('application', 'octet-stream') 
        # To change the payload into encoded form 
        p.set_payload((attach).read()) 
        # encode into base64 
        encoders.encode_base64(p) 
        p.add_header('Content-Disposition', "attachment; filename= %s" % attachment) 
        # attach the instance 'p' to instance 'msg' 
        msg.attach(p) 
    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    # start TLS for security 
    s.starttls() 
    # Authentication 
    s.login(fromaddr, "PASSWORD") 
    # Converts the Multipart msg into a string 
    text = msg.as_string() 
    # sending the mail 
    s.sendmail(fromaddr, toaddr, text) 
    # terminating the session 
    s.quit()
    return 
