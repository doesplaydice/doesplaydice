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
      /* Material wraps every table in a scrolling div AT RUNTIME, so the child
         here is that wrapper and not the table -- which is why looking only for
         a TABLE child silently dropped the three Skill dice from the PDF. Check
         the built HTML all you like; this only shows up in a live page. */
      var table = node.tagName === 'TABLE'
        ? node
        : (node.querySelector && node.querySelector('table'));
      if (table) {
        var rows = [];
        [].forEach.call(table.querySelectorAll('tbody tr'), function (tr) {
          var cells = tr.children;
          if (cells.length < 3) return;
          var chooser = cells[2].querySelector('select');
          rows.push({
            skill: textOf(cells[0]),
            covers: textOf(cells[1]),
            /* textContent of a cell holding a <select> is every option at once,
               which is not what anybody picked. */
            die: chooser ? chooser.value : textOf(cells[2])
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

  /* There are five dice and there will only ever be five: the game is built on
     the five Platonic solids, and a sixth would not be a house rule, it would be
     a different cosmology. So the die cell is a chooser rather than somewhere to
     type -- you cannot put "BS" in it, and on a phone you get the native picker
     instead of a keyboard. */
  var DICE = ['d4', 'd6', 'd8', 'd12', 'd20'];

  function makeDieChooser(cell, label) {
    var select = document.createElement('select');
    select.className = 'dpd-die-select';
    select.setAttribute('aria-label', label ? label + ' die' : 'Die');
    [''].concat(DICE).forEach(function (d) {
      var option = document.createElement('option');
      option.value = d;
      option.textContent = d || 'd\u2014';   /* the empty state still reads as a die */
      select.appendChild(option);
    });
    select.value = '';
    /* An unchosen die is a prompt, not an answer, and should look like the
       ruled lines do before anyone writes on them. */
    select.sync = function () {
      select.classList.toggle('is-empty', !select.value);
    };
    select.addEventListener('change', select.sync);
    select.sync();
    cell.textContent = '';
    cell.appendChild(select);
    return select;
  }

  function build(sheet) {
    /* Ruled lines, then the die cell at the end of each Skills row. The order
       here is what the saved values are keyed on -- leave it alone. Each entry
       knows how to read and write itself, because the dice are a <select> and
       everything else is contenteditable. */
    var cells = [].slice.call(sheet.querySelectorAll('.dpd-field')).map(function (el) {
      return { el: el, text: true };
    });
    sheet.querySelectorAll('table tr').forEach(function (row) {
      var last = row.lastElementChild;
      if (!last || last.tagName !== 'TD') return;
      var name = row.firstElementChild ? row.firstElementChild.textContent.trim() : '';
      cells.push({ el: last, text: false, label: name });
    });

    var data = load();
    var pending = null;

    function queueSave() {
      clearTimeout(pending);
      pending = setTimeout(function () {
        var out = {};
        cells.forEach(function (c, j) {
          var v = c.get();
          if (v) out['f' + j] = v;
        });
        save(out);
      }, 400);
    }

    cells.forEach(function (cell, i) {
      var el = cell.el;
      if (cell.text) {
        el.setAttribute('contenteditable', 'plaintext-only');
        el.setAttribute('role', 'textbox');
        el.setAttribute('spellcheck', 'false');
        el.classList.add('is-fillable');
        cell.get = function () { return el.textContent.trim(); };
        cell.set = function (v) { el.textContent = v; };
        el.addEventListener('input', queueSave);
      } else {
        var select = makeDieChooser(el, cell.label);
        el.classList.add('is-die');
        cell.get = function () { return select.value; };
        /* Anything that is not one of the five is simply not restored, which is
           how the free-text answers people typed before now fall away. */
        cell.set = function (v) {
          select.value = DICE.indexOf(v) === -1 ? '' : v;
          select.sync();
        };
        select.addEventListener('change', queueSave);
      }
      if (typeof data['f' + i] === 'string') cell.set(data['f' + i]);
    });

    /* Chrome's print preview opens and then closes again on a page that is in
       the middle of being edited. Nothing needs to be editable while it is
       being printed, so hand the page over as ordinary text and take it back
       afterwards. This also drops the focus ring out of the printed sheet. */
    window.addEventListener('beforeprint', function () {
      if (document.activeElement && document.activeElement.blur) {
        document.activeElement.blur();
      }
      cells.forEach(function (c) {
        if (c.text) c.el.removeAttribute('contenteditable');
      });
    });
    window.addEventListener('afterprint', function () {
      cells.forEach(function (c) {
        if (c.text) c.el.setAttribute('contenteditable', 'plaintext-only');
      });
    });

    // Somewhere to say what this does, and a way out of it.
    var bar = document.createElement('p');
    bar.className = 'dpd-sheet-note';
    bar.innerHTML =
      'Type straight into the sheet &mdash; it saves in this browser only, and is ' +
      'never sent anywhere. When you are done, download it as a PDF, or ' +
      '<a href="../../downloads/does-play-dice-character-sheet.pdf">take the blank one</a> ' +
      'to fill in with a pencil.' +
      '<span class="dpd-sheet-actions">' +
      '<button type="button" class="dpd-sheet-get">Download PDF</button>' +
      '<button type="button" class="dpd-sheet-clear">Clear the sheet</button>' +
      '</span>';
    sheet.parentNode.insertBefore(bar, sheet);

    bar.querySelector('.dpd-sheet-clear').addEventListener('click', function () {
      cells.forEach(function (c) { c.set(''); });
      save({});
    });

    var get = bar.querySelector('.dpd-sheet-get');
    if (typeof window.dpdSheetPDF !== 'function') {
      get.remove();
      return;
    }
    /* The PDF is the designed sheet fetched and written onto, so this is a
       network round trip the first time. Say so, and say it plainly if it
       fails, rather than leaving a button that looks broken. */
    get.addEventListener('click', function () {
      var groups = describe(sheet);
      var named = groups.filter(function (g) { return !g.kind && g.values.some(Boolean); });
      var name = named.length ? named[0].values.filter(Boolean)[0] : '';
      var label = get.textContent;
      get.disabled = true;
      get.textContent = 'Building\u2026';
      Promise.resolve(window.dpdSheetPDF({ groups: groups },
        'does-play-dice-' + slug(name) + '.pdf'))
        .catch(function (err) {
          var note = bar.querySelector('.dpd-sheet-error');
          if (!note) {
            note = document.createElement('span');
            note.className = 'dpd-sheet-error';
            bar.appendChild(note);
          }
          note.textContent = ' The sheet could not be built \u2014 ' +
            (err && err.message ? err.message : 'something went wrong') +
            '. You can still print this page.';
        })
        .then(function () {
          get.disabled = false;
          get.textContent = label;
        });
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
