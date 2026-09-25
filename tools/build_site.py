"""
Builds the crawlable parts of the site from assets/js/products.js:

  produk/<slug>.html      one page per product (title, OG card, Product JSON-LD)
  kategori/<key>.html     one page per category (static product links)
  sitemap.xml             every page, with product images
  produk.html             its ItemList JSON-LD, pointing at the product pages

It also writes slug, marketplace links and warranty into products.js so the
catalogue cards can link to the product pages.

products.js stays the single source of truth for names, prices and specs.
Run after every edit to it:

    python3 tools/build_site.py
"""
import datetime, hashlib, html, json, re, sys, unicodedata
from urllib.parse import quote
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from content import DESC, WARRANTY_YEARS, blibli_url, tokopedia_url  # noqa: E402

SITE = "https://tdme.pnglobalindo.com"
ORG_ID = f"{SITE}/#org"
DEFAULT_WARRANTY = 3
TODAY = datetime.date.today().isoformat()

PRODUCTS_JS = ROOT / "assets/js/products.js"
src = PRODUCTS_JS.read_text()
CATEGORIES = json.loads(re.search(r"const CATEGORIES = (\[.*?\n\]);", src, re.S).group(1))
PRODUCTS = json.loads(re.search(r"const PRODUCTS = (\[.*?\n\]);", src, re.S).group(1))
CAT = {c["key"]: c for c in CATEGORIES}

esc = lambda s: html.escape(str(s), quote=True)


def slugify(text):
    t = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    t = re.sub(r"[^a-zA-Z0-9]+", "-", t.lower()).strip("-")
    return re.sub(r"-{2,}", "-", t)


def rp(n):
    return "Rp" + f"{n:,}".replace(",", ".")


# ---------------------------------------------------------------- products.js
for p in PRODUCTS:
    p["slug"] = f"{slugify(p['nameId'])}-{p['sku'].lower()}"
    p["tokopedia"] = tokopedia_url(p["sku"])
    p["blibli"] = blibli_url(p["sku"])
    p["warrantyYears"] = WARRANTY_YEARS.get(p["sku"], DEFAULT_WARRANTY)
    missing = [k for k in ("slug", "blibli") if not p[k]]
    assert not missing, f"{p['sku']}: missing {missing}"
    assert p["sku"] in DESC, f"{p['sku']}: no description in tools/content.py"

new_src = re.sub(r"const PRODUCTS = \[.*?\n\];",
                 lambda _: "const PRODUCTS = " + json.dumps(PRODUCTS, ensure_ascii=False, indent=2) + ";",
                 src, count=1, flags=re.S)
PRODUCTS_JS.write_text(new_src)

page_url = lambda p: f"{SITE}/produk/{p['slug']}.html"
cat_url = lambda key: f"{SITE}/kategori/{key}.html"
img_url = lambda p: f"{SITE}/{p['images'][0]}"

# ---------------------------------------------------------------- page shell
shell = (ROOT / "produk.html").read_text()
top = shell[shell.index('<div class="topbar">'):shell.index("</header>") + len("</header>")]
foot = shell[shell.index('<footer class="footer">'):shell.index("</svg>\n</a>", shell.index('class="wa-float"')) + len("</svg>\n</a>")]


def rebase(fragment, prefix="../"):
    """Point relative links at the site root from one folder down."""
    def fix(m):
        attr, val = m.group(1), m.group(2)
        if re.match(r"(https?:|mailto:|tel:|#|/|data:)", val) or val == "":
            return m.group(0)
        return f'{attr}="{prefix}{val}"'
    return re.sub(r'\b(href|src)="([^"]*)"', fix, fragment)


TOP = rebase(top).replace('class="active"', "")
TOP_PRODUCTS_ACTIVE = TOP.replace('<a href="../produk.html">', '<a href="../produk.html" class="active">', 1)
FOOT = rebase(foot)


def head(title, desc, canonical, image, og_type="website", extra_meta="", jsonld=None):
    ld = ""
    if jsonld:
        ld = '\n<script type="application/ld+json">\n' + json.dumps(jsonld, ensure_ascii=False, indent=1) + "\n</script>"
    return f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#F5700B">
<link rel="apple-touch-icon" href="../assets/img/logo.jpeg">
<link rel="icon" href="../assets/img/logo.jpeg">

