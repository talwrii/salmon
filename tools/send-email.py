

# Import smtplib for the actual sending function
import argparse
import smtplib

# Here are the email package modules we'll need
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email.policy

PARSER = argparse.ArgumentParser(description='')
PARSER.add_argument('--html-file', type=str)


def main():
    # Create the container (outer) email message.

    args = PARSER.parse_args()
    msg = MIMEMultipart(policy=email.policy.HTTP.clone(max_line_length=78))
    msg['Subject'] = 'Our family reunion'
    # me == the sender's email address
    # family = the list of all recipients' email addresses

    me = 'user@localhost'
    recipient = 'recipient@localhost'
    msg['From'] = me
    msg['To'] = recipient
    msg.preamble = 'Subject'

    if args.html_file:
        with open(args.html_file) as stream:
            html = stream.read()
    else:
        html = '<a>html message</a>\n'

    msg.attach(MIMEText('plain email\n', 'plain'))
    msg.attach(MIMEText(html, 'html'))

    # Send the email via our own SMTP server.
    s = smtplib.SMTP('localhost', port=1025)
    s.sendmail(me, recipient, msg.as_string())
    s.quit()


if __name__ == '__main__':
	main()
