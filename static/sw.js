const CACHE_NAME = 'agrivision-v1';

// Install event
self.addEventListener('install', (e) => {
    console.log('[Service Worker] Installed');
});

// Fetch event (Basic pass-through for now)
self.addEventListener('fetch', (e) => {
    e.respondWith(fetch(e.request).catch(() => new Response("Offline mode active.")));
});