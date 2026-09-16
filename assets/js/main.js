/* ==========================================================================
   TDM Electric Indonesia — site behaviour
   Edit CONFIG below: WhatsApp number and marketplace store links.
   ========================================================================== */

const CONFIG = {
  waNumber: "6282317379932",
  waGreetingId: "Halo TDM Electric Indonesia, saya ingin menanyakan produk",
  waGreetingEn: "Hello TDM Electric Indonesia, I would like to ask about",
  tokopedia: "https://www.tokopedia.com/tdm-electric",
  blibli: "", // isi setelah toko Blibli aktif
  email: "mike@pnglobalindo.com",
};

/* ---------- i18n --------------------------------------------------------- */
const T = {
  id: {
    allProducts: "Semua Produk",
    searchPlaceholder: "Cari nama produk atau kode SKU...",
    showing: (n, t) => `Menampilkan ${n} dari ${t} produk`,
    empty: "Produk tidak ditemukan. Coba kata kunci lain.",
    perPack: "/ paket",
    detail: "Lihat detail",
    sku: "Kode Artikel",
    category: "Kategori",
    material: "Material",
    dims: "Dimensi",
    weight: "Berat",
    pack: "Isi Kemasan",
    ean: "Barcode (EAN)",
    warranty: "Garansi",
    warrantyVal: "3 tahun resmi TDM Electric",
    askWa: "Tanya stok & harga grosir",
    buyTokopedia: "Beli di Tokopedia",
    buyBlibli: "Beli di Blibli",
    soon: "Segera hadir",
    modalNote: "Harga satuan indikatif. Untuk pembelian proyek atau grosir, harga khusus tersedia via WhatsApp.",
  },
  en: {
    allProducts: "All Products",
    searchPlaceholder: "Search product name or SKU code...",
    showing: (n, t) => `Showing ${n} of ${t} products`,
    empty: "No products found. Try a different keyword.",
    perPack: "/ pack",
    detail: "View details",
    sku: "Article Code",
    category: "Category",
    material: "Material",
    dims: "Dimensions",
    weight: "Weight",
    pack: "Pack Contents",
    ean: "Barcode (EAN)",
    warranty: "Warranty",
    warrantyVal: "3-year official TDM Electric",
    askWa: "Ask stock & wholesale price",
    buyTokopedia: "Buy on Tokopedia",
    buyBlibli: "Buy on Blibli",
    soon: "Coming soon",
    modalNote: "Indicative unit price. Project and wholesale pricing is available via WhatsApp.",
  },
};

let LANG = localStorage.getItem("tdm-lang") === "en" ? "en" : "id";
const t = () => T[LANG];

function applyLang(lang) {
  LANG = lang;
  localStorage.setItem("tdm-lang", lang);
  document.documentElement.lang = lang;
  document.querySelectorAll(".lang-toggle button").forEach((b) => {
    b.setAttribute("aria-pressed", String(b.dataset.lang === lang));
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
    el.placeholder = t()[el.dataset.i18nPlaceholder];
  });
  if (typeof renderAll === "function") renderAll();
}

/* ---------- helpers ------------------------------------------------------ */
const rp = (n) => "Rp" + n.toLocaleString("id-ID");

function waLink(subject) {
  const greeting = LANG === "en" ? CONFIG.waGreetingEn : CONFIG.waGreetingId;
  const text = subject ? `${greeting}: ${subject}` : greeting.replace(/:?$/, "");
  return `https://wa.me/${CONFIG.waNumber}?text=${encodeURIComponent(text)}`;
}

const pName = (p) => (LANG === "en" ? p.nameEn : p.nameId);
const cName = (c) => (LANG === "en" ? c.en : c.id);
const cDesc = (c) => (LANG === "en" ? c.descEn : c.descId);
const catOf = (key) => CATEGORIES.find((c) => c.key === key);

