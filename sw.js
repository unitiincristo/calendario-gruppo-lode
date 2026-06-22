self.addEventListener('install', (e) => {
  console.log('[Service Worker] Installato');
});
self.addEventListener('fetch', (e) => {
  // Lascia passare tutte le richieste (ci serve per Google Sheets)
});