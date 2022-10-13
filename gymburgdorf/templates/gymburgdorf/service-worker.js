////// Service Worker for GymBurgdorf website {% load static %}

const offlineUrl = "{% url 'gymburgdorf:error' %}?errorcode=Keine Internetverbindung!&errormsg=Bitte gehe online, um diese Seite anzuzeigen!";
const errorUrl = "{% url 'gymburgdorf:error' %}?errorcode=Error&errormsg=Beim Laden dieser Seite ist ein Fehler aufgetreten!";

const cacheUrls = [
    "{% url 'gymburgdorf:main' %}",

    "{% static 'gymburgdorf/js/main.js' %}",
    "{% static 'gymburgdorf/js/navigation.js' %}",
    "{% static 'gymburgdorf/js/noten.js' %}",
    "{% static 'gymburgdorf/js/panels.js' %}",
    "{% static 'gymburgdorf/js/workermanager.js' %}",

    offlineUrl,
    errorUrl,
]

const cacheName = "gymburgdorf-cache-v1";

//// Install
self.addEventListener('install', e => {
    console.log('[SW] - Install');
    e.waitUntil(
        caches.open(cacheName).then(cache => {
            console.log("[SW] - Install: Caching 'gymburgdorf' urls.");
            return cache.addAll(cacheUrls)
                .then(() => self.skipWaiting());

        })
    );
});

//// Activate
self.addEventListener('activate', event => {
    console.log('[SW] - Activate');
    event.waitUntil(self.clients.claim());
});

//// Fetch

self.addEventListener('fetch', event => {
    console.log("[SW] - Fetch", event.request.url);
    event.respondWith(fetch(event.request));
});