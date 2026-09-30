document.querySelectorAll('[data-year]').forEach((node) => {
  node.textContent = new Date().getFullYear();
});

const heroArt = document.querySelector('.hero-art');
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');

if (heroArt && finePointer.matches && !reducedMotion.matches) {
  heroArt.addEventListener('pointermove', (event) => {
    const bounds = heroArt.getBoundingClientRect();
    const x = ((event.clientX - bounds.left) / bounds.width - 0.5) * 10;
    const y = ((event.clientY - bounds.top) / bounds.height - 0.5) * 8;
    heroArt.style.setProperty('--parallax-x', `${x.toFixed(2)}px`);
    heroArt.style.setProperty('--parallax-y', `${y.toFixed(2)}px`);
  });

  heroArt.addEventListener('pointerleave', () => {
    heroArt.style.setProperty('--parallax-x', '0px');
    heroArt.style.setProperty('--parallax-y', '0px');
  });
}

const scrollQr = document.querySelector('.scroll-qr');
const scrollQrClose = scrollQr?.querySelector('.scroll-qr-close');
const siteHeader = document.querySelector('.site-header');
let scrollQrClosed = false;

if (scrollQr) {
  const updateScrollQr = () => {
    const headerStillVisible = siteHeader && siteHeader.getBoundingClientRect().bottom > 0;
    if (scrollQrClosed) return;
    scrollQr.classList.toggle('is-visible', !headerStillVisible);
    scrollQr.setAttribute('aria-hidden', headerStillVisible ? 'true' : 'false');
  };

  window.addEventListener('scroll', updateScrollQr, { passive: true });
  scrollQrClose?.addEventListener('click', () => {
    scrollQrClosed = true;
    scrollQr.classList.remove('is-visible');
    scrollQr.setAttribute('aria-hidden', 'true');
  });
}
