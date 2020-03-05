import os
import time
import credentials

username = credentials.email
password = credentials.passwd
my_name = credentials.my_name

bad_guys = set()

def _read_email(email_from):
    import imaplib

    server = imaplib.IMAP4_SSL('imap.gmail.com', 993)
    server.login(username, password)

    d = server.list()[1]

    for ch in d:
        folder = ch.decode().split(' "/" ')[1]
        
        state, date = server.select(folder)
        if state == 'NO':
            continue

        print(f'Checking folder: {folder}')

        filter_term = f'(FROM "{email_from}")'
        status, data = server.search(None, filter_term)

        for num in data[0].split():
            status, data = server.fetch(num, '(BODY[HEADER.FIELDS (FROM)])')
            bad_guy = (data[0][1]).decode("utf-8")
            bad_guy = bad_guy.replace('From:', '')
            bad_guy = bad_guy.strip()
            full_name, email = bad_guy.split('<')
            email = email.replace('>', '')

            bad_guys.add((full_name.strip(), email.strip()))
    return bad_guys


def _send_email(bad_guys):
    import smtplib
    from email.message import EmailMessage

    # server = smtplib.SMTP( "localhost", 1025 )
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(username, password)

    email_template = 'email_template.html'
    tracking_already_sent = 'already_send.txt'

    print(f'\n Found {len(bad_guys)} bad guys')
    print('=' * 50)
    
    for i, val in enumerate(bad_guys):
        print(f'{i}. {val[0]} \t {val[1]}')

    print('=' * 50)

    answer = input('\nSend email all the bad guys(y/n)? ')
    if (answer.strip().lower() != 'y'):
        print('\nNo Warnings Sent!')
        return

    already_notified_people = []

    if os.path.isfile(tracking_already_sent):
        with open(tracking_already_sent, 'r') as f:
            for line in f:
                already_notified_people.append(eval(line.strip()))

    for bad_guy in bad_guys:
        if bad_guy in already_notified_people:
            print(f'{bad_guy[0]} already been notified!')
            continue
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

        print(f'Sending email to: {bad_guy_name}, \t target_email: {bad_guy_email}')
        server.send_message(msg)

        with open(tracking_already_sent, 'a+') as f:
            f.write(str(bad_guy))
            f.write('\n')

    server.quit()


if __name__ == "__main__":
    os.system('clear')
    from_who = input('\nPlease enter partial or full email [company_name or name@company.com]: ')
    bad_guys = _read_email(from_who)
    # Uncomment this line to add someone manually
    # bad_guys.add(('John Doe', 'john.doe@companyinc.com'))
    _send_email(bad_guys)
    print('\nDONE!')