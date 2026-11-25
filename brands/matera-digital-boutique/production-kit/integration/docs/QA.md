# Boutique asset acceptance and release checklist

Use this with the migration matrix. **A checked asset export does not approve the Shopify cutover, a product claim, an external channel post, or a legal designation.**

## Package completeness

- [ ] Root manifest states actual included families, format counts and known omissions. Legacy-only and rejected assets are visibly labeled, not mixed with Boutique candidates.
- [ ] Each record has exact relative file path, type, bytes, SHA-256, intended role, approval state and source/provenance. Missing dimensions are disclosed, not fabricated. Downloaded ZIP tests without errors.
- [ ] Primary, compact/stacked, dark, light, one-color, favicon, avatars, email header, desktop/mobile hero, collection/guide covers, social ratios, surfaces, utilities, optional motion and fallback each have a real export or explicit hold. Verify no duplicate named exports with different content and no claimed full kit based on placeholder drafts.
- [ ] Recipient can extract ZIP and open the landing entry in an ordinary browser without a build, sign-in, GitHub Pages, remote scripts, fonts, CDNs or trackers. Tabs, search, format/family filters, result counts, reset, show more, image labels and downloads work against actual local paths.
- [ ] Download filenames are meaningful and case-exact on a case-sensitive system; paths contain no hostnames, path traversal or root-relative URLs. Broken media is flagged visually, not replaced by mock output. Spot-check representative downloads by hash.

## Brand and media quality

| Asset | QA proof | Hold if |
| --- | --- | --- |
| SVG masters | XML parses; viewBox is tight; no external images/fonts, code/script tags, clip artifacts, or undisclosed paths; accessibility name; open on both light/dark | missing text/glyphs, font family substituted without approval, oversized exported empty space, unclear letterforms |
| PNG lockups and icons | True transparency checked on mid-tone surface; expected dimensions and legibility at 16/32/40 px and high-density export; circle-safe avatar at 128/512 px | halos, aliasing, cramped crop, redundant or microscopically small text |
| Editorial/collection art | Exact native/crop dimensions recorded; separate landscape/portrait composition QA, correct crop/safe zones, photo model/source and license disclosure; WebP and compatible fallback | generated art creates credibility claim or misrepresents an actual SKU, legacy mall still in frame, visibly interpolated weak source |
| Product images | Exact variant and supplier photo rights confirmed, clean alt text, label/product color matches, dimensions and sharpness satisfy channel | representative art is treated as the product, ambiguous version/color/size, touched-up model details, supplier channel restrictions |
| Social and campaign exports | Verify square and 4:5 and 9:16 when intended; no hidden overlays or rendering shifts; available assets and plain captions support humor without deception | unverified product, price, discount, testimonial, supplier association, ETA or shipping promise |
| Motion, when included | ffprobe confirms codec / duration / dimensions; silent track or source-rights checked; file opens and finishes; still frame fallback; manual playback; caption if spoken | autoplay on landing, visible motion flashes, no static rendering or mixed voice/audio evidence |
| Print/email, when included | Print format and safe margin tested; email images-off alt text, mobile alignment and dark mode fallback | mail clients obscure brand/message; artwork reused as policy guarantee |
| Palette and typography | Normal text ≥4.5:1, large ≥3:1, states readable on chosen backgrounds; visible keyboard focus; test line breaks/letter-spacing | typography fights wordmark, illegible dark version, clipping, meaningful message communicated only through color |

For the gallery itself, sample phone widths **320, 375, 430 px**, tablet **768 px**, desktop **1280+ px**; zoom **200%**; keyboard navigate the filters and downloads; verify reduce-motion behavior. Visual QA requires an actual browser screenshot or human viewing at each representative breakpoint; syntax and DOM mocks alone are not equivalent.

Suggested initial performance budgets to test on production: homepage initial hero ≤250 KiB mobile / ≤450 KiB desktop if feasible with acceptable visual detail; no required motion for first paint; lazy-load below fold; use responsive width sources and explicit image dimensions to avoid layout shift. These are proposed budgets, not measured performance.

## Draft Shopify acceptance

- [ ] Exact store, exact live theme ID, and a recoverable separate unpublished draft confirmed; tag/hash all materials. Native protections respected. No publish, domain, payment, inventory, credential or supplier action implied by this checklist.
- [ ] Brand name and marks are consistent across draft header/footer/favicon, offsite cards, mobile/desktop crops, checkout visuals, transactional emails and Shop logo staging. Plain description clarifies that selected products are physical if that is the actual assortment.
- [ ] Preview the newsletter/consent UI, support, Privacy / Refund / Shipping / Terms / Contact / Legal, real navigation and relative URLs. Existing account/order links remain valid under any later host decision.
- [ ] With exact cleared SKU/product ID verify signed-out homepage → collection → exact searchable variant → cart → checkout, availability and price, handheld sizes, shipping rates/return constraints; **do not place a real order or charge**. Confirm timestamp, geography and responsible owner on each proof. No unverified sibling variant remains purchasable because the hero branch is stocked.
- [ ] An unavailable/archived SKU cannot buy via old URL or channel, and only a relevant redirect where appropriate. No deletion of legacy asset or release, sweeps of existing account settings, or filename overwrites. Confirm tested rollback plan separately for shared resources and product/channel states.
- [ ] Candidate moves to a reviewed published version only after the owner authorizes that cutover. Verify live readback separately before changing ads, public stores, catalogs, or claiming completion.
