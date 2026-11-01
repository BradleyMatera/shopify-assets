# Real Mall of America — separated asset library

**Open `START-HERE.html` after extracting this ZIP.** The gallery runs locally without a build process, account, or server. Every card links to the actual exported files.

This release contains **1,302 media exports** in **275 asset groups**. Counts include formats, sizes and color variants, not that many unique photographs.

## What is inside
- Transparent wordmarks, stacked identity, brand marks, app icons and a multi-size favicon.
- A text-free lifestyle hero with desktop, portrait, square and story crops.
- 12 isolated department/detail photographs, native masters, thumbnails and clearly marked enlarged variants.
- 81 alternate small department crops from the supplied concept boards.
- Six decorative material/background crops and softened larger canvases.
- Three editorial campaigns in six layouts each, exported as PNG, JPG and WebP.
- 32 utility icons in champagne, ivory and ink; PNG at 24, 48 and 96 pixels; SVG and currentColor SVG.
- Four actual silent animated loops, each as MP4, WebM and GIF, with static posters.
- Nine full concept boards and 52 separated composed panels, all under `reference-only`.
- A JSON/CSV asset registry, format and source documentation, usage examples, Shopify section source, and a file-integrity check.

## Important source-quality distinction
Most supplied concept boards are only 1536 × 1024 pixels **for the entire board**. Their individual photographic tiles are much smaller. The full text-free lifestyle image is 1672 × 941. Cropping/exporting does not create missing photographic detail.

`native/`, `responsive/` and `thumbnails/` keep detail within the available source size. `resampled/` contains requested larger dimensions and is marked in filenames and the registry. Large campaign compositions and soft backgrounds also disclose their source resolution. These are not secretly described as 4K photography or print masters.

## Upload to GitHub
1. Extract this archive. Open your local clone of `BradleyMatera/shopify-assets` in GitHub Desktop.
2. Copy the **contents** of this folder into the repository root, preserving the folders. Review existing-file replacements before committing.
3. Commit and push. Do not upload just the ZIP expecting GitHub to unpack it.
4. To view the catalog online, configure GitHub Pages from the repository root; `index.html` is included. Pages is not enabled by this archive.

For browser uploads, GitHub permits at most 100 files in one upload and 25 MiB per individual file. Use small subfolders or the separately supplied browser-batch archive. Every individual file in this pack is below 25 MiB. GitHub Desktop is the simpler route for the whole library.

## Use on Shopify
Upload selected images/videos through Shopify and select them in theme settings. A GitHub commit does not install media into Shopify. Use PNG for transparent identity/icons; WebP/JPG for most photography; MP4 for broad video use. AVIF is included for custom web use, with JPG/WebP fallbacks. SVG utility icons can be used in theme assets or inline code; prefer PNG for a straightforward Files upload.

`integration/shopify/rma-editorial-hero.liquid` is a configurable section starter, not a complete theme. Add it to an unpublished theme, select the uploaded images, set real destinations and preview it. It has not been installed or tested against your live theme.

## Truth and merchandising
Use the generated photographs as editorial/category atmosphere, never as proof of the exact merchandise sold. Keep actual supplier product photography authoritative. Reference boards include invented prices, shipping statements, ratings, supplier claims, logos and UI details; they are clearly isolated from working assets. No free-shipping or supplier guarantee is embedded in the newly composited campaign exports. No affiliation or trademark clearance is asserted.

## Format inventory
- AVIF: 24
- GIF: 4
- ICO: 1
- JPG: 202
- MP4: 4
- PNG: 654
- SVG: 137
- WEBM: 4
- WEBP: 272

See `docs/FORMAT-AND-SIZE-GUIDE.md`, `docs/SOURCE-AND-QUALITY.md`, and `docs/OFFICIAL-REFERENCES.md`.
