#!/usr/bin/env python3
"""Генерує внутрішні сторінки і блог для kyslipychki.shop. Запуск: python3 build_pages.py <repo>"""
import json, os, sys, html

REPO = sys.argv[1]
SITE = "https://kyslipychki.shop"
TODAY = "2026-11-27"
ORDER = "/#order"

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i18n_home import SLUGS, BRAND as BRAND_I18N, PRICES as PRICES_INTL

LANG = "uk"
GA = """<script async src="https://www.googletagmanager.com/gtm.js?id=GTM-NXWSKHWM"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());</script>"""
BRAND = {"uk": "Кислі пички", **BRAND_I18N}
HOME = {"uk": "/", "en": "/en/", "fr": "/fr/"}
ALT = {uk: {"uk": uk, "en": SLUGS["en"][uk], "fr": SLUGS["fr"][uk]} for uk in SLUGS["en"]}
REV = {v: k for k, m in ALT.items() for v in m.values()}
LOCALE = {"uk": "uk_UA", "en": "en_US", "fr": "fr_FR"}

UI = {
  "uk": dict(menu=[("/", "Головна"), ("/#how", "Як це працює"), ("/#prices", "Ціни"), ("/portret-po-foto/", "Портрет по фото"),
                   ("/sharzh-po-foto/", "Шарж по фото"), ("/blog/", "Блог"), ("/#faq", "Питання")],
             top=[("/portret-po-foto/", "Портрет по фото"), ("/sharzh-po-foto/", "Шарж по фото"), ("/blog/", "Блог")],
             main_menu="Головне меню", home_aria="Кислі пички, на головну", order="Замовити", order_portrait="Замовити портрет",
             burger="Меню", tagline="Портрети фарбами на полотні для тих, кому зараз сумно.", privacy="Політика конфіденційності",
             made="Сайт розроблено", more="Читати далі", blog_list="Статті блогу", stretched="полотно на підрамнику",
             cta="Надішли фото, художник намалює портрет фарбами на полотні.",
             price_note="Терміново за 48 годин: +666 ₴. Доставка Новою поштою за тарифами перевізника.",
             cookie="Ми використовуємо Google Analytics, щоб розуміти, звідки приходять люди і що їм цікаво. Без твоєї згоди аналітика не вмикається.",
             cookie_more="Детальніше", allow="Дозволити", deny="Лише необхідні",
             help="""<div class="help">
  <b>Якщо людина говорить, що не хоче жити, спершу не подарунок, а розмова з тими, хто вміє допомагати.</b>
  Lifeline Ukraine, цілодобово і безкоштовно:
  <div class="num">7333</div>
  Можна подзвонити або написати на <a href="https://lifelineukraine.com">lifelineukraine.com</a>.
</div>"""),
  "en": dict(menu=[("/en/", "Home"), ("/en/#how", "How it works"), ("/en/#prices", "Prices"), ("/en/portrait-from-photo/", "Portrait from photo"),
                   ("/en/caricature-from-photo/", "Caricature from photo"), ("/en/blog/", "Blog"), ("/en/#faq", "FAQ")],
             top=[("/en/portrait-from-photo/", "Portrait from photo"), ("/en/caricature-from-photo/", "Caricature"), ("/en/blog/", "Blog")],
             main_menu="Main menu", home_aria="Sour Mugs, home", order="Order", order_portrait="Order a portrait",
             burger="Menu", tagline="Painted portraits on canvas for anyone feeling sad.", privacy="Privacy policy",
             made="Website by", more="Read next", blog_list="Blog articles", stretched="stretched canvas",
             cta="Send a photo and an artist will paint the portrait on canvas.",
             price_note="Rush, in 48 hours: +$22 / +£16 / +€19. Shipping from Ukraine with Nova Post is quoted for your country before you pay.",
             cookie="We use Google Analytics to understand where visitors come from and what they find useful. It stays off unless you agree.",
             cookie_more="Learn more", allow="Allow", deny="Essential only",
             help="""<div class="help">
  <b>If someone talks about not wanting to live, a gift comes second. First, talk to people who know how to help.</b>
  Free, confidential, 24/7: UK and Ireland, Samaritans
  <div class="num">116 123</div>
  USA and Canada: call or text 988. Anywhere else: <a href="https://findahelpline.com">findahelpline.com</a>.
</div>"""),
  "fr": dict(menu=[("/fr/", "Accueil"), ("/fr/#how", "Comment ça marche"), ("/fr/#prices", "Prix"), ("/fr/portrait-photo-peinture/", "Portrait d'après photo"),
                   ("/fr/caricature-photo/", "Caricature d'après photo"), ("/fr/blog/", "Blog"), ("/fr/#faq", "Questions")],
             top=[("/fr/portrait-photo-peinture/", "Portrait d'après photo"), ("/fr/caricature-photo/", "Caricature"), ("/fr/blog/", "Blog")],
             main_menu="Menu principal", home_aria="Mines Boudeuses, accueil", order="Commander", order_portrait="Commander un portrait",
             burger="Menu", tagline="Des portraits peints sur toile pour celles et ceux qui ont le moral en berne.", privacy="Politique de confidentialité",
             made="Site réalisé par", more="À lire aussi", blog_list="Articles du blog", stretched="toile sur châssis",
             cta="Envoyez une photo, un artiste peindra le portrait sur toile.",
             price_note="Express en 48 heures : +19 €. La livraison depuis l'Ukraine avec Nova Post est chiffrée pour votre pays avant le paiement.",
             cookie="Nous utilisons Google Analytics pour comprendre d'où viennent les visiteurs et ce qui les intéresse. Rien n'est activé sans votre accord.",
             cookie_more="En savoir plus", allow="Accepter", deny="Refuser",
             help="""<div class="help">
  <b>Si la personne dit ne plus vouloir vivre, le cadeau attendra. Parlez d'abord à ceux qui savent aider.</b>
  Gratuit, 24 h/24 : France
  <div class="num">3114</div>
  Belgique : 0800 32 123 · Suisse : 143 · Canada : 988. Ailleurs : <a href="https://findahelpline.com/fr-FR">findahelpline.com</a>.
</div>"""),
}
SIZES_I18N = {"uk": [("sq", "Квадрат", "20×20 см"), ("pt", "Портрет", "30×40 см"), ("lg", "Великий портрет", "50×70 см")],
              "en": [("sq", "Square", "20×20 cm"), ("pt", "Portrait", "30×40 cm"), ("lg", "Large portrait", "50×70 cm")],
              "fr": [("sq", "Carré", "20×20 cm"), ("pt", "Portrait", "30×40 cm"), ("lg", "Grand portrait", "50×70 cm")]}
