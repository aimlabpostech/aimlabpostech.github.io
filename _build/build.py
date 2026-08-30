#!/usr/bin/env python3
"""
Static-site generator for the AIM Lab homepage.

Usage:  python3 _build/build.py
Writes plain .html files into the repository root. No dependencies.
Edit the CONTENT sections below, then re-run to regenerate every page
with a consistent header, navigation and footer.
"""

import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "_build", "data")
SITE_URL = "https://www.analyticsim.org"

MEMBER_PAGES = [
    ("members/professor/index.html", "Professor"),
    ("members/emeritus/index.html", "Emeritus Professors"),
    ("members/students/index.html", "Students"),
    ("members/alumni/index.html", "Alumni"),
]

PUBLICATION_PAGES = [
    ("publications/journal/index.html", "Journal Articles"),
    ("publications/conference/index.html", "Conference Papers"),
]

NAV = [
    ("index.html", "Home", []),
    ("research.html", "Research", []),
    ("members/index.html", "Members", MEMBER_PAGES),
    ("publications/index.html", "Publications", PUBLICATION_PAGES),
    ("projects.html", "Projects", []),
    ("news.html", "News", []),
    ("join.html", "Join Us", []),
    ("contact.html", "Contact", []),
]


def nav_url(href):
    if href == "index.html":
        return "/"
    if href.endswith("/index.html"):
        return "/" + href[: -len("index.html")]
    return "/" + href


def section_of(slug):
    """Which top-level nav entry a page belongs to."""
    if slug.startswith("members/"):
        return "members/index.html"
    if slug.startswith("publications/"):
        return "publications/index.html"
    if slug.startswith("news/"):
        return "news.html"
    return slug


# --------------------------------------------------------------------------
# Layout
# --------------------------------------------------------------------------
def page(slug, title, description, body, extra_head=""):
    section = section_of(slug)
    parts = []
    for href, label, subs in NAV:
        active = " active" if href == section else ""
        if not subs:
            aria = ' aria-current="page"' if href == slug else ""
            parts.append(
                f'        <a href="{nav_url(href)}" class="nav-link{active}"{aria}>{label}</a>'
            )
            continue
        sub_items = []
        for sh, sl in subs:
            cur = ' class="current" aria-current="page"' if sh == slug else ""
            sub_items.append(f'            <a href="{nav_url(sh)}"{cur}>{sl}</a>')
        sub_html = "\n".join(sub_items)
        parts.append(
            f'        <div class="nav-item has-sub">\n'
            f'          <a href="{nav_url(href)}" class="nav-link{active}">{label}'
            f'<svg class="caret" width="9" height="6" viewBox="0 0 9 6" aria-hidden="true">'
            f'<path d="M1 1l3.5 3.5L8 1" fill="none" stroke="currentColor" stroke-width="1.5" '
            f'stroke-linecap="round"/></svg></a>\n'
            f'          <div class="subnav">\n{sub_html}\n          </div>\n'
            f'        </div>'
        )
    nav_html = "\n".join(parts)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="canonical" href="{SITE_URL}{nav_url(slug)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:url" content="{SITE_URL}{nav_url(slug)}">
<meta property="og:site_name" content="AIM Lab, POSTECH">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/style.css">
{extra_head}</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>

<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="/">
      <span class="brand-mark">AIM</span>
      <span class="brand-text">
        <span class="brand-name"><span class="brand-full">Analytics &amp; Information Management Lab</span><span class="brand-short">POSTECH AIM Lab</span></span>
        <span class="brand-sub">POSTECH &middot; Industrial &amp; Management Engineering</span>
      </span>
    </a>
    <button class="nav-toggle" type="button" aria-label="Menu" aria-expanded="false" aria-controls="primary-nav"><span></span></button>
    <nav class="nav" id="primary-nav" aria-label="Primary">
{nav_html}
    </nav>
  </div>
</header>

<main id="main">
{body}
</main>

<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <div class="footer-brand">
          <span class="brand-mark">AIM</span>
          <strong>Analytics &amp; Information Management Lab</strong>
        </div>
        <p>Department of Industrial &amp; Management Engineering<br>
        Pohang University of Science and Technology (POSTECH)</p>
        <p>Engineering Building 4, Room 408<br>
        77 Cheongam-ro, Nam-gu, Pohang, Gyeongbuk 37673, Republic of Korea</p>
      </div>
      <div>
        <h4>Navigate</h4>
        <ul>
          <li><a href="/research.html">Research</a></li>
          <li><a href="/members/">Members</a></li>
          <li><a href="/publications/">Publications</a></li>
          <li><a href="/projects.html">Projects &amp; Centers</a></li>
          <li><a href="/join.html">Join Us</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href="mailto:mssong@postech.ac.kr">mssong@postech.ac.kr</a></li>
          <li><a href="tel:+82542798260">+82-54-279-8260</a></li>
          <li><a href="https://www.postech.ac.kr/eng/" rel="noopener">POSTECH</a></li>
          <li><a href="https://ime.postech.ac.kr/" rel="noopener">Dept. of IME</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span data-year>2026</span> Analytics &amp; Information Management Lab, POSTECH. All rights reserved.</span>
      <span>www.analyticsim.org</span>
    </div>
  </div>
</footer>

<script src="/assets/js/main.js"></script>
</body>
</html>
"""


def page_head(eyebrow, title, sub):
    """No visible banner — content starts straight away — but keep one h1 per page."""
    plain = re.sub(r"<[^>]+>", "", f"{title}")
    return f'<h1 class="sr-only">{plain}</h1>\n'


# --------------------------------------------------------------------------
# Publications
# --------------------------------------------------------------------------
INITIAL_END = re.compile(r"(?:\b[A-Z]|\bal|\bDr|\bProf|\bvol|\bpp|\bNo|\bEds?)\.$")


def parse_citation(line):
    m = re.match(r"^(?P<authors>.*?)\((?P<year>\d{4})[a-z]?\)\.?\s*(?P<rest>.*)$", line.strip())
    if not m:
        return None
    authors = m.group("authors").strip().rstrip(",").strip()
    year = int(m.group("year"))
    rest = m.group("rest").strip()

    title, venue = rest, ""
    for mm in re.finditer(r"[.?!]\s+", rest):
        head = rest[: mm.start() + 1]
        if head.endswith(".") and INITIAL_END.search(head):
            continue
        title = head.strip()
        venue = rest[mm.end():].strip()
        break

    # Fallback: some records separate title and venue with a comma
    # e.g. "... to Enhance User Comprehension, Data & Knowledge Engineering, 164, 102601."
    if not venue:
        cm = re.search(r",\s*([A-Z][^,]{3,80}?),\s*(\d+[^,]*(?:,.*)?)$", title)
        if cm:
            venue = f"{cm.group(1)}, {cm.group(2)}"
            title = title[: cm.start()].strip()

    title = title.rstrip(".").strip()
    venue = venue.rstrip().rstrip(".").strip()
    return {"authors": authors, "year": year, "title": title, "venue": venue}


def bucket(year):
    if year >= 2025:
        return "b2025"
    if year >= 2020:
        return "b2020"
    if year >= 2015:
        return "b2015"
    if year >= 2010:
        return "b2010"
    return "b2009"


def load_publications():
    """Citations with DOI, BibTeX and (where available) the paper PDF."""
    with open(os.path.join(DATA, "publications.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    for group in data.values():
        group.sort(key=lambda x: -x["year"])
    return data["journals"], data["conferences"]


def pub_links(it):
    links = []
    if it.get("pdf"):
        links.append(
            f'<a class="pill pill-pdf" href="/assets/papers/{it["pdf"]}" target="_blank" rel="noopener">PDF</a>'
        )
    if it.get("doi"):
        doi = it["doi"].replace("http://", "https://")
        links.append(f'<a class="pill" href="{doi}" target="_blank" rel="noopener">DOI</a>')
    if it.get("url") and not it.get("doi"):
        links.append(
            f'<a class="pill" href="{it["url"]}" target="_blank" rel="noopener">Full text</a>'
        )
    if it.get("bib"):
        links.append(
            '<details class="bib"><summary class="pill">BibTeX</summary>'
            f'<div class="bib-body"><button class="bib-copy" type="button">Copy</button>'
            f'<pre>{html.escape(it["bib"])}</pre></div></details>'
        )
    if not links:
        return ""
    return '\n      <div class="pub-links">' + "".join(links) + "</div>"


def render_pubs(items, list_id):
    out = []
    current = None
    for it in items:
        if it["year"] != current:
            if current is not None:
                out.append("  </ul>\n</div>")
            current = it["year"]
            out.append(
                f'<div data-group>\n  <div class="pub-year">{current}</div>\n  <ul class="pub-list">'
            )
        venue = (
            f' &middot; <span class="v">{html.escape(it["venue"])}</span>' if it["venue"] else ""
        )
        out.append(
            f'    <li class="pub" data-tags="{bucket(it["year"])}">'
            f'<span class="t">{html.escape(it["title"])}</span>'
            f'<span class="a">{html.escape(it["authors"])}{venue}</span>'
            f'{pub_links(it)}</li>'
        )
    if current is not None:
        out.append("  </ul>\n</div>")
    return f'<div id="{list_id}">\n' + "\n".join(out) + "\n</div>"


FILTER_BAR = """<div class="filters" data-filter-bar="#{lid}">
  <button data-filter="all" aria-pressed="true">All</button>
  <button data-filter="b2025" aria-pressed="false">2025&ndash;</button>
  <button data-filter="b2020" aria-pressed="false">2020&ndash;2024</button>
  <button data-filter="b2015" aria-pressed="false">2015&ndash;2019</button>
  <button data-filter="b2010" aria-pressed="false">2010&ndash;2014</button>
  <button data-filter="b2009" aria-pressed="false">&ndash;2009</button>
