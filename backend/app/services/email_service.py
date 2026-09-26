import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional
from app.core.config import settings

logger = logging.getLogger(__name__)


def send_otp_email(to_email: str, otp: str, user_name: Optional[str] = None) -> bool:
    """
    Sends OTP to the user's email via SMTP (e.g. Gmail SMTP or custom host).
    If SMTP credentials are not yet set in .env, logs the email content gracefully.
    """
    if not settings.SMTP_HOST or not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        logger.info(
            f"[OTP Service] SMTP not configured. Simulated email to {to_email} with OTP: {otp}"
        )
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"StockSense Security Verification Code: {otp}"
        msg["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL or settings.SMTP_USER}>"
        msg["To"] = to_email

        greeting = f"Hello {user_name}," if user_name else "Hello,"

        text_content = f"""{greeting}

You have requested a one-time verification code (OTP) to reset your StockSense account password.

Your verification code is: {otp}

This code will expire in {settings.OTP_EXPIRE_MINUTES} minutes.

If you did not request this password reset, please ignore this email.

Best regards,
The StockSense Team
"""

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="utf-8">
          <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #0b0f17; color: #f3f6fa; padding: 24px; }}
            .container {{ max-width: 540px; margin: 0 auto; background: #131b26; border: 1px solid #222f42; border-radius: 12px; padding: 32px; }}
            .brand {{ font-size: 20px; font-weight: 800; color: #ff5e62; margin-bottom: 20px; }}
            .code-box {{ background: #1a2332; border: 1px dashed #ff5e62; border-radius: 8px; padding: 18px; text-align: center; margin: 24px 0; }}
            .code {{ font-size: 32px; font-weight: 800; letter-spacing: 6px; color: #ffffff; }}
            .footer {{ font-size: 12px; color: #8b9bb4; margin-top: 24px; border-top: 1px solid #222f42; padding-top: 16px; }}
          </style>
        </head>
        <body>
          <div class="container">
            <div class="brand">StockSense</div>
            <p>{greeting}</p>
            <p>You have requested a one-time verification code (OTP) to reset your password.</p>
            <div class="code-box">
              <div class="code">{otp}</div>
            </div>
            <p style="font-size: 14px; color: #8b9bb4;">This code is valid for <strong>{settings.OTP_EXPIRE_MINUTES} minutes</strong>. Do not share this code with anyone.</p>
            <div class="footer">
              If you did not request this change, you can safely ignore this email.<br>
              &copy; StockSense Inventory Platform
            </div>
          </div>
        </body>
        </html>
        """

        part1 = MIMEText(text_content, "plain")
        part2 = MIMEText(html_content, "html")
        msg.attach(part1)
        msg.attach(part2)

        if settings.SMTP_TLS:
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.sendmail(settings.SMTP_FROM_EMAIL or settings.SMTP_USER, to_email, msg.as_string())
        else:
            with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.sendmail(settings.SMTP_FROM_EMAIL or settings.SMTP_USER, to_email, msg.as_string())

        logger.info(f"[OTP Service] Successfully sent OTP email to {to_email}")
        return True
    except Exception as e:
        logger.error(f"[OTP Service] Failed to send email via SMTP: {e}")
        return False