UAH = {"sq": 1700, "pt": 2666, "lg": 4111}


def u(key):
    """Шлях сторінки поточною мовою за українським ключем."""
    return ALT[key][LANG] if key in ALT else key


def order_link():
    return HOME[LANG] + "#order"


ORDER = "/#order"


def fmt_price(sid):
    if LANG == "uk":
        return f"{UAH[sid]:,} ₴".replace(",", " ")
    if LANG == "fr":
        return f"{PRICES_INTL['EUR'][sid]} €"
    return f"${PRICES_INTL['USD'][sid]} · £{PRICES_INTL['GBP'][sid]} · €{PRICES_INTL['EUR'][sid]}"


def nav():
    ui = UI[LANG]
    links = "".join(f'<a href="{a}">{t}</a>' for a, t in ui["menu"])
    top = "".join(f'\n  <a class="l" href="{a}">{t}</a>' for a, t in ui["top"])
    return f"""<nav aria-label="{ui['main_menu']}">
  <a class="logo" href="{HOME[LANG]}" aria-label="{ui['home_aria']}"><img src="{logo_src()}" alt="{BRAND[LANG]}" width="160" height="48"></a>{top}
  {langs_html()}
  <a class="btn" href="{order_link()}">{ui['order']}</a>
  <button class="burger" type="button" aria-label="{ui['burger']}" aria-expanded="false" aria-controls="menu"><span></span></button>
  <div class="menu" id="menu">{links}{langs_html(mobile=True)}</div>
</nav>
<script>(()=>{{const b=document.querySelector('.burger'),m=document.getElementById('menu');b.onclick=()=>{{const on=m.classList.toggle('on');b.setAttribute('aria-expanded',on);}};m.onclick=e=>{{if(e.target.tagName==='A'){{m.classList.remove('on');b.setAttribute('aria-expanded',false);}}}};}})();</script>"""


CUR_KEY = "/"


def langs_html(mobile=False):
    alts = ALT.get(CUR_KEY, HOME)
    names = {"uk": ("UA", "Українська"), "en": ("EN", "English"), "fr": ("FR", "Français")}
    a = "".join(f'<a href="{alts[l]}" lang="{l}" hreflang="{l}"{" aria-current=\"true\"" if l == LANG else ""}>{names[l][1 if mobile else 0]}</a>'
                for l in ("uk", "en", "fr"))
    return f'<span class="{"mlangs" if mobile else "langs"}">{a}</span>'


def logo_src():
    return "/logo-white.svg" if LANG == "uk" else f"/assets/logo-{LANG}-white.svg"


def footer():
    ui = UI[LANG]
    top = "".join(f'\n    <a href="{a}">{t}</a>' for a, t in ui["top"])
    return f"""<footer class="band">
  <div>
    <a class="logo" href="{HOME[LANG]}" aria-label="{BRAND[LANG]}"><img src="{logo_src()}" alt="{BRAND[LANG]}" width="186" height="56"></a>
    <span>{ui['tagline']}</span>
  </div>
  <div class="flinks">{top}
    <a href="{HOME[LANG]}#privacy">{ui['privacy']}</a>
    <span>{ui['made']} <a href="https://webrarium.com" target="_blank" rel="noopener">Webrarium</a></span>
  </div>
  <a class="btn" href="{order_link()}">{ui['order']}</a>
</footer>
<div class="cc" id="cc" hidden role="region" aria-label="Cookies">
  <p>{ui['cookie']} <a href="{HOME[LANG]}#privacy">{ui['cookie_more']}</a></p>
  <div class="row"><button class="btn" type="button" id="ccY">{ui['allow']}</button><button class="btn ghost" type="button" id="ccN">{ui['deny']}</button></div>
</div>
<script>(()=>{{const c=document.getElementById('cc');let v=null;try{{v=localStorage.getItem('kp_consent')}}catch(e){{}}
if(!v)c.hidden=false;const set=x=>{{try{{localStorage.setItem('kp_consent',x)}}catch(e){{}}c.hidden=true;if(x==='yes')gtag('consent','update',{{analytics_storage:'granted'}});}};
document.getElementById('ccY').onclick=()=>set('yes');document.getElementById('ccN').onclick=()=>set('no');}})();</script>"""


def help_block():
    return UI[LANG]["help"]


