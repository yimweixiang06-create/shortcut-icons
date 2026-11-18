from PIL import Image, ImageFilter, ImageDraw
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "assets/maybank-original.webp"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)
S = 2048
im = Image.open(SRC).convert("RGB").resize((S,S), Image.Resampling.LANCZOS)
a = np.asarray(im).astype(np.float32)
gray = a.mean(axis=2)
m = Image.new("L",(S,S))
d = ImageDraw.Draw(m)
scale = S / 980
d.rounded_rectangle(tuple(round(v*scale) for v in (91,91,889,889)),
                    radius=round(183*scale), fill=255)
inside = np.asarray(m.filter(ImageFilter.GaussianBlur(1.3)),dtype=np.float32)/255
y,x = np.mgrid[0:S,0:S]
white = np.clip((gray-105)/120,0,1)
blend = np.clip(.98-.09*(y/S),.86,1)
new = a*(1-white[:,:,None])+(a*blend[:,:,None])*white[:,:,None]
soft = np.asarray(m.filter(ImageFilter.GaussianBlur(12)),dtype=np.float32)/255
outer = np.maximum(soft-inside,0)
spot1 = np.exp(-(((x-190*scale)/(265*scale))**2+((y-190*scale)/(265*scale))**2)*.9)
spot2 = np.exp(-(((x-795*scale)/(265*scale))**2+((y-795*scale)/(265*scale))**2)*.9)
shine = np.clip((spot1+spot2)*outer*.9,0,1)
new = np.clip(new+(235-new)*shine[:,:,None],0,255).astype("uint8")
Image.fromarray(new,"RGB").save(OUT/"maybank-liquid-glass-2048.png",optimize=True)
Image.fromarray(new,"RGB").resize((1024,1024),Image.Resampling.LANCZOS).save(OUT/"maybank-liquid-glass-1024.png",optimize=True)
print("Created 1024 and 2048 PNG.")
