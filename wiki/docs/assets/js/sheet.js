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
  /* Saved answers are keyed by name: the label a line sits under and which
     line it is ("background-2"), or the Skill a die, floor or stamina track
     belongs to ("die-body"). Version 1 keyed them by position instead, which
     misfiles everything the moment a field is added above another one. */
  var KEY = 'dpd-sheet-v2';
  var OLD_KEY = 'dpd-sheet-v1';

  /* What position f0, f1 ... meant in version 1, which is fixed forever, so
     a sheet saved then still comes back with every answer where it was. */
  var V1_ORDER = [
    'character-name-1', 'played-by-1', 'background-1', 'background-2',
    'school-or-job-1', 'habits-and-quirks-1', 'habits-and-quirks-2',
    'connections-1', 'notes-1', 'notes-2', 'notes-3',
    'die-body', 'die-mind', 'die-soul'
  ];

  function load() {
    try {
      var saved = localStorage.getItem(KEY);
      if (saved) return JSON.parse(saved);
      var old = JSON.parse(localStorage.getItem(OLD_KEY) || '{}');
      var data = {};
      V1_ORDER.forEach(function (name, i) {
        if (typeof old['f' + i] === 'string') data[name] = old['f' + i];
      });
      save(data);
      localStorage.removeItem(OLD_KEY);
      return data;
    } catch (e) { return {}; }
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
    var skills = null;

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
        var col = columnsOf(table);
        var rows = [];
        [].forEach.call(table.querySelectorAll('tbody tr'), function (tr) {
          var cells = tr.children;
          if (cells.length < 3) return;
          var dieCell = cells[col.die] || cells[cells.length - 1];
          var chooser = dieCell.querySelector('select');
          rows.push({
            skill: textOf(cells[0]),
            covers: textOf(cells[1]),
            /* textContent of a cell holding a <select> is every option at once,
               which is not what anybody picked. */
            die: chooser ? chooser.value : textOf(dieCell),
            floor: col.floor >= 0 && cells[col.floor] ? textOf(cells[col.floor]) : '',
            spent: []
          });
        });
        if (rows.length) {
          skills = { kind: 'skills', rows: rows };
          groups.push(skills);
          current = null;
        }
      }
    });

    /* The stamina boxes sit further down the sheet, but they belong to the
       Skills, so the ones ticked off travel with each Skill's row. */
    if (skills) {
      [].forEach.call(sheet.querySelectorAll('.dpd-st-row'), function (track) {
        var row = skills.rows.filter(function (r) {
          return firstWord(r.skill) === firstWord(textOf(track.querySelector('b')));
        })[0];
        if (!row) return;
        [].forEach.call(track.querySelectorAll('.dpd-bx i'), function (box, b) {
          if (box.classList.contains('is-spent')) row.spent.push(b);
        });
      });
    }

    return groups;
  }

  function slug(name) {
    var s = name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
    return s || 'character-vitae';
  }

  function firstWord(text) { return (text || '').trim().split(/\s+/)[0].toLowerCase(); }

  /* Which column holds the die and which the floor, read from the headings so
     that adding a column cannot quietly move an answer into the wrong one. */
  function columnsOf(table) {
    var col = { die: -1, floor: -1 };
    [].forEach.call(table.querySelectorAll('thead th'), function (th, i) {
      var t = textOf(th);
      if (/\bdie\b/i.test(t)) col.die = i;
      if (/floor/i.test(t)) col.floor = i;
    });
    return col;
  }

  /* The stamina boxes past a die's sides are not yours: grey them out, as the
     printed sheet asks you to with a pencil. */
  function sides(die) { return parseInt(String(die || '').replace(/^d/i, ''), 10) || 0; }

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
    /* Every answer on the sheet, each under its own name. Each entry knows how
       to read and write itself, because the dice are a <select>, the floors and
       the ruled lines are contenteditable, and stamina is a row of boxes. */
    var cells = [];
    var label = '', line = 0;
    [].forEach.call(sheet.children, function (node) {
      var span = node.querySelector && node.querySelector('.dpd-field-label');
      if (span) {
        label = slug(textOf(span).split(/\s+\u2014\s+/)[0]);
        line = 0;
        return;
      }
      if (node.classList && node.classList.contains('dpd-field')) {
        line += 1;
        cells.push({ el: node, kind: 'text', key: label + '-' + line });
      }
    });

    var tracks = {};
    sheet.querySelectorAll('.dpd-st-row').forEach(function (track) {
      tracks[firstWord(textOf(track.querySelector('b')))] = track;
    });

    sheet.querySelectorAll('table').forEach(function (table) {
      var col = columnsOf(table);
      if (col.die < 0) return;
      table.querySelectorAll('tbody tr').forEach(function (row) {
        var name = row.firstElementChild ? textOf(row.firstElementChild) : '';
        var skill = firstWord(name);
        var die = { el: row.children[col.die], kind: 'die', key: 'die-' + skill,
                    label: name.split(/\s+/)[0] };
        cells.push(die);
        if (col.floor >= 0 && row.children[col.floor]) {
          cells.push({ el: row.children[col.floor], kind: 'floor', key: 'floor-' + skill,
                       label: name.split(/\s+/)[0] });
        }
        if (tracks[skill]) {
          cells.push({ el: tracks[skill], kind: 'stamina', key: 'stamina-' + skill,
                       label: name.split(/\s+/)[0], die: die });
        }
      });
    });

    var data = load();
    var pending = null;

    function queueSave() {
      clearTimeout(pending);
      pending = setTimeout(function () {
        var out = {};
        cells.forEach(function (c) {
          var v = c.get();
          if (v) out[c.key] = v;
        });
        save(out);
      }, 400);
    }

    cells.forEach(function (cell) {
      var el = cell.el;
      if (cell.kind === 'text') {
        el.setAttribute('contenteditable', 'plaintext-only');
        el.setAttribute('role', 'textbox');
        el.setAttribute('spellcheck', 'false');
        el.classList.add('is-fillable');
        cell.get = function () { return el.textContent.trim(); };
        cell.set = function (v) { el.textContent = v; };
        el.addEventListener('input', queueSave);
      } else if (cell.kind === 'die') {
        var select = makeDieChooser(el, cell.label);
        el.classList.add('is-die');
        cell.get = function () { return select.value; };
        /* Anything that is not one of the five is simply not restored, which is
           how the free-text answers people typed before now fall away. */
        cell.set = function (v) {
          select.value = DICE.indexOf(v) === -1 ? '' : v;
          select.sync();
          select.dispatchEvent(new Event('dpd-die'));
        };
        select.addEventListener('change', function () {
          select.dispatchEvent(new Event('dpd-die'));
          queueSave();
        });
        cell.select = select;
      } else if (cell.kind === 'floor') {
        /* A floor is a small number: the training points in that Skill. */
        var box = document.createElement('span');
        box.className = 'dpd-floor';
        box.setAttribute('contenteditable', 'plaintext-only');
        box.setAttribute('role', 'textbox');
        box.setAttribute('inputmode', 'numeric');
        box.setAttribute('aria-label', cell.label + ' floor');
        el.textContent = '';
        el.appendChild(box);
        el.classList.add('is-floor');
        cell.text = box;
        cell.get = function () { return box.textContent.trim(); };
        cell.set = function (v) { box.textContent = v; };
        box.addEventListener('input', function () {
          var clean = box.textContent.replace(/\D/g, '').slice(0, 2);
          if (clean !== box.textContent) box.textContent = clean;
          queueSave();
        });
      } else {
        /* Stamina: tick a box off for each point lost, untick it as it comes
           back. Boxes past the die are greyed out and cannot be ticked. */
        var boxes = [].slice.call(el.querySelectorAll('.dpd-bx i'));
        var spent = [];
        boxes.forEach(function (b, n) {
          b.setAttribute('role', 'checkbox');
          b.setAttribute('aria-label', cell.label + ' stamina ' + (n + 1));
          function toggle() {
            if (b.classList.contains('is-out')) return;
            b.classList.toggle('is-spent');
            b.setAttribute('aria-checked', b.classList.contains('is-spent'));
            queueSave();
          }
          b.addEventListener('click', toggle);
          b.addEventListener('keydown', function (e) {
            if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); toggle(); }
          });
        });
        function fit() {
          var n = sides(cell.die.select.value);
          boxes.forEach(function (b, j) {
            var out = n > 0 && j >= n;
            b.classList.toggle('is-out', out);
            if (out) b.classList.remove('is-spent');
            b.setAttribute('aria-checked', b.classList.contains('is-spent'));
            b.setAttribute('aria-disabled', out);
            b.tabIndex = out ? -1 : 0;
          });
        }
        cell.die.select.addEventListener('dpd-die', fit);
        cell.get = function () {
          spent = [];
          boxes.forEach(function (b, j) { if (b.classList.contains('is-spent')) spent.push(j + 1); });
          return spent.join(',');
        };
        cell.set = function (v) {
          var marks = String(v || '').split(',').map(Number);
          boxes.forEach(function (b, j) {
            b.classList.toggle('is-spent', marks.indexOf(j + 1) !== -1);
          });
          fit();
        };
        fit();
      }
    });

    /* Dice before stamina, so a track knows its die before it restores. */
    cells.forEach(function (cell) {
      if (cell.kind !== 'stamina' && typeof data[cell.key] === 'string') cell.set(data[cell.key]);
    });
    cells.forEach(function (cell) {
      if (cell.kind === 'stamina' && typeof data[cell.key] === 'string') cell.set(data[cell.key]);
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
        if (c.kind === 'text') c.el.removeAttribute('contenteditable');
        if (c.kind === 'floor') c.text.removeAttribute('contenteditable');
      });
    });
    window.addEventListener('afterprint', function () {
      cells.forEach(function (c) {
        if (c.kind === 'text') c.el.setAttribute('contenteditable', 'plaintext-only');
        if (c.kind === 'floor') c.text.setAttribute('contenteditable', 'plaintext-only');
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
