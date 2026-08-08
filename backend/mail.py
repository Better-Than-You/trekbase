import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import current_app


def init_mail(app):
    # Mailpit dev server runs its SMTP on localhost:1025 (no auth / TLS by default)
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'localhost')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 1025))
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'false').lower() == 'true'
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@trekbase.com')


def send_email(recipient, subject, html_content, text_content=None):
    # reads settings from current_app (set up by init_mail)
    smtp_server = current_app.config.get("MAIL_SERVER", "localhost")
    smtp_port = current_app.config.get("MAIL_PORT", 1025)
    use_tls = current_app.config.get("MAIL_USE_TLS", False)
    sender_email = current_app.config.get("MAIL_DEFAULT_SENDER", "noreply@trekbase.com")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient

    plain_text = text_content or "Please use an HTML-compatible email client."
    msg.attach(MIMEText(plain_text, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    try:
        if use_tls:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.sendmail(sender_email, recipient, msg.as_string())
        else:
            # plain SMTP is enough for local Mailpit
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.sendmail(sender_email, recipient, msg.as_string())
        return True
    except Exception as e:
        current_app.logger.error(f"Email delivery failed: {e}")
        return False