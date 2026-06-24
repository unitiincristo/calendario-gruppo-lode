const CACHE_NAME = 'lode-app-v6';
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
    if (e.request.url.includes('docs.google.com/spreadsheets')) {
        // Stale-While-Revalidate per i dati CSV (Foglio Google)
        e.respondWith(
            caches.open(CACHE_NAME).then((cache) => {
                return cache.match(e.request).then((cachedResponse) => {
                    const fetchPromise = fetch(e.request).then((networkResponse) => {
                        cache.put(e.request, networkResponse.clone());
                        return networkResponse;
                    }).catch(() => {
                        return cachedResponse;
                    });
                    return cachedResponse || fetchPromise;
                });
            })
        );
    } else {
        // Network-First per l'interfaccia (HTML, CSS, JS) e icone
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
                // Se fallisce (utente offline), restituiamo la versione in cache
                return caches.match(e.request);
            })
        );
    }
});