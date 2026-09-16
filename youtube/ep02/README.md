# Ep 2 — Opening the Box: Every File Explained

| | |
|---|---|
| **Video file** | `youtube/ep02/out/ep02.mp4` |
| **Subtitles** | `youtube/ep02/out/ep02.srt` |
| **Thumbnail** | `youtube/ep02/assets/thumb.png` |
| **Runtime** | 7:51 |
| **Git tag** | `ep02-end` — **push it before publishing** |
| **Category** | Education |

## Title

```
Wagtail Project Structure Explained: Every File | Wagtail Tutorial #2
```

Target search: `wagtail project structure`. Front-loaded, 69 characters.

Previous (brand-first) version, kept for reference:
`Wagtail Unboxed #2: Every File Wagtail Generates, Explained`

**Alternatives:**

```
The Files Wagtail Tutorials Tell You To Ignore | Wagtail Unboxed #2
What's Actually In A New Wagtail Project?
```

---

## Description

```
`wagtail start` generates 29 files. Most tutorials explain three of them. We read all of them —
because the ones you're told to ignore are the ones deciding how your site behaves.

The highlight: the data migration that quietly created your homepage. Nobody opens
0002_create_homepage.py, and it explains the page tree, content types, and Wagtail's
multi-site model all at once — including why your homepage's database row has a path
of "00010001".

ALSO COVERED
• Wagtail is ~11 Django apps in INSTALLED_APPS — that's the whole mental model
• Why the wagtail_urls catch-all MUST be the last URL pattern
• PROJECT_DIR vs BASE_DIR, and STATIC_ROOT vs STATICFILES_DIRS vs MEDIA_ROOT
• The settings split: dev.py, production.py, and the local.py escape hatch
• Two settings that ship as broken placeholders (the dev SECRET_KEY and WAGTAILADMIN_BASE_URL)
• A real inconsistency: the generated requirements.txt caps Django below 6.1, but pip installs 6.1.1

No code is written this episode. Read the box before you rebuild it.

📋 Commands and the full reading order:
https://github.com/apequaltowork/wagtail-unbox/blob/main/youtube/ep02/commands.md

📦 CODE — start from where this episode begins:
https://github.com/apequaltowork/wagtail-unbox

    git checkout ep01-end

CHAPTERS
0:00 29 files, and why we're reading all of them
0:20 No code today
0:32 manage.py and the settings split
0:51 PROJECT_DIR vs BASE_DIR
1:07 INSTALLED_APPS
1:13 Wagtail is just Django apps
1:31 The one middleware addition
1:46 Static vs media
2:09 The Wagtail settings block
2:36 dev.py, production.py, and local.py
3:01 urls.py
3:06 Why the catch-all must be last
3:30 HomePage(Page) — six lines
3:51 How templates find themselves
4:10 The migration nobody opens
4:30 Inside the migration
4:48 Treebeard: what "00010001" means
5:22 Two pages, not one
5:38 The Site row
5:54 The search app
6:13 base.html and the Wagtail userbar
6:30 The requirements.txt discrepancy
7:02 Five things to remember
7:31 Next episode

NEXT → Ep 3: The Page Model & the Tree — we finally change something.

📦 Code: https://github.com/apequaltowork/wagtail-unbox
🌐 Site: https://apequaltowork.github.io/ashish-pitroda/
💼 LinkedIn: https://www.linkedin.com/in/ashish-pitroda/
✉️ apequaltowork@gmail.com

🔧 Wagtail 7.4.3 · Django 6.1.1 · Python 3.12
Recorded on Windows. macOS and Linux commands are in the repo for every episode.

#wagtail #django #python #cms #webdev
```

---

## Tags

```
wagtail tutorial, wagtail project structure, wagtail settings, django settings, wagtail page tree, treebeard, django migrations, data migration, wagtail cms, django cms, wagtail explained, wagtail for beginners, wagtail 7.4, django project structure
```

---

## Thumbnail

`youtube/ep02/assets/thumb.png`

VS Code file tree on the left, `0002_create_homepage.py` open on the right with
`path="00010001"` circled in red.
Overlay: **EVERY FILE**, small *Wagtail Unboxed 2*.

---

## Pinned comment

```
The bit worth rewatching is 15:45 — the path="00010001" in the homepage migration.

Wagtail stores the page tree as a materialised path: 4 characters per level. Root is "0001",
its first child is "00010001", that child's first child is "000100010001". Encoding the whole
ancestry in the string is how Wagtail gets a page's ancestors in ONE query instead of walking
parent links up the tree. That's django-treebeard, which you watched install in episode 1.

See it on your own site:

  cd site
  python manage.py shell

  from wagtail.models import Page
  for p in Page.objects.all():
      print(repr(p.path), p.depth, p.url_path, p.title)

You'll see two pages, not one — there's an invisible "Root" above your homepage.

Which file surprised you most? I'd guess the migration.
```

---

## Before publishing

```bash
git push origin ep02-end
```

---

## End screen

- Subscribe element
- "Next video" → Ep 3
- Link element → the repo
