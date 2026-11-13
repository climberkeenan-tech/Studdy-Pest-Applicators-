import sys, os
from PIL import Image, ImageDraw
U='/root/.claude/uploads/6304c840-3110-546e-9878-0f53f682cebd/'
# coordinates in the 1500x2000 display space (raw pixels, no EXIF rotation)
C = {
 'p31-jug':      ('e37285ad', (880, 630, 1425, 1275)),
 'p32-shelf':    ('f0516825', (130, 605, 408, 858)),
 'p34-fish':     ('ed30d0ba', (150, 255, 597, 915)),
 'p35-reader':   ('d5be84fb', (965, 275, 1312, 605)),
 'p37-signals':  ('bdce5a7f', (935, 700, 1320, 978)),
 'p38-ppe':      ('8b0ec1ae', (130, 1285, 552, 1632)),
 'p41-wpssign':  ('e3fcc689', (1045, 245, 1385, 490)),
}
mode = sys.argv[1]; tiles=[]
for k,(f,box) in C.items():
    im = Image.open(U+f+'-image.jpg')
    sx = im.size[0]/1500; sy = im.size[1]/2000
    c = im.crop(tuple(int(v*s) for v,s in zip(box,(sx,sy,sx,sy)))).convert('RGB')
    if mode == 'sheet':
        t=c.copy(); t.thumbnail((360,360)); d=ImageDraw.Draw(t); d.rectangle((0,0,len(k)*7+6,14),fill='white'); d.text((3,2),k,fill='black'); tiles.append(t)
    else:
        c.thumbnail((560,560)); p=sys.argv[2]+'/'+k+'.jpg'
        c.save(p,'JPEG',quality=72,optimize=True,progressive=True); print(k,c.size,os.path.getsize(p)//1024,'KB')
if mode == 'sheet':
    cols=4; w=370; rows=(len(tiles)+cols-1)//cols
    sheet=Image.new('RGB',(cols*w,rows*w),'white')
    for i,t in enumerate(tiles): sheet.paste(t,((i%cols)*w,(i//cols)*w))
    sheet.save(sys.argv[2],quality=80)
