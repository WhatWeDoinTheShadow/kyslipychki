/**
 * Кислі пички — бекенд замовлень на Google Apps Script.
 *
 * Як розгорнути:
 * 1. Окремий проєкт Apps Script в акаунті kyslipychki@gmail.com, вставити цей файл, вписати SPREADSHEET_ID.
 * 2. Запустити функцію setup() один раз і дати доступ. У журналі з'явиться пароль адмінки.
 * 3. Розгорнути → Нове розгортання → Веб-застосунок:
 *    «Виконувати як: я», «Хто має доступ: усі». Скопіювати URL у config.js сайту.
 */

const SPREADSHEET_ID = '1qnL1-woMteoMTsZ5aUOsnx0XI4X10zNlD_pM7Hp-7U4'; // таблиця «Кислі пички — замовлення» у kyslipychki@gmail.com
const SHEET_NAME = 'Замовлення';
const FOLDER_NAME = 'Кислі пички — фото замовлень';
const HEAD = ['id', 'created', 'status', 'who', 'name', 'size', 'sizeLabel', 'price', 'tech', 'rush', 'total',
  'about', 'email', 'phone', 'city', 'photoId', 'photoName',
  'utm_source', 'utm_medium', 'utm_campaign', 'referrer', 'landing', 'device', 'note', 'updated',
  'lang', 'currency', 'country'];

/** Ціни за валютами. UAH — Україна (Нова пошта), інші — міжнародні замовлення, доставка рахується окремо. */
const PRICES = {
  UAH: { sq: 1700, pt: 2666, lg: 4111, rush: 666 },
  EUR: { sq: 49, pt: 75, lg: 115, rush: 19 },
  GBP: { sq: 42, pt: 65, lg: 99, rush: 16 },
  USD: { sq: 55, pt: 85, lg: 129, rush: 22 }
};
const CUR_SIGN = { UAH: '₴', EUR: '€', GBP: '£', USD: '$' };
const LANGS = ['uk', 'en', 'fr'];
const SIZE_LABELS = {
  uk: { sq: 'Квадрат 20×20 см', pt: 'Портрет 30×40 см', lg: 'Великий портрет 50×70 см' },
  en: { sq: 'Square 20×20 cm', pt: 'Portrait 30×40 cm', lg: 'Large portrait 50×70 cm' },
  fr: { sq: 'Carré 20×20 cm', pt: 'Portrait 30×40 cm', lg: 'Grand portrait 50×70 cm' }
};
function money_(n, cur) {
  return cur === 'UAH' ? n + ' ₴' : (cur === 'EUR' ? n + ' €' : CUR_SIGN[cur] + n);
}
const STATUSES = ['new', 'paid', 'painting', 'shipped', 'done', 'cancelled'];
const MAX_PHOTO_BYTES = 8 * 1024 * 1024;
const SITE = 'https://kyslipychki.shop';
const REVIEW_SHEET = 'Відгуки';
const REVIEW_HEAD = ['id', 'created', 'orderId', 'status', 'rating', 'author', 'text', 'consent', 'photoId', 'email', 'updated', 'lang'];
const REVIEW_STATUSES = ['pending', 'published', 'hidden'];

/** Запустити один раз вручну з редактора. */
function setup() {
  const sh = sheet_();
  const props = PropertiesService.getScriptProperties();
  if (!props.getProperty('ADMIN_TOKEN')) {
    props.setProperty('ADMIN_TOKEN', Utilities.getUuid().replace(/-/g, '').slice(0, 20));
  }
  folder_();
  Logger.log('Таблиця: ' + sh.getParent().getUrl());
  Logger.log('Пароль адмінки: ' + props.getProperty('ADMIN_TOKEN'));
}

function doGet() {
  return json_({ ok: true, service: 'kyslipychki' });
}