function el(tag, cls, html) {
  const n = document.createElement(tag);
  if (cls) n.className = cls;
  if (html !== undefined) n.innerHTML = html;
  return n;
}

/* ---------- product card ------------------------------------------------- */
function productCard(p) {
  const card = el("button", "product-card");
  card.type = "button";
  card.setAttribute("aria-label", pName(p));
  card.innerHTML = `
    <div class="product-photo">
      <span class="product-sku">${p.sku}</span>
      <img src="${p.images[0]}" alt="${pName(p)}" loading="lazy" width="400" height="300">
    </div>
    <div class="product-body">
      <div class="product-name">${pName(p)}</div>
      <div class="chips">${p.specs.map((s) => `<span class="chip">${s}</span>`).join("")}</div>
      <div class="product-foot">
        <span class="price">${rp(p.price)}${p.pack ? ` <span class="price-unit">${t().perPack}</span>` : ""}</span>
        <span class="product-more">${t().detail} →</span>
      </div>
    </div>`;
  card.addEventListener("click", () => openModal(p));
  return card;
}

/* ---------- modal -------------------------------------------------------- */
let openProduct = null;

function openModal(p) {
  const modal = document.getElementById("productModal");
  if (!modal) return;
  openProduct = p;

  const rows = [
    [t().sku, p.sku],
    [t().category, cName(catOf(p.cat))],
    [t().material, p.material],
    [t().dims, p.dims],
    [t().weight, p.weight],
    [t().pack, p.pack],
    [t().ean, p.ean],
    [t().warranty, t().warrantyVal],
  ].filter(([, v]) => v);

  modal.querySelector(".modal-panel").innerHTML = `
    <button class="modal-close" aria-label="Close">&times;</button>
    <div class="modal-gallery">
      <div class="modal-main-img">
        <img id="modalMainImg" src="${p.images[0]}" alt="${pName(p)}">
      </div>
      ${p.images.length > 1 ? `<div class="modal-thumbs">${p.images
        .map((src, i) => `<button type="button" aria-pressed="${i === 0}" data-src="${src}">
            <img src="${src}" alt=""></button>`).join("")}</div>` : ""}
    </div>
    <div class="modal-info">
      <div>
        <div class="modal-sku">${p.sku}</div>
        <h3>${pName(p)}</h3>
      </div>
      <div class="chips">${p.specs.map((s) => `<span class="chip">${s}</span>`).join("")}</div>
      <div class="modal-price">${rp(p.price)}${p.pack ? ` <span class="price-unit">${t().perPack}</span>` : ""}</div>
      <table class="spec-table"><tbody>
        ${rows.map(([k, v]) => `<tr><th>${k}</th><td>${v}</td></tr>`).join("")}
      </tbody></table>
      <div class="modal-actions">
        <a class="btn btn-wa" href="${waLink(`${pName(p)} (${p.sku})`)}" target="_blank" rel="noopener">
          ${waIcon(17)} ${t().askWa}
        </a>
        ${CONFIG.tokopedia ? `<a class="btn btn-ghost" href="${CONFIG.tokopedia}" target="_blank" rel="noopener">${t().buyTokopedia} →</a>` : ""}
        ${CONFIG.blibli ? `<a class="btn btn-ghost" href="${CONFIG.blibli}" target="_blank" rel="noopener">${t().buyBlibli} →</a>` : ""}
      </div>
      <p class="modal-note">${t().modalNote}</p>
    </div>`;

  modal.querySelector(".modal-close").addEventListener("click", closeModal);
  modal.querySelectorAll(".modal-thumbs button").forEach((b) => {
    b.addEventListener("click", () => {
      document.getElementById("modalMainImg").src = b.dataset.src;
      modal.querySelectorAll(".modal-thumbs button").forEach((x) =>
        x.setAttribute("aria-pressed", String(x === b)));
    });
  });

  modal.setAttribute("open", "");
  document.body.style.overflow = "hidden";
}

