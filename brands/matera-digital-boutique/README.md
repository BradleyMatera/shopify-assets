# Matera Digital Boutique · identity candidate v1

Start with [preview.html](preview.html) (open locally for the rendered visual) or inspect the actual [ink wordmark](assets/wordmark-ink.svg), [ivory wordmark](assets/wordmark-ivory.svg) and [MD mark](assets/monogram.svg). This is a **candidate**, not a live Shopify theme or a legal-name clearance. No product photos, vendor imagery, web fonts, or third-party logo files are redistributed. The monogram geometry is original, and the wordmarks reference system fonts. Keep the pre-cutover website, branch, releases and historical audit resources intact.

## Design direction

A restrained identity for a small, carefully checked assortment of physical goods, not an everything store. Warm paper is the default canvas; pine carries the identity and primary buttons; clay is an editorial accent. Set headings in Georgia, body in the system sans stack. Avoid simulated storefronts, deal claims, fake ratings or delivery promises.

| Token | Color | Role |
| --- | --- | --- |
| Paper | `#FBF5EB` | light surfaces |
| Pine | `#20352C` | primary identity, dark surfaces |
| Clay | `#85523D` | accent on light |
| Apricot | `#E5BC9E` | accent on pine |
| Charcoal | `#222823` | general text |
| Linen | `#F1E7D7` | secondary surface |

Typography and colors are in [tokens.css](tokens.css). On narrow chrome use the square mark only alongside native text where legibility would be lost. Keep one quarter-mark of clear space around the icon. Do not put the ink logo on pine or the ivory logo on paper.

## Responsive export and usage

| Use | Candidate master | Suggested exports and checks |
| --- | --- | --- |
| Header / footer | Ink for light, ivory for pine | SVG in theme assets; transparent PNG at 580×112 and 1160×224 only if the consuming field needs raster. Check crop/undersize at 375 px navigation. |
| Favicon | Square monogram SVG | PNG 32×32 and ICO fallback if needed. At 16 px recheck recognizability. |
| Social profile / Shop logo | Square monogram SVG | PNG 512×512; center with clear space for circle crops. |
| Social and guide cards | Palette and caption layout | 1200×630, 1080×1350, 1080×1920. Use only cleared supplier imagery for exact products; no simulated inventory. |
| Homepage hero | No image approved in v1 | Add signed-off exact product or non-product editorial art later, cropped separately for phone and desktop. Use WebP/AVIF plus a fallback if needed. |

Suggested sizes are not pre-made raster exports. The candidate preview’s icon download generates a 512×512 PNG locally using the supplied original artwork. For production wordmark exports preserve the SVG master, render on a machine with Georgia installed, verify text width/letterfit, and use an outlined build only if the operator validates its font rights and geometry.

## Shopify cutover map

1. Back up the true live Shopify theme and shared resources. Add new namespaced `mdb-*` assets to an **unpublished** theme; never overwrite `rma-*` files in place.
2. `layout/theme.liquid`: replace the old favicon reference with a tested MDB export. `sections/matera-footer.liquid`: replace the old ivory wordmark with MDB on pine, and keep footer policies linked.
3. `sections/rma-editorial-hero.liquid` and `sections/rma-department-grid.liquid`: stop using mall footage, directory crops and legacy department messaging. Use the approved boutique layout and real approved imagery. Do not migrate the old loft hero by default.
4. `templates/index.json`: remove old-host hardcoding and old guide image from the new home unless still relevant; use relative guide/collection paths and only catalog candidates cleared for launch.
5. Review active brand settings, favicon, email sender visuals, checkout, Shop logo, social crop and merchant feeds separately. Theme file changes do not update those surfaces or publish anything.
6. Check the phone/desktop rendering, image loads/contrast, checkout, screen reader alternative text and old public path redirects before the live cutover. Roll back by republishing the prior theme and restoring recorded shared resources if needed.

## Legacy package

The original catalog remains under [complete-library](../../complete-library/START-HERE.html), with the [verified original release](https://github.com/BradleyMatera/shopify-assets/releases/tag/complete-asset-pack-2026-11-01) and its existing checksums intact. The [old storefront composition](../../preview/storefront.html) is a historical view with live old-host/shop links; do not use it as the boutique’s launch preview. A GitHub commit does not install or publish these files to Shopify.
