/* Service worker: salva l'app sul telefono così si apre anche senza campo.
   Quando pubblichi una versione nuova, aumenta il numero qui sotto. */
const CACHE = 'diario-palestra-v2';
const SHELL = ['./', './index.html', './firebase-config.js', './manifest.webmanifest', './icon.svg', './icon-192.png',
  './vendor/firebase-app-compat.js', './vendor/firebase-auth-compat.js', './vendor/firebase-firestore-compat.js'];
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL))); self.skipWaiting(); });
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const req = e.request, u = new URL(req.url);
  if (req.method !== 'GET') return;
  const fonts = u.hostname === 'fonts.googleapis.com' || u.hostname === 'fonts.gstatic.com';
  if (!(u.origin === self.location.origin || fonts) || u.pathname.startsWith('/__/')) return;
  // Rete prima (così vedi subito gli aggiornamenti), copia salvata se sei offline.
  e.respondWith(fetch(req).then(r => {
    if (r && (r.ok || r.type === 'opaque')) { const c = r.clone(); caches.open(CACHE).then(k => k.put(req, c)); }
    return r;
  }).catch(() => caches.match(req).then(hit => hit || caches.match('./index.html'))));
});
