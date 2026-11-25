/**
 * Кислі пички — бекенд замовлень на Google Apps Script.
 *
 * Як розгорнути:
 * 1. Таблиця → Розширення → Apps Script, вставити цей файл.
 * 2. Запустити функцію setup() один раз і дати доступ. У журналі з'явиться пароль адмінки.
 * 3. Розгорнути → Нове розгортання → Веб-застосунок:
 *    «Виконувати як: я», «Хто має доступ: усі». Скопіювати URL у config.js сайту.
 */

const SHEET_NAME = 'Замовлення';
const FOLDER_NAME = 'Кислі пички — фото замовлень';
const HEAD = ['id', 'created', 'status', 'who', 'name', 'size', 'sizeLabel', 'price', 'tech', 'rush', 'total',
  'about', 'email', 'phone', 'city', 'photoId', 'photoName',
  'utm_source', 'utm_medium', 'utm_campaign', 'referrer', 'landing', 'device', 'note', 'updated'];

const SIZES = {
  sq: { label: 'Квадрат 20×20 см', price: 1700 },
  pt: { label: 'Портрет 30×40 см', price: 2666 },
  lg: { label: 'Великий портрет 50×70 см', price: 4111 }
};
const RUSH_PRICE = 666;
const STATUSES = ['new', 'paid', 'painting', 'shipped', 'done', 'cancelled'];
const MAX_PHOTO_BYTES = 8 * 1024 * 1024;

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
    auth_(body.token);
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
  const size = SIZES[b.size];
  if (!size) throw new Error('bad_size');
  const name = clean_(b.name, 80);
  const email = clean_(b.email, 120);
  const phone = clean_(b.phone, 40);
  const city = clean_(b.city, 160);
  if (!name || !/^\S+@\S+\.\S+$/.test(email) || phone.replace(/\D/g, '').length < 10 || !city) {
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
    const total = size.price + (rush ? RUSH_PRICE : 0);
    const now = new Date();
    const row = {
      id: id, created: now, status: 'new', who: b.who === 'me' ? 'me' : 'friend', name: name,
      size: b.size, sizeLabel: size.label, price: size.price, tech: clean_(b.tech, 40), rush: rush ? 'так' : '',
      total: total, about: clean_(b.about, 2000), email: email, phone: phone, city: city,
      photoId: file.getId(), photoName: clean_(b.photo.name, 120),
      utm_source: clean_(b.utm_source, 80), utm_medium: clean_(b.utm_medium, 80), utm_campaign: clean_(b.utm_campaign, 120),
      referrer: clean_(b.referrer, 300), landing: clean_(b.landing, 300), device: clean_(b.device, 200),
      note: '', updated: now
    };
    sheet_().appendRow(HEAD.map(function (h) { return row[h]; }));
    notify_(row);
    confirm_(row);
    return { ok: true, id: id, total: total };
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

/* ---------- допоміжне ---------- */

function auth_(token) {
  const real = PropertiesService.getScriptProperties().getProperty('ADMIN_TOKEN');
  if (!real || token !== real) throw new Error('unauthorized');
}

function sheet_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) {
    sh = ss.insertSheet(SHEET_NAME);
    sh.appendRow(HEAD);
    sh.setFrozenRows(1);
    sh.getRange(1, 1, 1, HEAD.length).setFontWeight('bold');
  }
  return sh;
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
      subject: 'Нове замовлення ' + o.id + ' · ' + o.sizeLabel + ' · ' + o.total + ' ₴',
      body: [
        'Для: ' + o.name + (o.who === 'friend' ? ' (подарунок)' : ' (для себе)'),
        'Полотно: ' + o.sizeLabel + ', техніка: ' + (o.tech || '—') + (o.rush ? ', терміново' : ''),
        'Сума: ' + o.total + ' ₴',
        'Email: ' + o.email + ', тел.: ' + o.phone,
        'НП: ' + o.city,
        'Джерело: ' + (o.utm_source || o.referrer || 'прямий захід'),
        '',
        'Про людину: ' + (o.about || '—')
      ].join('\n')
    });
  } catch (e) { /* лист не критичний */ }
}

/** Лист-підтвердження замовнику. */
function confirm_(o) {
  try {
    const esc = function (t) { return String(t).replace(/[&<>"']/g, function (c) { return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]; }); };
    const gift = o.who === 'friend';
    const lines = [
      ['Номер замовлення', o.id],
      ['Портрет для', o.name + (gift ? ' (подарунок)' : '')],
      ['Полотно', o.sizeLabel],
      ['Техніка', o.tech || 'на вибір художника'],
      ['Терміново', o.rush ? 'так, 48 годин' : 'ні, 3–5 днів'],
      ['Сума', o.total + ' ₴'],
      ['Доставка', 'Нова пошта: ' + o.city]
    ];
    const rows = lines.map(function (l) {
      return '<tr><td style="padding:6px 12px 6px 0;color:#6a6c7c">' + esc(l[0]) + '</td><td style="padding:6px 0;font-weight:700">' + esc(l[1]) + '</td></tr>';
    }).join('');
    const html =
      '<div style="font-family:Arial,sans-serif;max-width:560px;margin:0 auto;color:#1b1d2a">' +
      '<div style="background:#ffd23f;padding:22px 24px;border-radius:16px 16px 0 0;font-size:26px;font-weight:700">Кислі пички</div>' +
      '<div style="border:2px solid #1b1d2a;border-top:0;border-radius:0 0 16px 16px;padding:22px 24px">' +
      '<p style="font-size:18px;margin:0 0 14px">Дякуємо! Замовлення прийнято, художник уже готує фарби.</p>' +
      '<table style="border-collapse:collapse;font-size:15px;margin:0 0 16px">' + rows + '</table>' +
      '<p style="margin:0 0 10px">Ми напишемо тобі найближчим часом, щоб узгодити оплату й деталі. Якщо щось хочеш уточнити, просто відповідай на цей лист.</p>' +
      '<p style="margin:0;color:#6a6c7c;font-size:13px">Сум не лікуємо. Трошки сміємося разом з ним.</p>' +
      '</div></div>';
    MailApp.sendEmail({
      to: o.email,
      subject: 'Кислі пички: замовлення ' + o.id + ' прийнято',
      name: 'Кислі пички',
      replyTo: Session.getEffectiveUser().getEmail(),
      htmlBody: html,
      body: lines.map(function (l) { return l[0] + ': ' + l[1]; }).join('\n') + '\n\nМи напишемо найближчим часом, щоб узгодити оплату.'
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