<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="TDM Electric Indonesia">
<meta property="og:locale" content="id_ID">
<meta property="og:locale:alternate" content="en_US">
<meta property="og:url" content="{canonical}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{image}">
<meta property="og:image:alt" content="{esc(title)}">{extra_meta}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{image}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/css/style.css">{ld}
</head>
<body>
"""


TAIL = """
<script>window.SITE_ROOT = "../";</script>
<script src="../assets/js/products.js"></script>
<script src="../assets/js/main.js"></script>
<script>document.getElementById('year').textContent = new Date().getFullYear();</script>
</body>
</html>
"""


def bi(id_text, en_text):
    return f"<span data-lang-id>{id_text}</span><span data-lang-en>{en_text}</span>"


def price_html(p):
    unit = f' <span class="price-unit">{bi("/ paket", "/ pack")}</span>' if p["pack"] else ""
    return f"{rp(p['price'])}{unit}"


def card(p, prefix="../"):
    chips = "".join(f'<span class="chip">{esc(s)}</span>' for s in p["specs"])
    return f"""<a class="product-card" href="{prefix}produk/{p['slug']}.html">
      <div class="product-photo">
        <span class="product-sku">{p['sku']}</span>
        <img src="{prefix}{p['images'][0]}" alt="{esc(p['nameId'])}" loading="lazy" width="400" height="300">
      </div>
      <div class="product-body">
        <div class="product-name">{bi(esc(p['nameId']), esc(p['nameEn']))}</div>
        <div class="chips">{chips}</div>
        <div class="product-foot">
          <span class="price">{price_html(p)}</span>
          <span class="product-more">{bi("Lihat detail", "View details")} →</span>
        </div>
      </div>
    </a>"""


def breadcrumb(items):
    """items: [(label_id, label_en, href or None)]"""
    parts = []
    for i, (lid, len_, href) in enumerate(items):
        label = bi(esc(lid), esc(len_))
        parts.append(f'<a href="{href}">{label}</a>' if href else f'<span aria-current="page">{label}</span>')
    return '<nav class="breadcrumb" aria-label="Breadcrumb"><div class="wrap">' + ' <span class="sep">/</span> '.join(parts) + "</div></nav>"


def breadcrumb_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": name, **({"item": url} if url else {})}
        for i, (name, url) in enumerate(items)]}


# ---------------------------------------------------------------- product pages
(ROOT / "produk").mkdir(exist_ok=True)
for old in (ROOT / "produk").glob("*.html"):
    old.unlink()

for p in PRODUCTS:
    c = CAT[p["cat"]]
    d_id, d_en = DESC[p["sku"]]
    specs = ", ".join(p["specs"])
    pack_note = f" (isi {p['pack']})" if p["pack"] else ""
    title = f"{p['nameId']} {p['sku']} — TDM Electric Indonesia"
    desc = (f"{p['nameId']} TDM Electric {p['sku']}{pack_note}: {specs}. "
            f"Harga {rp(p['price'])}. Produk asli dari distributor resmi, beli di Tokopedia, Blibli atau WhatsApp.")
    years = p["warrantyYears"]

    rows = [
        (("Kode Artikel", "Article Code"), p["sku"]),
        (("Kategori", "Category"), bi(esc(c["id"]), esc(c["en"]))),
        (("Material", "Material"), p.get("material")),
        (("Dimensi", "Dimensions"), p.get("dims")),
        (("Berat", "Weight"), p.get("weight")),
        (("Isi Kemasan", "Pack Contents"), p.get("pack")),
        (("Barcode (EAN)", "Barcode (EAN)"), p.get("ean")),
        (("Garansi", "Warranty"), bi(f"{years} tahun resmi TDM Electric", f"{years}-year official TDM Electric")),
    ]
    rows_html = "".join(f"<tr><th>{bi(*k)}</th><td>{v}</td></tr>" for k, v in rows if v)

    buttons = [f'<a class="btn btn-wa" data-wa="{esc(p["nameId"])} ({p["sku"]})" target="_blank" rel="noopener">'
               f'{bi("Tanya stok &amp; harga grosir", "Ask stock &amp; wholesale price")}</a>']
    if p["tokopedia"]:
        buttons.append(f'<a class="btn btn-ghost" href="{p["tokopedia"]}" target="_blank" rel="noopener">'
                       f'{bi("Beli di Tokopedia", "Buy on Tokopedia")} →</a>')
    buttons.append(f'<a class="btn btn-ghost" href="{p["blibli"]}" target="_blank" rel="noopener">'
                   f'{bi("Beli di Blibli", "Buy on Blibli")} →</a>')
    share_text = f"{p['nameId']} ({p['sku']}) — {rp(p['price'])}\n{page_url(p)}"
    share = (f'<a class="share-link" href="https://wa.me/?text={esc(quote(share_text))}" '
             f'target="_blank" rel="noopener">{bi("Bagikan ke WhatsApp", "Share on WhatsApp")}</a>')

    related = [q for q in PRODUCTS if q["cat"] == p["cat"] and q["sku"] != p["sku"]][:4]
    if len(related) < 4:
        related += [q for q in PRODUCTS if q["cat"] != p["cat"]][: 4 - len(related)]

    offer = {"@type": "Offer", "url": page_url(p), "price": p["price"], "priceCurrency": "IDR",
             "availability": "https://schema.org/InStock", "itemCondition": "https://schema.org/NewCondition",
             "seller": {"@id": ORG_ID}}
    product_ld = {"@type": "Product", "@id": page_url(p) + "#product",
                  "name": f"TDM Electric {p['nameId']}", "sku": p["sku"], "mpn": p["sku"],
                  "brand": {"@type": "Brand", "name": "TDM Electric"},
                  "category": c["id"], "image": img_url(p), "description": d_id, "offers": offer,
                  "additionalProperty": [{"@type": "PropertyValue", "name": "Spesifikasi", "value": s} for s in p["specs"]]}
    if p.get("ean"):
        product_ld["gtin13"] = p["ean"]
    if p.get("material"):
        product_ld["material"] = p["material"]
    crumbs = [("Beranda", f"{SITE}/"), ("Produk", f"{SITE}/produk.html"), (c["id"], cat_url(c["key"])), (p["nameId"], None)]
    ld = {"@context": "https://schema.org", "@graph": [product_ld, breadcrumb_ld(crumbs)]}

    extra = (f'\n<meta property="product:price:amount" content="{p["price"]}">'
             f'\n<meta property="product:price:currency" content="IDR">'
             f'\n<meta property="product:brand" content="TDM Electric">'
             f'\n<meta property="product:availability" content="in stock">'
             f'\n<meta property="product:retailer_item_id" content="{p["sku"]}">')
    body = head(title, desc, page_url(p), img_url(p), "product", extra, ld) + TOP_PRODUCTS_ACTIVE + "\n"
    body += breadcrumb([("Beranda", "Home", "../index.html"), ("Produk", "Products", "../produk.html"),
                        (c["id"], c["en"], f"../kategori/{c['key']}.html"), (p["nameId"], p["nameEn"], None)])
    body += f"""
