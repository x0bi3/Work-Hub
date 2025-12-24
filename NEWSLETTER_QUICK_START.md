# Newsletter Quick Start Guide

## What Was Created

Your newsletter system is now set up with the following components:

### Files Created:
1. **`index.html`** - Updated with newsletter subscription form
2. **`subscribers.json`** - Stores all subscriber data (starts empty)
3. **`.github/workflows/process-subscription.yml`** - Processes new subscriptions automatically
4. **`.github/workflows/send-newsletter.yml`** - Sends newsletters to all subscribers
5. **`send_newsletter.py`** - Python script for sending emails via Outlook SMTP
6. **`test_email.py`** - Test script to verify SMTP configuration
7. **`newsletter_template.html`** - Sample newsletter HTML template

## Quick Setup (5 Steps)

### 1. Configure GitHub Secrets
Go to: **Repository Settings → Secrets and variables → Actions**

Add these secrets:
- `SMTP_SERVER` = `smtp-mail.outlook.com`
- `SMTP_PORT` = `587`
- `SMTP_USER` = `your-email@company.com`
- `SMTP_PASSWORD` = `your-password-or-app-password`
- `FROM_EMAIL` = `your-email@company.com`

### 2. Update Repository Name in HTML
In `index.html`, find this line (around line 200):
```javascript
const GITHUB_REPO = 'x0bi3/Work-Hub'; // Change to your username/repo
```

### 3. Enable GitHub Actions Permissions
Go to: **Repository Settings → Actions → General**
- Enable "Read and write permissions"
- Save changes

### 4. Test SMTP Connection (Optional but Recommended)
```bash
export SMTP_USER=your-email@company.com
export SMTP_PASSWORD=your-password
python3 test_email.py
```

### 5. Test the Subscription Form
1. Open your site (GitHub Pages or locally)
2. Go to Newsletter page
3. Fill out and submit the form
4. Check GitHub Issues - a new issue should be created
5. Check Actions tab - workflow should process it
6. Check `subscribers.json` - subscriber should be added
7. Check email - confirmation should arrive

## How It Works

### Subscription Flow:
1. User fills out form on website
2. Form creates GitHub Issue via API
3. GitHub Action detects new issue with `newsletter-subscription` label
4. Action extracts subscriber data and adds to `subscribers.json`
5. Confirmation email sent to subscriber
6. Issue automatically closed

### Sending Newsletters:
1. Go to **Actions** → **Send Newsletter** → **Run workflow**
2. Enter subject and HTML content
3. Click "Run workflow"
4. Newsletter sent to all subscribers in `subscribers.json`

## Sending Your First Newsletter

### Method 1: Via GitHub Actions (Recommended)
1. Go to **Actions** tab
2. Click **Send Newsletter** workflow
3. Click **Run workflow**
4. Fill in:
   - Subject: "Welcome to Work Hub Newsletter"
   - HTML Content: Copy/paste from `newsletter_template.html`
   - Preview only: `false`
5. Click **Run workflow**

### Method 2: Via Command Line
```bash
# Set environment variables
export SMTP_SERVER=smtp-mail.outlook.com
export SMTP_PORT=587
export SMTP_USER=your-email@company.com
export SMTP_PASSWORD=your-password
export FROM_EMAIL=your-email@company.com

# Send newsletter
python3 send_newsletter.py "My Newsletter" newsletter_template.html
```

## Newsletter Template Tips

- Use `{name}` placeholder for personalization
- Keep HTML simple and test in email clients
- Include unsubscribe information
- Use inline CSS (email clients strip `<style>` tags)
- Test with preview option first

## Troubleshooting

**Form doesn't submit?**
- Check browser console for errors
- Verify `GITHUB_REPO` constant is correct
- Ensure repository is public (or use GitHub token)

**Emails not sending?**
- Verify all secrets are set correctly
- Test SMTP with `test_email.py`
- Check GitHub Actions logs for errors
- Contact IT if SMTP is blocked

**Workflow not running?**
- Check Actions tab for errors
- Verify workflow files are in `.github/workflows/`
- Ensure Actions are enabled in repository settings

## Next Steps

1. ✅ Set up GitHub Secrets
2. ✅ Test subscription form
3. ✅ Customize newsletter template
4. ✅ Send your first newsletter
5. 📅 Set up scheduled newsletters (optional)

For detailed documentation, see `NEWSLETTER_SETUP.md`
