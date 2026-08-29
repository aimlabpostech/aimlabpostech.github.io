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

PEOPLE_PAGES = [
    ("people/professor.html", "Professor"),
    ("people/emeritus.html", "Emeritus Professors"),
    ("people/students.html", "Students"),
    ("people/alumni.html", "Alumni"),
]

NAV = [
    ("index.html", "Home", []),
    ("research.html", "Research", []),
    ("people/professor.html", "People", PEOPLE_PAGES),
    ("publications.html", "Publications", []),
    ("projects.html", "Projects", []),
    ("news.html", "News", []),
    ("join.html", "Join Us", []),
    ("contact.html", "Contact", []),
]


def nav_url(href):
    return "/" if href == "index.html" else "/" + href


def section_of(slug):
    """Which top-level nav entry a page belongs to."""
    if slug.startswith("people/"):
        return "people/professor.html"
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
<link rel="canonical" href="{SITE_URL}/{'' if slug == 'index.html' else slug}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:url" content="{SITE_URL}/{'' if slug == 'index.html' else slug}">
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
        <span class="brand-name"><span class="brand-full">Analytics &amp; Information Management Lab</span><span class="brand-short">AIM Lab</span></span>
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
          <li><a href="/people/professor.html">People</a></li>
          <li><a href="/publications.html">Publications</a></li>
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
          <li><a href="https://scholar.google.com/citations?user=8ACzAlkAAAAJ" rel="noopener">Google Scholar</a></li>
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
    return f"""<section class="page-head">
  <div class="wrap">
    <span class="eyebrow">{eyebrow}</span>
    <h1>{title}</h1>
    <p>{sub}</p>
  </div>
</section>
"""


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


def load(fname):
    path = os.path.join(DATA, fname)
    items = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            p = parse_citation(line)
            if p:
                items.append(p)
    items.sort(key=lambda x: -x["year"])
    return items


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
            f'<span class="a">{html.escape(it["authors"])}{venue}</span></li>'
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
    ("Hyunjun Jung", "M.S. student, Industrial & Management Engineering", "jhj1769@postech.ac.kr", 2024),
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
    posts.sort(key=lambda p: (p["date"], int(p["no"])), reverse=True)
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
PROJECTS = [
    ("Manufacturing Foundation Model", "Large Language Models",
     "2025.09 &ndash; 2029.12", "Ministry of Trade, Industry and Energy",
     "A national programme with Seoul National University and KAIST to build foundation models for manufacturing."),
    ("Hospital operation technology based on process mining and digital twins",
     "Process Mining &middot; Healthcare", "2023.04 &ndash; 2027.12",
     "Korea Health Industry Development Institute",
     "Development and field validation of a digital-twin hospital operating system that optimises in- and out-patient management."),
    ("Object-centric process mining: modelling, simulation and optimisation",
     "Process Mining", "2025.01 &ndash; 2025.12", "National Research Foundation of Korea",
     "Foundational research on object-centric event data, from discovery to simulation and optimisation."),
    ("Wil van der Aalst Data &amp; Process Science Research Center (Glocal R&amp;D Centre)",
     "Research Centre", "2025.01 &ndash; 2025.12", "Glocal University 30",
     "Operation of the lab's international research centre for data and process science."),
    ("Process-mining-converged AI for smart factory operation",
     "Process Mining &middot; Manufacturing", "2025.01 &ndash; 2025.12",
     "Korea Technology and Information Promotion Agency for SMEs",
     "Development and demonstration of AI-based smart factory operating technology for digital transformation in manufacturing."),
    ("AI-based OTT user and content analytics and video recommendation",
     "Recommender Systems", "2025.01 &ndash; 2025.12",
     "Institute for Information &amp; Communications Technology Planning &amp; Evaluation",
     "Analysis of viewing behaviour and content metadata to drive a video recommendation engine."),
    ("Samsung C&amp;T Fashion recommendation system",
     "Recommender Systems", "2024.01 &ndash; 2025.12", "Samsung C&amp;T (Fashion)",
     "Personalised product and curation models that lift conversion rate and shopping satisfaction."),
    ("Plate post-processing load simulator", "Simulation", "2024.02 &ndash; 2024.11", "POSCO",
     "A simulator for downstream load in heavy-plate production."),
    ("TSV process inefficiency and optimal path discovery from manufacturing data",
     "Process Mining &middot; Semiconductor", "2024.03 &ndash; 2024.10", "SK hynix",
     "Event-data analysis of through-silicon-via processes to locate inefficiencies and optimal routings."),
]

