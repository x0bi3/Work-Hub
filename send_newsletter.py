#!/usr/bin/env python3
"""
Newsletter Email Sender
Sends newsletter emails to all subscribers using Outlook SMTP
"""

import json
import smtplib
import sys
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def load_subscribers():
    """Load subscribers from subscribers.json"""
    try:
        with open('subscribers.json', 'r') as f:
            subscribers = json.load(f)
        print(f"[newsletter] Loaded {len(subscribers)} subscribers")
        return subscribers
    except FileNotFoundError:
        print("[newsletter] No subscribers.json file found")
        return []
    except json.JSONDecodeError as e:
        print(f"[newsletter] Error parsing subscribers.json: {e}")
        return []

def send_newsletter(subject, html_content, text_content=None):
    """
    Send newsletter to all subscribers
    
    Args:
        subject: Email subject line
        html_content: HTML email content
        text_content: Plain text email content (optional)
    """
    # Load configuration from environment variables
    smtp_server = os.getenv('SMTP_SERVER', 'smtp-mail.outlook.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    smtp_user = os.getenv('SMTP_USER')
    smtp_password = os.getenv('SMTP_PASSWORD')
    from_email = os.getenv('FROM_EMAIL', smtp_user)
    
    if not smtp_user or not smtp_password:
        print("[newsletter] Error: SMTP credentials not configured")
        print("[newsletter] Please set SMTP_USER, SMTP_PASSWORD, and optionally SMTP_SERVER, SMTP_PORT, FROM_EMAIL")
        return False
    
    # Load subscribers
    subscribers = load_subscribers()
    if not subscribers:
        print("[newsletter] No subscribers found")
        return False
    
    # Generate plain text version if not provided
    if not text_content:
        # Simple HTML to text conversion
        import re
        text_content = re.sub(r'<[^>]+>', '', html_content)
        text_content = text_content.replace('&nbsp;', ' ')
    
    success_count = 0
    error_count = 0
    
    # Connect to SMTP server
    try:
        print(f"[newsletter] Connecting to {smtp_server}:{smtp_port}")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        print("[newsletter] Successfully authenticated")
    except Exception as e:
        print(f"[newsletter] Error connecting to SMTP server: {e}")
        return False
    
    # Send to each subscriber
    for subscriber in subscribers:
        email = subscriber.get('email', '').strip()
        name = subscriber.get('name', 'Subscriber')
        
        if not email:
            print(f"[newsletter] Skipping subscriber with no email: {name}")
            continue
        
        try:
            # Create email message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = from_email
            msg['To'] = email
            
            # Personalize content
            personalized_html = html_content.replace('{name}', name)
            personalized_text = text_content.replace('{name}', name)
            
            # Add parts
            part1 = MIMEText(personalized_text, 'plain')
            part2 = MIMEText(personalized_html, 'html')
            
            msg.attach(part1)
            msg.attach(part2)
            
            # Send email
            server.send_message(msg)
            print(f"[newsletter] Sent to {email} ({name})")
            success_count += 1
            
        except Exception as e:
            print(f"[newsletter] Error sending to {email}: {e}")
            error_count += 1
    
    # Close connection
    try:
        server.quit()
    except:
        pass
    
    print(f"[newsletter] Newsletter sent: {success_count} successful, {error_count} errors")
    return success_count > 0

def main():
    """Main function - can be called from command line or GitHub Actions"""
    if len(sys.argv) < 3:
        print("Usage: python send_newsletter.py <subject> <html_file> [text_file]")
        print("\nOr set environment variables:")
        print("  NEWSLETTER_SUBJECT - Email subject")
        print("  NEWSLETTER_HTML - HTML content file path")
        print("  NEWSLETTER_TEXT - Plain text content file path (optional)")
        sys.exit(1)
    
    subject = sys.argv[1] if len(sys.argv) > 1 else os.getenv('NEWSLETTER_SUBJECT', 'Newsletter')
    html_file = sys.argv[2] if len(sys.argv) > 2 else os.getenv('NEWSLETTER_HTML')
    text_file = sys.argv[3] if len(sys.argv) > 3 else os.getenv('NEWSLETTER_TEXT')
    
    # Read HTML content
    try:
        with open(html_file, 'r') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"[newsletter] Error: HTML file not found: {html_file}")
        sys.exit(1)
    
    # Read text content if provided
    text_content = None
    if text_file:
        try:
            with open(text_file, 'r') as f:
                text_content = f.read()
        except FileNotFoundError:
            print(f"[newsletter] Warning: Text file not found: {text_file}")
    
    # Send newsletter
    success = send_newsletter(subject, html_content, text_content)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
