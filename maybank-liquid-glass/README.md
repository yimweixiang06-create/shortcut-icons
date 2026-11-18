# Maybank Black Liquid Glass Icon

Generates an almost pure-black Maybank icon, keeping the existing tiger and wordmark geometry. The top-left and bottom-right highlights appear only **outside** the rounded square.

## Use GitHub Actions
1. Add the user-supplied original black Maybank image as `maybank-liquid-glass/assets/maybank-original.webp` on the `maybank-liquid-glass` branch.
2. Choose **Actions → Build Maybank Black Glass Icon → Run workflow**.
3. Download the `maybank-black-liquid-glass` artifact containing 1024 and 2048 PNGs.

Run locally with `pip install Pillow numpy && python maybank-liquid-glass/build.py`.

This is a static appearance for iOS 18, not native dynamic Liquid Glass.
