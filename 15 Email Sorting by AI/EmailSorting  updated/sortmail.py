import imapclient
import pyzmail, re, os, platform
from Testing import Predict_mail
from main import Mail
import pandas as pd
import email
from utils import find_between
from utils import get_sender

email_id = 'quickresponse21@outlook.com'
paswrd = "Inspire9"
current_platform = platform.system()

if current_platform == 'Windows':
    clear = lambda: os.system('cls')
else:
    clear = lambda: os.system('clear')
clear()

imap = "outlook.office365.com"
folder = "Inbox"
search = "UNSEEN"

try:
    imapObj = imapclient.IMAPClient(imap, ssl=True)
except:
    print('\nError - \nCould Not Connect \nPlease Check Your Internet Connection')
    exit(0)

try:
    imapObj.login(email_id, paswrd)
except:
    print('\nError - \nAuthentication Failed \nPlease Provide Valid Credentials')
    exit(0)

print('\nProcessing Please Wait ....')

imapObj.select_folder(folder, readonly=True)

while True:
    UIDs = imapObj.search([search])
    if UIDs:
        print("Start Scrapping..")
        for uid in UIDs:
            rawMessage = imapObj.fetch([uid], ['BODY[]', 'FLAGS'])
            message = pyzmail.PyzMessage.factory(rawMessage[uid][b'BODY[]'])

            if message.text_part:
                text = message.text_part.get_payload()
                text = text.decode(message.text_part.charset)
                text = text[:-2]

                escapes = '\b\n\r\t\\'
                for c in escapes:
                    text = text.replace(c, '')

                index, label = Predict_mail(text)

                mail = Mail()
                sender = get_sender(imapObj, uid)
                # sender = "abdulrehman19427@gmail.com"
                if index==0:
                    mail.send_mail([sender], label, "Recieved, thank you.")
                if index==1:
                    mail.send_mail([sender], label, "We will review, thank you.")
                imapObj.move(uid, label)
    else:
        print("waiting...")
