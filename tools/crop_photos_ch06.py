import sys, os
from PIL import Image, ImageDraw
U = '/root/.claude/uploads/b88792c3-90f3-59e8-ade3-71d612c1d326/'
# coordinates in the 1500x2000 display space (raw pixels, no EXIF rotation)
C = {
 'p91-posted':      ('ebcd06bb', (848, 332, 1212, 590)),
 'p91-ppe':         ('ebcd06bb', (845, 862, 1265, 1515)),
 'p92-minimum':     ('542d9d8f', (325, 300, 540, 915)),
 'p92-coverall':    ('542d9d8f', (240, 1070, 555, 1595)),
 'p93-apron':       ('f0ae7fcf', (158, 958, 492, 1342)),
 'p93-nocotton':    ('f0ae7fcf', (868, 655, 1205, 935)),
 'p94-gloves':      ('0d56104b', (760, 1350, 1290, 1770)),
 'p95-fig62':       ('a8397586', (905, 200, 1245, 575)),
 'p95-goggles':     ('a8397586', (895, 1212, 1312, 1500)),
 'p96-scba':        ('984624bd', (630, 1090, 830, 1480)),
 'p96-suppliedair': ('984624bd', (860, 1100, 1260, 1600)),
 'p98-papr':        ('9dca3b92', (345, 172, 570, 570)),
 'p98-halfface':    ('9dca3b92', (275, 735, 525, 955)),
 'p98-gasmask':     ('9dca3b92', (240, 1050, 498, 1478)),
 'p99-fittest':     ('77ed1550', (872, 1240, 1172, 1568)),
 'p100-sealcheck':  ('6a61fed2', (225, 275, 485, 725)),
 'p100-wash':       ('6a61fed2', (55, 1025, 400, 1595)),
 'p101-dispose':    ('faae1eb8', (170, 1135, 575, 1650)),
 'p102-clean':      ('e0ba7b24', (285, 300, 752, 605)),
}
mode = sys.argv[1]
tiles = []
for k, (f, box) in C.items():
    im = Image.open(U + f + '-image.jpg')
    sx = im.size[0] / 1500; sy = im.size[1] / 2000
    b = tuple(int(v * s) for v, s in zip(box, (sx, sy, sx, sy)))
    c = im.crop(b).convert('RGB')
    if mode == 'sheet':
        t = c.copy(); t.thumbnail((360, 360)); d = ImageDraw.Draw(t)
        d.rectangle((0, 0, len(k) * 7 + 6, 14), fill='white'); d.text((3, 2), k, fill='black'); tiles.append(t)
    else:
        c.thumbnail((560, 560))
        p = os.path.join(sys.argv[2], k + '.jpg')
        c.save(p, 'JPEG', quality=72, optimize=True, progressive=True)
        print(k, c.size, os.path.getsize(p) // 1024, 'KB')
if mode == 'sheet':
    cols = 5; w = 370; rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * w, rows * w), 'white')
    for i, t in enumerate(tiles): sheet.paste(t, ((i % cols) * w, (i // cols) * w))
    sheet.save(sys.argv[2], quality=80)
