# Кислі пички — довідка по проєкту

Сервіс: людина завантажує сумне фото себе чи друга, художник малює смішний портрет фарбами на полотні. Головна аудиторія — друзі людей, яким зараз важко (подарунок). Бренд-розробник: Webrarium.

## Адреси
- Сайт: https://kyslipychki.shop (GitHub Pages, кастомний домен, HTTPS)
- Адмінка (PWA): https://kyslipychki.shop/admin/ — пароль у власника (не зберігаємо в документах); на екрані входу є «Запам'ятати мене»
- Сторінка відгуку: /vidguk/?id=…&t=… (лише за підписаним посиланням з листа, noindex)
- Репозиторій: github.com/WhatWeDoinTheShadow/kyslipychki, гілка main
- Домен і DNS: adm.tools (у adm.tools пошта для домену платна, від 99 ₴/міс; поки не підключена)

## Акаунт і бекенд
- Усе працює від Google-акаунта **kyslipychki@gmail.com** (у Chrome це /u/4).
- Таблиця «Кислі пички — замовлення»: ID 1qnL1-woMteoMTsZ5aUOsnx0XI4X10zNlD_pM7Hp-7U4, аркуші «Замовлення» і «Відгуки».
- Apps Script «Кислі пички — бекенд»: проєкт 1DFnQV_1RVUPPr3-pyCumSENkQopNVIWZArTSPd8DZOLsBs4Wr7CEbxWZ (standalone, openById).
- Web app (у config.js): https://script.google.com/macros/s/AKfycbxo_Bt3O_mxjE2xG9BjiOqmpvJ-cHdw-hLtEnD-Os3RHuX9TgO5Z7sccNjp3Hg8H2iq/exec
- Оновлення бекенду: правимо backend/Code.gs у репо → пуш → у редакторі Apps Script вставляємо код (fetch з kyslipychki.shop/backend/Code.gs у Monaco) → Ctrl/Cmd+S → Deploy → Manage deployments → олівець → New version → Deploy. URL не змінюється.
- Дії API: order, reviewInfo, review, reviews (публічні); з токеном: list, status, photo, reviewsAdmin, reviewStatus, reviewPhoto, sendReviewRequest.
- Мультиакаунтний баг Google: OAuth-вікна авторизації краще проходити в інкогніто, залогінившись лише в kyslipychki.

## Листи
- Замовнику: підтвердження з таблицею замовлення; для подарунків — блок «Зніми момент, коли даруєш» (4 поради).
- Власнику: «Нове замовлення …» і «Новий відгук ★…».
- Статус «Вручено» (done) → автоматично лист «Замовлення KP-…: як вам портрет?» з посиланням на відгук (один раз; повторно — кнопкою в картці замовлення).
- Відгук публікується лише вручну в адмінці і лише зі згодою клієнта; тоді з'являється на головній + рейтинг у JSON-LD Product.
- Проблема: листи з нового Gmail інколи йдуть у спам. Остаточне рішення — відправка з домену (Resend/Brevo безкоштовно або пошта adm.tools 99 ₴/міс) з SPF/DKIM у DNS adm.tools. Рішення ще не прийняте.
- Підпис Gmail: анімоване лого kyslipychki.shop/email-logo-blink.gif + текст.

## Ціни
Квадрат 20×20 — 1700 ₴, Портрет 30×40 — 2666 ₴, Великий 50×70 — 4111 ₴; терміново 48 год +666 ₴. Доставка Новою поштою. Техніки: олія, акрил, пастель, на вибір художника.

## Аналітика і SEO
- Google Analytics: акаунт «Кислі пички» (417540232), ресурс kyslipychki.shop (565965256), тег GTM-NXWSKHWM; подія generate_lead при замовленні.
- Search Console: власність підтверджена файлом google0b2f771689c4d729.html (не видаляти), sitemap.xml надіслано.
- Сторінки: головна, /portret-po-foto/, /sharzh-po-foto/, /blog/, /blog/shcho-podaruvaty-druhu-yakomu-vazhko/, /blog/druk-chy-zhyvopys-portret-z-foto/.
- Обкладинки сторінок: assets/covers/*.jpg (600×450 для карток) і *-wide.jpg (1200×630 для статей і OG). Мобільне бургер-меню є і на головній, і в шаблоні скрипта.
- Внутрішні сторінки, блог і sitemap.xml генерує `tools/build_pages.py` (запуск з кореня репо: `python3 tools/build_pages.py .`), стиль `assets/page.css`. Тексти сторінок правимо в цьому скрипті, а не в згенерованих HTML.
- Розмітка: Organization, WebSite, Product (AggregateOffer), FAQPage, BreadcrumbList, BlogPosting.

## Мови (EN/FR)
- Англійська /en/ (бренд «Sour Mugs», ціни USD/GBP/EUR з перемикачем) і французька /fr/ (бренд «Mines Boudeuses», ціни EUR), доставка по світу Nova Post, вартість доставки узгоджуємо листом.
- Ціни за валютами: PRICES у backend/Code.gs і в tools/i18n_home.py (мають збігатися).
- Головні /en/ і /fr/ генерує `python3 tools/build_i18n.py` з української index.html + перекладів у tools/i18n_home.py і tools/i18n_privacy.py. Змінив текст на українській головній — онови пару в i18n_home.py, інакше скрипт підкаже, що не знайшов.
- Внутрішні сторінки EN/FR — tools/pages_i18n.py (запускається разом із build_pages.py). Sitemap з hreflang генерується там же.
- Листи клієнтам (підтвердження, «Зніми момент», прохання про відгук) ідуть мовою замовлення; власнику — українською з позначкою [EN]/[FR].
- Банер cookies + Google Consent Mode: аналітика вмикається лише після згоди (на всіх мовах).

## Бренд
- Лого: обличчя (фіолетове волосся, жовті окуляри, червоні губи, чокер з патьоками) + напис «Кислі пички». Очі кліпають (SMIL) на сайті; GIF-версії для пошти/аватарки.
- Шрифти Caveat + Nunito. Кольори: жовтий #ffd23f, чорнило #1b1d2a, корал #ff5a5f, синій #5b7bd5, темна тема індиго #262a52.

## Відкриті питання
- Пошта з домену проти спаму (вибір сервісу).
- Видалити тестові рядки «ТЕСТ… (видалити)» в таблиці.
- Через 2–3 тижні — переглянути реальні запити в Search Console і доробити тексти/статті.
