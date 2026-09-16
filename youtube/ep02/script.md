# Ep 2 — Opening the Box: Every File Explained

**Target: 24 min.** No code is written. This is the episode most tutorials skip, and it's why
people stay confused for months.

Start from `git checkout ep01-end`. Nothing gets edited — we read.

## Beats

### 0:00–0:50 — The premise
**[SCREEN: the file tree in VS Code, fully expanded]**
> "Twenty-nine files. Most tutorials tell you to ignore twenty-five of them. We're reading all
> of them, because the ones you're told to ignore are the ones that decide how your site behaves."

Show the tree once, whole. Then go top-down.

### 0:50–2:30 — `manage.py` and the two paths
**[SCREEN: manage.py]**
- Standard Django. One line matters: `DJANGO_SETTINGS_MODULE` defaults to `studio.settings.dev`.
- **That's the split:** dev settings by default, production settings only when you say so.

Then `studio/settings/base.py`, lines 13–17:

```python
PROJECT_DIR = Path(__file__).resolve().parent.parent   # site/studio
BASE_DIR = PROJECT_DIR.parent                          # site/
```

Two path variables, one letter apart in your head, meaning different things. `PROJECT_DIR` is
the package; `BASE_DIR` is the folder above it. Confusing these is a classic ep-4 bug.

### 2:30–7:00 — `settings/base.py`: the interesting parts
**[SCREEN: base.py, scrolling section by section]**

**`INSTALLED_APPS` (line 26)** — read it out and group it:

```
home, search                                   <- yours
wagtail.contrib.forms, .redirects, .embeds,
  .sites, .users, .snippets, .documents,
  .images, .search, .admin, wagtail            <- Wagtail, ~11 apps
modelcluster, taggit, django_filters           <- Wagtail's dependencies
django.contrib.*                               <- Django
```

> "This is the whole thesis of the series. Wagtail isn't a black box bolted on — it's eleven
> Django apps in your INSTALLED_APPS. Every one of them has models you can query."

Call out two now, because they pay off later:
- `wagtail.contrib.forms` -> episode 10's contact form
- `wagtail.contrib.redirects` -> why there's an extra middleware

**`MIDDLEWARE` (line 51)** — standard Django plus exactly one addition, at the end:
`wagtail.contrib.redirects.middleware.RedirectMiddleware`. It's last on purpose — it only acts
once everything else has produced a 404, then checks the redirects table.

**`TEMPLATES` (line 64)** — `DIRS: [PROJECT_DIR / "templates"]` **and** `APP_DIRS: True`.
Two places templates can live. Ep 4 depends on knowing which wins.

**`DATABASES` (line 91)** — `BASE_DIR / "db.sqlite3"`. One line. No server.

**Static and media (lines 130–143)** — the four names people mix up:

| Setting | Means |
|---|---|
| `STATICFILES_DIRS` | where *you* put CSS (`PROJECT_DIR / "static"`) |
| `STATIC_ROOT` | where `collectstatic` *dumps* it for production |
| `MEDIA_ROOT` | where *uploads* land |
| `STATIC_URL` / `MEDIA_URL` | the URL prefixes |

> "Static is code. Media is content. Static is committed; media never is."

**The Wagtail block (lines 163–184):**
- `WAGTAIL_SITE_NAME = "studio"` — shows in the admin and in page titles
- `WAGTAILSEARCH_BACKENDS` — database backend by default. Fine for now; revisited in ep 11.
- `WAGTAILADMIN_BASE_URL = "http://example.com"` — **a placeholder that ships broken.** It builds absolute URLs for notification emails and previews. Flag it now, fix it in ep 13.
- `WAGTAILDOCS_EXTENSIONS` / `WAGTAILDOCS_MAX_UPLOAD_SIZE` — an upload allowlist and a 10 MB cap, on by default. Good defaults worth knowing exist.

