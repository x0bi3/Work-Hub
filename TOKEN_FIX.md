# Fix Invalid Credentials Error

Your GitHub token is invalid or expired. Here's how to fix it:

## Quick Fix Steps

### 1. Create a New GitHub Personal Access Token

1. Go to: **https://github.com/settings/tokens**
2. Click **"Generate new token (classic)"**
3. Give it a name: **"Newsletter Form Token"**
4. Set expiration (recommended: 90 days or custom)
5. **Select ONLY this scope:**
   - ✅ `repo` (for private repos) OR `public_repo` (for public repos)
   - ❌ Do NOT select other scopes
6. Click **"Generate token"**
7. **COPY THE TOKEN IMMEDIATELY** (starts with `ghp_`) - you won't see it again!

### 2. Set the Token

**Option A: Using Browser Console (Recommended for Testing)**

1. Open your website
2. Press `F12` (or `Cmd+Option+I` on Mac) to open Developer Tools
3. Click the **"Console"** tab
4. Run this command (replace `YOUR_NEW_TOKEN` with your actual token):
   ```javascript
   localStorage.setItem('github_token', 'YOUR_NEW_TOKEN');
   ```
5. Verify it's set:
   ```javascript
   localStorage.getItem('github_token');
   ```
   Should show your token.

6. **Test it:**
   - Open `test-token.html` in your browser
   - Click "Test Token"
   - Should see ✅ Success message

**Option B: Update Code Directly (For Testing Only)**

1. Open `index.html`
2. Find line ~1036:
   ```javascript
   const PUBLIC_FORM_TOKEN = localStorage.getItem('github_token') || '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';
   ```
3. Replace the hardcoded token with your new one:
   ```javascript
   const PUBLIC_FORM_TOKEN = localStorage.getItem('github_token') || 'YOUR_NEW_TOKEN_HERE';
   ```
4. **⚠️ WARNING:** This exposes the token in your code. Remove it before committing!

### 3. Test the Token

1. Open `test-token.html` in your browser
2. Click **"Test Token"**
3. You should see:
   - ✅ Authenticated as: [your-username]
   - ✅ Success! Issue #[number] created!

If you see errors, check the troubleshooting section below.

## Troubleshooting

### ❌ "Bad credentials" (401 Error)

**Cause:** Token is invalid, expired, or revoked

**Fix:**
1. Create a new token (see Step 1 above)
2. Make sure you copied the entire token (starts with `ghp_` and is about 40+ characters)
3. Set it again using Option A or B above

### ❌ "Resource not accessible by integration" (403 Error)

**Cause:** Token doesn't have the right permissions

**Fix:**
1. Create a new token
2. Make sure you selected `repo` scope (or `public_repo` for public repos)
3. The token needs permission to create issues

### ❌ "Not Found" (404 Error)

**Cause:** Repository name is wrong or token doesn't have access

**Fix:**
1. Check `GITHUB_REPO` in `index.html` (line ~736)
2. Format should be: `username/repo-name`
3. Make sure the token has access to this repository

### ❌ Token works but form still fails

**Possible causes:**
1. Token not set in localStorage - use Option A above
2. Browser cache - try hard refresh (Ctrl+F5 or Cmd+Shift+R)
3. Token expired - create a new one

## Security Best Practices

1. ✅ **Use localStorage** (Option A) instead of hardcoding tokens
2. ✅ **Never commit tokens** to Git
3. ✅ **Rotate tokens regularly** (every 90 days)
4. ✅ **Use minimal permissions** (only `repo` or `public_repo`)
5. ✅ **Revoke old tokens** after creating new ones

## Production Setup (More Secure)

For production, consider:
- Using GitHub Actions with secrets (server-side)
- Using a GitHub App instead of Personal Access Token
- Using a backend service to handle form submissions

See `AUTH_SETUP.md` for more options.

## Verify Everything Works

After setting your token:

1. ✅ Test token: Open `test-token.html` → Click "Test Token" → Should succeed
2. ✅ Test form: Submit newsletter form → Should create GitHub issue
3. ✅ Check GitHub: Go to Issues → Should see new subscription issue
4. ✅ Check Actions: Go to Actions → Should see workflow processing

## Still Having Issues?

1. Check browser console for detailed error messages
2. Verify token format: Should start with `ghp_` and be 40+ characters
3. Test token directly: Use `test-token.html` to isolate the issue
4. Check GitHub token page: Make sure token is still active (not revoked)
