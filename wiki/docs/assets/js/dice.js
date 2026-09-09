/* The try-it dice roller on the rules page.
 *
 * The whole pitch is "fifteen minutes to learn", and the mechanic is a single
 * comparison: your Skill die against the Narrator's difficulty die, highest
 * wins, a tie means both sides get something. Reading that takes a paragraph.
 * Doing it takes one click, so the page lets you do it.
 *
 * The five dice are drawn as the five Platonic solids, which is not decoration:
 * the setting is named for the Plato dialogue that assigns the solids to the
 * elements, so the dice and the cosmology are the same five objects.
 */
(function () {
  // Where the solid drawings live. Derived from this script's own URL rather
  // than written as "../assets/img/", because a relative path resolves against
  // the *page*, not the script -- so it would break on any page at a different
  // depth, and on a fork hosted under a subpath. The browser has already
  // resolved this src absolutely for us.
  var IMG_BASE = (function () {
    var self = document.currentScript;
    if (self && self.src) return self.src.replace(/js\/dice\.js.*$/, 'img/');
    return '../assets/img/';   // last resort, correct for /rules/
  })();

  var DICE = [
    { sides: 4,  solid: 'tetrahedron',  name: 'Tetrahedron' },
    { sides: 6,  solid: 'hexahedron',   name: 'Cube' },
    { sides: 8,  solid: 'octahedron',   name: 'Octahedron' },
    { sides: 12, solid: 'dodecahedron', name: 'Dodecahedron' },
    { sides: 20, solid: 'icosahedron',  name: 'Icosahedron' }
  ];

  // The rules walk through a d6 Skill against a d12 door. Start there, so the
  // widget is already showing the example the reader just read.
  var DEFAULTS = { you: 6, narrator: 12 };

  var OUTCOMES = {
    you: {
      verdict: 'You win.',
      detail: 'You do what you described. The Narrator says how it looks.'
    },
    narrator: {
      verdict: 'The Narrator wins.',
      detail: 'It does not go your way — but the story still moves. Something ' +
              'happens; it just is not what you wanted.'
    },
    tie: {
      verdict: 'A tie. Both sides get something.',
      detail: 'You get through the door, and you hurt your shoulder doing it. ' +
              'This is the rule that makes the game feel generous.'
    }
  };

  function roll(sides) {
    // Modulo on a 32-bit value would bias the low faces; none of 4, 6, 8, 12
    // or 20 divides 2^32 evenly. Reject the ragged tail instead.
    var limit = Math.floor(4294967296 / sides) * sides;
    var buf = new Uint32Array(1);
    if (window.crypto && window.crypto.getRandomValues) {
      do { window.crypto.getRandomValues(buf); } while (buf[0] >= limit);
      return (buf[0] % sides) + 1;
    }
    return Math.floor(Math.random() * sides) + 1;
  }

  var solidCache = {};

  function paintSolids(root) {
    root.querySelectorAll('.dpd-roller-solid[data-solid]').forEach(function (slot) {
      var name = slot.dataset.solid;
      if (!solidCache[name]) {
        solidCache[name] = fetch(IMG_BASE + 'solid-' + name + '.svg')
          .then(function (response) {
            if (!response.ok) throw new Error(response.status);
            return response.text();
          });
      }
      solidCache[name].then(function (markup) {
        slot.innerHTML = markup;
        slot.removeAttribute('data-solid');
      }).catch(function () {
        // The die label alone still says everything the control needs to say.
        slot.remove();
      });
    });
  }

  function build(root) {
    var state = { you: DEFAULTS.you, narrator: DEFAULTS.narrator, rolling: false };
    var sides = {};

    root.querySelectorAll('[data-side]').forEach(function (panel) {
      var who = panel.dataset.side;
      var picks = panel.querySelector('.dpd-roller-picks');
      var buttons = [];

      DICE.forEach(function (die) {
        var button = document.createElement('button');
        button.type = 'button';
        button.className = 'dpd-roller-pick';
        button.dataset.sides = die.sides;
        button.setAttribute('aria-label', die.name + ', d' + die.sides);
        button.innerHTML =
          '<span class="dpd-roller-solid" data-solid="' + die.solid + '"></span>' +
          '<span class="dpd-roller-dname">d' + die.sides + '</span>';
        button.addEventListener('click', function () {
          state[who] = die.sides;
          sync();
        });
        picks.appendChild(button);
        buttons.push(button);
      });

      sides[who] = {
        buttons: buttons,
        number: panel.querySelector('.dpd-roller-num')
      };
    });

    function sync() {
      Object.keys(sides).forEach(function (who) {
        sides[who].buttons.forEach(function (button) {
          var on = +button.dataset.sides === state[who];
          button.classList.toggle('is-on', on);
          button.setAttribute('aria-pressed', on ? 'true' : 'false');
        });
      });
    }

    var outcome = root.querySelector('.dpd-roller-outcome');
    var go = root.querySelector('.dpd-roller-go');

    function settle(you, narrator) {
      sides.you.number.textContent = you;
      sides.narrator.number.textContent = narrator;
      var key = you > narrator ? 'you' : (narrator > you ? 'narrator' : 'tie');
      root.dataset.result = key;
      outcome.innerHTML =
        '<strong>' + OUTCOMES[key].verdict + '</strong> ' + OUTCOMES[key].detail;
      state.rolling = false;
      go.disabled = false;
      go.textContent = 'Roll again';
    }

    go.addEventListener('click', function () {
      if (state.rolling) return;
      state.rolling = true;
      go.disabled = true;
      delete root.dataset.result;
      outcome.textContent = '';

      var you = roll(state.you);
      var narrator = roll(state.narrator);

      var reduced = window.matchMedia &&
        window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      if (reduced) { settle(you, narrator); return; }

      // A short tumble, so the result reads as a roll rather than an update.
      root.classList.add('is-rolling');
      var ticks = 0;
      var timer = setInterval(function () {
        sides.you.number.textContent = roll(state.you);
        sides.narrator.number.textContent = roll(state.narrator);
        if (++ticks >= 8) {
          clearInterval(timer);
          root.classList.remove('is-rolling');
          settle(you, narrator);
        }
      }, 55);
    });

    sync();
    paintSolids(root);
    root.classList.add('is-ready');
  }

  function init() {
    document.querySelectorAll('[data-roller]').forEach(function (root) {
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
