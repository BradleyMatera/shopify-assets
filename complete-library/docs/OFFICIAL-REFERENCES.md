# Technical references checked for this package

Checked November 1, 2026. These sources document upload/format and template behavior, not approval of the generated assets.

- GitHub, Adding a file to a repository: https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository
- Shopify, Uploading and managing files: https://help.shopify.com/en/manual/shopify-admin/productivity-tools/file-uploads
- Shopify, Uploading images: https://help.shopify.com/en/manual/online-store/images/theme-images
- Shopify Liquid, image_tag: https://shopify.dev/docs/api/liquid/filters/image_tag
- Shopify Liquid, video_tag: https://shopify.dev/docs/api/liquid/filters/video_tag
- Shopify theme input settings: https://shopify.dev/docs/storefronts/themes/architecture/settings/input-settings

The GitHub web uploader allows 100 files per upload and 25 MiB per file. Shopify's pages list different image-resolution limits for different contexts; this package keeps its individual images below 20 megapixels and 20 MB, so it does not depend on the more generous limits. AVIF delivery should use a JPG/WebP fallback; the default Shopify upload examples use PNG/JPG/WebP.
