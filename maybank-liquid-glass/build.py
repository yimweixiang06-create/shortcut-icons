"""Preserve original Maybank icon. Apply subtle reflections OUTSIDE only."""
from pathlib import Path
from PIL import Image, ImageFilter
import numpy as np

HERE = Path(__file__).resolve().parent
SRC = HERE / "assets/maybank-original.webp"
OUT = HERE / "output"
OUT.mkdir(parents=True, exist_ok=True)
original = Image.open(SRC).convert("RGB")
w, h = original.size
pixels = np.asarray(original).astype(np.float32)
gray = pixels.mean(axis=2)

# This threshold only locates the rounded tile; original image pixels are never recolored.
solid = Image.fromarray(((gray > 12).astype("uint8") * 255), "L")
solid = solid.filter(ImageFilter.MaxFilter(5))
shape = np.asarray(solid, dtype=np.float32) / 255.
dilated = solid.filter(ImageFilter.MaxFilter(7))
soft_dilation = np.asarray(dilated.filter(ImageFilter.GaussianBlur(1.0)), dtype=np.float32) / 255.
outside_only = np.maximum(soft_dilation - shape, 0)
yy, xx = np.mgrid[:h, :w]
sx, sy = w / 980, h / 980
upper_left = np.exp(-.5 * (((xx-165*sx)/(270*sx))**2 + ((yy-165*sy)/(270*sy))**2))
lower_right = np.exp(-.5 * (((xx-815*sx)/(270*sx))**2 + ((yy-815*sy)/(270*sy))**2))
shine = np.clip(outside_only * (upper_left + lower_right) * .58, 0, .5)
result = Image.fromarray(np.clip(pixels + (215-pixels)*shine[...,None],0,255).astype("uint8"), "RGB")
for size in (1024, 2048):
    result.resize((size,size), Image.Resampling.LANCZOS).save(
        OUT / f"maybank-black-liquid-glass-{size}.png", optimize=True)
