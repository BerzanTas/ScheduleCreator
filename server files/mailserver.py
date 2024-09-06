import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import os

def send_confirmation_email(recipient_email):
    """Send a confirmation email to the user after successful registration"""
    sender_email = os.getenv('EMAIL_ADDRESS')  # get the sender email from environment variables
    sender_password = os.getenv('EMAIL_PASSWORD')  # get the sender password from environment variables
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.examplesmtp.com')  # default SMTP server if not set
    smtp_port = os.getenv('SMTP_PORT', 1)  # default SMTP port if not set

    if not sender_email or not sender_password:
        # raise an error if email or password is not set in environment variables
        raise ValueError("Email address or password environment variables are not set.")

    print(f"Sender email: {sender_email}")  # log the sender email for debugging

    # email content setup
    subject = "Registration Confirmation"  # subject of the confirmation email
    body = f"""
    Hi there,

    Your account has been successfully created!

    Best regards,
    Schedule Creator Team
    """

    # create the email message
    msg = MIMEMultipart()
    msg['From'] = formataddr(('Schedule Creator', sender_email))  # format sender details
    msg['To'] = recipient_email  # set the recipient's email
    msg['Subject'] = subject  # set the email subject

    # attach the email body to the message
    msg.attach(MIMEText(body, 'plain'))

    try:
        # connect to the SMTP server
        with smtplib.SMTP(smtp_server, int(smtp_port)) as server:
            server.starttls()  # initiate TLS encryption for the connection
            server.login(sender_email, sender_password)  # login to the SMTP server
            server.sendmail(sender_email, recipient_email, msg.as_string())  # send the email
            print("Confirmation email sent successfully.")  # log success
    except smtplib.SMTPAuthenticationError:
        # handle error when authentication to the SMTP server fails
        print("Failed to send email: Authentication error. Please check your email and password.")
    except smtplib.SMTPConnectError:
        # handle error when the connection to the SMTP server fails
        print("Failed to send email: Could not connect to the SMTP server. Check server address and port.")
    except smtplib.SMTPException as e:
        # handle other SMTP-related errors
        print(f"Failed to send email due to SMTP error: {e}")
    except Exception as e:
        # handle any other unexpected errors
        print(f"An unexpected error occurred: {e}")
