# Matera Digital Boutique | Public brand re-audit
November 27, 2026. Read-only public HTML, no browser session or live edits. All seven exact final-primary-domain URLs in the list below returned HTTP 200. Asset proof shows the actual pixels, not just file names.

## Verified now, in release order

| Priority / exact route | Customer-visible evidence | Safe action and asset |
|---|---|---|
| 1. [/pages/about](https://materadigitalboutique.myshopify.com/pages/about) | H1 “About Matera Digital”; main text still says “an online mall” and lists the broad mall departments; no main image. | Replace body and page title with the About draft below. No image needed. Preserve the contact route. |
| 2. [/pages/departments](https://materadigitalboutique.myshopify.com/pages/departments) | “Shop shipped products at Real Mall of America” and “Mall Directory”; 10 directory tiles. The “Digital Downloads / Stocking soon” tile uses `rma-library-mark.webp`, pixel-verified old gold double-peak Mall logo. Home & Kitchen already has Boutique art. | Replace intro and directory navigation together. Retire the empty downloads tile rather than merely replacing its logo. Keep the existing Boutique Home & Kitchen graphic or use the narrower editorial card `storefront/mdb-kitchen-editorial-card-900.webp`. Non-Boutique supplier/category photographs are not demonstrated to carry the Mall name. Do not replace supplier media without a separate exact product review. |
| 3. [/pages/mall-directory](https://materadigitalboutique.myshopify.com/pages/mall-directory) | Title “Mall Directory,” intro “Welcome to the mall. Pick a wing…,” and broad product-wing links. No main graphic. Global navigation sitewide still links “Mall Directory” and “More Stores” to this page in desktop/mobile DOM. | Keep the legacy path as a helpful text-first landing page, change its public title to “Explore the Boutique,” then remove/replace duplicate global navigation. This is safer than removing it before verifying link coverage. No image needed. |
| 4. [/pages/buying-guide-library](https://materadigitalboutique.myshopify.com/pages/buying-guide-library) | “Buying Guide Library”; no old public text or body image. Contains broad legacy archives by category plus policy links. | Keep title and route, add optional short featured editorial lead below, and retain searchable archive. Do not present archive links as in-stock merchandise. |
| 5. [Keyboard layout guide](https://materadigitalboutique.myshopify.com/blogs/news/60-65-75-or-full-size-choose-a-keyboard-layout) | Guide cover visibly says “MATERA DIGITAL BOUTIQUE / BUYING GUIDE” in `mdb-keyboard-layout-share-1200.jpg`. No legacy wording in visible article body. | Keep the new cover, alt and comparison. Do not use the legacy keyboard graphic that bakes in the old name. Existing direct product links are a separate exact inventory and availability review; do not revive keyboard promotion through this cleanup. |
| 6. [Kitchen counter guide](https://materadigitalboutique.myshopify.com/blogs/news/clear-a-crowded-kitchen-counter) | Current `mdb-kitchen-editorial-share-1200.jpg` correctly shows a neutral illustrative counter. No legacy body branding. | Keep image/alt; current two direct product links require separate eligibility proof before using the article in a sales offer. |
| 7. [Pantry planning guide](https://materadigitalboutique.myshopify.com/blogs/news/measure-before-you-buy-pantry-container-planning) | No old visible body text, artwork or direct product link. | Keep as an educational destination. If a card is useful, use `mdb-kitchen-editorial-card-900.webp` with illustrative descriptive alt. |

**Search/shared metadata is separate:** Prior batch confirmed 51 checked articles still label the structured-data author “Real Mall of America”; sampled fresh guides still show this in source. It is not rendered as body copy. Inspect theme/Shopify blog author source separately and maintain honest attribution. Avoid changing an account identity or purging existing articles simply to remove historic wording.

## Exact replacement draft

### About Matera Digital Boutique
```html
<p>Matera Digital Boutique is an online storefront operated by Matera Digital. Start with practical ideas for your home and kitchen, or browse our buying guides before you choose.</p>
<p>Check the product page for the selected option and availability. Shipping options, charges and any delivery estimates are shown at checkout. Some physical items are fulfilled by partner suppliers and may ship separately.</p>
<p><a href="/pages/buying-guide-library">Explore the buying guides</a> or <a href="/pages/contact">contact us</a> with a product question or for help with an order.</p>
```

### Departments (keep the existing /pages/departments path)
Public title: **Explore the Boutique**. If the legacy grid renders from the theme as an extra section, editing the page intro alone will not remove it. Verify which live page template owns the grid; replace or remove that exact module while retaining stable anchor routes.
```html
<p>Start with what you want to make easier: setting up a kitchen, organizing a space, or choosing an everyday essential.</p>
<p><a href="/pages/buying-guide-library">Browse the buying guides</a> for practical checks before you shop. Check each item’s product page for its options and availability; shipping options and any delivery estimates are shown at checkout.</p>
```
A retail card labeled **Home &amp; Kitchen** can link to the existing collection only after the current store cutover verifies its shopper-visible contents. For a guide-first module now, use **Kitchen planning** → `/blogs/news/measure-before-you-buy-pantry-container-planning` with the illustrative crop instead. Do not relabel uncleared catalog links as vetted collections.

### Legacy Mall Directory route
Public title: **Browse Matera Digital Boutique**.
```html
<p>Start with our <a href="/pages/buying-guide-library">Buying Guide Library</a> for practical advice, or <a href="/pages/departments">explore the Boutique</a>.</p>
<p>Looking for help with a product or order? <a href="/pages/contact">Contact us</a>.</p>
```
Global navigation: replace “Mall Directory” and “More Stores” links with one **Buying Guides** link to `/pages/buying-guide-library`, unless that link is already present. For a separate orientation link use **Explore** → `/pages/departments`; no duplicate links from nested desktop/mobile menus.

### Optional featured Buying Guide Library intro
```html
<p>Practical checks for choosing what fits. Start with <a href="/blogs/news/measure-before-you-buy-pantry-container-planning">measuring for pantry storage</a> or <a href="/blogs/news/a-kitchen-drawer-system-that-starts-with-what-you-use">planning a kitchen drawer around what you actually use</a>. Browse the full guide archive below.</p>
```

**Before/after:** Preserve current page bodies and menu values for rollback. Verify visitor page title, main copy, responsive navigation and footer links; no broken '/pages/mall-directory' bookmarks. Confirm non-legacy public render from the primary domain. Keep privacy/legal entity names, payments, policy terms and supplier records intact. Visual evidence: `[local build reference omitted]` shows the current keyboard cover, neutral kitchen cover and legacy gold department mark.