function doPost(e) {
  try {
    const body = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    const action = body.action || 'order';
    if (action === 'order') return json_(createOrder_(body));
    if (action === 'reviewInfo') return json_(reviewInfo_(body));
    if (action === 'review') return json_(createReview_(body));
    if (action === 'reviews') return json_({ ok: true, reviews: publicReviews_(body.lang) });
    auth_(body.token);
    if (action === 'reviewsAdmin') return json_({ ok: true, reviews: allReviews_() });
    if (action === 'reviewStatus') return json_(updateReview_(body));
    if (action === 'reviewPhoto') return json_(getReviewPhoto_(body.id));
    if (action === 'sendReviewRequest') return json_(sendReviewRequest_(body.id, true));
    if (action === 'list') return json_({ ok: true, orders: listOrders_() });
    if (action === 'status') return json_(updateOrder_(body));
    if (action === 'photo') return json_(getPhoto_(body.id));
    return json_({ ok: false, error: 'unknown_action' });
  } catch (err) {
    return json_({ ok: false, error: String(err && err.message || err) });
  }
}

/* ---------- замовлення ---------- */

function createOrder_(b) {
  const lang = LANGS.indexOf(b.lang) >= 0 ? b.lang : 'uk';
  const currency = PRICES[b.currency] ? b.currency : 'UAH';
  const prices = PRICES[currency];
  if (!prices[b.size] || b.size === 'rush') throw new Error('bad_size');
  const intl = currency !== 'UAH';
  const name = clean_(b.name, 80);
  const email = clean_(b.email, 120);
  const phone = clean_(b.phone, 40);
  const city = clean_(b.city, 160);
  const country = clean_(b.country, 60);
  if (!name || !/^\S+@\S+\.\S+$/.test(email) || phone.replace(/\D/g, '').length < (intl ? 7 : 10) || !city || (intl && !country)) {
    throw new Error('missing_fields');
  }
  if (!b.photo || !b.photo.data) throw new Error('missing_photo');

  // простий захист від повторних відправок: не частіше разу на 30 секунд з одного email
  const cache = CacheService.getScriptCache();
  const key = 'o_' + Utilities.base64EncodeWebSafe(email).slice(0, 60);
  if (cache.get(key)) throw new Error('too_fast');
  cache.put(key, '1', 30);

  const bytes = Utilities.base64Decode(String(b.photo.data));
  if (bytes.length > MAX_PHOTO_BYTES) throw new Error('photo_too_big');
  const mime = /^image\/[a-z0-9.+-]+$/i.test(b.photo.type || '') ? b.photo.type : 'image/jpeg';

  const lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    const id = 'KP-' + Utilities.formatDate(new Date(), 'Europe/Kyiv', 'yyMMdd') + '-' +
      Math.random().toString(36).slice(2, 6).toUpperCase();
    const file = folder_().createFile(Utilities.newBlob(bytes, mime, id + '_' + clean_(b.photo.name, 80)));
    const rush = !!b.rush;
    const price = prices[b.size];
    const total = price + (rush ? prices.rush : 0);
    const now = new Date();
    const row = {
      id: id, created: now, status: 'new', who: b.who === 'me' ? 'me' : 'friend', name: name,
      size: b.size, sizeLabel: SIZE_LABELS.uk[b.size], price: price, tech: clean_(b.tech, 40), rush: rush ? 'так' : '',
      total: total, about: clean_(b.about, 2000), email: email, phone: phone, city: city,
      photoId: file.getId(), photoName: clean_(b.photo.name, 120),
      utm_source: clean_(b.utm_source, 80), utm_medium: clean_(b.utm_medium, 80), utm_campaign: clean_(b.utm_campaign, 120),
      referrer: clean_(b.referrer, 300), landing: clean_(b.landing, 300), device: clean_(b.device, 200),
      note: '', updated: now, lang: lang, currency: currency, country: country
    };
    sheet_().appendRow(HEAD.map(function (h) { return row[h]; }));
    notify_(row);
    confirm_(row);
    return { ok: true, id: id, total: total, currency: currency };
  } finally {
    lock.releaseLock();
  }
}

