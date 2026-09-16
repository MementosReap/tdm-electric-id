# TDM Electric Indonesia

Brand and catalogue site for TDM Electric products in the Indonesian market.

**Live:** https://mementosreap.github.io/tdm-electric-id/

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

## Local preview

```bash
python3 -m http.server 4173
```

Then open http://localhost:4173.

## Deploying

Pushing to `main` publishes to GitHub Pages automatically. To host elsewhere, upload the folder as-is to any static host.

---

TDM ELECTRIC® is a registered trademark of its respective owner.