def price_cards(note=True):
    st = UI[LANG]["stretched"]
    cards = "".join(f'<div class="card"><b>{n}</b><div class="p">{fmt_price(i)}</div><p>{sz}, {st}</p></div>' for i, n, sz in SIZES_I18N[LANG])
    tail = f'<p class="meta">{UI[LANG]["price_note"]}</p>' if note else ""
    return f'<div class="cards{" cards-multi" if LANG == "en" else ""}">{cards}</div>{tail}'


def cta(text=None):
    return f'<div class="cta"><p>{text or UI[LANG]["cta"]}</p><a class="btn" href="{order_link()}">{UI[LANG]["order_portrait"]}</a></div>'


def faq_html(faqs):
    return "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs)


def faq_ld(faqs):
    import re
    strip = lambda s: re.sub(r"<[^>]+>", "", s)
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in faqs]}


def crumbs_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]}


def crumbs_html(items):
    parts = [f'<a href="{u}">{n}</a>' for n, u in items[:-1]] + [items[-1][0]]
    return '<div class="crumbs">' + " → ".join(parts) + "</div>"


def offer_ld(name, desc, url):
    return {"@type": "Product", "name": name, "description": desc, "url": SITE + url,
            "image": [SITE + wide(url), SITE + "/after.jpg"], "brand": {"@type": "Brand", "name": BRAND[LANG]},
            "offers": offers_ld()}


def offers_ld():
    if LANG == "uk":
        return {"@type": "AggregateOffer", "priceCurrency": "UAH", "lowPrice": 1700, "highPrice": 4111,
                "offerCount": 3, "availability": "https://schema.org/InStock"}
    curs = ["EUR"] if LANG == "fr" else ["USD", "GBP", "EUR"]
    o = [{"@type": "AggregateOffer", "priceCurrency": c, "lowPrice": PRICES_INTL[c]["sq"], "highPrice": PRICES_INTL[c]["lg"],
          "offerCount": 3, "availability": "https://schema.org/InStock"} for c in curs]
    return o if len(o) > 1 else o[0]


