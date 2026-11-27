# Matera Digital Boutique | Identity

A custom interlocked MD emblem and an editorial serif wordmark. The joined right stroke makes the letters a single visual form rather than two unrelated initials. The warm paper ground and pine ink keep it understated; rust and apricot distinguish editorial labels without turning the main name into a two-color headline.

**Production-ready art, not published brand changes.** The identity contains no real-product images, vendor marks, launch dates, stock, pricing, shipping claims or sales assertions.

## Pick the right file

| Use | Deliverable | Placement |
|---|---|---|
| Light storefront header | `shopify/mdb-horizontal-light-440x102.png` | Transparent; display at 220 × 51 CSS px, a 2× image. Set photo/primary fill separately. |
| Pine or near-black header | `shopify/mdb-horizontal-dark-440x102.png` | Transparent; ivory text and apricot BOUTIQUE. |
| Narrow mobile area | `shopify/mdb-wordmark-light-360x89.png` / `-dark-360x89.png` | Display around 180px wide. Use the version matching its background. |
| Cover, editorial, opening card | `masters/mdb-stacked-light.svg` or `-dark.svg` | Use above 220 CSS px wide; center with visible clear space. PNG counterparts are available at 840 × 504. |
| Large-format print / emboss | `masters/mdb-horizontal-mono-black.svg` / `-mono-white.svg` | Transparent one-color outline. Confirm the vendor's color and ink workflow; SVG is RGB, not print-separation output. |
| Social profile | `social/mdb-avatar-pine-1080x1080.png` | Default for Facebook, Instagram, Pinterest and any proven brand-owned social surface. The central mark and keyline survive a round mask. Ivory is the alternate. |
| Tiny active tab | `icons/favicon.ico` or `icons/favicon-16x16.png` and `favicon-32x32.png` | ICO embeds the real 16, 32, 48, 64 frames. Use the optical correction supplied at 16/32, not a reduction of the full lockup. |
| SVG favicon support | `icons/favicon.svg` | Vector browser icon. Prefer the explicit optical 16/32 PNG or ICO entries as fallbacks. |
| Apple Home Screen / PWA | `icons/apple-touch-icon-180x180.png`, `icon-192x192.png`, `icon-512x512.png`, `icon-maskable-512x512.png` | Solid pine edge-to-edge, not the transparent avatar/SVG. Logo is contained inside the icon mask safe zone. |

- Light means the canvas behind it is light. Dark means the canvas behind it is dark. Masters do not carry a background unless it is an avatar or app tile.
- Keep at least half the monogram's displayed cap height clear of other content around its visual bounds. For regular use follow the transparent bounds in the masters. Do not squeeze horizontal as a substitute for mobile; switch to wordmark-only at 180–219px or use monogram-only below 180px.
- Keep orientation and proportions, no glow, shadow, text replacement or recoloring beyond the sanctioned variants. For readability use the name as live nearby text if logo must be displayed below the minimum size.
- Use alt text exactly “Matera Digital Boutique” when this image is the home link. Use empty alt when adjacent real text already gives the accessible name.
- Don't pair rust with pine or apricot with ivory for small meaningful text. Verified contrast: pine on ivory 13.56:1, rust on ivory 5.33:1, apricot on pine 7.61:1. For web UI use existing site text styles and focus treatment, not an image of text.

## Source and use

`masters/` holds editable, grouped-by-contour SVG art. The MD monogram geometry is custom path data. The wordmark outlines are based on Noto Serif Regular (SIL OFL 1.1; Google LLC; Monotype Imaging Inc.) and the descriptor on Open Sans Semibold (Apache 2.0; Google Corporation; Ascender Corporation). Their Debian package notices and Apache text are in `source/`. No font binaries or remote dependencies are included in the deployed SVGs. For independent brand typography install and license the actual fonts separately.

To reproduce the exports with the same fonts on Debian/Ubuntu:

```sh
python source/build_identity.py
python source/verify_identity.py
```

Requires Python 3, Pillow, fontTools, Inkscape, Noto Serif and Open Sans. Override source font paths with `MDB_SERIF`/`MDB_SANS` only with matching font builds; supplying different builds can alter alignment. The path masters are the authoritative use-ready assets. `identity-proof.jpg` demonstrates the file set in context. The QA script verifies actual PNG dimensions, SVG portability, transparent border/absence of clipping, contrast calculations, and exact ICO frames; it also produces the native-size proof and circle crop.

No website upload, account rename, domain or listing was performed by producing these assets.
