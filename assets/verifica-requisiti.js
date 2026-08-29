/* ═══════════════════════════════════════════════════════════════
   Verificatore requisiti — componente condiviso

   Usato da finanziamenti.dc.html e da blog-corsi-gratuiti-calabria.html.
   Una sola copia della logica: se cambiano le regole sui finanziamenti
   si aggiorna qui e cambia ovunque.

   USO
   <div id="verificaRequisiti" data-tema="chiaro|scuro"></div>
   <script src="assets/verifica-requisiti.js" defer></script>

   Il tema decide solo i colori: "scuro" per fondi scuri (l'articolo del
   blog), "chiaro" per fondi crema (la pagina finanziamenti).
   ═══════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  var root = document.getElementById('verificaRequisiti');
  if (!root) return;

  var scuro = (root.dataset.tema || 'scuro') === 'scuro';

  // ── palette ──
  var C = scuro ? {
    testo: '#F7F3EC', testoSoft: 'rgba(247,243,236,.8)', oro: '#B8925A',
    optBg: 'rgba(247,243,236,.07)', optBd: 'rgba(247,243,236,.18)',
    optBgH: 'rgba(247,243,236,.14)', barBg: 'rgba(247,243,236,.16)',
    liSoft: 'rgba(247,243,236,.88)', btnGhostBd: 'rgba(247,243,236,.3)',
    noBg: 'rgba(247,243,236,.16)', noFg: '#F7F3EC', again: 'rgba(247,243,236,.55)'
  } : {
    testo: '#4A2B25', testoSoft: '#5c4038', oro: '#8A4B3A',
    optBg: '#FBF8F2', optBd: 'rgba(74,43,37,.14)',
    optBgH: '#fff', barBg: 'rgba(74,43,37,.1)',
    liSoft: '#5c4038', btnGhostBd: 'rgba(74,43,37,.22)',
    noBg: 'rgba(74,43,37,.1)', noFg: '#4A2B25', again: '#8C8478'
  };

  // ── stile, iniettato una volta sola ──
  if (!document.getElementById('vr-style')) {
    var st = document.createElement('style');
    st.id = 'vr-style';
    st.textContent = [
      '.vr__k{font-size:11.5px;font-weight:600;letter-spacing:.22em;text-transform:uppercase;color:' + C.oro + ';margin-bottom:14px}',
      '.vr__t{font-family:"Playfair Display",serif;font-weight:600;font-size:clamp(24px,3.4vw,40px);line-height:1.08;margin:0 0 12px;color:' + C.testo + '}',
      '.vr__s{font-size:15.5px;line-height:1.6;color:' + C.testoSoft + ';margin:0 0 28px;max-width:52ch}',
      '.vr__bar{height:4px;background:' + C.barBg + ';border-radius:100px;overflow:hidden;margin-bottom:28px}',
      '.vr__bar i{display:block;height:100%;background:' + C.oro + ';border-radius:100px;transition:width .5s cubic-bezier(.16,1,.3,1)}',
      '.vr__qn{font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:' + C.oro + ';margin-bottom:12px}',
      '.vr__qt{font-family:"Playfair Display",serif;font-size:clamp(20px,2.6vw,28px);line-height:1.2;margin:0 0 22px;color:' + C.testo + '}',
      '.vr__opts{display:grid;gap:11px}',
      '.vr__opt{display:flex;align-items:center;gap:14px;text-align:left;background:' + C.optBg + ';border:1.5px solid ' + C.optBd + ';border-radius:13px;padding:16px 20px;color:' + C.testo + ';font-size:15.5px;font-family:inherit;cursor:pointer;transition:background .25s,border-color .25s,transform .25s}',
      '.vr__opt:hover{background:' + C.optBgH + ';border-color:' + C.oro + ';transform:translateX(4px)}',
      '.vr__i{width:26px;height:26px;border-radius:50%;border:1.5px solid ' + C.optBd + ';display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:600;flex:none;color:' + C.oro + '}',
      '.vr__back{background:none;border:0;color:' + C.again + ';font-size:13.5px;margin-top:20px;padding:6px 0;text-decoration:underline;cursor:pointer;font-family:inherit}',
      '.vr__res{animation:vrFade .5s cubic-bezier(.16,1,.3,1) both}',
      '@keyframes vrFade{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}',
      '.vr__badge{display:inline-flex;align-items:center;gap:9px;font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;padding:9px 18px;border-radius:100px;margin-bottom:18px}',
      '.vr__rt{font-family:"Playfair Display",serif;font-size:clamp(23px,3.2vw,38px);line-height:1.1;margin:0 0 14px;color:' + C.testo + '}',
      '.vr__rd{font-size:16px;line-height:1.68;color:' + C.testoSoft + ';margin:0 0 24px;max-width:56ch}',
      '.vr__list{list-style:none;padding:0;margin:0 0 28px;display:grid;gap:11px}',
      '.vr__list li{position:relative;padding-left:29px;font-size:15px;line-height:1.55;color:' + C.liSoft + '}',
      '.vr__list li::before{content:"";position:absolute;left:0;top:7px;width:15px;height:15px;border-radius:50%;background:rgba(184,146,90,.3);border:1.5px solid ' + C.oro + '}',
      '.vr__cta{display:flex;flex-wrap:wrap;gap:12px}',
      '.vr__btn{display:inline-flex;align-items:center;gap:9px;font-size:15px;font-weight:600;padding:15px 30px;border-radius:100px;text-decoration:none;transition:transform .28s,background .28s}',
      '.vr__btn:hover{transform:translateY(-2px)}',
      '.vr__btn--gold{background:#B8925A;color:#4A2B25}.vr__btn--gold:hover{background:#D4B482;color:#4A2B25}',
      '.vr__btn--ghost{border:1.5px solid ' + C.btnGhostBd + ';color:' + C.testo + '}.vr__btn--ghost:hover{border-color:' + C.oro + ';color:' + C.oro + '}',
      '.vr__again{background:none;border:0;color:' + C.again + ';font-size:13.5px;margin-top:18px;text-decoration:underline;cursor:pointer;font-family:inherit}',
      '@media(prefers-reduced-motion:reduce){.vr__res{animation:none}.vr__opt,.vr__btn{transition:none}}'
    ].join('\n');
    document.head.appendChild(st);
  }

  var DOMANDE = [
    { t: 'Qual è la tua situazione lavorativa?', o: [
        { l: 'Sono disoccupato/a',     v: 'disoccupato' },
        { l: 'Lavoro come dipendente', v: 'dipendente' },
        { l: 'Sono studente/essa',     v: 'studente' },
        { l: 'Lavoro in proprio',      v: 'autonomo' } ] },
    { t: 'Ricevi uno di questi sostegni?', o: [
        { l: 'Supporto Formazione e Lavoro (SFL)',  v: 'sfl' },
        { l: 'Assegno di Inclusione (ADI)',         v: 'adi' },
        { l: 'NASpI / indennità di disoccupazione', v: 'naspi' },
        { l: 'Nessuno di questi',                    v: 'nessuno' } ] },
    { t: 'Quanti anni hai?', o: [
        { l: 'Meno di 30',  v: 'u30' },
        { l: 'Fra 30 e 59', v: '3059' },
        { l: '60 o più', v: 'o60' } ] },
    { t: 'Sei iscritto/a al Centro per l’Impiego?', o: [
        { l: 'Sì, con dichiarazione di disponibilità', v: 'cpi_si' },
        { l: 'No, non ancora',                                  v: 'cpi_no' },
        { l: 'Non lo so',                                       v: 'cpi_ns' } ] }
  ];

  var risposte = [], idx = 0;

  function esito() {
    var lavoro = risposte[0], sostegno = risposte[1], eta = risposte[2], cpi = risposte[3];
    var r;

    if (sostegno === 'sfl') {
      r = { tipo: 'yes', titolo: 'Sì — e ti pagano anche per studiare.',
        testo: 'Con il <strong>Supporto Formazione e Lavoro</strong> il corso è gratuito e continui a ricevere <strong>500 € al mese</strong> mentre lo frequenti, fino a dodici mesi. Se prosegui con un altro percorso, la misura può essere prorogata.',
        punti: ['Corso interamente gratuito',
                '500 € al mese durante la frequenza',
                'Proroga possibile fino a 12 mesi aggiuntivi',
                'Il corso deve essere registrato nel sistema SIISL — ci pensiamo noi'] };
    } else if (sostegno === 'adi') {
      r = { tipo: 'yes', titolo: 'Sì, con ogni probabilità.',
        testo: 'Chi fa parte di un nucleo con <strong>Assegno di Inclusione</strong> ed è considerato occupabile accede al percorso SFL, e da lì ai corsi gratuiti. Va verificata la tua posizione nel nucleo familiare.',
        punti: ['Corso gratuito attraverso il percorso SFL',
                'Da verificare la tua posizione nel nucleo',
                'Serve il patto di servizio con il Centro per l’Impiego'] };
    } else if (sostegno === 'naspi' || lavoro === 'disoccupato') {
      r = { tipo: 'yes', titolo: 'Sì, rientri fra i destinatari.',
        testo: 'Disoccupati e percettori di NASpI sono il bacino principale del <strong>Programma GOL</strong>. Le disponibilità dipendono dal catalogo regionale aperto in questo momento: la verifichiamo noi, in giornata.',
        punti: ['Corso gratuito tramite Programma GOL',
                'Serve iscrizione al Centro per l’Impiego',
                'Disponibilità legata al catalogo regionale attivo'] };
    } else if (eta === 'u30') {
      r = { tipo: 'yes', titolo: 'Sì — anche se studi o lavori.',
        testo: 'Dal 2023 il <strong>Programma GOL</strong> è aperto agli under 30 anche non NEET. È il punto che sfugge a quasi tutti: non serve essere disoccupati.',
        punti: ['Corso gratuito tramite GOL under 30',
                'Vale anche se studi o hai già un lavoro',
                'Serve comunque il passaggio dal Centro per l’Impiego'] };
    } else if (lavoro === 'dipendente') {
      r = { tipo: 'maybe', titolo: 'Forse — dipende dalla tua azienda.',
        testo: 'Se la tua impresa aderisce a un <strong>fondo interprofessionale</strong> (Fondimpresa, For.Te e altri), la formazione può essere coperta senza costi né per te né per l’azienda. Molti lavoratori non sanno di averne diritto.',
        punti: ['Da verificare l’adesione della tua azienda a un fondo',
                'Se aderisce, il corso è coperto integralmente',
                'In alternativa: rate senza interessi',
                'Possiamo parlarne noi con il tuo datore di lavoro'] };
    } else {
      r = { tipo: 'no', titolo: 'Probabilmente no — ma non finisce qui.',
        testo: 'Dalle risposte non emergono i requisiti per le misure attualmente aperte. Restano due strade concrete: le <strong>rate senza interessi</strong> e i bandi in uscita, che cambiano più spesso di quanto si pensi.',
        punti: ['Pagamento a rate, senza interessi né finanziarie',
                'Il corso OSS si paga in 12 rate da 150 €',
                'Ti avvisiamo appena esce un bando adatto a te',
                'La verifica dei requisiti resta gratuita'] };
    }

    if (cpi === 'cpi_no' && r.tipo === 'yes') {
      r.punti.push('Prima cosa da fare: iscriverti al Centro per l’Impiego. Ti spieghiamo come.');
    }
    return r;
  }

  function intro() {
    return '<div class="vr__k">Verifica in 30 secondi</div>' +
      '<h2 class="vr__t">Hai diritto a un corso gratuito?</h2>' +
      '<p class="vr__s">Nessuna registrazione, nessuna email. Alla fine ti diciamo cosa puoi fare e a chi rivolgerti.</p>' +
      '<div class="vr__bar"><i style="width:25%"></i></div><div id="vrBox"></div>' +
      '<button class="vr__back" id="vrBack" hidden>← Torna alla domanda precedente</button>';
  }

  function disegna() {
    var q = DOMANDE[idx];
    root.querySelector('.vr__bar i').style.width = (idx / DOMANDE.length * 100 + 25) + '%';
    root.querySelector('#vrBack').hidden = (idx === 0);
    root.querySelector('#vrBox').innerHTML =
      '<div class="vr__qn">Domanda ' + (idx + 1) + ' di ' + DOMANDE.length + '</div>' +
      '<h3 class="vr__qt">' + q.t + '</h3><div class="vr__opts">' +
      q.o.map(function (o, i) {
        return '<button type="button" class="vr__opt" data-v="' + o.v + '">' +
               '<span class="vr__i">' + String.fromCharCode(65 + i) + '</span>' + o.l + '</button>';
      }).join('') + '</div>';

    Array.prototype.forEach.call(root.querySelectorAll('.vr__opt'), function (b) {
      b.addEventListener('click', function () {
        risposte[idx] = b.dataset.v;
        idx++;
        if (idx < DOMANDE.length) disegna(); else mostraEsito();
      });
    });
  }

  function mostraEsito() {
    var r = esito();
    var etichetta = r.tipo === 'yes' ? 'Buone notizie'
                  : r.tipo === 'maybe' ? 'Da verificare' : 'Situazione da approfondire';
    var badgeCss = r.tipo === 'yes' ? 'background:#7C8A5A;color:#fff'
                 : r.tipo === 'maybe' ? 'background:#B8925A;color:#4A2B25'
                 : 'background:' + C.noBg + ';color:' + C.noFg;

    root.innerHTML =
      '<div class="vr__res">' +
        '<span class="vr__badge" style="' + badgeCss + '">' + etichetta + '</span>' +
        '<h2 class="vr__rt">' + r.titolo + '</h2>' +
        '<p class="vr__rd">' + r.testo + '</p>' +
        '<ul class="vr__list">' + r.punti.map(function (p) { return '<li>' + p + '</li>'; }).join('') + '</ul>' +
        '<div class="vr__cta">' +
          '<a href="candidati.dc.html" class="vr__btn vr__btn--gold">Fissa un colloquio gratuito →</a>' +
          '<a href="https://wa.me/393935726245" target="_blank" rel="noopener" class="vr__btn vr__btn--ghost">Scrivici su WhatsApp</a>' +
        '</div>' +
        '<button class="vr__again" id="vrAgain">↺ Rifai il test</button>' +
      '</div>';

    if (window.glTrack) window.glTrack('verifica_requisiti', { esito: r.tipo });

    root.querySelector('#vrAgain').addEventListener('click', avvia);
  }

  function avvia() {
    risposte = []; idx = 0;
    root.innerHTML = intro();
    root.querySelector('#vrBack').addEventListener('click', function () {
      if (idx > 0) { idx--; disegna(); }
    });
    disegna();
  }

  avvia();
})();
