"""Chapter 11 photo crops. Shot under purple light, so crops are converted to grayscale."""
import sys, os
from PIL import Image, ImageDraw, ImageOps
U='/root/.claude/uploads/75adad86-abd8-57ad-9e02-d63f1cd05671/'
# coordinates in the 1500x2000 display space (raw pixels, no EXIF rotation)
C = {
 'p158-broadcast':  ('9c614065', (270, 180, 885, 458)),
 'p158-crack':      ('9c614065', (255, 485, 560, 760)),
 'p158-foliar':     ('9c614065', (572, 505, 875, 772)),
 'p159-closed':     ('cef438f7', (130, 48, 548, 355)),
 'p159-cab':        ('cef438f7', (872, 608, 1358, 992)),
 'p159-minibulk':   ('cef438f7', (45, 1290, 340, 1605)),
 'p160-pad':        ('056b6723', (215, 280, 850, 655)),
 'p160-backpack':   ('056b6723', (805, 940, 1212, 1500)),
 'p160-hydraulic':  ('056b6723', (50, 1252, 500, 1615)),
 'p161-airblast':   ('ea377b2a', (145, 553, 562, 842)),
 'p161-ground':     ('ea377b2a', (945, 245, 1342, 552)),
 'p161-turret':     ('ea377b2a', (1005, 665, 1240, 955)),
 'p161-nozzles':    ('ea377b2a', (68, 1185, 1312, 1735)),
 'p162-flow':       ('dac83295', (75, 238, 402, 798)),
 'p162-rotary':     ('dac83295', (28, 915, 440, 1250)),
 'p162-drop':       ('dac83295', (28, 1312, 420, 1645)),
 'p162-rubs':       ('dac83295', (798, 1298, 1242, 1692)),
 'p163-calibrate':  ('595dd078', (60, 1383, 648, 1802)),
 'p165-cylinder':   ('e0ee707d', (775, 325, 1172, 612)),
 'p166-wind':       ('5295ceee', (88, 722, 430, 998)),
 'p166-uniformity': ('5295ceee', (848, 965, 1292, 1535)),
}
mode = sys.argv[1]
tiles = []
for k,(f,box) in C.items():
    im = Image.open(U+f+'-image.jpg')
    sx = im.size[0]/1500; sy = im.size[1]/2000
    c = ImageOps.autocontrast(im.crop(tuple(int(v*s) for v,s in zip(box,(sx,sy,sx,sy)))).convert('L'), cutoff=1).convert('RGB')
    if mode == 'sheet':
        t = c.copy(); t.thumbnail((360,360)); d=ImageDraw.Draw(t); d.rectangle((0,0,len(k)*7+6,14),fill='white'); d.text((3,2),k,fill='black'); tiles.append(t)
    else:
        lim = 1100 if k == 'p161-nozzles' else 560
        c.thumbnail((lim,lim))
        p = os.path.join(sys.argv[2], k + '.jpg')
        c.save(p, 'JPEG', quality=72, optimize=True, progressive=True)
        print(k, c.size, os.path.getsize(p)//1024, 'KB')
if mode == 'sheet':
    cols=4; w=370; rows=(len(tiles)+cols-1)//cols
    sheet=Image.new('RGB',(cols*w, rows*w),'white')
    for i,t in enumerate(tiles): sheet.paste(t,((i%cols)*w,(i//cols)*w))
    sheet.save(sys.argv[2], quality=80)