</div>"""


# --------------------------------------------------------------------------
# People
# --------------------------------------------------------------------------
STUDENTS = [
    ("Seunguk Kang", "Ph.D. student, Industrial & Management Engineering", "kangsu@postech.ac.kr", 2025),
    ("Gyeunggeun Doh", "Ph.D. student, Industrial & Management Engineering", "doh2629@postech.ac.kr", 2025),
    ("Kongdan Zhou", "Ph.D. student, Industrial & Management Engineering", "kdzhou@postech.ac.kr", 2026),
    ("Hyunjun Jung", "Ph.D. student, Industrial & Management Engineering", "jhj1769@postech.ac.kr", 2026),
    ("Yoojin Jeong", "M.S. student, Industrial Data Science", "y8jin@postech.ac.kr", 2025),
    ("Jiwon Park", "M.S. student, Industrial Data Science", "jiwon23@postech.ac.kr", 2025),
    ("Jaehun Hwang", "M.S. student, Industrial & Management Engineering", "jaehunh@postech.ac.kr", 2025),
    ("Dongseok Seo", "M.S. student, Industrial & Management Engineering", "seods99@postech.ac.kr", 2025),
    ("Hyovin Park", "M.S. student, Industrial & Management Engineering", "hvpark19@postech.ac.kr", 2025),
    ("Keonwoo Park", "M.S. student, Industrial & Management Engineering", "pkwoo2001@postech.ac.kr", 2025),
    ("Jihyun Park", "M.S. student, Industrial & Management Engineering", "jihyun03140@postech.ac.kr", 2025),
    ("Hyeonmin Park", "M.S. student, Industrial & Management Engineering", "parkhm@postech.ac.kr", 2025),
    ("Hyeongkyeong Lee", "M.S. student, Industrial & Management Engineering", "hk.lee@postech.ac.kr", 2025),
    ("Sunah Min", "M.S. student, Social Data Science", "sunahmin@postech.ac.kr", 2025),
    ("Ingon Chu", "M.S. student, Defense Science and Technology", "chuingon1226@postech.ac.kr", 2026),
    ("Heeryeong Park", "M.S. student, Industrial & Management Engineering", "hee010505@postech.ac.kr", 2026),
]

POSTDOC_ALUMNI = [
    ("Jitaek Lim", "2023&ndash;2024", "KISTI"),
    ("Hyunyoung Ryu", "2021", "POSTECH Future City Open Innovation Center"),
    ("Seongcheol Hong", "2014&ndash;2016", "&mdash;"),
    ("Bernardo Nugroho Yahya", "2012&ndash;2013", "Hankuk University of Foreign Studies"),
]

PHD_ALUMNI = [
    ("2025", "Kangah Park", "POSTECH"),
    ("2025", "Deoksang Lee", "Samsung Electronics"),
    ("2025", "Jungeun Lim", "Samsung SDI"),
    ("2024", "Kyunghoon Park", "Samsung Research"),
    ("2021", "Kiwon Lee", "Samsung Electronics"),
    ("2019", "Jaeyoung Lee", "Samsung Electronics"),
    ("2018", "Minsu Cho", "Kwangwoon University"),
]

MS_ALUMNI = [
    ("2026", "Hyunjun Jung", "POSTECH (Ph.D. programme)"),
    ("2026", "Sohyeon Lee", "&mdash;"),
    ("2026", "Kina Park", "&mdash;"),
    ("2025", "Hyeyoung Koh", "Samsung Electronics"),
    ("2025", "Junghyun Kim", "Samsung Electronics"),
    ("2024", "Hyojin Lee", "Woorien"),
    ("2024", "Jieun Kim", "Nexon"),
    ("2024", "Yujung Han", "Kakao Bank"),
    ("2023", "Eunchae Lee", "SK hynix"),
    ("2023", "Jaekwan Koo", "LG Electronics"),
    ("2023", "Seungye Bae", "Koylabs"),
    ("2023", "Seungmin Chung", "SK hynix"),
    ("2023", "Soohyeon Hwang", "Hankookilbo"),
    ("2022", "Virda Setyani", "Evermos"),
    ("2022", "Jaemin Shin", "TmaxSoft"),
    ("2022", "Yunhui Jang", "POSTECH"),
    ("2022", "Junhyun Park", "UPSTAGE"),
    ("2022", "Youngseok Jang", "Riiid"),
    ("2022", "Minchul Jeong", "Fitogether"),
    ("2021", "Sinnyum Park", "Samsung Fire &amp; Marine Insurance"),
    ("2020", "Hyeonah Cho", "Samsung Electronics"),
    ("2020", "SungHee Kim", "Puzzle Data"),
    ("2020", "Jeongwoo Seo", "SK hynix"),
    ("2020", "Jongwon Kim", "LG Electronics"),
    ("2019", "Gyunam Park", "Eindhoven University of Technology"),
    ("2019", "Minkyu Choi", "Innodep"),
    ("2018", "Dohyeon Kim", "Trenbe"),
    ("2018", "Hojeong Yi", "SK hynix"),
    ("2017", "Yonghyeok Lee", "SK Innovation"),
    ("2016", "Tu Thi Bich Hong", "VF Corporation"),
    ("2015", "Minjeong Park", "SK hynix"),
    ("2014", "Sookyoung Son", "Hyundai Heavy Industries"),
    ("2012", "Hanna Yang", "Busan Metropolitan City"),
    ("2012", "Jason Jihoon Ree", "&mdash;"),
]


def photo_slug(name):
    """assets/img/people/<slug>.jpg — matches the filenames of the member photos."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def initials(name):
    parts = [p for p in re.split(r"\s+", name) if p]
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()


# --------------------------------------------------------------------------
# News
# --------------------------------------------------------------------------
def load_news():
    """Lab notices imported from aim.postech.ac.kr, English translation + Korean original."""
    with open(os.path.join(DATA, "news.json"), encoding="utf-8") as fh:
        posts = json.load(fh)
    posts.sort(key=lambda p: (p["date"], str(p["no"])), reverse=True)
    for p in posts:
        p["iso"] = p["date"].replace(".", "-")
        p["year"] = p["date"][:4]
        p["slug"] = news_slug(p)
        p["url"] = "/news/" + p["slug"]
        p["images"] = [
            f"/assets/img/news/{p['no']}-{i + 1}.jpg" for i in range(p.get("nimg", 0))
        ]
        p["thumb"] = f"/assets/img/news/thumb/{p['no']}.jpg" if p.get("nimg") else ""
        p["excerpt"] = (p.get("paras_en") or [""])[0]
    return posts


def news_slug(post):
    base = re.sub(r"[^a-z0-9]+", "-", post["title_en"].lower()).strip("-")
    words, out = base.split("-"), []
    for w in words:
        if len("-".join(out + [w])) > 60:
            break
        out.append(w)
    return f"{post['date'].replace('.', '-')}-{'-'.join(out) or post['no']}.html"


NEWS_TAGS = {"Notice": "Notice", "News": "News"}


# --------------------------------------------------------------------------
# Projects
# --------------------------------------------------------------------------
ONGOING_PROJECTS = [
    ("Manufacturing Foundation Model", "Large Language Models",
     "2025.09 &ndash; 2029.12", "Ministry of Trade, Industry and Energy",
     "A national programme with Seoul National University and KAIST to build foundation models for "
     "manufacturing."),
    ("Object-centric process mining: modelling, simulation and optimisation",
     "Process Mining", "2024.05 &ndash; 2029.04", "National Research Foundation of Korea",
     "Foundational research on object-centric event data, from discovery to simulation and optimisation."),
    ("Wil van der Aalst Data &amp; Process Science Research Center (Glocal R&amp;D Centre)",
     "Research Centre", "2025.01 &ndash; 2025.12", "Glocal University 30",
     "Operation of the lab's international research centre for data and process science."),
    ("Process-mining-converged AI for smart factory operation",
     "Process Mining &middot; Manufacturing", "2025.01 &ndash; 2025.12",
     "Korea Technology and Information Promotion Agency for SMEs",
     "Development and demonstration of AI-based smart factory operating technology for digital "
     "transformation in manufacturing."),
    ("AI-based OTT user and content analytics and video recommendation",
     "Recommender Systems", "2025.01 &ndash; 2025.12",
     "Institute for Information &amp; Communications Technology Planning &amp; Evaluation",
     "Analysis of viewing behaviour and content metadata to drive a video recommendation engine."),
]


