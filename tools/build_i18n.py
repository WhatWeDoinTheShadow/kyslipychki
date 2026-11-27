#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Будує /en/index.html і /fr/index.html з української головної (index.html) + лого для мов.
Запуск з кореня репо: python3 tools/build_i18n.py"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from i18n_home import T, META, SLUGS, BRAND, HELP, COUNTRIES, CURRENCIES, PRICES
from i18n_privacy import PRIVACY
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE = "https://kyslipychki.shop"
_font = TTFont(os.path.join(os.path.dirname(__file__), "fonts", "Caveat-Bold.ttf"))
_gs, _cmap, _upm = _font.getGlyphSet(), _font.getBestCmap(), _font["head"].unitsPerEm


def wordmark(text, x0=122, base=84, size=62, maxw=286):
    w = sum(_gs[_cmap[ord(c)]].width for c in text)
    k = min(size / _upm, maxw / w)
    pen, x = SVGPathPen(_gs), 0
    for c in text:
        g = _gs[_cmap[ord(c)]]
        g.draw(TransformPen(pen, (k, 0, 0, -k, x0 + x * k, base)))
        x += g.width
    return pen.getCommands()


def logos():
    """Лого з написом потрібною мовою: для інлайн-символу і файли для внутрішніх сторінок."""
    src = {n: open(os.path.join(ROOT, n)).read() for n in ("logo.svg", "logo-white.svg")}
    for lang, name in BRAND.items():
        d = wordmark(name)
        for n, s in src.items():
            s2 = re.sub(r'<path fill="(currentColor|#[0-9a-fA-F]+)" d="M1[0-9][0-9][^"]*"/>',
                        lambda m: f'<path fill="{m.group(1)}" d="{d}"/>', s, count=1)
            s2 = s2.replace("<title>Кислі пички</title>", f"<title>{name}</title>")
            assert s2 != s, "wordmark not replaced in " + n
            open(os.path.join(ROOT, "assets", n.replace("logo", f"logo-{lang}")), "w").write(s2)


def rep(s, a, b, lang):
    if a not in s:
        raise SystemExit(f"[{lang}] не знайдено в index.html: {a[:90]!r}")
    return s.replace(a, b)


