# GitHub Pages Setup Guide

## Step-by-Step Settings on GitHub Portal

### 1. Enable GitHub Pages

1. Go to your repository: `https://github.com/mynextfireblog/mynextfireblog.github.io`
2. Click on **Settings** (top menu)
3. Scroll down to **Pages** in the left sidebar
4. Under **Source**, select:
   - **Branch**: `main` (or `master` if that's your default branch)
   - **Folder**: `/ (root)`
5. Click **Save**

### 2. Repository Visibility

**Important**: For `username.github.io` repositories:
- The repository **MUST be public** (free GitHub accounts)
- OR you need GitHub Pro/Team for private repos with Pages

To check/make it public:
1. Go to **Settings** → **General**
2. Scroll to **Danger Zone**
3. If it says "Change repository visibility", make sure it's set to **Public**

### 3. Wait for Build

After enabling Pages:
- Wait 1-2 minutes for the first build
- You'll see a yellow banner: "Your site is ready to be published"
- Once built, it turns green: "Your site is published at..."

### 4. Check Build Status

1. Go to **Actions** tab in your repository
2. Look for "Pages build and deployment" workflow
3. If it fails, click to see error details

### 5. Access Your Site

Once published, your site will be available at:
- `https://mynextfireblog.github.io`

**Note**: It may take up to 10 minutes for DNS to propagate after first setup.

## Troubleshooting 404 Errors

### If you still get 404:

1. **Check the branch name**: Make sure you're using `main` or `master` (whichever is your default)
2. **Check repository name**: Must be exactly `mynextfireblog.github.io` (case-sensitive)
3. **Wait longer**: First build can take 5-10 minutes
4. **Check Actions tab**: Look for build errors
5. **Try accessing**: `https://mynextfireblog.github.io/index.html` directly

## Common Issues

### Issue: "Build failed" in Actions
- Check the error message
- Common fix: Update `_config.yml` plugins (see below)

### Issue: Site loads but shows 404 for posts
- Check that `_posts` folder exists
- Verify post filenames follow `YYYY-MM-DD-title.md` format
- Check `_config.yml` permalink setting

