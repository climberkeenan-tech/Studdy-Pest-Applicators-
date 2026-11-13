"""Crop the Chapter 5 label photos (pp. 77-78) from the user's page photos.
Coordinates are in a 1500x2000 display space on the raw pixels (no EXIF rotation)."""
import sys, os
from PIL import Image
U = '/root/.claude/uploads/8f531f50-b11c-5fbd-86e5-89f13904cc0f/'
C = {
 'p77-danger-poison': ('b574ec70', (600, 290, 1120, 425)),
 'p77-danger':        ('b574ec70', (625, 895, 1175, 1045)),
 'p78-warning':       ('ce73906f', (290, 255, 830, 405)),
 'p78-caution':       ('ce73906f', (220, 930, 785, 1090)),
}
out = sys.argv[1]
for k, (f, box) in C.items():
    im = Image.open(U + f + '-image.jpg')
    sx, sy = im.size[0] / 1500, im.size[1] / 2000
    c = im.crop(tuple(int(v * s) for v, s in zip(box, (sx, sy, sx, sy)))).convert('RGB')
    c.thumbnail((700, 700))
    p = os.path.join(out, k + '.jpg')
    c.save(p, 'JPEG', quality=80, optimize=True, progressive=True)
    print(k, c.size, os.path.getsize(p) // 1024, 'KB')