def js_block(lang):
    L = {
        "en": dict(locale="en-GB", sizes=[("sq", "Square", "20×20 cm", ["One person, head and shoulders", "Stretched canvas"]),
                                          ("pt", "Portrait", "30×40 cm", ["The person plus funny details around them", "Stretched canvas"]),
                                          ("lg", "Large portrait", "50×70 cm", ["A whole scene with background", "Stretched canvas"])],
                   tech=["Oil", "Acrylic", "Pastel", "Artist's choice"], pick="Choose",
                   nameF="Your friend's name", nameM="Your name", forWho="For", gift="A friend, as a gift", self="For myself",
                   canvas="Canvas", technique="Technique", rush="Rush, 48 hours", photo="Photo", nophoto="not added yet",
                   ship="Delivery", shipV="Nova Post, quoted for your country",
                   miss="Please add: ", missP="photo", missN="name", missE="email", missA="country and address", missT="phone",
                   noapi="Orders are being set up. Please try again a little later.", sending="Sending…", submit="Order the portrait",
                   done="Order {id}, {tot} + shipping. Portrait of {name}. We'll email {email} with the shipping quote and payment details.",
                   errs=dict(missing_fields="Please check the name, email, phone and address.", missing_photo="Please add a photo.",
                             photo_too_big="The photo is too large, try another one or a screenshot.", too_fast="Your order has already been sent, please wait 30 seconds."),
                   neterr="Couldn't send. Check your connection and try again.", photoWord="photo", dropText="Click or drop a photo here",
                   curLabel="Currency"),
        "fr": dict(locale="fr-FR", sizes=[("sq", "Carré", "20×20 cm", ["Une personne, en buste", "Toile sur châssis"]),
                                          ("pt", "Portrait", "30×40 cm", ["La personne et des détails drôles autour", "Toile sur châssis"]),
                                          ("lg", "Grand portrait", "50×70 cm", ["Toute une scène avec décor", "Toile sur châssis"])],
                   tech=["Huile", "Acrylique", "Pastel", "Au choix de l'artiste"], pick="Choisir",
                   nameF="Prénom de votre ami", nameM="Votre prénom", forWho="Pour qui", gift="Un ami, en cadeau", self="Pour moi",
                   canvas="Toile", technique="Technique", rush="Express, 48 heures", photo="Photo", nophoto="pas encore ajoutée",
                   ship="Livraison", shipV="Nova Post, chiffrée pour votre pays",
                   miss="Merci d'ajouter : ", missP="la photo", missN="le prénom", missE="l'e-mail", missA="le pays et l'adresse", missT="le téléphone",
                   noapi="La prise de commande est en cours de configuration. Réessayez un peu plus tard.", sending="Envoi…", submit="Commander le portrait",
                   done="Commande {id}, {tot} + livraison. Portrait de {name}. Nous écrivons à {email} avec le prix de la livraison et le paiement.",
                   errs=dict(missing_fields="Vérifiez le prénom, l'e-mail, le téléphone et l'adresse.", missing_photo="Ajoutez une photo.",
                             photo_too_big="La photo est trop lourde, essayez-en une autre ou une capture d'écran.", too_fast="Commande déjà envoyée, patientez 30 secondes."),
                   neterr="Envoi impossible. Vérifiez votre connexion et réessayez.", photoWord="photo", dropText="Cliquez ou déposez une photo ici",
                   curLabel="Devise"),
    }[lang]
    S = [{"id": i, "n": n, "sz": sz, "f": f} for i, n, sz, f in L["sizes"]]
    curs = CURRENCIES[lang]
    js = f"""<script>
{{
const LANG='{lang}',LOCALE='{L['locale']}';
const PR={json.dumps({c: PRICES[c] for c in curs})};
const CURS={json.dumps(curs)};
let CUR=CURS[0];
try{{const saved=localStorage.getItem('kp_cur');if(saved&&CURS.includes(saved))CUR=saved;else if(CURS.length>1){{const l=(navigator.language||'').toLowerCase(),tz=(Intl.DateTimeFormat().resolvedOptions().timeZone||'');
  if(l.endsWith('-gb')||tz==='Europe/London')CUR='GBP';else if(tz.startsWith('Europe/')||/-(ie|de|fr|nl|es|it|at|be|fi|pt)$/.test(l))CUR='EUR';else CUR='USD';}}}}catch(e){{}}
const S={json.dumps(S, ensure_ascii=False)};
const T={json.dumps(L['tech'], ensure_ascii=False)};
const L={json.dumps({k: L[k] for k in ('pick','nameF','nameM','forWho','gift','self','canvas','technique','rush','photo','nophoto','ship','shipV','miss','missP','missN','missE','missA','missT','noapi','sending','submit','done','neterr','photoWord','dropText','curLabel')}, ensure_ascii=False)};
const ERR={json.dumps(L['errs'], ensure_ascii=False)};
const $=id=>document.getElementById(id);
const fmt=n=>new Intl.NumberFormat(LOCALE,{{style:'currency',currency:CUR,maximumFractionDigits:0}}).format(n);
const price=id=>PR[CUR][id];
function paintPrices(){{
  const chk=(document.querySelector('input[name=style]:checked')||{{}}).value||'pt';
  $('styles').innerHTML=S.map(s=>`<label class="opt"><input type="radio" name="style" value="${{s.id}}" ${{s.id==chk?'checked':''}}><b>${{s.n}}</b><small>${{s.sz}}</small><br><span class="price">${{fmt(price(s.id))}}</span></label>`).join('');
  $('priceCards').innerHTML=S.map(s=>`<div class="card"><h3>${{s.n}}, ${{s.sz}}</h3><div class="tag">${{fmt(price(s.id))}}</div><ul>${{s.f.map(x=>`<li>${{x}}</li>`).join('')}}</ul><a class="btn ghost" href="#order" data-s="${{s.id}}">${{L.pick}}</a></div>`).join('');
  document.querySelectorAll('.rushp').forEach(e=>e.textContent='+'+fmt(price('rush')));
  document.querySelectorAll('[data-s]').forEach(a=>a.addEventListener('click',()=>{{const i=f.querySelector(`input[name=style][value=${{a.dataset.s}}]`);if(i){{i.checked=true;render();}}}}));
  document.querySelectorAll('.cursw button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.c===CUR));
}}
if(CURS.length>1)document.querySelectorAll('.cursw').forEach(w=>{{w.innerHTML=`<span>${{L.curLabel}}:</span>`+CURS.map(c=>`<button type="button" data-c="${{c}}">${{c}}</button>`).join('');
  w.addEventListener('click',e=>{{const c=e.target.dataset&&e.target.dataset.c;if(!c)return;CUR=c;try{{localStorage.setItem('kp_cur',c)}}catch(x){{}}paintPrices();render();}});}});
$('tech').innerHTML=T.map((t,i)=>`<label class="opt"><input type="radio" name="tech" value="${{t}}" ${{i==3?'checked':''}}><b>${{t}}</b></label>`).join('');

let photoName='',photoFile=null;
let src={{}};try{{src=JSON.parse(sessionStorage.getItem('kp_src')||'null')}}catch(e){{}}
if(!src){{const q=new URLSearchParams(location.search);src={{utm_source:q.get('utm_source')||'',utm_medium:q.get('utm_medium')||'',utm_campaign:q.get('utm_campaign')||'',referrer:document.referrer||'',landing:location.pathname+location.search}};try{{sessionStorage.setItem('kp_src',JSON.stringify(src))}}catch(e){{}}}}
const f=$('f');
const val=n=>(f.querySelector(`input[name=${{n}}]:checked`)||{{}}).value;
function render(){{
  const who=val('who'),st=S.find(s=>s.id==val('style'))||S[1];
  const gift=who=='friend';
  $('nameL').textContent=gift?L.nameF:L.nameM;
  const rows=[[L.forWho,gift?L.gift:L.self],[L.canvas,st.n+' '+st.sz,price(st.id)],[L.technique,val('tech')]];
  if($('rush').checked)rows.push([L.rush,'',price('rush')]);
  rows.push([L.photo,photoName||L.nophoto],[L.ship,L.shipV]);
  const tot=rows.reduce((a,r)=>a+(r[2]||0),0);
  const esc=t=>String(t).replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));
  $('sumList').innerHTML=rows.map(r=>`<dt>${{esc(r[0])}}${{r[2]&&r[1]?': '+esc(r[1]):''}}</dt><dd>${{r[2]?fmt(r[2]):esc(r[1])}}</dd>`).join('');
  $('tot').textContent=fmt(tot);
  return tot;
}}
f.addEventListener('input',render);
f.addEventListener('change',render);
paintPrices();

function setFile(file){{
  if(!file||!file.type.startsWith('image/'))return;
  photoName=file.name;photoFile=file;
  $('fname').textContent=file.name;
  const r=new FileReader();
  r.onload=()=>{{const t=$('thumb');t.style.backgroundImage=`url("${{r.result}}")`;t.textContent='';}};
  r.readAsDataURL(file);
  render();
}}
$('photo').addEventListener('change',e=>setFile(e.target.files[0]));
const d=$('drop');
['dragenter','dragover'].forEach(ev=>d.addEventListener(ev,e=>{{e.preventDefault();d.classList.add('over')}}));
['dragleave','drop'].forEach(ev=>d.addEventListener(ev,e=>{{e.preventDefault();d.classList.remove('over')}}));
d.addEventListener('drop',e=>setFile(e.dataTransfer.files[0]));

function toB64(blob){{return new Promise((ok,no)=>{{const r=new FileReader();r.onload=()=>ok(String(r.result).split(',')[1]);r.onerror=no;r.readAsDataURL(blob);}});}}
async function packPhoto(file){{
  try{{
    const img=await new Promise((ok,no)=>{{const u=URL.createObjectURL(file),im=new Image();im.onload=()=>ok(im);im.onerror=no;im.src=u;}});
    const k=Math.min(1,1600/Math.max(img.naturalWidth,img.naturalHeight));
    const c=document.createElement('canvas');c.width=Math.round(img.naturalWidth*k);c.height=Math.round(img.naturalHeight*k);
    c.getContext('2d').drawImage(img,0,0,c.width,c.height);
    const blob=await new Promise(ok=>c.toBlob(ok,'image/jpeg',.86));
    if(blob)return{{name:file.name.replace(/\\.[^.]+$/,'')+'.jpg',type:'image/jpeg',data:await toB64(blob)}};
  }}catch(e){{}}
  if(file.size>8e6)throw new Error('photo_too_big');
  return{{name:file.name,type:file.type||'image/jpeg',data:await toB64(file)}};
}}
f.addEventListener('submit',async e=>{{
  e.preventDefault();
  const miss=[];
  if(!photoFile)miss.push(L.missP);
  if(!$('name').value.trim())miss.push(L.missN);
  if(!/^\\S+@\\S+\\.\\S+$/.test($('contact').value.trim()))miss.push(L.missE);
  if(!$('country').value||!$('city').value.trim())miss.push(L.missA);
  if($('phone').value.replace(/\\D/g,'').length<7)miss.push(L.missT);
  if(miss.length){{$('err').textContent=L.miss+miss.join(', ')+'.';return;}}
  const api=window.KP_API;
  if(!api){{$('err').textContent=L.noapi;return;}}
  $('err').textContent='';
  const btn=f.querySelector('button[type=submit]');btn.disabled=true;btn.textContent=L.sending;
  try{{
    const payload={{action:'order',lang:LANG,currency:CUR,who:val('who'),size:val('style'),tech:val('tech'),rush:$('rush').checked,
      name:$('name').value.trim(),email:$('contact').value.trim(),phone:$('phone').value.trim(),country:$('country').value,city:$('city').value.trim(),
      about:$('about').value.trim(),photo:await packPhoto(photoFile),device:navigator.userAgent.slice(0,200),...src}};
    const res=await fetch(api,{{method:'POST',body:JSON.stringify(payload)}});
    const out=await res.json();
    if(!out.ok)throw new Error(out.error||'fail');
    $('doneText').textContent=L.done.replace('{{id}}',out.id).replace('{{tot}}',fmt(out.total)).replace('{{name}}',payload.name).replace('{{email}}',payload.email);
    try{{gtag('event','generate_lead',{{currency:CUR,value:out.total,size:payload.size,rush:!!payload.rush,who:payload.who,language:LANG}});}}catch(e){{}}
    f.hidden=true;$('done').hidden=false;
    $('done').scrollIntoView({{behavior:'smooth',block:'start'}});
  }}catch(err){{
    $('err').textContent=ERR[err.message]||L.neterr;
  }}finally{{btn.disabled=false;btn.textContent=L.submit;}}
}});
$('again').addEventListener('click',()=>{{f.reset();photoName='';photoFile=null;$('thumb').style.backgroundImage='';$('thumb').textContent=L.photoWord;$('fname').textContent=L.dropText;f.hidden=false;$('done').hidden=true;paintPrices();render();}});
render();
const mq=matchMedia('(min-width:900px)');
const faqs=[...document.querySelectorAll('.faqs details')];
function faqMode(){{if(mq.matches)faqs.forEach(d=>d.open=true);}}
faqMode();mq.addEventListener('change',faqMode);
faqs.forEach(d=>d.addEventListener('toggle',()=>{{if(mq.matches&&!d.open)d.open=true;}}));
const pp=$('pp');
function route(){{const on=location.hash==='#privacy';pp.classList.toggle('on',on);document.body.style.overflow=on?'hidden':'';if(on)pp.scrollTop=0;}}
window.addEventListener('hashchange',route);route();
pp.addEventListener('click',e=>{{if(e.target===pp)location.hash='top';}});
document.addEventListener('keydown',e=>{{if(e.key==='Escape'&&pp.classList.contains('on'))location.hash='top';}});
}}
"""
    return js


