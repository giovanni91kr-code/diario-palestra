# Genera la versione Firebase (login email/password + database online) a partire da app.html.
# Uso: python3 build_firebase.py   ->  crea/aggiorna la cartella firebase/public
import re, pathlib

ROOT = pathlib.Path(__file__).parent
src = (ROOT / 'app.html').read_text(encoding='utf-8')
OUT = ROOT / 'firebase' / 'public'
OUT.mkdir(parents=True, exist_ok=True)

def rep(s, a, b):
    assert s.count(a) == 1, ('pattern non trovato o multiplo', a[:70])
    return s.replace(a, b)

HEAD = """<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#1052FF">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Palestra">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon-v2.svg" type="image/svg+xml">
<link rel="icon" href="favicon-v2.png" type="image/png" sizes="64x64">
<link rel="apple-touch-icon" href="icon-v2-180.png">
<script src="vendor/firebase-app-compat.js"></script>
<script src="vendor/firebase-auth-compat.js"></script>
<script src="vendor/firebase-firestore-compat.js"></script>
<script src="firebase-config.js"></script>
</head>
<body>
"""

GATE_CSS = """
/* schermata di accesso */
.gate{position:fixed;inset:0;z-index:60;background:var(--bg);overflow:auto;padding:calc(40px + env(safe-area-inset-top,0px)) 16px 40px}
.gate-in{max-width:400px;margin:0 auto;display:flex;flex-direction:column;gap:14px}
.gate .brand{font-size:34px}
.gate-card{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:18px 16px;box-shadow:var(--shadow)}
.gate-card .field{margin-top:6px}
.gate-card label{display:block;margin-top:12px;font-size:13px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.06em}
.gate-msg{min-height:20px;font-size:14px;font-weight:500;margin-top:10px}
.gate-msg.err{color:var(--down)} .gate-msg.ok{color:var(--up)}
.gate code{background:var(--surface2);padding:2px 6px;border-radius:6px;font-size:14px}
"""

GATE_HTML = """
<div class="gate" id="gate"><div class="gate-in">
  <div class="brand">Diario <span>Palestra</span></div>
  <p class="muted" style="margin:0">Il tuo registro allenamenti, su tutti i tuoi dispositivi.</p>
  <div id="gate-body"><p class="muted">Caricamento…</p></div>
</div></div>
"""