CENTERS = [
    ("Wil van der Aalst Data &amp; Process Science Research Center",
     "Opened in 2024 and named after the founder of process mining, the centre anchors POSTECH's international "
     "research agenda in data and process science, hosting joint projects, visiting researchers and the "
     "Asia-Pacific Process Mining workshop series."),
    ("Future City Open Innovation Big Data Center",
     "A POSTECH centre applying big-data and process analytics to urban problems &mdash; mobility, shrinking cities, "
     "energy use and public services &mdash; in partnership with local government."),
    ("Puzzle Data (spin-off)",
     "Korea's first process-mining solution company, founded as a spin-off of the lab. It commercialises the "
     "lab's research through the ProDiscovery process-mining platform."),
]

PARTNERS = [
    "Samsung Electronics", "Samsung SDI", "Samsung C&amp;T", "POSCO", "SK hynix",
    "Hyundai Heavy Industries", "LG Electronics", "Seoul National University Bundang Hospital",
    "National Research Foundation of Korea", "Korea Health Industry Development Institute",
    "IITP", "Ministry of Trade, Industry and Energy", "Puzzle Data",
]


# --------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------
def build_index(journals, conferences, news):
    news_items = "\n".join(news_row(p) for p in news[:5])

    areas = [
        ("Process Mining",
         "Discovery, conformance checking and enhancement on event logs &mdash; including object-centric process mining, "
         "event abstraction and privacy-aware discovery."),
        ("Business Process Management",
         "Evidence-based redesign, service-level agreements, resource and organisational models, and process performance "
         "indicators grounded in real event data."),
        ("Predictive Process Monitoring",
         "Deep learning on process data to predict remaining time, outcomes and workloads, and to allocate resources before "
         "bottlenecks form."),
        ("Simulation &amp; Digital Twins",
         "Automatically generating simulation models from event data, and running digital twins of hospitals, factories and "
         "city traffic."),
        ("Industrial AI &amp; LLMs",
         "Large language model agents for event-log extraction, process improvement scenarios and manufacturing foundation "
         "models."),
        ("Recommender Systems &amp; Analytics",
         "Personalised recommendation for fashion and media, customer-journey analysis, and applied business analytics."),
    ]
    area_cards = "\n".join(
        f"""      <div class="card"><span class="kicker">Area</span><h3>{t}</h3><p>{d}</p></div>"""
        for t, d in areas
    )

    partner_pills = "\n".join(f"      <span>{p}</span>" for p in PARTNERS)

    body = f"""<section class="hero">
  <div class="wrap">
    <span class="eyebrow">POSTECH &middot; Industrial &amp; Management Engineering</span>
    <h1>Turning event data into process intelligence.</h1>
    <p class="lead">The Analytics &amp; Information Management (AIM) Lab studies how organisations really work.
    We read the traces that information systems leave behind &mdash; in factories, hospitals, ports and cities &mdash;
    and turn them into models, predictions and decisions that make those processes measurably better.</p>
    <div class="btn-row">
      <a class="btn btn-primary" href="/research.html">Explore our research</a>
      <a class="btn btn-ghost" href="/join.html">Join the lab</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="stats">
      <div class="stat"><b>150+</b><span>Scientific publications</span></div>
      <div class="stat"><b>70+</b><span>Funded research projects</span></div>
      <div class="stat"><b>16</b><span>Current graduate students</span></div>
      <div class="stat"><b>40+</b><span>Ph.D. and M.S. alumni</span></div>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="grid grid-2" style="gap:56px;align-items:start">
      <div>
        <h2>About the lab</h2>
        <p>POSTECH AIM Lab conducts research to analyse and innovate the processes that run modern organisations.
        Process mining and data mining are our primary lenses; on top of them we build methods that draw on machine
        learning, artificial intelligence, simulation and optimisation.</p>
        <p>Our work has been funded by the Korean government and by leading global companies based in Korea, including
        Samsung Electronics, Hyundai Heavy Industries and POSCO. We have published more than 150 scientific papers in
        venues such as <em>Decision Support Systems</em>, <em>Information Systems</em>, the
        <em>Journal of Information Technology</em>, the <em>International Journal of Medical Informatics</em>, BPM and ICPM.</p>
        <p>We also care about getting research into use. <a href="https://www.puzzledata.com/" rel="noopener">Puzzle Data</a>,
        the first process-mining solution company in Korea, was established as a spin-off of the lab.</p>
        <div class="btn-row">
          <a class="btn btn-ghost" href="/people/students.html">Meet the team</a>
        </div>
      </div>
      <div>
        <div class="callout" style="margin-top:0">
          <h3>Where our methods are applied</h3>
          <ul style="margin:0;padding-left:1.1em">
            <li><strong>Manufacturing</strong> &mdash; semiconductor yield, steelmaking, shipbuilding, smart factories</li>
            <li><strong>Healthcare</strong> &mdash; clinical pathways, outpatient flow, emergency-room performance</li>
            <li><strong>Logistics &amp; ports</strong> &mdash; container handling, supply chains, baggage systems</li>
            <li><strong>Cities &amp; mobility</strong> &mdash; traffic simulation, hydrogen refuelling networks, shrinking cities</li>
            <li><strong>Commerce &amp; media</strong> &mdash; customer journeys, fashion and OTT recommendation</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="wrap">
    <div class="section-head">
      <h2>Research areas</h2>
      <p>Six threads run through our work. They overlap far more than they compete &mdash; most projects in the lab pull on
      several at once.</p>
    </div>
    <div class="grid grid-3">
{area_cards}
    </div>
  </div>
</section>

<section class="section">
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

<section class="section section-soft">
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

<section class="section">
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
        "The Analytics & Information Management Lab at POSTECH studies process mining, business process management, "
        "predictive process monitoring, simulation and industrial AI.",
        body,
    )


def build_research():
    detail = [
        ("Process mining",
         "Process mining extracts meaningful information and knowledge from the event logs recorded by the information "
         "systems that organisations already run &mdash; BPM, ERP, CRM and SCM. Discovering process models, measuring process "
         "performance, deriving organisational models and building simulation models from logs are the core problems we work on.",
         ["Object-centric process mining and object-centric directly-follows graphs",
          "Event abstraction: raising low-level events to the level people reason at",
          "Privacy-aware process discovery and the effect of event-data partitioning",
          "Process layout generation using integer programming so that models are readable",
          "Trace clustering and dimensionality reduction for heterogeneous logs"]),
        ("Business process management",
         "Once a process is visible it can be redesigned. We study evidence-based redesign: which best practices actually pay "
         "off, how to define realistic service-level agreements, and how to measure process performance in a way that survives "
         "contact with operational reality.",
         ["Evidence-based evaluation of business process redesign best practices",
          "Process performance indicators, including for emergency-room processes",
          "Organisational mining and social network discovery from event logs",
          "Optimal resource assignment in workflows"]),
        ("Predictive process monitoring and optimisation",
         "Prediction is only useful if it changes a decision. We build deep-learning models that predict how a running case "
         "will unfold, then couple them to allocation and scheduling algorithms that act on the prediction.",
         ["Predicting process performance with deep neural networks",
          "LSTM-based prediction combined with minimum-cost maximum-flow resource allocation",
          "Resource allocation driven by predictive process monitoring"]),
        ("Simulation and digital twins",
         "Simulation models are expensive to build by hand and go stale quickly. We generate them automatically from event "
         "data and open data, so that a digital twin of a hospital, a plant or a city network stays close to the system it mirrors.",
         ["MedProSim: finding the causes of outpatient waiting times",
          "Automatic generation of open-data-based traffic simulation models",
          "Process simulation models for steelmaking and plate post-processing",
          "Digital-twin-based hospital operation for in- and out-patient management"]),
        ("Industrial AI and large language models",
         "Large language models change what is cheap: reading unfamiliar schemas, writing extraction logic, proposing "
         "improvement scenarios. We study where that helps a process analyst and where it quietly misleads one.",
         ["Multi-agent frameworks for automated event-log extraction",
          "Generating process improvement scenarios with LLM agents and XAI feature importance",
          "Manufacturing foundation models",
          "Multi-hop question answering over visually rich medical documents"]),
        ("Recommender systems and business analytics",
         "The lab has a long line of applied analytics work with industry, from fashion e-commerce to video streaming to "
         "sports, where the question is usually the same: what should this particular person or asset do next?",
         ["Personalised product and outfit recommendation for fashion retail",
          "OTT user and content analytics for video recommendation",
          "Customer-journey analysis combining process mining and machine learning",
          "Sports analytics: passing-style analysis and similar-situation retrieval"]),
    ]
    blocks = []
    for title, intro, bullets in detail:
        lis = "\n".join(f"        <li>{b}</li>" for b in bullets)
        blocks.append(f"""    <section style="margin-bottom:56px">
      <h2>{title}</h2>
      <p>{intro}</p>
      <ul>
{lis}
      </ul>
    </section>""")
    blocks = "\n".join(blocks)

    domains = [
        ("Manufacturing", "Semiconductor yield analysis and visualisation, steelmaking simulation, shipbuilding schedules, "
                          "configurable manufacturing execution systems, smart factory operation."),
        ("Healthcare", "Clinical pathway development from order logs, outpatient and emergency process analysis, OMOP "
                       "common data model for process mining, hospital digital twins."),
        ("Logistics &amp; ports", "Container-handling analytics, lateness analysis in port logistics, supply-chain process "
                                  "analysis, airport baggage handling systems."),
        ("Cities &amp; energy", "Traffic simulation from open data, hydrogen refuelling station siting and supply chains, "
                                "campus electricity consumption, shrinking-city transition models."),
    ]
    domain_cards = "\n".join(
        f'      <div class="card"><h3>{t}</h3><p>{d}</p></div>' for t, d in domains
    )

    body = page_head(
        "Research",
        "What we work on",
        "Process mining is the lab's foundation. Around it we build machine learning, simulation and optimisation "
        "methods, and we test all of them on processes that people actually depend on."
    ) + f"""
