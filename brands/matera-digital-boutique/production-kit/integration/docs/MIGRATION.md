# Replace the mall brand kit without breaking Shopify

**Candidate only.** The goal is a smaller, trustworthy catalog with a distinctive visual system, not to reproduce every legacy crop. New assets belong under a distinct Boutique path. The current storefront, old package, history, and release remain intact until a separately authorized cutover. This matrix is complete by legacy family; it does not assert each replacement has been produced or approved.

## Verified old package and dependencies

- [Asset repository](https://github.com/BradleyMatera/shopify-assets), default `main`, verified baseline `423d08a557d6c8966d00a08ef20106f263bf2328`; earlier 273 assets in `assets/` and complete package in `complete-library/`.
- [Complete package verification](https://github.com/BradleyMatera/shopify-assets/blob/main/production/complete-library-verification.json): 1,323 archived files, of which 1,302 are media exports; 1,322 original checksum entries, 186,141,158-byte original ZIP SHA-256 `d2f5f5c4828d3e3876995779ce6e58791f4369ada66682941846eb3444891915`. Preserve [release](https://github.com/BradleyMatera/shopify-assets/releases/tag/complete-asset-pack-2026-11-01), manifests, raw paths, and links unchanged.
- [Legacy full export registry](https://github.com/BradleyMatera/shopify-assets/blob/main/complete-library/asset-manifest.csv) and [earlier checksums](https://github.com/BradleyMatera/shopify-assets/blob/main/production/SHA256SUMS.txt). Counts below are files, not unique designs or validated product photographs.
- [Initial Boutique candidate branch](https://github.com/BradleyMatera/shopify-assets/tree/brand/matera-digital-boutique-v1/brands/matera-digital-boutique). Retain its identity study as history. A subsequent premium library belongs in a new version or a new candidate branch; do not rewrite published Git history or upload generated assets to Shopify from this package.
- Verified Shopify live theme ID `189946822884`, **Real Mall - VERIFIED locale repair Nov 4**. Historical `189786620132` is unpublished. Library was at 20 themes on the prior read. Recheck role and capacity immediately before any later write.
- Two verified byte matches demonstrate provenance, not a runtime GitHub dependency: theme `assets/rma-library-loft-desktop-640.webp` matches repo `complete-library/assets/hero/lifestyle-loft/responsive/lifestyle-loft-desktop-640x360.webp`; theme `assets/rma-library-wordmark-ivory.png` matches repo `complete-library/assets/brand/png/ivory/wordmark-horizontal-ivory-600x103.png`. The 21 brand-relevant theme files inspected use Shopify-local media, not GitHub raw URLs. Do not delete the old Shopify-hosted copies.
- [Historical storefront composition](https://github.com/BradleyMatera/shopify-assets/blob/main/preview/storefront.html) contains twelve links to the old customer host (home, cart, nine collections, arrivals). Keep historical preview clearly labeled; preserve matching guide/product URLs and do not use this page as a Boutique demo.

## Complete library: family-by-family disposition

| Legacy group | Files | Boutique replacement / disposition | Acceptance and integration |
| --- | ---: | --- | --- |
| `assets/brand` | 73 | Replace visible mall wordmarks, lockups, mark, avatars, and favicon with one identity system. Retain mall originals only as historical. | Primary horizontal, compact/stacked, light/dark/one-color, transparent large raster, narrow mobile, square avatar and multi-size favicon. No old name, font licensing assumption, or photographic texture baked into wordmark. |
| `assets/hero` | 72 | Replace atrium and loft with non-product Boutique editorial direction or exact supplier photography after clearance. Reuse safe responsive layout pattern, not old imagery. | Different desktop/mobile art direction and crop; no simulated premises or exact product claims. WebP and fallback where appropriate, responsive source widths and sizing, no autoplay requirement. |
| `assets/departments` | 259 | Retire old mall wings. Create only covers for the curated live collections; hold art for any unverified collection. | Never exhibit a product-shaped illustration as a SKU. Link only to a curated in-stock collection, not empty or archived sections. Preview at 375 px and desk-width. |
| `assets/alternate-small-crops` | 162 | Keep as archival source only. Do not bulk migrate or upscale low-detail mall crops. | New alternates need purpose, native source dimensions, ratio list, and file-size gate; label resampled derivatives. |
| `assets/backgrounds` | 108 | Rebuild a small restrained paper/pine/linen/background family as CSS tokens and a few optimized optional textures. | Test contrast on patterned surfaces and provide a flat color fallback. Avoid heavy hero overlays and backgrounds at mobile LCP. |
| `assets/icons` | 416 | Replace legacy utility styling with coherent small icon system. Reuse familiar pictograms only if the implementation is owned or licensed and matches Boutique stroke. | Prefer 24 px SVG geometry with 16/24/32 visual QA, accessible labels on controls and decorative images hidden as appropriate. Shopify native cart/search icons should not be replaced unless needed. |
| `assets/campaigns` | 54 | Retire old creative as approved history. Build Boutique campaign and guide formats from proven offers rather than making 54 new promotions. | 1200×630, 1080×1350, 1080×1920, clear safe zones, readable CTA and seller identity. No unverified price, claims, arrival, discount, or endorsement. Only authorized pages/placements. |
| `assets/editorial` | 12 | Build Boutique guide/announcement visuals around task or category, with supplier-approved product photo only when precise. | Useful alt text or empty alt for decorative crops; no text-only image dependence; original source and rights recorded. |
| `assets/motion` | 24 | Replace mall tours/atrium loops with Boutique ident and restrained motion if used; otherwise poster-only. | Silent MP4/WebM, static poster, no autoplay by default, respects reduction preference, no invented filmed footage, small payload. Animated stills remain labeled honestly. |
| `reference-only/boards` | 18 | Preserve reference-only, never import as a Shopify Media or campaign export. | Review for obsolete identity, claims, photo rights, and provenance; retain clear reference label. |
| `reference-only/separated-panels` | 104 | Preserve reference-only, never promote artwork just because it was separated or enlarged. | No policy, product or shipping copy taken from concept boards without fresh primary proof. |

## Earlier standalone batch: remaining use cases

| Legacy folder | Files | Boutique action |
| --- | ---: | --- |
| `backgrounds` | 12 | Replace with flexible tokens and restrained optional texture set; flat fallback. |
| `brand` | 17 | Replace with Boutique primary, secondary, dark, light, compact, social and favicon variants. |
| `campaigns` | 2 | Archive early promo creative; build separate Boutique signed-off campaign formats. |
| `email` | 1 | Build a Shopify-friendly email header and text-only fallback. Test desktop, mobile, images-off and dark mode. |
| `hero` | 14 | Old atrium crops and fallback are historical only; true responsive Boutique story and safe framing. |
| `icons` | 216 | Replace with one readable, consistent collection of frequently used symbols. Count variants honestly. |
| `masters` | 1 | Preserve original Shopify CDN source in the legacy provenance record. New masters include rights, factual limits, size, checksum. |
| `motion` | 7 | Keep archival. Boutique motion versions and static fallback, optional only. |
| `social` | 3 | Replace sale-era profile/banners with offline Boutique avatar and channel crops. No login, account, ad, or publish action. |

## Exact Shopify reference and handoff

| Source | Existing verified reference | Draft replacement or test |
| --- | --- | --- |
| `layout/theme.liquid` | `rma-library-favicon.png` | Add a distinct `mdb-favicon-32.png` or tested scalable reference. Refresh in signed-out mobile/browser tab. |
| `sections/matera-footer.liquid` | `rma-library-wordmark-ivory.png` | Set reversed mark on verified pine surface, preserve policy/help links, verify alt name. |
| `sections/rma-editorial-hero.liquid` | `rma-library-loft-mobile-* / desktop-* / loft-loop.mp4` | Replace section in draft; use responsive images or editor-selectable asset, poster and static route. Do not rename old section files in place. |
| `sections/rma-department-grid.liquid` | Seven mall department photos, download crop, mall mark | Replace old directory UI with a compact collection edit, remove unsupported shelf paths and images. |
| `templates/index.json` | `shopify://shop_images/real-mall-keyboard-layout-65-75-96.webp`; hard-coded old keyboard guide URL | Keep the guide only if useful and current, use approved Shopify Files media and a relative route. Verify new home does not expose unrelated products. |
| Native live home | Ten enabled modules; `matera-mall` legacy section disabled | Audit actual enabled hero, department grid, shelves, media, help, and directory. Editing disabled legacy section is not sufficient. |
| Native site resources | Menus, collections, pages, policies, Checkout brand, email, Shop and Google/Meta/Pinterest assets are not bundled into a theme backup | Snapshot individually; stage new menus under separate handles, keep source-policy words and clear product facts, gate all releases separately. |

The draft sample guidance does not imply a Shopify direct-store file update. Logo and product graphics can be served using Shopify Files or per-theme assets as appropriate; do not hotlink GitHub raw URLs into Shopify. Use a local brand branch, a prepared asset manifest, and approved filenames on the unpublished draft. [Shopify theme architecture](https://shopify.dev/docs/storefronts/themes/architecture) · [Theme backups](https://help.shopify.com/en/manual/online-store/themes/managing-themes/duplicating-themes).

### Integration sequence

1. Capture branch HEAD, hash manifest and Shopify theme role. Preserve current Shopify setup and old logo/favicons/art until rollback is unnecessary. If the 20-slot cap remains, separately back up a verified stale draft before any approved reuse; no delete to make space without authorization.
2. Add all candidates under a new repository version, preserve old gallery/release. Verify local gallery totals, preview/decode, accessible contrast, size/artifact path, case sensitivity, and origin for each asset. Store media filenames as short lowercase ASCII with Boutique prefix and version if multiple variants coexist.
3. Draft theme maps brand identity, offsite preview proof, responsive media, alt copy, conditional optional motion, and new menus. Switch only to verified product imagery supplied for that exact SKU; retain semantic headings and useful descriptions.
4. With catalog and commerce acceptance complete, acquire the final go/no-go. Record exact theme ID, source version, changed shared resources, and rollback plan. Do not change any working Shopify, payment, supplier, or channel setting as a side effect of gallery/repo staging.
5. Rehearse reversion without publishing: restoration order is previous theme + any previous shared settings per snapshot, including published collections and supplier-safe availability, not a blanket return to the old mall lineup.
