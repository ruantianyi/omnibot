const CACHE_NAME = 'anthocyan-v7-cache-v2';

const urlsToCache = [
  './7.0.html',
  './manifest.json'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache).catch(err => {
            console.warn('Some static assets could not be cached:', err);
        });
      })
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Network first, falling back to cache strategy for all GET requests to ensure updates
self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  
  // Skip caching for API requests (like Gemini/OpenRouter API endpoints)
  const url = new URL(event.request.url);
  if (url.hostname.includes('googleapis.com') || url.hostname.includes('openrouter.ai') || url.hostname.includes('groq.com')) {
      return;
  }

  event.respondWith(
    fetch(event.request).then(networkResponse => {
      if (!networkResponse || networkResponse.status !== 200 || networkResponse.type !== 'basic' && networkResponse.type !== 'cors') {
        return networkResponse;
      }
      const responseToCache = networkResponse.clone();
      caches.open(CACHE_NAME).then(cache => {
        cache.put(event.request, responseToCache);
      });
      return networkResponse;
    }).catch(() => {
      return caches.match(event.request).then(cachedResponse => {
        if (cachedResponse) {
          return cachedResponse;
        }
        return new Response('Offline: Resource not available in cache.', {
            status: 503,
            statusText: 'Service Unavailable'
        });
      });
    })
  );
});