<section class="section pdp-section">
  <div class="wrap pdp">
    <div class="pdp-gallery">
      <img src="../{p['images'][0]}" alt="{esc(p['nameId'])} TDM Electric {p['sku']}" width="1000" height="667" fetchpriority="high">
    </div>
    <div class="pdp-info">
      <div class="modal-sku">{p['sku']}</div>
      <h1>{bi(esc(p['nameId']), esc(p['nameEn']))}</h1>
      <div class="chips">{''.join(f'<span class="chip">{esc(s)}</span>' for s in p['specs'])}</div>
      <div class="modal-price">{price_html(p)}</div>
      <table class="spec-table"><tbody>{rows_html}</tbody></table>
      <div class="modal-actions">{''.join(buttons)}</div>
      {share}
      <p class="modal-note">{bi("Harga satuan indikatif. Untuk pembelian proyek atau grosir, harga khusus tersedia via WhatsApp.",
                               "Indicative unit price. Project and wholesale pricing is available via WhatsApp.")}</p>
    </div>
  </div>
</section>
<section class="section section-alt">
  <div class="wrap pdp-desc">
    <h2>{bi("Deskripsi Produk", "Product Description")}</h2>
    <p>{bi(esc(d_id), esc(d_en))}</p>
    <p class="pdp-brand">{bi("TDM Electric adalah merek perlengkapan listrik asal Rusia yang berdiri sejak 2008. Produk dijual dalam kemasan original pabrik dengan kode artikel " + p['sku'] + ".",
                             "TDM Electric is a Russian electrical brand founded in 2008. Products ship in original factory packaging marked with article code " + p['sku'] + ".")}</p>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>{bi("Produk Terkait", "Related Products")}</h2></div>
    <div class="product-grid">
    {''.join(card(q) for q in related)}
    </div>
  </div>
</section>
"""
    body += FOOT + TAIL
    (ROOT / "produk" / f"{p['slug']}.html").write_text(body)

# ---------------------------------------------------------------- category pages
(ROOT / "kategori").mkdir(exist_ok=True)
for c in CATEGORIES:
    items = [p for p in PRODUCTS if p["cat"] == c["key"]]
    lo, hi = min(p["price"] for p in items), max(p["price"] for p in items)
    title = f"{c['id']} TDM Electric — Harga & Spesifikasi | TDM Electric Indonesia"
    desc = f"{c['descId']} {len(items)} produk TDM Electric asli, harga {rp(lo)}–{rp(hi)}. Beli di Tokopedia, Blibli atau WhatsApp."
    crumbs = [("Beranda", f"{SITE}/"), ("Produk", f"{SITE}/produk.html"), (c["id"], None)]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": cat_url(c["key"]), "name": f"{c['id']} TDM Electric", "description": desc,
         "isPartOf": {"@id": f"{SITE}/#site"},
         "mainEntity": {"@type": "ItemList", "numberOfItems": len(items), "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "url": page_url(p), "name": p["nameId"]} for i, p in enumerate(items)]}},
        breadcrumb_ld(crumbs)]}
    body = head(title, desc, cat_url(c["key"]), img_url(items[0]), "website", "", ld) + TOP_PRODUCTS_ACTIVE + "\n"
    body += breadcrumb([("Beranda", "Home", "../index.html"), ("Produk", "Products", "../produk.html"), (c["id"], c["en"], None)])
    pills = "".join(
        f'<a class="pill" href="{cc["key"]}.html" aria-pressed="{str(cc["key"] == c["key"]).lower()}">{bi(esc(cc["id"]), esc(cc["en"]))}</a>'
        for cc in CATEGORIES)
    body += f"""
