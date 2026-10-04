/* Leira — web oficial. Sin dependencias. */

/**
 * Enlace de Leira en Google Play. Vacío hasta que la app esté publicada: mientras tanto, los
 * botones de descarga dicen «Próximamente en Google Play» y no llevan a ningún sitio. En cuanto
 * se pegue aquí la URL real (p. ej. https://play.google.com/store/apps/details?id=com.leiraapp.mobile),
 * todos pasan solos a «Descargar en Google Play» y abren la ficha de la tienda.
 */
const GOOGLE_PLAY_URL = '';

const SOON_LABEL = 'Próximamente en Google Play';
const READY_LABEL = 'Descargar en Google Play';

document.documentElement.classList.add('js');

function setupPlayButtons() {
  const ready = GOOGLE_PLAY_URL.trim() !== '';
  document.querySelectorAll('[data-play]').forEach((btn) => {
    const label = btn.querySelector('[data-play-label]');
    if (ready) {
      btn.href = GOOGLE_PLAY_URL;
      btn.target = '_blank';
      btn.rel = 'noopener';
      btn.removeAttribute('aria-disabled');
      if (label) label.textContent = label.dataset.readyLabel || READY_LABEL;
    } else {
      if (label) label.textContent = SOON_LABEL;
      // Sin enlace todavía: el del hero lleva a la sección de descarga; el de esa sección, a nada.
      if (btn.closest('#descargar')) {
        btn.setAttribute('aria-disabled', 'true');
        btn.addEventListener('click', (e) => e.preventDefault());
      }
    }
  });
  document.querySelectorAll('[data-play-text]').forEach((a) => {
    if (ready) {
      a.href = GOOGLE_PLAY_URL;
      a.target = '_blank';
      a.rel = 'noopener';
    }
  });
}

function setupNav() {
  const nav = document.querySelector('[data-nav]');
  const toggle = document.querySelector('[data-nav-toggle]');
  const links = document.getElementById('nav-links');
  if (!nav || !toggle || !links) return;

  const setOpen = (open) => {
    links.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
    toggle.querySelector('.ms').textContent = open ? 'close' : 'menu';
  };
  toggle.addEventListener('click', () => setOpen(!links.classList.contains('open')));
  links.addEventListener('click', (e) => {
    if (e.target.closest('a')) setOpen(false);
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') setOpen(false);
  });

  const onScroll = () => nav.classList.toggle('scrolled', window.scrollY > 8);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
}

/** La ilustración del mapa vive una sola vez en un <template> y se clona en cada mockup. */
function mountMaps() {
  const tpl = document.getElementById('map-art');
  if (!tpl) return;
  document.querySelectorAll('[data-map]').forEach((map) => {
    map.prepend(tpl.content.cloneNode(true));
  });
}

function setupReveal() {
  const items = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window)) {
    items.forEach((el) => el.classList.add('in'));
    return;
  }
  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    },
    { rootMargin: '0px 0px -8% 0px', threshold: 0.12 },
  );
  items.forEach((el) => io.observe(el));
}

/** Selector Satélite | Mapa de la sección del mapa. */
function setupLayerSwitch() {
  const target = document.querySelector('[data-layer-target]');
  const buttons = document.querySelectorAll('[data-layer-btn]');
  if (!target || !buttons.length) return;
  buttons.forEach((btn) => {
    btn.addEventListener('click', () => {
      const layer = btn.dataset.layerBtn;
      target.dataset.layer = layer;
      buttons.forEach((b) => {
        const on = b === btn;
        b.classList.toggle('on', on);
        b.setAttribute('aria-pressed', String(on));
      });
      target.querySelectorAll('[data-pill]').forEach((p) => p.classList.toggle('on', p.dataset.pill === layer));
    });
  });
}

/** Demo de la sección Catastro: recorre los 4 pasos mientras la sección está a la vista. */
function setupCatastroDemo() {
  const map = document.querySelector('[data-demo-step]');
  const steps = document.querySelectorAll('[data-steps] li');
  if (!map || !steps.length) return;

  const show = (n) => {
    map.dataset.demoStep = String(n);
    steps.forEach((li) => li.classList.toggle('active', li.dataset.step === String(n)));
  };
  // Sin animaciones: estado final (parcela seleccionada con su tarjeta) y todos los pasos visibles.
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)) {
    show(4);
    return;
  }

  let step = 1;
  let timer = null;
  const tick = () => {
    show(step);
    step = step === 4 ? 1 : step + 1;
  };
  const io = new IntersectionObserver(
    ([entry]) => {
      if (entry.isIntersecting && !timer) {
        tick();
        timer = setInterval(tick, 2200);
      } else if (!entry.isIntersecting && timer) {
        clearInterval(timer);
        timer = null;
      }
    },
    { threshold: 0.3 },
  );
  io.observe(map);
  steps.forEach((li) =>
    li.addEventListener('mouseenter', () => {
      if (timer) {
        clearInterval(timer);
        timer = null;
      }
      step = Number(li.dataset.step);
      tick();
    }),
  );
}

function setYear() {
  document.querySelectorAll('[data-year]').forEach((el) => {
    el.textContent = String(new Date().getFullYear());
  });
}

setupPlayButtons();
setupNav();
mountMaps();
setupReveal();
setupLayerSwitch();
setupCatastroDemo();
setYear();