function listOrders_() {
  const sh = sheet_();
  const values = sh.getDataRange().getValues();
  const head = values.shift();
  return values.filter(function (r) { return r[0]; }).map(function (r) {
    const o = {};
    head.forEach(function (h, i) { o[h] = r[i] instanceof Date ? r[i].toISOString() : r[i]; });
    return o;
  }).reverse();
}

function updateOrder_(b) {
  const sh = sheet_();
  const values = sh.getDataRange().getValues();
  const head = values[0];
  for (let i = 1; i < values.length; i++) {
    if (values[i][0] === b.id) {
      if (b.status !== undefined) {
        if (STATUSES.indexOf(b.status) < 0) throw new Error('bad_status');
        sh.getRange(i + 1, head.indexOf('status') + 1).setValue(b.status);
        if (b.status === 'done') sendReviewRequest_(b.id, false);
      }
      if (b.note !== undefined) sh.getRange(i + 1, head.indexOf('note') + 1).setValue(clean_(b.note, 2000));
      sh.getRange(i + 1, head.indexOf('updated') + 1).setValue(new Date());
      return { ok: true };
    }
  }
  throw new Error('not_found');
}

function getPhoto_(id) {
  const o = listOrders_().filter(function (x) { return x.id === id; })[0];
  if (!o || !o.photoId) throw new Error('not_found');
  const blob = DriveApp.getFileById(o.photoId).getBlob();
  return { ok: true, type: blob.getContentType(), data: Utilities.base64Encode(blob.getBytes()) };
}

/* ---------- відгуки ---------- */

/** Підпис посилання на відгук: лише той, хто отримав лист, може залишити відгук до свого замовлення. */
function reviewSig_(orderId) {
  const props = PropertiesService.getScriptProperties();
  let secret = props.getProperty('REVIEW_SECRET');
  if (!secret) { secret = Utilities.getUuid() + Utilities.getUuid(); props.setProperty('REVIEW_SECRET', secret); }
  const raw = Utilities.computeHmacSha256Signature(String(orderId), secret);
  return Utilities.base64EncodeWebSafe(raw).replace(/=+$/, '').slice(0, 22);
}

function findOrder_(id) {
  return listOrders_().filter(function (x) { return x.id === id; })[0];
}

function checkReviewLink_(b) {
  const id = String(b.id || '');
  if (!id || String(b.t || '') !== reviewSig_(id)) throw new Error('bad_link');
  const o = findOrder_(id);
  if (!o) throw new Error('bad_link');
  return o;
}

function reviewSheet_() {
  const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  let sh = ss.getSheetByName(REVIEW_SHEET);
  if (!sh) {
    sh = ss.insertSheet(REVIEW_SHEET);
    sh.appendRow(REVIEW_HEAD);
    sh.setFrozenRows(1);
    sh.getRange(1, 1, 1, REVIEW_HEAD.length).setFontWeight('bold');
  }
  ensureHead_(sh, REVIEW_HEAD);
  return sh;
}

function allReviews_() {
  const values = reviewSheet_().getDataRange().getValues();
  const head = values.shift();
  return values.filter(function (r) { return r[0]; }).map(function (r) {
    const o = {};
    head.forEach(function (h, i) { o[h] = r[i] instanceof Date ? r[i].toISOString() : r[i]; });
    return o;
  }).reverse();
}

function reviewInfo_(b) {
  const o = checkReviewLink_(b);
  const done = allReviews_().some(function (r) { return r.orderId === o.id; });
  const lang = LANGS.indexOf(o.lang) >= 0 ? o.lang : 'uk';
  return { ok: true, orderId: o.id, name: o.name, sizeLabel: SIZE_LABELS[lang][o.size] || o.sizeLabel, who: o.who, lang: lang, already: done };
}

