# Setup Public Token for Newsletter Form

The form needs a GitHub token to create issues. Since we can't use secrets client-side, we need a **public token** with minimal permissions.

## Step 1: Create a Minimal Permission Token

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token (classic)"**
3. Name: **"Newsletter Form Token"**
4. **Select ONLY this scope:**
   - ✅ `public_repo` (if repo is public) OR `repo` (if private)
   - ❌ **DO NOT** select any other scopes
5. Click **"Generate token"**
6. **Copy the token immediately** (starts with `ghp_`)

## Step 2: Add Token to index.html

1. Open `index.html`
2. Find this line (around line 1045):
   ```javascript
   const PUBLIC_FORM_TOKEN = ''; // Set this to a minimal-permission token if needed
   ```
3. Replace with:
   ```javascript
   const PUBLIC_FORM_TOKEN = 'ghp_your_token_here';
   ```
4. Save and commit

## Step 3: Test

1. Submit the newsletter form
2. Check browser console - should see success message
3. Check GitHub Issues - new issue should be created
4. Check GitHub Actions - workflow should process it

## Security Notes

✅ **Safe to expose**: This token only has permission to create issues  
✅ **Minimal permissions**: Can't access sensitive data  
✅ **Can be revoked**: If compromised, just revoke and create new one  
⚠️ **Visible in code**: Token will be in your repository (but that's okay with minimal permissions)

## Alternative: Use GitHub App (More Secure)

For better security, you could create a GitHub App with issue creation permissions, but that's more complex. The public token approach is fine for most use cases.
