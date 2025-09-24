const initNavigationSliding = () => {
  const navigation = document.querySelector(
    '.p-navigation, .p-navigation--reduced'
  );
  const secondaryNavigation = document.querySelector(
    '.p-navigation--reduced + .p-navigation'
  );
  const menuButton = document.querySelector('.js-menu-button');

  const closeAllDropdowns = () => {
    navigation.classList.remove('has-menu-open');
    if (secondaryNavigation) {
      secondaryNavigation.classList.remove('has-menu-open');
    }
    menuButton.innerHTML = 'Menu';
  };

  const secondaryNavToggle = document.querySelector(
    '.js-secondary-menu-toggle-button'
  );
  if (secondaryNavToggle) {
    secondaryNavToggle.addEventListener('click', event => {
      event.preventDefault();
      if (secondaryNavigation.classList.contains('has-menu-open')) {
        closeAllDropdowns();
      } else {
        secondaryNavigation.classList.add('has-menu-open');
      }
    });
  }

  const setActiveDropdown = (dropdownToggleButton, isActive = true) => {
    // set active state of the dropdown toggle (to slide the panel into view)
    const dropdownToggleEl = dropdownToggleButton.closest(
      '.js-navigation-dropdown-toggle'
    );
    dropdownToggleEl.classList.toggle('is-active', isActive);

    // set active state of the parent dropdown panel (to fade it out of view)
    const parentLevelDropdown = dropdownToggleEl.closest(
      '.js-navigation-sliding-panel'
    );
    parentLevelDropdown.classList.toggle('is-active', isActive);
  };

  // when clicking outside navigation, close all dropdowns
  document.addEventListener('click', function (event) {
    const target = event.target;
    if (target.closest) {
      if (
        !target.closest(
          '.p-navigation, .p-navigation--sliding, .p-navigation--reduced'
        )
      ) {
        closeAllDropdowns();
      }
    }
  });

  const setListFocusable = list => {
    // turn on focusability for all direct children in the target dropdown
    if (list) {
      for (const item of list.children) {
        item.children[0].setAttribute('tabindex', '0');
      }
    }
  };

  const setFocusable = target => {
    // if target dropdown is not a list, find the list in it
    const isList = target.classList.contains('js-dropdown-nav-list');
    if (!isList) {
      // find all lists in the target dropdown and make them focusable
      target
        .querySelectorAll('.js-dropdown-nav-list')
        .forEach(function (element) {
          setListFocusable(element);
        });
    } else {
      setListFocusable(target);
    }
  };

  const goBackOneLevel = (e, backButton) => {
    e.preventDefault();
    const target = backButton.closest('.p-navigation__dropdown');
    target.setAttribute('aria-hidden', 'true');
    setActiveDropdown(backButton, false);
    setFocusable(target.parentNode.parentNode);
  };

  document.querySelectorAll('.js-back-button').forEach(function (backButton) {
    backButton.addEventListener('click', function (e) {
      goBackOneLevel(e, backButton);
    });
  });

  // throttle util (for window resize event)
  var throttle = function (fn, delay) {
    var timer = null;
    return function () {
      var context = this,
        args = arguments;
      clearTimeout(timer);
      timer = setTimeout(function () {
        fn.apply(context, args);
      }, delay);
    };
  };

  // hide side navigation drawer when screen is resized horizontally
  let previousWidth = window.innerWidth;
  window.addEventListener(
    'resize',
    throttle(function () {
      const currentWidth = window.innerWidth;
      if (currentWidth !== previousWidth) {
        closeAllDropdowns();
        previousWidth = currentWidth;
      }
    }, 10)
  );
};

initNavigationSliding();
