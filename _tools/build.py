#!/usr/bin/env python3
"""Static builder for japanesegrimoire.com (hubs, blog, articles, sitemap, llms.txt).

Source:   _content/articles/*.html  (META json block + body html)
          _content/hubs.json
Output:   public/blog/<slug>.html, public/blog/index.html, public/<hub>.html,
          public/sitemap.xml, public/llms.txt
Run:      python3 _tools/build.py
The existing landing pages (index, shingon-reiki-level-1, contact, legal, thank-you,
confirmed) are NOT generated here and stay hand-maintained.
"""
import json, re, html, os, glob, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, 'public')
SITE = 'https://japanesegrimoire.com'
SKOOL = 'https://www.skool.com/japanese-grimoire-society'
SR1 = 'https://markhosak.my-ablefy.com/s/markhosak/shingon-reiki-level-1?locale=en'

HUBS = json.load(open(os.path.join(ROOT, '_content', 'hubs.json'), encoding='utf-8'))
HUB_BY = {h['slug']: h for h in HUBS}

MARK = {
    "@type": "Person", "@id": SITE + "/#mark", "name": "Dr. Mark Hosak",
    "jobTitle": "Japanologist, Shingon practitioner and researcher",
    "alumniOf": "Heidelberg University", "url": SITE + "/",
    "sameAs": ["https://www.shingon-reiki.com/en/about-mark-and-eileen",
               "https://www.shamanic-worlds.com", "https://www.tengu-akasha-dojo.de/en",
               "https://www.homecomingjapan.com", "https://www.instagram.com/japanesegrimoire",
               "https://www.youtube.com/channel/UCn7IHhHHqZ7LP4aqaCtLM5w"]}
ORG = {"@type": "Organization", "@id": SITE + "/#org", "name": "Japanese Grimoire",
       "url": SITE + "/", "logo": SITE + "/images/logo.png", "founder": {"@id": SITE + "/#mark"},
       "sameAs": [SKOOL, "https://www.instagram.com/japanesegrimoire",
                  "https://www.tiktok.com/@japanesegrimoire", "https://www.pinterest.com/japanesegrimoire"]}

def esc(s): return html.escape(s, quote=True)

def load_articles():
    arts = []
    for f in sorted(glob.glob(os.path.join(ROOT, '_content', 'articles', '*.html'))):
        raw = open(f, encoding='utf-8').read()
        m = re.match(r'\s*<!--META\s*(\{.*?\})\s*META-->\s*(.*)$', raw, re.S)
        if not m: raise SystemExit('no META in ' + f)
        meta = json.loads(m.group(1)); meta['body'] = m.group(2).strip()
        words = len(re.sub(r'<[^>]+>', ' ', meta['body']).split())
        meta['words'] = words; meta['minutes'] = max(3, round(words / 230))
        arts.append(meta)
    arts.sort(key=lambda a: (a.get('rank', 99)))
    return arts

def jsonld(objs):
    return '\n'.join('<script type="application/ld+json">%s</script>' % json.dumps(o, ensure_ascii=False) for o in objs)

def head(title, desc, path, image, og_type='website', ld=(), preload=None):
    url = SITE + path
    img = SITE + image if image.startswith('/') else image
    pre = '<link rel="preload" as="image" href="%s" fetchpriority="high">\n' % preload if preload else ''
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="author" content="Dr. Mark Hosak">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Japanese Grimoire">
<meta property="og:locale" content="en_US">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{img}">
<link rel="icon" type="image/webp" href="/images/logo.webp">
<link rel="stylesheet" href="/fonts/google-selbst.css">
<link rel="stylesheet" href="/fonts/eb-garamond.css">
<link rel="stylesheet" href="/assets/site.css">
{pre}{jsonld(ld)}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
'''

def nav(active=''):
    items = [(h['slug'], h['nav']) for h in HUBS] + [('blog', 'Blog')]
    lis = ''.join('<li><a href="/%s%s"%s>%s</a></li>' % (s, '/' if s == 'blog' else '',
                  ' aria-current="page"' if s == active else '', esc(n)) for s, n in items)
    return f'''<header class="site-header">
<nav class="nav" aria-label="Main">
<a class="brand" href="/"><img src="/images/logo.webp" alt="" width="34" height="34"><span>Japanese Grimoire</span></a>
<button class="nav-toggle" aria-expanded="false" aria-controls="nav-links">Menu</button>
<ul class="nav-links" id="nav-links">{lis}<li><a class="nav-cta" href="{SKOOL}">The Society</a></li></ul>
</nav>
</header>
'''

def footer():
    hubs = ''.join('<li><a href="/%s">%s</a></li>' % (h['slug'], esc(h['name'])) for h in HUBS)
    return f'''<footer class="site-footer">
