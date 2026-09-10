/* Turn a filled-in Character Vitae into a PDF, in the browser.
 *
 * There is no server here and there never will be, so the PDF has to be built
 * on the reader's own machine. That rules out sending the answers anywhere to
 * be rendered, which is the whole point: what you type about your character is
 * nobody's business but yours.
 *
 * It also rules out a PDF library. Every one of them is hundreds of kilobytes
 * fetched from a CDN, and this site makes zero third-party requests and works
 * with the network switched off. So this writes the PDF itself. That sounds
 * worse than it is -- a PDF is a text format with a byte-offset table at the
 * end, and the fourteen standard fonts are built into every reader, so nothing
 * has to be embedded. What follows is about a hundred lines of writer and a
 * hundred lines of layout.
 *
 * Exposes window.dpdSheetPDF(model, filename). sheet.js owns the model.
 */
(function () {
  'use strict';

  /* ======================================================================
     Part one: the smallest PDF writer that can set type
     ====================================================================== */

  /* Helvetica advance widths, 1/1000 em, for the printable ASCII range.
     Straight from the Adobe metrics. Only needed so lines can be wrapped at
     the right place -- the reader does the actual spacing. */
  var W = ('278 278 355 556 556 889 667 191 333 333 389 584 278 333 278 278 ' +
           '556 556 556 556 556 556 556 556 556 556 278 278 584 584 584 556 ' +
           '1015 667 667 722 722 667 611 778 722 278 500 667 556 833 722 778 ' +
           '667 778 722 667 611 722 667 944 667 667 611 278 278 278 469 556 ' +
           '333 556 556 500 556 556 278 556 556 222 222 500 222 833 556 556 ' +
           '556 556 333 500 278 556 500 722 500 500 500 334 260 334 584'
          ).split(' ').map(Number);

  /* Anything outside ASCII gets folded into WinAnsi, which is what the standard
     fonts speak. Latin-1 passes straight through; the typographic quotes and
     dashes people actually paste in have their own slots down in the 0x80s. */
  var WINANSI = {
    0x2018: 0x91, 0x2019: 0x92, 0x201A: 0x82, 0x201C: 0x93, 0x201D: 0x94,
    0x201E: 0x84, 0x2013: 0x96, 0x2014: 0x97, 0x2026: 0x85, 0x2022: 0x95,
    0x2020: 0x86, 0x2021: 0x87, 0x2030: 0x89, 0x20AC: 0x80, 0x2122: 0x99,
    0x02C6: 0x88, 0x02DC: 0x98, 0x2039: 0x8B, 0x203A: 0x9B
  };

  function encode(str) {
    var out = '';
    for (var i = 0; i < str.length; i++) {
      var c = str.charCodeAt(i);
      if (c === 9) { out += ' '; continue; }
      if (c >= 32 && c <= 255) { out += String.fromCharCode(c); continue; }
      out += String.fromCharCode(WINANSI[c] || 63); /* '?' for the rest */
    }
    return out;
  }

  function charWidth(code) {
    if (code >= 32 && code <= 126) return W[code - 32];
    return 556; /* accented letters cluster here; close enough to wrap by */
  }

  function measure(str, size, tracking) {
    var total = 0;
    for (var i = 0; i < str.length; i++) total += charWidth(str.charCodeAt(i));
    return total * size / 1000 + (tracking || 0) * str.length;
  }

  /* Greedy wrap. Words longer than the column are broken rather than allowed to
     run off the page -- someone will paste a URL in the notes eventually. */
  function wrap(str, size, maxWidth) {
    var words = String(str).split(/\s+/).filter(Boolean);
    var lines = [], line = '';
    while (words.length) {
      var word = words.shift();
      var candidate = line ? line + ' ' + word : word;
      if (measure(candidate, size) <= maxWidth) { line = candidate; continue; }
      if (line) { lines.push(line); line = ''; words.unshift(word); continue; }
      var cut = word.length;
      while (cut > 1 && measure(word.slice(0, cut), size) > maxWidth) cut--;
      lines.push(word.slice(0, cut));
      words.unshift(word.slice(cut));
    }
    if (line) lines.push(line);
    return lines.length ? lines : [''];
  }

  function escape(str) { return str.replace(/[\\()]/g, '\\$&'); }

  function Doc() { this.pages = []; this.page = null; }

  Doc.prototype.addPage = function () { this.page = []; this.pages.push(this.page); };

  Doc.prototype.text = function (x, y, size, font, str, tracking, gray) {
    this.page.push(
      (gray === undefined ? 0 : gray).toFixed(3) + ' g BT /' + font + ' ' +
      size + ' Tf ' + (tracking || 0) + ' Tc ' + x.toFixed(2) + ' ' +
      y.toFixed(2) + ' Td (' + escape(encode(String(str))) + ') Tj ET'
    );
  };

  Doc.prototype.rule = function (x1, y, x2, weight, gray) {
    this.page.push(
      gray.toFixed(3) + ' G ' + weight + ' w ' + x1.toFixed(2) + ' ' +
      y.toFixed(2) + ' m ' + x2.toFixed(2) + ' ' + y.toFixed(2) + ' l S'
    );
  };

  /* Assemble the file. Objects are written in order, their byte offsets
     recorded as we go, and the cross-reference table written from those. Get an
     offset wrong by one byte and no reader will open it, so the offsets are
     taken from the string itself rather than counted by hand. */
  Doc.prototype.toBlob = function () {
    var n = this.pages.length;
    var offsets = [];
    var out = '%PDF-1.4\n%\xE2\xE3\xCF\xD3\n';
    var objects = [];

    var kids = [];
    for (var i = 0; i < n; i++) kids.push((3 + i * 2) + ' 0 R');

    objects.push('<< /Type /Catalog /Pages 2 0 R >>');
    objects.push('<< /Type /Pages /Kids [' + kids.join(' ') + '] /Count ' + n + ' >>');

    var fontBase = 3 + n * 2;
    for (i = 0; i < n; i++) {
      objects.push(
        '<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] ' +
        '/Resources << /Font << /F1 ' + fontBase + ' 0 R /F2 ' + (fontBase + 1) + ' 0 R >> >> ' +
        '/Contents ' + (4 + i * 2) + ' 0 R >>'
      );
      var stream = this.pages[i].join('\n');
      objects.push('<< /Length ' + stream.length + ' >>\nstream\n' + stream + '\nendstream');
    }
    objects.push('<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>');
    objects.push('<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>');

    for (i = 0; i < objects.length; i++) {
      offsets.push(out.length);
      out += (i + 1) + ' 0 obj\n' + objects[i] + '\nendobj\n';
    }

    var startxref = out.length;
    out += 'xref\n0 ' + (objects.length + 1) + '\n0000000000 65535 f \n';
    for (i = 0; i < offsets.length; i++) {
      out += ('0000000000' + offsets[i]).slice(-10) + ' 00000 n \n';
    }
    out += 'trailer\n<< /Size ' + (objects.length + 1) + ' /Root 1 0 R >>\n' +
           'startxref\n' + startxref + '\n%%EOF\n';

    var bytes = new Uint8Array(out.length);
    for (i = 0; i < out.length; i++) bytes[i] = out.charCodeAt(i) & 0xFF;
    return new Blob([bytes], { type: 'application/pdf' });
  };

  /* ======================================================================
     Part two: laying the Vitae out on Letter paper
     ====================================================================== */

  var PAGE_H = 792, LEFT = 56, RIGHT = 556, COL = RIGHT - LEFT;
  var TOP = 730, BOTTOM = 62;
  var LABEL = 7.5, VALUE = 10.5, ROW = 27;
  var INK = 0, MUTED = 0.42, LINE = 0.74;

  function layout(model) {
    var doc = new Doc();
    var y = 0;

    function newPage(withHeader) {
      doc.addPage();
      y = TOP;
      if (withHeader) {
        doc.text(LEFT, y, 8, 'F2', 'DOES PLAY DICE', 1.7, MUTED);
        y -= 26;
        doc.text(LEFT, y, 21, 'F2', 'Character Vitae', 0, INK);
        y -= 12;
        doc.rule(LEFT, y, RIGHT, 1, 0.55);
        y -= 30;
      }
    }

    function room(needed) { if (y - needed < BOTTOM) newPage(false); }

    function label(text) {
      room(ROW + 14);
      doc.text(LEFT, y, LABEL, 'F2', text.toUpperCase(), 1.1, MUTED);
      y -= 15;
    }

    /* A ruled line with the answer sitting on it, the way it looks on screen. */
    function ruledLines(lines, minimum) {
      var count = Math.max(lines.length, minimum || 1);
      for (var i = 0; i < count; i++) {
        /* Spare rules are an invitation to keep writing, not content. Never
           start a second page just to carry them over. */
        if (!lines[i] && y - ROW < BOTTOM) break;
        room(ROW);
        if (lines[i]) doc.text(LEFT + 2, y, VALUE, 'F1', lines[i], 0, INK);
        doc.rule(LEFT, y - 5, RIGHT, 0.6, LINE);
        y -= ROW;
      }
      y -= 6;
    }

    newPage(true);

    model.groups.forEach(function (group) {
      if (group.kind === 'skills') {
        room(ROW * 5);
        y -= 4;
        doc.text(LEFT, y, LABEL, 'F2', 'SKILLS', 1.1, MUTED);
        y -= 8;
        doc.rule(LEFT, y, RIGHT, 0.6, LINE);
        y -= 20;
        group.rows.forEach(function (row) {
          room(ROW);
          doc.text(LEFT + 2, y, VALUE, 'F2', row.skill, 0, INK);
          doc.text(LEFT + 92, y, VALUE - 1, 'F1', row.covers, 0, 0.34);
          var die = row.die || '—';
          doc.text(RIGHT - 2 - measure(die, VALUE), y, VALUE, 'F2', die, 0, INK);
          doc.rule(LEFT, y - 7, RIGHT, 0.5, 0.86);
          y -= 24;
        });
        y -= 10;
        return;
      }

      /* Each ruled line on screen is its own answer, so it stays its own line
         here. A single long answer still wraps, and gains rules as it needs
         them; an empty one keeps its rule, because a sheet with room left on it
         is the point. */
      label(group.label);
      var lines = [];
      group.values.forEach(function (value) {
        if (value) { lines = lines.concat(wrap(value, VALUE, COL - 6)); }
        else { lines.push(''); }
      });
      ruledLines(lines, group.values.length);
    });

    /* Say where it came from, since this page will outlive the browser tab. */
    doc.text(LEFT, BOTTOM - 18, 7.5, 'F1',
      'doesplaydice.com  ·  filled in on ' + model.date +
      '  ·  Does Play Dice is free under CC BY 4.0', 0.6, 0.55);

    return doc;
  }

  window.dpdSheetPDF = function (model, filename) {
    var blob = layout(model).toBlob();
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
  };
})();