<section class="section">
  <div class="wrap prose">
{blocks}
  </div>
</section>

<section class="section section-soft">
  <div class="wrap">
    <div class="section-head">
      <h2>Application domains</h2>
      <p>Methods earn their keep in the field. These are the settings our projects keep returning to.</p>
    </div>
    <div class="grid grid-2">
{domain_cards}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="cta">
      <div>
        <h2>Read the work itself</h2>
        <p>Every claim above traces back to a paper. The publication list covers journal articles and international
        conference papers from 2001 to today.</p>
      </div>
      <a class="btn btn-primary" href="/publications.html">Publications</a>
    </div>
  </div>
</section>
"""
    return page(
        "research.html",
        "Research — AIM Lab, POSTECH",
        "Process mining, business process management, predictive process monitoring, simulation and digital twins, "
        "industrial AI and recommender systems at POSTECH's AIM Lab.",
        body,
    )


PEOPLE_INTRO = {
    "people/professor.html": (
        "Professor",
        "The principal investigator of the Analytics &amp; Information Management Lab.",
    ),
    "people/emeritus.html": (
        "Emeritus Professors",
        "Faculty who shaped the lab and remain part of its wider circle.",
    ),
    "people/students.html": (
        "Students",
        "Ph.D. and M.S. researchers currently in the lab, across industrial &amp; management "
        "engineering, industrial data science, social data science and defence science and technology.",
    ),
    "people/alumni.html": (
        "Alumni",
        "Post-doctoral researchers and graduates of the lab, and where they went next.",
    ),
}


def people_tabs(current):
    items = []
    for h, l in PEOPLE_PAGES:
        cur = ' class="current" aria-current="page"' if h == current else ""
        items.append(f'      <a href="{nav_url(h)}"{cur}>{l}</a>')
    links = "\n".join(items)
    return f"""<nav class="subtabs" aria-label="People sections">
  <div class="wrap">
    <div class="subtabs-inner">
{links}
    </div>
  </div>
