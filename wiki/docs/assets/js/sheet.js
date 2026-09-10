/* Make the character sheet fillable in the browser.
 *
 * The fields are ruled lines -- divs with a bottom border -- because the sheet
 * was designed to be printed and written on. But a ruled line under an
 * uppercase label looks exactly like a web form, so people try to type in it
 * and nothing happens. Rather than explain the difference, let them type.
 *
 * Deliberately small: contenteditable rather than real inputs, so the fields
 * keep looking like ruled paper and print without any browser form chrome. What
 * you type stays in this browser and is never sent anywhere -- there is no
 * account here, and that is the point.
 */
(function () {
  var KEY = 'dpd-sheet-v1';

  function load() {
    try { return JSON.parse(localStorage.getItem(KEY) || '{}'); }
    catch (e) { return {}; }
  }

  function save(data) {
    try { localStorage.setItem(KEY, JSON.stringify(data)); } catch (e) { /* private mode */ }
  }

  function build(sheet) {
    // Ruled lines, plus the die cell at the end of each Skills row.
    var fields = [].slice.call(sheet.querySelectorAll('.dpd-field'));
    sheet.querySelectorAll('table tr').forEach(function (row) {
      var last = row.lastElementChild;
      if (last && last.tagName === 'TD') fields.push(last);
    });

    var data = load();
    var pending = null;

    fields.forEach(function (field, i) {
      var id = 'f' + i;
      field.setAttribute('contenteditable', 'plaintext-only');
      field.setAttribute('role', 'textbox');
      field.setAttribute('spellcheck', 'false');
      field.classList.add('is-fillable');

      // A die cell ships with a placeholder glyph; clear it so it does not have
      // to be deleted before typing.
      if (field.tagName === 'TD' && field.textContent.trim() === '▢') {
        field.textContent = '';
        field.dataset.hint = 'die';
      }
      if (typeof data[id] === 'string') field.textContent = data[id];

      field.addEventListener('input', function () {
        clearTimeout(pending);
        pending = setTimeout(function () {
          var out = {};
          fields.forEach(function (f, j) {
            var v = f.textContent.trim();
            if (v) out['f' + j] = v;
          });
          save(out);
        }, 400);
      });
    });

    // Somewhere to say what this does, and a way out of it.
    var bar = document.createElement('p');
    bar.className = 'dpd-sheet-note';
    bar.innerHTML =
      'Type straight into the sheet &mdash; it saves in this browser only, and is ' +
      'never sent anywhere. Print the page when you are done, or ' +
      '<a href="../../downloads/does-play-dice-character-sheet.pdf">download the blank PDF</a> ' +
      'to fill in with a pencil. <button type="button" class="dpd-sheet-clear">Clear the sheet</button>';
    sheet.parentNode.insertBefore(bar, sheet);

    bar.querySelector('.dpd-sheet-clear').addEventListener('click', function () {
      fields.forEach(function (f) { f.textContent = ''; });
      save({});
    });
  }

  function init() {
    var sheet = document.querySelector('.dpd-sheet');
    if (sheet && !sheet.dataset.fillable) {
      sheet.dataset.fillable = '1';
      build(sheet);
    }
  }

  if (window.document$ && typeof window.document$.subscribe === 'function') {
    window.document$.subscribe(init);
  } else if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
