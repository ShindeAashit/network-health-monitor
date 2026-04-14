# alerter.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import config

# Track last alert time per host to avoid spam
_last_alert = {}

def should_alert(host):
    """Returns True if cooldown period has passed for this host."""
    import time
    last = _last_alert.get(host, 0)
    return (time.time() - last) > config.ALERT_COOLDOWN

def send_alert(host, label, status):
    """Sends an email alert for a host going DOWN or recovering UP."""
    if status == "DOWN" and not should_alert(host):
        return  # Still in cooldown

    import time
    _last_alert[host] = time.time()

    subject = f"[ALERT] Host {status}: {label} ({host})"
    body = (
        f"Network Monitor Alert"
        f"{'='*40}"
        f"Host    : {host}"
        f"Label   : {label}"
        f"Status  : {status}"
        f"Time    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        f"{'='*40}"
        f"Check your infrastructure immediately."
    )

    msg = MIMEMultipart()
    msg["From"]    = config.EMAIL_SENDER
    msg["To"]      = config.EMAIL_RECIEVER
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as server:
            server.starttls()
            server.login(config.EMAIL_SENDER, config.EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"  >> Alert sent for {host}")
    except Exception as e:
        print(f"  >> Alert failed: {e}")