</nav>
"""


def people_page(slug, body_sections):
    heading, sub = PEOPLE_INTRO[slug]
    body = page_head("People", heading, sub) + people_tabs(slug) + body_sections
    return page(
        slug,
        f"{heading} — AIM Lab, POSTECH",
        re.sub(r"&[a-z]+;", "&", sub),
        body,
    )


def build_people_professor():
    return people_page("people/professor.html", """
<section class="section">
  <div class="wrap">
    <div class="pi-card">
      <img class="pi-photo" src="/assets/img/people/minseok-song.jpg" alt="Minseok Song" width="512" height="512">
      <div>
        <h3>Minseok Song (송민석), Ph.D.</h3>
        <p class="pi-role">Professor &middot; Principal Investigator</p>
        <p>Minseok Song is a Professor in the Department of Industrial &amp; Management Engineering at POSTECH, where he
        also serves as Vice President of Planning. He directs the Wil van der Aalst Data &amp; Process Science Research
        Center and the Future City Open Innovation Big Data Center, and is an associated partner member of ERCIS
        (European Research Center of Information Systems).</p>
        <p>An industrial engineer by training with a background in information systems and computer science, his research
        interests span process mining, recommendation systems, business analytics and industrial AI. He held a
        postdoctoral position at Eindhoven University of Technology, where he worked with Wil van der Aalst on the
        foundations of process mining.</p>
        <ul class="meta-list">
          <li><span class="k">Position</span><span>Professor, Dept. of Industrial &amp; Management Engineering</span></li>
          <li><span class="k">Office</span><span>Engineering Building 4, Room 223</span></li>
          <li><span class="k">Telephone</span><span><a href="tel:+82542792376">+82-54-279-2376</a></span></li>
          <li><span class="k">E-mail</span><span><a href="mailto:mssong@postech.ac.kr">mssong@postech.ac.kr</a></span></li>
          <li><span class="k">Profiles</span><span><a href="https://scholar.google.com/citations?user=8ACzAlkAAAAJ" rel="noopener">Google Scholar</a> &middot; <a href="https://dblp.org/pid/71/4935.html" rel="noopener">DBLP</a></span></li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section section-soft" style="padding-top:56px">
  <div class="wrap">
    <div class="section-head"><h2>Roles</h2></div>
    <div class="grid grid-3">
      <div class="card"><span class="kicker">POSTECH</span><h3>Vice President of Planning</h3>
      <p>University-level planning and strategy.</p></div>
      <div class="card"><span class="kicker">Centre</span><h3>Wil van der Aalst Data &amp; Process Science Research Center</h3>
      <p>Director of the lab's international research centre, opened in 2024.</p></div>
      <div class="card"><span class="kicker">Centre</span><h3>Future City Open Innovation Big Data Center</h3>
      <p>Director; urban analytics with local government and industry partners.</p></div>
    </div>
  </div>
