/* Exit card for japanesegrimoire.com
   Same pattern as shingon-reiki.com (gemeinsam/neu/site.js): no pop-up, just a
   small card in the bottom right corner. Shows at the earliest after 8 seconds,
   when the mouse leaves the window at the top or the visitor scrolls back up
   after reading deep into the page. At most once every 30 days, never after a
   sign-up. Sign-up goes to the same Brevo form as the gift on the homepage
   ("The Energy Between Your Hands", Brevo double opt-in), then /thank-you.html.
   Turn off per page: <body data-abschied="aus">. Styles are injected here so
   the card also works on pages with inline CSS only. */
(function () {
  var K = {
    endpoint: 'https://dc276ca0.sibforms.com/serve/MUIFAK3fpJiNFfswdNu2AO5M-RKM1x3FtAWlQZ8fPDXdvGkHoPCiDKbq4X0UmKs6Diz5qE2Gdrkg_vWOYPxgxlvu9Ubd4Vv_lLKNcQEIOBzfN9GgG_UKBUpnVld2k5wvCnIxeJcKPe7LwB6ioMHB8KujB_rg8eiECf-sAEFm8Zp2XSzS8m36istfPoVL69fCpmgT6m_igc1yxSxyBg==?isAjax=1',
    weiter: '/thank-you.html',
    h: 'Before you go: a small gift',
    p: 'The Energy Between Your Hands: a short practice from the Japanese tradition. Two minutes, breath and hands. As a PDF, in your inbox.',
    knopf: 'Send it to me',
    klein: 'One click to confirm, unsubscribe anytime. <a href="/privacy.html">Privacy policy</a>',
    mail: 'you@example.com', mailLabel: 'Email address',
    email: 'Please enter a valid email address.',
    fehler: 'That didn\'t go through. Please try again.',
    sendet: 'Sending…', schliessen: 'Close', geschenk: 'Gift'
  };
  var MERK_ZULETZT = 'jg-abschied', MERK_DRIN = 'jg-eingetragen', MONAT = 30 * 864e5;
  function merk(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }

  var pfad = location.pathname.replace(/\.html$/, '').replace(/\/$/, '');
  if (/(^|\/)(thank-you|confirmed)$/.test(pfad)) { merk(MERK_DRIN, Date.now()); return; }
  if (/(^|\/)(impressum|privacy|shingon-reiki-level-1)$/.test(pfad)) return;
  if (document.body.dataset.abschied === 'aus') return;

  var zuletzt = +merk(MERK_ZULETZT) || 0, drin = +merk(MERK_DRIN) || 0;
  if (drin || Date.now() - zuletzt < MONAT) return;

  var css = '.jg-abschied{position:fixed;right:18px;bottom:18px;z-index:1000;width:min(360px,calc(100vw - 32px));background:#0d0820;color:#f2eee7;border:1px solid rgba(212,168,67,.35);border-radius:16px;box-shadow:0 18px 50px rgba(0,0,0,.55),0 0 40px rgba(131,0,235,.18);padding:22px 22px 16px;font-family:inherit;transform:translateY(130%);transition:transform .45s cubic-bezier(.2,.8,.2,1)}' +
    '.jg-abschied.da{transform:none}' +
    '.jg-abschied h3{font-size:1.15rem;line-height:1.25;margin:0 26px 8px 0;color:#d4a843}' +
    '.jg-abschied p{font-size:.92rem;line-height:1.55;color:rgba(242,238,231,.82);margin:0 0 10px}' +
    '.jg-abschied .zu{position:absolute;top:8px;right:10px;background:none;border:0;font-size:1.5rem;line-height:1;color:rgba(242,238,231,.7);cursor:pointer;padding:4px}' +
    '.jg-abschied form{display:flex;flex-direction:column;gap:10px;margin:0 0 8px}' +
    '.jg-abschied input[type=email]{font:inherit;font-size:1rem;padding:11px 14px;border:1px solid rgba(212,168,67,.35);border-radius:10px;background:#06030f;color:#f2eee7;width:100%;box-sizing:border-box}' +
    '.jg-abschied button[type=submit]{font:inherit;font-weight:700;font-size:.95rem;padding:11px 18px;border:0;border-radius:999px;background:#8300eb;color:#fff;cursor:pointer}' +
    '.jg-abschied button[type=submit]:disabled{opacity:.7;cursor:default}' +
    '.jg-abschied .meldung{font-size:.88rem;font-weight:700;color:#f2eee7;margin:0}' +
    '.jg-abschied .klein{font-size:.78rem;margin:0;color:rgba(242,238,231,.65)}.jg-abschied .klein a{color:inherit}' +
    '.jg-abschied a:focus-visible,.jg-abschied button:focus-visible,.jg-abschied input:focus-visible{outline:3px solid #d4a843;outline-offset:2px}' +
    '@media (prefers-reduced-motion:reduce){.jg-abschied{transition:none}}';

  var start = Date.now(), gezeigt = false;
  var karte = document.createElement('aside');
  karte.className = 'jg-abschied'; karte.setAttribute('aria-label', K.geschenk);
  karte.innerHTML = '<button class="zu" type="button" aria-label="' + K.schliessen + '">×</button>' +
    '<h3>' + K.h + '</h3><p>' + K.p + '</p>' +
    '<form novalidate><input type="email" name="email" required maxlength="200" autocomplete="email" placeholder="' + K.mail + '" aria-label="' + K.mailLabel + '">' +
    '<button type="submit">' + K.knopf + '</button>' +
    '<p class="meldung" role="status" aria-live="polite" hidden></p></form>' +
    '<p class="klein">' + K.klein + '</p>';

  function verbinde() {
    var f = karte.querySelector('form'), knopf = f.querySelector('button'), feld = f.querySelector('input[type=email]'),
      meldung = f.querySelector('.meldung'), text = knopf.textContent;
    function zeigeFehler(t) { meldung.textContent = t; meldung.hidden = false; }
    f.addEventListener('submit', function (e) {
      e.preventDefault(); meldung.hidden = true;
      var w = String(feld.value || '').trim();
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(w)) { zeigeFehler(K.email); feld.focus(); return; }
      knopf.disabled = true; knopf.textContent = K.sendet;
      var fd = new FormData(); fd.append('EMAIL', w); fd.append('email_address_check', ''); fd.append('locale', 'en');
      fetch(K.endpoint, { method: 'POST', body: fd, headers: { 'Accept': 'application/json' } })
        .then(function (r) {
          return r.json().catch(function () { return {}; }).then(function (d) {
            if (r.ok && !(d && d.success === false)) { merk(MERK_DRIN, Date.now()); location.href = K.weiter; return; }
            knopf.disabled = false; knopf.textContent = text; zeigeFehler(K.fehler);
          });
        })
        .catch(function () { knopf.disabled = false; knopf.textContent = text; zeigeFehler(K.fehler); });
    });
  }
  function zeige() {
    if (gezeigt || Date.now() - start < 8000) return;
    gezeigt = true;
    var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
    document.body.appendChild(karte); verbinde();
    requestAnimationFrame(function () { requestAnimationFrame(function () { karte.classList.add('da'); }); });
    merk(MERK_ZULETZT, Date.now());
  }
  function weg() { karte.classList.remove('da'); }
  karte.addEventListener('click', function (e) { if (e.target.classList.contains('zu')) weg(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') weg(); });
  document.addEventListener('mouseout', function (e) { if (!e.relatedTarget && e.clientY <= 0) zeige(); });
  var tiefste = 0;
  window.addEventListener('scroll', function () {
    var y = window.scrollY, h = document.documentElement.scrollHeight - innerHeight;
    if (y > tiefste) tiefste = y;
    if (h > 0 && tiefste / h > .55 && tiefste - y > 350) zeige();
  }, { passive: true });
})();
