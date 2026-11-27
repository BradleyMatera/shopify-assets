# Matera Digital Boutique | Print & customer operations

## Print master files

| File | Finished size | Specification |
|---|---|---|
| packing-insert-4x6-cmyk.pdf | 4 × 6 in, portrait | Two pages in order: thank-you front, general order/care back. Duplex on long edge; proof orientation. |
| round-seal-2in-cmyk.pdf | 2 in diameter | Square CMYK artwork with bleed; use the separate circular geometry guide. Confirm the printer’s die and cut-line layer requirements. |
| box-label-3x1.25-cmyk.pdf | 3 × 1.25 in | Single rectangular brand label. Not a shipping, regulatory, SKU/barcode or materials label. |

All print PDFs are vector-first, use embedded font subsets and process CMYK operators with explicit TrimBox and BleedBox. Allow 0.125 in bleed on every edge. Process colors are starting recipes, not a printer-specific ICC match; files are not certified PDF/X. Request a proof on your chosen material and ask the printer about required output intent, overprint settings and die tolerances. Do not place an order from the previews. The round seal SVG is **non-printing guide geometry**, not a color artwork layer. The box label and seal are for the outside of packaging, not food contact or safety sealing. Recommended stock: matte card or matte label after approval; not a purchase instruction.

The JPG is a screen preview. Screen color and stock are not proofs. The small triple arch is a typographic ornament, not the primary store logo.

**Packaging scope:** Send these files to a printer or include them in a parcel only for merchant-packed inventory, or when the relevant fulfillment partner has specifically accepted the packaging workflow. Do not imply that Shopify Collective suppliers add store-branded packaging. Before printing the insert, verify the actual public Contact link routes to an actively monitored mailbox. Do not add unverified claims about origin, certification, shipment or product care.

## Shopify email assets

- `email-header-pine-1200x260.png` and `email-header-ivory-1200x260.png` are RGB versions for web/email. Aim for 600 × 130 CSS px when displaying a banner, shrink to container width on mobile, and use alt text **Matera Digital Boutique**.
- In Shopify’s notification brand settings, the primary full wordmark is usually a better standard logo than the full-width banner. Use the banner only where a template has an appropriate header image slot. The standalone `email-header-text-fallback.html` is editable, live text with no tracking, font files, or image dependency.
- Do not replace order bodies or remove live order variables, unsubscribe/compliance links, attribution or accessible text. Verify desktop, mobile, image blocked and test email render. No notifications changed as part of this export.
- `customer-support-templates.md` contains four operator-reviewed drafts, not automatic replies. Never paste unresolved placeholders into a real reply.

## Source and preflight

`build-production.py` is editable using Python, ReportLab, Pillow, Noto Serif and Open Sans. Font binaries are not bundled. PDFs include required font subsets. The layout was reviewed in the rendered trim contact sheet. A PDF content check verified CMYK paint operations, exact trim and bleed geometry, text extraction, and no external image dependencies. Email PNGs are 1200 × 260 px. The preview JPEG represents the layouts, not a printer proof.