</section>
""")


def build_people_emeritus():
    return people_page("people/emeritus.html", """
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
          <li><span class="k">E-mail</span><span><a href="mailto:ehsuh@postech.ac.kr">ehsuh@postech.ac.kr</a></span></li>
        </ul>
      </div>
    </div>
  </div>
</section>
""")


def build_people_students():
    cards = "\n".join(
        f'''      <div class="person">
        <img class="photo" src="/assets/img/people/{photo_slug(n)}.jpg" alt="{n}" width="360" height="360" loading="lazy">
        <div class="person-body">
          <h4>{n}</h4>
          <p class="role">{r}<br>{y}&ndash;present</p>
          <a class="mail" href="mailto:{m}">{m}</a>
        </div>
      </div>'''
        for n, r, m, y in STUDENTS
    )
    phd = sum(1 for _, r, _, _ in STUDENTS if r.startswith("Ph.D."))
    ms = len(STUDENTS) - phd
    return people_page("people/students.html", f"""
<section class="section">
  <div class="wrap">
    <p class="count-note" style="margin-bottom:28px">{len(STUDENTS)} graduate students &mdash; {phd} Ph.D., {ms} M.S.</p>
    <div class="grid grid-4">
{cards}
    </div>
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


def build_people_alumni():
    postdocs = "\n".join(
        f"        <tr><td>{n}</td><td>{p}</td><td>{d}</td></tr>" for n, p, d in POSTDOC_ALUMNI
    )
    phds = "\n".join(
        f"        <tr><td>{y}</td><td>{n}</td><td>{d}</td></tr>" for y, n, d in PHD_ALUMNI
    )
    ms = "\n".join(
        f"        <tr><td>{y}</td><td>{n}</td><td>{d}</td></tr>" for y, n, d in MS_ALUMNI
    )
    return people_page("people/alumni.html", f"""
<section class="section">
  <div class="wrap">
    <p class="count-note" style="margin-bottom:28px">{len(POSTDOC_ALUMNI)} post-doctoral researchers,
    {len(PHD_ALUMNI)} doctoral and {len(MS_ALUMNI)} master's graduates.</p>

    <h2>Post-doctoral researchers</h2>
    <div class="table-scroll">
      <table>
        <thead><tr><th>Name</th><th>Period</th><th>Now at</th></tr></thead>
        <tbody>
{postdocs}
        </tbody>
      </table>
    </div>

    <h2 style="margin-top:56px">Doctoral</h2>
    <div class="table-scroll">
      <table>
        <thead><tr><th>Year</th><th>Name</th><th>Now at</th></tr></thead>
        <tbody>
{phds}
        </tbody>
      </table>
    </div>

    <h2 style="margin-top:56px">Master's</h2>
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


def build_publications(journals, conferences):
    body = page_head(
        "Publications",
        "Publications",
        "Journal articles and international conference papers from the lab. Filter by period, or search the full record "
        "on Google Scholar and DBLP."
    ) + f"""
<section class="section">
  <div class="wrap">
    <div class="btn-row" style="margin:0 0 36px">
      <a class="btn btn-ghost" href="#journals-section">Journal articles ({len(journals)})</a>
      <a class="btn btn-ghost" href="#conferences-section">Conference papers ({len(conferences)})</a>
      <a class="btn btn-ghost" href="https://scholar.google.com/citations?user=8ACzAlkAAAAJ" rel="noopener">Google Scholar</a>
    </div>

    <div id="journals-section">
      <h2>Journal articles</h2>
      <p class="count-note">Showing <span id="journals-count">{len(journals)}</span> of {len(journals)} articles.</p>
      {FILTER_BAR.format(lid="journals")}
      {render_pubs(journals, "journals")}
    </div>

    <div id="conferences-section" style="margin-top:72px">
      <h2>International conference papers</h2>
      <p class="count-note">Showing <span id="conferences-count">{len(conferences)}</span> of {len(conferences)} papers.
      Domestic conference papers are listed on the <a href="https://aim.postech.ac.kr/" rel="noopener">departmental lab
      pages</a>.</p>
      {FILTER_BAR.format(lid="conferences")}
      {render_pubs(conferences, "conferences")}
    </div>
  </div>
</section>
"""
    return page(
        "publications.html",
        "Publications — AIM Lab, POSTECH",
        "Journal articles and international conference papers on process mining, business process management, "
        "healthcare analytics and industrial AI from POSTECH's AIM Lab.",
        body,
    )


def build_projects():
    rows = "\n".join(
        f"""      <div class="card">
        <span class="kicker">{tag}</span>
        <h3>{title}</h3>
        <p>{desc}</p>
        <ul class="meta-list" style="margin-top:14px">
          <li><span class="k">Period</span><span>{period}</span></li>
          <li><span class="k">Funder</span><span>{funder}</span></li>
        </ul>
      </div>"""
        for title, tag, period, funder, desc in PROJECTS
    )
    centres = "\n".join(
        f'      <div class="card"><h3>{t}</h3><p>{d}</p></div>' for t, d in CENTERS
    )
    partner_pills = "\n".join(f"      <span>{p}</span>" for p in PARTNERS)

    body = page_head(
        "Projects &amp; Centers",
        "Projects and centers",
        "More than seventy funded projects since the lab was founded, run with national agencies, hospitals and industry. "
        "A selection of current and recent work is below."
    ) + f"""
<section class="section">
  <div class="wrap">
    <div class="section-head">
      <h2>Selected projects</h2>
      <p>Current and recently completed research programmes.</p>
    </div>
    <div class="grid grid-2">
{rows}
    </div>
    <p class="small muted" style="margin-top:28px">The full project record, including work dating back to 2001, is
    maintained on the <a href="https://aim.postech.ac.kr/aim2/prj/projects.do" rel="noopener">departmental lab site</a>.</p>
  </div>
</section>

<section class="section section-soft">
  <div class="wrap">
    <div class="section-head">
      <h2>Centers and spin-off</h2>
      <p>The lab anchors two research centres at POSTECH and one company.</p>
    </div>
    <div class="grid grid-3">
{centres}
    </div>
  </div>
</section>

<section class="section">
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
    return page(
        "projects.html",
        "Projects & Centers — AIM Lab, POSTECH",
        "Funded research projects and the research centres anchored by POSTECH's Analytics & Information Management Lab.",
        body,
    )


def news_row(p):
    thumb = (
        f'<img class="news-thumb" src="{p["thumb"]}" alt="" width="176" height="176" loading="lazy">'
        if p["thumb"] else ""
    )
    excerpt = html.escape(p["excerpt"][:160] + ("…" if len(p["excerpt"]) > 160 else ""))
    return f"""      <li class="news-item" data-tags="y{p['year']}">
        <time datetime="{p['iso']}">{p['date']}</time>
        <div class="news-main">
          <h3><span class="tag">{p['cat']}</span><a href="{p['url']}">{html.escape(p['title_en'])}</a></h3>
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

    ko_paras = "\n".join(
        f"        <p>{html.escape(t)}</p>" for t in (p.get("paras") or [])
    ) or "        <p>—</p>"

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

    body = f"""<section class="page-head">
  <div class="wrap">
    <a class="back-link" href="/news.html">&larr; All news</a>
    <span class="eyebrow">{p['cat']} &middot; {p['date']}</span>
    <h1>{html.escape(p['title_en'])}</h1>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <article class="news-article">
{paras}
{gallery}
      <details class="news-original">
        <summary>Korean original &middot; 원문 보기</summary>
        <h3>{html.escape(p['title'])}</h3>
{ko_paras}
        <p class="small muted">Originally published on the
        <a href="https://aim.postech.ac.kr/aim2/bbs/notice.do?mode=view&amp;articleNo={p['no']}" rel="noopener">AIM Lab board</a>
        on {p['date']}.</p>
      </details>
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
        <h3>Undergraduate researchers</h3>
        <p>POSTECH undergraduates can join through the URP or as research interns during the semester or vacation. This is
        the usual route into the lab for our own students.</p>

        <h2>How to apply</h2>
        <p>Admission is through POSTECH's graduate admissions process, but contact the lab first &mdash; we can tell you
        whether there is a fit before you invest in an application. Write to
        <a href="mailto:mssong@postech.ac.kr">mssong@postech.ac.kr</a> with the subject line
        <em>&ldquo;Prospective student &mdash; [your name]&rdquo;</em> and include:</p>
        <ul>
          <li>A CV, including your transcript and any publications or projects</li>
          <li>A short paragraph on which of our research areas interests you and why</li>
          <li>Your intended start semester and degree programme</li>
        </ul>
        <p>Applications from international students are welcome. POSTECH offers graduate programmes taught in English and
        supports visa and housing arrangements for admitted students.</p>
      </div>

      <div>
        <div class="callout" style="margin-top:0">
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

        <div class="card">
          <span class="kicker">Enquiry template</span>
          <h3>Email us</h3>
          <div class="code-block">To: mssong@postech.ac.kr
Subject: Prospective student — [your name]

Dear Professor Song,

I am a [degree, major] student at [university],
graduating in [month year]. I am interested in
joining AIM Lab as a [Ph.D. / M.S.] student
starting [semester].

I am particularly interested in [research area],
after [course / project / paper that prompted it].

My CV and transcript are attached.

Best regards,
[name]</div>
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
            <li style="padding:6px 0"><a href="https://scholar.google.com/citations?user=8ACzAlkAAAAJ" rel="noopener">Google Scholar</a></li>
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
    journals = load("journals.txt")
    conferences = load("conferences.txt")
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
      <a class="btn btn-ghost" href="/publications.html">Publications</a>
    </div>
  </div>
</section>
""",
    )

    pages = {
        "index.html": build_index(journals, conferences, news),
        "research.html": build_research(),
        "people/professor.html": build_people_professor(),
        "people/emeritus.html": build_people_emeritus(),
        "people/students.html": build_people_students(),
        "people/alumni.html": build_people_alumni(),
        "publications.html": build_publications(journals, conferences),
        "projects.html": build_projects(),
        "news.html": build_news(news),
        "join.html": build_join(),
        "contact.html": build_contact(),
    }
    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8") as fh:
        fh.write(notfound)
    print("wrote 404.html")
    os.makedirs(os.path.join(ROOT, "people"), exist_ok=True)
    with open(os.path.join(ROOT, "people.html"), "w", encoding="utf-8") as fh:
        fh.write(
            '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta http-equiv="refresh" content="0; url=/people/professor.html">\n'
            '<link rel="canonical" href="' + SITE_URL + '/people/professor.html">\n'
            "<title>People — AIM Lab, POSTECH</title>\n</head>\n"
            '<body><p>Redirecting to <a href="/people/professor.html">People</a>.</p></body>\n'
            "</html>\n"
        )
    print("wrote people.html (redirect)")
    for name, content in pages.items():
        with open(os.path.join(ROOT, name), "w", encoding="utf-8") as fh:
            fh.write(content)
        print("wrote", name, len(content), "bytes")

    # news detail pages
    news_dir = os.path.join(ROOT, "news")
    os.makedirs(news_dir, exist_ok=True)
    for existing in os.listdir(news_dir):
        if existing.endswith(".html"):
            os.remove(os.path.join(news_dir, existing))
    for i, post in enumerate(news):
        prev_p = news[i + 1] if i + 1 < len(news) else None
        next_p = news[i - 1] if i > 0 else None
        with open(os.path.join(news_dir, post["slug"]), "w", encoding="utf-8") as fh:
            fh.write(build_news_detail(post, prev_p, next_p))
    print(f"wrote {len(news)} pages in news/")

    # sitemap
    urls = "\n".join(
        [f"  <url><loc>{SITE_URL}/{'' if n == 'index.html' else n}</loc></url>" for n in pages]
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
