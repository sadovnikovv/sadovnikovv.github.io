from pathlib import Path

f = Path(r"C:/Users/user/Downloads/Sasha_II_TUT/site-src/build_site.py")
s = f.read_text(encoding="utf-8")
old = """<script src="{root}assets/code-copy.js" defer></script>
</body>"""
new = """<script src="{root}assets/code-copy.js" defer></script>
<script>
document.addEventListener('click', function (e) {{
  document.querySelectorAll('.header-support[open]').forEach(function (d) {{
    if (!d.contains(e.target)) d.open = false;
  }});
}});
document.addEventListener('keydown', function (e) {{
  if (e.key !== 'Escape') return;
  document.querySelectorAll('.header-support[open]').forEach(function (d) {{
    d.open = false;
    var s = d.querySelector('summary');
    if (s) s.focus();
  }});
}});
</script>
</body>"""
assert old in s
s = s.replace(old, new, 1)
f.write_text(s, encoding="utf-8", newline="\n")
print("ok")
