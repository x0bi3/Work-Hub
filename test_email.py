#!/usr/bin/env python3
"""
Test script to verify SMTP configuration
Run this to test your Outlook SMTP connection before sending newsletters
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_smtp_connection():
    """Test SMTP connection and send a test email"""
    
    # Get configuration from environment or prompt
    smtp_server = os.getenv('SMTP_SERVER', 'smtp-mail.outlook.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    smtp_user = os.getenv('SMTP_USER')
    smtp_password = os.getenv('SMTP_PASSWORD')
    from_email = os.getenv('FROM_EMAIL', smtp_user)
    test_email = os.getenv('TEST_EMAIL', smtp_user)
    
    # Prompt for missing values
    if not smtp_user:
        smtp_user = input("Enter your Outlook email: ")
    if not smtp_password:
        import getpass
        smtp_password = getpass.getpass("Enter your Outlook password (or app password): ")
    if not test_email:
        test_email = input(f"Enter test recipient email (default: {smtp_user}): ") or smtp_user
    
    print(f"\n[test] Testing SMTP connection...")
    print(f"[test] Server: {smtp_server}:{smtp_port}")
    print(f"[test] User: {smtp_user}")
    print(f"[test] Sending test email to: {test_email}\n")
    
    try:
        # Create test email
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Work Hub - SMTP Test Email'
        msg['From'] = from_email or smtp_user
        msg['To'] = test_email
        
        text = """This is a test email from Work Hub Newsletter system.
        
If you received this, your SMTP configuration is working correctly!
        
You can now send newsletters to your subscribers."""
        
        html = """<html>
        <body>
            <h2>Work Hub - SMTP Test Email</h2>
            <p>This is a test email from Work Hub Newsletter system.</p>
            <p>If you received this, your SMTP configuration is working correctly!</p>
            <p>You can now send newsletters to your subscribers.</p>
        </body>
        </html>"""
        
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        
        msg.attach(part1)
        msg.attach(part2)
        
        # Connect and send
        print("[test] Connecting to SMTP server...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        print("[test] Starting TLS...")
        server.starttls()
        print("[test] Authenticating...")
        server.login(smtp_user, smtp_password)
        print("[test] Sending test email...")
        server.send_message(msg)
        server.quit()
        
        print("\n✅ SUCCESS! Test email sent successfully.")
        print(f"   Check your inbox at: {test_email}")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"\n❌ AUTHENTICATION FAILED: {e}")
        print("\nPossible solutions:")
        print("1. Verify your email and password are correct")
        print("2. If using 2FA, generate an app-specific password")
        print("3. Check if your organization requires special SMTP settings")
        return False
        
    except smtplib.SMTPConnectError as e:
        print(f"\n❌ CONNECTION FAILED: {e}")
        print("\nPossible solutions:")
        print("1. Verify SMTP_SERVER and SMTP_PORT are correct")
        print("2. Check your internet connection")
        print("3. Check if firewall is blocking SMTP connections")
        print("4. Try port 465 with SSL instead of 587 with TLS")
        return False
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nCheck your configuration and try again.")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("Work Hub Newsletter - SMTP Configuration Test")
    print("=" * 60)
    print()
    
    success = test_smtp_connection()
    
    print()
    print("=" * 60)
    if success:
        print("✅ Your SMTP configuration is ready!")
        print("   You can now configure GitHub Secrets and send newsletters.")
    else:
        print("❌ Please fix the issues above before proceeding.")
    print("=" * 60)
