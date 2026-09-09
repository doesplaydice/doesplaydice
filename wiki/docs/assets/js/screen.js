/* The quick roller on the Narrator's screen.
 *
 * Deliberately not the teaching roller from the rules page. That one exists to
 * explain a comparison; this one exists to answer "what did I roll" in the
 * middle of a sentence, at a noisy table, without looking away for long. One
 * tap, one big number, no configuration to get wrong.
 */
(function () {
  var DICE = [4, 6, 8, 12, 20];

  function roll(sides) {
    // Same rejection sampling as the rules-page roller: no die size divides
    // 2^32 evenly, so plain modulo would quietly favour the low faces.
    var limit = Math.floor(4294967296 / sides) * sides;
    var buf = new Uint32Array(1);
    if (window.crypto && window.crypto.getRandomValues) {
      do { window.crypto.getRandomValues(buf); } while (buf[0] >= limit);
      return (buf[0] % sides) + 1;
    }
    return Math.floor(Math.random() * sides) + 1;
  }

  function build(root) {
    var picks = root.querySelector('.dpd-quickroll-picks');
    var num = root.querySelector('.dpd-quickroll-num');
    var label = root.querySelector('.dpd-quickroll-die');

    DICE.forEach(function (sides) {
      var button = document.createElement('button');
      button.type = 'button';
      button.className = 'dpd-quickroll-btn';
      button.textContent = 'd' + sides;
      button.setAttribute('aria-label', 'Roll a d' + sides);
      button.addEventListener('click', function () {
        var value = roll(sides);
        num.textContent = value;
        label.textContent = 'd' + sides;
        // The result box is role="status" aria-live="polite", so changing its
        // text is what announces the roll. Setting an aria-label here as well
        // would compete with that and get read instead of the number.
        root.classList.remove('is-hit');
        void root.offsetWidth;
        root.classList.add('is-hit');
      });
      picks.appendChild(button);
    });
    root.classList.add('is-ready');
  }

  function init() {
    document.querySelectorAll('[data-quickroll]').forEach(function (root) {
      if (!root.classList.contains('is-ready')) build(root);
    });
  }

  if (window.document$ && typeof window.document$.subscribe === 'function') {
    window.document$.subscribe(init);
  } else if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