def address_row(lang):
    if lang == "en":
        lab = ("Country", "Choose a country", "Full delivery address", "Street, house, apartment, city, postcode",
               "Recipient's phone", "+1 555 123 4567")
    else:
        lab = ("Pays", "Choisissez un pays", "Adresse de livraison complète", "Rue, numéro, appartement, ville, code postal",
               "Téléphone du destinataire", "+33 6 12 34 56 78")
    opts = "".join(f'<option>{c}</option>' for c in COUNTRIES[lang])
    return (f'<div class="row2">\n          <div><label class="t" for="country">{lab[0]}</label><select id="country"><option value="">{lab[1]}</option>{opts}</select></div>\n'
            f'          <div><label class="t" for="phone">{lab[4]}</label><input type="text" id="phone" inputmode="tel" placeholder="{lab[5]}"></div>\n        </div>\n'
            f'        <div><label class="t" for="city">{lab[2]}</label><input type="text" id="city" autocomplete="street-address" placeholder="{lab[3]}"></div>')


def ld(lang, faq_pairs):
    m, brand = META[lang], BRAND[lang]
    url = f"{SITE}/{lang}/"
    cur = CURRENCIES[lang][0]
    offers = [{"@type": "AggregateOffer", "priceCurrency": c, "lowPrice": PRICES[c]["sq"], "highPrice": PRICES[c]["lg"],
               "offerCount": 3, "availability": "https://schema.org/InStock"} for c in CURRENCIES[lang]]
    menu = {"en": [("#idea", "Idea"), ("#how", "How it works"), ("#prices", "Prices"), ("#faq", "FAQ")],
            "fr": [("#idea", "L'idée"), ("#how", "Comment ça marche"), ("#prices", "Prix"), ("#faq", "Questions")]}[lang]
    pages = [(SLUGS[lang][k], k) for k in ("/portret-po-foto/", "/sharzh-po-foto/", "/blog/")]
    return {"@context": "https://schema.org", "@graph": [
        {"@type": "Organization", "@id": SITE + "/#org", "name": brand, "alternateName": ["Кислі пички", "Kysli Pychky"],
         "url": url, "logo": f"{SITE}/assets/logo-{lang}.svg", "email": "kyslipychki@gmail.com",
         "contactPoint": {"@type": "ContactPoint", "contactType": "customer support", "email": "kyslipychki@gmail.com", "availableLanguage": ["uk", "en", "fr"]}},
        {"@type": "WebSite", "@id": url + "#site", "url": url, "name": brand, "inLanguage": lang, "publisher": {"@id": SITE + "/#org"}},
        {"@type": "WebPage", "@id": url, "url": url, "name": m["title"], "description": m["desc"], "inLanguage": lang,
         "primaryImageOfPage": {"@type": "ImageObject", "url": f"{SITE}/og-{lang}.jpg", "width": 1200, "height": 630}},
        {"@type": "Product", "name": m["og_title"].split(" — ")[0], "description": m["desc"], "image": [f"{SITE}/og-{lang}.jpg", SITE + "/after.jpg"],
         "brand": {"@type": "Brand", "name": brand}, "url": url, "offers": offers if len(offers) > 1 else offers[0]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq_pairs]},
        {"@type": "SiteNavigationElement", "name": [n for _, n in menu], "url": [url + h for h, _ in menu]},
    ]}


