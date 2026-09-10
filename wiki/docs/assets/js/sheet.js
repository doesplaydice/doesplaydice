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
 * account here, and that is the point. The Download button hands the same
 * promise to a PDF: it is built on this machine, by sheet-pdf.js, and never
 * leaves it.
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

  function textOf(node) { return (node.textContent || '').trim(); }

  /* Walk the sheet in reading order and describe it: label, then the ruled
     lines that belong to it. The PDF is laid out from this rather than from the
     DOM, so the two cannot drift apart when the markdown changes. */
  function describe(sheet) {
    var groups = [];
    var current = null;

    [].forEach.call(sheet.children, function (node) {
      var labelSpan = node.querySelector && node.querySelector('.dpd-field-label');
      if (labelSpan) {
        current = { label: textOf(labelSpan), values: [] };
        groups.push(current);
        return;
      }
      if (node.classList && node.classList.contains('dpd-field')) {
        if (!current) { current = { label: '', values: [] }; groups.push(current); }
        current.values.push(textOf(node));
        return;
      }
      if (node.tagName === 'TABLE') {
        var rows = [];
        [].forEach.call(node.querySelectorAll('tbody tr'), function (tr) {
          var cells = tr.children;
          if (cells.length < 3) return;
          rows.push({
            skill: textOf(cells[0]),
            covers: textOf(cells[1]),
            die: textOf(cells[2])
          });
        });
        if (rows.length) { groups.push({ kind: 'skills', rows: rows }); current = null; }
      }
    });

    return groups;
  }

  function slug(name) {
    var s = name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
    return s || 'character-vitae';
  }

  function build(sheet) {
    /* Ruled lines, plus the die cell at the end of each Skills row. The order
       here is what the saved values are keyed on -- leave it alone. */
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

    /* Chrome's print preview opens and then closes again on a page that is in
       the middle of being edited. Nothing needs to be editable while it is
       being printed, so hand the page over as ordinary text and take it back
       afterwards. This also drops the focus ring out of the printed sheet. */
    window.addEventListener('beforeprint', function () {
      if (document.activeElement && document.activeElement.blur) {
        document.activeElement.blur();
      }
      fields.forEach(function (f) { f.removeAttribute('contenteditable'); });
    });
    window.addEventListener('afterprint', function () {
      fields.forEach(function (f) { f.setAttribute('contenteditable', 'plaintext-only'); });
    });

    // Somewhere to say what this does, and a way out of it.
    var bar = document.createElement('p');
    bar.className = 'dpd-sheet-note';
    bar.innerHTML =
      'Type straight into the sheet &mdash; it saves in this browser only, and is ' +
      'never sent anywhere. When you are done, download it as a PDF, or ' +
      '<a href="../../downloads/does-play-dice-character-sheet.pdf">take the blank one</a> ' +
      'to fill in with a pencil. ' +
      '<button type="button" class="dpd-sheet-get">Download PDF</button>' +
      '<button type="button" class="dpd-sheet-clear">Clear the sheet</button>';
    sheet.parentNode.insertBefore(bar, sheet);

    bar.querySelector('.dpd-sheet-clear').addEventListener('click', function () {
      fields.forEach(function (f) { f.textContent = ''; });
      save({});
    });

    var get = bar.querySelector('.dpd-sheet-get');
    if (typeof window.dpdSheetPDF !== 'function') {
      get.remove();
      return;
    }
    get.addEventListener('click', function () {
      var groups = describe(sheet);
      var named = groups.filter(function (g) { return !g.kind && g.values.some(Boolean); });
      var name = named.length ? named[0].values.filter(Boolean)[0] : '';
      window.dpdSheetPDF({
        groups: groups,
        date: new Date().toLocaleDateString(undefined,
          { year: 'numeric', month: 'long', day: 'numeric' })
      }, 'does-play-dice-' + slug(name) + '.pdf');
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
