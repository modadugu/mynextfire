# Setup Instructions for GitHub Pages

## Your GitHub Username: `modadugu`

## ⚠️ IMPORTANT: Choose One Option

### Option 1: User Site (Recommended) ✅

**Repository Name:** `modadugu.github.io`  
**Site URL:** `https://modadugu.github.io`

**Steps:**
1. Rename your repository:
   - Go to: `https://github.com/modadugu/mynextfireblog.github.io/settings`
   - Scroll to "Repository name"
   - Change to: `modadugu.github.io`
   - Click "Rename"

2. Enable GitHub Pages:
   - Settings → Pages
   - Source: Branch `main` (or `master`)
   - Folder: `/ (root)`
   - Save

3. Wait 2-5 minutes

4. Access: `https://modadugu.github.io`

**Current `_config.yml` is already set for this option!**

---

### Option 2: Project Site

**Repository Name:** `mynextfireblog.github.io` (keep current)  
**Site URL:** `https://modadugu.github.io/mynextfireblog/`

**Steps:**
1. Update `_config.yml`:
   - Change `baseurl: ""` to `baseurl: "/mynextfireblog"`

2. Enable GitHub Pages:
   - Settings → Pages
   - Source: Branch `main` (or `master`)
   - Folder: `/ (root)`
   - Save

3. Wait 2-5 minutes

4. Access: `https://modadugu.github.io/mynextfireblog/`

---

## After Setup

1. **Make sure repository is Public:**
   - Settings → General → Scroll to bottom
   - Must be "Public" for free accounts

2. **Check build status:**
   - Go to "Actions" tab
   - Should show successful build

3. **Test your site:**
   - Homepage: Your chosen URL above
   - Posts: `[your-url]/2025/03/02/pitch-perfect-crafting-your-business-pitch-with-ai.html`

## Which Option Should You Choose?

- **Option 1** if you want a clean URL: `modadugu.github.io`
- **Option 2** if you want to keep the current repository name

**Recommendation:** Choose Option 1 for a cleaner, simpler URL.

