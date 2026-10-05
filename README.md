# Leira — web oficial (landing)

Página estática, sin dependencias ni paso de build: `index.html` + `styles.css` + `main.js` +
`assets/`. Se puede servir tal cual desde cualquier hosting estático (GitHub Pages, Netlify,
Cloudflare Pages…) o abrir `index.html` directamente en el navegador.

Vive en `landing/` del repo de la app, fuera de `src/`: Metro/Expo no la empaquetan y el lint de la
app la ignora (`eslint.config.js`).

## Antes de publicar

- **Google Play**: pegar la URL de la ficha en `GOOGLE_PLAY_URL` (`main.js`). Mientras esté vacía,
  los botones dicen «Próximamente en Google Play»; con URL pasan solos a «Descargar en Google Play».
- **Dominio**: publicada en GitHub Pages, repo `asvdesarrolloweb-cmd/leira-web`
  (<https://asvdesarrolloweb-cmd.github.io/leira-web/>). Si cambia de dominio, actualizar
  `canonical`, `og:url` y `og:image` en `index.html`.

## Publicar cambios

Copiar el contenido de `landing/` al repo `leira-web` (rama `main`) y hacer push: GitHub Pages
redespliega solo en ~1 minuto.

## Identidad (tomada de la app, no inventada)

- Colores: paleta del Paywall (`src/components/PaywallModal.tsx`), esmeralda del tema oscuro
  (`src/constants/theme.ts`), dorado Premium de la corona del interruptor Catastro y colores del
  mapa (`src/components/leaflet-html.ts`).
- Logo/favicons: generados desde `assets/images/splash-icon.png` e `icon.png`.
- Iconos: Material Symbols (misma familia que los iconos de la app), solo los usados.
- Textos de los mockups: los de `src/constants/strings.ts`.

## Ilustración del mapa

El parcelario de los mockups lo genera `tools/build-map-art.py` (Python, sin dependencias) dentro
del `<template id="map-art">` de `index.html`; `main.js` lo clona en cada `[data-map]`. Para
cambiarlo, editar el script y ejecutarlo: `python landing/tools/build-map-art.py`.

## Iconos

Solo se descargan los iconos que usa la página (`icon_names=` en la URL de Google Fonts). Tras
añadir o quitar iconos, ejecutar `python landing/tools/update-icons.py`.

## Distintivo de Google Play

`assets/google-play-badge.png` es el distintivo oficial (en español) de Google Play. `main.js` solo
lo muestra, en el bloque final de descarga, cuando `GOOGLE_PLAY_URL` tiene valor.

## Páginas legales

Enlazadas desde el pie, publicadas en el repo `leira-privacidad` (GitHub Pages): privacidad,
aviso legal, términos y eliminación de cuenta.