def page(path, title, desc, body, graph, og_type="website", image=None):
    global CUR_KEY
    CUR_KEY = REV.get(path, path)
    url = SITE + path
    image = image or wide(path)
    graph = graph + [{"@type": "WebPage", "@id": url, "url": url, "name": title, "inLanguage": LANG,
                      "primaryImageOfPage": {"@type": "ImageObject", "url": SITE + image, "width": 1200, "height": 630},
                      "isPartOf": {"@type": "WebSite", "url": SITE + HOME[LANG], "name": BRAND[LANG]}},
                     {"@type": "SiteNavigationElement", "name": [t for _, t in UI[LANG]["menu"]], "url": [SITE + a for a, _ in UI[LANG]["menu"]]}]
    if CUR_KEY in COVERS or CUR_KEY == "/blog/":
        items = more_items(path) if CUR_KEY != "/blog/" else [c for c in cards_list() if REV.get(c[0], c[0]).startswith("/blog/")]
        graph.append(cards_ld(items, UI[LANG]["more"] if CUR_KEY != "/blog/" else UI[LANG]["blog_list"]))
    org = {"@type": "Organization", "@id": SITE + "/#org", "name": BRAND[LANG], "alternateName": ["Кислі пички", "Sour Mugs", "Mines Boudeuses"],
           "url": SITE + HOME[LANG], "logo": SITE + logo_src().replace("-white", ""), "email": "kyslipychki@gmail.com"}
    ld = json.dumps({"@context": "https://schema.org", "@graph": [org] + graph}, ensure_ascii=False)
    alts = ALT.get(CUR_KEY)
    alt_links = ("".join(f'\n<link rel="alternate" hreflang="{l}" href="{SITE}{alts[l]}">' for l in ("uk", "en", "fr"))
                 + f'\n<link rel="alternate" hreflang="x-default" href="{SITE}{alts["en"]}">') if alts else ""
    doc = f"""<!DOCTYPE html>
<html lang="{LANG}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">{alt_links}
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#ffd23f">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="{LOCALE[LANG]}">
<meta property="og:site_name" content="{BRAND[LANG]}">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{SITE}{image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/admin/icon-192.png">
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}
gtag('consent','default',{{analytics_storage:'denied',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied'}});
try{{if(localStorage.getItem('kp_consent')==='yes')gtag('consent','update',{{analytics_storage:'granted'}});}}catch(e){{}}</script>
{GA}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Nunito:wght@400;600;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/page.css">
<script type="application/ld+json">{ld}</script>
</head>
<body>
{nav()}
{body}
{footer()}
</body>
</html>
"""
    out = os.path.join(REPO, path.strip("/"), "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(doc)
    return path


COVERS = {
    "/": ("/assets/covers/home.jpg", "Сумне фото, портрет фарбами і сміх людини, якій його подарували"),
    "/portret-po-foto/": ("/assets/covers/portret.jpg", "Портрет по фото фарбами на полотні"),
    "/sharzh-po-foto/": ("/assets/covers/sharzh.jpg", "Шарж пастеллю: дівчина та її гора депресії"),
    "/blog/shcho-podaruvaty-druhu-yakomu-vazhko/": ("/assets/covers/podaruvaty.jpg", "Людина сміється, побачивши подарований портрет"),
    "/blog/druk-chy-zhyvopys-portret-z-foto/": ("/assets/covers/druk.jpg", "Рука художника на тлі портрета фарбами"),
}
WIDE = {k: v[0].replace(".jpg", "-wide.jpg") for k, v in COVERS.items() if k != "/"}
WIDE["/"] = "/og.jpg"
COVER_ALT = {
    "en": {"/": "A sad photo, a painted portrait and the laugh of the person who received it", "/portret-po-foto/": "Portrait painted on canvas from a photo",
           "/sharzh-po-foto/": "Pastel caricature: a girl and her mountain of depression", "/blog/shcho-podaruvaty-druhu-yakomu-vazhko/": "Laughing after seeing the portrait they were given",
           "/blog/druk-chy-zhyvopys-portret-z-foto/": "The artist's hand against a painted portrait"},
    "fr": {"/": "Une photo triste, un portrait peint et le rire de la personne qui l'a reçu", "/portret-po-foto/": "Portrait peint sur toile d'après une photo",
           "/sharzh-po-foto/": "Caricature au pastel : une jeune femme et sa montagne de déprime", "/blog/shcho-podaruvaty-druhu-yakomu-vazhko/": "Fou rire en découvrant le portrait offert",
           "/blog/druk-chy-zhyvopys-portret-z-foto/": "La main de l'artiste devant un portrait peint"}}
CARDS_I18N = {
    "en": [("/", "Sad photo = funny portrait", "How we turn a sad photo into a warm, funny painting."),
           ("/portret-po-foto/", "Custom portrait from a photo", "Painted by hand on canvas, shipped worldwide."),
           ("/sharzh-po-foto/", "Caricature from a photo on canvas", "A kind caricature where the situation is funny, not their looks."),
           ("/blog/shcho-podaruvaty-druhu-yakomu-vazhko/", "Gifts for a friend going through a hard time", "9 no-pressure ideas and how to give them gently."),
           ("/blog/druk-chy-zhyvopys-portret-z-foto/", "Canvas print vs hand-painted portrait", "The difference, and how not to buy a print sold as a painting.")],
    "fr": [("/", "Photo triste = portrait drôle", "Comment une photo triste devient un tableau tendre et drôle."),
           ("/portret-po-foto/", "Portrait sur mesure d'après photo", "Peint à la main sur toile, dès 49 €."),
           ("/sharzh-po-foto/", "Caricature d'après photo sur toile", "Une caricature tendre : la situation est drôle, pas le physique."),
           ("/blog/shcho-podaruvaty-druhu-yakomu-vazhko/", "Quel cadeau pour un ami qui va mal", "9 idées sans pression et comment offrir avec délicatesse."),
           ("/blog/druk-chy-zhyvopys-portret-z-foto/", "Impression sur toile ou peinture", "La différence, et comment ne pas acheter une impression vendue comme un tableau.")]}


def wide(path):
    k = REV.get(path, path)
    if k == "/":
        return "/og.jpg" if LANG == "uk" else f"/og-{LANG}.jpg"
    return WIDE.get(k, "/og.jpg")


def cards_list():
    if LANG == "uk":
        return CARDS
    return [(ALT[k][LANG], t, d) for k, t, d in CARDS_I18N[LANG]]


def cover(path):
    k = REV.get(path, path)
    img, alt = COVERS[k]
    return img, (alt if LANG == "uk" else COVER_ALT[LANG][k])
CARDS = [("/", "Сумна фотка = смішний портрет", "Як ми перетворюємо сумне фото на теплу смішну картину фарбами."),
         ("/portret-po-foto/", "Портрет по фото на замовлення", "Живопис фарбами на полотні, від 1700 ₴, доставка по Україні."),
         ("/sharzh-po-foto/", "Шарж по фото на полотні", "Добрий шарж, де смішні обставини, а не зовнішність."),
         ("/blog/shcho-podaruvaty-druhu-yakomu-vazhko/", "Що подарувати другу, якому зараз важко", "9 ідей без тиску і як подарувати делікатно."),
         ("/blog/druk-chy-zhyvopys-portret-z-foto/", "Друк на полотні чи живопис", "У чому різниця і як не купити друк під виглядом картини.")]


def card(u, t, d):
    img, alt = cover(u)
    return (f'<a class="pcard" href="{u}"><img src="{img}" alt="{alt}" width="600" height="450" loading="lazy">'
            f'<span class="pc-t">{t}</span><span class="pc-d">{d}</span></a>')


def cards_ld(items, name):
    return {"@type": "ItemList", "name": name, "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": SITE + u, "name": t, "image": SITE + cover(u)[0]}
        for i, (u, t, d) in enumerate(items)]}


def more_items(exclude):
    return [c for c in cards_list() if c[0] != exclude]


def more_links(exclude):
    return (f'<section class="band more"><div class="wrap"><h2>{UI[LANG]["more"]}</h2><div class="pcards">'
            + "".join(card(*c) for c in more_items(exclude)) + '</div></div></section>')


def hero_cover(u):
    return (f'<figure class="cover"><img src="{wide(u)}" alt="{cover(u)[1]}" width="1200" height="630" fetchpriority="high"></figure>')


def old_more_links(exclude):
    links = [("/portret-po-foto/", "Портрет по фото на замовлення"),
             ("/sharzh-po-foto/", "Шарж по фото на полотні"),
             ("/blog/shcho-podaruvaty-druhu-yakomu-vazhko/", "Що подарувати другу, якому зараз важко"),
             ("/blog/druk-chy-zhyvopys-portret-z-foto/", "Друк на полотні чи живопис: у чому різниця"),
             ("/", "Кислі пички: сумна фотка = смішний портрет")]
    li = "".join(f'<li><a href="{u}">{t}</a></li>' for u, t in links if u != exclude)
    return f'<section class="band more"><div class="narrow"><h2>Читати далі</h2><ul>{li}</ul></div></section>'


pages = []

