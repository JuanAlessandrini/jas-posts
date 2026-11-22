# jas-posts

Imágenes de las publicaciones diarias de JAS Software (carrusel de noticias de IA, tecnología y negocios) que se programan en Metricool.

- `plantilla/`: generador del carrusel (`gen.py` + `shot.js`), logo y un `slides_ejemplo.json`.
- `posts/AAAA-MM-DD/`: las 4 imágenes de cada día (`jas_noticias_AAAA-MM-DD_N.jpg`) y su `slides.json`.

Metricool toma las imágenes desde `https://raw.githubusercontent.com/JuanAlessandrini/jas-posts/main/posts/AAAA-MM-DD/<archivo>`.

Generar: `python3 -I plantilla/gen.py slides.json out && NODE_PATH=$(npm root -g) node plantilla/shot.js $(ls $PWD/out/*.html)`

## Carrusel con foto (rutina de las 8:00)

- `plantilla/gen_foto.py`: variante con foto real de Unsplash, badge de topic (Negocios / Tecnología), logo, título y descripción.
- Imágenes en `posts-foto/AAAA-MM-DD/` (`jas_foto_AAAA-MM-DD_N.png`) con su `slides.json`.
- Generar: `python3 -I plantilla/gen_foto.py slides.json out && NODE_PATH=$(npm root -g) node plantilla/shot.js $(ls $PWD/out/*.html)`

## Historias de tendencias (9:16)

- `plantilla/gen_historia.py`: genera historias 1080x1920 desde un `historias.json` (layouts: titular, tweet, meme, encuesta, dato, split), respetando las zonas seguras de Instagram (250 px arriba, 340 px abajo).
- `plantilla/shot_story.js`: como `shot.js` pero a 1080x1920 (o `SHOT_W`/`SHOT_H`).
- Imágenes en `historias-tendencias/AAAA-MM-DD/` (`historia_AAAA-MM-DD_N.png`) con su `historias.json`.
- Generar: `python3 -I plantilla/gen_historia.py historias.json out && NODE_PATH=$(npm root -g) node plantilla/shot_story.js $(ls $PWD/out/*.html)`