<section class="page-head">
  <div class="wrap">
    <span class="eyebrow">{bi("Kategori", "Category")}</span>
    <h1>{bi(esc(c['id']), esc(c['en']))}</h1>
    <p>{bi(esc(c['descId']), esc(c['descEn']))}</p>
  </div>
</section>
<section class="section" style="padding-top:38px">
  <div class="wrap">
    <div class="filters"><div class="filter-pills"><a class="pill" href="../produk.html" aria-pressed="false">{bi("Semua Produk", "All Products")}</a>{pills}</div></div>
    <div class="results-count">{bi(f"{len(items)} produk", f"{len(items)} products")}</div>
    <div class="product-grid">
    {''.join(card(p) for p in items)}
    </div>
  </div>
</section>
"""
    body += FOOT + TAIL
    (ROOT / "kategori" / f"{c['key']}.html").write_text(body)

# ---------------------------------------------------------------- produk.html ItemList
page = (ROOT / "produk.html").read_text()
raw = re.search(r'<script type="application/ld\+json">(.*?)</script>', page, re.S).group(1)
doc = json.loads(raw)
for g in doc["@graph"]:
    if g.get("@type") == "ItemList":
        g["numberOfItems"] = len(PRODUCTS)
        g["itemListElement"] = [{"@type": "ListItem", "position": i + 1, "url": page_url(p), "name": p["nameId"]}
                                for i, p in enumerate(PRODUCTS)]
page = page.replace(raw, "\n" + json.dumps(doc, ensure_ascii=False, indent=1) + "\n", 1)
page = re.sub(r"Katalog lengkap \d+ produk", f"Katalog lengkap {len(PRODUCTS)} produk", page)
(ROOT / "produk.html").write_text(page)

# ---------------------------------------------------------------- category links on the root pages
for name in ("index.html", "produk.html", "tentang.html", "kontak.html"):
    f = ROOT / name
    f.write_text(re.sub(r'href="produk\.html\?cat=(\w+)"', r'href="kategori/\1.html"', f.read_text()))

# ---------------------------------------------------------------- sitemap
urls = [(f"{SITE}/", "1.0", None), (f"{SITE}/produk.html", "0.9", None),
        (f"{SITE}/tentang.html", "0.6", None), (f"{SITE}/kontak.html", "0.6", None)]
urls += [(cat_url(c["key"]), "0.8", None) for c in CATEGORIES]
urls += [(page_url(p), "0.7", p) for p in PRODUCTS]
lines = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
         'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
for loc, prio, p in urls:
    img = (f"<image:image><image:loc>{img_url(p)}</image:loc><image:title>{esc(p['nameId'])}</image:title></image:image>"
           if p else "")
    lines.append(f"  <url><loc>{loc}</loc><lastmod>{TODAY}</lastmod><priority>{prio}</priority>{img}</url>")
lines.append("</urlset>")
(ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n")

# ---------------------------------------------------------------- cache busting
# CSS/JS URLs carry a hash of the file's content, so a changed products.js
# (prices) reaches visitors at once instead of after the browser cache expires.
stamp = {}
for asset in list((ROOT / "assets/css").glob("*.css")) + list((ROOT / "assets/js").glob("*.js")):
    stamp[asset.relative_to(ROOT).as_posix()] = hashlib.md5(asset.read_bytes()).hexdigest()[:8]
pages = [ROOT / n for n in ("index.html", "produk.html", "tentang.html", "kontak.html")]
pages += list((ROOT / "produk").glob("*.html")) + list((ROOT / "kategori").glob("*.html"))
for f in pages:
    text = f.read_text()
    text = re.sub(r'((?:\.\./)?(assets/(?:css|js)/[\w.-]+\.(?:css|js)))(?:\?v=\w+)?"',
                  lambda m: f'{m.group(1)}?v={stamp[m.group(2)]}"' if m.group(2) in stamp else m.group(0), text)
    f.write_text(text)

print(f"{len(PRODUCTS)} product pages, {len(CATEGORIES)} category pages, {len(urls)} sitemap URLs")
