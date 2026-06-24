const CACHE_NAME = 'lode-app-v4';
const STATIC_ASSETS = [
    './',
    './index.html',
    './icon.png',
    './manifest.json',
    'https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4',
    'https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js'
];
const CSV_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRJvRESTof_RVpmAyb5vkGX7mAweXbXESyE3BaaX81f4YS3PCo_4c395DvcP7q-iBwr59diu4DLzzCt/pub?gid=1040693821&single=true&output=csv';

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

self.addEventListener('fetch', (e) => {
    if (e.request.url.includes('docs.google.com/spreadsheets')) {
        // Stale-While-Revalidate per i dati CSV
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
        // Cache-First per le risorse statiche
        e.respondWith(
            caches.match(e.request).then((response) => {
                return response || fetch(e.request).then((networkResponse) => {
                    if (e.request.method === 'GET' && e.request.url.startsWith('http')) {
                        return caches.open(CACHE_NAME).then((cache) => {
                            cache.put(e.request, networkResponse.clone());
                            return networkResponse;
                        });
                    }
                    return networkResponse;
                }).catch(() => {
                    // Ignora errori offline per file non essenziali
                });
            })
        );
    }
});