"""Chapter 9 photo crops. Shot under purple light, so crops are converted to grayscale."""
import sys, os
from PIL import Image, ImageDraw, ImageOps
U='/root/.claude/uploads/1b053c7f-e9bd-5a4f-80a0-0942958c3cb3/'
# coordinates in the 1500x2000 display space (raw pixels, no EXIF rotation)
C = {
 'p135-spillkit':   ('50fc0015', (1060, 525, 1500, 1005)),
 'p136-fire':       ('d31b2a37', (115, 138, 600, 495)),
 'p137-sprinkler':  ('a9ca9386', (140, 1325, 572, 1612)),
 'p137-plan':       ('a9ca9386', (1018, 588, 1300, 945)),
 'p137-sign':       ('a9ca9386', (1040, 1310, 1312, 1592)),
 'p138-nfpa':       ('15b6f8e6', (85, 170, 482, 432)),
 'p138-salvage':    ('15b6f8e6', (55, 665, 458, 972)),
 'p138-spill':      ('15b6f8e6', (55, 1185, 535, 1568)),
 'p138-extinguisher':('15b6f8e6', (925, 165, 1402, 812)),
 'p138-ppe':        ('15b6f8e6', (918, 1412, 1418, 1770)),
 'p139-tube':       ('0a8ae21a', (128, 505, 585, 782)),
 'p140-absorbent':  ('e61f04a1', (215, 172, 962, 570)),
 'p140-supplies':   ('e61f04a1', (102, 745, 585, 1372)),
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
        c.thumbnail((560,560))
        p = sys.argv[2] + '/' + k + '.jpg'
        c.save(p, 'JPEG', quality=72, optimize=True, progressive=True)
        print(k, c.size, os.path.getsize(p)//1024, 'KB')
if mode == 'sheet':
    cols=4; w=370; rows=(len(tiles)+cols-1)//cols
    sheet=Image.new('RGB',(cols*w, rows*w),'white')
    for i,t in enumerate(tiles): sheet.paste(t,((i%cols)*w,(i//cols)*w))
    sheet.save(sys.argv[2] + '/crops.jpg', quality=80)
