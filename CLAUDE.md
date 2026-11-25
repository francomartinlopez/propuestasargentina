# 100 propuestas para la Argentina

Sitio estático de Franco Martín López: https://propuestasargentina.netlify.app (Netlify publica la rama `main` en cada push, sin paso de armado).

## Regla de oro: nada se publica sin «publica»

- Todo cambio va a una rama aparte y a un pull request. Netlify arma sola una vista previa del pull request.
- Solo Franco decide publicar: dice «publica» en el chat (o toca «Merge» en GitHub). Nunca hacer merge ni push a `main` sin esa orden.
- No trabajar el mismo repositorio desde dos sesiones a la vez.

## Dónde está cada cosa

| Qué | Dónde | Se edita a mano |
|---|---|---|
| Las 100 propuestas (textos, datos, fuentes, mapas) | `datos/propuestas.json` | sí |
| Plan de los primeros 100 días | `datos/cien_dias.json` | sí |
| Cada norma, una sola vez | `fuente/normas/N###.json` | sí |
| Qué normas lleva cada propuesta y en qué orden | `fuente/normas_por_propuesta.json` | sí |
| Organismos de cada propuesta (árbol y externos) | `fuente/organismos/<n>.json` | sí |
| Portada, estilos y código del sitio | `index.html` | sí |
| Datos de normas del sitio, anexos, lista | `datos/normas/*.json`, `datos/anexo*.json` | **no**: los arma `armar_normas.py` |
| PDF de cada norma, compendio, PDF del programa | `datos/normas/pdf/`, `datos/normas/todas-las-normas.pdf`, `100-propuestas*.pdf` | **no** |
| Páginas e imágenes para compartir | `p/<n>/`, `og.jpg`, `icono-180.png` | **no**: las arma `compartir.py` |
| Cifras de la portada (normas, páginas, MB, fecha) | `index.html` | **no**: las pone `cifras.py` |
| Datos de los mapas interactivos (tramos, puertos, lugares, capas, obras) | `fuente/mapas/<mapa>/datos.json` | sí |
| Textos fijos, estilos y código de los mapas | `fuente/mapas/<mapa>/interior.html`, `pagina.html`, `embed.js` | sí, con cuidado |
| Mapas armados e imágenes para el PDF | `mapa-hidrovia.html`, `mapa-hidrovia-embed.js`, `mapa-integracion.html`, `mapa-embed.js`, `mapa-*.png` | **no**: los arma `mapas.py` |

Campos de una norma: `id`, `tipo` (ley_nacional, decreto, resolucion, acuerdo_federal, ley_provincial, tratado, ley_aprobatoria, ordenanza_modelo, invitacion), `titulo`, `sumilla`, `cuando`, `cuando_breve` (lo que muestra el anexo del PDF), `tramite`, `motivos`, `visto`, `considerando`, `formula`, `capitulos` (con `articulos`: `n`, `epigrafe`, `texto`), `modifica`, `deroga`, `variantes`. Mapas: un puerto, un tramo o un lugar nuevo se puede cargar con longitud y latitud (`lonlat`, `puntos` o `xy_lonlat`); `mapas.py` lo pasa a coordenadas del dibujo con la `proyeccion` de cada mapa. Si solo cambió un mapa: `python3 herramientas/mapas.py hidrovia` y después `pdf_programa.cjs completo`.

Una norma nueva necesita su archivo y su lugar en `normas_por_propuesta.json`; los números siguen la serie (la próxima es la siguiente libre).

## Armar y verificar

```
bash herramientas/armar.sh
```

Hace todo en orden: `armar_normas.py` → `pdf_normas.cjs` → `compendio.py` → `mapas.py` → `pdf_programa.cjs` → `compartir.py` → `cifras.py` → `verificar.py`. Tarda unos 4 minutos. Necesita python3 con pypdf, node con playwright (chromium) y poppler-utils. Si solo cambió el texto de una norma alcanza con `armar_normas.py`, `node herramientas/pdf_normas.cjs N###`, `compendio.py`, `pdf_programa.cjs completo` y `cifras.py`, pero ante la duda se corre todo. `verificar.py` tiene que terminar en «Todo en orden».

## Reglas de contenido (no negociables)

- Exactamente 100 propuestas.
- Registro formal pero accesible en los textos del programa: sin voseo ni tuteo («cada contribuyente paga», no «pagás»). El voseo va solo en la interfaz (botones, ayudas). «solo» sin tilde, «US$» y no «USD», montos aclarados en pesos.
- Vocabulario simple («impuesto a la importación», no «aranceles»). Sin odio, sin confrontación, sin adjetivos de campaña.
- No nombrar personas investigadas. No poner teléfonos ni correos personales. Nunca decir si alguien es o no candidato. En casos testigo se nombran hechos, no personas.
- Solo fuentes oficiales (INDEC, BCRA, Boletín Oficial, ministerios, Congreso, organismos provinciales, tratados). La prensa sirve para enterarse, no como fuente citada; si no hay fuente oficial, se dice y se marca con ⚠.
- Umbrales y cifras salen de estadísticas con fuente, no «a dedo». Lo estimado se marca con ⚠ y se aclara su alcance.
- Ninguna referencia a escritos personales inéditos ni a documentos privados (Dossier, Cuaderno de ruta, Entrevista).
- Nombres genéricos de organismos por función; la estructura de hoy va en `hoy`.
- Preferencias del autor: «convivencia de monedas»; RIGI condicionado a inversión en infraestructura; sin indulto a ex presidentes.
- Ninguna cifra fija escrita a mano que pueda quedar vieja (para eso está `cifras.py`).
- Las páginas en blanco de los PDF son a propósito (total par).

## Revisión semanal (la hace una tarea programada)

1. Clonar, crear la rama `semana-AAAA-MM-DD` desde `main`. Si hay un pull request semanal anterior sin publicar, partir de esa rama y sumarle los cambios (no abrir otro).
2. Buscar en la web lo ocurrido en la última semana que toque las propuestas:
   - leyes sancionadas o promulgadas, DNU, decretos y resoluciones (Boletín Oficial, Congreso, ministerios);
   - proyectos que el sitio describe en trámite (por ejemplo la Carta Orgánica del BCRA, Súper RIGI, apuestas online) y cualquier norma citada que haya cambiado o se haya derogado;
   - inversiones aprobadas (RIGI y regímenes provinciales), licitaciones y obras que el sitio menciona (hidrovía, Canal Magdalena, gasoductos, trenes);
   - datos oficiales nuevos de los «datos destacados» (IPC, EPH, SIPA, ISAC, UCII, mora, jubilación mínima y otros que cite cada propuesta).
3. Ajustar: datos y fechas, textos que quedaron falsos («espera la sanción» → «se sancionó»), normas del programa que ya no hacen falta o cambian por lo aprobado (se ajusta su texto o se avisa), fuentes con enlace oficial. Si algo exige cambiar el fondo de una propuesta, **no** cambiarlo: anotarlo como pregunta para Franco.
4. `bash herramientas/armar.sh` hasta «Todo en orden».
5. Commit con un mensaje claro y push de la rama; abrir o actualizar el pull request contra `main` con la lista de cambios (propuesta, qué cambió, fuente) y las preguntas para Franco. Netlify agrega el enlace de vista previa al pull request.
6. Si no hubo nada que cambiar, no abrir pull request.
