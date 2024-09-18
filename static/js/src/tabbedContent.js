(() => {
  (function () {
    let d = {
        left: 'ArrowLeft',
        right: 'ArrowRight',
      },
      l = {
        ArrowLeft: -1,
        ArrowRight: 1,
      },
      f = {
        left: 37,
        right: 39,
      },
      a = {
        37: l.ArrowLeft,
        39: l.ArrowRight,
      },
      h = (r, o) => {
        let e = f,
          c = a,
          t = r.keyCode;
        if ((r.code && ((e = d), (c = l), (t = r.code)), c[t])) {
          let i = r.target;
          i.index !== void 0 &&
            (o[i.index + c[t]]
              ? o[i.index + c[t]].focus()
              : t === e.left
              ? o[o.length - 1].focus()
              : t === e.right && o[0].focus());
        }
      },
      u = (r, o) => {
        r.forEach(function (e, c) {
          e.addEventListener('keyup', function (t) {
            let i = f,
              s = t.keyCode;
            t.code && ((i = d), (s = t.code)),
              (s === i.left || s === i.right) && h(t, r);
          }),
            e.addEventListener('click', t => {
              t.preventDefault(),
                o &&
                  (history.pushState({}, '', e.href),
                  history.pushState({}, '', e.href),
                  history.back()),
                n(e, r);
            }),
            e.addEventListener('focus', () => {
              n(e, r);
            }),
            (e.index = c);
        });
      },
      n = (r, o) => {
        o.forEach(e => {
          var c = document.querySelectorAll(
            '#' + e.getAttribute('aria-controls')
          );
          c.forEach(t => {
            e === r
              ? (e.setAttribute('aria-selected', !0),
                t.removeAttribute('hidden'))
              : (e.setAttribute('aria-selected', !1),
                t.setAttribute('hidden', !0));
          });
        });
      },
      A = r => {
        var o = [].slice.call(document.querySelectorAll(r));
        o.forEach(e => {
          var c = e.getAttribute('data-maintain-hash'),
            t = window.location.hash,
            i = [].slice.call(e.querySelectorAll('[aria-controls]'));
          if ((u(i, c), c && t)) {
            var s = document.querySelector(".p-tabs__link[href='" + t + "']");
            s && n(s, i);
          } else n(i[0], i);
        });
      };
    document.addEventListener('DOMContentLoaded', () => {
      A('.js-tabbed-content');
    });
  })();
})();

(function () {
  // Toggles show board based on selection on small screens

  const boards = document.querySelectorAll(`[role=tabpanel]`);
  const dropdownSelect = document.getElementById('boardSelect');

  if (dropdownSelect) {
    dropdownSelect.addEventListener('change', () => {
      selectBoard();
    });
  }
  function selectBoard() {
    boards.forEach(board => {
      if (board.id === dropdownSelect.value) {
        board.removeAttribute('hidden');
        board.focus();
      } else {
        board.setAttribute('hidden', true);
      }
    });
  }
})();
