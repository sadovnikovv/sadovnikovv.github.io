/* ==========================================================================
   Рендер книги на странице.
   Книга (book.html) по-прежнему работает сама по себе, без сети и без этого
   файла. Здесь страница забирает из неё титул (h1 в .cover) и текст
   (main#content) — это единственный источник содержимого. Правки содержания
   делаются в Книга-Claude-Code.html и затем `python build_site.py`.
   ========================================================================== */
(function () {
  'use strict';

  var BOOK_URL = document.documentElement.getAttribute('data-book-src') || '../book.html';
  var DONE_KEY = 'cc-book-render-v1';

  var root = document.getElementById('book');
  // Пользователь уже был в книге: сразу живой рендер, без тёмного титула.
  // file:// меняет document.referrer на путь к css — тогда это первый визит.
  var fromBook = history.state === 'book' || /book\.html/i.test(document.referrer);
  var skipIntro = false;
  try { skipIntro = fromBook || sessionStorage.getItem(DONE_KEY) === '1'; } catch (e) {}

  var pages = (function () {
    var el = document.getElementById('page-list');
    if (!el) return [];
    try { return JSON.parse(el.textContent); } catch (e) { return []; }
  })();
  var idxEl = document.getElementById('page-index');
  var idx = idxEl ? parseInt(idxEl.getAttribute('content'), 10) || 0 : 0;

  // Названия и ссылки соседних глав работают и до рендера.
  if (pages.length) {
    var prev = pages[idx - 1], next = pages[idx + 1];
    document.querySelectorAll('[data-rel="prev"]').forEach(function (a) {
      if (prev) { a.dataset.href = prev.url; a.textContent = '← ' + prev.title; a.hidden = false; }
      else a.remove();
    });
    document.querySelectorAll('[data-rel="next"]').forEach(function (a) {
      if (next) { a.dataset.href = next.url; a.textContent = next.title + ' →'; a.hidden = false; }
      else a.remove();
    });
    if (pages[idx]) document.title = pages[idx].title + ' — ' + document.title.split(' — ').pop();
  }

  if (!root) return;

  function showError(msg) {
    var box = document.createElement('div');
    box.className = 'error-box';
    var head = document.createElement('p');
    head.innerHTML = '<strong>Не удалось загрузить текст книги.</strong>';
    var why = document.createElement('p');
    why.textContent = msg;
    var link = document.createElement('p');
    link.innerHTML = '<a href="../book.html">Открыть книгу целиком</a>';
    box.appendChild(head);
    box.appendChild(why);
    box.appendChild(link);
    root.replaceChildren(box);
    document.body.classList.add('rendered');
    document.body.classList.remove('is-loading');
  }

  // Плавный переход с тёмного титула.
  var html = document.documentElement;
  if (!skipIntro) {
    html.classList.add('intro');
    setTimeout(function () { html.classList.remove('intro'); }, 650);
  }
  document.body.classList.add('is-loading');

  function fetchBook(url) {
    return window.fetch(url, { credentials: 'same-origin' })
      .then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.text();
      })
      .catch(function () {
        // file:// в Chrome не даёт fetch — откатываемся на обычный запрос.
        return new Promise(function (resolve, reject) {
          var x = new XMLHttpRequest();
          x.open('GET', url);
          x.onload = function () {
            if (x.status === 200 || (x.status === 0 && x.responseText)) resolve(x.responseText);
            else reject(new Error('не удалось прочитать ' + url));
          };
          x.onerror = function () { reject(new Error('не удалось прочитать ' + url)); };
          x.send();
        });
      });
  }

  function prepare(main) {
    main.querySelectorAll('h2[id], h3[id], h4[id]').forEach(function (h) {
      var a = document.createElement('a');
      a.className = 'h-anchor';
      a.href = '#' + h.id;
      a.setAttribute('aria-label', 'Ссылка на раздел');
      a.textContent = '#';
      h.appendChild(a);
    });
    // Титул и оглавление есть на главной странице; внутри глав они лишние.
    if (idx > 0) main.querySelectorAll('.cover, .toc-inline').forEach(function (n) { n.remove(); });
    return main;
  }

  fetchBook(BOOK_URL).then(function (text) {
    var parsed = new DOMParser().parseFromString(text, 'text/html');

    var cover = parsed.querySelector('.cover h1');
    var coverTitle = document.getElementById('cover-title');
    if (cover && coverTitle && !coverTitle.textContent.trim()) coverTitle.textContent = cover.textContent;

    var main = parsed.querySelector('main#content');
    if (!main) throw new Error('в book.html не найден блок <main id="content">');
    main = prepare(document.adoptNode(main));

    root.replaceChildren(main);

    // Соседние главы: ссылки и prefetch при наведении.
    document.querySelectorAll('[data-href]').forEach(function (a) {
      a.href = a.dataset.href;
      a.addEventListener('mouseenter', function () {
        var l = document.createElement('link');
        l.rel = 'prefetch';
        l.href = a.dataset.href;
        document.head.appendChild(l);
      }, { once: true });
    });

    try { sessionStorage.setItem(DONE_KEY, '1'); } catch (e) {}
    document.body.classList.add('rendered');
    document.body.classList.remove('is-loading');

    // #якорь пришёл раньше содержимого — довести до нужного раздела.
    if (location.hash.length > 1) {
      var t = document.getElementById(decodeURIComponent(location.hash.slice(1)));
      if (t) t.scrollIntoView();
    }
  }).catch(function (e) {
    showError(String(e && e.message ? e.message : e));
  });
})();
