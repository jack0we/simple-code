import smtplib
import os
from email.message import EmailMessage
from email.utils import make_msgid
from getpass import getpass
from email_validator import validate_email, EmailNotValidError

# validate
def prompt_email(prompt):
    while True:
        try:
            email_input = input(prompt)
            valid = validate_email(email_input)
            return valid.email  # Return the normalized form of the email if valid
        except EmailNotValidError as e:
            print(str(e))

# send email with attacjment
def send_email(smtp_server, port, sender_email, receiver_email, password, subject, body, attachment_path):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content(body)

    # input attchment
    if os.path.isfile(attachment_path):
        with open(attachment_path, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(f.name)
        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
    else:
        print("Attachment file not found.")
        return

    try:
        with smtplib.SMTP_SSL(smtp_server, port) as smtp:
            smtp.login(sender_email, password)
            smtp.send_message(msg)
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# cred and information
smtp_server = input("Enter SMTP server: ")
port = 465  # change if necessary
sender_email = prompt_email("Enter your email: ")
receiver_email = prompt_email("Enter receiver email: ")
subject = "Subject of the email"
body = "This is the body of the email."
attachment_path = input("Enter the path to the PDF file: ")

password = getpass("Enter your password: ")

send_email(smtp_server, port, sender_email, receiver_email, password, subject, body, attachment_path)
