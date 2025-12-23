# 🚀 Work-Hub GitHub Pages Setup Guide

## Overview

You've successfully created a modern, accessible dashboard homepage! This guide will help you get it live on GitHub Pages in minutes.

## ✅ What You Have

✅ Professional HTML5 homepage
✅ Modern, responsive CSS styling
✅ Interactive JavaScript features
✅ WCAG 2.2 Level AA accessibility
✅ Mobile-optimized design
✅ SEO-friendly structure

## 🗣 Prerequisites

Before you proceed, make sure you have:

1. **Git installed** - [Download here](https://git-scm.com/download/win)
2. **GitHub account** - [Create one here](https://github.com/signup)
3. **Access to your Work-Hub repository** at https://github.com/x0bi3/Work-Hub

### Installing Git on Windows

If you don't have git installed yet:

1. Visit https://git-scm.com/download/win
2. Download the installer
3. Run it and follow the default options
4. Restart your terminal/PowerShell
5. Verify with: `git --version`

## 💻 Step-by-Step Setup

### Step 1: Clone Your Repository

Open PowerShell or Command Prompt and run:

```powershell
cd C:\Users\r0b09wo\Documents
git clone https://github.com/x0bi3/Work-Hub.git
cd Work-Hub
```

### Step 2: Copy the Files

I've already created all files in `C:\Users\r0b09wo\Documents\Work-Hub\`. Now you need to copy them to the cloned repository:

**Option A: Using GUI**
- Open File Explorer
- Navigate to `C:\Users\r0b09wo\Documents\Work-Hub\`
- Select all files (Ctrl+A)
- Copy them (Ctrl+C)
- Go to the cloned repository folder
- Paste (Ctrl+V)

**Option B: Using PowerShell**

```powershell
# Copy all files
Copy-Item -Path "C:\Users\r0b09wo\Documents\Work-Hub\*" -Destination "C:\path\to\cloned\Work-Hub" -Recurse
```

### Step 3: Configure Git

If this is your first time using git:

```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 4: Stage and Commit Changes

```powershell
# Navigate to your repository
cd C:\path\to\cloned\Work-Hub

# Check what files changed
git status

# Stage all changes
git add .

# Commit with a message
git commit -m "Add professional homepage with accessibility features"
```

### Step 5: Push to GitHub

```powershell
git push origin main
```

You may be asked to authenticate. Follow GitHub's authentication prompt.

### Step 6: Enable GitHub Pages

1. Go to https://github.com/x0bi3/Work-Hub
2. Click **Settings** (in the top right)
3. Scroll down to **Pages** section on the left sidebar
4. Under "Build and deployment":
   - **Source**: Select `Deploy from a branch`
   - **Branch**: Select `main`
   - **Folder**: Select `/ (root)`
5. Click **Save**

### Step 7: View Your Site

Wait 1-2 minutes for GitHub to build your site, then visit:

```
https://x0bi3.github.io/Work-Hub/
```

Your beautiful dashboard homepage is now live! 🌟

## 🎨 Customization Tips

### Change Colors

Edit `styles.css` and look for the `:root` section:

```css
:root {
    --primary-color: #0f766e;      /* Change this! */
    --primary-dark: #0d5850;
    --primary-light: #14b8a6;
    /* ... */
}
```

Some great color tools:
- https://coolors.co
- https://color.adobe.com
- https://colormind.io

### Update Content

Edit `index.html` to:
- Change the hero title and description
- Update feature descriptions
- Modify the statistics
- Add your contact information

### Add Navigation Links

Update the navbar links in `index.html`:

```html
<ul class="nav-links">
    <li><a href="#features">Features</a></li>
    <li><a href="#about">About</a></li>
    <!-- Add your own links! -->
</ul>
```

### Custom Domain (Optional)

If you want to use a custom domain like `work-hub.com`:

1. Go to repository **Settings** → **Pages**
2. Under "Custom domain", enter your domain
3. Update your domain's DNS settings (check your domain provider)

## 📱 Mobile Testing

Before publishing changes:

1. Open Chrome DevTools (F12)
2. Click the mobile device icon (or Ctrl+Shift+M)
3. Test on different screen sizes
4. Verify all buttons and forms work

## 🔚 Version Control Best Practices

### Making Changes

Always follow this workflow:

```powershell
# 1. Create a feature branch
git checkout -b feature/my-changes

# 2. Make your edits
# (Edit files in your editor)

# 3. Check what changed
git status

# 4. Stage changes
git add .

# 5. Commit with clear message
git commit -m "Update feature section with new details"

# 6. Push to GitHub
git push origin feature/my-changes

# 7. Go to GitHub and create a Pull Request
# (optional, but good practice)

# 8. Merge to main
# (Either via GitHub UI or locally with git merge)
```

### Useful Git Commands

```powershell
# See commit history
git log

# See changes since last commit
git diff

# Undo uncommitted changes
git checkout .

# Remove a file from staging
git reset filename

# See branches
git branch -a

# Switch branches
git checkout branch-name
```

## 🚠 Troubleshooting

### Site not showing up

- Wait 2-3 minutes after pushing
- Clear your browser cache (Ctrl+Shift+Delete)
- Check GitHub Actions tab to see if build succeeded
- Verify `.gitignore` isn't excluding your files

### 404 Error on subpages

- GitHub Pages requires URLs to match your folder structure
- For root level pages: `https://x0bi3.github.io/Work-Hub/page.html`
- Make sure HTML files are in the root or in correct folders

### Changes not appearing

```powershell
# Hard refresh your browser
# Windows: Ctrl+Shift+R
# Mac: Cmd+Shift+R

# Or use an incognito window
```

### Git push authentication error

- Use GitHub's Personal Access Token instead of password
- See: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens

## 🔗 Useful Resources

- GitHub Pages Documentation: https://docs.github.com/en/pages
- Git Tutorial: https://git-scm.com/book/en/v2
- HTML Best Practices: https://www.w3.org/TR/html-design-principles/
- CSS Reference: https://developer.mozilla.org/en-US/docs/Web/CSS
- Accessibility Guide: https://www.w3.org/WAI/WCAG22/quickref/

## 🚀 Next Steps

1. **Customize the content** - Make it your own!
2. **Add a favicon** - Create `favicon.ico` in the root
3. **Set up analytics** - Add Google Analytics or Plausible
4. **Add more pages** - Create additional HTML files
5. **Set up CI/CD** - Use GitHub Actions for automated deployments

## 🙨 Need Help?

- Check GitHub Issues: https://github.com/x0bi3/Work-Hub/issues
- GitHub Community: https://github.community
- Stack Overflow: https://stackoverflow.com/questions/tagged/github-pages

---

**Happy deploying!** 🚀🈟
