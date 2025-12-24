# Authentication Setup for Newsletter Form

The newsletter subscription form needs authentication to create GitHub Issues. Since we can't expose tokens in client-side code, here are your options:

## Option 1: Use GitHub Personal Access Token (Recommended for Testing)

### Step 1: Create a GitHub Personal Access Token

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name like "Newsletter Form Token"
4. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `public_repo` (if your repo is public)
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again!)

### Step 2: Add Token to GitHub Secrets

1. Go to your repository → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `GITHUB_TOKEN_FOR_SUBSCRIPTIONS`
4. Value: Paste your token
5. Click "Add secret"

### Step 3: Update the Form (Temporary Solution)

**⚠️ WARNING: This exposes the token in client-side code. Only use for testing or private repos!**

In `index.html`, find the `handleNewsletterSignup` function and add:

```javascript
// TEMPORARY: For testing only - token will be visible in client code
const GITHUB_TOKEN = 'your-token-here'; // Replace with your token

// Then in the fetch call, add:
headers: {
    'Accept': 'application/vnd.github.v3+json',
    'Authorization': `token ${GITHUB_TOKEN}`, // Add this line
    'Content-Type': 'application/json'
}
```

**⚠️ This is NOT secure for production!** Anyone can see the token in the page source.

## Option 2: Use GitHub Actions Webhook (Recommended for Production)

Create a backend endpoint that uses the token server-side. Since you're limited to GitHub, you can:

### Use GitHub Actions with `repository_dispatch`

1. The workflow is already set up to handle `repository_dispatch` events
2. Create a GitHub Personal Access Token (same as Option 1, Step 1)
3. Store it as `GITHUB_TOKEN_FOR_SUBSCRIPTIONS` secret
4. Update the form to call the GitHub API with the token:

```javascript
const response = await fetch(`https://api.github.com/repos/${GITHUB_REPO}/dispatches`, {
    method: 'POST',
    headers: {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': `token ${GITHUB_TOKEN}`, // From secure source
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        event_type: 'newsletter-subscription',
        client_payload: {
            subscriber: formData
        }
    })
});
```

## Option 3: Use a Form Submission Service (If Allowed)

If your organization allows it, you can use services like:
- **Formspree** - Free tier available, integrates with GitHub
- **Netlify Forms** - If hosting on Netlify
- **Google Forms** - Can export to CSV, then process with GitHub Actions

## Option 4: Manual Processing (Simplest, No Auth Needed)

1. Users submit the form
2. Form data is stored in browser localStorage
3. You manually check localStorage and process subscriptions
4. Or create a GitHub Action that runs on schedule to check for submissions

### Implementation:

The form already stores submissions in localStorage. You can:

1. Check localStorage in browser console:
```javascript
JSON.parse(localStorage.getItem('pendingNewsletterSubscriptions'))
```

2. Or create a GitHub Action that processes them (see `process-pending-subscriptions.yml`)

## Option 5: Use GitHub Discussions (If Enabled)

If your repository has Discussions enabled:

1. Create a GitHub Personal Access Token
2. Use the Discussions API instead of Issues API
3. Discussions might have different auth requirements

## Recommended Approach

For **testing/development**: Use Option 1 (temporary token in code)

For **production**: 
- Use Option 2 (GitHub Actions webhook)
- Or Option 4 (manual processing)
- Or use a form submission service

## Security Notes

- ⚠️ **Never commit tokens to your repository**
- ⚠️ **Never expose tokens in client-side JavaScript**
- ✅ **Always use GitHub Secrets for tokens**
- ✅ **Use minimal token permissions (only what's needed)**
- ✅ **Rotate tokens regularly**

## Quick Test

After setting up authentication, test the form:

1. Fill out the newsletter subscription form
2. Submit it
3. Check GitHub Issues - a new issue should be created
4. Check GitHub Actions - workflow should process it
5. Check `subscribers.json` - subscriber should be added
6. Check email - confirmation should arrive

## Troubleshooting

**401 Unauthorized**: Token is missing or invalid
- Verify token is correct
- Check token has correct scopes
- Ensure token hasn't expired

**403 Forbidden**: Token doesn't have required permissions
- Add `repo` scope to token
- For public repos, add `public_repo` scope

**404 Not Found**: Repository name is incorrect
- Verify `GITHUB_REPO` constant in `index.html`
- Format should be: `username/repo-name`
