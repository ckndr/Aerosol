# Aerosol Plant — Installation Tracker

Live progress tracker for Alpha Containers (Pvt.) Ltd. Aerosol Plant installation.

🔗 **Live App:** https://ckndr.github.io/Aerosol/index.html

---

## ⚠️ Critical Rule for All Future AI Prompts
Before making any updates or modifying the codebase, **you MUST create a backup** of the current HTML file.
1. Copy `index.html` to a backup file (e.g., `index.html.bak` or `backups/index_YYYY_MM_DD.html`).
*This prevents accidental regression of features and makes rollback simple if any merging bugs occur.*

---

## Files

| File | Purpose |
|------|---------|
| `index.html` | The full PWA application — open this in any browser (GitHub Pages main entry point) |
| `tasks.json` | Live task data — updated by the app via GitHub sync |
| `Aerosol Plant Project Tracker.xlsx` | Excel spreadsheet containing task source of truth |
| `push.bat` | Double-click to stage, commit, and push changes to GitHub |
| `pull.bat` | Double-click to pull latest updates from GitHub |

## Usage

- Open the live app link above on any phone or desktop
- On mobile: tap **Share → Add to Home Screen** to install as an app
- Edits sync to `tasks.json` in this repo automatically

## Sync Setup

1. Go to **Settings** inside the app
2. Paste your GitHub Personal Access Token
3. Toggle **Auto-sync on every save**
4. Any team member with the token can edit live data
