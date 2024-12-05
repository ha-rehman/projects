# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import base64
import pyzmail


class Mail:

    def __init__(self):
        sender_name = u'MAA TEST'
        sender_email = 'quickresponse21@outlook.com'
        self.__sender = (sender_name, sender_email)

        self.__text_encoding = 'iso-8859-1'
        self.__preferred_encoding = 'iso-8859-1'

        self.__smtp_host = 'smtp.outlook.com'
        self.__smtp_port = 587
        self.__smtp_mode = 'tls'
        self.__smtp_login = sender_email
        self.__smtp_password = 'Inspire9'

    def __get_status(self, mail_obj):
        if isinstance(mail_obj, dict):
            if mail_obj:
                print('failed recipients:', ', '.join(mail_obj.keys()))
            else:
                pass
                # print('success')
        else:
            print('error:', mail_obj)

    def send_mail(self, recipients, subject, text_content):
        payload, mail_from, rcpt_to, msg_id = pyzmail.compose_mail(
            self.__sender,
            recipients,
            subject,
            self.__preferred_encoding,
            (text_content, self.__text_encoding),
            html=None,
            # attachments=[('attached content', 'text', 'plain', 'text.txt', 'us-ascii')]
            )

        ret = pyzmail.send_mail(payload, mail_from, rcpt_to, self.__smtp_host,
                                smtp_port=self.__smtp_port, smtp_mode=self.__smtp_mode,
                                smtp_login=self.__smtp_login, smtp_password=self.__smtp_password)

        self.__get_status(ret)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    mail = Mail()
    mail.send_mail(['abdul.rehman@kics.edu.pk'], "Testing", "it is an testing mail.")


