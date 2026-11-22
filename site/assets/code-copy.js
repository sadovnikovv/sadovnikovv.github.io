/* Блоки кода: как в чатах DeepSeek. Над каждым <pre> - панель с названием языка,
   кнопками «Копировать», «Скачать» и «Перенос строк», а для одиночной строки
   вместо «Скачать» - «Вставить в терминал».
   Работает и на страницах глав (текст рендерится позже), и в book.html. */
(function () {
  'use strict';

  var EXT = { bash: 'sh', shell: 'sh', sh: 'sh', powershell: 'ps1', ps1: 'ps1', cmd: 'bat', bat: 'bat',
    json: 'json', js: 'js', javascript: 'js', ts: 'ts', typescript: 'ts', python: 'py', py: 'py',
    html: 'html', css: 'css', xml: 'xml', yaml: 'yml', yml: 'yml', markdown: 'md', md: 'md',
    sql: 'sql', c: 'c', cpp: 'cpp', svg: 'svg', text: 'txt' };

  var ICON_COPY = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M6.15 4.02c.96 0 1.73 0 2.35.06.62.05 1.16.17 1.64.45.58.34 1.06.82 1.39 1.4.28.48.4 1.01.46 1.64.06.62.06 1.38.06 2.35s0 1.73-.06 2.34c-.06.63-.18 1.16-.46 1.65a3.5 3.5 0 0 1-1.39 1.39c-.48.28-1.02.4-1.64.46-.62.05-1.39.05-2.35.05s-1.73 0-2.35-.05c-.62-.06-1.16-.18-1.64-.46a3.5 3.5 0 0 1-1.4-1.39c-.28-.49-.4-1.02-.45-1.65C.25 11.65.25 10.88.25 9.92s0-1.73.06-2.35c.05-.62.17-1.16.45-1.64a3.5 3.5 0 0 1 1.4-1.4c.48-.28 1.02-.4 1.64-.45.62-.06 1.39-.05 2.35-.05Zm0 1.36c-.99 0-1.68 0-2.22.05-.53.05-.85.14-1.09.28-.37.21-.68.52-.9.9-.14.24-.23.56-.28 1.09-.05.54-.05 1.24-.05 2.22s0 1.68.05 2.22c.05.53.14.85.28 1.09.22.37.53.68.9.9.24.14.56.23 1.09.28.54.05 1.24.05 2.22.05s1.68 0 2.22-.05c.53-.05.85-.14 1.09-.28.37-.21.68-.52.9-.9.14-.24.23-.56.28-1.09.05-.54.05-1.24.05-2.22s0-1.68-.05-2.22c-.05-.53-.14-.85-.28-1.09-.22-.37-.53-.68-.9-.9-.24-.14-.56-.23-1.09-.28-.54-.05-1.24-.05-2.22-.05Zm3.65-5.01c.96 0 1.73 0 2.35.06.63.06 1.16.17 1.65.45.58.34 1.06.82 1.39 1.4.28.48.4 1.02.46 1.64.06.62.06 1.39.06 2.35v1.57c0 .46 0 .76-.04 1.02a3.5 3.5 0 0 1-2.68 3.15v-1.45a2.1 2.1 0 0 0 1.34-1.88c.02-.15.02-.33.02-.84V6.26c0-.98 0-1.68-.05-2.22-.05-.53-.14-.85-.28-1.09a2.1 2.1 0 0 0-.9-.9c-.24-.14-.56-.23-1.09-.28-.54-.05-1.24-.05-2.22-.05H7.71a2.1 2.1 0 0 0-2.19 1.36H4.07A3.46 3.46 0 0 1 7.71.37h2.09Z" fill="currentColor"/></svg>';
  var ICON_DL = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="m15.37 11.41-.25 1.48a3.15 3.15 0 0 1-3.14 2.62H3.78a3.15 3.15 0 0 1-3.14-2.62L.38 11.41l1.42-.24.25 1.48c.12.72.74 1.25 1.48 1.25h8.44c.74 0 1.36-.53 1.48-1.25l.25-1.48 1.42.24ZM8.72 9c.06-.06.12-.12.18-.18l3.58-3.58 1.02 1.02-3.58 3.58c-.28.28-.53.54-.76.72-.24.19-.52.36-.87.42-.19.03-.38.03-.57 0a1.9 1.9 0 0 1-.87-.42c-.23-.18-.48-.44-.76-.72L2.5 6.26l1.02-1.02 3.58 3.58c.06.06.12.12.18.18V1.31h1.44V9Z" fill="currentColor"/></svg>';
  var ICON_CHECK = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M2.5 8.5 6 12l7.5-8" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  var ICON_TERM = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M2 3.5h12v9H2zM4.5 6.5l2 1.5-2 1.5M8 9.5h3.5" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/></svg>';

  function guessLang(pre, code) {
    var cls = (code.className || '') + ' ' + (pre.className || '');
    var m = cls.match(/language-([\w+#.-]+)/);
    if (m) return m[1].toLowerCase();
    var t = code.textContent.trim();
    if (/^(irm|Invoke-|Set-|Get-|Remove-Item|Set-Location|\$env:|claude\s|pwsh)/.test(t)) return 'powershell';
    if (/^(curl|brew|npm|pip|git|sudo|apt|chmod|uv|python|node|export|cd|mkdir|ls)\b/.test(t) || /\(\)\s*\{/.test(t)) return 'bash';
    if (/^[{[][\s\S]*[}\]]$/.test(t)) return 'json';
    return 'text';
  }

  function isOneLiner(text) {
    var lines = text.split('\n').filter(function (l) { return l.trim(); });
    return lines.length === 1;
  }

  function button(cls, icon, label, title) {
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'code-btn ' + (cls || '');
    if (title) b.title = title;
    b.innerHTML = icon + (label ? '<span class="code-btn-text">' + label + '</span>' : '');
    return b;
  }

  function flash(btn, ok) {
    var text = btn.querySelector('.code-btn-text');
    var saved = text ? text.textContent : '';
    btn.classList.add(ok ? 'is-ok' : 'is-fail');
    if (text) text.textContent = ok ? 'Скопировано' : 'Не вышло';
    setTimeout(function () {
      btn.classList.remove('is-ok', 'is-fail');
      if (text) text.textContent = saved;
    }, 1400);
  }

  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise(function (resolve, reject) {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.setAttribute('readonly', '');
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      try {
        var ok = document.execCommand('copy');
        document.body.removeChild(ta);
        ok ? resolve() : reject(new Error('copy'));
      } catch (e) {
        document.body.removeChild(ta);
        reject(e);
      }
    });
  }

  function decorate(pre) {
    if (pre.closest('.code-block') || pre.parentNode.classList.contains('code-content')) return;
    var code = pre.querySelector('code') || pre;
    var lang = guessLang(pre, code);
    var text = code.textContent.replace(/\n$/, '');

    var wrap = document.createElement('div');
    wrap.className = 'code-block';
    var bar = document.createElement('div');
    bar.className = 'code-bar';
    var name = document.createElement('span');
    name.className = 'code-lang';
    name.textContent = lang;
    bar.appendChild(name);

    var actions = document.createElement('div');
    actions.className = 'code-actions';

    var cp = button('btn-copy', ICON_COPY, 'Копировать', 'Скопировать весь блок');
    cp.addEventListener('click', function () {
      copyText(text).then(function () { flash(cp, true); }).catch(function () { flash(cp, false); });
    });
    actions.appendChild(cp);

    if (isOneLiner(text)) {
      var term = button('btn-term', ICON_TERM, 'Вставить в терминал', 'Открыть терминал и вставить команду');
      term.addEventListener('click', function () {
        window.location.href = 'gcode:' + encodeURIComponent(text);
      });
      actions.appendChild(term);
    } else {
      var dl = button('btn-dl', ICON_DL, 'Скачать', 'Сохранить как файл');
      dl.addEventListener('click', function () {
        var ext = EXT[lang] || 'txt';
        var blob = new Blob([text + '\n'], { type: 'text/plain;charset=utf-8' });
        var a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = 'snippet.' + ext;
        document.body.appendChild(a);
        a.click();
        setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 1000);
      });
      actions.appendChild(dl);
    }

    var wl = button('btn-wrap', '↵', 'Перенос строк', 'Переносить длинные строки');
    wl.setAttribute('aria-pressed', 'false');
    wl.addEventListener('click', function () {
      var on = wrap.classList.toggle('wrap-lines');
      wl.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    actions.appendChild(wl);

    bar.appendChild(actions);
    pre.parentNode.insertBefore(wrap, pre);
    wrap.appendChild(bar);
    wrap.appendChild(pre);

    // Одиночная строка без копирования - показать текст для выделения.
    if (isOneLiner(text) && !document.queryCommandSupported) cp.hidden = true;
  }

  function run() {
    document.querySelectorAll('#book pre, main pre').forEach(decorate);
  }

  document.addEventListener('DOMContentLoaded', run);
  window.addEventListener('book:rendered', run);
})();
