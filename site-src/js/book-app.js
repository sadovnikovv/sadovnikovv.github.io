/* Дополнения к встроенному скрипту книги на сайте (book.html).
   Сама книга по-прежнему работает без этого файла; здесь только то,
   что нужно на сайте: полоса прогресса чтения. */
(function () {
  'use strict';

  var bar = document.getElementById('progress-bar');
  if (!bar) {
    var box = document.querySelector('.progress');
    if (box) box.hidden = true;
    return;
  }
  var onScroll = function () {
    var h = document.documentElement.scrollHeight - window.innerHeight;
    var p = h > 0 ? Math.min(100, Math.max(0, window.scrollY / h * 100)) : 0;
    bar.style.width = p + '%';
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
})();
