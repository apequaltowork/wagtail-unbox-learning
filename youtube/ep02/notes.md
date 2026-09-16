# Ep 2 — Rehearsal notes & gotchas

## Verified against the real generated project

- **29 files** in `site/`, excluding `__pycache__/` and `db.sqlite3`. (I said 28 on the first
  pass of the script — it's 29. Counted, not estimated.)
- `INSTALLED_APPS` order confirmed at line 26 of `studio/settings/base.py`:
  `home`, `search`, then 11 Wagtail entries, then `modelcluster`, `taggit`, `django_filters`,
  then the `django.contrib.*` block.
- Exactly **one** non-Django middleware, and it is last:
  `wagtail.contrib.redirects.middleware.RedirectMiddleware`.
- Line numbers cited in the script are real for Wagtail 7.4.3:
  13–17 paths · 26 INSTALLED_APPS · 51 MIDDLEWARE · 64 TEMPLATES · 91 DATABASES ·
  130–143 static/media · 163–184 the Wagtail block. `base.py` is 184 lines total.
  **Re-check these if the Wagtail version ever moves.**
- `WAGTAILADMIN_BASE_URL` really is `"http://example.com"` out of the box.
- `WAGTAILDOCS_MAX_UPLOAD_SIZE` is 10 MB; `WAGTAILDOCS_EXTENSIONS` is a 10-entry allowlist.

## Treebeard paths — verified live

```
'0001'      depth 1   /        Root
'00010001'  depth 2   /home/   Home
```

Site row: `hostname="localhost"`, `is_default_site=True`, `root_page_id=3`.

Two things worth noting on camera:
- There are **two** pages, not one. The invisible "Root" above the homepage surprises people —
  it's why the admin shows your homepage nested one level down.
- `root_page_id` is **3**, not 1 or 2. Because migration 0002 *deletes* wagtailcore's default
  home page and creates a new one, the IDs skip. Don't promise a specific ID on camera; a
  viewer's number may differ.

## The requirements.txt discrepancy (the 20:00 beat)

Generated `site/requirements.txt`:
```
Django>=6,<6.1
wagtail>=7.4,<7.5
```

Actually installed by `pip install wagtail==7.4.3`: **Django 6.1.1**.

Because Wagtail's own metadata declares no upper bound:
```
['Django>=5.2', 'django-modelcluster<7.0,>=6.5', ...]
```

So the generated file and the real resolution disagree. Nothing breaks, but it's the mechanism
by which a viewer's environment drifts from the one on screen — which is exactly why the repo
root has its own pinned `requirements.txt`. Introduced in ep 1, dissected here.

Reproduce on camera:
```bash
python -c "from importlib.metadata import requires; print([r for r in requires('wagtail') if r.lower().startswith('django')])"
```

## Recording notes

- **This episode will run long.** 24 minutes is the target and the `base.py` section is where it
  blows out. Only cover the sections in the script; the rest of `base.py` is stock Django and
  saying so is enough.
- Font size up. Two-thirds of this episode is reading a screen.
- The `{% wagtailuserbar %}` beat needs the browser, logged in, on the front end — set that tab
  up before recording so there's no login fumble mid-take.
- Have the shell session for the treebeard paths pre-warmed in a second terminal; `manage.py
  shell` takes a few seconds to boot and it kills the pacing.

## Open

- The treebeard animation (`0001` -> `00010001` -> `000100010001`) needs making. It's the single
  highest-value graphic in the first three episodes.
- Consider whether the Dockerfile skim earns its 90 seconds, or should be cut to 20 and deferred
  to ep 14 entirely. Decide in the edit.
