



obuff = []
for ln in open('D:/brush/slave/scripts/pachong/name.txt', encoding='utf-8'):
    if ln in obuff:
        continue
    obuff.append(ln)
with open('D:/brush/slave/scripts/pachong/name2.txt', 'w', encoding='utf-8') as handle:
    handle.writelines(obuff)