<div class="wrap">
<div class="foot-grid">
<div><p class="foot-brand">JAPANESE GRIMOIRE</p><p>The real Japanese traditions behind the hand signs, spirits and sacred places you know from anime. Written by Dr. Mark Hosak, Japanologist (PhD, Heidelberg), Shingon practitioner and researcher.</p></div>
<div><h4>Explore</h4><ul>{hubs}<li><a href="/blog/">All articles</a></li></ul></div>
<div><h4>Go deeper</h4><ul><li><a href="{SKOOL}">Japanese Grimoire Society</a></li><li><a href="/#join">Free practice by email</a></li><li><a href="https://www.shingon-reiki.com/en/kuji-kiri">Kuji Kiri live events</a></li><li><a href="https://markhosak.my-ablefy.com/s/markhosak/kuji-kiri-level-1-online-course?locale=en">Kuji Kiri Level 1 Online Course</a></li><li><a href="/shingon-reiki-level-1">Shingon Reiki Level 1</a></li><li><a href="https://www.shingon-reiki.com/en/japan">Journey to Japan 2027</a></li></ul></div>
<div><h4>Info</h4><ul><li><a href="/contact.html">Contact</a></li><li><a href="/privacy.html">Privacy Policy</a></li><li><a href="/impressum.html">Impressum</a></li><li><a href="https://www.instagram.com/japanesegrimoire">Instagram</a></li><li><a href="https://www.youtube.com/channel/UCn7IHhHHqZ7LP4aqaCtLM5w">YouTube</a></li></ul></div>
</div>
<p class="disclaimer">Japanese Grimoire is an independent project and is not affiliated with, endorsed by or connected to any anime or manga series, studio or publisher. Series and character names are trademarks of their respective owners and are mentioned for commentary only. All illustrations on this site are original artwork. Articles share history and background, not medical advice.<br>&copy; {datetime.date.today().year} Dr. Mark Hosak &middot; japanesegrimoire.com</p>
</div>
</footer>
<script src="/assets/site.js" defer></script>
</body>
</html>
'''

def optin_box(heading='The Energy Between Your Hands', text=None):
    text = text or 'A short practice from the Japanese tradition, free as a PDF: two minutes, breath and hands, no experience needed. After that, a few letters from me about the real tradition behind the anime.'
    return f'''<div class="invite">
<h2>{esc(heading)}</h2>
<p>{text}</p>
<form class="optin-form" novalidate>
<input type="email" name="email" placeholder="Your email address" autocomplete="email" required aria-label="Your email address">
<button type="submit" class="btn">Send me the practice</button>
<p class="form-status" role="status" aria-live="polite"></p>
</form>
<p class="fine">Free. Unsubscribe anytime. <a href="/privacy.html">Privacy policy</a></p>
</div>'''

def community_box(text):
    return f'''<div class="invite">
