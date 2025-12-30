# Newsletter Authentication Setup

The newsletter form is fully automated and requires no user configuration. All authentication is handled server-side using GitHub Actions.

## How It Works

1. **User submits form** (name and email only)
2. **Form triggers GitHub Action** via `repository_dispatch` API
3. **GitHub Action uses WORKHUB_GH_PAT secret** to:
   - Create a GitHub issue for the subscription
   - Add subscriber to `subscribers.json`
   - Send confirmation email

## Configuration

### Required GitHub Secret

The workflow uses the `WORKHUB_GH_PAT` secret stored in GitHub repository settings:

1. Go to: Repository → Settings → Secrets and variables → Actions
2. Ensure `WORKHUB_GH_PAT` is set with your Personal Access Token
3. Token needs `repo` scope (or `public_repo` for public repos)

### Token in Code

The form uses a hardcoded token to trigger the `repository_dispatch` API. This token:
- Only needs permission to trigger workflows (`repo` scope)
- Cannot access sensitive repository data
- Is used only to trigger the GitHub Action

**Note:** The same token is used both client-side (to trigger) and server-side (via WORKHUB_GH_PAT secret) for simplicity. For enhanced security, you could use separate tokens.

## Workflow

The `handle-newsletter-form.yml` workflow:
1. Receives subscription data via `repository_dispatch`
2. Creates a GitHub issue using `WORKHUB_GH_PAT`
3. Adds subscriber to `subscribers.json`
4. Commits the update
5. Sends confirmation email (if SMTP secrets are configured)

## User Experience

Users simply:
1. Enter their name
2. Enter their email
3. Click "Subscribe Now"

No configuration, tokens, or setup required on their end.

## Troubleshooting

**Form submission fails:**
- Check that the token in `index.html` is valid
- Verify `WORKHUB_GH_PAT` secret is set in repository settings
- Check GitHub Actions logs for errors

**No confirmation email:**
- Verify SMTP secrets are configured (SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, FROM_EMAIL)
- Check GitHub Actions logs for email errors

**Subscriber not added:**
- Check GitHub Actions workflow logs
- Verify `subscribers.json` file exists and is writable
- Check for commit permissions
