import time
import credentials


username = credentials.email
password = credentials.passwd
my_name = credentials.my_name

bad_guys = [('Elyorbek Soliev', 'elyorbeksoliev@gmail.com')]


def _read_email(email_from):
    import imaplib

    server = imaplib.IMAP4_SSL('imap.gmail.com', 993)

    server.login(username, password)
    server.select('INBOX')

    filter_term = f'(FROM "{email_from}")'
    status, data = server.search(None, filter_term)

    for num in data[0].split():
      status, data = server.fetch(num, '(BODY[HEADER.FIELDS (FROM)])')
      bad_guy = (data[0][1]).decode("utf-8")
      bad_guy = bad_guy.replace('From:', '')
      bad_guy = bad_guy.strip()
      full_name, email = bad_guy.split('<')
      email = email.replace('>', '')

      bad_guys.append((full_name, email))

    server.quit()


def _send_email():
    import smtplib
    from email.message import EmailMessage

    # python -m smtpd -n -c DebuggingServer localhost:1025
    # server = smtplib.SMTP( "localhost", 1025 )
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(username, password)

    email_template = 'email_template.html'

    for bad_guy in bad_guys:
        bad_guy_name = bad_guy[0]
        bad_guy_email = bad_guy[1] 
        today = time.ctime()

        with open(email_template) as template:
            email_body = template.read()
            email_body = email_body.replace('{bad_guy_name}', bad_guy_name)
            email_body = email_body.replace('{today}', str(today))
            email_body = email_body.replace('{my_name}', my_name)

        msg = EmailMessage()
        msg.set_content(email_body, subtype='html')
        msg['Subject'] = 'Warning!'
        msg['From'] = username
        msg['To'] = bad_guy_email

        server.send_message(msg)

    server.quit()


if __name__ == "__main__":
    from_who = input('Please enter partial or full email [company_name or name@company.com]:')
    # _read_email(email_from)
    _send_email()