def load_grants():
    with open(os.path.join(DATA, "grants.json"), encoding="utf-8") as fh:
        return json.load(fh)


CENTERS = [
    ("Wil van der Aalst Data &amp; Process Science Research Center",
     "Opened in 2024 and named after the founder of process mining, the centre anchors POSTECH's international "
     "research agenda in data and process science, hosting joint projects, visiting researchers and the "
     "Asia-Pacific Process Mining workshop series."),
    ("Future City Open Innovation Big Data Center",
     "A POSTECH centre applying big-data and process analytics to urban problems &mdash; mobility, shrinking cities, "
     "energy use and public services &mdash; in partnership with local government."),
    ("Puzzle Data (spin-off)",
     "Korea's first process mining software company, established as a spin-off from the lab. It brings the lab's "
     "process mining research into enterprise applications."),
    ("ZenAii Co. (spin-off)",
     "An AI-powered fashion recommendation company spun off from the lab, translating its research in recommender "
     "systems and artificial intelligence into personalised fashion services."),
]

PARTNERS = [
    "Samsung Electronics", "Samsung SDI", "Samsung C&amp;T", "POSCO", "SK hynix",
    "HD Hyundai", "LG Electronics", "Seoul National University Bundang Hospital",
    "National Research Foundation of Korea", "Korea Health Industry Development Institute",
    "IITP", "Ministry of Trade, Industry and Energy", "Puzzle Data", "ZenAii",
]


# --------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------
def build_index(journals, conferences, news):
    # Some entries are kept off the home page (see "home": false in news.json)
    home_news = [p for p in news if p.get("home", True)]
    news_items = "\n".join(news_row(p) for p in home_news[:5])

    areas = [
        ("Process Mining",
         "Discovering, monitoring, and improving real-world processes from event data, including process discovery, "
         "conformance checking, object-centric process mining, event abstraction, and predictive process monitoring."),
        ("Recommender Systems",
         "Developing personalized and context-aware recommendation methods, with a particular focus on fashion, "
         "customer preferences, and data-driven decision support."),
        ("Applied AI",
         "Developing AI and machine learning methods for real-world problems, including deep learning, generative AI, "
         "large language models, and domain-specific foundation models."),
        ("AI-Driven Process Innovation",
         "Combining process intelligence and AI to identify improvement opportunities, redesign workflows, automate "
         "decision-making, and develop new ways of working with human and AI collaboration."),
        ("Simulation &amp; Digital Twins",
         "Building data-driven simulation models and digital twins to understand, evaluate, and improve complex "
         "systems, particularly in manufacturing and healthcare."),
        ("Predictive &amp; Prescriptive Analytics",
         "Developing predictive and optimization methods to anticipate outcomes, recommend actions, allocate "
         "resources, and support better operational decisions."),
    ]
    area_cards = "\n".join(
        f"""      <div class="card"><span class="kicker">Research area</span><h3>{t}</h3><p>{d}</p></div>"""
        for t, d in areas
    )

    partner_pills = "\n".join(f"      <span>{p}</span>" for p in PARTNERS)

    body = f"""<section class="hero">
  <div class="wrap">
    <span class="eyebrow">POSTECH &middot; Industrial &amp; Management Engineering</span>
    <h1>Turning data into intelligence for processes and decisions.</h1>
    <p class="lead">The Analytics &amp; Information Management (AIM) Lab at POSTECH develops data-driven methods to
    understand how processes work, determine what should happen next, and build intelligent solutions for real-world
    problems.</p>
    <div class="hero-stats">
      <span class="hero-stat"><b>150+</b> Scientific publications</span>
      <span class="hero-stat"><b>70+</b> Funded research projects</span>
      <span class="hero-stat"><b>16</b> Current graduate students</span>
      <span class="hero-stat"><b>2</b> Spin-off companies</span>
    </div>
    <div class="btn-row">
      <a class="btn btn-primary" href="/research.html">Explore our research</a>
      <a class="btn btn-ghost" href="/join.html">Join the lab</a>
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="wrap">
    <div class="section-head">
      <h2>Research areas</h2>
      <p>Six areas the lab works in. They overlap far more than they compete &mdash; most projects pull on several
      at once.</p>
    </div>
    <div class="grid grid-3">
{area_cards}
    </div>
    <div class="btn-row"><a class="btn btn-ghost" href="/research.html">Research in detail</a></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2>About the Lab</h2>
    <figure class="lab-figure">
      <a href="/assets/img/lab-overview.jpg" target="_blank" rel="noopener" aria-label="Open the overview at full size">
        <picture>
          <source srcset="/assets/img/lab-overview.webp" type="image/webp">
          <img src="/assets/img/lab-overview.jpg" width="1536" height="1024" loading="lazy"
               alt="Overview of the AIM Lab: six research areas &mdash; Process Mining, Recommender Systems, Applied AI, AI-Driven Process Innovation, Simulation &amp; Digital Twins, and Predictive &amp; Prescriptive Analytics &mdash; arranged around the lab at the centre, leading to a From Data to Impact band underneath.">
        </picture>
      </a>
    </figure>
    <div class="prose" style="max-width:78ch">
      <p>The Analytics &amp; Information Management (AIM) Lab at POSTECH conducts research at the intersection of
      <strong>Process Mining, Recommender Systems, and Applied AI</strong>. We develop data-driven methods to
      understand how complex processes work, determine what should happen next, and build intelligent solutions for
      real-world problems.</p>
      <p>Our research combines <strong>artificial intelligence, machine learning, simulation, optimization, and
      digital twins</strong> to discover, predict, and improve process behavior, provide personalized recommendations,
      and support better operational decisions. Through these approaches, we aim to turn complex data into
      <strong>actionable intelligence and measurable improvement</strong>.</p>
      <p>A defining feature of the AIM Lab is our <strong>close collaboration with industry</strong>. Our research has
      been supported by the Korean government and leading companies including <strong>Samsung Electronics, Samsung
      C&amp;T, HD Hyundai, and POSCO</strong>, with projects spanning <strong>manufacturing, healthcare, and the
      fashion industry</strong>. These long-term collaborations provide opportunities to develop and validate new
      methods with real-world data and translate research into practical impact.</p>
      <p>The lab has published <strong>more than 150 scientific papers</strong> in leading journals and conferences,
      including <em>Decision Support Systems</em>, <em>Information Systems</em>, <em>Journal of Information
      Technology</em>, <em>International Journal of Medical Informatics</em>, Business Process Management (BPM), and
      the International Conference on Process Mining (ICPM).</p>
      <p>We are equally committed to translating research into practice.
      <strong><a href="https://www.puzzledata.com/" rel="noopener">Puzzle Data</a></strong>, Korea&rsquo;s first
      process mining software company, was established as a spin-off from the AIM Lab, bringing process mining
      research into enterprise applications. <strong>ZenAii Co.</strong>, an AI-powered fashion recommendation
      company, was also spun off from the lab, translating our research in recommender systems and AI into
      personalized fashion services. Together, these ventures demonstrate our commitment to turning academic research
      into technologies, solutions, and businesses with real-world impact.</p>
      <div class="btn-row">
        <a class="btn btn-ghost" href="/members/students/">Meet the team</a>
        <a class="btn btn-ghost" href="/publications/">Publications</a>
      </div>
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="wrap">
    <div class="section-head">
      <h2>Latest news</h2>
      <p>Awards, appointments and events from the lab.</p>
    </div>
    <ul class="news-list">
{news_items}
    </ul>
    <div class="btn-row"><a class="btn btn-ghost" href="/news.html">All news</a></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <h2>Partners and funding</h2>
      <p>Our research is carried out with government agencies, hospitals and industry.</p>
    </div>
    <div class="logos">
{partner_pills}
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="wrap">
    <div class="cta">
      <div>
        <h2>Considering graduate study?</h2>
        <p>We look for students who enjoy both the modelling and the messiness of real data. Ph.D., M.S. and
        undergraduate research positions open every semester.</p>
      </div>
      <a class="btn btn-primary" href="/join.html">How to apply</a>
    </div>
  </div>
</section>
"""
    return page(
        "index.html",
        "AIM Lab, POSTECH — Analytics & Information Management Laboratory",
        "The Analytics & Information Management Lab at POSTECH works on process mining, recommender systems and "
        "applied AI, with industry partners in manufacturing, healthcare and fashion.",
        body,
    )


