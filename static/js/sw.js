let cacheName = 'easybook';
let filesToCache = [
    '/auth/login',
    '/',
    '/prenotazioni',
    '/static/css/Homepage1.css',
    '/static/css/navbar.css',
    '/static/css/universal.css',
    '/static/css/bootstrap.css',
    'static/css/owl.carousel.min.css',
    '/static/js/bootstrap.js',
    '/static/js/owl.carousel.min.js',
    'static/js//popper.min.js',
    'static/js/main.js'
];
/* Start the service worker and cache all of the app's content */
self.addEventListener('install', function(e) {
    e.waitUntil(
        caches.open(cacheName).then(function(cache) {
            return cache.addAll(filesToCache);
        })
    );
});

/* Serve cached content when offline */
self.addEventListener('fetch', function(e) {
    e.respondWith(
        caches.match(e.request).then(function(response) {
            return response || fetch(e.request);
        })
    );
});
