"""Generate a black Maybank icon from its original artwork with a fine outside rim."""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "assets/maybank-original.webp"
OUT = HERE / "output"
OUT.mkdir(parents=True, exist_ok=True)
SIZE = 2048
if not SOURCE.exists():
    raise SystemExit("Missing assets/maybank-original.webp: upload the user-supplied original.")

src = Image.open(SOURCE).convert("RGB").resize((SIZE, SIZE), Image.Resampling.LANCZOS)
p = np.asarray(src, dtype=np.float32)
yy, xx = np.mgrid[:SIZE, :SIZE]
scale = SIZE / 980
shape = Image.new("L", (SIZE, SIZE), 0)
ImageDraw.Draw(shape).rounded_rectangle(
    tuple(round(v * scale) for v in (91, 91, 889, 889)),
    radius=round(183 * scale), fill=255
)
mask = np.asarray(shape, dtype=np.float32) / 255
brightness = np.max(p, axis=2) / 255
white = np.clip((brightness - .18) / .72, 0, 1) * mask
white_strength = .94 - .045 * yy / SIZE
canvas = np.zeros((SIZE, SIZE, 3), dtype=np.float32)
canvas[:] = (8, 8, 9)
canvas = canvas * (1 - white[..., None]) + 255 * white[..., None] * white_strength[..., None]
canvas *= mask[..., None]

# Only external reflection, never a large glow in the dark interior.
blurred = np.asarray(shape.filter(ImageFilter.GaussianBlur(10 * scale)), dtype=np.float32) / 255
outside = np.maximum(blurred - mask, 0)
upper = np.exp(-.5 * (((xx - 184 * scale) / (290 * scale))**2 + ((yy - 174 * scale) / (260 * scale))**2))
lower = np.exp(-.5 * (((xx - 805 * scale) / (290 * scale))**2 + ((yy - 807 * scale) / (260 * scale))**2))
shine = np.clip(outside * (upper + lower) * 1.5, 0, .44)
canvas += shine[..., None] * 205

result = Image.fromarray(np.clip(canvas, 0, 255).astype("uint8"), "RGB")
for size in (1024, 2048):
    icon = result if size == SIZE else result.resize((size, size), Image.Resampling.LANCZOS)
    path = OUT / f"maybank-black-liquid-glass-{size}.png"
    icon.save(path, optimize=True)
    print(f"Created {path}")