RESEARCH_AREAS = [
    ("Process Mining",
     "We develop methods to <strong>discover, analyze, predict, and improve real-world processes from event data</strong>, "
     "transforming operational data into actionable process intelligence.",
     ["<strong>Object-centric process mining</strong> and process discovery",
      "<strong>Event abstraction</strong>, conformance checking, and predictive monitoring",
      "Process visualization, organizational mining, and process optimization"]),
    ("Recommender Systems",
     "We develop <strong>personalized and context-aware recommendation technologies</strong> that help users make better "
     "choices, with a particular focus on the <strong>fashion industry</strong>.",
     ["Personalized <strong>product, outfit, and fashion recommendation</strong>",
      "User preference and behavioral modeling",
      "Context-aware and AI-enhanced recommendation"]),
    ("Applied AI",
     "We develop and apply <strong>AI and machine learning technologies to real-world problems</strong>, combining "
     "advanced models with domain knowledge and operational data.",
     ["<strong>Generative AI, large language models, and AI agents</strong>",
      "<strong>Domain-specific foundation models</strong>",
      "Deep learning, multimodal AI, and explainable AI"]),
    ("AI-Driven Process Innovation",
     "We combine <strong>process intelligence and AI to redesign how organizations operate</strong>, moving beyond "
     "process analysis toward intelligent and adaptive ways of working.",
     ["AI-assisted <strong>process redesign and improvement</strong>",
      "Generative AI and agents for process innovation",
      "<strong>Human&ndash;AI collaboration</strong> and intelligent workflow automation"]),
    ("Simulation &amp; Digital Twins",
     "We build <strong>data-driven simulation models and digital twins</strong> to evaluate alternatives and improve "
     "complex systems before changes are implemented in the real world.",
     ["<strong>Process digital twins</strong> and automated simulation modeling",
      "What-if analysis and scenario evaluation",
      "Applications in <strong>manufacturing and healthcare</strong>"]),
    ("Predictive &amp; Prescriptive Analytics",
     "We integrate <strong>prediction, optimization, and decision support</strong> to anticipate outcomes and determine "
     "what actions should be taken next.",
     ["Process performance prediction",
      "<strong>Resource allocation and optimization</strong>",
      "Data-driven operational decision support"]),
]

RESEARCH_DOMAINS = [
    ("Manufacturing",
     "We apply <strong>process mining, AI, simulation, and optimization</strong> to semiconductor manufacturing, steel "
     "production, smart factories, and other complex manufacturing systems."),
    ("Healthcare",
     "We develop <strong>process intelligence, predictive analytics, and digital twins</strong> for clinical pathways, "
     "hospital operations, patient flows, and healthcare decision support."),
    ("Fashion",
     "We develop <strong>AI-powered recommender systems</strong> for personalized fashion services, including product "
     "recommendation, outfit recommendation, customer preference modeling, and intelligent curation."),
]


def build_research():
    area_cards = "\n".join(
        '      <div class="card area-card">\n'
        f'        <h3>{title}</h3>\n'
        f'        <p>{desc}</p>\n'
        '        <ul class="topics">\n'
        + "\n".join(f"          <li>{t}</li>" for t in topics)
        + "\n        </ul>\n      </div>"
        for title, desc, topics in RESEARCH_AREAS
    )
    domain_cards = "\n".join(
        f'      <div class="card"><h3>{t}</h3><p>{d}</p></div>' for t, d in RESEARCH_DOMAINS
    )

    body = f"""
<section class="section" style="padding:30px 0 22px">
  <div class="wrap">
    <div class="research-intro">
      <h1 class="lede-head">What We Work On</h1>
      <div>
      <p class="lede">Our research is centered on <strong>Process Mining, Recommender Systems, and Applied AI</strong>,
      complemented by <strong>AI-Driven Process Innovation, Simulation &amp; Digital Twins, and Predictive &amp;
      Prescriptive Analytics</strong>.</p>
      <p class="lede">Together, these areas enable us to understand complex processes, predict what happens next,
      recommend better actions, and develop intelligent solutions for real-world problems.</p>
      </div>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="grid grid-3" style="gap:14px">
{area_cards}
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="wrap">
    <div class="section-head">
      <h2>Application Domains</h2>
      <p>Our research is grounded in real-world challenges and strengthened through long-term collaboration with
      industry and public-sector partners.</p>
    </div>
    <div class="grid grid-3">
{domain_cards}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="prose">
      <h2>From Data to Impact</h2>
      <p>Our research areas are deeply interconnected. We combine <strong>process mining with AI</strong>, predictions
      with <strong>optimization</strong>, process data with <strong>digital twins</strong>, and recommender systems
      with <strong>generative AI</strong> to address complex real-world problems.</p>
      <p>Our goal is to move from data to <strong>understanding, prediction, recommendation, innovation, and
      measurable real-world impact</strong>.</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="/publications/">View our publications &rarr;</a>
        <a class="btn btn-ghost" href="/projects.html">Explore our projects &rarr;</a>
      </div>
    </div>
  </div>
</section>
"""
    return page(
        "research.html",
        "Research — AIM Lab, POSTECH",
        "Process mining, recommender systems, applied AI, AI-driven process innovation, simulation and digital twins, "
        "and predictive and prescriptive analytics at POSTECH's AIM Lab.",
        body,
    )


MEMBER_INTRO = {
    "members/index.html": (
        "Members",
        "The people of the Analytics &amp; Information Management Lab.",
    ),
    "members/professor/index.html": (
        "Professor",
        "The principal investigator of the lab.",
    ),
    "members/emeritus/index.html": (
        "Emeritus Professors",
        "Faculty who shaped the lab and remain part of its wider circle.",
    ),
    "members/students/index.html": (
        "Students",
        "Ph.D. and M.S. researchers currently in the lab.",
    ),
    "members/alumni/index.html": (
        "Alumni",
        "Post-doctoral researchers and graduates of the lab, and where they went next.",
    ),
}


def obfuscate(email):
    """Write an address the way lab sites do, to keep it away from scrapers."""
    local, _, domain = email.partition("@")
    return local + " (at) " + domain.replace(".", " (dot) ")


def member_page(slug, body_sections):
    heading, sub = MEMBER_INTRO[slug]
    body = page_head("Members", heading, sub) + body_sections
    return page(
        slug,
        f"{heading} — AIM Lab, POSTECH",
        re.sub(r"&[a-z]+;", "&", sub),
        body,
    )


def build_members_index():
    phd = sum(1 for _, r, _, _ in STUDENTS if r.startswith("Ph.D."))
    ms = len(STUDENTS) - phd
    alumni_total = len(POSTDOC_ALUMNI) + len(PHD_ALUMNI) + len(MS_ALUMNI)
    cards = [
        ("members/professor/index.html", "Professor",
         "Minseok Song, Ph.D. &mdash; principal investigator, and the centres he directs.",
         "1 faculty member"),
        ("members/emeritus/index.html", "Emeritus Professors",
         "Euiho Suh, Ph.D. &mdash; Professor Emeritus of the department.",
         "1 emeritus professor"),
        ("members/students/index.html", "Students",
         "Ph.D. and M.S. researchers currently in the lab.",
         f"{phd} Ph.D. &middot; {ms} M.S."),
        ("members/alumni/index.html", "Alumni",
         "Where members of the lab went next, from 2012 onwards.",
         f"{alumni_total} alumni"),
    ]
    grid = "\n".join(
        f'''      <a class="card member-card" href="{nav_url(h)}">
        <span class="kicker">{count}</span>
        <h3>{title}</h3>
        <p>{desc}</p>
      </a>'''
        for h, title, desc, count in cards
    )
    return member_page("members/index.html", f"""
<section class="section">
  <div class="wrap">
    <div class="grid grid-2">
{grid}
    </div>
  </div>
</section>
""")


PROF_ROLES = [
    "Vice President of Planning, POSTECH",
    "Director, Wil van der Aalst Data &amp; Process Science Research Center, POSTECH",
    "Director, Future City Open Innovation Center, POSTECH",
    "Team Leader, BK21 Data &amp; Process Science Research Team, POSTECH",
    "Founder and CEO, ZenAii Co.",
    "Associate Editor, <em>Business &amp; Information Systems Engineering</em> (BISE)",
    "Editorial Board Member, <em>Process Science</em>",
    "Steering Committee Member, IEEE Task Force on Process Mining",
    "Associated Member, European Research Center for Information Systems (ERCIS)",
]

