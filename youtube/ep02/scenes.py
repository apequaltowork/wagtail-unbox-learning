"""Ep 2 — Opening the Box: Every File Explained.

Scene spec for video/build.py. No code is written this episode; it is a
read-through of the 29 files `wagtail start` generates.

Every line number, setting value and path string here was read out of the real
generated project on Wagtail 7.4.3. If the pinned version ever moves, re-check
them before re-rendering -- stale line numbers on screen are worse than none.

The treebeard sequence is the episode's centrepiece and is animated: the path
string builds four characters at a time, one per tree level.
"""

import sys
from pathlib import Path

VIDEO = Path(__file__).resolve().parent.parent.parent / "video"
sys.path.insert(0, str(VIDEO))
from build import FPS, Episode, Scene  # noqa: E402

BADGE = 'WAGTAIL <b>UNBOXED</b> &nbsp;&middot;&nbsp; 02'


# --------------------------------------------------------------------- treebeard
# Verified live against the real database:
#   '0001'      depth 1   /        Root
#   '00010001'  depth 2   /home/   Home
NODES = [
    ("0001", "Root", "depth 1 &nbsp;&middot;&nbsp; the invisible page above yours", 0),
    ("00010001", "Home", "depth 2 &nbsp;&middot;&nbsp; /home/", 1),
    ("000100010001", "About", "depth 3 &nbsp;&middot;&nbsp; /home/about/", 2),
]


def _node_html(path: str, label: str, meta: str, indent: int, shown_chunks: int) -> str:
    """Render one tree row with only `shown_chunks` four-character groups visible."""
    chunks = [path[i:i + 4] for i in range(0, len(path), 4)]
    out = []
    for n, chunk in enumerate(chunks):
        if n < shown_chunks:
            colour = "var(--teal)" if n == shown_chunks - 1 else "var(--teal-dim)"
            out.append(f'<span style="color:{colour}">{chunk}</span>')
        else:
            out.append(f'<span style="color:#1b2030">{chunk}</span>')
    pad = indent * 60
    return (f'<div class="node" style="margin-left:{pad}px">'
            f'<span class="path">{"".join(out)}</span>'
            f'<span class="label">{label}</span>'
            f'<span class="meta">{meta}</span></div>')