def build(lang):
    s = open(os.path.join(ROOT, "index.html")).read()
    m = META[lang]
    s = s.replace('<html lang="uk">', f'<html lang="{lang}">', 1)
    s = re.sub(r"<title>.*?</title>", f"<title>{m['title']}</title>", s, count=1)
    s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{m["desc"]}">', s, count=1)
    s = s.replace('<link rel="canonical" href="https://kyslipychki.shop/">', f'<link rel="canonical" href="{SITE}/{lang}/">', 1)
    s = s.replace('<meta property="og:locale" content="uk_UA">', f'<meta property="og:locale" content="{m["locale"]}">', 1)
    s = s.replace('<meta property="og:site_name" content="Кислі пички">', f'<meta property="og:site_name" content="{BRAND[lang]}">', 1)
    s = s.replace('<meta property="og:url" content="https://kyslipychki.shop/">', f'<meta property="og:url" content="{SITE}/{lang}/">', 1)
    s = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{m["og_title"]}">', s, count=1)
    s = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{m["og_desc"]}">', s, count=1)
    s = re.sub(r'<meta property="og:image:alt" content="[^"]*">', f'<meta property="og:image:alt" content="{m["og_alt"]}">', s, count=1)
    s = s.replace(f'content="{SITE}/og.jpg"', f'content="{SITE}/og-{lang}.jpg"')
    # лого в символі
    s = re.sub(r'(<symbol id="logo"[\s\S]*?)<path fill="currentColor" d="M1[^"]*"/>', lambda mm: mm.group(1) + f'<path fill="currentColor" d="{wordmark(BRAND[lang])}"/>', s, count=1)
    # тексти
    for a, b in sorted(T[lang], key=lambda p: -len(p[0])):
        s = rep(s, a, b, lang)
    # посилання на внутрішні сторінки
    for uk, loc in sorted(SLUGS[lang].items(), key=lambda kv: -len(kv[0])):
        if uk != "/":
            s = s.replace(f'href="{uk}"', f'href="{loc}"')
    # адреса замість відділення НП
    i = s.index('<div class="row2">\n          <div><label class="t" for="city">')
    j = s.index("</div>\n        </div>", i) + len("</div>\n        </div>")
    s = s[:i] + address_row(lang) + s[j:]
    # термінове
    rush = {"en": "Rush, in 48 hours", "fr": "Express, en 48 heures"}[lang]
    s = rep(s, "Терміново, за 48 годин <svg", f"{rush} <svg", lang)
    s = rep(s, '<span class="price">+666 ₴</span></label>', '<span class="price rushp"></span></label>', lang)
    s = rep(s, '<span id="tot">0 ₴</span></div>', '<span id="tot"></span></div>\n        <div class="cursw" role="group"></div>', lang)
    s = rep(s, '<div class="prices" id="priceCards"></div>', '<div class="cursw" role="group"></div>\n    <div class="prices" id="priceCards"></div>', lang)
    s = s.replace('.cc{position:fixed;', '.cursw{display:flex;gap:6px;align-items:center;flex-wrap:wrap;font-size:14px;margin:10px 0}.cursw:empty{display:none}.cursw button{font:800 13px Nunito,sans-serif;padding:6px 10px;border-radius:999px;border:2px solid var(--ink);background:var(--paper);color:var(--ink);cursor:pointer}.cursw button[aria-pressed=true]{background:var(--ink);color:var(--bg)}\nselect{width:100%;font:inherit;color:inherit;background:var(--paper);border:2px solid var(--ink);border-radius:12px;padding:12px 14px;min-height:48px}\n.cc{position:fixed;', 1)
    # гаряча лінія
    i = s.index('<div class="help">')
    j = s.index("</div>\n  </div>\n</section>", i)
    s = s[:i] + HELP[lang] + s[j + len("</div>"):]
    # політика
    i = s.index('<div class="pptop">')
    j = s.index("</div>\n</div>", i)
    s = s[:i] + PRIVACY[lang] + s[j:]
    # головний скрипт
    i = s.index("<script>\n{\nconst S=[")
    j = s.index("}\n\n/* відгуки")
    s = s[:i] + js_block(lang) + s[j + 2:]
    # відгуки
    rv = {"en": ("{action:'reviews'}", "{action:'reviews',lang:'en'}", "`${avg.toFixed(1)} out of 5 · ${L.length} ${L.length===1?'review':'reviews'}`",
                 "Portrait by Sour Mugs at ", " out of 5", "'en-GB'"),
          "fr": ("{action:'reviews'}", "{action:'reviews',lang:'fr'}", "`${avg.toFixed(1).replace('.',',')} sur 5 · ${L.length} avis`",
                 "Portrait Mines Boudeuses chez ", " sur 5", "'fr-FR'")}[lang]
    s = rep(s, "JSON.stringify({action:'reviews'})", "JSON.stringify(" + rv[1] + ")", lang)
    s = re.sub(r"document\.getElementById\('rvsum'\)\.textContent=`.*?`;", "document.getElementById('rvsum').textContent=" + rv[2] + ";", s, count=1)
    s = rep(s, 'alt="Портрет від Кислих пичок у ${e(x.author)}"', f'alt="{rv[3]}${{e(x.author)}}"', lang)
    s = rep(s, 'aria-label="${x.rating} з 5"', f'aria-label="${{x.rating}}{rv[4]}"', lang)
    s = rep(s, "toLocaleDateString('uk-UA'", f"toLocaleDateString({rv[5]}", lang)
    # schema
    faq_pairs = [(re.sub(r"<[^>]+>", "", q), re.sub(r"<[^>]+>", "", a)) for q, a in
                 re.findall(r"<details[^>]*><summary>(.*?)</summary><p>(.*?)</p></details>", s)]
    i = s.index('<script type="application/ld+json">') + len('<script type="application/ld+json">')
    j = s.index("</script>", i)
    s = s[:i] + json.dumps(ld(lang, faq_pairs), ensure_ascii=False) + s[j:]
    # контроль: кирилиця не повинна лишитись поза перемикачем мов і alternateName
    left = re.findall(r"[А-ЩЬЮЯЄІЇҐа-щьюяєіїґ’']{3,}[^<>\"]{0,40}", re.sub(r"<script[\s\S]*?</script>", "", s))
    left = [x for x in left if "Українська" not in x and "Кислі пички" not in x]
    if left:
        print(f"[{lang}] УВАГА, лишився український текст:", left[:15])
    os.makedirs(os.path.join(ROOT, lang), exist_ok=True)
    open(os.path.join(ROOT, lang, "index.html"), "w").write(s)
    print("ok", lang)


if __name__ == "__main__":
    logos()
    for lang in ("en", "fr"):
        build(lang)