function createReview_(b) {
  const o = checkReviewLink_(b);
  if (allReviews_().some(function (r) { return r.orderId === o.id; })) throw new Error('already');
  const rating = Math.round(Number(b.rating));
  if (!(rating >= 1 && rating <= 5)) throw new Error('bad_rating');
  const text = clean_(b.text, 1500);
  const author = clean_(b.author, 60);
  if (!text || !author) throw new Error('missing_fields');
  let photoId = '';
  if (b.photo && b.photo.data) {
    const bytes = Utilities.base64Decode(String(b.photo.data));
    if (bytes.length > MAX_PHOTO_BYTES) throw new Error('photo_too_big');
    photoId = folder_().createFile(Utilities.newBlob(bytes, 'image/jpeg', 'review_' + o.id + '.jpg')).getId();
  }
  const now = new Date();
  const row = { id: 'R-' + o.id, created: now, orderId: o.id, status: 'pending', rating: rating, author: author,
    text: text, consent: b.consent ? 'так' : 'ні', photoId: photoId, email: o.email, updated: now,
    lang: LANGS.indexOf(o.lang) >= 0 ? o.lang : 'uk' };
  reviewSheet_().appendRow(REVIEW_HEAD.map(function (h) { return row[h]; }));
  try {
    MailApp.sendEmail({
      to: Session.getEffectiveUser().getEmail(),
      subject: 'Новий відгук ' + '★'.repeat(rating) + ' · ' + o.id,
      body: author + ' (' + rating + '/5)' + (b.consent ? '' : ' — БЕЗ згоди на публікацію') + ':\n\n' + text +
        '\n\nОпублікувати можна в адмінці: ' + SITE + '/admin/'
    });
  } catch (e) { /* не критично */ }
  return { ok: true };
}

function publicReviews_(lang) {
  lang = LANGS.indexOf(lang) >= 0 ? lang : 'uk';
  const cache = CacheService.getScriptCache();
  const hit = cache.get('pub_reviews_' + lang);
  if (hit) return JSON.parse(hit);
  const list = allReviews_().filter(function (r) { return r.status === 'published' && r.consent === 'так' && (r.lang || 'uk') === lang; })
    .map(function (r) {
      return { rating: Number(r.rating), author: String(r.author).replace(/^'/, ''), text: String(r.text).replace(/^'/, ''),
        date: String(r.created).slice(0, 10),
        photo: r.photoId ? 'https://drive.google.com/thumbnail?id=' + r.photoId + '&sz=w800' : '' };
    });
  cache.put('pub_reviews_' + lang, JSON.stringify(list), 300);
  return list;
}

function updateReview_(b) {
  if (REVIEW_STATUSES.indexOf(b.status) < 0) throw new Error('bad_status');
  const sh = reviewSheet_();
  const values = sh.getDataRange().getValues();
  const head = values[0];
  for (let i = 1; i < values.length; i++) {
    if (values[i][0] === b.id) {
      if (b.status === 'published' && values[i][head.indexOf('consent')] !== 'так') throw new Error('no_consent');
      sh.getRange(i + 1, head.indexOf('status') + 1).setValue(b.status);
      sh.getRange(i + 1, head.indexOf('updated') + 1).setValue(new Date());
      const photoId = values[i][head.indexOf('photoId')];
      if (photoId) {
        try {
          DriveApp.getFileById(photoId).setSharing(
            b.status === 'published' ? DriveApp.Access.ANYONE_WITH_LINK : DriveApp.Access.PRIVATE, DriveApp.Permission.VIEW);
        } catch (e) { /* фото не критичне */ }
      }
      CacheService.getScriptCache().removeAll(['pub_reviews_uk', 'pub_reviews_en', 'pub_reviews_fr']);
      return { ok: true };
    }
  }
  throw new Error('not_found');
}

function getReviewPhoto_(id) {
  const r = allReviews_().filter(function (x) { return x.id === id; })[0];
  if (!r || !r.photoId) throw new Error('not_found');
  const blob = DriveApp.getFileById(r.photoId).getBlob();
  return { ok: true, type: blob.getContentType(), data: Utilities.base64Encode(blob.getBytes()) };
}

