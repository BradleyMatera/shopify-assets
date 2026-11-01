# Validation report

Release: November 1, 2026

## File checks
- Registered media exports: 1302.
- Missing/corrupted/dimension-mismatched registered assets: **0**.
- Static example/gallery file references checked: 29.
- All PNG/JPG/WebP/AVIF/GIF/ICO files opened and verified.
- Transparent identity and utility PNGs contain alpha channels.
- All four GIF exports contain multiple frames.
- All SVGs parsed as XML.
- All eight video files were inspected with ffprobe: H.264 MP4 / VP9 WebM; correct dimensions; no audio track; expected 4- or 6-second durations.
- Every individual registered file is below 20 MB and every raster image is below 20 megapixels. The largest file is 3.96 MB.
- No font binaries are included.

## Gallery checks
- Working-library view: 133 asset groups.
- Search filtered the library successfully.
- Motion and GIF filters each return 4 loop assets.
- No JavaScript runtime errors or broken loaded preview images.
- No horizontal overflow at 1440px desktop or 390px mobile viewport width.
- Browser rendering/interaction tests used an in-memory copy with local images embedded as data URLs because the environment blocks direct file:// and localhost navigation. Separate filesystem validation checked the shipped relative paths. No claim is made that a remote GitHub Pages deployment was tested.

## Visual inspection
The package preview, desktop gallery, principal photographic crops, transparency and identity/icon samples were inspected. Crops with text fragments or incorrect subjects were adjusted. Small alternate crops and reference boards still require individual brand/merchandising review.

## Shopify limitation
The included Liquid section's schema JSON was structurally checked. It was not installed, compiled in the user's theme or tested against the live Shopify store. No store settings or products were changed.

## Source resolution
Enlarged exports are explicitly marked. This report is not certification of original high-resolution category photography, product accuracy, trademark clearance or universal client compatibility.
