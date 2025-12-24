# Quick Setup: Using Your GitHub Personal Access Token

You have a PAT! Here's how to use it with the newsletter form.

## Method 1: Quick Test (Browser Console) ⚡

**Fastest way to test, but token is visible in browser:**

1. **Open your website** (GitHub Pages or locally)

2. **Open Browser Console:**
   - Press `F12` (or `Cmd+Option+I` on Mac)
   - Click the "Console" tab

3. **Set your token:**
   ```javascript
   localStorage.setItem('github_token', 'YOUR_PAT_HERE');
   ```
   Replace `YOUR_PAT_HERE` with your actual Personal Access Token.

4. **Verify it's set:**
   ```javascript
   localStorage.getItem('github_token');
   ```
   Should show your token.

5. **Test the form** - Submit a newsletter subscription and it should work!

**⚠️ Note:** This stores the token in your browser's localStorage. Anyone with access to your browser can see it. This is fine for testing, but not for production.

---

## Method 2: Add Token to HTML (For Testing Only) ⚠️

**Quick but insecure - only use for testing:**

1. **Edit `index.html`**

2. **Find this section** (around line 736):
   ```javascript
   const GITHUB_REPO = 'x0bi3/Work-Hub';
   const GITHUB_BRANCH = 'main';
   ```

3. **Add your token right after:**
   ```javascript
   const GITHUB_REPO = 'x0bi3/Work-Hub';
   const GITHUB_BRANCH = 'main';
   const GITHUB_TOKEN = 'YOUR_PAT_HERE'; // ⚠️ TEMPORARY - Remove before committing!
   ```

4. **Update the form code** to use this token. Find the `handleNewsletterSignup` function (around line 1030) and change:
   ```javascript
   // Change this line:
   const githubToken = localStorage.getItem('github_token') || '';
   
   // To this:
   const githubToken = GITHUB_TOKEN || localStorage.getItem('github_token') || '';
   ```

5. **⚠️ IMPORTANT:** Remove the token before committing to GitHub!

---

## Method 3: Secure Production Setup (Recommended) 🔒

**Best for production - token stays secure:**

### Option A: Use GitHub Secrets + Build Process

1. **Add token as GitHub Secret:**
   - Go to: Repository → Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `GITHUB_TOKEN_FOR_SUBSCRIPTIONS`
   - Value: Your PAT
   - Click "Add secret"

2. **Create a build workflow** that injects the token at build time (see below)

### Option B: Use GitHub Actions Webhook

Create a backend endpoint using GitHub Actions that uses the secret token server-side.

---

## Method 4: Environment Variable (For Local Development)

If running locally with a server:

1. **Set environment variable:**
   ```bash
   export GITHUB_TOKEN=your_pat_here
   ```

2. **Update your build process** to inject it into the HTML

---

## Quick Test Script

Create a file `set-token.html` (for testing only):

```html
<!DOCTYPE html>
<html>
<head>
    <title>Set GitHub Token</title>
</head>
<body>
    <h1>Set GitHub Token for Newsletter</h1>
    <input type="password" id="token" placeholder="Paste your GitHub PAT">
    <button onclick="setToken()">Set Token</button>
    <p id="status"></p>
    
    <script>
        function setToken() {
            const token = document.getElementById('token').value;
            if (token) {
                localStorage.setItem('github_token', token);
                document.getElementById('status').textContent = '✅ Token set! You can now use the newsletter form.';
            }
        }
        
        // Check if token is already set
        if (localStorage.getItem('github_token')) {
            document.getElementById('status').textContent = '✅ Token is already set.';
        }
    </script>
</body>
</html>
```

Open this file, paste your token, click "Set Token", then use the newsletter form.

---

## Verify It's Working

1. **Set your token** using Method 1 or 2 above

2. **Open browser console** and check:
   ```javascript
   localStorage.getItem('github_token')
   ```
   Should show your token (or `null` if not set)

3. **Submit the newsletter form**

4. **Check GitHub Issues** - A new issue should be created with label `newsletter-subscription`

5. **Check GitHub Actions** - The workflow should process it automatically

6. **Check `subscribers.json`** - Subscriber should be added

7. **Check email** - Confirmation should arrive

---

## Troubleshooting

**Token not working?**
- Verify token has `repo` scope (or `public_repo` for public repos)
- Check token hasn't expired
- Make sure token is correctly set: `localStorage.getItem('github_token')`

**Still getting 401 error?**
- Token might be invalid or expired
- Token might not have correct permissions
- Try creating a new token

**Form works but no email?**
- Check GitHub Secrets are configured (SMTP settings)
- Check GitHub Actions logs for email errors
- Verify Outlook SMTP credentials are correct

---

## Security Best Practices

1. ✅ **Never commit tokens to Git**
2. ✅ **Use GitHub Secrets for production**
3. ✅ **Rotate tokens regularly**
4. ✅ **Use minimal token permissions** (only `repo` scope needed)
5. ✅ **Remove tokens from localStorage when done testing**

---

## Next Steps

Once you've tested with localStorage:
1. Set up GitHub Secrets (Method 3)
2. Create a secure build process
3. Remove any hardcoded tokens from code
4. Deploy with secure token handling
