import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_event_email(event_name, event_date, recipient_email):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    sender_email = "volunteerapp29@gmail.com"
    sender_password = "bvtc znga zvtv egyz"  # Your app password here

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = f"New Event Created: {event_name}"

    body = f"""
Hello,

A new event has been created:

Event: {event_name}
Date: {event_date}

Thank you,
Ripple App
"""
    msg.attach(MIMEText(body, 'plain'))

    try:
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        smtp.starttls()
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)
        smtp.quit()
        print(f"Email sent to {recipient_email} successfully.")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
