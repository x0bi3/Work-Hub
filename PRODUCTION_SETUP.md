# Production Setup with GitHub Secret (WORKHUB_GH_PAT)

You've set up the GitHub Secret `WORKHUB_GH_PAT`. Here's how the secure flow works:

## How It Works

1. **User submits form** → Form calls GitHub API with a token (from localStorage)
2. **Triggers `repository_dispatch`** → This requires a token with `repo` scope
3. **GitHub Actions workflow runs** → Uses `WORKHUB_GH_PAT` secret server-side (secure!)
4. **Processes subscription** → Adds to `subscribers.json`, sends email
5. **All done securely** → Token never exposed in client code

## Setup Steps

### Step 1: GitHub Secret is Already Set ✅
- Secret name: `WORKHUB_GH_PAT`
- Value: Your Personal Access Token
- Location: Repository → Settings → Secrets and variables → Actions

### Step 2: Set Token in Browser (For Form Submission)

The form needs a token to **trigger** the workflow, but the actual **processing** uses your secret.

**Option A: Use Your PAT (Quick Test)**
```javascript
// In browser console:
localStorage.setItem('github_token', 'YOUR_PAT_HERE');
```

**Option B: Create a Public Token (Recommended for Production)**

Create a separate token with minimal permissions:
1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Name: "Newsletter Form Trigger"
4. **Scopes needed:**
   - ✅ `public_repo` (if repo is public) OR `repo` (if private)
   - ✅ `workflow` (to trigger workflows)
5. Copy the token
6. Set in browser: `localStorage.setItem('github_token', 'NEW_TOKEN')`

**Why two tokens?**
- **Browser token**: Only needs to trigger workflows (minimal permissions)
- **WORKHUB_GH_PAT secret**: Has full permissions for processing (stays secure server-side)

### Step 3: Test the Flow

1. **Set token in browser console:**
   ```javascript
   localStorage.setItem('github_token', 'YOUR_TOKEN');
   ```

2. **Submit the newsletter form**

3. **Check GitHub Actions:**
   - Go to Actions tab
   - You should see "Newsletter Subscription Webhook" workflow running
   - It uses `WORKHUB_GH_PAT` secret (not visible in logs)

4. **Verify results:**
   - Check `subscribers.json` - subscriber should be added
   - Check email - confirmation should arrive

## Security Benefits

✅ **WORKHUB_GH_PAT secret**: Never exposed, only used server-side  
✅ **Browser token**: Can have minimal permissions (just trigger workflows)  
✅ **Processing**: All done securely in GitHub Actions  
✅ **No tokens in code**: Everything uses secrets/localStorage

## Workflow Details

### `webhook-subscription.yml`
- Triggered by: `repository_dispatch` event
- Uses: `WORKHUB_GH_PAT` secret for all operations
- Does: Adds subscriber, commits to repo, sends email

### `process-subscription.yml`
- Triggered by: GitHub Issues OR `repository_dispatch`
- Uses: `WORKHUB_GH_PAT` secret
- Does: Same processing, alternative trigger method

## Troubleshooting

**Form says "authentication required"**
- Set token: `localStorage.setItem('github_token', 'YOUR_TOKEN')`
- Verify: `localStorage.getItem('github_token')`

**Workflow not running**
- Check Actions tab for errors
- Verify `WORKHUB_GH_PAT` secret is set correctly
- Check workflow file exists: `.github/workflows/webhook-subscription.yml`

**401/403 errors**
- Token needs `repo` scope (or `public_repo` for public repos)
- Token needs `workflow` scope to trigger workflows
- Verify token hasn't expired

**Subscriber not added**
- Check GitHub Actions logs
- Verify `WORKHUB_GH_PAT` has write permissions
- Check `subscribers.json` file exists

## Production Recommendations

1. **Use a separate token** for browser (minimal permissions)
2. **Rotate tokens regularly** (every 90 days)
3. **Monitor Actions logs** for any issues
4. **Keep WORKHUB_GH_PAT secret** secure (never commit it)
5. **Consider rate limits** (GitHub API has limits)

## Alternative: Fully Automated (No Browser Token)

If you want to eliminate the browser token requirement entirely:

1. **Create a public token** with minimal permissions
2. **Inject it at build time** via GitHub Actions
3. **Store in a config file** (still visible, but only to trigger workflows)
4. **Use WORKHUB_GH_PAT** for all actual processing

This requires modifying the build workflow to inject the token. Let me know if you want this approach!

## Current Status

✅ GitHub Secret configured: `WORKHUB_GH_PAT`  
✅ Workflows updated to use secret  
✅ Form updated to use `repository_dispatch`  
⏳ Browser token needed: Set via `localStorage.setItem('github_token', 'TOKEN')`

Once you set the browser token, everything will work securely!
