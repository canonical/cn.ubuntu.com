const menuButton = document.querySelector('.js-menu-button');
const secondaryNavigation = document.querySelector(
  '.p-navigation--reduced + .p-navigation'
);
const secondaryNavToggle = document.querySelector(
  '.js-secondary-menu-toggle-button'
);

const overlay = document.querySelector('.dropdown-window-overlay');
const dropdownWindow = document.querySelector('.dropdown-window');
const dropdownWindowOverlay = document.querySelector(
  '.dropdown-window-overlay'
);
const navigation = document.querySelector(
  '.p-navigation, .p-navigation--reduced, .p-navigation--sliding'
);
const globalNavToggle = document.querySelector('.global-nav__dropdown-toggle');
const globalNavBtn = globalNavToggle.querySelector('button');

// Helper functions
const isDesktop = window.matchMedia('(min-width: 1150px)').matches;

const closeAllDropdowns = () => {
  if (navigation && 'classList' in navigation) {
    // Add fade and slide animation classes to hide overlay and dropdown window
    overlay.classList.add('fade-animation');
    dropdownWindow.classList.add('slide-animation');

    // Set all "dropdown toggle" buttons to inactive state by removing "is-active" from classlist
    const dropdownToggles = document.querySelectorAll(
      '.p-navigation__item--dropdown-toggle'
    );
    for (const toggle of dropdownToggles) {
      toggle.classList.remove('is-active');
    }

    // Hide all dropdown contents
    const dropdownContents = dropdownWindow.children;
    for (const content of dropdownContents) {
      content.classList.add('u-hide');
    }
    if (secondaryNavigation) {
      secondaryNavigation.classList.remove('has-menu-open');
    }
    menuButton.innerHTML = 'Menu';

    // Handle navigation state on mobile
    if (!isDesktop) {
      const navigationEl = document.querySelector('.js-navigation-items');
      navigationEl.classList.toggle('is-active', false);
    }
  }
};

const closeGlobalNav = () => {
  if (globalNavBtn) {
    globalNavBtn.click();
  }
};

const toggleDropdown = (toggleEl, shouldOpen) => {
  // Handle navigation and dropdown window states
  navigation.classList.toggle('has-menu-open', isDesktop ? false : true);

  toggleEl.classList.remove('is-selected');
  toggleEl.classList.toggle('is-active', shouldOpen);

  const dropdownContentID = toggleEl.id + '-content';
  const mobileContentID = isDesktop
    ? dropdownContentID
    : dropdownContentID + '-mobile';

  const dropdownContents = document.querySelectorAll(
    `#${isDesktop ? dropdownContentID : mobileContentID}`
  );

  // On mobile, add "is-active" to navigation items container when it should toggle open
  if (!isDesktop) {
    const navigationEl = document.querySelector('.js-navigation-items');
    if (shouldOpen) {
      navigationEl.classList.add('is-active');
    } else {
      navigationEl.classList.remove('is-active');
    }
  } else {
    // Add slide and fade animations on desktop
    dropdownWindow.classList.toggle('slide-animation', !shouldOpen);
    dropdownWindowOverlay.classList.toggle('fade-animation', !shouldOpen);
  }

  dropdownContents.forEach(content => {
    content.classList.toggle('u-hide', !shouldOpen);
    if (shouldOpen) {
      content.removeAttribute('aria-hidden');
    } else {
      content.setAttribute('aria-hidden', !shouldOpen);
    }

    // Handle nested "p-navigation__dropdown" inside the mobile dropdown content
    const innerDropdown = content.querySelector('.p-navigation__dropdown');
    if (innerDropdown) {
      if (shouldOpen) {
        innerDropdown.removeAttribute('aria-hidden');
      } else {
        innerDropdown.setAttribute('aria-hidden', 'true');
      }
    }
  });
};

const initNavigationSliding = () => {
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
    if (backButton) {
      setActiveDropdown(backButton, false);
    }
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

// Setup dropdown toggle functionality
document.addEventListener('DOMContentLoaded', function () {
  // Close all dropdowns if global nav is triggered
  globalNavBtn.addEventListener('click', function () {
    closeAllDropdowns();
  });

  const dropdownToggles = document.querySelectorAll('[data-dropdown-url]');
  dropdownToggles.forEach(el => {
    const anchor = el.querySelector('a');

    if (anchor) {
      anchor.addEventListener('click', function (e) {
        e.preventDefault();

        const isOpen = el.classList.contains('is-active') ? true : false;
        if (isOpen) {
          toggleDropdown(el, false);
        } else {
          closeGlobalNav();
          closeAllDropdowns();
          toggleDropdown(el, true);
        }
      });
    }
  });
});
