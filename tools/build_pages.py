#!/usr/bin/env python3
"""Генерує внутрішні сторінки і блог для kyslipychki.shop. Запуск: python3 build_pages.py <repo>"""
import json, os, sys, html

REPO = sys.argv[1]
SITE = "https://kyslipychki.shop"
TODAY = "2026-11-26"
ORDER = "/#order"

PRICES = [("Квадрат", "20×20 см", 1700), ("Портрет", "30×40 см", 2666), ("Великий портрет", "50×70 см", 4111)]

GA = """<script async src="https://www.googletagmanager.com/gtm.js?id=GTM-NXWSKHWM"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());</script>"""

MENU = [("/", "Головна"), ("/#how", "Як це працює"), ("/#prices", "Ціни"), ("/portret-po-foto/", "Портрет по фото"),
        ("/sharzh-po-foto/", "Шарж по фото"), ("/blog/", "Блог"), ("/#faq", "Питання")]
MENU_LINKS = "".join(f'<a href="{u}">{t}</a>' for u, t in MENU)
NAV = f"""<nav aria-label="Головне меню">
  <a class="logo" href="/" aria-label="Кислі пички, на головну"><img src="/logo-white.svg" alt="Кислі пички" width="160" height="48"></a>
  <a class="l" href="/portret-po-foto/">Портрет по фото</a>
  <a class="l" href="/sharzh-po-foto/">Шарж по фото</a>
  <a class="l" href="/blog/">Блог</a>
  <a class="btn" href="/#order">Замовити</a>
  <button class="burger" type="button" aria-label="Меню" aria-expanded="false" aria-controls="menu"><span></span></button>
  <div class="menu" id="menu">{MENU_LINKS}</div>
</nav>
<script>(()=>{{const b=document.querySelector('.burger'),m=document.getElementById('menu');b.onclick=()=>{{const on=m.classList.toggle('on');b.setAttribute('aria-expanded',on);}};m.onclick=e=>{{if(e.target.tagName==='A'){{m.classList.remove('on');b.setAttribute('aria-expanded',false);}}}};}})();</script>"""
NAV_LD = {"@type": "SiteNavigationElement", "name": [t for _, t in MENU], "url": [SITE + u for u, _ in MENU]}

FOOTER = """<footer class="band">
  <div>
    <a class="logo" href="/" aria-label="Кислі пички"><img src="/logo-white.svg" alt="Кислі пички" width="186" height="56"></a>
    <span>Портрети фарбами на полотні для тих, кому зараз сумно.</span>
  </div>
  <div class="flinks">
    <a href="/portret-po-foto/">Портрет по фото</a>
    <a href="/sharzh-po-foto/">Шарж по фото</a>
    <a href="/blog/">Блог</a>
    <a href="/#privacy">Політика конфіденційності</a>
    <span>Сайт розроблено <a href="https://webrarium.com" target="_blank" rel="noopener">Webrarium</a></span>
  </div>
  <a class="btn" href="/#order">Замовити</a>
</footer>"""

HELP = """<div class="help">
  <b>Якщо людина говорить, що не хоче жити, спершу не подарунок, а розмова з тими, хто вміє допомагати.</b>
  Lifeline Ukraine, цілодобово і безкоштовно:
  <div class="num">7333</div>
  Можна подзвонити або написати на <a href="https://lifelineukraine.com">lifelineukraine.com</a>.
</div>"""


def price_cards(note=True):
    cards = "".join(
        f'<div class="card"><b>{n}</b><div class="p">{p:,} ₴</div><p>{sz}, полотно на підрамнику</p></div>'.replace(f"{p:,}", f"{p:,}".replace(",", " "))
        for n, sz, p in PRICES)
    tail = '<p class="meta">Терміново за 48 годин: +666 ₴. Доставка Новою поштою за тарифами перевізника.</p>' if note else ""
    return f'<div class="cards">{cards}</div>{tail}'


