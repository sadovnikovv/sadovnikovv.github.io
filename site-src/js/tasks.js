/* Задания и самопроверка без сервера.
   Ответ задания хранится в localStorage браузера (ключ cc-task:ID).
   Вшитый data-quiz (academy_build.py) используется, если нет отдельного файла. */
(function () {
  'use strict';

  var KEY = 'cc-task:';
  var TAB = 'cc-tab';
  var ACTIVE = 'cc-active';

  function store(key, value) {
    try {
      if (value === undefined) return localStorage.getItem(key);
      if (value === null) localStorage.removeItem(key);
      else localStorage.setItem(key, value);
    } catch (e) { return null; }
  }

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text !== undefined) n.textContent = text;
    return n;
  }

  function fmtDate(ts) {
    try { return new Date(ts).toLocaleDateString('ru-RU'); } catch (e) { return ''; }
  }

  function activeTab() {
    var t = store(TAB);
    return t === 'step' ? 'step' : 'answer';
  }

  function setActive(btn) {
    var group = btn.parentNode.querySelectorAll('button[data-tab]');
    group.forEach(function (b) { b.setAttribute('aria-selected', b === btn ? 'true' : 'false'); });
    var panes = btn.parentNode.parentNode.querySelectorAll('.task-pane');
    panes.forEach(function (p) { p.hidden = p.getAttribute('data-pane') !== btn.dataset.tab; });
    store(TAB, btn.dataset.tab);
  }

  /* ---------- одно задание ---------- */
  function buildTask(box) {
    if (box.querySelector('.task-tabs')) return;
    var id = box.dataset.task;
    var body = box.querySelector('.task-body');
    if (!body) return;

    // Шаги из блока «Условие» уже есть в HTML. Здесь - вкладки и ввод.
    var tabs = el('div', 'task-tabs');
    tabs.setAttribute('role', 'tablist');
    [['answer', 'Ответ'], ['step', 'Отметка']].forEach(function (t) {
      var b = el('button', 'task-tab', t[1]);
      b.type = 'button';
      b.dataset.tab = t[0];
      b.setAttribute('role', 'tab');
      b.setAttribute('aria-selected', 'false');
      b.addEventListener('click', function () { setActive(b); });
      tabs.appendChild(b);
    });
    body.appendChild(tabs);

    var answer = el('div', 'task-pane');
    answer.dataset.pane = 'answer';
    var ta = el('textarea', 'task-input');
    ta.rows = 6;
    ta.placeholder = 'Ваш ответ: что сделано, что получилось, какие критерии проверены. Сохраняется в этом браузере.';
    ta.setAttribute('aria-label', 'Ответ на задание');
    var saved = store(KEY + id + ':text') || '';
    ta.value = saved;
    var bar = el('div', 'task-bar');
    var save = el('button', 'btn', 'Сохранить');
    save.type = 'button';
    var status = el('span', 'task-status', saved ? 'черновик сохранён' : '');
    var timer = null;
    function persist() {
      store(KEY + id + ':text', ta.value);
      status.textContent = 'черновик сохранён ' + fmtDate(Date.now());
      var c = box.querySelector('.task-count');
      if (c) refreshCount(c);
    }
    ta.addEventListener('input', function () {
      status.textContent = 'печатаете…';
      clearTimeout(timer);
      timer = setTimeout(persist, 600);
    });
    save.addEventListener('click', persist);

    var done = el('label', 'task-done');
    var cb = document.createElement('input');
    cb.type = 'checkbox';
    cb.checked = store(KEY + id + ':done') === '1';
    cb.addEventListener('change', function () {
      store(KEY + id + ':done', cb.checked ? '1' : null);
      var c = box.querySelector('.task-count');
      if (c) refreshCount(c);
      updateBadge();
    });
    done.appendChild(cb);
    done.appendChild(document.createTextNode(' Задание сдано (сохраняется в браузере)'));
    var reset = el('button', 'btn btn-link', 'Очистить');
    reset.type = 'button';
    reset.addEventListener('click', function () {
      if (!confirm('Удалить ответ и отметку этого задания?')) return;
      store(KEY + id + ':text', null);
      store(KEY + id + ':done', null);
      ta.value = '';
      cb.checked = false;
      status.textContent = '';
      var c = box.querySelector('.task-count');
      if (c) refreshCount(c);
      updateBadge();
    });
    bar.appendChild(save);
    bar.appendChild(done);
    bar.appendChild(reset);
    bar.appendChild(status);
    answer.appendChild(ta);
    answer.appendChild(bar);
    body.appendChild(answer);

    var step = el('div', 'task-pane');
    step.dataset.pane = 'step';
    step.appendChild(el('p', 'task-step-note', 'Отметьте, какие шаги задания сделаны. Отметки тоже хранятся только в этом браузере.'));
    var details = box.querySelector('.task-brief-steps');
    var steps = details ? details.querySelectorAll('li') : [];
    var count = el('span', 'task-count');
    if (steps.length) {
      var list = el('ul', 'task-step-list');
      Array.prototype.forEach.call(steps, function (li, i) {
        var key = KEY + id + ':step:' + i;
        var lab = el('label');
        var c = document.createElement('input');
        c.type = 'checkbox';
        c.checked = store(key) === '1';
        c.addEventListener('change', function () { store(key, c.checked ? '1' : null); refreshCount(count); });
        lab.appendChild(c);
        lab.appendChild(document.createTextNode(' ' + li.textContent));
        var item = el('li');
        item.appendChild(lab);
        list.appendChild(item);
      });
      step.appendChild(list);
    } else {
      step.appendChild(el('p', '', 'У этого задания нет разбивки на шаги.'));
    }
    step.appendChild(count);
    body.appendChild(step);
    box.querySelector('.task-brief').appendChild(count);

    refreshCount(count);

    var t = activeTab();
    var b = tabs.querySelector('button[data-tab="' + t + '"]') || tabs.firstChild;
    setActive(b);
  }

  function refreshCount(node) {
    var box = node.closest('.task');
    if (!box) return;
    var total = box.querySelectorAll('.task-step-list input').length;
    var on = box.querySelectorAll('.task-step-list input:checked').length;
    var done = store(KEY + box.dataset.task + ':done') === '1';
    node.textContent = total ? ('шаги: ' + on + ' из ' + total + (done ? ' · сдано' : '')) : (done ? 'сдано' : '');
    box.classList.toggle('is-done', done);
  }

  function updateBadge() {
    var all = document.querySelectorAll('.task');
    var n = 0;
    all.forEach(function (t) { if (store(KEY + t.dataset.task + ':done') === '1') n++; });
    var b = document.getElementById('task-badge');
    if (b) {
      b.textContent = n ? ('сдано: ' + n + ' из ' + all.length) : '';
      b.hidden = !n;
    }
    var line = document.getElementById('task-progress');
    if (line) line.textContent = n + ' из ' + all.length;
  }

  /* ---------- тест ---------- */
  var QUIZ_BUILTIN = null;

  function readQuizData() {
    if (QUIZ_BUILTIN) return QUIZ_BUILTIN;
    var node = document.getElementById('quiz-data');
    var practice = document.getElementById('practice-quiz-data');
    var all = [];
    [node, practice].forEach(function (n) {
      if (!n) return;
      try {
        var arr = JSON.parse(n.textContent);
        if (Array.isArray(arr)) all = all.concat(arr);
      } catch (e) {}
    });
    QUIZ_BUILTIN = all;
    return QUIZ_BUILTIN;
  }

  function buildQuiz(host) {
    var qs = readQuizData();
    if (!qs.length) return;
    var state = {};
    var list = el('ol', 'quiz-list');
    qs.forEach(function (q, qi) {
      var li = el('li', 'quiz-q');
      li.appendChild(el('p', 'quiz-text', (qi + 1) + '. ' + q.q));
      var opts = el('div', 'quiz-opts');
      opts.setAttribute('role', 'radiogroup');
      q.options.forEach(function (o, oi) {
        var lab = el('label', 'quiz-opt');
        var r = document.createElement('input');
        r.type = 'radio';
        r.name = host.id + '-' + qi;
        r.value = String(oi);
        r.addEventListener('change', function () {
          var wasAnswered = qi in state;
          state[qi] = oi;
          opts.querySelectorAll('label').forEach(function (l, k) {
            l.classList.toggle('is-right', k === q.answer);
            l.classList.toggle('is-wrong', k === oi && oi !== q.answer);
          });
          var ex = li.querySelector('.quiz-explain');
          ex.hidden = false;
          ex.textContent = (oi === q.answer ? 'Верно. ' : 'Неверно. ') + (q.explain || '');
          if (wasAnswered) score();
          saveQuiz(host, state);
        });
        lab.appendChild(r);
        lab.appendChild(document.createTextNode(' ' + o));
        opts.appendChild(lab);
      });
      li.appendChild(opts);
      var ex = el('p', 'quiz-explain');
      ex.hidden = true;
      li.appendChild(ex);
      list.appendChild(li);
    });
    host.appendChild(list);
    var res = el('p', 'quiz-result');
    res.setAttribute('aria-live', 'polite');
    host.appendChild(res);

    function score() {
      var n = 0;
      Object.keys(state).forEach(function (k) { if (qs[k] && state[k] === qs[k].answer) n++; });
      res.textContent = 'Правильно: ' + n + ' из ' + qs.length + '.';
    }

    var saved = {};
    try { saved = JSON.parse(store('cc-quiz:' + host.dataset.quiz) || '{}'); } catch (e) { saved = {}; }
    Object.keys(saved).forEach(function (k) {
      var qi = Number(k), oi = saved[k];
      var input = host.querySelector('input[name="' + host.id + '-' + qi + '"][value="' + oi + '"]');
      if (input) { input.checked = true; input.dispatchEvent(new Event('change')); }
    });
  }

  function saveQuiz(host, state) {
    try { store('cc-quiz:' + host.dataset.quiz, JSON.stringify(state)); } catch (e) {}
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.task').forEach(buildTask);
    document.querySelectorAll('.quiz').forEach(buildQuiz);
    updateBadge();
  });

  window.addEventListener('book:rendered', function () {
    document.querySelectorAll('.task').forEach(function (t) { if (!t.querySelector('.task-tabs')) buildTask(t); });
    document.querySelectorAll('.quiz').forEach(function (q) { if (!q.querySelector('.quiz-list')) buildQuiz(q); });
    updateBadge();
  });
})();
