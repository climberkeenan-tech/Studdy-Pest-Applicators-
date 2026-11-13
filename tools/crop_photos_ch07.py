"""Crop the Chapter 7 photographs from the user's page photos.
Usage: python3 tools/crop_photos_ch07.py sheet <dir>   (contact sheet for checking)
       python3 tools/crop_photos_ch07.py save content/images
Coordinates are in a 1500x2000 display space on the raw pixels (no EXIF rotation).
The page photos have a purple cast from room lighting, so crops are saved in grayscale."""
import sys, os
from PIL import Image, ImageDraw, ImageOps
U = '/root/.claude/uploads/f814ea2d-2ca2-53f6-8b21-fd7854923436/'
C = {
 'p112-particle':   ('677f28b2', (272, 342, 884, 700)),
 'p116-airgap':     ('91507bab', (218, 532, 624, 790)),
 'p116-checkvalve': ('91507bab', (212, 1052, 524, 1488)),
 'p117-apiary':     ('a2982aab', (965, 165, 1335, 440)),
 'p117-wildlife':   ('a2982aab', (978, 540, 1355, 820)),
 'p117-playground': ('a2982aab', (980, 925, 1372, 1215)),
 'p117-plants':     ('a2982aab', (992, 1325, 1398, 1630)),
 'p118-beeicon':    ('c2cb3da4', (112, 198, 432, 472)),
 'p118-bee':        ('c2cb3da4', (30, 975, 418, 1296)),
 'p119-falcon':     ('176164a8', (838, 758, 1228, 1192)),
 'p119-bulletin':   ('176164a8', (120, 1190, 500, 1702)),
 'p120-manatee':    ('3e42fe6e', (365, 785, 920, 1225)),
}
mode, outdir = sys.argv[1], sys.argv[2]
tiles = []
for k, (f, box) in C.items():
    im = Image.open(U + f + '-image.jpg')
    sx = im.size[0] / 1500; sy = im.size[1] / 2000
    b = tuple(int(v * s) for v, s in zip(box, (sx, sy, sx, sy)))
    c = ImageOps.autocontrast(im.crop(b).convert('L'), cutoff=1)
    if mode == 'sheet':
        t = c.convert('RGB'); t.thumbnail((360, 360)); d = ImageDraw.Draw(t)
        d.rectangle((0, 0, len(k) * 7 + 6, 14), fill='white'); d.text((3, 2), k, fill='black'); tiles.append(t)
    else:
        c.thumbnail((560, 560))
        p = os.path.join(outdir, k + '.jpg')
        c.save(p, 'JPEG', quality=74, optimize=True, progressive=True)
        print(k, c.size, os.path.getsize(p) // 1024, 'KB')
if mode == 'sheet':
    cols, w = 4, 370; rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * w, rows * w), 'white')
    for i, t in enumerate(tiles): sheet.paste(t, ((i % cols) * w, (i // cols) * w))
    sheet.save(os.path.join(outdir, 'crops07.jpg'), quality=80)