### 7:00–9:00 — `dev.py` and `production.py`
**[SCREEN: both files side by side — they're tiny]**

`dev.py`: `DEBUG = True`, a hardcoded `SECRET_KEY` prefixed `django-insecure-`,
`ALLOWED_HOSTS = ["*"]`, console email backend.

> "Wagtail is telling you, in the variable name, not to ship this key. It generates a fresh one
> per project — and it's in your git history the moment you commit."

`production.py`: `DEBUG = False`, and swaps in `ManifestStaticFilesStorage`.

**Both end with the same trick:**

```python
try:
    from .local import *
except ImportError:
    pass
```

A `settings/local.py` that doesn't exist and isn't committed can override anything. That's the
escape hatch for machine-specific config. Ep 13 uses it.

### 9:00–11:00 — `studio/urls.py`
**[SCREEN: urls.py]**

Read it in order, because **order is the whole point**:
1. `django-admin/` — the raw Django admin, still there, rarely used
2. `admin/` — **Wagtail's** admin
3. `documents/`, `search/`
4. `if settings.DEBUG:` — serve static and media from the dev server, debug only. Ep 13 material.
5. **Last:** `path("", include(wagtail_urls))`

> "That last line is Wagtail's catch-all. Any URL that didn't match above gets handed to the page
> tree, which resolves it by walking slugs. That's why a page at /about/team/ just works — nobody
> wrote a URL pattern for it. And it's why this line must stay last: put a route after it and it
> will never be reached."

Also show the commented-out `pages/` alternative and say when you'd want it.

### 11:00–13:30 — The `home` app
**[SCREEN: home/models.py — all six lines]**

```python
class HomePage(Page):
    pass
```

> "That's a working CMS page type. It inherits title, slug, SEO fields, publishing dates,
> revisions, previews and permissions from `Page`. We add fields to it next episode."

Tease only — ep 3 owns this.

- `home/apps.py` — boilerplate `AppConfig`, `BigAutoField`.
- `home/templates/home/home_page.html` — note the convention: `app/model_name.html`, lowercased with underscores. Wagtail derives it from the model name automatically. Point at it; ep 4 exploits it.
- `home/static/css/welcome_page.css` + `welcome_page.html` — the teal egg. Deleted in ep 4.
- `home/tests.py` — empty. Acknowledge, move on.

### 13:30–17:30 — ⭐ The migration that creates your homepage
**[SCREEN: home/migrations/0002_create_homepage.py]**

The centrepiece of the episode. Almost nobody opens this file, and it explains a lot.

Walk `create_homepage()` line by line:

1. **It deletes a page first.** `wagtailcore` ships its own default page with slug `home` at depth 2; this migration removes it.
2. Gets or creates a `ContentType` for `HomePage`. **That's how a `Page` row knows which model it really is** — one shared table, many page types, `content_type` says which.
3. Creates the HomePage with values that look like magic:

   ```python
   path="00010001", depth=2, numchild=0, url_path="/home/"
   ```

   > "`path` is a materialised path — that's django-treebeard, the package we watched install in
   > episode 1. Four characters per level. `0001` is the root, `00010001` is its first child.
   > Depth 2. The entire tree position is encoded in that string, which is how Wagtail fetches a
   > page's ancestors in one query instead of walking parent links."

4. Creates a `Site` — hostname `localhost`, `is_default_site=True`, root page = our homepage.

   > "Wagtail is multi-site out of the box. This is the row that makes your one site exist."

Then `run_before = [("wagtailcore", "0053_locale_model")]` — 20 seconds on why ordering matters.

And `remove_homepage`, the reverse function, with its comment noting Page and Site cascade.

> "So your homepage isn't a fixture and wasn't created in the admin. A data migration made it,
> the first time you ran migrate. That's why a brand-new Wagtail site already has exactly one page."

### 17:30–20:00 — The `search` app and `base.html`
**[SCREEN: search/views.py]**
- A plain Django function view, ~35 lines. `Page.objects.live().search(query)` plus a paginator.
- `.live()` — published only; drafts excluded.
- Note the commented-out `Query.get(...)` promoted-results block — Wagtail leaving a door open. Ep 11.
- It's wired up already, but nothing is indexed yet. Ep 11.

**[SCREEN: studio/templates/base.html]**
- `{% load static wagtailcore_tags wagtailuserbar %}`
- The `title` block: `page.seo_title` falling back to `page.title`, plus `{% wagtail_site %}` for the suffix. **SEO defaults, for free.**
- `{% wagtailuserbar %}` — the floating admin bar logged-in editors get on the front end. Show it live in the browser; it's a nice moment.
- `{% if request.in_preview_panel %}<base target="_blank">` — a small detail that makes the live preview panel behave.
- `{% block content %}` — empty, waiting for ep 4.
- `404.html` / `500.html` — exist, minimal.

### 20:00–22:30 — The files nobody explains
**[SCREEN: Dockerfile, .dockerignore, requirements.txt]**

- `Dockerfile` + `.dockerignore` — Wagtail ships a production-ready Dockerfile. Skim it, name gunicorn, don't teach Docker. Ep 14 decides whether we use it.
- **`site/requirements.txt` — the discrepancy.** The big one. Open it on screen:

  ```
  Django>=6,<6.1
  wagtail>=7.4,<7.5
  ```

  Then run `python -c "import django; print(django.__version__)"` -> **6.1.1**.

  > "The file the template generated says Django under 6.1. The Django pip actually installed is
  > 6.1.1. They disagree — because Wagtail's own package metadata says `Django>=5.2` with no upper
  > bound, and pip follows that, not this file. Nothing is broken. But this is exactly how your
  > screen stops matching mine three episodes from now."

  That's why the repo root carries its own pinned `requirements.txt`. Show it.

### 22:30–24:00 — Recap and close
**[SCREEN: the tree again, now annotated with on-screen labels]**

Five things to carry forward:
1. Wagtail is ~11 Django apps in `INSTALLED_APPS`.
2. `wagtail_urls` is a catch-all and must stay last.
3. Your homepage came from a **data migration**, and its position is a treebeard path string.
4. Templates resolve from `app/model_name.html` automatically.
5. Two settings ship as placeholders: the dev `SECRET_KEY` and `WAGTAILADMIN_BASE_URL`.

> "Next episode we finally change something — starting with the Page model those six lines inherit from."

```bash
git tag ep02-end
```

(Same tree as `ep01-end`; the tag exists so the README table stays consistent.)

## Do NOT do in this episode
- Add any field to `HomePage`. Ep 3.
- Explain StreamField. Ep 5.
- Teach Docker.
- Read every line of `base.py` aloud — only the sections listed above. The rest is stock Django.

## Editing notes
- VS Code, large font, breadcrumbs on. This is a reading episode; legibility *is* the production value.
- Highlight the specific line numbers as they come up: 26, 51, 64, 91, 130–143, 163–184.
- The treebeard `path` explanation deserves a small animated graphic:
  `0001` -> `00010001` -> `000100010001`.