def cta(text="Надішли фото, художник намалює портрет фарбами на полотні."):
    return f'<div class="cta"><p>{text}</p><a class="btn" href="{ORDER}">Замовити портрет</a></div>'


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
            "image": [SITE + WIDE.get(url, "/og.jpg"), SITE + "/after.jpg"], "brand": {"@type": "Brand", "name": "Кислі пички"},
            "offers": {"@type": "AggregateOffer", "priceCurrency": "UAH", "lowPrice": 1700, "highPrice": 4111,
                       "offerCount": 3, "availability": "https://schema.org/InStock"}}


def page(path, title, desc, body, graph, og_type="website", image=None):
    url = SITE + path
    image = image or WIDE.get(path, "/og.jpg")
    graph = graph + [{"@type": "WebPage", "@id": url, "url": url, "name": title, "inLanguage": "uk",
                      "primaryImageOfPage": {"@type": "ImageObject", "url": SITE + image, "width": 1200, "height": 630},
                      "isPartOf": {"@type": "WebSite", "url": SITE + "/", "name": "Кислі пички"}}, NAV_LD]
    if path in COVERS or path == "/blog/":
        graph.append(cards_ld(more_items(path) if path != "/blog/" else [c for c in CARDS if c[0].startswith("/blog/")],
                              "Читати далі" if path != "/blog/" else "Статті блогу"))
    org = {"@type": "Organization", "@id": SITE + "/#org", "name": "Кислі пички", "url": SITE + "/",
           "logo": SITE + "/logo.svg", "email": "kyslipychki@gmail.com"}
    ld = json.dumps({"@context": "https://schema.org", "@graph": [org] + graph}, ensure_ascii=False)
    doc = f"""<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#ffd23f">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="uk_UA">
<meta property="og:site_name" content="Кислі пички">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{SITE}{image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/admin/icon-192.png">
{GA}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Nunito:wght@400;600;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/page.css">
<script type="application/ld+json">{ld}</script>
</head>
<body>
{NAV}
{body}
{FOOTER}
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
CARDS = [("/", "Сумна фотка = смішний портрет", "Як ми перетворюємо сумне фото на теплу смішну картину фарбами."),
         ("/portret-po-foto/", "Портрет по фото на замовлення", "Живопис фарбами на полотні, від 1700 ₴, доставка по Україні."),
         ("/sharzh-po-foto/", "Шарж по фото на полотні", "Добрий шарж, де смішні обставини, а не зовнішність."),
         ("/blog/shcho-podaruvaty-druhu-yakomu-vazhko/", "Що подарувати другу, якому зараз важко", "9 ідей без тиску і як подарувати делікатно."),
         ("/blog/druk-chy-zhyvopys-portret-z-foto/", "Друк на полотні чи живопис", "У чому різниця і як не купити друк під виглядом картини.")]


def card(u, t, d):
    img, alt = COVERS[u]
    return (f'<a class="pcard" href="{u}"><img src="{img}" alt="{alt}" width="600" height="450" loading="lazy">'
            f'<span class="pc-t">{t}</span><span class="pc-d">{d}</span></a>')


def cards_ld(items, name):
    return {"@type": "ItemList", "name": name, "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": SITE + u, "name": t, "image": SITE + COVERS[u][0]}
        for i, (u, t, d) in enumerate(items)]}


def more_items(exclude):
    return [c for c in CARDS if c[0] != exclude]


def more_links(exclude):
    return ('<section class="band more"><div class="wrap"><h2>Читати далі</h2><div class="pcards">'
            + "".join(card(*c) for c in more_items(exclude)) + '</div></div></section>')


def hero_cover(u):
    return (f'<figure class="cover"><img src="{WIDE[u]}" alt="{COVERS[u][1]}" width="1200" height="630" fetchpriority="high"></figure>')


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
  {HELP}
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

# ---------- sitemap ----------
urls = ["/"] + pages
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n"
open(os.path.join(REPO, "sitemap.xml"), "w").write(sm)
print("\n".join(urls))
