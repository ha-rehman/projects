import datetime
import email
from email.header import decode_header
import imaplib
import mailbox
import pyzmail, re, os, platform



def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def get_sender(imapObj, uid):
    response = imapObj.fetch([uid], ['RFC822'])
    for msgid, data in response.items():
        msg_string = data[b'RFC822']
        msg = email.message_from_string(msg_string.decode())
        sender_mail = find_between(msg['From'], '<', '>')
        sender_id = (find_between(msg['From'], '', '<')).strip()
        # print(sender_id)
        return sender_mail, sender_id
