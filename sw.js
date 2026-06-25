const CACHE_NAME = 'omnibot-v7-cache-v1';

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

// Cache first, falling back to network strategy for all GET requests (including CDNs)
self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  
  // Skip caching for API requests (like Gemini/OpenRouter API endpoints)
  const url = new URL(event.request.url);
  if (url.hostname.includes('googleapis.com') || url.hostname.includes('openrouter.ai') || url.hostname.includes('groq.com')) {
      return;
  }

  event.respondWith(
    caches.match(event.request).then(cachedResponse => {
      if (cachedResponse) {
        return cachedResponse;
      }
      
      return fetch(event.request).then(networkResponse => {
        // Don't cache if not a valid response or if it's an opaque cross-origin response that failed
        if (!networkResponse || networkResponse.status !== 200 || networkResponse.type !== 'basic' && networkResponse.type !== 'cors') {
          return networkResponse;
        }

        // Clone the response because it can only be consumed once
        const responseToCache = networkResponse.clone();
        caches.open(CACHE_NAME).then(cache => {
          cache.put(event.request, responseToCache);
        });

        return networkResponse;
      }).catch(() => {
          // If network fails and we don't have it in cache, we just fail gracefully
          return new Response('Offline: Resource not available in cache.', {
              status: 503,
              statusText: 'Service Unavailable'
          });
      });
    })
  );
});
