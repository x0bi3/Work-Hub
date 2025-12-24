# Newsletter Setup Guide

This guide will help you set up the newsletter and email system using GitHub and Outlook.

## Overview

The newsletter system consists of:
1. **Frontend**: HTML form that collects subscriber information
2. **Storage**: `subscribers.json` file that stores all subscribers
3. **Processing**: GitHub Actions workflow that processes new subscriptions
4. **Email Sending**: Python script that sends emails via Outlook SMTP

## Prerequisites

- GitHub repository (already set up)
- Outlook/Office 365 work account with SMTP access
- GitHub Actions enabled in your repository

## Step 1: Configure GitHub Secrets

You need to add the following secrets to your GitHub repository:

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** and add:

### Required Secrets:

- **`SMTP_SERVER`**: `smtp-mail.outlook.com` (or your organization's SMTP server)
- **`SMTP_PORT`**: `587` (standard TLS port)
- **`SMTP_USER`**: Your Outlook email address (e.g., `yourname@company.com`)
- **`SMTP_PASSWORD`**: Your Outlook password or app-specific password
- **`FROM_EMAIL`**: Your Outlook email address (usually same as SMTP_USER)

### How to Get SMTP Password:

If your organization uses two-factor authentication, you may need an **App Password**:

1. Go to your Microsoft Account security settings
2. Enable **App passwords** (if available)
3. Generate a new app password for "Mail"
4. Use this app password as `SMTP_PASSWORD`

**Note**: Some organizations restrict SMTP access. Contact your IT department if you encounter issues.

## Step 2: Update Repository Configuration

In `index.html`, update these constants at the top of the JavaScript section:

```javascript
const GITHUB_REPO = 'your-username/your-repo-name'; // Format: username/repo-name
const GITHUB_BRANCH = 'main'; // Your default branch name
```

## Step 3: Enable GitHub Actions

1. Go to your repository **Settings** → **Actions** → **General**
2. Under **Workflow permissions**, select **Read and write permissions**
3. Check **Allow GitHub Actions to create and approve pull requests**
4. Save changes

## Step 4: Test the Subscription Form

1. Open your GitHub Pages site (or run locally)
2. Navigate to the Newsletter page
3. Fill out the subscription form
4. Submit the form

**What happens:**
- A GitHub Issue is created with the subscription details
- The GitHub Action workflow processes the issue
- The subscriber is added to `subscribers.json`
- A confirmation email is sent to the subscriber
- The issue is automatically closed

## Step 5: Send Your First Newsletter

### Option A: Manual Send via GitHub Actions

1. Go to your repository on GitHub
2. Click **Actions** tab
3. Select **Send Newsletter** workflow
4. Click **Run workflow**
5. Fill in:
   - **Subject**: Your newsletter subject line
   - **HTML Content**: Paste your HTML newsletter content
   - **Preview only**: Set to `true` to preview first
6. Click **Run workflow**

### Option B: Scheduled Newsletter

The workflow is configured to run every Monday at 9 AM UTC. To customize:

1. Edit `.github/workflows/send-newsletter.yml`
2. Modify the `schedule` cron expression:
   ```yaml
   schedule:
     - cron: '0 9 * * 1'  # Monday 9 AM UTC
   ```
3. For different times, use [crontab.guru](https://crontab.guru/) to generate cron expressions

### Option C: Send from Command Line

If you have the repository cloned locally:

```bash
# Set environment variables
export SMTP_SERVER=smtp-mail.outlook.com
export SMTP_PORT=587
export SMTP_USER=your-email@company.com
export SMTP_PASSWORD=your-password
export FROM_EMAIL=your-email@company.com

# Create newsletter HTML file
cat > my_newsletter.html << EOF
<html>
<body>
  <h1>Hello {name}!</h1>
  <p>This is your newsletter content.</p>
</body>
</html>
EOF

# Send newsletter
python3 send_newsletter.py "My Newsletter Subject" my_newsletter.html
```

## Newsletter HTML Template

Use `{name}` placeholder for personalization. Example:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body { font-family: Arial, sans-serif; line-height: 1.6; }
    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
    .header { background: #0f766e; color: white; padding: 20px; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>Work Hub Newsletter</h1>
    </div>
    <div class="content">
      <p>Hi {name},</p>
      <p>Your newsletter content here...</p>
    </div>
  </div>
</body>
</html>
```

## Troubleshooting

### Form Submission Issues

**Problem**: Form submission fails with authentication error
- **Solution**: The form uses GitHub's public API. For private repos, you may need to use a GitHub Personal Access Token (not recommended for public sites)

**Problem**: Issue is created but not processed
- **Solution**: Check that the issue has the `newsletter-subscription` label. The workflow only processes issues with this label.

### Email Sending Issues

**Problem**: "SMTP authentication failed"
- **Solution**: 
  - Verify your email and password are correct
  - Check if your organization requires app-specific passwords
  - Contact IT to ensure SMTP access is enabled

**Problem**: "Connection refused" or "Connection timeout"
- **Solution**:
  - Verify SMTP_SERVER and SMTP_PORT are correct
  - Check if your organization's firewall blocks SMTP connections
  - Try using port 465 with SSL instead of 587 with TLS

**Problem**: Emails go to spam
- **Solution**:
  - Use a proper FROM_EMAIL address
  - Include unsubscribe links
  - Avoid spam trigger words
  - Consider using a dedicated email service for better deliverability

### GitHub Actions Issues

**Problem**: Workflow doesn't run
- **Solution**: 
  - Check that GitHub Actions is enabled in repository settings
  - Verify workflow files are in `.github/workflows/` directory
  - Check Actions tab for error messages

**Problem**: "Permission denied" errors
- **Solution**:
  - Go to Settings → Actions → General
  - Enable "Read and write permissions" for workflows
  - Ensure GITHUB_TOKEN has proper permissions

## Security Considerations

1. **Never commit secrets**: All sensitive data should be in GitHub Secrets
2. **App passwords**: Use app-specific passwords instead of your main password
3. **Rate limiting**: Be aware of SMTP rate limits to avoid being blocked
4. **GDPR compliance**: Ensure you have permission to store and email subscriber data

## Managing Subscribers

### View Subscribers

```bash
cat subscribers.json | python3 -m json.tool
```

### Remove a Subscriber

Edit `subscribers.json` and remove the subscriber entry, then commit:

```bash
# Edit subscribers.json to remove entry
git add subscribers.json
git commit -m "Remove subscriber"
git push
```

### Export Subscribers

```bash
python3 << EOF
import json
import csv

with open('subscribers.json') as f:
    subscribers = json.load(f)

with open('subscribers.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'email', 'department', 'weeklyDigest', 'subscribedAt'])
    writer.writeheader()
    writer.writerows(subscribers)

print(f"Exported {len(subscribers)} subscribers to subscribers.csv")
EOF
```

## Next Steps

1. Customize the newsletter HTML template
2. Set up a regular newsletter schedule
3. Add unsubscribe functionality (optional)
4. Consider adding email analytics (optional)

## Support

If you encounter issues:
1. Check GitHub Actions logs for detailed error messages
2. Verify all secrets are set correctly
3. Test SMTP connection manually using a Python script
4. Contact your IT department for SMTP configuration help