FB_CLOUD = r"""/* ---- Cloud: Firebase (login email/password + Firestore) ----
   I dati stanno in users/<tuo id>/data/<documento>: solo tu puoi leggerli e scriverli (vedi firestore.rules). */
const FB = {auth: null, db: null, user: null};
function withTimeout(p, ms = 12000){ return Promise.race([p, new Promise((_, r) => setTimeout(() => r({code: 'unavailable'}), ms))]); }
function wrapCol(col){
  return {
    doc: k => ({set: b => withTimeout(col.doc(k).set(b)), delete: () => withTimeout(col.doc(k).delete())}),
    limit: n => ({get: () => withTimeout(col.limit(n).get())})
  };
}
function resetLocal(){
  S = {v: 2, plans: defaultPlans(), library: defaultLibrary(), plansUpdatedAt: 0, sessions: [], settings: {rest: 90}};
  D = null; P = [];
  LS.set('dp.state', S); LS.del('dp.draft'); LS.set('dp.pending', P);
}
async function cloudInit(){
  const cfg = window.FIREBASE_CONFIG || {};
  if (!cfg.apiKey || /INCOLLA/.test(cfg.apiKey)) return showGate('setup');
  if (!window.firebase) { if (LS.get('dp.owner', null)) { hideGate(); return setSync('offline'); } return showGate('offline'); }
  try {
    firebase.initializeApp(cfg);
    FB.auth = firebase.auth(); FB.auth.languageCode = 'it';
    FB.db = firebase.firestore();
    try { FB.db.settings({ignoreUndefinedProperties: true, merge: true}); } catch (e) {}
  } catch (e) { return showGate('setup'); }
  FB.auth.onAuthStateChanged(user => {
    FB.user = user;
    if (!user) { C.col = null; setSync('local'); return showGate('login'); }
    const owner = LS.get('dp.owner', null);
    if (owner && owner !== user.uid) resetLocal();     // un altro account su questo dispositivo
    LS.set('dp.owner', user.uid);
    C.col = wrapCol(FB.db.collection('users').doc(user.uid).collection('data'));
    hideGate(); if (D) view = 'workout'; render(); sync();
  });
}

/* ---- Schermata di accesso ---- */
let gateMode = 'login';
const AUTH_ERR = {
  'auth/invalid-credential': 'Email o password non corrette.', 'auth/wrong-password': 'Email o password non corrette.',
  'auth/user-not-found': 'Nessun account con questa email.', 'auth/invalid-email': 'Email non valida.',
  'auth/email-already-in-use': 'Esiste già un account con questa email: usa Accedi.',
  'auth/weak-password': 'La password deve avere almeno 6 caratteri.', 'auth/missing-password': 'Scrivi la password.',
  'auth/too-many-requests': 'Troppi tentativi. Riprova tra qualche minuto.',
  'auth/network-request-failed': 'Nessuna connessione. Controlla la rete e riprova.',
  'auth/operation-not-allowed': 'Login con email non attivo: abilitalo in Firebase → Authentication.',
  'auth/unauthorized-domain': 'Questo indirizzo non è autorizzato: aggiungilo in Firebase → Authentication → Impostazioni → Domini autorizzati.'
};
function showGate(mode){ gateMode = mode; $('#gate').hidden = false; renderGate(); }
function hideGate(){ $('#gate').hidden = true; }
function renderGate(){
  const b = $('#gate-body');
  if (gateMode === 'setup') { b.innerHTML = `<div class="gate-card"><h2>Manca la configurazione</h2><p class="muted">Apri il file <code>firebase-config.js</code> e incolla i codici del tuo progetto Firebase, come spiegato nella guida (passo 3).</p></div>`; return; }
  if (gateMode === 'offline') { b.innerHTML = `<div class="gate-card"><h2>Nessuna connessione</h2><p class="muted">Per il primo accesso su questo dispositivo serve internet. Dopo, l'app funziona anche offline.</p><div class="stack"><button class="btn" onclick="location.reload()">Riprova</button></div></div>`; return; }
  const reg = gateMode === 'register', reset = gateMode === 'reset';
  b.innerHTML = `${reset ? '' : `<div class="seg" role="group"><button data-a="gate-mode" data-m="login" aria-pressed="${!reg}">Accedi</button><button data-a="gate-mode" data-m="register" aria-pressed="${reg}">Registrati</button></div>`}
    <form class="gate-card" id="auth-form" method="post" action="#" novalidate>
      <h2>${reset ? 'Recupera password' : reg ? 'Crea il tuo account' : 'Bentornato'}</h2>
      ${reset ? '<p class="muted small">Ti mandiamo un link per scegliere una nuova password.</p>' : ''}
      <label for="au-email">Email</label>
      <input class="field" id="au-email" name="username" type="email" autocomplete="username" autocapitalize="none" spellcheck="false" inputmode="email" required value="${esc(LS.get('dp.lastEmail', '') || '')}">
      ${reset ? '' : `<label for="au-pass">Password</label>
      <input class="field" id="au-pass" name="password" type="password" autocomplete="${reg ? 'new-password' : 'current-password'}" required minlength="6" placeholder="${reg ? 'Almeno 6 caratteri' : ''}">`}
      <div class="gate-msg" id="gate-msg" role="status"></div>
      <div class="stack" style="margin-top:6px"><button class="btn big" type="submit" id="au-go">${reset ? 'Invia link' : reg ? 'Registrati' : 'Accedi'}</button></div>
      ${reset ? '<button type="button" class="link" data-a="gate-mode" data-m="login" style="margin-top:10px">← Torna ad Accedi</button>'
        : reg ? '' : '<button type="button" class="link" data-a="gate-mode" data-m="reset" style="margin-top:10px">Password dimenticata?</button>'}
    </form>`;
}
function gateMsg(t, ok){ const m = $('#gate-msg'); if (m) { m.textContent = t; m.className = 'gate-msg ' + (ok ? 'ok' : 'err'); } }
document.addEventListener('submit', async ev => {
  if (ev.target.id !== 'auth-form') return;
  ev.preventDefault();
  if (!FB.auth) return gateMsg('Firebase non è pronto: ricarica la pagina.');
  const email = ($('#au-email').value || '').trim(), pass = $('#au-pass') ? $('#au-pass').value : '';
  if (!email) return gateMsg('Scrivi la tua email.');
  LS.set('dp.lastEmail', email);
  const btn = $('#au-go'), label = btn.textContent; btn.disabled = true; btn.textContent = 'Attendere…'; gateMsg('', true);
  try {
    if (gateMode === 'reset') { await FB.auth.sendPasswordResetEmail(email); gateMsg('Fatto: controlla la posta (anche lo spam).', true); }
    else {
      if (gateMode === 'register') await FB.auth.createUserWithEmailAndPassword(email, pass);
      else await FB.auth.signInWithEmailAndPassword(email, pass);
      // Chiede al browser di salvare la password (Chrome/Android); poi toglie il modulo:
      // così anche Safari/iPhone riconosce l'accesso riuscito e propone "Salva password" nel Portachiavi.
      try { if (window.PasswordCredential) await navigator.credentials.store(new PasswordCredential({id: email, password: pass, name: email})); } catch (e2) {}
      const form = $('#auth-form'); if (form) form.remove();
      return;
    }
  } catch (e) { gateMsg(AUTH_ERR[e && e.code] || 'Qualcosa non ha funzionato. Riprova.'); }
  if (btn.isConnected) { btn.disabled = false; btn.textContent = label; }
});

const SYNC_SHORT = {"""

