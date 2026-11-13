"""Crop Chapter 4 photos/illustrations. Usage: crop_photos_ch04.py sheet|save OUTDIR"""
import sys, os
from PIL import Image, ImageDraw
U = '/root/.claude/uploads/b95927b7-44ef-5d17-906b-2a22b86e698c/'
# coordinates in the 1500x2000 display space (raw pixels, no EXIF rotation)
# areas of page text to paint over with the page color (display space)
MASK = {'p54-baitstation': (452, 1180, 800, 1380)}
C = {
 'p54-baitstation': ('3aa42bb8', (140, 1190, 800, 1625)),
 'p57-dust':        ('f6b15cc1', (820, 235, 1330, 500)),
 'p57-bulbduster':  ('f6b15cc1', (115, 1200, 560, 1440)),
 'p58-granules':    ('852b15e8', (125, 230, 600, 535)),
 'p58-pellets':     ('852b15e8', (40, 1100, 500, 1500)),
 'p59-wp':          ('91341b53', (780, 160, 1270, 455)),
 'p59-wdg-before':  ('91341b53', (950, 775, 1245, 1015)),
 'p59-wdg-after':   ('91341b53', (965, 1110, 1250, 1465)),
 'p60-baitgun':     ('d44ce3bb', (55, 910, 420, 1150)),
 'p61-fumigants':   ('a1bbc558', (890, 235, 1340, 525)),
 'p62-wsp':         ('dae05048', (35, 1005, 525, 1440)),
 'p63-incompat':    ('46b80155', (960, 580, 1280, 955)),
}
mode, outdir = sys.argv[1], sys.argv[2]
tiles = []
for k, (f, box) in C.items():
    im = Image.open(U + f + '-image.jpg')
    sx = im.size[0] / 1500; sy = im.size[1] / 2000
    if k in MASK:
        m = tuple(int(v * s) for v, s in zip(MASK[k], (sx, sy, sx, sy)))
        px = sorted(im.crop(m).convert('L').get_flattened_data()); thr = px[len(px) // 2]
        reg = [c for c in im.crop(m).convert('RGB').get_flattened_data() if sum(c) / 3 >= thr - 5]
        bg = tuple(sorted(ch)[len(ch) // 2] for ch in zip(*reg))
        im = im.copy(); ImageDraw.Draw(im).rectangle(m, fill=bg)
    c = im.crop(tuple(int(v * s) for v, s in zip(box, (sx, sy, sx, sy)))).convert('RGB')
    if mode == 'sheet':
        t = c.copy(); t.thumbnail((360, 360)); d = ImageDraw.Draw(t)
        d.rectangle((0, 0, len(k) * 7 + 6, 14), fill='white'); d.text((3, 2), k, fill='black'); tiles.append(t)
    else:
        c.thumbnail((560, 560))
        p = os.path.join(outdir, k + '.jpg')
        c.save(p, 'JPEG', quality=72, optimize=True, progressive=True)
        print(k, c.size, os.path.getsize(p) // 1024, 'KB')
if mode == 'sheet':
    cols = 4; w = 370; rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * w, rows * w), 'white')
    for i, t in enumerate(tiles): sheet.paste(t, ((i % cols) * w, (i // cols) * w))
    sheet.save(os.path.join(outdir, 'crops.jpg'), quality=80)