PROF_APPOINTMENTS = [
    ("2025 &ndash; present", "Vice President of Planning, POSTECH"),
    ("2025 &ndash; present", "Board Member, POSTECH Holdings"),
    ("2024 &ndash; present", "Director, Wil van der Aalst Data &amp; Process Science Research Center, POSTECH"),
    ("2024 &ndash; present", "Team Leader, BK21 Data &amp; Process Science Research Team, POSTECH"),
    ("2024 &ndash; present", "Founder and CEO, ZenAii Co."),
    ("2023 &ndash; present", "Director, Future City Open Innovation Center, POSTECH"),
    ("2022 &ndash; present", "Full Professor, Dept. of Industrial &amp; Management Engineering, POSTECH"),
    ("2023 &ndash; 2025", "Head, Dept. of Industrial &amp; Management Engineering, POSTECH"),
    ("2018 &ndash; 2024", "Director, Open Innovation Big Data Center, POSTECH"),
    ("2016 &ndash; 2021", "Associate Professor, Dept. of Industrial &amp; Management Engineering, POSTECH"),
    ("2015 &ndash; 2016", "Founder and CEO, Puzzle Data Co."),
    ("2014 &ndash; 2015", "Dean, Academic Information Affairs Office, UNIST"),
    ("2014 &ndash; 2015", "Associate Professor, School of Business Administration, UNIST"),
    ("2012 &ndash; 2013", "Dean (interim), School of Business Administration, UNIST"),
    ("2010 &ndash; 2013", "Assistant Professor, School of Business Administration, UNIST"),
    ("2006 &ndash; 2009", "Postdoctoral Researcher, TU Eindhoven (with Prof. Wil van der Aalst)"),
]

PROF_SERVICE = [
    ("2025 &ndash; present", "Associate Editor, <em>Business &amp; Information Systems Engineering</em> (BISE)"),
    ("2025 &ndash; present", "Editorial Board Member, <em>Process Science</em>"),
    ("2024 &ndash; present", "Steering Committee Member, IEEE Task Force on Process Mining"),
    ("2024", "Program Chair, International Conference on Process Mining (ICPM 2024)"),
    ("2022 &ndash; 2025", "Review Board Member, ICT Convergence &ndash; Industrial Engineering Division, "
                          "National Research Foundation of Korea"),
    ("2021", "Chair, BPM 2021 Industry Forum"),
    ("2013 &ndash; present", "Associated Member, European Research Center for Information Systems (ERCIS)"),
]

PROF_EDUCATION = [
    ("2006", "Ph.D., Dept. of Industrial &amp; Management Engineering, POSTECH "
             "(advisor: Prof. Injun Choi)"),
]

PROF_HONORS = [
    ("2025", "Best Paper Award, Responsible BPM Forum, International Conference on Business Process Management"),
    ("2023", "Grand Prize, CDE DX Award (Minister of Science and ICT Award), Korean Society of CAD/CAM Engineers"),
    ("2022", "Best Paper Award, The Korean Society of Medical Informatics"),
    ("2021 &ndash; 2022", "Mueunje Chair Professor, POSTECH"),
    ("2021", "Young Researcher Award, Society for Industrial and Applied Mathematics Korea (SIAM Korea)"),
    ("2021", "Proud Postechian Award (Education), POSTECH"),
    ("2020", "Minister of Trade, Industry and Energy Award (1st Prize), Korea Industrial Research Project Challenge"),
]


def timeline(rows):
    items = "\n".join(
        f'      <li><span class="when">{when}</span><span class="what">{what}</span></li>'
        for when, what in rows
    )
    return f'    <ul class="timeline">\n{items}\n    </ul>'


def build_members_professor():
    roles = "\n".join(f"          <li>{r}</li>" for r in PROF_ROLES)
    return member_page("members/professor/index.html", f"""
<section class="section">
  <div class="wrap">
    <div class="pi-card">
      <img class="pi-photo" src="/assets/img/people/minseok-song.jpg" alt="Minseok Song" width="512" height="512">
      <div>
        <h2>Minseok Song (송민석), Ph.D.</h2>
        <p class="pi-role">Mueunje Professor &middot; Principal Investigator</p>
        <p class="pi-affil">Department of Industrial &amp; Management Engineering<br>
        Pohang University of Science and Technology (POSTECH)<br>
        77 Cheongam-ro, Nam-gu, Pohang, Gyeongbuk 37673, Republic of Korea</p>
        <ul class="role-list">
{roles}
        </ul>
        <ul class="meta-list">
          <li><span class="k">Office</span><span>Engineering Building 4, Room 223</span></li>
          <li><span class="k">Telephone</span><span><a href="tel:+82542792376">+82-54-279-2376</a></span></li>
          <li><span class="k">Contact</span><span>mssong (at) postech (dot) ac (dot) kr</span></li>
          <li><span class="k">Web</span><span><a href="https://minseoksong.github.io/" rel="noopener">minseoksong.github.io</a></span></li>
          <li><span class="k">Profiles</span><span><a href="https://scholar.google.com/citations?user=8ACzAlkAAAAJ" rel="noopener">Google Scholar</a> &middot; <a href="https://dblp.org/pid/71/4935.html" rel="noopener">DBLP</a></span></li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section section-soft" style="padding-top:56px">
  <div class="wrap">
    <h2 class="member-group">Appointments</h2>
{timeline(PROF_APPOINTMENTS)}

    <h2 class="member-group" style="margin-top:56px">Service</h2>
{timeline(PROF_SERVICE)}

    <h2 class="member-group" style="margin-top:56px">Education</h2>
{timeline(PROF_EDUCATION)}

    <h2 class="member-group" style="margin-top:56px">Honors &amp; Awards</h2>
{timeline(PROF_HONORS)}

  </div>
</section>
""")


def build_members_emeritus():
    return member_page("members/emeritus/index.html", """
<section class="section">
  <div class="wrap">
    <div class="pi-card">
      <img class="pi-photo" src="/assets/img/people/euiho-suh.jpg" alt="Euiho Suh" width="360" height="360">
      <div>
        <h3>Euiho Suh (서의호), Ph.D.</h3>
        <p class="pi-role">Professor Emeritus &middot; VP &amp; Chair Professor</p>
        <p>Euiho Suh is Professor Emeritus of the Department of Industrial &amp; Management Engineering at POSTECH and a
        founding figure of the lab's research programme in information management and knowledge management systems.
        He is currently at aSSIST University.</p>
        <ul class="meta-list">
          <li><span class="k">Position</span><span>Professor Emeritus (VP &amp; Chair Professor)</span></li>
          <li><span class="k">Affiliation</span><span>aSSIST University</span></li>
          <li><span class="k">Telephone</span><span><a href="tel:+82542795920">+82-54-279-5920</a></span></li>
          <li><span class="k">Contact</span><span>ehsuh (at) postech (dot) ac (dot) kr</span></li>
        </ul>
      </div>
    </div>
  </div>
</section>
""")


def student_card(n, r, m, y):
    dept = r.split(", ", 1)[1] if ", " in r else ""
    return f'''      <div class="person">
        <img class="photo" src="/assets/img/people/{photo_slug(n)}.jpg" alt="{n}" width="360" height="360" loading="lazy">
        <div class="person-body">
          <h4>{n}</h4>
          <p class="role">{dept}<br>Joined {y}</p>
          <p class="mail">Contact: {obfuscate(m)}</p>
        </div>
      </div>'''


def build_members_students():
    groups = [
        ("Ph.D. Students", [s for s in STUDENTS if s[1].startswith("Ph.D.")]),
        ("M.S. Students", [s for s in STUDENTS if s[1].startswith("M.S.")]),
    ]
    blocks = []
    for label, members in groups:
        if not members:
            continue
        cards = "\n".join(student_card(*m) for m in members)
        blocks.append(f'''    <h2 class="member-group">{label} <span>{len(members)}</span></h2>
    <div class="grid grid-4" style="margin-bottom:56px">
{cards}
    </div>''')
    return member_page("members/students/index.html", f"""
<section class="section">
  <div class="wrap">
{chr(10).join(blocks)}
  </div>
</section>

<section class="section section-soft">
  <div class="wrap">
    <div class="cta">
      <div>
        <h2>Thinking of joining them?</h2>
        <p>Ph.D., M.S. and undergraduate research positions open every semester.</p>
      </div>
      <a class="btn btn-primary" href="/join.html">How to apply</a>
    </div>
  </div>
</section>
""")


