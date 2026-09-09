/* Service worker for doesplaydice.com.
 *
 * Why this exists: the launch is a convention hall, and convention wifi is
 * reliably terrible. Someone scans the QR at the table once and the rules
 * should keep working for the rest of the weekend, on the floor, in the queue,
 * on the drive home.
 *
 * Strategy, and the choice matters while the site is still changing daily:
 *
 *   documents  network first, cache as fallback. Jeff edits a page, pushes,
 *              and sees the new version -- a cache-first shell would show him
 *              yesterday's text and he would reasonably conclude the site was
 *              broken. Offline, the cached copy is served instead.
 *   assets     stale-while-revalidate. Served from cache instantly, then
 *              refetched in the background so the next load is current.
 *
 *              This started as plain cache-first, which was wrong and I caught
 *              it by shipping it: extra.v3.css is versioned by hand rather than
 *              fingerprinted, so cache-first pinned one copy permanently. The
 *              terminal palette went live and every browser that had already
 *              visited kept rendering the old stylesheet -- silently, with no
 *              way for a visitor to know or fix it. Staleness is now bounded to
 *              a single page view.
 *
 * Bump CACHE when the precache list changes. Everything else self-heals,
 * because documents are always tried over the network first.
 */
const CACHE = 'dpd-v3';

// The smallest set that makes the game usable with no network at all.
const SHELL = [
  '/',
  '/rules/',
  '/rules/odds/',
  '/narrators/screen/',
  '/downloads/',
  '/assets/stylesheets/extra.v3.css',
  '/assets/stylesheets/fonts.css',
  '/assets/js/dice.js',
  '/assets/img/solid-tetrahedron.svg',
  '/assets/img/solid-hexahedron.svg',
  '/assets/img/solid-octahedron.svg',
  '/assets/img/solid-dodecahedron.svg',
  '/assets/img/solid-icosahedron.svg'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE)
      // addAll is all-or-nothing: one 404 and the whole worker fails to
      // install. Add them individually so a renamed page degrades to "that
      // one page is not available offline" instead of "offline is broken".
      .then((cache) => Promise.all(
        SHELL.map((url) => cache.add(url).catch(() => null))
      ))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(
        keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const request = event.request;
  if (request.method !== 'GET') return;

  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;

  // Skip anything with a query string.
  if (url.search) return;

  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .then((response) => {
          // Only cache a good response. Caching a 404 or a 503 here would
          // overwrite the working offline copy with an error page -- and the
          // fallback below is exactly what someone on dead convention wifi
          // depends on.
          if (response && response.ok) {
            const copy = response.clone();
            caches.open(CACHE).then((cache) => cache.put(request, copy));
          }
          return response;
        })
        .catch(() => caches.match(request).then((hit) => hit || caches.match('/')))
    );
    return;
  }

  // Stale-while-revalidate: answer from cache if we have it, and refresh in
  // the background either way.
  event.respondWith(
    caches.match(request).then((hit) => {
      const network = fetch(request).then((response) => {
        // Opaque and error responses are not worth keeping.
        if (response && response.status === 200 && response.type === 'basic') {
          const copy = response.clone();
          caches.open(CACHE).then((cache) => cache.put(request, copy));
        }
        return response;
      }).catch(() => hit);
      // Keep the worker alive long enough for the background refresh to land,
      // otherwise it can be killed before the cache is updated and the asset
      // stays stale for another visit.
      if (hit) event.waitUntil(network.catch(() => {}));
      return hit || network;
    })
  );
});