# ---------- 1. Портрет по фото ----------
P = "/portret-po-foto/"
faq1 = [
    ("Скільки коштує портрет по фото?", "1700 ₴ за квадрат 20×20 см, 2666 ₴ за портрет 30×40 см і 4111 ₴ за великий портрет 50×70 см. Ціна залежить лише від розміру полотна, техніку обираєш без доплати. Термінове виконання за 48 годин коштує +666 ₴."),
    ("Це друк чи справді малюють?", "Справді малюють. Художник пише портрет фарбами на полотні, вручну, без друку, планшета і нейромереж. На картині видно мазки й фактуру фарби."),
    ("Яке фото потрібне для портрета?", "Підійде звичайне фото з телефона, де видно обличчя й емоцію: селфі, кадр із відеодзвінка, фото з-під ковдри. Ідеальна якість не потрібна."),
    ("Скільки часу малюють портрет?", "Зазвичай 3–5 днів, термінове замовлення за 48 годин. Доставка Новою поштою додає 1–3 дні."),
]
body = f"""<header class="hero band"><div class="wrap grid">
  <div>
    {crumbs_html([("Головна", "/"), ("Портрет по фото", P)])}
    <h1>Портрет по фото на замовлення: фарбами на полотні</h1>
    <p class="lead">Надсилаєш фото, художник малює портрет фарбами на справжньому полотні з підрамником. Руками, а не принтером. Від 1700 ₴, доставка по Україні Новою поштою.</p>
    <div class="ctas"><a class="btn" href="{ORDER}">Замовити портрет</a><a class="btn ghost" href="#prices">Ціни</a></div>
  </div>
  <figure><img src="/after.jpg" alt="Портрет по фото, намальований фарбами на полотні" width="900" height="1261"><figcaption>намальовано руками</figcaption></figure>
</div></header>
<main class="band"><article class="narrow">
  <h2>Чим наш портрет відрізняється від «картини з фото»</h2>
  <p>Більшість пропозицій «портрет з фото на полотні» насправді друк: фото обробляють у редакторі й друкують на тканині. Ми робимо інакше. Художник дивиться на твоє фото і пише картину з нуля, мазок за мазком. Тому кожен портрет єдиний у своєму роді, а на полотні видно живу фактуру фарби. Детальніше про різницю пишемо в статті <a href="/blog/druk-chy-zhyvopys-portret-z-foto/">«Друк на полотні чи живопис»</a>.</p>
  <p>І ще одна відмінність: ми малюємо не парадні портрети, а теплі й трохи смішні. Як саме це працює, показуємо на головній: <a href="/">сумна фотка перетворюється на смішний портрет з фото на полотні</a>. Сумна фотка стає картиною, на якій смішними є обставини: власна дощова хмаринка, гора посуду, кіт, що сидить на голові. Над зовнішністю не жартуємо ніколи.</p>

  <h2 id="prices">Ціни на портрет по фото</h2>
  {price_cards()}

  <h2>Як замовити портрет з фото</h2>
  <ol>
    <li><b>Завантаж фото</b> у форму на сайті і напиши пару слів про людину: що любить, що зараз її гнітить, чого точно не торкатися.</li>
    <li><b>Обери розмір і техніку.</b> Ціна залежить лише від розміру.</li>
    <li><b>Художник малює</b> 3–5 днів, або 48 годин у терміновому режимі.</li>
    <li><b>Отримуєш картину</b> Новою поштою, на підрамнику, готову повісити на стіну.</li>
  </ol>
  {cta()}

  <h2>Яке фото підійде</h2>
  <p>Будь-яке, на якому видно обличчя й настрій. Не треба студійної зйомки: селфі в маршрутці, кадр із відеодзвінка, фото з-під ковдри підходять навіть краще, бо в них є емоція. Якщо фото дуже темне чи розмите, ми напишемо і попросимо інше.</p>

  <h2>Портрет у подарунок</h2>
  <p>Хочеш більше гумору? Подивись <a href="/sharzh-po-foto/">шарж по фото</a>: там смішніші сюжети навколо людини.</p>
  <p>Найчастіше портрет замовляють як подарунок другу, якому зараз важко. Картина приходить тобі, а не людині на фото, тож ти сам вирішуєш, коли і як її подарувати. Ідеї, як зробити це делікатно, зібрали в статті <a href="/blog/shcho-podaruvaty-druhu-yakomu-vazhko/">«Що подарувати другу, якому зараз важко»</a>.</p>

  <h2>Питання про портрет по фото</h2>
  {faq_html(faq1)}
</article></main>
{more_links(P)}"""
pages.append(page(P, "Портрет по фото на замовлення фарбами на полотні — Кислі пички",
    "Портрет по фото, намальований художником руками фарбами на полотні, а не друк. Від 1700 ₴, 3–5 днів, доставка Новою поштою по Україні.",
    body, [offer_ld("Портрет по фото на полотні", "Портрет по фото, намальований художником фарбами на полотні", P), faq_ld(faq1),
           crumbs_ld([("Головна", "/"), ("Портрет по фото", P)])]))