def build_members_alumni():
    postdocs = "\n".join(
        f"        <tr><td>{n}</td><td>{p}</td><td>{d}</td></tr>" for n, p, d in POSTDOC_ALUMNI
    )
    phds = "\n".join(
        f"        <tr><td>{y}</td><td>{n}</td><td>{d}</td></tr>" for y, n, d in PHD_ALUMNI
    )
    ms = "\n".join(
        f"        <tr><td>{y}</td><td>{n}</td><td>{d}</td></tr>" for y, n, d in MS_ALUMNI
    )
    return member_page("members/alumni/index.html", f"""
<section class="section">
  <div class="wrap">
    <h2 class="member-group">Post-doctoral Researchers <span>{len(POSTDOC_ALUMNI)}</span></h2>
    <div class="table-scroll">
      <table>
        <thead><tr><th>Name</th><th>Period</th><th>Now at</th></tr></thead>
        <tbody>
{postdocs}
        </tbody>
      </table>
    </div>

    <h2 class="member-group" style="margin-top:56px">Doctoral <span>{len(PHD_ALUMNI)}</span></h2>
    <div class="table-scroll">
      <table>
        <thead><tr><th>Year</th><th>Name</th><th>Now at</th></tr></thead>
        <tbody>
{phds}
        </tbody>
      </table>
    </div>

    <h2 class="member-group" style="margin-top:56px">Master's <span>{len(MS_ALUMNI)}</span></h2>
    <div class="table-scroll">
      <table>
        <thead><tr><th>Year</th><th>Name</th><th>Now at</th></tr></thead>
        <tbody>
{ms}
        </tbody>
      </table>
    </div>
  </div>
</section>
""")


PUBLICATION_INTRO = {
    "publications/index.html": (
        "Publications",
        "Journal articles and international conference papers from the lab, from 2001 to today.",
    ),
    "publications/journal/index.html": (
        "Journal Articles",
        "Peer-reviewed journal articles, newest first — with DOI, BibTeX and the paper where available.",
    ),
    "publications/conference/index.html": (
        "Conference Papers",
        "Conference and workshop papers, newest first — with DOI and BibTeX.",
    ),
}


def publication_page(slug, body_sections):
    heading, sub = PUBLICATION_INTRO[slug]
    body = page_head("Publications", heading, sub) + body_sections
    return page(
        slug,
        f"{heading} — AIM Lab, POSTECH",
        re.sub(r"&[a-z]+;", "&", sub),
        body,
    )


def build_publications_index(journals, conferences):
    j_years = f"{min(p['year'] for p in journals)}&ndash;{max(p['year'] for p in journals)}"
    c_years = f"{min(p['year'] for p in conferences)}&ndash;{max(p['year'] for p in conferences)}"
    cards = [
        ("publications/journal/index.html", "Journal Articles",
         "Peer-reviewed articles in venues such as <em>Decision Support Systems</em>, "
         "<em>Information Systems</em>, the <em>Journal of Information Technology</em> and the "
         "<em>International Journal of Medical Informatics</em>.",
         f"{len(journals)} articles &middot; {j_years}"),
        ("publications/conference/index.html", "Conference Papers",
         "Conference and workshop papers, including BPM, ICPM, CAiSE, INFORMS and the "
         "Winter Simulation Conference.",
         f"{len(conferences)} papers &middot; {c_years}"),
    ]
    grid = "\n".join(
        f'''      <a class="card member-card" href="{nav_url(h)}">
        <span class="kicker">{count}</span>
        <h3>{title}</h3>
        <p>{desc}</p>
      </a>'''
        for h, title, desc, count in cards
    )
    return publication_page("publications/index.html", f"""
<section class="section">
  <div class="wrap">
    <div class="grid grid-2">
{grid}
    </div>
    <p class="small muted" style="margin-top:32px">Every entry carries a BibTeX record; papers whose
    author copy is available also carry a PDF. The record is also indexed on
    <a href="https://dblp.org/pid/71/4935.html" rel="noopener">DBLP</a>.</p>
  </div>
</section>
""")


RIGHTS_NOTE = """    <p class="small muted rights-note">PDFs linked here are author copies, posted under each
    publisher's author-rights policy and provided for personal and classroom use only; copyright
    remains with the respective publishers. Articles in the <em>Communications of the Association for
    Information Systems</em> are &copy; the Association for Information Systems and may not be used
    for profit &mdash; see the journal at
    <a href="https://aisel.aisnet.org/cais/" rel="noopener">aisel.aisnet.org/cais</a>.</p>"""


def build_publications_list(slug, items, list_id, noun):
    note = RIGHTS_NOTE if any(i.get("pdf") for i in items) else ""
    return publication_page(slug, f"""
<section class="section">
  <div class="wrap">
    <p class="count-note">Showing <span id="{list_id}-count">{len(items)}</span> of {len(items)} {noun}.</p>
    {FILTER_BAR.format(lid=list_id)}
    {render_pubs(items, list_id)}
{note}
  </div>
</section>
""")


PROJECTS_BODY = """
<section class="section" style="padding-bottom:40px">
  <div class="wrap">
    <div class="section-head">
      <h2>Ongoing projects</h2>
      <p>Programmes the lab is running now, with national agencies and industry.</p>
    </div>
    <div class="grid grid-2">
{cards}
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="wrap">
    <div class="section-head">
      <h2>Research grants</h2>
      <p>{n} funded projects since 2002, {pi} of them as principal investigator, with the Korean government,
      hospitals and industry.</p>
    </div>
    <ul class="timeline grants">
{grant_rows}
    </ul>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <h2>Centers and spin-offs</h2>
      <p>The lab anchors two research centres at POSTECH and two companies.</p>
    </div>
    <div class="grid grid-3">
{centres}
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="wrap">
    <div class="section-head">
      <h2>Partners and funding bodies</h2>
    </div>
    <div class="logos">
{partner_pills}
    </div>
  </div>
</section>
"""


def build_projects():
    grants = load_grants()

    card_list = []
    for title, tag, period, funder, desc in ONGOING_PROJECTS:
        card_list.append(
            '      <div class="card">\n'
            f'        <span class="kicker">{tag}</span>\n'
            f'        <h3>{title}</h3>\n'
            f'        <p>{desc}</p>\n'
            '        <ul class="meta-list" style="margin-top:14px">\n'
            f'          <li><span class="k">Period</span><span>{period}</span></li>\n'
            f'          <li><span class="k">Funder</span><span>{funder}</span></li>\n'
            '        </ul>\n      </div>'
        )
    cards = "\n".join(card_list)

    ROLE = {"PI": "PI", "CO-PI": "Co-PI", "RESEARCHER": "Researcher"}
    rows = []
    for g in grants:
        bits = [g["funder"]] if g["funder"] else []
        if g["role"]:
            bits.append(ROLE.get(g["role"], g["role"]))
        meta = " &middot; ".join(html.escape(x) for x in bits)
        rows.append(
            f'      <li><span class="when">{g["period"]}</span>'
            f'<span class="what">{html.escape(g["title"])}'
            f'<span class="grant-meta">{meta}</span></span></li>'
        )
    grant_rows = "\n".join(rows)
    pi = sum(1 for g in grants if g["role"] == "PI")

    centres = "\n".join(
        f'      <div class="card"><h3>{t}</h3><p>{d}</p></div>' for t, d in CENTERS
    )
    partner_pills = "\n".join(f"      <span>{p}</span>" for p in PARTNERS)

    body = page_head(
        "Projects &amp; Centers", "Projects and centers",
        "Funded research projects, the centres the lab anchors, and its partners."
    ) + PROJECTS_BODY.format(
        cards=cards, grant_rows=grant_rows, centres=centres,
        partner_pills=partner_pills, n=len(grants), pi=pi,
    )
    return page(
        "projects.html",
        "Projects & Centers — AIM Lab, POSTECH",
        "Funded research projects, research centres and spin-off companies of POSTECH's Analytics & "
        "Information Management Lab.",
        body,
    )


def news_row(p):
    ko = f' <span class="ko">({html.escape(p["title"])})</span>' if p.get("title") else ""
    thumb = (
        f'<img class="news-thumb" src="{p["thumb"]}" alt="" width="176" height="176" loading="lazy">'
        if p["thumb"] else ""
    )
    excerpt = html.escape(p["excerpt"][:160] + ("…" if len(p["excerpt"]) > 160 else ""))
    return f"""      <li class="news-item" data-tags="y{p['year']}">
        <time datetime="{p['iso']}">{p['date']}</time>
        <div class="news-main">
          <h3><span class="tag">{p['cat']}</span><a href="{p['url']}">{html.escape(p['title_en'])}{ko}</a></h3>
          <p>{excerpt}</p>
        </div>
        {thumb}
      </li>"""


