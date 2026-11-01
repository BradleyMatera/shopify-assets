# Integration

## Static site or framework
Serve the repository contents as static files. Use the responsive example in `example.html`. Paths are relative, so they work under a repository subpath. The gallery itself uses no build process and no external services.

## Shopify
The supplied `.liquid` file is an optional image hero section. It does not depend on GitHub raw URLs. Upload the chosen PNG/JPG/WebP files to Shopify first, create `sections/rma-editorial-hero.liquid` in an unpublished theme, then add "RMA editorial hero" in the theme editor. Select desktop and mobile images, edit the live text, and set a real destination. No collection handles are guessed. Preview the result before publication.

This is not a complete theme ZIP, and the whole asset ZIP must not be uploaded as a theme. The optional section has been structurally checked but not exercised against your connected Shopify theme. The asset gallery and local media have been tested separately.

## Accessibility
Keep storefront headings/buttons as HTML. Use meaningful alt text for informative images and empty alt text for decorative ones. UI icons need labels on the control rather than ambiguous standalone images. Offer static posters instead of motion for reduced-motion visitors. Video examples use controls and do not autoplay.
