const CACHE_NAME = 'qr-pwa-v1';

self.addEventListener('install', (e) => {
    self.skipWaiting();
});

self.addEventListener('activate', (e) => {
    return self.clients.claim();
});

// Network-first Service Worker para no romper los WebSockets de Streamlit
self.addEventListener('fetch', function (event) {
    event.respondWith(
        fetch(event.request).catch(function() {
            return caches.match(event.request);
        })
    );
});