def build_news(posts):
    years = sorted({p["year"] for p in posts}, reverse=True)
    filters = "\n".join(
        f'  <button data-filter="y{y}" aria-pressed="false">{y}</button>' for y in years
    )
    groups = []
    for y in years:
        rows = "\n".join(news_row(p) for p in posts if p["year"] == y)
        groups.append(
            f'  <div data-group>\n    <div class="pub-year">{y}</div>\n'
            f'    <ul class="news-list">\n{rows}\n    </ul>\n  </div>'
        )
    body = page_head(
        "News",
        "News and events",
        "Awards, appointments, conferences and lab milestones, from 2015 to today. "
        "Each entry is translated into English; the Korean original is kept on every page."
    ) + f"""
<section class="section">
  <div class="wrap">
    <p class="count-note">Showing <span id="news-count">{len(posts)}</span> of {len(posts)} entries.</p>
    <div class="filters" data-filter-bar="#news">
      <button data-filter="all" aria-pressed="true">All</button>
{filters}
    </div>
    <div id="news">
{chr(10).join(groups)}
    </div>
  </div>
</section>
"""
    return page(
        "news.html",
        "News — AIM Lab, POSTECH",
        "Awards, appointments and events from the Analytics & Information Management Lab at POSTECH, "
        "from 2015 to today.",
        body,
    )


def build_news_detail(p, prev_p, next_p):
    paras = "\n".join(
        f"      <p>{html.escape(t)}</p>" for t in (p.get("paras_en") or [])
    ) or '      <p class="muted">This entry has no body text.</p>'

    if p["images"]:
        figs = "\n".join(
            f'        <a class="news-figure" href="{src}"><img src="{src}" alt="{html.escape(p["title_en"])} — photo {i + 1}" loading="lazy"></a>'
            for i, src in enumerate(p["images"])
        )
        gallery = f"""
    <div class="news-gallery{' single' if len(p['images']) == 1 else ''}">
{figs}
    </div>"""
    else:
        gallery = ""

    ko_title = (
        f'<span class="ko">({html.escape(p["title"])})</span>' if p.get("title") else ""
    )
    more = (
        f'      <p class="news-more"><a href="{p["more"]}">Read more &rarr;</a></p>'
        if p.get("more") else ""
    )
    if p.get("paras"):
        ko_paras = "\n".join(f"        <p>{html.escape(t)}</p>" for t in p["paras"])
        original = (
            '      <details class="news-original">\n'
            "        <summary>Korean original &middot; 원문 보기</summary>\n"
            f"        <h3>{html.escape(p['title'])}</h3>\n"
            f"{ko_paras}\n"
            '        <p class="small muted">Originally published on the\n'
            '        <a href="https://aim.postech.ac.kr/aim2/bbs/notice.do?mode=view&amp;articleNo='
            f'{p["no"]}" rel="noopener">AIM Lab board</a>\n'
            f"        on {p['date']}.</p>\n"
            "      </details>"
        )
    else:
        original = ""

    nav_links = []
    if next_p:
        nav_links.append(
            f'      <a class="news-nav-item" href="{next_p["url"]}">'
            f'<span>&larr; Newer</span>{html.escape(next_p["title_en"][:70])}</a>'
        )
    if prev_p:
        nav_links.append(
            f'      <a class="news-nav-item align-right" href="{prev_p["url"]}">'
            f'<span>Older &rarr;</span>{html.escape(prev_p["title_en"][:70])}</a>'
        )

    body = f"""<section class="section">
  <div class="wrap">
    <article class="news-article">
      <a class="back-link" href="/news.html">&larr; All news</a>
      <p class="news-meta">{p['cat']} &middot; {p['date']}</p>
      <h1 class="news-title">{html.escape(p['title_en'])}{ko_title}</h1>
{paras}
{more}
{gallery}
{original}
    </article>

    <nav class="news-nav">
{chr(10).join(nav_links)}
    </nav>
  </div>
</section>
"""
    desc = (p["excerpt"] or p["title_en"])[:180]
    return page(
        "news/" + p["slug"],
        f"{p['title_en']} — AIM Lab, POSTECH",
        desc,
        body,
    )


def build_join():
    body = page_head(
        "Join Us",
        "Join the lab",
        "We recruit Ph.D. students, M.S. students and undergraduate researchers every semester."
    ) + """
<section class="section">
  <div class="wrap">
    <div class="grid grid-2" style="gap:56px;align-items:start">
      <div class="prose">
        <h2>Who we look for</h2>
        <p>Research in the lab sits between three things: a real process, the messy data it leaves behind, and a method
        strong enough to say something true about both. The students who do well here enjoy all three, not just the third.</p>
        <p>Concretely, we look for:</p>
        <ul>
          <li>A background in industrial engineering, computer science, statistics, information systems or a related field</li>
          <li>Comfort with programming &mdash; Python is the lab's working language</li>
          <li>Curiosity about how organisations actually operate, and patience with imperfect data</li>
          <li>Willingness to write and present in English; much of our collaboration is international</li>
        </ul>
        <p>Prior experience with process mining is welcome but not expected. Most students learn it here.</p>

        <h2>Positions</h2>
        <h3>Ph.D. students</h3>
        <p>Full funding through research assistantships. Ph.D. students lead a research agenda, publish at venues such as
        BPM, ICPM and top information-systems journals, and typically spend time with our international partners.</p>
        <h3>M.S. students</h3>
        <p>Two-year programme combining coursework with an industry-facing research project. Many M.S. projects run
        directly with a partner company and end in a deployed prototype.</p>
        <h2>대학원 입학 프로그램 <span class="h2-en">Graduate admission programmes</span></h2>
        <p>아래 네 개 대학원 프로그램 중 하나로 진학할 수 있습니다. 지원하는 프로그램에 따라 교과 과정 및 전형 일정이
        다르니, 어떤 프로그램이 맞을지 고민해 보고, 판단이 어려우면 지원 전에 먼저 문의해 주기 바랍니다.</p>
        <p class="prog-en">Students enter through one of the four POSTECH graduate programmes below. Curricula and
        admission schedules differ by programme, so consider which one suits you &mdash; and ask us before applying if
        you are unsure.</p>
        <ul class="prog-list">
          <li>
            <a href="https://ime.postech.ac.kr/" rel="noopener">산업경영공학과</a>
            <span class="en-name">Department of Industrial &amp; Management Engineering</span>
            <span>연구실이 소속된 학과입니다. 가장 일반적인 경로이며, 프로세스 마이닝과 운영·데이터 기반 의사결정을
            가장 폭넓게 다룹니다.</span>
          </li>
          <li>
            <a href="https://ax.postech.ac.kr/" rel="noopener">인공지능융합대학원 (AX)</a>
            <span class="en-name">Graduate School of Artificial Intelligence Convergence</span>
            <span>인공지능과 산업 전환이 만나는 주제 &mdash; AI 기반 프로세스 인텔리전스, 실제 운영에 적용하는
            에이전틱·생성형 방법론을 다루고자 하는 경우에 적합합니다.</span>
          </li>
          <li>
            <a href="https://ids.postech.ac.kr/index_ko" rel="noopener">융합대학원 산업데이터사이언스전공 (IDS)</a>
            <span class="en-name">Industrial Data Science, Graduate School of Convergence</span>
            <span>대규모 제조·기업 데이터를 토대로 연구를 설계하려는 학생에게 적합한 산업 지향 프로그램입니다.</span>
          </li>
          <li>
            <a href="https://dst.postech.ac.kr/" rel="noopener">국방과학기술전공 (DST)</a>
            <span class="en-name">Defense Science and Technology</span>
            <span>분석·시뮬레이션·프로세스 인텔리전스를 국방 분야에 응용하려는 경우의 경로입니다.</span>
          </li>
        </ul>

        <h2>How to apply</h2>
        <p>Admission is through POSTECH's graduate admissions process in one of the programmes above, but contact the lab
        first &mdash; we can tell you whether there is a fit, and which programme suits you, before you invest in an
        application. Write to
        <a href="mailto:mssong@postech.ac.kr">mssong@postech.ac.kr</a> with the subject line
        <em>&ldquo;Prospective student &mdash; [your name]&rdquo;</em> and include:</p>
        <ul>
          <li>A CV, including your transcript and any publications or projects</li>
          <li>A short paragraph on which of our research areas interests you and why</li>
          <li>Your intended start semester, degree, and which of the four admission programmes you are considering</li>
        </ul>
        <p>Applications from international students are welcome. POSTECH offers graduate programmes taught in English and
        supports visa and housing arrangements for admitted students.</p>
      </div>

      <div>
        <div class="callout join-aside" style="margin-top:0">
          <h3>What you get</h3>
          <ul style="margin:0;padding-left:1.1em">
            <li>Funded research assistantship for graduate students</li>
            <li>Real event data from manufacturing, hospitals and public agencies</li>
            <li>Co-authorship on international publications</li>
            <li>Conference travel, including BPM, ICPM and INFORMS</li>
            <li>Collaboration with the Wil van der Aalst Data &amp; Process Science Research Center and its visitors</li>
            <li>A strong industry placement record &mdash; Samsung, SK hynix, LG, POSCO, and academia</li>
          </ul>
        </div>

      </div>
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="wrap">
    <div class="section-head"><h2>Frequently asked</h2></div>
    <div class="grid grid-2">
      <div class="card"><h3>Do I need a process-mining background?</h3><p>No. A solid grounding in programming and
      statistics matters more; process mining itself is taught in the lab and in POSTECH coursework.</p></div>
      <div class="card"><h3>Is the programme in English?</h3><p>Graduate courses relevant to the lab are offered in
      English, and lab meetings accommodate international members. Korean is useful for industry projects but not required.</p></div>
      <div class="card"><h3>Which programme should I apply to?</h3><p>Industrial &amp; Management Engineering is the
      default. Choose AX, Industrial Data Science or Defense Science and Technology if its focus matches the work you
      want to do &mdash; the advisor and the lab are the same either way. Ask us if you are unsure.</p></div>
      <div class="card"><h3>Is funding available?</h3><p>Graduate students in the lab are supported through research
      assistantships on funded projects.</p></div>
      <div class="card"><h3>Can I visit or intern?</h3><p>Yes &mdash; we host visiting students and researchers, especially
      through the Wil van der Aalst Data &amp; Process Science Research Center. Write to us with your dates and interests.</p></div>
    </div>
  </div>
</section>
"""
    return page(
        "join.html",
        "Join Us — AIM Lab, POSTECH",
        "Ph.D., M.S. and undergraduate research positions at the Analytics & Information Management Lab, POSTECH. "
        "How to apply and what to expect.",
        body,
    )