# ---------- 2. Шарж по фото ----------
S = "/sharzh-po-foto/"
faq2 = [
    ("Чим ваш шарж відрізняється від звичайного?", "Класичний шарж перебільшує риси обличчя. Ми перебільшуємо обставини: власну хмаринку над головою, гору справ, ковдру-фортецю. Людина на картині впізнавана і гарна, смішна ситуація навколо неї."),
    ("Шарж намальований на планшеті?", "Ні. Кожен шарж малюють руками фарбами на полотні з підрамником. Ніякого планшета, друку чи нейромереж."),
    ("Скільки коштує шарж по фото?", "Від 1700 ₴ за полотно 20×20 см, 2666 ₴ за 30×40 см і 4111 ₴ за 50×70 см. Терміново за 48 годин: +666 ₴."),
    ("А якщо людина образиться?", "Ми малюємо з любов'ю і не жартуємо над зовнішністю. У формі можна написати, яких тем точно не торкатися. А дарувати чи ні, вирішуєш ти: картина приходить тобі."),
    ("Можна шарж для себе?", "Звісно. Іноді найкраще, що можна зробити з поганим днем, це повісити його на стіну і посміятися."),
]
body = f"""<header class="hero band"><div class="wrap grid">
  <div>
    {crumbs_html([("Головна", "/"), ("Шарж по фото", S)])}
    <h1>Шарж по фото на полотні, намальований руками</h1>
    <p class="lead">Добрий, смішний шарж із сумного фото. Художник малює його фарбами на справжньому полотні: це подарунок, який повісять на стіну, а не картинка в телефоні. Від 1700 ₴.</p>
    <div class="ctas"><a class="btn" href="{ORDER}">Замовити шарж</a><a class="btn ghost" href="#how">Як це працює</a></div>
  </div>
  <figure><img src="/before.jpg" alt="Сумне селфі, з якого художник малює шарж" width="720" height="899"><figcaption>було сумно</figcaption></figure>
</div></header>
<main class="band"><article class="narrow">
  <h2>Шарж, над яким сміються разом</h2>
  <p>Звичайний шарж збільшує ніс і вуха. Наш шарж збільшує обставини. Якщо в людини тиждень, як осіння злива, на картині над нею буде власна маленька хмаринка. Якщо вона тоне в дедлайнах, то сидітиме на горі паперів із чашкою кави. Людина лишається собою і гарною, смішною стає ситуація.</p>
  <p>Тому такий шарж можна подарувати навіть тому, кому зараз невесело. Приклади «було / стало» є на <a href="/">головній сторінці Кислих пичок</a>. Він не каже «збадьорся», він каже «я бачу, як тобі, і я поруч».</p>

  <h2 id="how">Як ми малюємо шарж по фото</h2>
  <ol>
    <li><b>Ти надсилаєш фото</b> і пишеш кілька слів: що в людини відбувається, що вона любить, чого не торкатися.</li>
    <li><b>Художник придумує сюжет</b> із цих деталей і малює його фарбами на полотні: олією, акрилом або пастеллю.</li>
    <li><b>Картина приїжджає</b> Новою поштою на підрамнику, готова висіти на стіні. Зазвичай за 3–5 днів, терміново за 48 годин.</li>
  </ol>
  <figure style="margin:24px 0"><img src="/gift.jpg" alt="Шарж фарбами на полотні: дівчина і її гора депресії" width="900" height="1200" loading="lazy" style="border:2px solid var(--ink);border-radius:12px;width:100%;max-width:420px"></figure>

  <h2>Ціни на шарж</h2>
  {price_cards()}
  {cta("Сумне фото є? Значить, шарж уже майже готовий.")}

  <h2>Кому дарують такий шарж</h2>
  <ul>
    <li><b>Другу, якому зараз важко.</b> Лагідний спосіб сказати «я поруч» без зайвих слів.</li>
    <li><b>Колезі, що вигорів</b> на проєкті, як привід посміятися разом, а не з нього.</li>
    <li><b>Собі</b>, щоб повісити поганий день на стіну і більше його не боятися.</li>
  </ul>
  <p>Шукаєш класичніший варіант? Подивись <a href="/portret-po-foto/">портрет по фото</a>: той самий живопис на полотні, з меншою часткою жарту.</p>

  <h2>Питання про шарж по фото</h2>
  {faq_html(faq2)}
</article></main>
{more_links(S)}"""
pages.append(page(S, "Шарж по фото на полотні фарбами в подарунок — Кислі пички",
    "Добрий шарж по фото, намальований руками фарбами на полотні. Смішні обставини, а не зовнішність. Від 1700 ₴, 3–5 днів, доставка по Україні.",
    body, [offer_ld("Шарж по фото на полотні", "Шарж по фото, намальований художником фарбами на полотні", S), faq_ld(faq2),
           crumbs_ld([("Головна", "/"), ("Шарж по фото", S)])]))

