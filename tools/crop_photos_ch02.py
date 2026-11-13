import sys, json, base64, io
from PIL import Image, ImageDraw
U=sys.argv[3] if len(sys.argv)>3 else "/root/.claude/uploads/00b335e3-7a86-5392-9680-ab130a21e84e/"
# coordinates in the 1500x2000 display space (raw pixels, no EXIF rotation)
C = {
 'p19-epa-doc':      ('3ae48773', (925, 590, 1312, 1040)),
 'p20-epa-seal':     ('69a363e8', (205, 490, 552, 835)),
 'p20-rup-label':    ('69a363e8', (140, 1140, 785, 1588)),
 'p22-24c-label':    ('96971220', (105, 250, 515, 550)),
 'p23-usda-chemist': ('1f9439c9', (1020, 525, 1390, 940)),
 'p23-produce':      ('1f9439c9', (868, 1188, 1388, 1562)),
 'p24-scales':       ('13ec6ed5', (145, 450, 445, 765)),
 'p26-wolf':         ('bb60c9a9', (250, 245, 543, 482)),
 'p26-owl':          ('bb60c9a9', (188, 575, 497, 808)),
 'p26-butterfly':    ('bb60c9a9', (105, 890, 462, 1148)),
 'p26-trillium':     ('bb60c9a9', (80, 1245, 378, 1525)),
 'p27-records':      ('20c492b2', (992, 640, 1305, 905)),
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
    sheet.save(sys.argv[2]+'/crops.jpg', quality=80)

