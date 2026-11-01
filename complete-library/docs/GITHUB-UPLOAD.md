# Uploading this pack

## Recommended: GitHub Desktop
Clone BradleyMatera/shopify-assets, open its local folder, and copy the extracted archive contents into that folder. Keep `assets/`, `reference-only/`, `docs/`, `integration/`, `sources/`, `tools/`, the gallery HTML and the registries together. Review replacements, commit and push. This package does not delete older remote files automatically.

## GitHub website
GitHub limits each browser upload to 100 files and each individual file to 25 MiB. Use small asset subfolders, or use the separately provided browser-batch ZIP. Each `batch-NN` contains at most 95 files while retaining their final paths. Open the target repository root, choose Add file > Upload files, and drag the **contents inside** one batch folder, not the enclosing batch folder. Commit, then repeat for the next batch. Folder preservation on drag-and-drop depends on the browser; GitHub Desktop avoids that issue.

Do not upload just the archive expecting GitHub to extract it. Do not put `batch-NN` in the final repository paths. Do not enable GitHub Pages as a substitute for serving Shopify product images; store live Shopify media in Shopify.

## Gallery
Open `START-HERE.html` locally. For online viewing, GitHub Pages can serve `index.html` from the repository root after you configure it in repository settings. No account settings were changed by creating this ZIP.
