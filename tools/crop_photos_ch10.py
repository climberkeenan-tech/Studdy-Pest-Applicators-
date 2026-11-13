"""Crop Chapter 10 photos (pp. 145-151) from the user's page photos.

Usage: python3 tools/crop_photos_ch10.py sheet <dir>   (contact sheet for checking)
       python3 tools/crop_photos_ch10.py save content/images
Coordinates are in the 1500x2000 display space, raw pixel orientation (no EXIF rotation).
The page photos have a purple cast from the lighting, so crops are converted to grayscale
with autocontrast (the manual's photos are single-color duotones anyway).
"""
import os
import sys
from PIL import Image, ImageDraw, ImageOps

U = '/root/.claude/uploads/89afd96f-c298-50f7-8690-e8b79ef89f31/'
C = {
    'p145-foaming':     ('0955751b', (95, 445, 505, 748)),
    'p145-corn':        ('0955751b', (900, 205, 1325, 770)),
    'p146-site':        ('8c60da51', (255, 1295, 850, 1650)),
    'p146-pouring':     ('8c60da51', (905, 1135, 1372, 1478)),
    'p147-backflow':    ('ef112ccf', (75, 905, 508, 1218)),
    'p147-airgap':      ('ef112ccf', (60, 1330, 508, 1645)),
    'p147-knife':       ('ef112ccf', (935, 1150, 1402, 1692)),
    'p148-measure':     ('e732549c', (28, 382, 546, 805)),
    'p148-transfer':    ('e732549c', (915, 88, 1398, 412)),
    'p148-triplerinse': ('e732549c', (95, 1175, 452, 1690)),
    'p149-pressure':    ('31be5b21', (118, 903, 602, 1228)),
    'p149-recycling':   ('31be5b21', (1030, 85, 1500, 730)),
    'p150-walkpath':    ('eeb0c155', (98, 218, 448, 462)),
    'p150-highpressure': ('eeb0c155', (368, 1015, 822, 1678)),
    'p151-cleaning':    ('28c37805', (872, 603, 1402, 978)),
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
    cols, w = 4, 370
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * w, rows * w), 'white')
    for i, t in enumerate(tiles):
        sheet.paste(t, ((i % cols) * w, (i // cols) * w))
    sheet.save(os.path.join(out, 'crops.jpg'), quality=80)