# ---------- 3. Блог: що подарувати ----------
B1 = "/blog/shcho-podaruvaty-druhu-yakomu-vazhko/"
t1 = "Що подарувати другу, якому зараз важко: 9 ідей без тиску"
d1 = "Як підтримати подарунком друга, у якого депресія чи важкий період: 9 ідей, що дарувати не варто і як подарувати делікатно."
body = f"""<main class="band"><article class="narrow">
  {crumbs_html([("Головна", "/"), ("Блог", "/blog/"), ("Що подарувати другу, якому важко", B1)])}
  <h1>{t1}</h1>
  <p class="meta">26 листопада 2026 · 6 хвилин читання</p>
  {hero_cover(B1)}
  <p>Коли другу погано, хочеться щось зробити, але незрозуміло що. Слова звучать фальшиво, порада «тримайся» не допомагає, а великий жест може налякати. Подарунок тут працює як записка без слів: «я про тебе думаю, нічого від тебе не чекаю». Головне, щоб він не вимагав від людини сил, яких у неї зараз немає.</p>
  <p>Ми не психологи. Ця добірка про турботу, а не про лікування. Депресія лікується у фахівців, а подарунок лише нагадує людині, що вона не сама.</p>

  <h2>9 ідей подарунка для друга, якому зараз важко</h2>
  <h3>1. Їжа, яку не треба готувати</h3>
  <p>Коли немає сил, першим зникає нормальна їжа. Доставка улюбленої страви, суп у контейнерах на кілька днів чи сертифікат у кафе біля дому знімають одну щоденну задачу.</p>
  <h3>2. Допомога з побутом</h3>
  <p>Оплачене прибирання, прання чи просто «я прийду в суботу і помию посуд». Це звучить буденно, але гора немитого посуду для людини в депресії буває справжньою горою.</p>
  <h3>3. Щось м'яке і тепле</h3>
  <p>Плед, теплі шкарпетки, худі на розмір більше. Речі, в які можна загорнутися, дають відчуття безпеки без жодних зусиль.</p>
  <h3>4. Записка або лист від руки</h3>
  <p>Кілька чесних речень: за що ти цінуєш друга, який спільний спогад тебе смішить. Без «все буде добре». Такі записки зберігають роками.</p>
  <h3>5. Спільний час без зобов'язань</h3>
  <p>«Я буду поруч у неділю, можемо подивитися серіал, можемо мовчати». Важливо дати можливість відмовитися без провини.</p>
  <h3>6. Кімнатна рослина, яку важко вбити</h3>
  <p>Сансев'єрія чи замікулькас переживуть і тиждень без поливу. Живе зелене поруч тихо радує, а не стає ще одним обов'язком.</p>
  <h3>7. Аудіокнига чи подкаст замість паперової книжки</h3>
  <p>Читати складно, коли важко зосередитися. Слухати можна лежачи, і для цього не треба сил.</p>
  <h3>8. Картина, яка змушує усміхнутися</h3>
  <p>Ми самі робимо такі подарунки, тож скажемо чесно, навіщо вони. Сумне фото друга художник перетворює на <a href="/sharzh-po-foto/">добрий шарж фарбами на полотні</a>: смішними стають обставини, а не людина. Картина лишається на стіні й тихо нагадує, що хтось бачить, як тобі, і сміється разом з тобою, а не з тебе. Як це виглядає, <a href="/">показуємо на головній</a>.</p>
  <h3>9. Оплачена консультація фахівця, але лише за згодою</h3>
  <p>Якщо друг сам говорив, що хоче піти до психолога, але відкладає через гроші, допомога з оплатою може бути найціннішим подарунком. Не дарувати сюрпризом і не наполягати.</p>

  <h2>Чого краще не дарувати</h2>
  <ul>
    <li><b>Книжки «як стати щасливим»</b> і мотиваційні постери. Вони звучать як докір.</li>
    <li><b>Абонемент у спортзал</b> з натяком «тобі треба рухатися». Це ще один обов'язок, який людина не виконає і за який картатиме себе.</li>
    <li><b>Великі сюрпризи і вечірки.</b> Увага натовпу буває виснажливою.</li>
    <li><b>Алкоголь.</b> Він погіршує стан і погано поєднується з ліками.</li>
  </ul>

  <h2>Як подарувати делікатно</h2>
  <ul>
    <li><b>Без очікувань.</b> Не чекай радісної реакції чи довгої подяки. Тихе «дякую» вже багато.</li>
    <li><b>Без умов.</b> Подарунок, а не обмін на «тепер ти маєш зібратися».</li>
    <li><b>Наодинці.</b> Не при всіх, щоб людина могла реагувати так, як їй зараз вдається.</li>
    <li><b>І потім залишайся поруч.</b> Подарунок відкриває розмову, але не замінює її.</li>
  </ul>
  {help_block()}
  {cta("Хочеш подарувати другу картину, на яку не можна дивитися без усмішки?")}
</article></main>
{more_links(B1)}"""
pages.append(page(B1, t1 + " — Кислі пички", d1, body, [
    {"@type": "BlogPosting", "headline": t1, "description": d1, "datePublished": TODAY, "dateModified": TODAY,
     "inLanguage": "uk", "mainEntityOfPage": SITE + B1, "image": SITE + WIDE[B1],
     "author": {"@type": "Organization", "name": "Кислі пички", "url": SITE + "/"},
     "publisher": {"@id": SITE + "/#org"}},
    crumbs_ld([("Головна", "/"), ("Блог", "/blog/"), ("Що подарувати другу, якому важко", B1)])], og_type="article"))

