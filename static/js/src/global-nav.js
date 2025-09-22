import { createNav } from '@canonical/global-nav';

createNav({
  maxWidth: '80rem',
  breakpoint: 1150,
  isSliding: true,
});

function handleGlobalNavItems() {
  const globalNavMobile = document.querySelector('#all-canonical-mobile');
  const globalNav = document.querySelector('#all-canonical');
  const navigationItemsContainer = document.querySelector(
    '.js-navigation-items'
  );

  if (globalNav && globalNavMobile && navigationItemsContainer) {
    navigationItemsContainer.appendChild(globalNav);
    navigationItemsContainer.appendChild(globalNavMobile);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  handleGlobalNavItems();
});
