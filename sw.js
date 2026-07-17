// sw.js — Production-ready Service Worker for Aerosol Plant Tracker
const CACHE_NAME = 'aerosol-tracker-v12';
const PRECACHE_URLS = [
  './',
  './index.html',
  './manifest.json',
  './logo_light.png',
  './logo_dark.png',
  './icon-192.png',
  './icon-512.png',
  './apple-touch-icon.png',
  'https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&family=Fraunces:ital,wght@0,300;0,600;1,300&display=swap',
  'https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js'
];
// Install — precache critical assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(PRECACHE_URLS))
      .then(() => self.skipWaiting())
  );
});
// Activate — clean old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
      )
    ).then(() => self.clients.claim())
     .then(() => {
       return self.clients.matchAll({ type: 'window' }).then(clients => {
         clients.forEach(client => client.postMessage({ type: 'SW_UPDATED' }));
       });
     })
  );
});
// Fetch — Stale-While-Revalidate for HTML/CSS/JS, Network-First for API
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  // GitHub API calls — always network, never cache.
  // By returning without calling event.respondWith(), we let the browser handle these cross-origin requests natively.
  // This avoids issues with authorization headers being stripped in standalone PWA/webview modes.
  if (url.hostname === 'api.github.com' || url.hostname === 'raw.githubusercontent.com') {
    return;
  }
  // Google Fonts — Cache-First (fonts rarely change)
  if (url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com') {
    event.respondWith(
      caches.match(event.request).then(cached => {
        if (cached) return cached;
        return fetch(event.request).then(response => {
          if (response.ok) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
          }
          return response;
        });
      })
    );
    return;
  }
  // All other requests — Stale-While-Revalidate
  event.respondWith(
    caches.match(event.request).then(cached => {
      const networkFetch = fetch(event.request).then(response => {
        if (response.ok) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        }
        return response;
      }).catch(() => {
        // If network fails and no cache, return offline fallback
        if (event.request.destination === 'document') {
          return caches.match('./index.html');
        }
        return new Response('', { status: 503, statusText: 'Offline' });
      });
      return cached || networkFetch;
    })
  );
});