# ---------- 4. Блог: друк чи живопис ----------
B2 = "/blog/druk-chy-zhyvopys-portret-z-foto/"
t2 = "Картина з фото: друк на полотні чи живопис руками — у чому різниця"
d2 = "Чим портрет, намальований фарбами, відрізняється від друку фото на полотні: ціна, вигляд, термін, як не купити друк під виглядом картини."
body = f"""<main class="band"><article class="narrow">
  {crumbs_html([("Головна", "/"), ("Блог", "/blog/"), ("Друк чи живопис", B2)])}
  <h1>{t2}</h1>
  <p class="meta">26 листопада 2026 · 5 хвилин читання</p>
  {hero_cover(B2)}
  <p>Шукаєш «картину з фото на полотні» і бачиш сотні пропозицій із дуже різними цінами: від кількох сотень гривень до кількох тисяч. Здебільшого причина не в жадібності художників, а в тому, що під однією назвою продають два різні продукти: <b>друк</b> і <b>живопис</b>.</p>

  <h2>Коротко: чим вони відрізняються</h2>
  <div class="scroll"><table class="tbl">
    <tr><th></th><th>Друк фото на полотні</th><th>Портрет фарбами</th></tr>
    <tr><td><b>Як роблять</b></td><td>Фото обробляють у редакторі й друкують принтером на тканині</td><td>Художник пише картину з нуля, дивлячись на фото</td></tr>
    <tr><td><b>Поверхня</b></td><td>Рівна, як у фотографії</td><td>Видно мазки, рельєф фарби, сліди пензля</td></tr>
    <tr><td><b>Унікальність</b></td><td>Можна надрукувати скільки завгодно копій</td><td>Одна-єдина картина</td></tr>
    <tr><td><b>Термін</b></td><td>Зазвичай 1–2 дні</td><td>Кілька днів роботи художника</td></tr>
    <tr><td><b>Ціна</b></td><td>У рази дешевше</td><td>Дорожче, бо це години ручної роботи</td></tr>
    <tr><td><b>Можна змінити сюжет</b></td><td>Лише фільтри й колаж</td><td>Так: додати деталі, жарт, інший фон</td></tr>
  </table></div>

  <h2>Коли обрати друк</h2>
  <p>Друк чесний і корисний, коли потрібна саме фотографія у великому форматі: весільне фото на стіну, пейзаж із подорожі, сімейний знімок для бабусі. Швидко, недорого, точно як на фото.</p>

  <h2>Коли обрати живопис</h2>
  <p>Живопис потрібен, коли важлива не точна копія, а погляд художника: щось додати, перебільшити, пожартувати, передати настрій. Такий портрет сприймають як мистецтво і подарунок «на роки», а не як фото в рамці. Саме так ми працюємо в <a href="/">Кислих пичках</a>: <a href="/portret-po-foto/">портрет по фото</a> або <a href="/sharzh-po-foto/">шарж по фото</a> малюють руками фарбами на полотні.</p>

  <h2>Як не купити друк під виглядом картини</h2>
  <ul>
    <li><b>Шукай слова «друк», «печать», «фотоплотер», «полотно з вашим фото»</b> в описі. Це майже завжди принтер.</li>
    <li><b>Попроси фото процесу.</b> Художник легко покаже недомальоване полотно чи палітру.</li>
    <li><b>Подивися на прикладах фактуру крупним планом:</b> у живопису видно мазки й нерівності фарби.</li>
    <li><b>Зверни увагу на «стилізацію під олію».</b> Часто це цифровий фільтр, надрукований на полотні.</li>
    <li><b>Порівняй ціну з терміном.</b> Велика «картина маслом» за пару сотень гривень і за день навряд чи намальована вручну.</li>
  </ul>
  <p>Окремий випадок: цифровий портрет на планшеті. Його малює людина, але результат так само друкують. Це гарний варіант, якщо хочеш стилізацію, але не живопис.</p>
  {cta("Хочеш саме живопис, з мазками і характером?")}
</article></main>
{more_links(B2)}"""
pages.append(page(B2, "Друк на полотні чи портрет фарбами: у чому різниця — Кислі пички", d2, body, [
    {"@type": "BlogPosting", "headline": t2, "description": d2, "datePublished": TODAY, "dateModified": TODAY,
     "inLanguage": "uk", "mainEntityOfPage": SITE + B2, "image": SITE + WIDE[B2],
     "author": {"@type": "Organization", "name": "Кислі пички", "url": SITE + "/"},
     "publisher": {"@id": SITE + "/#org"}},
    crumbs_ld([("Головна", "/"), ("Блог", "/blog/"), ("Друк чи живопис", B2)])], og_type="article"))

# ---------- 5. Блог: список ----------
BL = "/blog/"
posts = [(B1, t1, d1), (B2, t2, d2)]
cards = "".join(f'<a class="post" href="{u}"><img src="{COVERS[u][0]}" alt="{COVERS[u][1]}" width="600" height="450" loading="lazy"><h2>{t}</h2><p>{d}</p></a>' for u, t, d in posts)
body = f"""<main class="band"><div class="wrap">
  {crumbs_html([("Головна", "/"), ("Блог", BL)])}
  <h1>Блог Кислих пичок</h1>
  <p>Про подарунки людям, яким зараз важко, про живопис і про те, як сумне фото стає смішною картиною.</p>
  <div class="posts">{cards}</div>
</div></main>"""
pages.append(page(BL, "Блог про подарунки й портрети з фото — Кислі пички",
    "Статті Кислих пичок: що подарувати другу, якому важко, чим живопис відрізняється від друку, як замовити портрет з фото.",
    body, [{"@type": "Blog", "name": "Блог Кислих пичок", "url": SITE + BL, "inLanguage": "uk",
            "blogPost": [{"@type": "BlogPosting", "headline": t, "url": SITE + u} for u, t, d in posts]},
           crumbs_ld([("Головна", "/"), ("Блог", BL)])]))

# ---------- англійська і французька ----------
import pages_i18n
for _l in ("en", "fr"):
    pages += pages_i18n.build(_l, sys.modules[__name__])
LANG = "uk"

# ---------- sitemap з hreflang ----------
urls = []
for key in ["/"] + [REV.get(p, p) for p in pages]:
    if key not in [k for k, _ in urls]:
        urls.append((key, ALT.get(key, {"uk": key})))
items = []
for key, alts in urls:
    links = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{SITE}{alts[l]}"/>' for l in ("uk", "en", "fr") if l in alts)
    if "en" in alts:
        links += f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{alts["en"]}"/>'
    for l in ("uk", "en", "fr"):
        if l in alts:
            items.append(f"  <url><loc>{SITE}{alts[l]}</loc><lastmod>{TODAY}</lastmod>{links}</url>\n")
sm = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
      + "".join(items) + "</urlset>\n")
open(os.path.join(REPO, "sitemap.xml"), "w").write(sm)
print("\n".join(pages))
