# TDM Electric Indonesia

Brand and catalogue site for TDM Electric products in the Indonesian market.

**Live:** https://tdme.pnglobalindo.com/ (Hostinger, the canonical address)

**Mirror:** https://mementosreap.github.io/tdm-electric-id/ (GitHub Pages). Keep this running: the Blibli listings load their product photos from `assets/img/products/` here.

Static HTML, CSS and JavaScript. No build step, no dependencies, no framework. Clone it and open `index.html`, or serve the folder.

## Pages

| File | Purpose |
|---|---|
| `index.html` | Home. Animated hero, categories, featured products, where to buy. |
| `produk.html` | Full catalogue with category filter, search and a detail view. |
| `tentang.html` | About the brand and our role. |
| `kontak.html` | Contact routes and how to request wholesale pricing. |

## Structure

```
assets/
  css/style.css    site styles
  css/hero.css     homepage hero, scoped under .hx
  js/products.js   product data — edit prices and specs here
  js/main.js       config, i18n, catalogue rendering, detail view
  js/hero.js       hero carousel, type fitter, entrance animation
  img/products/    product photography
```

## Editing

**Prices and products** live in `assets/js/products.js`, one object per item. Change `price` (plain number, IDR) and reload; nothing to rebuild.

**Contact details** are in the `CONFIG` block at the top of `assets/js/main.js` — WhatsApp number, email, and marketplace store links.

**Languages.** Indonesian is the default, English is a toggle in the header, remembered per visitor. Static copy uses paired `data-lang-id` / `data-lang-en` elements; product names come from `nameId` / `nameEn`; interface strings live in the `T` dictionary in `main.js`.

## Search and social metadata

Each page carries a canonical URL, Open Graph and Twitter card tags, and a `theme-color`. Shared links preview with `assets/img/og-cover.jpg` (1200×630).

Structured data is JSON-LD: `Organization` + `WebSite` on the homepage, and an `ItemList` of every product on the catalogue. **The catalogue block is generated from `products.js`** — if you change a price there, regenerate it rather than hand-editing the JSON, so the two cannot disagree. Google reads price and availability from it, and a mismatch with the visible page can cost you the rich result.

One known limit: both languages live in the same HTML and are toggled with CSS, so a crawler sees Indonesian and English on a single URL. Indonesian is the declared page language and the primary market, so this is a deliberate trade. Proper `hreflang` would need separate `/en/` URLs.

If you move to a custom domain, update the URLs in `sitemap.xml`, `robots.txt`, the canonical and `og:*` tags on all four pages, and the JSON-LD `@id` values.

## Local preview

```bash
python3 -m http.server 4173
```

Then open http://localhost:4173.

## Deploying

Pushing to `main` publishes to GitHub Pages automatically. To host elsewhere, upload the folder as-is to any static host.

---

TDM ELECTRIC® is a registered trademark of its respective owner.

## Updating products

`assets/js/products.js` holds every name, price and spec. After editing it (or the descriptions and marketplace links in `tools/content.py`), run:

```bash
python3 tools/build_site.py
```

This regenerates the product pages in `produk/`, the category pages in `kategori/`, `sitemap.xml`, the catalogue's structured data, and the cache-busting stamps on CSS/JS links. Commit everything it changes, then upload to Hostinger.
