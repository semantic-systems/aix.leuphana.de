# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv"
# ]
# ///

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

def test_smtp():
    load_dotenv()
    
    smtp_host = "sysmail.leuphana.de"
    smtp_port = 587
    smtp_user = "creativespace"
    smtp_pass = os.environ.get('SMTP_PASSWORD')
    
    if not smtp_pass:
        print("❌ Error: SMTP_PASSWORD is not set in your .env file!")
        return
        
    from_email = "creativespace-noreply@leuphana.de"
    to_email = "Muratbek.Nurmatov@stud.leuphana.de"
    
    print(f"Attempting to connect to {smtp_host}:{smtp_port} as {smtp_user}...")
    
    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.set_debuglevel(1) # This will print out exactly what the server is saying
        
        print("Starting TLS...")
        server.starttls()
        
        print("Logging in...")
        server.login(smtp_user, smtp_pass)
        
        print("Composing email...")
        msg = MIMEMultipart()
        msg['From'] = f"SMTP Tester <{from_email}>"
        msg['To'] = to_email
        msg['Subject'] = "Test Email from Python SMTP"
        
        body = "Hello!\n\nIf you are reading this, your SMTP configuration works perfectly.\n\nBest,\nSMTP Tester Script"
        msg.attach(MIMEText(body, 'plain'))
        
        print("Sending message...")
        server.send_message(msg)
        server.quit()
        
        print(f"\n✅ SUCCESS! Email sent to {to_email}")
        
    except Exception as e:
        print(f"\n❌ FAILED! Error details:\n{str(e)}")

if __name__ == "__main__":
    test_smtp()