<h2>The Japanese Grimoire Society</h2>
<p>{text}</p>
<a class="btn" href="{SKOOL}">Have a look inside</a>
</div>'''

def card(a):
    hub = HUB_BY[a['hub']]
    return f'''<a class="card" href="/blog/{a['slug']}"><img src="/images/blog/{a['slug']}-card.webp" alt="{esc(a['image_alt'])}" width="800" height="450" loading="lazy"><div class="body"><span class="kicker">{esc(hub['name'])}</span><h3>{esc(a['h1'])}</h3><p>{esc(a['description'])}</p></div></a>'''

def crumbs(items):
    out = []
    for name, href in items:
        out.append('<a href="%s">%s</a>' % (href, esc(name)) if href else '<span aria-current="page" style="margin:0;opacity:1">%s</span>' % esc(name))
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<span>›</span>'.join(out) + '</nav>'

def bc_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        dict({"@type": "ListItem", "position": i + 1, "name": n}, **({"item": SITE + h} if h else {}))
        for i, (n, h) in enumerate(items)]}

def build_article(a, arts):
    hub = HUB_BY[a['hub']]
    path = '/blog/' + a['slug']
    img = '/images/blog/%s.webp' % a['slug']
    items = [('Home', '/'), (hub['name'], '/' + hub['slug']), (a['h1'], None)]
    ld = [{"@context": "https://schema.org", "@type": "BlogPosting", "headline": a['h1'],
           "description": a['description'], "image": SITE + img, "datePublished": a['date'],
           "dateModified": a.get('modified', a['date']), "inLanguage": "en-US",
           "author": MARK, "publisher": ORG, "mainEntityOfPage": SITE + path,
           "articleSection": hub['name'], "keywords": a.get('keywords', ''), "wordCount": a['words']},
          bc_ld(items)]
    if a.get('faq'):
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q['q'], "acceptedAnswer": {"@type": "Answer", "text": q['a']}} for q in a['faq']]})
    faq = ''
    if a.get('faq'):
        faq = '<section class="faq"><h2>Quick answers</h2>' + ''.join(
            '<details><summary>%s</summary><p>%s</p></details>' % (esc(q['q']), esc(q['a'])) for q in a['faq']) + '</section>'
    if a.get('invite') == 'newsletter':
        inv = optin_box(text=a.get('invite_text'))
    else:
        inv = community_box(a.get('invite_text') or 'This is where the practice lives: the deeper material, the sources, and a group of people who take this seriously and still have fun with it. You can start with a free trial.')
    sources = ''
    if a.get('sources'):
        sources = '<section class="sources"><h2>Sources and further reading</h2><ul>' + ''.join('<li>%s</li>' % s for s in a['sources']) + '</ul></section>'
    rel = [x for x in arts if x['slug'] in a.get('related', [])] or [x for x in arts if x['hub'] == a['hub'] and x['slug'] != a['slug']][:3]
    rel_html = ''
    if rel:
        rel_html = '<div class="wrap"><div class="section-head"><span class="kicker">Keep reading</span><h2>Related articles</h2></div><div class="cards">' + ''.join(card(x) for x in rel[:3]) + '</div></div>'
    date_h = datetime.date.fromisoformat(a['date']).strftime('%B %-d, %Y')
    page = head(a['title'], a['description'], path, img, 'article', ld, preload=img)
    page += nav(a['hub'])
    page += f'''<main id="main">
<article>
<div class="narrow">
{crumbs(items)}
<header class="art-head">
<span class="kicker"><a href="/{hub['slug']}">{esc(hub['name'])}</a></span>
<h1>{esc(a['h1'])}</h1>
<p class="dek">{a['dek']}</p>
<p class="byline">By <a href="#about-mark">Dr. Mark Hosak</a> &middot; <time datetime="{a['date']}">{date_h}</time> &middot; {a['minutes']} min read</p>
</header>
</div>
<figure class="hero-img"><img src="{img}" alt="{esc(a['image_alt'])}" width="1600" height="900" fetchpriority="high"></figure>
<div class="narrow prose">
{a['body']}
{inv}
{faq}
{sources}
<section class="author" id="about-mark"><img src="/images/mark-hosak.webp" alt="Dr. Mark Hosak" width="84" height="84" loading="lazy"><div><h3>Dr. Mark Hosak</h3><p>Japanologist with a PhD from Heidelberg University and about three years of research at Kyoto University on Buddhist art, architecture and ritual. Shingon practitioner and researcher, successor of Taguchi Sensei in his line of Ninjutsu, author of books on Reiki and its Japanese roots. He walked all 88 temples of the Shikoku pilgrimage on foot.</p></div></section>
</div>
</article>
{rel_html}
</main>
'''
    page += footer()
    out = os.path.join(PUB, 'blog', a['slug'] + '.html')
    open(out, 'w', encoding='utf-8').write(page)

def build_hub(h, arts):
    path = '/' + h['slug']
    mine = [a for a in arts if a['hub'] == h['slug']] + [a for a in arts if a['hub'] != h['slug'] and h['slug'] in a.get('also', [])]
    img = '/images/blog/%s.webp' % mine[0]['slug'] if mine else '/images/hero-bg.webp'
    items = [('Home', '/'), (h['name'], None)]
    ld = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": h['title'], "description": h['description'],
           "url": SITE + path, "inLanguage": "en-US", "isPartOf": {"@type": "WebSite", "name": "Japanese Grimoire", "url": SITE + "/"},
           "author": MARK, "hasPart": [{"@type": "BlogPosting", "headline": a['h1'], "url": SITE + '/blog/' + a['slug']} for a in mine]},
          bc_ld(items)]
    cards = ''.join(card(a) for a in mine)
    published = {a['h1'] for a in mine}
    planned = [p for p in h.get('planned', []) if p not in published]
    planned_html = ''
    if planned:
        planned_html = '<div class="section-head"><span class="kicker">In the works</span><h2>Coming to this section</h2></div><ul class="planned">' + ''.join('<li>%s</li>' % esc(p) for p in planned) + '</ul>'
    if h.get('invite') == 'newsletter':
        inv = optin_box(text=h.get('invite_text'))
    else:
        inv = community_box(h.get('invite_text'))
    others = ''.join('<a class="hub-tile" href="/%s"><b>%s</b><span>%s</span><small>%s</small></a>' % (o['slug'], o['kanji'], esc(o['name']), esc(o['short'])) for o in HUBS if o['slug'] != h['slug'])
    page = head(h['title'], h['description'], path, img, 'website', ld)
    page += nav(h['slug'])
    page += f'''<main id="main">