def tree_frames() -> list[str]:
    """Build the tree one level at a time, four path characters per level."""
    head = ('<div class="eyebrow">What "00010001" means</div>'
            '<h2 style="font-size:56px;margin-bottom:20px">A materialised path</h2>'
            '<div class="sub" style="font-size:30px;margin-bottom:40px">'
            'django-treebeard &mdash; four characters per level</div>')
    frames: list[str] = []

    for revealed in range(1, len(NODES) + 1):
        for chunks in range(1, revealed + 2):
            rows = []
            for i, (path, label, meta, indent) in enumerate(NODES):
                if i > revealed - 1:
                    continue
                full = len(path) // 4
                vis = full if i < revealed - 1 else min(chunks, full)
                rows.append(_node_html(path, label, meta, indent, vis))
            frames.extend([head + f'<div class="tree">{"".join(rows)}</div>'] * 8)

    # Final state, held.
    rows = [_node_html(p, l, m, i, len(p) // 4) for p, l, m, i in NODES]
    payoff = ('<div class="sub" style="font-size:32px;margin-top:46px;color:var(--teal)">'
              'The whole ancestry is in the string &mdash; so Wagtail fetches a page\'s '
              'parents in <b>one query</b>, not one per level.</div>')
    frames.extend([head + f'<div class="tree">{"".join(rows)}</div>' + payoff] * (FPS * 2))
    return frames


EPISODE = Episode(
    key="ep02",
    number="02",
    title="Ep 2 - Opening the Box: Every File Explained",
    badge=BADGE,
    intro_say="Opening the box. Every file, explained.",
    outro_say="Next episode, we finally change something. Thanks for watching.",
    scenes=[
        Scene(
            id="premise",
            body="""
            <h2>29 files</h2>
            <div class="quote" style="font-size:48px">Most tutorials explain three of them.<br>
            <span class="hl">We're reading all of them.</span><br><br>
            <span style="font-size:36px;color:var(--muted)">The files you're told to ignore are
            the ones deciding how your site behaves.</span></div>
            """,
            say="Wagtail start generated twenty nine files. Most tutorials explain three of them "
                "and tell you to ignore the rest. We are reading all of them, because the ones you "
                "are told to ignore are the ones deciding how your site actually behaves.",
        ),
        Scene(
            id="no_code",
            body="""
            <h2>No code today</h2>
            <ul class="bullets">
              <li>We don't change a single line</li>
              <li><span class="dim">Start from</span> <b>git checkout ep01-end</b></li>
              <li>Read the box before you rebuild it</li>
            </ul>
            """,
            say="And we change nothing. Not one line. Start from git checkout e p zero one end if "
                "you are following along. Read the box before you rebuild it.",
        ),

        # ------------------------------------------------- settings
        Scene(
            id="manage",
            body="""
            <div class="filename">site/manage.py</div>
            <pre class="code">os.environ.setdefault(
    <span class="s">"DJANGO_SETTINGS_MODULE"</span>,
    <span class="s">"studio.settings.dev"</span>   <span class="c">&lt;-- the split</span>
)</pre>
            <div class="sub" style="margin-top:36px">Dev settings by default. Production only when
            you say so.</div>
            """,
            say="Start at manage dot pie. Standard Django, and one line matters: the settings "
                "module defaults to studio dot settings dot dev. That is the split. You get "
                "development settings by default, and production settings only when you ask for "
                "them.",
        ),
        Scene(
            id="two_paths",
            body="""
            <div class="filename">site/studio/settings/base.py &nbsp;&middot;&nbsp; lines 13&ndash;17</div>
            <pre class="code">PROJECT_DIR = Path(__file__).resolve().parent.parent  <span class="c"># site/studio</span>
BASE_DIR    = PROJECT_DIR.parent                      <span class="c"># site/</span></pre>
            <div class="sub" style="margin-top:40px">One letter apart in your head. Different
            directories. Mixing them up is a classic episode-4 bug.</div>
            """,
            say="Then two path variables that look almost the same and are not. Project dir is the "
                "package. Base dir is the folder above it. They are one letter apart in your head "
                "and mixing them up is a classic bug two episodes from now.",
        ),
        Scene(
            id="installed_apps",
            body="""
            <div class="filename">base.py &nbsp;&middot;&nbsp; line 26</div>
            <pre class="code">INSTALLED_APPS = [
    <span class="s">"home"</span>, <span class="s">"search"</span>,                          <span class="c"># yours</span>
    <span class="k">"wagtail.contrib.forms"</span>,
    <span class="k">"wagtail.contrib.redirects"</span>,
    <span class="k">"wagtail.embeds"</span>, <span class="k">"wagtail.sites"</span>,
    <span class="k">"wagtail.users"</span>, <span class="k">"wagtail.snippets"</span>,
    <span class="k">"wagtail.documents"</span>, <span class="k">"wagtail.images"</span>,
    <span class="k">"wagtail.search"</span>, <span class="k">"wagtail.admin"</span>,
    <span class="k">"wagtail"</span>,                               <span class="c"># 11 Wagtail apps</span>
    <span class="s">"modelcluster"</span>, <span class="s">"taggit"</span>, <span class="s">"django_filters"</span>,
    <span class="s">"django.contrib..."</span>,
]</pre>
            """,
            say="Now the file that matters most. Installed apps.",
        ),
        Scene(
            id="thesis",
            body="""
            <div class="quote">Wagtail isn't a black box bolted on.<br>
            It's <span class="hl">eleven Django apps</span> in your INSTALLED_APPS.<br><br>
            <span style="font-size:40px;color:var(--muted)">Every one of them has models you can
            query.</span></div>
            """,
            say="This is the whole thesis of the series. Wagtail is not a black box bolted onto "
                "Django. It is eleven Django apps sitting in your installed apps list. Every one "
                "of them has models, and you can query them like any other Django model.",
        ),
        Scene(
            id="middleware",
            body="""
            <div class="filename">base.py &nbsp;&middot;&nbsp; line 51</div>
            <h2 style="font-size:52px">One addition to the middleware</h2>
            <pre class="code"><span class="c"># ... the standard Django stack ...</span>
<span class="k">"wagtail.contrib.redirects.middleware.RedirectMiddleware"</span>,</pre>
            <div class="sub" style="margin-top:40px"><b>Last on purpose.</b> It only acts once
            everything else has produced a 404 &mdash; then checks the redirects table.</div>
            """,
            say="Middleware is the standard Django stack plus exactly one addition, and it is last "
                "on purpose. The redirect middleware only acts once everything else has produced a "
                "four oh four, and then it checks the redirects table.",
        ),
        Scene(
            id="static_media",
            body="""
            <div class="filename">base.py &nbsp;&middot;&nbsp; lines 130&ndash;143</div>
            <table>
              <tr><th>Setting</th><th>Means</th></tr>
              <tr><td class="k">STATICFILES_DIRS</td><td class="v">where <i>you</i> put CSS</td></tr>
              <tr><td class="k">STATIC_ROOT</td><td class="v">where collectstatic <i>dumps</i> it for production</td></tr>
              <tr><td class="k">MEDIA_ROOT</td><td class="v">where <i>uploads</i> land</td></tr>
            </table>
            <div class="quote" style="font-size:40px;margin-top:44px">Static is code. Media is
            content.<br><span class="hl">Static is committed; media never is.</span></div>
            """,
            say="Then four settings people mix up constantly. Static files dirs is where you put "
                "CSS. Static root is where collect static dumps it for production. Media root is "
                "where uploads land. The rule that keeps it straight: static is code, media is "
                "content. Static gets committed, media never does.",
        ),
        Scene(
            id="wagtail_block",
            body="""
            <div class="filename">base.py &nbsp;&middot;&nbsp; lines 163&ndash;184</div>
            <pre class="code">WAGTAIL_SITE_NAME = <span class="s">"studio"</span>
WAGTAILSEARCH_BACKENDS = {...}          <span class="c"># database backend, for now</span>
WAGTAILADMIN_BASE_URL = <span class="bad">"http://example.com"</span>
WAGTAILDOCS_MAX_UPLOAD_SIZE = 10 * 1024 * 1024</pre>
            <div class="sub" style="margin-top:40px">That base URL is a
            <b style="color:var(--red)">placeholder that ships broken</b> &mdash; it builds absolute
            URLs for notification emails and previews. Fixed in episode 13.</div>
            """,
            say="And the Wagtail block at the bottom. Site name, the search backend, a ten megabyte "
                "cap on document uploads. But look at wagtail admin base url. It ships as http "
                "colon slash slash example dot com. That is a placeholder that ships broken. It "
                "builds absolute URLs for notification emails and previews. We fix it in episode "
                "thirteen.",
        ),
        Scene(
            id="settings_split",
            body="""
            <h2>dev.py, production.py &mdash; and local.py</h2>
            <pre class="code"><span class="c"># both files end with this:</span>
<span class="k">try</span>:
    <span class="k">from</span> .local <span class="k">import</span> *
<span class="k">except</span> ImportError:
    <span class="k">pass</span></pre>
            <div class="sub" style="margin-top:40px">A <b>settings/local.py</b> that doesn't exist
            and isn't committed can override anything. That's the escape hatch for
            machine-specific config.</div>
            """,
            say="The two settings files are tiny. Dev turns debug on and ships a secret key marked, "
                "in the variable name, as insecure. Production turns debug off. And both end with "
                "the same trick: a local dot pie file that does not exist and is not committed can "
                "override anything. That is the escape hatch for machine specific config.",
        ),

        # ------------------------------------------------- urls
        Scene(
            id="urls",
            body="""
            <div class="filename">site/studio/urls.py</div>
            <pre class="code">path(<span class="s">"django-admin/"</span>, admin.site.urls),
path(<span class="s">"admin/"</span>, include(wagtailadmin_urls)),
path(<span class="s">"documents/"</span>, include(wagtaildocs_urls)),
path(<span class="s">"search/"</span>, search_views.search),

<span class="hl">path(<span class="s">""</span>, include(wagtail_urls)),   <span class="c"># must be LAST</span></span></pre>
            """,
            say="Now urls dot pie, and the order is the whole point.",
        ),
        Scene(
            id="catch_all",
            body="""
            <div class="quote" style="font-size:46px">That last line is Wagtail's
            <span class="hl">catch-all</span>.<br><br>
            Any URL that didn't match above is handed to the page tree,<br>
            which resolves it by walking slugs.<br><br>
            <span style="font-size:36px;color:var(--muted)">That's why /about/team/ just works and
            nobody wrote a URL pattern for it &mdash; and why anything after this line is never
            reached.</span></div>
            """,
            say="That last line is Wagtail's catch all. Any URL that did not match above gets "
                "handed to the page tree, which resolves it by walking slugs. That is why a page at "
                "slash about slash team just works and nobody wrote a URL pattern for it. And it is "
                "why this line has to stay last. Put a route after it and it will never be reached.",
        ),

        # ------------------------------------------------- the home app
        Scene(
            id="homepage_model",
            body="""
            <div class="filename">site/home/models.py &nbsp;&middot;&nbsp; the whole file</div>
            <pre class="code"><span class="k">from</span> django.db <span class="k">import</span> models
<span class="k">from</span> wagtail.models <span class="k">import</span> Page


<span class="k">class</span> HomePage(Page):
    <span class="k">pass</span></pre>
            <div class="sub" style="margin-top:40px">Six lines, and it's a working CMS page type.
            Title, slug, SEO fields, publishing dates, revisions, previews, permissions &mdash; all
            inherited from <b>Page</b>.</div>
            """,
            say="The home app. Models dot pie is six lines, and that is already a working C M S "
                "page type. Title, slug, S E O fields, publishing dates, revisions, previews, "
                "permissions. All of it inherited from Page. We add fields to it next episode.",
        ),
        Scene(
            id="template_convention",
            body="""
            <h2>Templates find themselves</h2>
            <pre class="code">class <span class="k">HomePage</span>(Page)
        &darr;
home/templates/home/<span class="k">home_page</span>.html</pre>
            <div class="sub" style="margin-top:40px">Model name, lowercased, underscored. Wagtail
            derives the template path automatically. Episode 4 exploits this.</div>
            """,
            say="And notice the template naming convention. The model is called HomePage, so "
                "Wagtail looks for home underscore page dot html. Model name, lowercased, with "
                "underscores. You never wire it up. Episode four exploits that.",
        ),

        # ------------------------------------------------- the migration
        Scene(
            id="migration_intro",
            body="""
            <div class="eyebrow">The centrepiece</div>
            <div class="filename">site/home/migrations/0002_create_homepage.py</div>
            <h2>The file nobody opens</h2>
            <div class="sub">Your homepage wasn't a fixture, and you didn't make it in the admin.<br>
            <b>A data migration created it</b> the first time you ran migrate.</div>
            """,
            say="Now the centrepiece of this episode, and the file almost nobody opens. Your "
                "homepage was not a fixture, and you did not create it in the admin. A data "
                "migration made it, the first time you ran migrate. That is why a brand new Wagtail "
                "site already has exactly one page.",
        ),
        Scene(
            id="migration_code",
            body="""
            <div class="filename">0002_create_homepage.py</div>
            <pre class="code"><span class="c"># 1. delete wagtailcore's own default page</span>
Page.objects.filter(slug=<span class="s">"home"</span>, depth=2).delete()

<span class="c"># 2. a ContentType, so a Page row knows which model it is</span>
homepage_content_type, __ = ContentType.objects.get_or_create(
    model=<span class="s">"homepage"</span>, app_label=<span class="s">"home"</span>)

<span class="c"># 3. the page itself</span>
homepage = HomePage.objects.create(
    title=<span class="s">"Home"</span>, slug=<span class="s">"home"</span>,
    <span class="hl">path=<span class="s">"00010001"</span>, depth=2, url_path=<span class="s">"/home/"</span></span>)</pre>
            """,
            say="It does three things. It deletes the default page that wagtail core ships. It "
                "gets or creates a content type, which is how a single Page row knows which model "
                "it really is. And then it creates the page, with values that look like magic.",
        ),
        Scene(id="tree", body="", frames=tree_frames(),
              say="Path equals zero zero zero one, zero zero zero one. That is a materialised path, "
                  "from django treebeard, the package we watched install in episode one. Four "
                  "characters per level. Zero zero zero one is the root. Its first child is that "
                  "plus another zero zero zero one. Its child adds four more. The entire ancestry is "
                  "encoded in the string, which is how Wagtail can fetch a page's parents in one "
                  "query instead of walking up the tree one level at a time."),
        Scene(
            id="two_pages",
            body="""
            <h2>Two pages, not one</h2>
            <div class="term">
              <div class="bar">python manage.py shell</div>
              <div class="body"><span class="o">'0001'         1  /        Root</span>
<span class="hl-out">'00010001'     2  /home/   Home</span></div>
            </div>
            <div class="sub" style="margin-top:36px">There's an invisible <b>Root</b> above your
            homepage. That's why the admin shows your page nested one level down.</div>
            """,
            say="Run that query on your own site and you will see something surprising: there are "
                "two pages, not one. There is an invisible Root above your homepage. That is why "
                "the admin shows your page nested one level down.",
        ),
        Scene(
            id="site_row",
            body="""
            <div class="filename">0002_create_homepage.py &nbsp;&middot;&nbsp; the last line</div>
            <pre class="code">Site.objects.create(
    hostname=<span class="s">"localhost"</span>,
    root_page=homepage,
    is_default_site=<span class="k">True</span>)</pre>
            <div class="sub" style="margin-top:40px">Wagtail is <b>multi-site out of the box</b>.
            This is the row that makes your one site exist.</div>
            """,
            say="And one last line in that migration creates a Site row. Hostname localhost, "
                "default site, root page set to our homepage. Wagtail is multi site out of the box, "
                "and this is the row that makes your one site exist.",
        ),

        # ------------------------------------------------- the rest
        Scene(
            id="search_app",
            body="""
            <div class="filename">site/search/views.py</div>
            <pre class="code">search_results = Page.objects.<span class="k">live</span>().search(search_query)</pre>
            <div class="sub" style="margin-top:40px">A plain Django function view, 35 lines, with a
            paginator. <b>.live()</b> means published only &mdash; drafts excluded.<br>
            Wired up already; nothing indexed yet. That's episode 11.</div>
            """,
            say="The search app is a plain Django function view, about thirty five lines, with a "
                "paginator. Note dot live, which means published pages only, so drafts are "
                "excluded. It is wired up already, but nothing is indexed yet. That is episode "
                "eleven.",
        ),
        Scene(
            id="base_html",
            body="""
            <div class="filename">site/studio/templates/base.html</div>
            <pre class="code">{% <span class="k">if</span> page.seo_title %}{{ page.seo_title }}
{% <span class="k">else</span> %}{{ page.title }}{% <span class="k">endif</span> %}

{% <span class="k">wagtailuserbar</span> %}
{% <span class="k">block</span> content %}{% <span class="k">endblock</span> %}</pre>
            <div class="sub" style="margin-top:40px">SEO title fallback for free. And the
            <b>userbar</b> &mdash; the floating admin bar logged-in editors see on the front end.</div>
            """,
            say="Base dot html gives you an S E O title with a fallback for free, and the wagtail "
                "user bar, which is the floating admin bar that logged in editors see on the front "
                "end of the site. The content block is empty, waiting for episode four.",
        ),
        Scene(
            id="requirements",
            body="""
            <div class="eyebrow">A real inconsistency</div>
            <h2>The generated requirements.txt</h2>
            <pre class="code"><span class="c"># site/requirements.txt says:</span>
Django &gt;= 6, &lt; 6.1

<span class="c"># but pip actually installed:</span>
<span class="bad">Django 6.1.1</span></pre>
            <div class="sub" style="margin-top:40px">Wagtail's own metadata asks only for Django 5.2
            or newer, with no upper limit &mdash; and pip follows metadata, not this file.</div>
            """,
            say="And one last thing, which is a genuine inconsistency. The requirements file that "
                "the template generated caps Django below six point one. But the Django pip "
                "actually installed is six point one point one. They disagree, because Wagtail's "
                "own package metadata asks only for Django five point two or newer with no upper "
                "limit, and pip follows the metadata, not this file. Nothing is broken. But that is "
                "exactly how your environment drifts away from mine.",
        ),
        Scene(
            id="recap",
            body="""
            <h2>Five things to carry forward</h2>
            <ul class="bullets" style="font-size:40px">
              <li>Wagtail is <b>~11 Django apps</b> in INSTALLED_APPS</li>
              <li><b>wagtail_urls is a catch-all</b> and must stay last</li>
              <li>Your homepage came from a <b>data migration</b>, positioned by a treebeard path</li>
              <li>Templates resolve from <b>app/model_name.html</b> automatically</li>
              <li>Two settings ship as <b>placeholders</b>: the dev SECRET_KEY and WAGTAILADMIN_BASE_URL</li>
            </ul>
            """,
            say="Five things to carry forward. Wagtail is about eleven Django apps in installed "
                "apps. The wagtail urls catch all must stay last. Your homepage came from a data "
                "migration, and its position is a treebeard path string. Templates resolve from app "
                "slash model name dot html automatically. And two settings ship as placeholders: "
                "the dev secret key, and the admin base url.",
        ),
        Scene(
            id="next",
            body="""
            <div class="eyebrow">Next</div>
            <h2>Ep 3 &mdash; The Page Model &amp; the Tree</h2>
            <div class="quote" style="font-size:46px">We finally change something.<br>
            <span class="hl">Starting with the Page model those six lines inherit from.</span></div>
            """,
            say="Next episode we finally change something, and the first thing to understand is the "
                "Page model that those six lines inherit from.",
        ),
    ],
)
