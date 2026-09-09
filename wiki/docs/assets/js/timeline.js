/* The "you are here" strip on the plan pages.
 *
 * The plan's own stated risk is losing another fortnight to silence, so the
 * page should say how many days are left every time it is opened -- computed
 * in the browser rather than written into the markdown, because a hand-written
 * countdown is wrong the day after it is written.
 *
 * Markup contract:
 *   <div class="dpd-timeline" data-con="2026-10-16"> ... </div>
 * with an <li data-date="YYYY-MM-DD"> per step. Steps are marked is-past,
 * is-now or is-future; the first step not yet passed becomes is-now.
 */
(function () {
  function midnight(d) {
    return new Date(d.getFullYear(), d.getMonth(), d.getDate());
  }

  // "2026-10-16" parsed as local, not UTC. new Date("2026-10-16") is UTC
  // midnight, which lands on the 15th for anyone west of Greenwich -- and
  // this project is being built in Vermont and Australia.
  function localDate(iso) {
    var p = iso.split('-');
    return new Date(+p[0], +p[1] - 1, +p[2]);
  }

  function render(root) {
    var today = midnight(new Date());
    var con = localDate(root.dataset.con);
    var days = Math.round((con - today) / 86400000);

    var num = root.querySelector('.dpd-tl-num');
    var label = root.querySelector('.dpd-tl-label');
    if (num) {
      if (days > 0) {
        num.textContent = days;
        label.textContent = days === 1 ? 'day to Carnage Con' : 'days to Carnage Con';
      } else if (days === 0) {
        num.textContent = 'Today';
        num.classList.add('is-word');
        label.textContent = 'Carnage Con';
      } else {
        num.textContent = 'Done';
        num.classList.add('is-word');
        label.textContent = 'Carnage Con has been and gone';
      }
    }

    var marked = false;
    var steps = root.querySelectorAll('.dpd-tl-steps li');
    Array.prototype.forEach.call(steps, function (li) {
      if (!li.dataset.date) return;
      var when = localDate(li.dataset.date);
      if (when < today) {
        li.classList.add('is-past');
      } else if (!marked) {
        li.classList.add('is-now');
        marked = true;
      } else {
        li.classList.add('is-future');
      }
    });
    root.classList.add('is-ready');
  }

  function init() {
    Array.prototype.forEach.call(
      document.querySelectorAll('.dpd-timeline'), render
    );
  }

  // navigation.instant swaps the body without a page load, so re-run on each
  // navigation as well as on first paint.
  if (window.document$ && typeof window.document$.subscribe === 'function') {
    window.document$.subscribe(init);
  } else if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