<section class="hub-hero">
<div class="bg" style="background-image:url('{img}')"></div>
<div class="big-kanji jp" aria-hidden="true">{h['kanji']}</div>
<div class="wrap"><div class="inner">
{crumbs(items)}
<span class="kicker">{esc(h['kicker'])}</span>
<h1>{esc(h['h1'])}</h1>
<p class="dek">{h['dek']}</p>
</div></div>
</section>
<div class="narrow prose" style="padding-top:2.5rem">
{h['intro']}
</div>
<div class="wrap">
<div class="section-head"><span class="kicker">Articles</span><h2>{esc(h['list_heading'])}</h2></div>
<div class="cards">{cards}</div>
{planned_html}
</div>
<div class="narrow">{inv}</div>
<div class="wrap"><div class="section-head"><span class="kicker">More of the grimoire</span><h2>Other sections</h2></div><div class="hub-grid">{others}</div></div>
</main>
'''
    page += footer()
    open(os.path.join(PUB, h['slug'] + '.html'), 'w', encoding='utf-8').write(page)

def build_blog(arts):
    path = '/blog/'
    items = [('Home', '/'), ('Blog', None)]
    ld = [{"@context": "https://schema.org", "@type": "Blog", "name": "Japanese Grimoire Blog", "url": SITE + path,
           "inLanguage": "en-US", "author": MARK, "publisher": ORG,
           "blogPost": [{"@type": "BlogPosting", "headline": a['h1'], "url": SITE + '/blog/' + a['slug'], "datePublished": a['date']} for a in arts]},
          bc_ld(items)]
    tiles = ''.join('<a class="hub-tile" href="/%s"><b>%s</b><span>%s</span><small>%s</small></a>' % (o['slug'], o['kanji'], esc(o['name']), esc(o['short'])) for o in HUBS)
    newest = sorted(arts, key=lambda a: (a['date'], -a.get('rank', 99)), reverse=True)
    page = head('Japanese Grimoire Blog · The Real Japan Behind the Anime', 'Kuji Kiri, yokai, kami, onmyodo and sacred places: articles by Japanologist Dr. Mark Hosak on the real Japanese traditions behind Naruto, Jujutsu Kaisen, Demon Slayer and more.', path, '/images/blog/%s.webp' % arts[0]['slug'], 'website', ld)
    page += nav('blog')
    page += f'''<main id="main">
