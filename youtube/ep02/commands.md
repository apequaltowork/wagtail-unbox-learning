# Ep 2 — Commands

This episode is a **reading** episode. Almost nothing is typed and nothing is changed.

## Start from episode 1's end state

```bash
git checkout ep01-end
```

Activate your venv:

```powershell
.venv\Scripts\activate          # Windows
```
```bash
source .venv/bin/activate       # macOS / Linux
```

## The three commands actually run on camera

**1. See the whole tree** (excluding caches and the database):

Windows (PowerShell):
```powershell
Get-ChildItem -Recurse -File site |
  Where-Object { $_.FullName -notmatch '__pycache__' -and $_.Name -ne 'db.sqlite3' } |
  Resolve-Path -Relative
```

macOS / Linux:
```bash
find site -type f -not -path "*/__pycache__/*" -not -name "db.sqlite3" | sort
```

Expect **29 files**.

**2. The Django version discrepancy** (the 20:00 beat):

```bash
cat site/requirements.txt
python -c "import django; print(django.__version__)"
```

`site/requirements.txt` says `Django>=6,<6.1`. The installed version is `6.1.1`. They disagree —
Wagtail 7.4.3's package metadata declares `Django>=5.2` with no upper bound, and pip follows
metadata, not the generated file. See `notes.md`.

To see the metadata yourself:

```bash
python -c "from importlib.metadata import requires; print([r for r in requires('wagtail') if r.lower().startswith('django')])"
```

**3. Tag the episode:**

```bash
git tag ep02-end
```

No code changed, so there's nothing to commit — the tag points at the same commit as
`ep01-end`. It exists so the episode table in the README is consistent.

## Files read, in episode order

| Order | File | Why it matters |
|---|---|---|
| 1 | `site/manage.py` | Defaults to `studio.settings.dev` |
| 2 | `site/studio/settings/base.py` | `INSTALLED_APPS`, middleware, templates, static/media, Wagtail block |
| 3 | `site/studio/settings/dev.py` | `DEBUG`, the insecure `SECRET_KEY`, `local.py` escape hatch |
| 4 | `site/studio/settings/production.py` | `DEBUG=False`, manifest static storage |
| 5 | `site/studio/urls.py` | `wagtail_urls` catch-all must stay last |
| 6 | `site/home/models.py` | `class HomePage(Page): pass` |
| 7 | `site/home/apps.py` | Boilerplate `AppConfig` |
| 8 | `site/home/migrations/0002_create_homepage.py` | ⭐ Creates your homepage + Site row |
| 9 | `site/home/templates/home/home_page.html` | `app/model_name.html` convention |
| 10 | `site/search/views.py` | `Page.objects.live().search(q)` + paginator |
| 11 | `site/studio/templates/base.html` | SEO title block, `{% wagtailuserbar %}` |
| 12 | `site/Dockerfile` | Skim only |
| 13 | `site/requirements.txt` | The version discrepancy |

## Optional: see the treebeard paths for yourself

A nice live moment for the 13:30 beat.

```bash
cd site
python manage.py shell
```

```python
from wagtail.models import Page, Site
for p in Page.objects.all():
    print(repr(p.path), p.depth, p.url_path, p.title)

Site.objects.all().values("hostname", "root_page_id", "is_default_site")
```

Expect the root at `0001` (depth 1) and your homepage at `00010001` (depth 2) — four characters
per tree level, exactly as the migration hardcoded them.

Exit with `exit()`.
