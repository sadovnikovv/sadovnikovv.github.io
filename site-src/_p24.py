from pathlib import Path

f = Path(r"C:/Users/user/Downloads/Sasha_II_TUT/site-src/build_site.py")
L = f.read_text(encoding="utf-8").split("\n")
first = next(i for i, l in enumerate(L) if "Глава 33 (курсы академии) и глава 34 (практикум)" in l)
dup = next(i for i, l in enumerate(L) if i > first + 2 and "ровно по одному разу, в конце" in l)
# удалить строки с первой копией: от first до второй копии комментариев (включительно)
end_first = next(k for k in range(first, dup) if "m = re.search(r'</main>'" in L[k])
L[first:end_first + 1] = []
f.write_text("\n".join(L), encoding="utf-8", newline="\n")
print("removed", end_first - first + 1, "lines")