function closeModal() {
  const modal = document.getElementById("productModal");
  if (!modal) return;
  openProduct = null;
  modal.removeAttribute("open");
  document.body.style.overflow = "";
}

function waIcon(size = 18) {
  return `<svg viewBox="0 0 24 24" fill="currentColor" width="${size}" height="${size}" aria-hidden="true"><path d="M17.5 14.4c-.3-.2-1.8-.9-2-1-.3-.1-.5-.2-.7.1s-.8 1-.9 1.2c-.2.2-.3.2-.6.1-.3-.2-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.5-.6c.1-.2.2-.3.3-.5 0-.2 0-.4 0-.5 0-.2-.7-1.6-.9-2.2-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.2.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.3-.7.3-1.3.2-1.4-.1-.2-.3-.2-.6-.3zM12 2a10 10 0 0 0-8.6 15L2 22l5.2-1.4A10 10 0 1 0 12 2zm0 18.2c-1.6 0-3.1-.4-4.4-1.2l-.3-.2-3.1.8.8-3-.2-.3a8.2 8.2 0 1 1 7.2 4z"/></svg>`;
}

/* ---------- page: home --------------------------------------------------- */
function renderHome() {
  const catGrid = document.getElementById("catGrid");
  if (catGrid) {
    catGrid.innerHTML = "";
    CATEGORIES.forEach((c) => {
      const n = PRODUCTS.filter((p) => p.cat === c.key).length;
      const a = el("a", "cat-card");
      a.href = `produk.html?cat=${c.key}`;
      a.innerHTML = `
        <span class="cat-icon">${CAT_ICONS[c.key] || ""}</span>
        <h3>${cName(c)}</h3>
        <p>${cDesc(c)}</p>
        <span class="cat-count">${n} ${LANG === "en" ? "products" : "produk"} →</span>`;
      catGrid.appendChild(a);
    });
  }

  const featured = document.getElementById("featuredGrid");
  if (featured) {
    featured.innerHTML = "";
    const picks = ["SQ1017-0101", "SQ1818-0009", "SQ1806-0009", "SQ0335-0050",
                   "SQ1010-0103", "SQ1824-0010", "SQ0512-0006", "SQ1809-0021"];
    picks.map((s) => PRODUCTS.find((p) => p.sku === s))
         .filter(Boolean)
         .forEach((p) => featured.appendChild(productCard(p)));
  }
}

/* ---------- page: catalogue ---------------------------------------------- */
let activeCat = "all";
let query = "";

function renderCatalogue() {
  const grid = document.getElementById("productGrid");
  if (!grid) return;

  const pills = document.getElementById("filterPills");
  if (pills && !pills.dataset.built) {
    const mk = (key, label) => {
      const b = el("button", "pill", label);
      b.type = "button";
      b.dataset.cat = key;
      b.setAttribute("aria-pressed", String(key === activeCat));
      b.addEventListener("click", () => {
        activeCat = key;
        renderCatalogue();
      });
      return b;
    };
    pills.appendChild(mk("all", t().allProducts));
    CATEGORIES.forEach((c) => pills.appendChild(mk(c.key, cName(c))));
    pills.dataset.built = "1";
  } else if (pills) {
    [...pills.children].forEach((b, i) => {
      b.textContent = i === 0 ? t().allProducts : cName(CATEGORIES[i - 1]);
      b.setAttribute("aria-pressed", String(b.dataset.cat === activeCat));
    });
  }

  const q = query.trim().toLowerCase();
  const list = PRODUCTS.filter((p) => {
    if (activeCat !== "all" && p.cat !== activeCat) return false;
    if (!q) return true;
    return (p.nameId + " " + p.nameEn + " " + p.sku + " " + p.specs.join(" "))
      .toLowerCase().includes(q);
  });

  const count = document.getElementById("resultsCount");
  if (count) count.textContent = t().showing(list.length, PRODUCTS.length);

  grid.innerHTML = "";
  if (!list.length) {
    grid.appendChild(el("div", "empty-state", t().empty));
    grid.style.display = "block";
    return;
  }
  grid.style.display = "";
  list.forEach((p) => grid.appendChild(productCard(p)));
}

