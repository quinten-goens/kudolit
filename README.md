# KudoLit

A shareable kudos board app built with Streamlit and PocketBase. Create appreciation pages for any person or occasion — birthdays, farewells, anniversaries, team wins.

## How it works

Every kudo page has three access codes (each ~10 characters):

| Code | What it does |
|------|-------------|
| **Admin code** | Full control: create/delete pages, delete messages, see all codes |
| **User code** | Add kudo messages (text + optional image/GIF) |
| **Viewer code** | Read-only view of the page |

Share the appropriate code with your audience. Codes also work as URL query parameters for easy linking: `https://your-app/?code=abc123xyz`

## Getting started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the app

```bash
streamlit run app.py
```

### 3. Create a kudo page

1. Open the app and enter an **admin code** (you need one from a previous session, or set up a bootstrap admin directly in PocketBase).
2. Go to the **Create page** tab.
3. Enter a heading (e.g. "Happy Birthday, Jane!") and pick a theme.
4. Click **Create page** — you'll receive three codes. Save them.

### 4. Collect kudos

Share the **user code** (or `?code=<user_code>` URL) with people who should leave messages. They can:
- Write a message with **markdown formatting** (bold, italic, lists, links)
- Attach an image by URL or file upload
- Messages appear as cards on the board in real time

### 5. View the board

Share the **viewer code** (or `?code=<viewer_code>` URL) with anyone who should see the finished board without being able to add messages.

## Themes

Available presets: **default**, **warm**, **cool**, **celebration**, **nature**, and **custom** (pick any background color).

## Tech stack

- [Streamlit](https://streamlit.io) — frontend
- [PocketBase](https://pocketbase.io) via [Pockethost](https://pockethost.io) — backend & file storage
- `markdown` — message content rendering
