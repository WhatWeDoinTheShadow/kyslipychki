# -*- coding: utf-8 -*-
"""Внутрішні сторінки й блог англійською і французькою. Викликається з build_pages.py."""

TODAY = "2026-11-27"


def build(lang, H):
    H.LANG = lang
    return EN(H) if lang == "en" else FR(H)


def _blog_ld(H, path, title, desc, crumbs):
    return [{"@type": "BlogPosting", "headline": title, "description": desc, "datePublished": TODAY, "dateModified": TODAY,
             "inLanguage": H.LANG, "mainEntityOfPage": H.SITE + path, "image": H.SITE + H.wide(path),
             "author": {"@type": "Organization", "name": H.BRAND[H.LANG], "url": H.SITE + H.HOME[H.LANG]},
             "publisher": {"@id": H.SITE + "/#org"}}, H.crumbs_ld(crumbs)]


# ======================================================================== EN
def EN(H):
    u, O, home = H.u, H.order_link(), "/en/"
    P, S, B1, B2, BL = u("/portret-po-foto/"), u("/sharzh-po-foto/"), u("/blog/shcho-podaruvaty-druhu-yakomu-vazhko/"), u("/blog/druk-chy-zhyvopys-portret-z-foto/"), u("/blog/")
    out = []

    faq = [("How much does a portrait from a photo cost?", "A 20×20 cm square is $55 / £42 / €49, a 30×40 cm portrait is $85 / £65 / €75 and a large 50×70 cm portrait is $129 / £99 / €115. The price depends only on the canvas size; the technique is included. Rush painting in 48 hours costs $22 / £16 / €19 extra. Shipping is quoted for your country."),
           ("Is it a print or really painted?", "Really painted. The artist paints the portrait on canvas by hand, with no printing, tablet or AI. You can see the brushstrokes and the texture of the paint."),
           ("What photo do I need?", "A regular phone photo where you can see the face and the emotion: a selfie, a video-call screenshot, a shot from under the blanket. It doesn't need to be perfect."),
           ("How long does it take?", "Usually 3–5 days to paint, or 48 hours with rush. Shipping from Ukraine adds about 5–10 days to Europe and the UK and 10–14 days to the USA, Canada and further."),
           ("Do you ship to my country?", "We ship worldwide with Nova Post and its partners. After you order, we email you the exact shipping cost for your address before you pay. Import VAT or duties may apply depending on your country.")]
    body = f"""<header class="hero band"><div class="wrap grid">
  <div>
    {H.crumbs_html([("Home", home), ("Portrait from photo", P)])}
    <h1>Custom portrait from a photo, hand-painted on canvas</h1>
    <p class="lead">Send us a photo and an artist paints the portrait with real paint on a stretched canvas. By hand, not by printer. From $55 / £42 / €49, shipped worldwide.</p>
    <div class="ctas"><a class="btn" href="{O}">Order a portrait</a><a class="btn ghost" href="#prices">Prices</a></div>
  </div>
  <figure><img src="/after.jpg" alt="A portrait from a photo, painted on canvas" width="900" height="1261"><figcaption>painted by hand</figcaption></figure>
</div></header>
<main class="band"><article class="narrow">
  <h2>How our portrait differs from a "photo on canvas"</h2>
  <p>Most "portrait from photo on canvas" offers are actually prints: the photo is edited and printed onto fabric. We do it differently. The artist looks at your photo and paints the picture from scratch, stroke by stroke. Every portrait is one of a kind, and you can see the living texture of the paint. We explain the difference in detail in <a href="{B2}">"Canvas print vs hand-painted portrait"</a>.</p>
  <p>One more thing: we don't paint formal portraits, we paint warm and slightly funny ones. A sad photo becomes a painting where the situation is funny: a personal rain cloud, a mountain of dishes, a cat sitting on their head. We never joke about appearance. See how it works on our home page: <a href="{home}">a sad photo turns into a funny portrait on canvas</a>.</p>

  <h2 id="prices">Prices for a portrait from a photo</h2>
  {H.price_cards()}

  <h2>How to order a portrait from a photo</h2>
  <ol>
    <li><b>Upload the photo</b> in the order form and write a few words about the person: what they love, what's weighing on them, what is off-limits.</li>
    <li><b>Choose the size and technique.</b> The price depends only on the size.</li>
    <li><b>The artist paints</b> for 3–5 days, or 48 hours with rush.</li>
    <li><b>We email you the shipping quote</b>, you pay, and the painting travels to you on its stretcher, ready to hang.</li>
  </ol>
  {H.cta()}

  <h2>What photo works</h2>
  <p>Any photo where the face and the mood are visible. No studio shoot needed: a selfie on the bus, a video-call screenshot or a photo from under the blanket often work even better because they carry emotion. If the photo is very dark or blurry, we'll write and ask for another one.</p>

  <h2>A portrait as a gift</h2>
  <p>Want more humour? Have a look at our <a href="{S}">caricature from a photo</a>: funnier scenes around the person.</p>
  <p>Most people order a portrait as a gift for a friend who's going through a hard time. The painting is delivered to you, not to the person in it, so you decide when and how to give it. We collected ideas on how to do it gently in <a href="{B1}">"Gifts for a friend going through a hard time"</a>.</p>

  <h2>Questions about portraits from photos</h2>
  {H.faq_html(faq)}
</article></main>
{H.more_links(P)}"""
    out.append(H.page(P, "Custom Portrait from Photo, Hand-Painted on Canvas — Sour Mugs",
                      "A portrait from your photo, painted by hand on canvas by a real artist, not printed. From $55 / £42 / €49, 3–5 days, shipped worldwide.",
                      body, [H.offer_ld("Custom portrait from a photo on canvas", "A portrait from a photo, hand-painted by an artist on canvas", P), H.faq_ld(faq),
                             H.crumbs_ld([("Home", home), ("Portrait from photo", P)])]))

    faq = [("How is your caricature different?", "A classic caricature exaggerates facial features. We exaggerate the situation: a personal cloud overhead, a mountain of to-dos, a blanket fortress. The person stays recognisable and lovely; the world around them is funny."),
           ("Is the caricature drawn on a tablet?", "No. Every caricature is painted by hand with real paint on a stretched canvas. No tablet, printing or AI."),
           ("How much does a caricature from a photo cost?", "From $55 / £42 / €49 for a 20×20 cm canvas, $85 / £65 / €75 for 30×40 cm and $129 / £99 / €115 for 50×70 cm. Rush in 48 hours: +$22 / £16 / €19. Shipping is quoted for your country."),
           ("What if they get offended?", "We paint with love and never joke about looks. In the form you can tell us which topics to avoid. Whether and when to give it is up to you: the painting is delivered to you."),
           ("Can I order one of myself?", "Of course. Sometimes the best thing to do with a bad day is to hang it on the wall and laugh at it.")]
    body = f"""<header class="hero band"><div class="wrap grid">
  <div>
    {H.crumbs_html([("Home", home), ("Caricature from photo", S)])}
    <h1>Caricature from a photo, hand-painted on canvas</h1>
    <p class="lead">A kind, funny caricature made from a sad photo. The artist paints it on real canvas: a gift that hangs on the wall, not a picture on a phone. From $55 / £42 / €49.</p>
    <div class="ctas"><a class="btn" href="{O}">Order a caricature</a><a class="btn ghost" href="#how">How it works</a></div>
  </div>
  <figure><img src="/before.jpg" alt="A sad selfie the caricature is painted from" width="720" height="899"><figcaption>feeling sad</figcaption></figure>
</div></header>
<main class="band"><article class="narrow">
  <h2>A caricature you laugh at together</h2>
  <p>A regular caricature enlarges the nose and ears. Ours enlarges the circumstances. If someone's week feels like an autumn storm, the painting gives them their own little rain cloud. If they're drowning in deadlines, they sit on a mountain of paperwork with a cup of coffee. The person stays themselves, and lovely; the situation becomes funny.</p>
  <p>That's why you can give this caricature even to someone who isn't feeling great. It doesn't say "cheer up", it says "I see how it is for you, and I'm here". You'll find before-and-after examples on the <a href="{home}">Sour Mugs home page</a>.</p>

  <h2 id="how">How we paint a caricature from a photo</h2>
  <ol>
    <li><b>You send a photo</b> and a few words: what's going on, what they love, what to avoid.</li>
    <li><b>The artist comes up with a scene</b> from those details and paints it on canvas in oil, acrylic or pastel.</li>
    <li><b>The painting is shipped</b> on its stretcher, ready to hang. Usually 3–5 days to paint, 48 hours with rush, plus delivery.</li>
  </ol>
  <figure style="margin:24px 0"><img src="/gift.jpg" alt="Pastel caricature on canvas: a girl and her mountain of depression" width="900" height="1200" loading="lazy" style="border:2px solid var(--ink);border-radius:12px;width:100%;max-width:420px"></figure>

  <h2>Caricature prices</h2>
  {H.price_cards()}
  {H.cta("Got a sad photo? Then the caricature is almost ready.")}

  <h2>Who gets this kind of caricature</h2>
  <ul>
    <li><b>A friend going through a hard time.</b> A gentle way to say "I'm here" without many words.</li>
    <li><b>A burnt-out colleague</b>, as a way to laugh with them, never at them.</li>
    <li><b>Yourself</b>, to hang a bad day on the wall and stop being afraid of it.</li>
  </ul>
  <p>Looking for something more classic? See our <a href="{P}">portrait from a photo</a>: the same painting on canvas, with a little less of a joke.</p>

  <h2>Questions about caricatures from photos</h2>
  {H.faq_html(faq)}
</article></main>
{H.more_links(S)}"""
    out.append(H.page(S, "Caricature from Photo, Hand-Painted on Canvas — a Gift | Sour Mugs",
                      "A kind caricature from your photo, painted by hand on canvas. The situation is funny, never their looks. From $55 / £42 / €49, shipped worldwide.",
                      body, [H.offer_ld("Caricature from a photo on canvas", "A caricature from a photo, hand-painted by an artist on canvas", S), H.faq_ld(faq),
                             H.crumbs_ld([("Home", home), ("Caricature from photo", S)])]))

    t1 = "Gifts for a friend going through a hard time: 9 no-pressure ideas"
    d1 = "How to support a friend with depression or a rough patch with a gift: 9 ideas, what not to give, and how to give it gently."
    body = f"""<main class="band"><article class="narrow">
  {H.crumbs_html([("Home", home), ("Blog", BL), ("Gifts for a friend going through a hard time", B1)])}
  <h1>{t1}</h1>
  <p class="meta">27 November 2026 · 6 min read</p>
  {H.hero_cover(B1)}
  <p>When a friend is struggling, you want to do something but don't know what. Words sound fake, "hang in there" doesn't help, and a big gesture can feel overwhelming. A gift works like a note without words: "I'm thinking of you, I expect nothing from you". The key is that it shouldn't demand energy they don't have right now.</p>
  <p>We're not therapists. This list is about care, not treatment. Depression is treated by professionals; a gift simply reminds someone they're not alone.</p>

  <h2>9 gift ideas for a friend who's having a hard time</h2>
  <h3>1. Food they don't have to cook</h3>
  <p>When energy runs out, proper meals are the first thing to go. A delivery of their favourite dish, soup in containers for a few days or a voucher for a café near home takes one daily task off their plate.</p>
  <h3>2. Help with chores</h3>
  <p>A paid cleaning session, laundry, or simply "I'll come over on Saturday and do the dishes". It sounds mundane, but for someone with depression a pile of dishes can feel like a real mountain.</p>
  <h3>3. Something soft and warm</h3>
  <p>A throw, warm socks, an oversized hoodie. Things you can wrap yourself in give a sense of safety without any effort.</p>
  <h3>4. A handwritten note or letter</h3>
  <p>A few honest sentences: what you value about your friend, which shared memory still makes you laugh. No "everything will be fine". People keep notes like that for years.</p>
  <h3>5. Time together, no obligations</h3>
  <p>"I'll be around on Sunday, we can watch a show or just sit in silence." Make sure they can say no without feeling guilty.</p>
  <h3>6. A houseplant that's hard to kill</h3>
  <p>A snake plant or a ZZ plant will survive a week without water. Something green and alive quietly brightens a room without becoming one more obligation.</p>
  <h3>7. An audiobook or podcast instead of a paper book</h3>
  <p>Reading is hard when concentration is low. Listening can be done lying down, with no effort at all.</p>
  <h3>8. A painting that makes them smile</h3>
  <p>We make gifts like this ourselves, so here's honestly why they work. An artist turns your friend's sad photo into a <a href="{S}">kind caricature painted on canvas</a>: the situation becomes funny, never the person. The painting stays on the wall and quietly reminds them that someone sees how it is and laughs with them, not at them. See what it looks like <a href="{home}">on our home page</a>.</p>
  <h3>9. A paid session with a professional, only if they want it</h3>
  <p>If your friend has said they'd like to see a therapist but keeps putting it off because of money, help with the cost can be the most valuable gift. Don't make it a surprise and don't push.</p>

  <h2>What not to give</h2>
  <ul>
    <li><b>"How to be happy" books</b> and motivational posters. They read like a reproach.</li>
    <li><b>A gym membership</b> with a hint that "you need to move more". One more obligation they won't keep and will blame themselves for.</li>
    <li><b>Big surprises and parties.</b> A crowd's attention can be exhausting.</li>
    <li><b>Alcohol.</b> It makes things worse and doesn't mix well with medication.</li>
  </ul>

  <h2>How to give it gently</h2>
  <ul>
    <li><b>No expectations.</b> Don't wait for a joyful reaction or a long thank you. A quiet "thanks" is already a lot.</li>
    <li><b>No conditions.</b> It's a gift, not a trade for "now pull yourself together".</li>
    <li><b>In private.</b> Not in front of everyone, so they can react however they can right now.</li>
    <li><b>And stay close afterwards.</b> A gift opens a conversation, it doesn't replace it.</li>
  </ul>
  {H.help_block()}
  {H.cta("Want to give your friend a painting nobody can look at without smiling?")}
</article></main>
{H.more_links(B1)}"""
    out.append(H.page(B1, t1 + " — Sour Mugs", d1, body, _blog_ld(H, B1, t1, d1, [("Home", home), ("Blog", BL), ("Gifts for a friend going through a hard time", B1)]), og_type="article"))

    t2 = "Portrait from a photo: canvas print vs hand-painted — what's the difference"
    d2 = "How a portrait painted by hand differs from a photo printed on canvas: price, look, timing, and how not to buy a print sold as a painting."
    body = f"""<main class="band"><article class="narrow">
  {H.crumbs_html([("Home", home), ("Blog", BL), ("Print vs painting", B2)])}
  <h1>{t2}</h1>
  <p class="meta">27 November 2026 · 5 min read</p>
  {H.hero_cover(B2)}
  <p>Search for a "portrait from photo on canvas" and you'll see hundreds of offers at very different prices. The reason is usually not greedy artists: two different products are sold under one name, <b>printing</b> and <b>painting</b>.</p>

  <h2>In short: how they differ</h2>
  <div class="scroll"><table class="tbl">
    <tr><th></th><th>Photo printed on canvas</th><th>Hand-painted portrait</th></tr>
    <tr><td><b>How it's made</b></td><td>The photo is edited and printed onto fabric</td><td>An artist paints the picture from scratch, looking at the photo</td></tr>
    <tr><td><b>Surface</b></td><td>Flat, like a photograph</td><td>Visible strokes, paint texture, brush marks</td></tr>
    <tr><td><b>Uniqueness</b></td><td>As many copies as you like</td><td>One single painting</td></tr>
    <tr><td><b>Time</b></td><td>Usually 1–2 days</td><td>Several days of an artist's work</td></tr>
    <tr><td><b>Price</b></td><td>Several times cheaper</td><td>More expensive: hours of handwork</td></tr>
    <tr><td><b>Can the scene change</b></td><td>Only filters and collage</td><td>Yes: add details, a joke, a new background</td></tr>
  </table></div>

  <h2>When to choose a print</h2>
  <p>A print is honest and useful when you want the photograph itself, large: a wedding photo for the wall, a landscape from a trip, a family picture for grandma. Fast, affordable, exactly like the photo.</p>

  <h2>When to choose a painting</h2>
  <p>A painting is for when the artist's view matters more than an exact copy: adding, exaggerating, joking, capturing a mood. Such a portrait is seen as art and a gift that lasts for years, not a photo in a frame. That's how we work at <a href="{home}">Sour Mugs</a>: a <a href="{P}">portrait from a photo</a> or a <a href="{S}">caricature from a photo</a> is painted by hand on canvas.</p>

  <h2>How not to buy a print sold as a painting</h2>
  <ul>
    <li><b>Look for "print", "giclée", "printed canvas" or "your photo on canvas"</b> in the description. That's almost always a printer.</li>
    <li><b>Ask for a photo of the process.</b> An artist can easily show a half-finished canvas or a palette.</li>
    <li><b>Zoom in on examples:</b> in a painting you can see strokes and uneven paint.</li>
    <li><b>Watch out for "oil painting effect".</b> Often it's a digital filter printed on canvas.</li>
    <li><b>Compare price and timing.</b> A large "oil painting" for the price of a takeaway, ready in a day, is unlikely to be painted by hand.</li>
  </ul>
  <p>A special case: a digital portrait drawn on a tablet. A person makes it, but the result is printed. It's a nice option if you want a stylised picture, not a painting.</p>
  {H.cta("Want a real painting, with brushstrokes and character?")}
</article></main>
{H.more_links(B2)}"""
    out.append(H.page(B2, "Canvas Print vs Hand-Painted Portrait: What's the Difference — Sour Mugs", d2, body,
                      _blog_ld(H, B2, t2, d2, [("Home", home), ("Blog", BL), ("Print vs painting", B2)]), og_type="article"))

    posts = [(B1, t1, d1), (B2, t2, d2)]
    cards = "".join(f'<a class="post" href="{p}"><img src="{H.cover(p)[0]}" alt="{H.cover(p)[1]}" width="600" height="450" loading="lazy"><h2>{t}</h2><p>{d}</p></a>' for p, t, d in posts)
    body = f"""<main class="band"><div class="wrap">
  {H.crumbs_html([("Home", home), ("Blog", BL)])}
  <h1>The Sour Mugs blog</h1>
  <p>About gifts for people going through a hard time, about painting, and about how a sad photo becomes a funny picture.</p>
  <div class="posts">{cards}</div>
</div></main>"""
    out.append(H.page(BL, "Blog: Gifts and Portraits from Photos — Sour Mugs",
                      "Sour Mugs articles: gifts for a friend going through a hard time, painting vs printing, how to order a portrait from a photo.",
                      body, [{"@type": "Blog", "name": "The Sour Mugs blog", "url": H.SITE + BL, "inLanguage": "en",
                              "blogPost": [{"@type": "BlogPosting", "headline": t, "url": H.SITE + p} for p, t, d in posts]},
                             H.crumbs_ld([("Home", home), ("Blog", BL)])]))
    return out


