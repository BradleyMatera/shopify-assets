# Format and size guide

All sizes are pixel dimensions, not print-quality claims. Filenames contain exact dimensions. The JSON/CSV registry is authoritative for source size and resampling.

| Asset | Delivered sizes | Best default |
|---|---|---|
| Lifestyle hero | Native 1672×941; 1600×900, 1280×720, 960×540, 640×360; additional proportional widths | 1600×900 WebP with smaller srcset variants |
| Mobile art direction | 640×853, 480×640, 360×480 | Portrait WebP, chosen separately from desktop |
| Requested enlarged hero/crops | 1920×1080, 2400×1350, 1080×1080, 1080×1350, 1080×1920 | Explicitly resampled; do not mistake for new detail |
| Department crops | Native dimensions vary; 64/96/128 square thumbnails when source permits | Native WebP for small editorial slots |
| Enlarged department tiles | 512×512 and 1024×1024 | Marked resampled; not suitable as new high-resolution photographs |
| Campaign compositions | 1200×630, 1080×1080, 1080×1350, 1080×1920, 1200×600, 1920×800 | JPG for email/social; live HTML text on storefront |
| Transparent horizontal/stacked identity | Widths 300, 600, 1200, 2400; height follows proportions | SVG for crisp scaling, PNG for upload compatibility |
| Transparent brand mark | Widths 64, 128, 256, 512, 1024 | SVG or transparent PNG |
| App/favicons | 16, 32, 48, 64, 128, 180, 192, 256, 512 square; ICO contains 16–64 | ICO for legacy/favicon; PNG for app/touch icons |
| Utility icons | SVG at any scale; PNG 24, 48, 96 square | 48px PNG displayed at 24 CSS pixels, or inline SVG |
| Backgrounds | Native crops; soft 640×256, 1280×512, 1920×768 canvases | WebP; these are not seamless repeats |
| Motion | Desktop 1280×720; portrait 480×640; atrium 492×352; brand 960×320 | MP4/WebM with poster; GIF only when needed |

PNG preserves transparency and sharp graphics. JPG is opaque and is intended for photographic content. WebP is supplied for lighter web delivery. AVIF is supplied for selected photographic assets, with fallbacks. SVG contains functional icon/identity paths, not the rejected generic campaign illustrations. GIF has a limited palette and visibly lower fidelity than MP4/WebM; do not use a GIF as the highest-quality homepage film.

Video loops are silent, H.264 MP4 / VP9 WebM. GIFs are smaller-width loops at 10 fps. Posters are available in PNG, JPG and WebP. Motion is derived from still images, not filmed action. Do not force autoplay on visitors who request reduced motion.

A single file cannot work identically in every environment. Use the supplied format suited to the target: website, Shopify, email or social upload. No PSD/AI/print-resolution masters or proprietary source files are claimed.
