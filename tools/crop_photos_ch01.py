import sys, json, base64, io
from PIL import Image, ImageDraw
U='/root/.claude/uploads/60eedd49-8ed0-5a31-9e3d-e8100822f80a/'
# coordinates in the 1500x2000 display space (raw pixels, no EXIF rotation)
C = {
 'p1-cockroach':   ('085a0dd2', (925, 470, 1260, 900)),
 'p4-thistle':     ('697af7be', (175, 430, 565, 730)),
 'p4-wasp':        ('697af7be', (135, 870, 545, 1175)),
 'p4-rust':        ('697af7be', (100, 1375, 515, 1670)),
 'p5-dove':        ('42df46a5', (1090, 190, 1410, 500)),
 'p6-lacewing':    ('1b8f9433', (160, 265, 590, 635)),
 'p6-ichneumonid': ('1b8f9433', (70, 1230, 595, 1600)),
 'p6-tractor':     ('1b8f9433', (925, 635, 1295, 985)),
 'p7-mulch':       ('a75296ff', (915, 1200, 1370, 1545)),
 'p8-aquatic':     ('43e3a683', (65, 655, 520, 895)),
 'p8-sticky':      ('43e3a683', (770, 1322, 1200, 1632)),
 'p9-usda':        ('620ed903', (660, 915, 1320, 1370)),
 'p11-inspect':    ('02925d78', (1045, 200, 1365, 620)),
}
mode = sys.argv[1]
out = {}
tiles = []
for k,(f,box) in C.items():
    im = Image.open(U+f+'-image.jpg')
    o = im.getexif().get(274)
    sx = im.size[0]/1500; sy = im.size[1]/2000
    b = tuple(int(v*s) for v,s in zip(box,(sx,sy,sx,sy)))
    c = im.crop(b).convert('RGB')
    if mode == 'sheet':
        t = c.copy(); t.thumbnail((360,360)); d=ImageDraw.Draw(t); d.rectangle((0,0,len(k)*7+6,14),fill='white'); d.text((3,2),k,fill='black'); tiles.append(t)
        print(k, 'orient', o, 'crop', c.size)
    else:
        c.thumbnail((560,560))
        c.save(sys.argv[2] + '/' + k + '.jpg', 'JPEG', quality=72, optimize=True, progressive=True)
        import os; print(k, c.size, os.path.getsize(sys.argv[2] + '/' + k + '.jpg')//1024, 'KB')
if mode == 'sheet':
    cols=4; w=370; rows=(len(tiles)+cols-1)//cols
    sheet=Image.new('RGB',(cols*w, rows*w),'white')
    for i,t in enumerate(tiles): sheet.paste(t,((i%cols)*w,(i//cols)*w))
    sheet.save('zoom/crops.jpg', quality=80)

