/* ==========================================================================
   Homepage hero: starfield, 37-card 3D ring, type fitter, scale law,
   nav panel, and the one-shot entrance timeline.
   Exposes window.hxLayout so main.js can re-fit the type after a language
   switch (the fitter sizes text by measured ink width, so new words need a
   new pass).
   ========================================================================== */
(function(){
'use strict';

var hx = document.getElementById('hx');
if (!hx) return;

var CW = 1172, CH = 657;
var TAB_MAX = 1080, TAB_MIN = 701, DW_MIN = 920;
var canvas = document.getElementById('canvas');
var ring   = document.getElementById('ring');
var k = 1, mobile = false, tablet = false, tboost = 1;
var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');

/* ---------- STARFIELD: one giant box-shadow list per layer ---------- */
function stars(el, n, blur, lo, hi){
  var out = [];
  for (var i = 0; i < n; i++){
    var a = (lo + Math.random() * (hi - lo)).toFixed(3);
    out.push((Math.random()*100).toFixed(2) + 'vw ' +
             (Math.random()*100).toFixed(2) + 'vh ' + blur + 'px 0 rgba(255,255,255,' + a + ')');
  }
  el.style.boxShadow = out.join(',');
}
stars(document.getElementById('stA'), 150, 0,   0.05, 0.30);
stars(document.getElementById('stB'),  18, 1.2, 0.35, 0.70);

/* ---------- CARD CREATIVES ---------- */
var B = 'assets/img/products/';
var SHOTS = [
  {url: B + 'SQ1806-0405.jpg', v: 'pay'},
  {url: B + 'SQ1818-0009.jpg', v: 'launch'},
  {url: B + 'SQ1017-0101.jpg', v: 'shop'},
  {url: B + 'SQ1806-0411.jpg', v: 'brand'},
  {url: B + 'SQ0512-0006.jpg', v: 'frete'},
  {url: B + 'SQ1815-0025.jpg', v: 'plain', t: 'INSTALASI RAPI'},
  {url: B + 'SQ1010-0103.jpg', v: 'power'},
  {url: B + 'SQ1824-0010.jpg', v: 'plain', t: 'BARU DATANG'},
  {url: B + 'SQ1809-0021.jpg', v: 'off'},
  {url: B + 'SQ0502-0001.jpg', v: 'plain', t: 'SIAP GROSIR'}
];

function creative(d){
  var im = '<img alt="" src="' + d.url + '">';
  switch (d.v){

  case 'pay':
    return '<div class="fill" style="background:#efedea"></div>'
      + '<div class="ph" style="top:112px;bottom:0">' + im + '</div>'
      + '<svg class="ph" style="top:118px;bottom:0" viewBox="0 0 130 182" preserveAspectRatio="none">'
      +   '<g stroke="#e5202f" stroke-width="8" fill="none" opacity=".92" stroke-linecap="square">'
      +     '<path d="M2 42h30M14 30v96M4 100l26-16"/>'
      +     '<path d="M96 34v58M120 34v58M96 92q12 15 24 0"/>'
      +     '<path d="M92 108l14 34M126 108l-12 34"/></g></svg>'
      + '<div class="cv" style="top:20px;text-align:right;font-size:3.4px;letter-spacing:.15em;color:#8d9298">METODE PEMBAYARAN</div>'
      + '<div class="cv t-big" style="top:32px;font-size:14px;color:#16171b">Pembayaran</div>'
      + '<div class="cv t-big" style="top:47px;font-size:14px;color:#e5202f">Cepat n aman</div>'
      + '<div class="cv" style="top:76px;font-size:5.2px;font-weight:700;color:#16171b;line-height:1.7">'
      +   '<div><b class="dot"></b>BAYAR VIA <b>TRANSFER</b></div>'
      +   '<div style="margin-top:8px"><b class="dot sq"></b>ATAU HINGGA <b>12X</b><br>'
      +     '<span style="margin-left:11px">TANPA BUNGA</span></div></div>';

  case 'launch':
    return '<div class="fill" style="background:linear-gradient(168deg,#ffe3cc,#ffc9a3 55%,#f2a878)"></div>'
      + '<div class="ph" style="top:100px;bottom:0">' + im
      +   '<div class="fill" style="background:linear-gradient(180deg,rgba(255,227,204,.97),rgba(255,227,204,0) 30%)"></div></div>'
      + '<div class="cv t-serif" style="top:36px;font-size:17px;color:#b34a10">SERI BARU</div>'
      + '<div class="cv t-serif" style="top:55px;font-size:17px;color:#b34a10">OUTDOOR!</div>';

  case 'shop':
    return '<div class="fill" style="background:#fff"></div>'
      + '<div class="ph" style="top:0;height:148px">' + im + '</div>'
      + '<div class="cv" style="top:158px;font-size:5.4px;font-weight:700;letter-spacing:.09em;color:#16171b">PERKAKAS HARIAN</div>'
      + '<div class="cv" style="top:168px;font-size:4.2px;color:#7b8087">Tang &#183; Obeng &#183; Tester</div>'
      + '<div style="position:absolute;left:10px;top:180px;padding:4px 11px;border-radius:20px;background:#F5700B;font-size:4.6px;font-weight:600;color:#fff;letter-spacing:.05em">Beli sekarang</div>';

  case 'brand':
    return '<div class="fill" style="background:linear-gradient(180deg,#3a1a06,#5c2a0a 50%,#24110a)"></div>'
      + '<div class="ph" style="top:92px;bottom:0">' + im
      +   '<div class="fill" style="background:linear-gradient(180deg,rgba(58,26,6,.98),rgba(58,26,6,0) 36%)"></div></div>'
      + '<div class="cv" style="top:16px;font-size:4.2px;line-height:1.7;color:rgba(255,255,255,.82);width:74px">Diuji sesuai standar GOST n dirancang untuk instalasi harian: bergaransi resmi sejak hari pertama.</div>'
      + '<div style="position:absolute;right:10px;top:16px;font-size:5.4px;font-weight:600;color:#fff;opacity:.92">&#10035; TDM</div>';

  case 'frete':
    return '<div class="fill" style="background:linear-gradient(158deg,#7a2c00 0%,#b84a08 40%,#e8721a 66%,#8f3404 100%)"></div>'
      + '<div class="ph" style="top:140px;bottom:0;opacity:.45;mix-blend-mode:screen">' + im + '</div>'
      + '<div class="fill" style="background:radial-gradient(44% 16% at 50% 62%, rgba(255,255,255,.92), rgba(255,255,255,0) 72%)"></div>'
      + '<div style="position:absolute;left:-6px;right:-6px;top:44px;height:13px;background:#ffb300;transform:rotate(-2.6deg);box-shadow:0 4px 12px rgba(255,179,0,.5)"></div>'
      + '<div style="position:absolute;left:0;right:0;top:45.5px;transform:rotate(-2.6deg);text-align:center;font-size:5.6px;font-weight:700;letter-spacing:.05em;color:#3a1a06">SAMPAI KE RUMAH DAN</div>'
      + '<div class="cv t-big" style="top:64px;font-size:24px;color:#fff;text-shadow:0 3px 0 rgba(90,30,0,.6)">Ongkir</div>'
      + '<div class="cv t-big" style="top:87px;font-size:24px;color:#fff;text-shadow:0 3px 0 rgba(90,30,0,.6)">Gratis</div>'
      + '<div class="cv t-big" style="top:113px;font-size:19px;color:#fff">+</div>';

  case 'power':
    return '<div class="ph phf">' + im + '</div>'
      + '<div class="fill" style="background:linear-gradient(180deg,rgba(6,5,10,0) 34%,rgba(6,5,10,.55) 52%,rgba(6,5,10,.92) 72%)"></div>'
      + '<div class="cv t-serif" style="top:132px;font-size:16px;color:#fff">DAYA YANG</div>'
      + '<div class="cv t-serif" style="top:150px;font-size:16px;color:#fff">TERUKUR</div>'
      + '<div class="cv" style="top:171px;font-size:4.4px;letter-spacing:.07em;color:rgba(255,255,255,.85)">hadir di tiap titik instalasi</div>';

  case 'off':
    return '<div class="ph phf">' + im + '</div>'
      + '<div class="fill" style="background:linear-gradient(180deg,rgba(3,9,20,0) 30%,rgba(3,9,20,.6) 48%,rgba(3,9,20,.95) 70%)"></div>'
      + '<div class="cv t-big" style="top:126px;font-size:10px;color:#fff;opacity:.9">Promo &#183; s/d</div>'
      + '<div class="cv t-big" style="top:139px;font-size:22px;color:#ffa03c;text-shadow:0 0 16px rgba(255,160,60,.5)">50% off</div>';

  default:
    return '<div class="ph phf">' + im + '</div>'
      + '<div class="fill" style="background:linear-gradient(180deg,rgba(4,8,16,0) 38%,rgba(4,8,16,.85) 68%)"></div>'
      + '<div class="cv" style="top:150px;font-size:5.4px;font-weight:600;letter-spacing:.2em;color:#fff">' + (d.t || '') + '</div>';
  }
}

/* ---------- RING GEOMETRY ----------
   R = perspective = 891 so the camera sits exactly on the cylinder axis.
   37 cards * 9.7297deg = 360. Beyond +-42deg is the back half: culled. */
var R = 891, N = 37, STEP = 360 / N, CULL = 42, SPEED = 1.9;
var cards = [], phase = -2;

(function build(){
  var frag = document.createDocumentFragment();
  for (var i = 0; i < N; i++){
    var el = document.createElement('div');
    el.className = 'card';
    el.innerHTML = creative(SHOTS[i % SHOTS.length]) + '<div class="edge"></div>';
    var img = el.querySelector('img');
    if (img) img.addEventListener('error', function(){ this.closest('.card').classList.add('broken'); });
    frag.appendChild(el);
    cards.push(el);
  }
  ring.appendChild(frag);
})();

function placeCards(){
  for (var i = 0; i < N; i++){
    var a = ((i * STEP + phase) % 360 + 540) % 360 - 180;
    var el = cards[i];
    if (Math.abs(a) > CULL){ el.style.visibility = 'hidden'; continue; }
    el.style.visibility = 'visible';
    var r = a * Math.PI / 180, c = Math.cos(r);
    el.style.transform = 'translate3d(' + (R * Math.sin(r)) + 'px,0,' + (R * (1 - c)) + 'px) rotateY(' + (-a) + 'deg)';
    el.style.filter = 'brightness(' + (0.84 + 0.5 * (1 / c - 1)) + ')';
  }
}

/* ---------- TYPE FITTER: exact ink width + cap height from measured metrics ---------- */
var mctx = document.createElement('canvas').getContext('2d');

function fontOf(el){
  var s = getComputedStyle(el);
  return {css: s.fontWeight + ' ' + s.fontSize + ' ' + s.fontFamily, size: parseFloat(s.fontSize)};
}
function inkWidth(el){ return el.getBoundingClientRect().width / (mobile ? 1 : k); }
function capRatio(el){
  mctx.font = fontOf(el).css.replace(/\b[\d.]+px\b/, '100px');
  return (mctx.measureText('H').actualBoundingBoxAscent || 70) / 100;
}
function fitBox(el, tw, tc, pre){
  el.style.transform = pre || '';
  el.style.fontSize = (tc / capRatio(el)) + 'px';
  var w = inkWidth(el);
  if (w > 0) el.style.transform = (pre ? pre + ' ' : '') + 'scaleX(' + (tw / w) + ')';
}
function baseline(el, y){
  var f = fontOf(el);
  mctx.font = f.css;
  var m = mctx.measureText('H');
  var A = m.fontBoundingBoxAscent  || f.size * 0.8;
  var D = m.fontBoundingBoxDescent || f.size * 0.2;
  el.style.top = (y - ((f.size - (A + D)) / 2 + A)) + 'px';
}
function centreLabel(btn, el, capPx){
  var probe = document.createElement('i');
  probe.style.cssText = 'display:inline-block;width:0;height:0;overflow:hidden';
  el.appendChild(probe);
  var base = probe.getBoundingClientRect().top - btn.getBoundingClientRect().top;
  probe.remove();
  var BIAS = 1.1;   // the reference sits labels ~0.6px below true centre
  el.style.top = ((btn.offsetHeight / 2) - (base / (mobile ? 1 : k) - capPx / 2) + BIAS) + 'px';
}

var h1a = document.getElementById('h1a'), h1b = document.getElementById('h1b');
var sub1 = document.getElementById('sub1'), sub2 = document.getElementById('sub2');
var badgeTxt = document.getElementById('badgeTxt'), wmName = document.getElementById('wmName');
var ctaLabel = document.getElementById('ctaLabel'), vpLabel = document.getElementById('vpLabel');
var links = document.getElementById('links');

function clearFitted(){
  [h1a, h1b, sub1, sub2, badgeTxt, wmName, ctaLabel, vpLabel].forEach(function(el){
    el.style.fontSize = ''; el.style.top = ''; el.style.transform = '';
  });
  links.style.fontSize = ''; links.style.transform = '';
  [].forEach.call(links.children, function(a){ a.style.fontSize = ''; });
}

function layout(){
  if (mobile){ clearFitted(); placeCards(); return; }
  var T = tablet ? tboost : 1;

  fitBox(h1a, 563.5 * T, 37.2 * T, 'translateX(-50%)'); baseline(h1a, 204.5);
  // second line inherits the first line's horizontal compression: same cap
  // height, same scaleX, natural proportion between the two lines
  var sxA = /scaleX\(([\d.]+)\)/.exec(h1a.style.transform);
  var kA = sxA ? parseFloat(sxA[1]) : 1;
  h1b.style.transform = 'translateX(-50%)';
  h1b.style.fontSize = (37.2 * T / capRatio(h1b)) + 'px';
  h1b.style.transform = 'translateX(-50%) scaleX(' + kA + ')';
  baseline(h1b, 258.5);

  fitBox(sub1, 389 * T, 8.4 * T, 'translateX(-50%)'); baseline(sub1, 300.5);
  fitBox(sub2, 311 * T, 8.4 * T, 'translateX(-50%)'); baseline(sub2, 316.5);
  fitBox(badgeTxt, 184 * T, 9.4 * T, 'translate(2px,-1px)');
  fitBox(wmName, 51 * T, 11.4 * T); baseline(wmName, 38.5);
  fitBox(ctaLabel, 87 * T, 8.9 * T); centreLabel(ctaLabel.parentNode, ctaLabel, 8.9 * T);
  fitBox(vpLabel,  76 * T, 9.5 * T); centreLabel(vpLabel.parentNode,  vpLabel,  9.5 * T);

  links.style.transform = '';
  if (tablet){
    [].forEach.call(links.children, function(a){ a.style.fontSize = ''; });
  } else {
    var fs = 7.9 / capRatio(links.children[0]);
    [].forEach.call(links.children, function(a){ a.style.fontSize = fs + 'px'; });
    var rw = links.getBoundingClientRect().width / k;
    if (rw > 0) links.style.transform = 'scaleX(' + (317 / rw) + ')';
  }
  placeCards();
}
window.hxLayout = layout;

/* ---------- SCALE LAW: k = min(vw/W, vh/560). Dividing by 560, not 657,
   fills the width and lets the mock bleed off the section's bottom edge. ---------- */
function resize(){
  var vw = hx.clientWidth, vh = hx.clientHeight;
  mobile = vw <= 700;
  tablet = !mobile && vw <= TAB_MAX;

  if (mobile){
    k = 1;
    ['--k','--fill','--stshift','--sshift','--rs'].forEach(function(p){ canvas.style.removeProperty(p); });
    layout();
    return;
  }

  var W = CW, fill, ss = 0, rs = 1, st = 0, ramp = 0;
  if (tablet){
    // the design WINDOW narrows so type stops shrinking with the viewport,
    // and k stays continuous across 1080 (no jump at the breakpoint)
    W = DW_MIN + (vw - TAB_MIN) * (CW - DW_MIN) / (TAB_MAX - TAB_MIN);
    if (vh > vw * 1.15) W = Math.min(W, 900);
    ramp = Math.min(1, (TAB_MAX - vw) / 120);
    tboost = 1 + 0.14 * ramp;
  }
  k = Math.min(vw / W, vh / 560);
  fill = Math.max(0, vh / k - CH);
  if (tablet && fill > 0){
    // surplus height shared three ways: wheel+mock travel, wheel scale, hero drop
    ss = Math.min(fill * 0.55, 420) * ramp;
    rs = 1 + Math.min(fill / 1100, 0.75) * ramp;
    st = Math.max(0, (219.5 - 125 * rs + ss) / 2 - 28) * ramp;
    fill -= ss;
  }
  canvas.style.setProperty('--k', k);
  canvas.style.setProperty('--fill', fill + 'px');
  canvas.style.setProperty('--stshift', st + 'px');
  canvas.style.setProperty('--sshift', ss + 'px');
  canvas.style.setProperty('--rs', rs);
  layout();
}

/* ---------- RING LOOP ---------- */
var last = 0;
function tick(t){
  if (!last) last = t;
  var dt = Math.min((t - last) / 1000, 0.1);
  last = t;
  if (!reduce.matches) phase -= SPEED * dt;
  placeCards();
  requestAnimationFrame(tick);
}
document.addEventListener('visibilitychange', function(){ last = 0; });

/* ---------- MENU ---------- */
var nav = document.getElementById('hxnav');
var burger = document.getElementById('burger');
function setMenu(open){
  nav.classList.toggle('open', open);
  burger.setAttribute('aria-expanded', String(open));
}
burger.addEventListener('click', function(e){ e.stopPropagation(); setMenu(!nav.classList.contains('open')); });
document.addEventListener('click', function(e){
  if (nav.classList.contains('open') && !nav.contains(e.target)) setMenu(false);
});
document.addEventListener('keydown', function(e){
  if (e.key === 'Escape' && nav.classList.contains('open')){ setMenu(false); burger.focus(); }
});
document.getElementById('navmenu').addEventListener('click', function(e){
  if (e.target.closest('a')) setMenu(false);
});

/* ---------- WIRING ---------- */
addEventListener('resize', resize);
if (window.visualViewport) window.visualViewport.addEventListener('resize', resize);
if (window.ResizeObserver) new ResizeObserver(function(){ resize(); }).observe(hx);
addEventListener('resize', function(){ if (hx.clientWidth > TAB_MAX || hx.clientWidth <= 700) setMenu(false); });

resize();
if (document.fonts && document.fonts.ready) document.fonts.ready.then(layout);
setTimeout(layout, 400);
setTimeout(layout, 1400);
requestAnimationFrame(tick);

/* ---------- ENTRANCE: runs once, then the hero is still ---------- */
(function intro(){
  var root = document.documentElement;
  function settle(){
    document.getAnimations().forEach(function(a){ if (a.id && a.id.indexOf('intro:') === 0) a.cancel(); });
    root.classList.remove('intro');
  }
  if (!root.classList.contains('intro') || reduce.matches || !Element.prototype.animate){ settle(); return; }

  var phone = hx.clientWidth <= 700;
  var D = phone ? 0.66 : 1;   // phones travel shorter distances
  // Phones also run the whole timeline at half length. The headline is the LCP
  // element and cannot count as painted until its opacity animation finishes,
  // so a leisurely entrance directly inflates Largest Contentful Paint.
  var S = phone ? 0.5 : 1;
  var EXPO = 'cubic-bezier(.16,1,.3,1)', SOFT = 'cubic-bezier(.22,.61,.36,1)';
  var n = 0, lastAnim = null, lastEnd = -1;
  function Y(px){ return '0 ' + (px * D) + 'px'; }
  function play(el, from, dur, delay, ease){
    if (!el) return;
    dur *= S; delay *= S;
    var to = {opacity: 1};
    if (from.translate) to.translate = '0 0';
    if (from.scale)     to.scale = '1';
    if (from.clipPath)  to.clipPath = 'inset(-30% 0 -30% 0)';
    var a = el.animate([from, to], {duration: dur, delay: delay, easing: ease, fill: 'both'});
    a.id = 'intro:' + (n++);
    if (delay + dur > lastEnd){ lastEnd = delay + dur; lastAnim = a; }
  }
  var q = function(s){ return hx.querySelector(s); };
  play(nav, {opacity: 0, translate: Y(-9)}, 620, 60, EXPO);
  play(q('.mark'), {opacity: 0, translate: Y(6)}, 520, 150, SOFT);
  play(q('.wm'),   {opacity: 0, translate: Y(6)}, 520, 185, SOFT);
  [].forEach.call(links.children, function(a, i){ play(a, {opacity: 0, translate: Y(6)}, 460, 215 + i * 45, SOFT); });
  play(burger, {opacity: 0, translate: Y(6)}, 460, 300, SOFT);
  play(q('.hx-nav .hx-btn'), {opacity: 0, translate: Y(6)}, 500, 400, SOFT);
  play(q('.badge'), {opacity: 0, translate: Y(11), scale: '.985'}, 560, 270, EXPO);
  play(h1a, {opacity: 0, translate: Y(15), clipPath: 'inset(100% 0 -30% 0)'}, 900, 380, EXPO);
  play(h1b, {opacity: 0, translate: Y(15), clipPath: 'inset(100% 0 -30% 0)'}, 900, 470, EXPO);
  play(sub1, {opacity: 0, translate: Y(10)}, 620, 690, EXPO);
  play(sub2, {opacity: 0, translate: Y(10)}, 620, 745, EXPO);
  play(q('.cta2'), {opacity: 0, translate: Y(13), scale: '.985'}, 620, 830, EXPO);
  play(ring, {opacity: 0, translate: Y(18), scale: '.99'}, 950, 700, EXPO);
  play(document.getElementById('browser'), {opacity: 0, translate: Y(26)}, 900, 900, EXPO);
  if (lastAnim) lastAnim.finished.then(settle).catch(settle); else settle();
})();

})();
