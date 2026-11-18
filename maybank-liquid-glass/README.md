# Maybank Black Liquid Glass Icon

Preserves the uploaded Maybank tiger and lettering pixels. Adds subtle highlights *outside* the top-left and bottom-right rounded tile edge, and a low-key gradient to white artwork.

## Required source image
Upload the original user-provided Maybank black icon named `maybank-original.webp` to `maybank-liquid-glass/assets/` (file is in the project ZIP). The source file is not yet in this branch.

## Build
Run `pip install pillow numpy && python maybank-liquid-glass/build.py` from repository root, or select **Actions > Build Maybank Glass Icon > Run workflow** after uploading the original asset. Download the generated 1024/2048 PNG artifact.

Works as a static visual on iOS 18; not native dynamic Liquid Glass. The existing shortcut-icons library is untouched.
