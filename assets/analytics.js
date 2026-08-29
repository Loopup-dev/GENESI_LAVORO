/* ═══════════════════════════════════════════════════════════════
   Genesi Lavoro — Google Analytics 4 + banner consenso (GDPR)

   COSA DEVI FARE PRIMA CHE FUNZIONI
   ---------------------------------
   1. Vai su https://analytics.google.com → Amministrazione → Crea proprietà
   2. Crea un "Flusso di dati" di tipo Web per genesilavoro.it
   3. Copia l'ID di misurazione (formato G-XXXXXXXXXX)
   4. Incollalo qui sotto al posto di G-XXXXXXXXXX
   Finché resta il placeholder, lo script non carica nulla: nessun cookie,
   nessuna chiamata a Google. Il sito funziona lo stesso.

   PERCHE' IL BANNER
   -----------------
   GA4 usa cookie di analisi. In Italia servono consenso preventivo e
   possibilità di rifiutare. Usiamo il Consent Mode v2 di Google: prima
   della scelta i cookie sono negati, dopo si adegua alla risposta.
   ═══════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  var GA_ID = 'G-XXXXXXXXXX';           // ← sostituisci qui
  var STORAGE_KEY = 'gl_consenso_v1';
  var attivo = GA_ID.indexOf('G-') === 0 && GA_ID !== 'G-XXXXXXXXXX';

  /* ── Consent Mode: si dichiara PRIMA di caricare gtag ── */
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;

  gtag('consent', 'default', {
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    analytics_storage: 'denied',
    functionality_storage: 'granted',
    security_storage: 'granted',
    wait_for_update: 500
  });

  function leggiConsenso() {
    try { return localStorage.getItem(STORAGE_KEY); } catch (e) { return null; }
  }
  function salvaConsenso(v) {
    try { localStorage.setItem(STORAGE_KEY, v); } catch (e) {}
  }

  function applicaConsenso(v) {
    gtag('consent', 'update', {
      analytics_storage: v === 'si' ? 'granted' : 'denied',
      ad_storage: 'denied',
      ad_user_data: 'denied',
      ad_personalization: 'denied'
    });
  }

  /* ── Caricamento gtag.js ── */
  var caricato = false;
  function caricaGA() {
    if (caricato || !attivo) return;
    caricato = true;
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
    gtag('js', new Date());
    gtag('config', GA_ID, { anonymize_ip: true });
  }

  /* ── Banner ── */
  function mostraBanner() {
    if (document.getElementById('gl-cookie')) return;

    var css = document.createElement('style');
    css.textContent =
      '#gl-cookie{position:fixed;left:16px;right:16px;bottom:16px;z-index:9998;max-width:660px;margin:0 auto;' +
      'background:#4A2B25;color:#F7F3EC;border-radius:16px;padding:22px 24px;box-shadow:0 20px 50px rgba(0,0,0,.34);' +
      "font-family:'Inter',system-ui,sans-serif;font-size:14px;line-height:1.6;transform:translateY(130%);" +
      'transition:transform .5s cubic-bezier(.16,1,.3,1)}' +
      '#gl-cookie.is-on{transform:translateY(0)}' +
      '#gl-cookie p{margin:0 0 16px}' +
      '#gl-cookie a{color:#D4B482}' +
      '#gl-cookie .r{display:flex;gap:10px;flex-wrap:wrap}' +
      '#gl-cookie button{font:inherit;font-weight:600;font-size:14px;padding:12px 24px;border-radius:100px;' +
      'border:0;cursor:pointer;transition:transform .25s,background .25s}' +
      '#gl-cookie button:hover{transform:translateY(-2px)}' +
      '#gl-ok{background:#B8925A;color:#4A2B25}' +
      '#gl-no{background:transparent;color:#F7F3EC;border:1.5px solid rgba(247,243,236,.3)}' +
      '@media(prefers-reduced-motion:reduce){#gl-cookie{transition:none}}';
    document.head.appendChild(css);

    var box = document.createElement('div');
    box.id = 'gl-cookie';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-label', 'Consenso ai cookie di analisi');
    box.innerHTML =
      '<p>Usiamo cookie di analisi per capire quali corsi vi interessano di più e ' +
      'migliorare il sito. Nessuna pubblicità, nessuna profilazione, nessun dato ceduto a terzi. ' +
      'Puoi rifiutare: il sito funziona esattamente allo stesso modo.</p>' +
      '<div class="r"><button id="gl-ok">Va bene</button>' +
      '<button id="gl-no">Solo i necessari</button></div>';
    document.body.appendChild(box);
    requestAnimationFrame(function () { box.classList.add('is-on'); });

    function chiudi(v) {
      salvaConsenso(v);
      applicaConsenso(v);
      if (v === 'si') caricaGA();
      box.classList.remove('is-on');
      setTimeout(function () { box.remove(); }, 500);
    }
    document.getElementById('gl-ok').addEventListener('click', function () { chiudi('si'); });
    document.getElementById('gl-no').addEventListener('click', function () { chiudi('no'); });
  }

  /* ── Avvio ── */
  var scelta = leggiConsenso();
  if (scelta === 'si') { applicaConsenso('si'); caricaGA(); }
  else if (scelta === 'no') { applicaConsenso('no'); }
  else if (attivo) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', mostraBanner);
    } else { mostraBanner(); }
  }

  /* ═══════════════════════════════════════════════════════════
     EVENTI PERSONALIZZATI
     Sono questi a rispondere alle domande vere: quali corsi
     interessano, quanti compilano i form, da dove arrivano.
     In GA4 li trovi in Report → Coinvolgimento → Eventi.
     ═══════════════════════════════════════════════════════════ */

  function ev(nome, params) {
    if (window.gtag) window.gtag('event', nome, params || {});
  }
  window.glTrack = ev;

  document.addEventListener('DOMContentLoaded', function () {

    /* Quale pagina corso si sta guardando */
    var m = location.pathname.match(/corso-([a-z0-9-]+)\.html/);
    if (m) ev('visualizza_corso', { corso: m[1] });
    if (/seminario-chitarra-baglioni/.test(location.pathname)) {
      ev('visualizza_corso', { corso: 'seminario-baglioni' });
    }

    /* Click sulle card corso: dice cosa attira davvero */
    document.querySelectorAll('a[href*="corso-"], a[href*="seminario-"]').forEach(function (a) {
      a.addEventListener('click', function () {
        var h = a.getAttribute('href') || '';
        var slug = (h.match(/(?:corso-|seminario-)([a-z0-9-]+)\.html/) || [])[1];
        if (slug) ev('click_corso', { corso: slug, da: location.pathname });
      });
    });

    /* Contatti diretti */
    document.querySelectorAll('a[href^="tel:"]').forEach(function (a) {
      a.addEventListener('click', function () { ev('click_telefono'); });
    });
    document.querySelectorAll('a[href*="wa.me"]').forEach(function (a) {
      a.addEventListener('click', function () { ev('click_whatsapp'); });
    });
    document.querySelectorAll('a[href^="mailto:"]').forEach(function (a) {
      a.addEventListener('click', function () { ev('click_email'); });
    });

    /* Invio form: il dato che conta di più */
    document.querySelectorAll('form').forEach(function (f) {
      f.addEventListener('submit', function () {
        var act = f.getAttribute('action') || '';
        var tipo = (act.match(/(?:invia|iscrivi)-([a-z]+)\.php/) || [])[1] || 'sconosciuto';
        ev('invio_form', { tipo: tipo, pagina: location.pathname });
      });
    });

    /* Profondità di lettura: capisce se le pagine vengono lette o abbandonate */
    var soglie = [25, 50, 75, 100], viste = {};
    var onScroll = function () {
      var h = document.documentElement;
      var perc = (h.scrollTop + window.innerHeight) / h.scrollHeight * 100;
      soglie.forEach(function (s) {
        if (perc >= s && !viste[s]) { viste[s] = 1; ev('scroll_' + s); }
      });
      if (viste[100]) window.removeEventListener('scroll', onScroll);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
  });
})();