/* ---------- icons -------------------------------------------------------- */
const CAT_ICONS = {
  plugs: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><path d="M9 2v6M15 2v6"/><path d="M6 8h12v3a6 6 0 0 1-6 6 6 6 0 0 1-6-6V8Z"/><path d="M12 17v5"/></svg>`,
  cables: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><path d="M4 7h7a4 4 0 0 1 0 8H9a4 4 0 0 0 0 8h11"/><circle cx="4" cy="7" r="2"/><path d="M17 3h4v4h-4z"/></svg>`,
  lighting: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><path d="M9 18h6M10 22h4"/><path d="M12 2a7 7 0 0 0-4 12.7V18h8v-3.3A7 7 0 0 0 12 2Z"/></svg>`,
  antenna: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><circle cx="12" cy="12" r="2"/><path d="M7.8 7.8a6 6 0 0 0 0 8.4M16.2 16.2a6 6 0 0 0 0-8.4"/><path d="M4.9 4.9a10 10 0 0 0 0 14.2M19.1 19.1a10 10 0 0 0 0-14.2"/></svg>`,
  tools: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a4 4 0 0 1 5.3 5L21 21l-3-3-8.5-8.5"/><path d="M7 3 3 7l4 4 2-2"/><path d="m3 21 7-7"/></svg>`,
};

/* ---------- boot --------------------------------------------------------- */
function renderAll() {
  renderHome();
  renderCatalogue();
  document.querySelectorAll("[data-wa]").forEach((a) => {
    a.href = waLink(a.dataset.wa || "");
  });
  // an open detail modal is rendered once at open time, so re-render it on language change
  if (openProduct) openModal(openProduct);
  // the homepage hero sizes its type by measured ink width; new words need a new pass
  if (window.hxLayout) window.hxLayout();
}

document.addEventListener("DOMContentLoaded", () => {
  // WhatsApp + marketplace links
  document.querySelectorAll("[data-wa]").forEach((a) => { a.href = waLink(a.dataset.wa || ""); });
  document.querySelectorAll("[data-link='tokopedia']").forEach((a) => {
    if (CONFIG.tokopedia) a.href = CONFIG.tokopedia;
  });
  document.querySelectorAll("[data-link='blibli']").forEach((a) => {
    if (CONFIG.blibli) { a.href = CONFIG.blibli; }
    else { a.setAttribute("aria-disabled", "true"); a.classList.add("btn-ghost"); a.href = "#"; }
  });
  document.querySelectorAll("[data-link='email']").forEach((a) => {
    a.href = "mailto:" + CONFIG.email;
    if (!a.textContent.trim()) a.textContent = CONFIG.email;
  });

  // language
  document.querySelectorAll(".lang-toggle button").forEach((b) => {
    b.addEventListener("click", () => applyLang(b.dataset.lang));
  });

  // mobile menu
  const menuBtn = document.querySelector(".menu-btn");
  if (menuBtn) menuBtn.addEventListener("click", () => {
    document.querySelector(".nav").classList.toggle("open");
  });

  // search
  const search = document.getElementById("searchInput");
  if (search) search.addEventListener("input", (e) => { query = e.target.value; renderCatalogue(); });

  // deep-link ?cat=
  const urlCat = new URLSearchParams(location.search).get("cat");
  if (urlCat && CATEGORIES.some((c) => c.key === urlCat)) activeCat = urlCat;

  // modal dismissal
  const modal = document.getElementById("productModal");
  if (modal) {
    modal.querySelector(".modal-backdrop").addEventListener("click", closeModal);
    document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeModal(); });
  }

  applyLang(LANG);
});
