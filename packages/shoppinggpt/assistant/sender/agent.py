import smtplib
from email.mime.text import MIMEText

def send_email(to_address, subject, content):
    from_address = "your_email@example.com"
    password = "your_password"
    
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = to_address

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(from_address, password)
        server.sendmail(from_address, to_address, msg.as_string())