# ======================================================================== FR
def FR(H):
    u, O, home = H.u, H.order_link(), "/fr/"
    P, S, B1, B2, BL = u("/portret-po-foto/"), u("/sharzh-po-foto/"), u("/blog/shcho-podaruvaty-druhu-yakomu-vazhko/"), u("/blog/druk-chy-zhyvopys-portret-z-foto/"), u("/blog/")
    out = []

    faq = [("Combien coûte un portrait d'après photo ?", "49 € pour un carré de 20×20 cm, 75 € pour un portrait 30×40 cm et 115 € pour un grand portrait 50×70 cm. Le prix dépend uniquement de la taille de la toile, la technique est incluse. L'option express en 48 heures coûte 19 € de plus. La livraison est chiffrée pour votre pays."),
           ("C'est une impression ou c'est vraiment peint ?", "C'est vraiment peint. L'artiste peint le portrait sur toile à la main, sans impression, sans tablette et sans IA. On voit les coups de pinceau et la texture de la peinture."),
           ("Quelle photo faut-il ?", "Une simple photo de téléphone où l'on voit le visage et l'émotion : un selfie, une capture de visio, une photo sous la couette. Pas besoin qu'elle soit parfaite."),
           ("Quel est le délai ?", "En général 3 à 5 jours de peinture, ou 48 heures en express. La livraison depuis l'Ukraine ajoute environ 5 à 10 jours vers la France, la Belgique et la Suisse, et 10 à 14 jours vers le Canada."),
           ("Livrez-vous dans mon pays ?", "Nous livrons en France, en Belgique, en Suisse, au Canada et ailleurs avec Nova Post et ses partenaires. Après la commande, nous vous envoyons le coût exact de la livraison avant le paiement. Selon le pays, des frais de douane ou une TVA à l'import peuvent s'appliquer.")]
    body = f"""<header class="hero band"><div class="wrap grid">
  <div>
    {H.crumbs_html([("Accueil", home), ("Portrait d'après photo", P)])}
    <h1>Portrait sur mesure d'après photo, peint à la main sur toile</h1>
    <p class="lead">Envoyez une photo : un artiste peint le portrait avec de la vraie peinture sur une toile tendue sur châssis. À la main, pas à l'imprimante. Dès 49 €, livré chez vous.</p>
    <div class="ctas"><a class="btn" href="{O}">Commander un portrait</a><a class="btn ghost" href="#prices">Prix</a></div>
  </div>
  <figure><img src="/after.jpg" alt="Portrait d'après photo peint sur toile" width="900" height="1261"><figcaption>peint à la main</figcaption></figure>
</div></header>
<main class="band"><article class="narrow">
  <h2>En quoi notre portrait diffère d'une « photo sur toile »</h2>
  <p>La plupart des offres « portrait photo sur toile » sont en réalité des impressions : la photo est retouchée puis imprimée sur du tissu. Nous faisons autrement. L'artiste regarde votre photo et peint le tableau de zéro, touche après touche. Chaque portrait est unique et la texture vivante de la peinture se voit. Nous détaillons la différence dans <a href="{B2}">« Impression sur toile ou peinture »</a>.</p>
  <p>Autre différence : nous ne peignons pas de portraits solennels, mais des portraits tendres et un peu drôles. Une photo triste devient un tableau où c'est la situation qui est drôle : un petit nuage de pluie personnel, une montagne de vaisselle, un chat assis sur la tête. Jamais de moquerie sur le physique. Découvrez comment ça marche sur notre page d'accueil : <a href="{home}">une photo triste devient un portrait drôle sur toile</a>.</p>

  <h2 id="prices">Prix d'un portrait d'après photo</h2>
  {H.price_cards()}

  <h2>Comment commander un portrait d'après photo</h2>
  <ol>
    <li><b>Envoyez la photo</b> dans le formulaire et écrivez quelques mots sur la personne : ce qu'elle aime, ce qui lui pèse, les sujets à éviter.</li>
    <li><b>Choisissez la taille et la technique.</b> Le prix dépend uniquement de la taille.</li>
    <li><b>L'artiste peint</b> pendant 3 à 5 jours, ou 48 heures en express.</li>
    <li><b>Nous vous envoyons le prix de la livraison</b>, vous payez, et le tableau part sur son châssis, prêt à accrocher.</li>
  </ol>
  {H.cta()}

  <h2>Quelle photo convient</h2>
  <p>Toute photo où l'on voit le visage et l'humeur. Inutile de faire une séance photo : un selfie dans le bus, une capture de visio ou une photo sous la couette fonctionnent souvent mieux, car il y a de l'émotion. Si la photo est trop sombre ou floue, nous vous en demanderons une autre.</p>

  <h2>Un portrait à offrir</h2>
  <p>Envie de plus d'humour ? Découvrez notre <a href="{S}">caricature d'après photo</a> : des scènes plus drôles autour de la personne.</p>
  <p>Le plus souvent, on commande un portrait pour un ami qui traverse une période difficile. Le tableau vous est livré, à vous et non à la personne représentée : c'est vous qui décidez quand et comment l'offrir. Nos idées pour le faire avec délicatesse sont dans <a href="{B1}">« Quel cadeau pour un ami qui va mal »</a>.</p>

  <h2>Questions sur le portrait d'après photo</h2>
  {H.faq_html(faq)}
</article></main>
{H.more_links(P)}"""
    out.append(H.page(P, "Portrait d'après photo peint à la main sur toile — Mines Boudeuses",
                      "Un portrait d'après votre photo, peint à la main sur toile par un vrai artiste, pas imprimé. Dès 49 €, 3 à 5 jours, livraison en France, Belgique, Suisse et Canada.",
                      body, [H.offer_ld("Portrait sur mesure d'après photo sur toile", "Portrait d'après photo peint à la main sur toile", P), H.faq_ld(faq),
                             H.crumbs_ld([("Accueil", home), ("Portrait d'après photo", P)])]))

    faq = [("En quoi votre caricature est-elle différente ?", "Une caricature classique exagère les traits du visage. Nous exagérons la situation : un nuage personnel au-dessus de la tête, une montagne de choses à faire, une forteresse de couettes. La personne reste reconnaissable et belle, c'est le monde autour d'elle qui est drôle."),
           ("La caricature est-elle dessinée sur tablette ?", "Non. Chaque caricature est peinte à la main avec de la vraie peinture sur une toile tendue sur châssis. Ni tablette, ni impression, ni IA."),
           ("Combien coûte une caricature d'après photo ?", "49 € pour une toile de 20×20 cm, 75 € pour 30×40 cm et 115 € pour 50×70 cm. Express en 48 heures : +19 €. La livraison est chiffrée pour votre pays."),
           ("Et si la personne se vexe ?", "Nous peignons avec tendresse et ne plaisantons jamais sur le physique. Dans le formulaire, indiquez les sujets à éviter. Offrir ou non, et quand, c'est vous qui décidez : le tableau vous est livré."),
           ("Puis-je en commander une de moi ?", "Bien sûr. Parfois, le mieux à faire d'une mauvaise journée, c'est de l'accrocher au mur et d'en rire.")]
    body = f"""<header class="hero band"><div class="wrap grid">
  <div>
    {H.crumbs_html([("Accueil", home), ("Caricature d'après photo", S)])}
    <h1>Caricature d'après photo, peinte à la main sur toile</h1>
    <p class="lead">Une caricature tendre et drôle à partir d'une photo triste. L'artiste la peint sur une vraie toile : un cadeau qu'on accroche au mur, pas une image dans le téléphone. Dès 49 €.</p>
    <div class="ctas"><a class="btn" href="{O}">Commander une caricature</a><a class="btn ghost" href="#how">Comment ça marche</a></div>
  </div>
  <figure><img src="/before.jpg" alt="Le selfie triste d'après lequel la caricature est peinte" width="720" height="899"><figcaption>coup de blues</figcaption></figure>
</div></header>
<main class="band"><article class="narrow">
  <h2>Une caricature dont on rit ensemble</h2>
  <p>Une caricature classique grossit le nez et les oreilles. La nôtre grossit les circonstances. Si la semaine de la personne ressemble à une averse d'automne, elle aura sur le tableau son propre petit nuage. Si elle croule sous les échéances, elle sera assise sur une montagne de dossiers, un café à la main. La personne reste elle-même, et belle ; c'est la situation qui devient drôle.</p>
  <p>C'est pourquoi on peut offrir cette caricature même à quelqu'un qui n'a pas le moral. Elle ne dit pas « reprends-toi », elle dit « je vois ce que tu vis, et je suis là ». Des exemples avant/après sont sur la <a href="{home}">page d'accueil de Mines Boudeuses</a>.</p>

  <h2 id="how">Comment nous peignons une caricature d'après photo</h2>
  <ol>
    <li><b>Vous envoyez une photo</b> et quelques mots : ce qui se passe, ce que la personne aime, ce qu'il faut éviter.</li>
    <li><b>L'artiste imagine une scène</b> à partir de ces détails et la peint sur toile, à l'huile, à l'acrylique ou au pastel.</li>
    <li><b>Le tableau est expédié</b> sur son châssis, prêt à accrocher. En général 3 à 5 jours de peinture, 48 heures en express, plus la livraison.</li>
  </ol>
  <figure style="margin:24px 0"><img src="/gift.jpg" alt="Caricature au pastel sur toile : une jeune femme et sa montagne de déprime" width="900" height="1200" loading="lazy" style="border:2px solid var(--ink);border-radius:12px;width:100%;max-width:420px"></figure>

  <h2>Prix d'une caricature</h2>
  {H.price_cards()}
  {H.cta("Vous avez une photo triste ? La caricature est presque prête.")}

  <h2>À qui offrir ce genre de caricature</h2>
  <ul>
    <li><b>Un ami qui traverse une période difficile.</b> Une façon douce de dire « je suis là » sans grands mots.</li>
    <li><b>Un collègue épuisé</b>, pour rire avec lui, jamais de lui.</li>
    <li><b>Vous-même</b>, pour accrocher une mauvaise journée au mur et ne plus en avoir peur.</li>
  </ul>
  <p>Vous cherchez quelque chose de plus classique ? Découvrez notre <a href="{P}">portrait d'après photo</a> : la même peinture sur toile, avec un peu moins d'humour.</p>

  <h2>Questions sur la caricature d'après photo</h2>
  {H.faq_html(faq)}
</article></main>
{H.more_links(S)}"""
    out.append(H.page(S, "Caricature d'après photo peinte sur toile, idée cadeau — Mines Boudeuses",
                      "Une caricature tendre d'après votre photo, peinte à la main sur toile. C'est la situation qui est drôle, jamais le physique. Dès 49 €, livrée en France, Belgique, Suisse et Canada.",
                      body, [H.offer_ld("Caricature d'après photo sur toile", "Caricature d'après photo peinte à la main sur toile", S), H.faq_ld(faq),
                             H.crumbs_ld([("Accueil", home), ("Caricature d'après photo", S)])]))

    t1 = "Quel cadeau pour un ami qui traverse une période difficile : 9 idées sans pression"
    d1 = "Comment soutenir par un cadeau un ami déprimé ou qui traverse un moment dur : 9 idées, ce qu'il vaut mieux éviter et comment offrir avec délicatesse."
    body = f"""<main class="band"><article class="narrow">
  {H.crumbs_html([("Accueil", home), ("Blog", BL), ("Cadeau pour un ami qui va mal", B1)])}
  <h1>{t1}</h1>
  <p class="meta">27 novembre 2026 · 6 min de lecture</p>
  {H.hero_cover(B1)}
  <p>Quand un ami va mal, on a envie de faire quelque chose sans savoir quoi. Les mots sonnent faux, « tiens bon » n'aide pas, et un grand geste peut intimider. Un cadeau agit comme un mot sans paroles : « je pense à toi, je n'attends rien de toi ». L'essentiel est qu'il ne demande pas une énergie que la personne n'a pas en ce moment.</p>
  <p>Nous ne sommes pas psychologues. Cette sélection parle d'attention, pas de traitement. La dépression se soigne avec des professionnels ; un cadeau rappelle seulement à la personne qu'elle n'est pas seule.</p>

  <h2>9 idées de cadeau pour un ami qui va mal</h2>
  <h3>1. Des repas à ne pas cuisiner</h3>
  <p>Quand l'énergie manque, les vrais repas disparaissent en premier. La livraison de son plat préféré, de la soupe en boîtes pour quelques jours ou un bon dans un café près de chez elle retirent une tâche quotidienne.</p>
  <h3>2. Un coup de main à la maison</h3>
  <p>Un ménage payé, une lessive, ou simplement « je passe samedi faire la vaisselle ». Ça paraît banal, mais pour une personne déprimée, une pile de vaisselle peut être une vraie montagne.</p>
  <h3>3. Quelque chose de doux et chaud</h3>
  <p>Un plaid, des chaussettes chaudes, un sweat trop grand. Des choses dans lesquelles s'emmitoufler donnent un sentiment de sécurité sans le moindre effort.</p>
  <h3>4. Un mot ou une lettre écrits à la main</h3>
  <p>Quelques phrases sincères : ce que vous appréciez chez votre ami, quel souvenir commun vous fait encore rire. Sans « tout ira bien ». Ces mots-là, on les garde des années.</p>
  <h3>5. Du temps ensemble, sans obligation</h3>
  <p>« Je serai là dimanche, on peut regarder une série ou juste se taire. » Laissez la possibilité de refuser sans culpabilité.</p>
  <h3>6. Une plante d'intérieur increvable</h3>
  <p>Une sansevière ou un zamioculcas survivent à une semaine sans arrosage. Du vert vivant réjouit en silence sans devenir une obligation de plus.</p>
  <h3>7. Un livre audio ou un podcast plutôt qu'un livre papier</h3>
  <p>Lire est difficile quand on n'arrive pas à se concentrer. Écouter se fait allongé, sans effort.</p>
  <h3>8. Un tableau qui fait sourire</h3>
  <p>Nous faisons nous-mêmes ce genre de cadeau, alors disons honnêtement pourquoi il fonctionne. Un artiste transforme la photo triste de votre ami en <a href="{S}">caricature tendre peinte sur toile</a> : c'est la situation qui devient drôle, jamais la personne. Le tableau reste au mur et rappelle doucement que quelqu'un voit ce qu'elle vit et rit avec elle, pas d'elle. Voyez à quoi ça ressemble <a href="{home}">sur notre page d'accueil</a>.</p>
  <h3>9. Une séance chez un professionnel, seulement si la personne le souhaite</h3>
  <p>Si votre ami a dit vouloir consulter mais repousse pour des raisons d'argent, l'aider à payer peut être le plus beau cadeau. Pas en surprise, et sans insister.</p>

  <h2>Ce qu'il vaut mieux éviter</h2>
  <ul>
    <li><b>Les livres « comment être heureux »</b> et les posters motivants. Ils sonnent comme un reproche.</li>
    <li><b>Un abonnement à la salle de sport</b> avec le sous-entendu « tu devrais bouger ». Une obligation de plus, qu'elle ne tiendra pas et se reprochera.</li>
    <li><b>Les grosses surprises et les fêtes.</b> L'attention d'un groupe peut épuiser.</li>
    <li><b>L'alcool.</b> Il aggrave l'état et se marie mal avec les traitements.</li>
  </ul>

  <h2>Comment offrir avec délicatesse</h2>
  <ul>
    <li><b>Sans attente.</b> N'espérez pas une réaction joyeuse ou de longs remerciements. Un petit « merci », c'est déjà beaucoup.</li>
    <li><b>Sans condition.</b> Un cadeau, pas un échange contre « maintenant ressaisis-toi ».</li>
    <li><b>En tête-à-tête.</b> Pas devant tout le monde, pour que la personne réagisse comme elle le peut.</li>
    <li><b>Et restez présent ensuite.</b> Un cadeau ouvre la conversation, il ne la remplace pas.</li>
  </ul>
  {H.help_block()}
  {H.cta("Envie d'offrir à votre ami un tableau qu'on ne peut pas regarder sans sourire ?")}
</article></main>
{H.more_links(B1)}"""
    out.append(H.page(B1, "Quel cadeau pour un ami qui va mal : 9 idées sans pression — Mines Boudeuses", d1, body,
                      _blog_ld(H, B1, t1, d1, [("Accueil", home), ("Blog", BL), ("Cadeau pour un ami qui va mal", B1)]), og_type="article"))

    t2 = "Portrait d'après photo : impression sur toile ou peinture à la main, quelle différence ?"
    d2 = "En quoi un portrait peint à la main diffère d'une photo imprimée sur toile : prix, rendu, délai, et comment ne pas acheter une impression vendue comme un tableau."
    body = f"""<main class="band"><article class="narrow">
  {H.crumbs_html([("Accueil", home), ("Blog", BL), ("Impression ou peinture", B2)])}
  <h1>{t2}</h1>
  <p class="meta">27 novembre 2026 · 5 min de lecture</p>
  {H.hero_cover(B2)}
  <p>Cherchez « portrait photo sur toile » et vous verrez des centaines d'offres à des prix très différents. La raison n'est généralement pas la cupidité des artistes : deux produits différents sont vendus sous le même nom, <b>l'impression</b> et <b>la peinture</b>.</p>

  <h2>En bref : les différences</h2>
  <div class="scroll"><table class="tbl">
    <tr><th></th><th>Photo imprimée sur toile</th><th>Portrait peint à la main</th></tr>
    <tr><td><b>Fabrication</b></td><td>La photo est retouchée puis imprimée sur du tissu</td><td>Un artiste peint le tableau de zéro en regardant la photo</td></tr>
    <tr><td><b>Surface</b></td><td>Lisse, comme une photographie</td><td>Coups de pinceau, relief et texture visibles</td></tr>
    <tr><td><b>Unicité</b></td><td>Autant de copies qu'on veut</td><td>Un seul et unique tableau</td></tr>
    <tr><td><b>Délai</b></td><td>En général 1 à 2 jours</td><td>Plusieurs jours de travail d'artiste</td></tr>
    <tr><td><b>Prix</b></td><td>Plusieurs fois moins cher</td><td>Plus cher : des heures de travail manuel</td></tr>
    <tr><td><b>Changer la scène</b></td><td>Seulement filtres et collage</td><td>Oui : ajouter des détails, une blague, un autre fond</td></tr>
  </table></div>

  <h2>Quand choisir l'impression</h2>
  <p>L'impression est honnête et utile quand on veut la photographie elle-même, en grand : une photo de mariage au mur, un paysage de voyage, une photo de famille pour mamie. Rapide, abordable, fidèle à la photo.</p>

  <h2>Quand choisir la peinture</h2>
  <p>La peinture s'impose quand le regard de l'artiste compte plus qu'une copie exacte : ajouter, exagérer, plaisanter, rendre une humeur. Un tel portrait est perçu comme une œuvre et un cadeau pour des années, pas comme une photo encadrée. C'est ainsi que nous travaillons chez <a href="{home}">Mines Boudeuses</a> : un <a href="{P}">portrait d'après photo</a> ou une <a href="{S}">caricature d'après photo</a> est peint à la main sur toile.</p>

  <h2>Comment ne pas acheter une impression vendue comme un tableau</h2>
  <ul>
    <li><b>Cherchez les mots « impression », « tirage », « giclée » ou « votre photo sur toile »</b> dans la description. C'est presque toujours une imprimante.</li>
    <li><b>Demandez une photo du travail en cours.</b> Un artiste peut facilement montrer une toile inachevée ou sa palette.</li>
    <li><b>Zoomez sur les exemples :</b> sur une peinture, on voit les coups de pinceau et les irrégularités.</li>
    <li><b>Méfiez-vous de « l'effet peinture à l'huile ».</b> C'est souvent un filtre numérique imprimé sur toile.</li>
    <li><b>Comparez prix et délai.</b> Une grande « peinture à l'huile » au prix d'un repas, prête en un jour, a peu de chances d'être peinte à la main.</li>
  </ul>
  <p>Cas particulier : le portrait numérique dessiné sur tablette. Une personne le réalise, mais le résultat est imprimé. C'est une bonne option si vous voulez une image stylisée, pas une peinture.</p>
  {H.cta("Vous voulez une vraie peinture, avec des coups de pinceau et du caractère ?")}
</article></main>
{H.more_links(B2)}"""
    out.append(H.page(B2, "Impression sur toile ou portrait peint : quelle différence — Mines Boudeuses", d2, body,
                      _blog_ld(H, B2, t2, d2, [("Accueil", home), ("Blog", BL), ("Impression ou peinture", B2)]), og_type="article"))

    posts = [(B1, t1, d1), (B2, t2, d2)]
    cards = "".join(f'<a class="post" href="{p}"><img src="{H.cover(p)[0]}" alt="{H.cover(p)[1]}" width="600" height="450" loading="lazy"><h2>{t}</h2><p>{d}</p></a>' for p, t, d in posts)
    body = f"""<main class="band"><div class="wrap">
  {H.crumbs_html([("Accueil", home), ("Blog", BL)])}
  <h1>Le blog de Mines Boudeuses</h1>
  <p>Des idées de cadeaux pour les personnes qui traversent un moment difficile, de la peinture, et comment une photo triste devient un tableau drôle.</p>
  <div class="posts">{cards}</div>
</div></main>"""
    out.append(H.page(BL, "Blog : cadeaux et portraits d'après photo — Mines Boudeuses",
                      "Les articles de Mines Boudeuses : quel cadeau pour un ami qui va mal, impression ou peinture, comment commander un portrait d'après photo.",
                      body, [{"@type": "Blog", "name": "Le blog de Mines Boudeuses", "url": H.SITE + BL, "inLanguage": "fr",
                              "blogPost": [{"@type": "BlogPosting", "headline": t, "url": H.SITE + p} for p, t, d in posts]},
                             H.crumbs_ld([("Accueil", home), ("Blog", BL)])]))
    return out
