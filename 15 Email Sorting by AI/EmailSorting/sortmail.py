import imapclient
import pyzmail, re, os, platform
from Testing import Predict_mail
from mail import Mail
import pandas as pd
import email
from utils import find_between
from utils import get_sender
from Data_Writer import write_csv

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

df = pd.DataFrame(columns=['Overlap', 'Ready to Send', 'Tax Impact', 'Same-Day Contribution', 'Termination', 'Date'])
df.to_csv("daily_email_stats.csv", index=False)

imapObj.select_folder(folder, readonly=True)
stats_list = [0, 0, 0, 0, 0]
last_date = None

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
                sender_email, sender_id = get_sender(imapObj, uid)
                sender_email = "abdulrehman19427@gmail.com"
                if index == 0:
                    content = "Hi {}, \nReceived, your overlap request. thank you.".format(sender_id)
                    mail.send_mail([sender_email], label, content)
                    stats_list[index] = stats_list[index] + 1
                if index == 1:
                    content = "Hi {}, \nReceived, your request is completed (Ready to send). thank you.".format(sender_id)
                    mail.send_mail([sender_email], label, content)
                    stats_list[index] = stats_list[index] + 1
                if index == 2:
                    content = "Hi {}, \nReceived, your Tax Impact request received. thank you.".format(sender_id)
                    mail.send_mail([sender_email], label, content)
                    stats_list[index] = stats_list[index] + 1
                if index == 3:
                    content = "Hi {}, \nReceived, your Same-Day Contributions request. thank you.".format(sender_id)
                    mail.send_mail([sender_email], label, content)
                    stats_list[index] = stats_list[index] + 1
                if index == 4:
                    content = "Hi {}, \nReceived, your Termination request. thank you.".format(sender_id)
                    mail.send_mail([sender_email], label, content)
                    stats_list[index] = stats_list[index] + 1
                imapObj.move(uid, label)
    else:
        print("waiting...")

    writen_status, writen_date = write_csv(last_date, stats_list)
    if writen_status:
        last_date = writen_date
        stats_list = [0, 0, 0, 0, 0]

