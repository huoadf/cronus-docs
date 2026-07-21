# Cronus Zen GPC Scripting Documentation

This repository contains the complete documentation for GPC scripting on the Cronus Zen device. It is built as a lightweight, clean, self-contained static site optimized for hosting on **GitHub Pages** or viewing locally.

## Features

- **Portability**: All assets and links use relative paths, meaning the site works perfectly locally (just double-click `index.html`), on a custom domain, or inside a subdirectory on GitHub Pages (e.g. `https://username.github.io/cronus-docs/`).
- **Markdown-Driven**: The page contents are stored in clean Markdown files inside the `src/` directory.
- **Search (⌘K)**: A fast client-side fuzzy search over all page content and headers.
- **Syntax Highlighting**: Beautiful code syntax highlighting for GPC/C, JSON, CSS, and HTML via Highlight.js.
- **Dark/Light Mode**: Smooth theme toggling that persists across page loads.
- **Aesthetic**: Deep dark mode theme with neon Cronus Cyan (`#00f0ff`) accents.

---

## Modifying the Documentation

If you want to edit or add content:

1. Edit the Markdown files inside the `src/` directory.
2. Run the generator script using Python:
   ```bash
   python generate.py
   ```
3. The script will automatically parse the Markdown files, update the navigation, rebuild the `search-index.json` database for the search bar, and regenerate the HTML files.

---

## Publishing to GitHub Pages

To host this documentation on GitHub Pages for free:

1. Create a new repository on GitHub (e.g. named `cronus-docs`).
2. Push this folder to your repository:
   ```bash
   git init
   git remote add origin https://github.com/YOUR_USERNAME/cronus-docs.git
   git branch -M main
   git add .
   git commit -m "Initial GPC docs"
   git push -u origin main
   ```
3. On GitHub, go to your repository settings:
   - Click **Settings** (gear icon) -> **Pages** (on the left menu).
   - Under **Build and deployment**, set **Source** to **Deploy from a branch**.
   - Under **Branch**, select **main** and `/ (root)`, then click **Save**.
4. Your site will be live at `https://YOUR_USERNAME.github.io/cronus-docs/` in a few moments!