def build_contact():
    body = page_head(
        "Contact",
        "Contact and directions",
        "The lab is on the POSTECH campus in Pohang, on Korea's south-east coast."
    ) + """
<section class="section">
  <div class="wrap">
    <div class="grid grid-2" style="gap:48px;align-items:start">
      <div>
        <h2>Lab office</h2>
        <ul class="meta-list" style="font-size:.95rem">
          <li><span class="k">Address</span><span>Engineering Building 4, Room 408<br>POSTECH, 77 Cheongam-ro, Nam-gu<br>Pohang, Gyeongbuk 37673, Republic of Korea</span></li>
          <li><span class="k">Telephone</span><span><a href="tel:+82542798260">+82-54-279-8260</a></span></li>
          <li><span class="k">E-mail</span><span><a href="mailto:mssong@postech.ac.kr">mssong@postech.ac.kr</a></span></li>
        </ul>

        <h2 style="margin-top:44px">Prof. Song's office</h2>
        <ul class="meta-list" style="font-size:.95rem">
          <li><span class="k">Address</span><span>Engineering Building 4, Room 223</span></li>
          <li><span class="k">Telephone</span><span><a href="tel:+82542792376">+82-54-279-2376</a></span></li>
        </ul>

        <div class="btn-row">
          <a class="btn btn-primary" href="mailto:mssong@postech.ac.kr">Send an email</a>
          <a class="btn btn-ghost" href="https://maps.google.com/?q=POSTECH+Engineering+Building+4,+77+Cheongam-ro,+Nam-gu,+Pohang" rel="noopener">Open in Maps</a>
        </div>
      </div>

      <div>
        <div class="callout" style="margin-top:0">
          <h3>Getting to POSTECH</h3>
          <p><strong>By air.</strong> Pohang&ndash;Gyeongju Airport is about 20 minutes from campus by taxi. Gimpo and Incheon
          both connect through Seoul.</p>
          <p><strong>By train.</strong> KTX from Seoul Station to Pohang Station takes roughly 2 hours 20 minutes; campus is
          about 20 minutes from the station by taxi or bus.</p>
          <p><strong>On campus.</strong> Engineering Building 4 sits in the engineering cluster; the department office can
          direct visitors.</p>
        </div>

        <div class="card">
          <span class="kicker">Elsewhere</span>
          <h3>Related links</h3>
          <ul style="list-style:none;padding:0;margin:0">
            <li style="padding:6px 0"><a href="https://www.postech.ac.kr/eng/" rel="noopener">POSTECH</a></li>
            <li style="padding:6px 0"><a href="https://ime.postech.ac.kr/" rel="noopener">Dept. of Industrial &amp; Management Engineering</a></li>
            <li style="padding:6px 0"><a href="https://aim.postech.ac.kr/" rel="noopener">Departmental lab pages (archive)</a></li>
            <li style="padding:6px 0"><a href="https://dblp.org/pid/71/4935.html" rel="noopener">DBLP</a></li>
            <li style="padding:6px 0"><a href="https://www.puzzledata.com/" rel="noopener">Puzzle Data (spin-off)</a></li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</section>
"""
    return page(
        "contact.html",
        "Contact — AIM Lab, POSTECH",
        "Address, telephone, email and directions for the Analytics & Information Management Lab at POSTECH, Pohang.",
        body,
    )


# --------------------------------------------------------------------------
def main():
    journals, conferences = load_publications()
    news = load_news()

    notfound = page(
        "404.html",
        "Page not found — AIM Lab, POSTECH",
        "The page you were looking for does not exist.",
        """<section class="section" style="padding:120px 0">
  <div class="wrap center">
    <span class="eyebrow" style="color:var(--red);font-weight:700;letter-spacing:.12em;text-transform:uppercase;font-size:.76rem">Error 404</span>
    <h1>This page does not exist.</h1>
    <p class="muted">The address may have changed, or the link that brought you here may be out of date.</p>
    <div class="btn-row" style="justify-content:center">
      <a class="btn btn-primary" href="/">Back to the home page</a>
      <a class="btn btn-ghost" href="/publications/">Publications</a>
    </div>
  </div>
</section>
""",
    )

    pages = {
        "index.html": build_index(journals, conferences, news),
        "research.html": build_research(),
        "members/index.html": build_members_index(),
        "members/professor/index.html": build_members_professor(),
        "members/emeritus/index.html": build_members_emeritus(),
        "members/students/index.html": build_members_students(),
        "members/alumni/index.html": build_members_alumni(),
        "publications/index.html": build_publications_index(journals, conferences),
        "publications/journal/index.html": build_publications_list(
            "publications/journal/index.html", journals, "journals", "articles"),
        "publications/conference/index.html": build_publications_list(
            "publications/conference/index.html", conferences, "conferences", "papers"),
        "projects.html": build_projects(),
        "news.html": build_news(news),
        "join.html": build_join(),
        "contact.html": build_contact(),
    }
    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8") as fh:
        fh.write(notfound)
    print("wrote 404.html")
    # Redirects from the previous /people/... layout
    redirects = {
        "people.html": "/members/",
        "people/professor.html": "/members/professor/",
        "people/emeritus.html": "/members/emeritus/",
        "people/students.html": "/members/students/",
        "people/alumni.html": "/members/alumni/",
        "publications.html": "/publications/",
    }
    os.makedirs(os.path.join(ROOT, "people"), exist_ok=True)
    for src, dest in redirects.items():
        with open(os.path.join(ROOT, src), "w", encoding="utf-8") as fh:
            fh.write(
                '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
                f'<meta http-equiv="refresh" content="0; url={dest}">\n'
                f'<link rel="canonical" href="{SITE_URL}{dest}">\n'
                "<title>Members — AIM Lab, POSTECH</title>\n</head>\n"
                f'<body><p>This page has moved to <a href="{dest}">{dest}</a>.</p></body>\n'
                "</html>\n"
            )
    print(f"wrote {len(redirects)} redirect stubs")

    for name, content in pages.items():
        os.makedirs(os.path.dirname(os.path.join(ROOT, name)) or ROOT, exist_ok=True)
        with open(os.path.join(ROOT, name), "w", encoding="utf-8") as fh:
            fh.write(content)
        print("wrote", name, len(content), "bytes")

    # news detail pages
    news_dir = os.path.join(ROOT, "news")
    os.makedirs(news_dir, exist_ok=True)
    for existing in os.listdir(news_dir):
        if existing.endswith(".html"):
            os.remove(os.path.join(news_dir, existing))
    LINKS = {
        "n2026-00": "/publications/journal/",
        "n2026-03-30": "/publications/journal/",
        "n2026-03-02": "/members/students/",
        "n2026-02-01": "/members/alumni/",
        "n2026-09-01": "/members/students/",
    }
    for post in news:
        post["more"] = LINKS.get(post["no"], "")
    for i, post in enumerate(news):
        prev_p = news[i + 1] if i + 1 < len(news) else None
        next_p = news[i - 1] if i > 0 else None
        with open(os.path.join(news_dir, post["slug"]), "w", encoding="utf-8") as fh:
            fh.write(build_news_detail(post, prev_p, next_p))
    print(f"wrote {len(news)} pages in news/")

    # sitemap
    urls = "\n".join(
        [f"  <url><loc>{SITE_URL}{nav_url(n)}</loc></url>" for n in pages]
        + [f"  <url><loc>{SITE_URL}/news/{p['slug']}</loc></url>" for p in news]
    )
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{urls}\n</urlset>\n"
        )
    print("wrote sitemap.xml")


if __name__ == "__main__":
    main()
