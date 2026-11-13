"""Crop Chapter 8 (pp. 123-130) photos from the user's page photos.
Usage: python3 tools/crop_photos_ch08.py sheet OUTDIR | save content/images
Coordinates are in the 1500x2000 display space (raw pixels, no EXIF rotation).
The photos were shot under purple light, so crops are converted to grayscale."""
import sys, os
from PIL import Image, ImageDraw, ImageOps
U = '/root/.claude/uploads/2bc1b631-2774-555c-9fe6-a75f29b0ad72/'
C = {
 'p123-danger':     ('4d8a9be2', (915, 685, 1385, 1115)),
 'p124-secure':     ('b16ac13a', (180, 195, 865, 560)),
 'p124-cargo':      ('b16ac13a', (880, 535, 1310, 840)),
 'p124-passenger':  ('b16ac13a', (420, 1340, 840, 1620)),
 'p125-spillkit':   ('2e1457f2', (580, 105, 1170, 665)),
 'p125-feedseed':   ('2e1457f2', (60, 1105, 545, 1395)),
 'p126-shed':       ('94839559', (110, 555, 555, 855)),
 'p126-damp':       ('94839559', (105, 1310, 505, 1630)),
 'p127-floor':      ('cca3e7b5', (140, 985, 560, 1245)),
 'p127-foodjars':   ('cca3e7b5', (985, 635, 1400, 915)),
 'p127-shelving':   ('cca3e7b5', (890, 1215, 1405, 1595)),
 'p128-damaged':    ('994eac94', (20, 390, 595, 815)),
 'p128-dates':      ('994eac94', (380, 1410, 855, 1800)),
 'p129-rinsed':     ('28e899d7', (555, 230, 995, 555)),
 'p129-visitors':   ('28e899d7', (815, 1020, 1245, 1345)),
 'p130-lights':     ('af69fcf3', (60, 675, 470, 925)),
 'p130-sprayers':   ('af69fcf3', (60, 1150, 535, 1505)),
}
mode, out = sys.argv[1], sys.argv[2]
tiles = []
for k, (f, box) in C.items():
    im = Image.open(U + f + '-image.jpg')
    sx, sy = im.size[0] / 1500, im.size[1] / 2000
    b = tuple(int(v * s) for v, s in zip(box, (sx, sy, sx, sy)))
    c = ImageOps.autocontrast(im.crop(b).convert('L'), cutoff=1).convert('RGB')
    if mode == 'sheet':
        t = c.copy(); t.thumbnail((360, 360)); d = ImageDraw.Draw(t)
        d.rectangle((0, 0, len(k) * 7 + 6, 14), fill='white'); d.text((3, 2), k, fill='black'); tiles.append(t)
    else:
        c.thumbnail((560, 560))
        p = os.path.join(out, k + '.jpg')
        c.save(p, 'JPEG', quality=72, optimize=True, progressive=True)
        print(k, c.size, os.path.getsize(p) // 1024, 'KB')
if mode == 'sheet':
    cols, w = 4, 370; rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * w, rows * w), 'white')
    for i, t in enumerate(tiles): sheet.paste(t, ((i % cols) * w, (i // cols) * w))
    sheet.save(os.path.join(out, 'crops.jpg'), quality=80)
