# Matera Digital Boutique · gallery and implementation handoff

1. Keep this folder next to the approved candidate asset folder inside the ZIP/repository version.
2. Build the manifest from actual files, then open `index.html` directly in a browser:
   ```bash
   python3 integration/build_gallery_manifest.py . --json integration/gallery-manifest.json
   ```
   You can scope a scan to a sibling folder (e.g. `assets`) or add `--include identity photography storefront social media-motion print`. The integration folder never scans itself.
3. When optional labels, approval status or motion posters are available, add `--metadata asset-labels.json`. That JSON object is keyed by exact paths relative to the scanned asset directory. Records can specify `title`, `family`, `status`, `tone: "light"` for an ivory mark, and `poster` for an existing still asset path. Example:
   ```json
   {"identity/mdb-wordmark-ivory.png":{"title":"Ivory wordmark","family":"Identity","tone":"light","status":"Candidate"}}
   ```
4. Read [migration matrix](docs/MIGRATION.md) and [release/QA checklist](docs/QA.md). Keep the original library unchanged until the approved release path. All exports are candidates unless the manifest says otherwise.

This gallery intentionally ships an empty default manifest until generated against an actual asset directory. It reads local `gallery-manifest.js` instead of fetching JSON because browsers usually restrict local file fetches. The optional JSON copy is for checksum/automation use, not needed at runtime. No network calls.