EXTRA_ACTIONS = r"""/* ---- Azioni account (versione Firebase) ---- */
Object.assign(ACT, {
  'gate-mode': b => { gateMode = b.dataset.m; renderGate(); const f = $('#au-email'); if (f && !f.value) f.focus(); },
  logout: async () => {
    if (P.length) { toast('Aspetta la sincronizzazione (serve internet), poi esci'); sync(); return; }
    if (D) { toast('Chiudi o annulla prima l\'allenamento in corso'); return; }
    await FB.auth.signOut(); resetLocal(); LS.del('dp.owner'); view = 'home'; render();
  }
});
if ('serviceWorker' in navigator && location.protocol === 'https:') navigator.serviceWorker.register('sw.js').catch(() => {});

/* ---------- 8. AVVIO ---------- */"""

s = src
# CSS e markup
s = rep(s, '@media (prefers-reduced-motion: reduce)', GATE_CSS + '@media (prefers-reduced-motion: reduce)')
s = rep(s, '<div class="toast" id="toast" hidden></div>', '<div class="toast" id="toast" hidden></div>' + GATE_HTML)
# sostituisce il collegamento al cloud di Claude con Firebase
a = s.index('async function cloudInit(){'); b = s.index('const SYNC_SHORT = {')
s = s[:a] + FB_CLOUD + s[b + len('const SYNC_SHORT = {'):]
s = rep(s, "local: 'Solo locale'", "local: 'Non connesso'")
s = rep(s, "local: ['Solo su questo dispositivo', 'I dati sono salvati nel browser di questo telefono. Esporta un backup JSON ogni tanto per sicurezza.'],",
           "local: ['Non connesso', 'Accedi con il tuo account per salvare il registro online.'],")
s = rep(s, "nel tuo account Claude: lo ritrovi da qualsiasi dispositivo.", "nel tuo account: fai login con la stessa email su un altro dispositivo e ritrovi tutto.")
# card account nella sezione Dati
s = rep(s, '<h1 class="title">Impostazioni</h1>',
        '<h1 class="title">Impostazioni</h1>\n    <section class="card"><h2>Account</h2><p class="muted">Accesso come <b>${esc(FB.user ? FB.user.email : \'\')}</b>. Usa la stessa email e password su un altro dispositivo per ritrovare tutto lo storico.</p>\n      <button class="btn-ghost sm danger" data-a="logout" data-confirm="Tocca di nuovo per uscire">Esci</button></section>')
s = rep(s, "Il backup JSON serve per ripristinare tutto.", "Il backup JSON serve per ripristinare tutto o per portare qui i dati della versione su Claude (Importa backup).")
# azioni extra + service worker prima dell'avvio
s = rep(s, '/* ---------- 8. AVVIO ---------- */', EXTRA_ACTIONS)
# all'avvio: se nessun account è mai entrato su questo dispositivo, mostra subito la schermata di accesso
s = rep(s, "if (D) view = 'workout';\nrender();\ncloudInit();",
        "if (D) view = 'workout';\nrender();\nif (LS.get('dp.owner', null)) hideGate();\ncloudInit();")

(OUT / 'index.html').write_text(HEAD + s + '\n</body>\n</html>\n', encoding='utf-8')
print('firebase/public/index.html creato')
