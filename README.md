# Automated Email Notificaiton Application

This little app will send `CEASE AND DESIST ORDER` email to people who you wish to stop emailing you!

# How To Use

## Required File

- create `credentials.py` in current location next to `warn_unwanted_people.py`
- it should have the following fields:
  - email = 'your_email@gmail.com'
  - passwd = 'your_email_password'
  - my_name = 'Your Fullname'

### You dont need virtual environment for this (including Pipenv)

## Send email using localhost

- run `python -m smtpd -n -c DebuggingServer localhost:1025` in another terminal
- instead of setting up your gmail smtp use `server = smtplib.SMTP( "localhost", 1025 )`
- your send email should show up in other terminal

## Full Usage

- When prompted to enter partial or full email enter full email or part of the email which can identify that person. Example:
  - Bad guy's full email is `bad_guy@gmail.com` then enter full email
  - If you want to send email from particular company such as `person1@domain_name.com` or `person2@domain_name.com` you can just enter `domain_name` and it will find all the recieved emails.
