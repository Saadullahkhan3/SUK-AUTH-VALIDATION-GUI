import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from random import randint

class SendMail:
    def __init__(self, 
                 EMAIL, 
                 EMAIL_PASSWORD, 
                 SMTP_SERVER,
                 SMTP_SSL_PORT) -> None:
        self._EMAIL = EMAIL
        self._EMAIL_PASSWORD = EMAIL_PASSWORD
        self.SMTP_SERVER = SMTP_SERVER
        self.SMTP_SSL_PORT = SMTP_SSL_PORT


    def random_code(aelf, length: int = 6) -> int:
        return "".join([str(randint(0, 9)) for i in range(length)])


    def code_message(self, code: int) -> int:
        return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verification Code</title>
    <style>
        *{
            padding: 0;
            margin: 0;
            box-sizing: border-box;
        }
        html, body{
            width: 100vw;
            height: 100vh;
        }
        h1{
            display: flex;
            align-items: center;
            justify-content: center;
            color: #414141;
            font-family: 'Franklin Gothic Medium';
        }
    </style>
</head>
<body>
    <h1>CODE : ''' + f"{code}" + '''</h1>
</body>
</html>
'''
    
    
    def send_email(self, to_email, subject, message, html=False):
        '''
        UseCase:
        ---
        Send Email via SMTP, Here MIMEMultipart() and MIMEText is used to make this function dynamic so it can also send HTML (with CSS, JS) content. Also can send Plain Text.

        Args:
        ---
        - to_email: str -> Where to send Email.
        - subjet: str -> Subject of the Email.
        - message: str -> Plain Text or HTML in str.
        - html: bool (default False) -> True when message is HTML  

        '''
        try:
            # Email Content and setting its attribute.
            msg = MIMEMultipart()
            msg['From'] = self._EMAIL
            msg['To'] = to_email
            msg['Subject'] = subject

            html_or_plain = 'html' if html else 'plain'
            msg.attach(MIMEText(message, html_or_plain))
            
            # Server Login and Sending Mail through SMTP SSL, then quit.
            mailserver = smtplib.SMTP_SSL(self.SMTP_SERVER, self.SMTP_SSL_PORT)        
            mailserver.ehlo()
            mailserver.login(self._EMAIL, self._EMAIL_PASSWORD) 
            mailserver.sendmail(self._EMAIL, to_email, msg.as_string())
            mailserver.quit()

            print(f"Successfully sent email to -> {to_email}")

        except Exception as e:
            print(f"Failed to send email to -> {to_email}: {e}")