<div class="wrap">
{crumbs(items)}
<header class="art-head" style="max-width:760px">
<span class="kicker">The Japanese Grimoire Blog</span>
<h1>The real Japan behind the anime</h1>
<p class="dek">You've seen it on screen. Here's where it actually comes from: the texts, the temples, the mountains and the people who still practice it.</p>
</header>
<div class="hub-grid">{tiles}</div>
<div class="section-head"><span class="kicker">All articles</span><h2>Latest from the grimoire</h2></div>
<div class="cards">{''.join(card(a) for a in newest)}</div>
</div>
<div class="narrow">{optin_box()}</div>
</main>
'''
    page += footer()
    open(os.path.join(PUB, 'blog', 'index.html'), 'w', encoding='utf-8').write(page)

def build_sitemap(arts):
    today = datetime.date.today().isoformat()
    urls = [('/', today, '1.0'), ('/blog/', today, '0.8')]
    urls += [('/' + h['slug'], today, '0.9') for h in HUBS]
    urls += [('/blog/' + a['slug'], a.get('modified', a['date']), '0.8') for a in arts]
    urls += [('/shingon-reiki-level-1', today, '0.6'), ('/contact.html', today, '0.3')]
    body = ''.join('  <url>\n    <loc>%s%s</loc>\n    <lastmod>%s</lastmod>\n    <priority>%s</priority>\n  </url>\n' % (SITE, u, d, p) for u, d, p in urls)
    open(os.path.join(PUB, 'sitemap.xml'), 'w', encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + '</urlset>\n')

def build_llms(arts):
    L = ['# Japanese Grimoire · japanesegrimoire.com', '',
         '> English-language site by Dr. Mark Hosak about the real Japanese traditions behind the hand signs, spirits and sacred places known from anime and manga: Kuji Kiri and mudras, yokai and kami, onmyodo, Shugendo, Shingon (esoteric Buddhism), Shinto, and the sacred places of Japan. Articles give history, background and meaning; practice happens in the Japanese Grimoire Society community and in live events. Not affiliated with any anime series.', '',
         '## About the author',
         '- Dr. Mark Hosak: Japanologist (PhD, Heidelberg University), about three years of research at Kyoto University on Buddhist art, architecture and ritual; Shingon practitioner and researcher; successor of Taguchi Sensei in his line of Ninjutsu; walked all 88 temples of the Shikoku pilgrimage; author of books on Reiki and its Japanese roots; founder of Shingon Reiki (https://www.shingon-reiki.com/en).', '',
         '## Start here',
         '- [Japanese Grimoire Society · free practice](%s/): Landing page with the free practice "The Energy Between Your Hands" (PDF by email).' % SITE,
         '- [Blog](%s/blog/): All articles.' % SITE,
         '- [Japanese Grimoire Society on Skool](%s): The community with practice, sources and live calls.' % SKOOL,
         '- [Shingon Reiki Level 1](%s/shingon-reiki-level-1): Live online initiation in English with Dr. Mark Hosak.' % SITE, '']
    for h in HUBS:
        L.append('## %s' % h['name'])
        L.append('- [%s](%s/%s): %s' % (h['title'], SITE, h['slug'], h['description']))
        for a in arts:
            if a['hub'] == h['slug']:
                L.append('- [%s](%s/blog/%s): %s' % (a['h1'], SITE, a['slug'], a['description']))
        L.append('')
    L += ['## Offers', '- Kuji Kiri live events and Master Path: https://www.shingon-reiki.com/en/kuji-kiri',
          '- Kuji Kiri Level 1 Online Course: https://markhosak.my-ablefy.com/s/markhosak/kuji-kiri-level-1-online-course?locale=en',
          '- Shingon Reiki Level 1 (English, live online): ' + SR1,
          '- Spiritual journey to Japan, May 2027: https://www.shingon-reiki.com/en/japan', '']
    open(os.path.join(PUB, 'llms.txt'), 'w', encoding='utf-8').write('\n'.join(L))

def build_home_latest(arts):
    p = os.path.join(PUB, 'index.html'); s = open(p, encoding='utf-8').read()
    newest = sorted(arts, key=lambda a: (a['date'], -a.get('rank', 99)), reverse=True)[:6]
    cards = ''.join('<a class="latest-card" href="/blog/%s"><img src="/images/blog/%s-card.webp" alt="%s" width="800" height="450" loading="lazy"><span>%s</span></a>' % (a['slug'], a['slug'], esc(a['image_alt']), esc(a['h1'])) for a in newest)
    block = '<!--LATEST-->\n  <div class="divider"></div>\n  <section class="latest reveal">\n    <div class="container" style="max-width:1100px">\n      <p class="section-label" style="text-align:center">From the grimoire</p>\n      <h2 class="section-title" style="text-align:center;margin-bottom:1.5rem">What anime borrowed from real Japan</h2>\n      <div class="latest-grid">' + cards + '</div>\n      <p class="latest-more"><a href="/blog/">All articles &rarr;</a></p>\n    </div>\n  </section>\n  <div class="divider"></div>\n<!--/LATEST-->'
    s = re.sub(r'<!--LATEST-->.*?<!--/LATEST-->', lambda m: block, s, flags=re.S)
    open(p, 'w', encoding='utf-8').write(s)

if __name__ == '__main__':
    arts = load_articles()
    for a in arts: build_article(a, arts)
    for h in HUBS: build_hub(h, arts)
    if arts: build_blog(arts)
    if arts: build_home_latest(arts)
    build_sitemap(arts)
    build_llms(arts)
    print('built %d articles, %d hubs' % (len(arts), len(HUBS)))
    for a in arts: print('  %-45s %5d words' % (a['slug'], a['words']))
