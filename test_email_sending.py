#!/usr/bin/env python3
"""
Test email sending with current configuration
"""

from admin_app import admin_app, mail
from flask_mail import Message
import os

def test_email():
    with admin_app.app_context():
        print("Email Configuration:")
        print("=" * 50)
        print(f"MAIL_SERVER: {admin_app.config['MAIL_SERVER']}")
        print(f"MAIL_PORT: {admin_app.config['MAIL_PORT']}")
        print(f"MAIL_USE_SSL: {admin_app.config.get('MAIL_USE_SSL', False)}")
        print(f"MAIL_USE_TLS: {admin_app.config.get('MAIL_USE_TLS', False)}")
        print(f"MAIL_USERNAME: {admin_app.config['MAIL_USERNAME']}")
        print(f"MAIL_DEFAULT_SENDER: {admin_app.config['MAIL_DEFAULT_SENDER']}")
        print("=" * 50)
        print()

        # Get test recipient
        recipient = input("Enter recipient email address (press Enter to use ilhan@impactai.ba): ").strip()
        if not recipient:
            recipient = "ilhan@impactai.ba"

        print(f"\nSending test email to: {recipient}")
        print("Please wait...")

        try:
            msg = Message(
                subject="Modern360 - Test Email",
                recipients=[recipient],
                body="""This is a test email from Modern360 Assessment Platform.

If you received this email, your SMTP configuration is working correctly!

Email Configuration:
- SMTP Server: mail.impactai.ba
- Port: 465 (SSL/TLS)
- Sender: ilhan@impactai.ba

Best regards,
Modern360 Team
""",
                html="""
<html>
<body style="font-family: Arial, sans-serif; padding: 20px;">
    <h2 style="color: #4CAF50;">Modern360 - Test Email</h2>
    <p>This is a test email from <strong>Modern360 Assessment Platform</strong>.</p>
    <p>If you received this email, your SMTP configuration is working correctly! ✅</p>

    <hr style="margin: 20px 0;">

    <h3>Email Configuration:</h3>
    <ul>
        <li><strong>SMTP Server:</strong> mail.impactai.ba</li>
        <li><strong>Port:</strong> 465 (SSL/TLS)</li>
        <li><strong>Sender:</strong> ilhan@impactai.ba</li>
    </ul>

    <hr style="margin: 20px 0;">

    <p style="color: #666;">
        Best regards,<br>
        <strong>Modern360 Team</strong>
    </p>
</body>
</html>
"""
            )

            mail.send(msg)
            print("\n✅ Email sent successfully!")
            print(f"Check your inbox at: {recipient}")

        except Exception as e:
            print(f"\n❌ Error sending email: {e}")
            print(f"\nError details: {type(e).__name__}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    test_email()
