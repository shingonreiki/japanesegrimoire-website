/* Shingon Reiki Level 1: Termine live aus ablefy über https://www.shingon-reiki.com/api/termine.
   Zeigt alle englischen Level-1-Termine (Mark und Eileen), nur buchbare. Der Button führt auf die
   ablefy-Produktseite. Ohne Termin: ein leiser Hinweis auf die kostenlose Praxis per E-Mail.
   In Netlify-Vorschauen lässt sich mit ?api=<Vorschau-Host von shingon-reiki-website> die
   Vorschau der Schnittstelle einhängen. */
(function () {
  var liste = document.getElementById('termine-liste');
  if (!liste || !window.fetch) return;
  var API = 'https://www.shingon-reiki.com';
  try {
    if (/netlify\.app$/.test(location.hostname)) {
      var q = (location.search.match(/[?&]api=([a-z0-9.-]+)/) || [])[1];
      if (q && /^shingon-reiki-website-[a-z0-9-]+\.vercel\.app$/.test(q)) API = 'https://' + q;
    }
  } catch (e) { /* Live-Schnittstelle */ }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function istLevel1(ev) { return ev.lang === 'en' && (ev.stufe === 'sr1' || /level[\s-]*1\b/i.test(ev.name || ev.titel || '')); }
  function link(ev) { return ev.url + (ev.anbieter ? '' : '?locale=en'); }
  function zeige(d) {
    var j = Date.now(), termine = [];
    (d.events || []).filter(istLevel1).forEach(function (ev) {
      (ev.termine || []).forEach(function (t) { if (new Date(t.ende || t.start).getTime() > j) termine.push([t, ev]); });
    });
    termine.sort(function (a, b) { return a[0].start < b[0].start ? -1 : 1; });
    if (!termine.length) {
      document.querySelector('#termine h2').textContent = 'The next date is not set yet';
      liste.innerHTML = '<p class="leise">New dates go out first to the people on the <a href="/#join">free practice email</a>.</p>';
      var f = document.getElementById('termine-fein'); if (f) f.hidden = true;
      return;
    }
    liste.innerHTML = termine.map(function (x) {
      var t = x[0], ev = x[1], eileen = ev.anbieter === 'eileen';
      return '<div class="termin">' +
        '<div class="mit">' + (eileen ? 'With Eileen Wiesmann' : 'With Dr. Mark Hosak') + '</div>' +
        '<div class="when">' + esc(t.datum_en) + '</div>' +
        '<div class="when-note">Live online · ' + esc((t.zeit_en || '') + (t.us_kurz_en ? ' (' + t.us_kurz_en + ')' : '')) + '</div>' +
        '<a class="btn" href="' + esc(link(ev)) + '">' + (eileen ? 'See Eileen’s event' : 'Take my place') + '</a></div>';
    }).join('');
  }
  fetch(API + '/api/termine').then(function (r) { if (!r.ok) throw 0; return r.json(); })
    .then(function (d) { try { localStorage.setItem('jg-termine', JSON.stringify(d)); } catch (e) {} zeige(d); })
    .catch(function () { var alt = null; try { alt = JSON.parse(localStorage.getItem('jg-termine') || 'null'); } catch (e) {} if (alt) zeige(alt); });
})();
