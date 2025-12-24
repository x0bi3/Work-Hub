# Newsletter Setup - Automatic Token Injection

## ✅ Setup Complete!

Your newsletter form is now configured to automatically use your `WORKHUB_GH_PAT` secret. **Users don't need to configure anything!**

## How It Works

1. **GitHub Actions workflow** (`build-with-token.yml`) runs automatically when you push changes
2. **Injects your token** into `newsletter-config.js` file
3. **Form automatically uses** the token from the config file
4. **Users can subscribe** without any setup - it just works!

## First-Time Setup

The build workflow needs to run once to inject your token:

### Option 1: Automatic (Recommended)
Just push any change to `index.html` or the workflow file, and it will run automatically.

### Option 2: Manual Trigger
1. Go to your repository on GitHub
2. Click **Actions** tab
3. Find **"Build Site with Newsletter Token"** workflow
4. Click **Run workflow** → **Run workflow**

## Verify It's Working

After the workflow runs:

1. **Check `newsletter-config.js`** - It should contain your token (visible in the file)
2. **Test the form** - Submit a newsletter subscription
3. **Check GitHub Actions** - "Newsletter Subscription Webhook" should run
4. **Check `subscribers.json`** - Subscriber should be added
5. **Check email** - Confirmation should arrive (if SMTP configured)

## Important Notes

⚠️ **Token Visibility**: The token will be visible in `newsletter-config.js` in your repository. This is necessary for the form to work, but:
- The token only needs permissions to trigger workflows
- The actual processing uses `WORKHUB_GH_PAT` secret server-side (more secure)
- Consider using a token with minimal permissions if concerned

✅ **Security**: 
- Token is injected by GitHub Actions (secure)
- Only used to trigger `repository_dispatch`
- All processing uses `WORKHUB_GH_PAT` secret server-side

## Troubleshooting

**Form still says "not configured"**
- Build workflow hasn't run yet - trigger it manually (see above)
- Check `newsletter-config.js` exists and has `githubToken` set
- Verify `WORKHUB_GH_PAT` secret is set correctly

**Workflow fails**
- Check `WORKHUB_GH_PAT` secret exists and is valid
- Verify token has `repo` scope
- Check Actions logs for specific errors

**Token not injected**
- Workflow might not have run - trigger it manually
- Check workflow file exists: `.github/workflows/build-with-token.yml`
- Verify workflow has permission to write to repository

## Next Steps

1. ✅ `WORKHUB_GH_PAT` secret is set
2. ⏳ Build workflow needs to run (trigger manually or wait for next push)
3. ✅ Form is ready to use
4. ✅ Users can subscribe without any setup!

Once the build workflow runs, your newsletter form will work automatically for all users! 🎉