/** Лист із проханням залишити відгук. Автоматично надсилається один раз, коли замовлення стає «Вручено». */
function sendReviewRequest_(orderId, force) {
  const props = PropertiesService.getScriptProperties();
  const key = 'rv_sent_' + orderId;
  if (!force && props.getProperty(key)) return { ok: true, skipped: true };
  const o = findOrder_(orderId);
  if (!o) throw new Error('not_found');
  const L = T_[LANGS.indexOf(o.lang) >= 0 ? o.lang : 'uk'];
  const link = SITE + '/vidguk/?id=' + encodeURIComponent(o.id) + '&t=' + reviewSig_(o.id);
  const intro = o.who === 'friend' ? L.rvGift(o.name) : L.rvSelf;
  const text = L.hi + '\n\n' + intro + '\n\n' + L.rvAsk + '\n' + link + '\n\n' + L.rvReply + '\n\n' + L.brand + '\n' + L.orderNo + ' ' + o.id;
  const html = '<div style="font-family:Arial,sans-serif;font-size:15px;line-height:1.55;color:#1b1d2a;max-width:560px">' +
    '<p>' + L.hi + '</p><p>' + esc_(intro) + '</p>' +
    '<p>' + L.rvAsk + '<br><a href="' + link + '">' + L.rvLink + '</a></p>' +
    '<p>' + L.rvReply + '</p>' +
    '<p>' + L.brand + '<br><span style="color:#6a6c7c">' + L.orderNo + ' ' + esc_(o.id) + '</span></p></div>';
  MailApp.sendEmail({ to: o.email, subject: L.rvSubject(o.id), name: L.brand,
    replyTo: Session.getEffectiveUser().getEmail(), htmlBody: html, body: text });
  props.setProperty(key, new Date().toISOString());
  return { ok: true, link: link };
}

function auth_(token) {
  const real = PropertiesService.getScriptProperties().getProperty('ADMIN_TOKEN');
  if (!real || token !== real) throw new Error('unauthorized');
}

function sheet_() {
  const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  let sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) {
    sh = ss.insertSheet(SHEET_NAME);
    sh.appendRow(HEAD);
    sh.setFrozenRows(1);
    sh.getRange(1, 1, 1, HEAD.length).setFontWeight('bold');
  }
  ensureHead_(sh, HEAD);
  return sh;
}

/** Дописує нові колонки в заголовок, якщо таблицю створено старою версією коду. */
function ensureHead_(sh, head) {
  const cur = sh.getRange(1, 1, 1, Math.max(sh.getLastColumn(), 1)).getValues()[0];
  if (cur.length < head.length || cur[head.length - 1] !== head[head.length - 1]) {
    sh.getRange(1, 1, 1, head.length).setValues([head]).setFontWeight('bold');
  }
}

function folder_() {
  const props = PropertiesService.getScriptProperties();
  const id = props.getProperty('FOLDER_ID');
  if (id) {
    try { return DriveApp.getFolderById(id); } catch (e) { /* створимо нову */ }
  }
  const f = DriveApp.createFolder(FOLDER_NAME);
  props.setProperty('FOLDER_ID', f.getId());
  return f;
}

function notify_(o) {
  try {
    MailApp.sendEmail({
      to: Session.getEffectiveUser().getEmail(),
      subject: 'Нове замовлення ' + o.id + (o.lang !== 'uk' ? ' [' + o.lang.toUpperCase() + ']' : '') + ' · ' + o.sizeLabel + ' · ' + money_(o.total, o.currency),
      body: [
        'Для: ' + o.name + (o.who === 'friend' ? ' (подарунок)' : ' (для себе)'),
        'Полотно: ' + o.sizeLabel + ', техніка: ' + (o.tech || '—') + (o.rush ? ', терміново' : ''),
        'Сума: ' + money_(o.total, o.currency) + (o.currency !== 'UAH' ? ' + доставка (порахувати й узгодити з клієнтом)' : ''),
        'Мова сайту: ' + o.lang,
        'Email: ' + o.email + ', тел.: ' + o.phone,
        (o.currency !== 'UAH' ? 'Країна: ' + o.country + '\nАдреса: ' : 'НП: ') + o.city,
        'Джерело: ' + (o.utm_source || o.referrer || 'прямий захід'),
        '',
        'Про людину: ' + (o.about || '—')
      ].join('\n')
    });
  } catch (e) { /* лист не критичний */ }
}

