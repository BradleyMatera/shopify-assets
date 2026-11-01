# Shopify handoff

The repository contains actual binary files plus optional Shopify section code. No live theme has been changed.

1. Duplicate the current theme in the actual connected store; do not assume a theme ID from another shop.
2. Copy the contents of `theme/assets`, `theme/sections`, and `theme/snippets` into the matching directories in that unpublished theme. The build creates uniquely named flat media assets for Shopify.
3. Add RMA editorial hero and RMA departments in the theme editor. Choose the existing collections listed in `production/collections.json`; do not rename or recreate them.
4. The campaign images are editorial AI imagery, not photographs of stocked SKUs. Preserve all real supplier product photos and product data.
5. Video defaults to off, loads only after a visitor presses Play, and respects reduced-motion and data-saving preferences. These files are camera-motion loops from stills, not live-action footage.
6. Verify all theme media URLs, font choices, image crops, keyboard navigation, mobile search, collection filtering, cart and checkout before publishing.

The packaged sections have not been installed or tested inside the live Shopify theme. Preview files are HTML/CSS visual demonstrations; they are not a substitute for checkout QA.

Raw GitHub URLs are not a production image CDN. Uploaded theme assets are served by Shopify.
