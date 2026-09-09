/* Register the service worker.
 *
 * Lives here rather than in the template so it survives the pre-launch
 * teardown: overrides/main.html loses its gate at launch, and offline support
 * should not go with it.
 */
(function () {
  if (!('serviceWorker' in navigator)) return;
  // Secure context only. Over plain http the API exists on localhost but not
  // elsewhere, and registering would throw.
  if (!window.isSecureContext) return;

  window.addEventListener('load', function () {
    navigator.serviceWorker.register('/sw.js').catch(function () {
      // Offline support is a bonus, never a dependency. If it fails the site
      // works exactly as it did before.
    });
  });
})();
