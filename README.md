# jas-posts

Imágenes de las publicaciones diarias de JAS Software (carrusel de noticias de IA, tecnología y negocios) que se programan en Metricool.

- `plantilla/`: generador del carrusel (`gen.py` + `shot.js`), logo y un `slides_ejemplo.json`.
- `posts/AAAA-MM-DD/`: las 4 imágenes de cada día (`jas_noticias_AAAA-MM-DD_N.jpg`) y su `slides.json`.

Metricool toma las imágenes desde `https://raw.githubusercontent.com/JuanAlessandrini/jas-posts/main/posts/AAAA-MM-DD/<archivo>`.

Generar: `python3 -I plantilla/gen.py slides.json out && NODE_PATH=$(npm root -g) node plantilla/shot.js $(ls $PWD/out/*.html)`
