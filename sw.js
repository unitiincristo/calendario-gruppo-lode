const CACHE_NAME = 'lode-app-v26';
const STATIC_ASSETS = [
    './',
    './index.html',
    './icon.png',
    './manifest.json',
    'https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4',
    'https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js'
];

self.addEventListener('install', (e) => {
    e.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(STATIC_ASSETS);
        })
    );
    self.skipWaiting();
});

self.addEventListener('activate', (e) => {
    e.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cache) => {
                    if (cache !== CACHE_NAME) {
                        return caches.delete(cache);
                    }
                })
            );
        })
    );
    self.clients.claim();
});

self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

self.addEventListener('fetch', (e) => {
    // Network-First per TUTTO (HTML, CSS, JS, e soprattutto il CSV Foglio Google)
    // Questo previene l'effetto "altalena" dove mostrava prima i dati vecchi e poi i nuovi
    e.respondWith(
        fetch(e.request).then((networkResponse) => {
            // Se la rete funziona ed è una GET valida, aggiorniamo la cache
            if (e.request.method === 'GET' && e.request.url.startsWith('http')) {
                const responseClone = networkResponse.clone();
                caches.open(CACHE_NAME).then((cache) => {
                    cache.put(e.request, responseClone);
                });
            }
            return networkResponse;
        }).catch(() => {
            // Se fallisce (utente offline), restituiamo la versione salvata in cache
            return caches.match(e.request);
        })
    );
});