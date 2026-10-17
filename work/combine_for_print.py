from pathlib import Path
from collections import Counter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader
from PIL import Image
import shutil

ROOT=Path('/Users/artem/Desktop/studies/my_projects/social_project')
SOURCE=ROOT/'posters'
ORDER=['volleyball.png','basketball.png','tennis.png','company.png',
       'booked.png','quest.png','where.png']
COPIES=3
assert set(ORDER)=={p.name for p in SOURCE.glob('*.png')}
out=ROOT/'posters-print-3-each-a4.pdf'
w,h=A4
c=canvas.Canvas(str(out),pagesize=A4,pageCompression=1)
c.setTitle('Выбранные постеры — по 3 экземпляра каждого, A4')
c.setSubject('7 постеров, 21 страница, односторонняя печать')
c.setViewerPreference('Duplex','Simplex')
for name in ORDER:
    path=SOURCE/name
    with Image.open(path) as im:
        iw,ih=im.size
    scale=min(w/iw,h/ih)
    dw,dh=iw*scale,ih*scale
    for copy in range(COPIES):
        c.drawImage(ImageReader(str(path)),(w-dw)/2,(h-dh)/2,
                    width=dw,height=dh,mask='auto')
        c.showPage()
c.save()

r=PdfReader(out)
assert len(r.pages)==len(ORDER)*COPIES
counts=Counter()
for i,p in enumerate(r.pages):
    assert abs(float(p.mediabox.width)-w)<.01
    assert abs(float(p.mediabox.height)-h)<.01
    image_ids=[]
    for obj in p['/Resources']['/XObject'].values():
        if obj.get_object().get('/Subtype')=='/Image':
            image_ids.append(obj.idnum)
    assert len(image_ids)==1
    counts[image_ids[0]]+=1
    if i%COPIES:
        assert image_ids[0]==last
    last=image_ids[0]
assert len(counts)==7 and set(counts.values())=={3}

delivery=Path('/Users/artem/Documents/Codex/2026-10-16/new-chat-2/outputs')/out.name
shutil.copy2(out,delivery)
print(f'Verified: {len(r.pages)} A4 pages; {len(counts)} selected posters; 3 copies each.')
print(f'Saved in project: {out}')
print(f'Download copy: {delivery}')