function esc_(t) {
  return String(t).replace(/[&<>"']/g, function (c) { return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]; });
}

/** Тексти листів трьома мовами. */
const T_ = {
  uk: {
    brand: 'Кислі пички', hi: 'Привіт!', orderNo: 'Замовлення',
    subject: function (id) { return 'Кислі пички: замовлення ' + id + ' прийнято'; },
    thanks: 'Дякуємо! Замовлення прийнято, художник уже готує фарби.',
    rows: ['Номер замовлення', 'Портрет для', 'Полотно', 'Техніка', 'Терміново', 'Сума', 'Доставка'],
    gift: ' (подарунок)', anyTech: 'на вибір художника', rushYes: 'так, 48 годин', rushNo: 'ні, 3–5 днів',
    shipUA: function (c) { return 'Нова пошта: ' + c; }, shipIntl: function (c, a) { return c + ', ' + a; },
    next: 'Ми напишемо тобі найближчим часом, щоб узгодити оплату й деталі. Якщо щось хочеш уточнити, просто відповідай на цей лист.',
    nextIntl: '', footer: 'Сум не лікуємо. Трошки сміємося разом з ним.',
    momentTitle: 'Зніми момент, коли даруєш',
    momentIntro: 'Найцінніше в цьому подарунку не сама картина, а секунда, коли людина вперше за довгий час сміється. Зафіксуй її на відео чи фото. Це доказ, якого їй так бракувало: я ще вмію сміятися.',
    moment: [['Увімкни запис заздалегідь', 'Постав телефон на полицю або попроси когось знімати. Реакція триває кілька секунд, її легко проґавити.'],
      ['Спершу сумне фото, потім картина', 'Нагадай, яким було те селфі, а тоді розгорни полотно. Найщиріший сміх буває саме на контрасті.'],
      ['Покажи відео пізніше', 'За день чи тиждень, коли знову накриє. Людина побачить себе усміхненою, і це працює краще за будь-які поради.'],
      ['Не наполягай', 'Якщо людина не хоче зніматися, просто будь поруч. Момент важливіший за кадр.']],
    rvSubject: function (id) { return 'Замовлення ' + id + ': як вам портрет?'; },
    rvGift: function (n) { return 'Портрет для ' + n + ' уже доїхав. Як пройшов момент, коли дарували? Нам дуже цікаво, чи вдалося розсмішити.'; },
    rvSelf: 'Ваш портрет уже вдома. Як він вам? Вдалося посміятися?',
    rvAsk: 'Якщо маєте хвилинку, залиште, будь ласка, короткий відгук: зірочки і пару слів. Художник читає кожен.',
    rvLink: 'Залишити відгук про портрет', rvReply: 'Або просто відповідайте на цей лист, ми теж прочитаємо.'
  },
  en: {
    brand: 'Sour Mugs', hi: 'Hi!', orderNo: 'Order',
    subject: function (id) { return 'Sour Mugs: order ' + id + ' received'; },
    thanks: 'Thank you! Your order is in, and the artist is already getting the paints out.',
    rows: ['Order number', 'Portrait of', 'Canvas', 'Technique', 'Rush', 'Price', 'Delivery'],
    gift: ' (gift)', anyTech: "artist's choice", rushYes: 'yes, 48 hours', rushNo: 'no, 3–5 days',
    shipUA: function (c) { return 'Nova Post: ' + c; }, shipIntl: function (c, a) { return c + ', ' + a; },
    next: "We'll email you shortly to confirm the details and payment. Got a question? Just reply to this email.",
    nextIntl: 'Shipping from Ukraine with Nova Post is calculated for your country. We will send you the exact cost before you pay. Import VAT or duties may apply depending on your country.',
    footer: "We don't cure sadness. We just laugh with it a little.",
    momentTitle: 'Film the moment you give it',
    momentIntro: "The most precious part of this gift isn't the painting. It's the second when someone laughs for the first time in a long while. Catch it on video or in a photo. It's the proof they've been missing: I can still laugh.",
    moment: [['Start recording early', 'Put your phone on a shelf or ask someone to film. The reaction lasts a few seconds and is easy to miss.'],
      ['Sad photo first, then the painting', 'Remind them of that selfie, then unwrap the canvas. The most honest laughs come from the contrast.'],
      ['Show the video later', 'A day or a week later, when things get heavy again. Seeing yourself smile works better than any advice.'],
      ["Don't insist", "If they don't want to be filmed, just be there. The moment matters more than the shot."]],
    rvSubject: function (id) { return 'Order ' + id + ': how do you like the portrait?'; },
    rvGift: function (n) { return 'The portrait of ' + n + ' has arrived. How did the moment go when you gave it? We would love to know if it made them laugh.'; },
    rvSelf: 'Your portrait is home. How do you like it? Did it make you laugh?',
    rvAsk: 'If you have a minute, please leave a short review: a few stars and a couple of words. The artist reads every one.',
    rvLink: 'Review your portrait', rvReply: "Or simply reply to this email, we'll read that too."
  },
  fr: {
    brand: 'Mines Boudeuses', hi: 'Bonjour !', orderNo: 'Commande',
    subject: function (id) { return 'Mines Boudeuses : commande ' + id + ' reçue'; },
    thanks: "Merci ! Votre commande est bien reçue, l'artiste sort déjà ses pinceaux.",
    rows: ['Numéro de commande', 'Portrait de', 'Toile', 'Technique', 'Express', 'Prix', 'Livraison'],
    gift: ' (cadeau)', anyTech: "au choix de l'artiste", rushYes: 'oui, 48 heures', rushNo: 'non, 3 à 5 jours',
    shipUA: function (c) { return 'Nova Post : ' + c; }, shipIntl: function (c, a) { return c + ', ' + a; },
    next: 'Nous vous écrivons très vite pour confirmer les détails et le paiement. Une question ? Répondez simplement à cet e-mail.',
    nextIntl: "La livraison depuis l'Ukraine avec Nova Post est calculée pour votre pays. Nous vous envoyons le coût exact avant le paiement. Selon le pays, des frais de douane ou une TVA à l'import peuvent s'appliquer.",
    footer: 'On ne soigne pas la tristesse. On en rit un peu ensemble.',
    momentTitle: "Filmez le moment où vous l'offrez",
    momentIntro: "Le plus précieux dans ce cadeau, ce n'est pas le tableau, c'est la seconde où la personne rit pour la première fois depuis longtemps. Capturez-la en vidéo ou en photo. C'est la preuve qui lui manquait : je sais encore rire.",
    moment: [["Lancez l'enregistrement à l'avance", "Posez le téléphone sur une étagère ou demandez à quelqu'un de filmer. La réaction dure quelques secondes, facile de la rater."],
      ["D'abord la photo triste, puis le tableau", 'Rappelez à quoi ressemblait ce selfie, puis déballez la toile. Les rires les plus sincères naissent du contraste.'],
      ['Montrez la vidéo plus tard', "Un jour ou une semaine après, quand ça redevient lourd. Se voir sourire marche mieux que n'importe quel conseil."],
      ["N'insistez pas", "Si la personne ne veut pas être filmée, soyez simplement là. Le moment compte plus que l'image."]],
    rvSubject: function (id) { return 'Commande ' + id + ' : que pensez-vous du portrait ?'; },
    rvGift: function (n) { return 'Le portrait de ' + n + ' est bien arrivé. Comment s’est passé le moment du cadeau ? On aimerait beaucoup savoir s’il a fait rire.'; },
    rvSelf: 'Votre portrait est arrivé. Il vous plaît ? Vous avez ri ?',
    rvAsk: "Si vous avez une minute, laissez-nous un petit avis : quelques étoiles et deux mots. L'artiste les lit tous.",
    rvLink: 'Donner mon avis sur le portrait', rvReply: 'Ou répondez simplement à cet e-mail, on le lira aussi.'
  }
};

/** Лист-підтвердження замовнику мовою сайту, з якого прийшло замовлення. */
function confirm_(o) {
  try {
    const lang = LANGS.indexOf(o.lang) >= 0 ? o.lang : 'uk';
    const L = T_[lang];
    const gift = o.who === 'friend';
    const intl = o.currency && o.currency !== 'UAH';
    const vals = [o.id, o.name + (gift ? L.gift : ''), SIZE_LABELS[lang][o.size], o.tech || L.anyTech,
      o.rush ? L.rushYes : L.rushNo, money_(o.total, o.currency || 'UAH'), intl ? L.shipIntl(o.country, o.city) : L.shipUA(o.city)];
    const lines = L.rows.map(function (r, i) { return [r, vals[i]]; });
    const rows = lines.map(function (l) {
      return '<tr><td style="padding:6px 12px 6px 0;color:#6a6c7c">' + esc_(l[0]) + '</td><td style="padding:6px 0;font-weight:700">' + esc_(l[1]) + '</td></tr>';
    }).join('');
    const momentHtml = '<div style="background:#fff6d6;border-radius:12px;padding:16px 18px;margin:18px 0 16px">' +
      '<div style="font-size:20px;font-weight:700;margin:0 0 8px">' + L.momentTitle + '</div>' +
      '<p style="margin:0 0 12px">' + L.momentIntro + '</p><ol style="margin:0;padding-left:20px">' +
      L.moment.map(function (x) { return '<li style="margin:0 0 8px"><b>' + x[0] + '.</b> ' + x[1] + '</li>'; }).join('') + '</ol></div>';
    const momentText = L.momentTitle.toUpperCase() + '\n' + L.momentIntro + '\n\n' +
      L.moment.map(function (x, i) { return (i + 1) + '. ' + x[0] + '. ' + x[1]; }).join('\n');
    const html =
      '<div style="font-family:Arial,sans-serif;max-width:560px;margin:0 auto;color:#1b1d2a">' +
      '<div style="background:#ffd23f;padding:22px 24px;border-radius:16px 16px 0 0;font-size:26px;font-weight:700">' + L.brand + '</div>' +
      '<div style="border:2px solid #1b1d2a;border-top:0;border-radius:0 0 16px 16px;padding:22px 24px">' +
      '<p style="font-size:18px;margin:0 0 14px">' + L.thanks + '</p>' +
      '<table style="border-collapse:collapse;font-size:15px;margin:0 0 16px">' + rows + '</table>' +
      '<p style="margin:0 0 10px">' + L.next + '</p>' +
      (intl ? '<p style="margin:0 0 10px">' + L.nextIntl + '</p>' : '') +
      (gift ? momentHtml : '') +
      '<p style="margin:0;color:#6a6c7c;font-size:13px">' + L.footer + '</p>' +
      '</div></div>';
    MailApp.sendEmail({
      to: o.email, subject: L.subject(o.id), name: L.brand,
      replyTo: Session.getEffectiveUser().getEmail(), htmlBody: html,
      body: lines.map(function (l) { return l[0] + ': ' + l[1]; }).join('\n') + '\n\n' + L.next +
        (intl ? '\n\n' + L.nextIntl : '') + (gift ? '\n\n' + momentText : '')
    });
  } catch (e) { /* лист не критичний */ }
}

function clean_(v, max) {
  const s = String(v == null ? '' : v).replace(/[\u0000-\u001f]/g, ' ').trim().slice(0, max);
  // щоб текст клієнта не став формулою в таблиці
  return /^[=+\-@]/.test(s) ? "'" + s : s;
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
