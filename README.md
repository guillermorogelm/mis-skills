# mis-skills

Marketplace personal de skills para Claude Code.

## Agregar una skill nueva
Copia la carpeta de la skill (la que contiene `SKILL.md`) a `plugins/mis-skills/skills/`, haz commit y push.

## Usarlo en un proyecto (local o en la nube)
Agrega esto a `.claude/settings.json` del proyecto (cambia USUARIO):

```json
{
  "extraKnownMarketplaces": {
    "mis-skills": { "source": { "source": "github", "repo": "USUARIO/mis-skills" } }
  },
  "enabledPlugins": {
    "mis-skills@mis-skills": true,
    "linkedin-skills@mis-skills": true,
    "founder@mis-skills": true
  }
}
```

## Cómo usarlas

### Llamar una skill
Hay tres plugins, y el nombre de cada skill lleva el del plugin delante:

| Plugin | Cómo se llama | Ejemplo |
|---|---|---|
| `mis-skills` | `/mis-skills:<skill>` | `/mis-skills:product-manager una app de reservas para spas` |
| `founder` (Emotix) | `/founder:<skill>` | `/founder:pricing-strategy asistente de WhatsApp para spas` |
| `linkedin-skills` | `/linkedin-skills:<skill>` | `/linkedin-skills:linkedin-post-writer sobre mi primer cliente` |

No hace falta escribir el nombre: si pides algo en lenguaje normal («escríbeme un PRD», «audita este post de LinkedIn»), Claude elige la skill por su descripción. Llámala por nombre cuando varias podrían servir (hay varias de diseño, de video y dos sets de fundador) o cuando quieras una en concreto.

Después de cambiar algo en este repo, abre una sesión nueva: los plugins se cargan al iniciar.

### Dónde dejan su trabajo
Varias skills guardan archivos para que la siguiente los lea. Conviene saber dónde:

| Skills | Guardan en | Nota |
|---|---|---|
| `founder-*` (Jake) | `founder/` del proyecto (`competitors.md`, `pricing.md`, `cfo.md`, `numbers.json`, `panel/`…) | Cada una lee lo que dejaron las anteriores |
| `/founder:*` (Emotix) | `founder/` del proyecto (`facts.md` + un archivo por skill: `pricing-strategy.md`…) | `facts.md` guarda los datos que tú diste; si dices algo nuevo, gana lo nuevo |
| `linkedin-*` | `references/story-bank.md` y `references/voice-profile.md` **dentro de la carpeta del plugin** | Una actualización del plugin puede pisarlos: guarda una copia aparte y no los subas a este repo público |
| `night-crew` | `NIGHT-CREW.md` en la raíz de tu repo | Las rutinas lo leen cada noche desde la rama principal |
| `harvey` | `~/harvey` (base de datos, `.env`, `harvey.yaml`) | Fuera de tus proyectos |
| `cinematic-site-prompt` | `<sitio>-cinematic-prompt.md` en la carpeta actual | |

### Lo que necesitan
- **Claves propias:** `linkedin-skills` (Publora para publicar o leer, Apify para analizar interacciones; ver `plugins/linkedin-skills/.env.example`), `gbro-collage-broll` (Gemini, y `ffmpeg`).
- **Plan de Claude Pro o Max:** `night-crew` (rutinas en la nube) y `harvey` (usa tu suscripción en vez de una API).
- **Python 3:** `shark`, `court`, `launch`, `founder-cfo`, `founder-consumer`, `founder-pricing`, `founder-plan`, `harvey`, `gbro-collage-broll`, `onetake`.
- **Node:** las de video (`hyperframes`, `motion-director`, `onetake`, `claude-animation`, `lemo-opuscar`). `onetake` y `claude-animation` además usan Chrome y `ffmpeg` para renderizar.
- `gbro-collage-broll` está pensada para Codex: su paso de imagen usa el generador de imágenes de Codex.

### ¿Qué uso para…?

| Quiero… | Usa |
|---|---|
| Saber si una idea vale la pena, rápido | `court` (juicio) o `shark` (inversores) |
| Validar y planear un negocio completo | cadena `founder-*` o `/founder:*` (ver abajo) |
| Ponerle precio a un servicio o armar una propuesta | `/founder:competitor-matrix` → `founder-pricing` o `/founder:pricing-strategy` → `founder-offer` |
| Definir qué construir antes de programar | `product-manager` |
| Diseñar o rediseñar una web | `design-inspiration` → `art-director` o `design-taste-frontend` (+ un estilo: `minimalist-ui`, `high-end-visual-design`, `industrial-brutalist-ui`); `redesign-existing-projects` si ya existe; `stitch-design-taste` si usas Google Stitch |
| Un prompt largo para una web cinematográfica | `cinematic-site-prompt` |
| Un prompt para un juguete 3D interactivo | `tactile-toy-prompt` |
| Kit de marca o identidad | `founder-brand` (nombre, voz, promesa) → `brandkit` (las láminas visuales) |
| Revisar código antes de publicar | `code-reviewer`, luego `launch` (GO / NO-GO) |
| Que Claude trabaje de noche en mi repo | `night-crew` |
| Conseguir clientes | `agency` (correos, llamadas, propuestas) o `harvey` (automático, con tu aprobación) |
| Mejorar mi LinkedIn | `linkedin-roast` o `/linkedin-skills:linkedin-profile-optimizer` |
| Escribir posts o guiones de reels | `content-principles` + `/linkedin-skills:linkedin-post-writer` |
| Un video | ver «Video» abajo |
| Que no recorte código ni deje «TODO» | `full-output-enforcement` |
| Encontrar más skills | `find-skills` |

## Cómo combinarlas

Cada receta va de lo barato a lo caro: primero lo que descarta rápido, después lo que cuesta tiempo.

### 1. De idea a negocio
1. **Filtro rápido:** `/mis-skills:court <idea>` o `/mis-skills:shark <idea>`. Si no sobrevive, no gastes más.
2. **Elige un set de fundador:**
   - **`founder-*` (Jake)** para un negocio con números de calle: un local, un servicio, un producto físico. Simula un panel de compradores y saca unit economics. Orden: `founder-board` → `founder-competitors` → `founder-consumer` → `founder-pricing` → `founder-offer` → `founder-cfo` → `founder-marketing` → `founder-brand` → `founder-ops` → `founder-launch` → `founder-plan`.
   - **`/founder:*` (Emotix)** para software o una startup: competidores con fuentes, MVP, landing y ronda. Orden sugerido: `validate-idea` → `product-brief` → `competitor-matrix` → `persona-gen` → `user-interviews` → `mvp-scope` → `pricing-strategy` → `go-to-market` → `landing-page` y `email-sequence` → `metrics-dashboard` → `pitch-deck` → `fundraise-prep`.
3. **Mezclar los dos sets:** no se leen solos. Pásale el archivo del otro: «`/founder:pricing-strategy` usa `founder/competitors.md` y `founder/panel/results.md` como fuente». Lo que pones en el pedido gana sobre lo guardado.
4. **Antes de lanzar:** `founder-launch` propone una prueba real barata (lista de espera, preventa). Hazla antes de construir de verdad.

### 2. De idea a producto publicado
1. `product-manager`: entrevista y PRD con criterios de aceptación.
2. `design-inspiration` → `art-director` o `design-taste-frontend` para la dirección visual; agrega un estilo si quieres uno concreto.
3. Mientras construyes: `full-output-enforcement` para archivos completos.
4. `code-reviewer` para encontrar y arreglar fallos uno por uno.
5. `launch`: 8 revisores dan GO o NO-GO. Un NO-GO se arregla antes de publicar.
6. `night-crew`: después de publicar, la lista de pendientes avanza cada noche con pull requests que tú apruebas.

### 3. Web nueva o rediseño (por ejemplo guillermorogel.com)
1. `/mis-skills:cinematic-site-prompt https://tusitio.com`: lee el sitio actual y escribe el prompt completo, con solo contenido real.
2. `design-inspiration` para elegir referencias antes de construir.
3. Construye con el prompt + `art-director` o `design-taste-frontend`; `redesign-existing-projects` si conservas la base actual.
4. `founder-brand` y `brandkit` si también cambia la identidad.
5. `launch` antes de apuntar el dominio.
6. Para una pieza 3D interactiva dentro del sitio: `tactile-toy-prompt`.

### 4. Conseguir clientes (QuitoWeb)
1. **La oferta primero:** `/founder:competitor-matrix` (precios con fuente) → `founder-pricing` o `/founder:pricing-strategy` → `founder-offer` (bonos y garantía).
2. **La prueba social:** `content-principles` para el gancho y un video corto (receta 6) que muestre el resultado.
3. **El contacto:** `agency` si quieres escribir y revisar tú cada correo y preparar llamadas; `harvey` si prefieres que busque negocios y redacte solo, con tu aprobación antes de cada envío. No uses los dos sobre la misma lista.
4. **Mientras duermes:** el scout de `night-crew` busca dónde habla tu cliente y redacta una semana de posts.
5. **Cerrar:** `/founder:landing-page` para la página de la oferta y `/founder:email-sequence` para el seguimiento.

### 5. Marca personal en LinkedIn
1. `linkedin-roast` (cinco críticos y luego la reescritura) o `/linkedin-skills:linkedin-profile-optimizer`.
2. `/linkedin-skills:linkedin-interviewer`: te entrevista y llena el banco de historias que leen las demás.
3. `/linkedin-skills:linkedin-content-planner`: plan de 7 días.
4. `/linkedin-skills:linkedin-post-writer` + `content-principles` para cada post; `linkedin-repurposer` si partes de un video o blog.
5. `/linkedin-skills:linkedin-humanizer --mode audit` antes de publicar.
6. Después: `linkedin-comment-drafter` y `linkedin-reply-handler` para conversar, `linkedin-thread-monitor` para ver quién respondió, `linkedin-engager-analytics` para saber quién interactúa.

### 6. Video
Elige el motor según el resultado:

| Quiero | Skill |
|---|---|
| Cualquier video desde HTML: promo, explicador, subtítulos, slideshow | `hyperframes` (entra siempre por aquí; ella llama a sus sub-skills) |
| 10–20 s con banda sonora original | `motion-director` |
| Demo de producto en un solo plano, sin cortes | `onetake` |
| Insertos de B-roll de collage de papel (~5 s) | `gbro-collage-broll` |
| Caricatura pintada a mano con Clawd | `claude-animation` |
| Corto en uno de 43 estilos de cine | `lemo-opuscar` |

Para combinarlas:
1. `content-principles` para el guion y el gancho.
2. El video principal con `onetake` o `hyperframes`.
3. Insertos de `gbro-collage-broll` o `claude-animation` donde el guion se pone abstracto.
4. Montaje y sonido en HyperFrames: `media-use` para música, voz y efectos; `hyperframes-audio` para la mezcla.

### 7. Mantener este repo
- `run-mis-skills` (solo dentro de este repo): valida, instala y prueba las skills. Úsala antes de subir una skill nueva.
- `find-skills` para buscar más.

## Skills incluidas

### Propias
| Skill | Para qué |
|---|---|
| `art-director` | Dirección de arte editorial para páginas web |
| `code-reviewer` | Auditoría de código con prueba de cada hallazgo |
| `motion-director` | Videos cortos (10–20 s) con banda sonora, en JS |
| `product-manager` | Entrevista, PRD y control de alcance |
| `claude-animation` | Caricaturas pintadas a mano con Clawd (p5.brush). Envuelve el kit de ClaudeAnimationBase |
| `design-inspiration` | Elige referencias reales de las galerías de mkdir.directory antes de diseñar |
| `tactile-toy-prompt` | Convierte una idea de una línea en un prompt para un juguete 3D blando en un solo HTML con three.js (estilo "Squishy Toast" / "Gummy Bears") |
| `cinematic-site-prompt` | Prompt largo y detallado (2.000–3.500 palabras) para un sitio web cinematográfico guiado por scroll: escenas, motion, rendimiento, accesibilidad, SEO y checklist. Usa solo contenido real del sitio actual |

### Descubrir más skills
| Skill | Fuente |
|---|---|
| `find-skills` | [vercel-labs/skills](https://github.com/vercel-labs/skills) (skills.sh) |

### Diseño frontend (Taste Skill)
De [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) ([tasteskill.dev](https://www.tasteskill.dev)).

| Skill | Para qué |
|---|---|
| `design-taste-frontend` | La principal (v2): infiere la dirección de diseño y evita interfaces genéricas |
| `redesign-existing-projects` | Auditoría visual y rediseño de un proyecto existente |
| `full-output-enforcement` | Salida completa, sin placeholders ni secciones omitidas |
| `high-end-visual-design` | Estilo suave, caro, mucho aire |
| `minimalist-ui` | Estilo editorial minimalista |
| `industrial-brutalist-ui` | Estilo brutalista / suizo |
| `brandkit` | Kit de marca |
| `stitch-design-taste` | Reglas compatibles con Google Stitch y export DESIGN.md |

### Video con código
Seleccionadas de [awesome-claude-video-skills](https://github.com/zhuyansen/awesome-claude-video-skills).

| Skill | Para qué | Fuente |
|---|---|---|
| `hyperframes` (+ `hyperframes-core`, `-cli`, `-animation`, `-audio`, `-creative`, `-keyframes`, `-registry`, `-studio`, `media-use`) | HTML → MP4 determinista. Empieza siempre por `hyperframes`; instala los flujos de creación bajo demanda con `npx hyperframes skills update <flujo>` | [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) |
| `onetake` | Clips de producto de un solo plano, sin cortes | [feitangyuan/onetake](https://github.com/feitangyuan/onetake) |
| `gbro-collage-broll` | B-roll de collage de papel con halftone | [pyang5166/gbro-collage-broll](https://github.com/pyang5166/gbro-collage-broll) |
| `claude-animation` | Clawd en animación pintada a mano | [JohnHeibel/ClaudeAnimationBase](https://github.com/JohnHeibel/ClaudeAnimationBase) |
| `lemo-opuscar` | Cortos en 43 estilos de cine; descarga la librería a `~/lemo-opuscar` en el primer uso | [lemomo-ai/lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar) |

### Negocio y lanzamiento (Alex Chen)
De [@alexyc9381](https://github.com/alexyc9381). Varias usan scripts de Python incluidos en la carpeta de la skill.

| Skill | Para qué | Fuente |
|---|---|---|
| `agency` | Agencia de automatización con IA: correos en frío, preparación de llamadas, propuestas y flujos | [agency-skill](https://github.com/alexyc9381/agency-skill) |
| `shark` | Presenta tu idea a 5 inversores estilo Shark Tank que la interrogan y deciden IN u OUT | [shark-skill](https://github.com/alexyc9381/shark-skill) |
| `court` | Juicio a una idea: fiscal, defensa, 12 jurados y un juez que lee el veredicto | [court-skill](https://github.com/alexyc9381/court-skill) |
| `launch` | Revisión pre-lanzamiento estilo NASA: 8 controladores dan GO o NO-GO a tu app | [launch-skill](https://github.com/alexyc9381/launch-skill) |
| `night-crew` | Tres rutinas nocturnas en la nube sobre tu repo de GitHub: un builder que hace la siguiente feature, un scout que busca clientes y redacta posts, y un tracker que revisa qué funciona. Solo abren pull requests; `/night-crew morning` da el resumen | [night-crew-skill](https://github.com/alexyc9381/night-crew-skill) |
| `harvey` | Instala y maneja [Harvey](https://github.com/ethanplusai/harvey) (de Ethan Rogers, MIT), un agente de ventas autónomo que busca negocios, escribe correos en frío y los envía solo con tu aprobación, usando tu plan de Claude. La skill es un lanzador propio; la app se clona en `~/harvey` | propia |
| `linkedin-roast` | Cinco perfiles critican tu LinkedIn y luego lo reescriben (titular, Acerca de, experiencia) | [linkedin-roast-skill](https://github.com/alexyc9381/linkedin-roast-skill) |

### Contenido
| Skill | Para qué | Fuente |
|---|---|---|
| `content-principles` | La psicología del contenido corto (reels, TikTok, Shorts, ganchos): cómo piensa quien mira, sin plantillas | [aiwithremy/content-principles](https://github.com/aiwithremy/content-principles), de Remy Gaskell. **Sin licencia** (ver abajo) |

### Fundadores (Jake Schincariol)
De [Jakeschincariol/founder-skill](https://github.com/Jakeschincariol/founder-skill). Se usan juntas: cada una lee lo que escribieron las anteriores y `founder-plan` lo compila en un plan de negocio.

| Skill | Para qué |
|---|---|
| `founder-board` | Junta directiva de 3 que evalúa la idea con marcos publicados |
| `founder-competitors` | Mapa de competidores y el hueco que dejan |
| `founder-consumer` | Panel de compradores simulados (100 por defecto) que reaccionan al pitch |
| `founder-pricing` | Precio que pagarían (Van Westendorp) frente a competidores y costos |
| `founder-offer` | Oferta irresistible: problemas, soluciones, bonos y garantía |
| `founder-cfo` | Unit economics, punto de equilibrio y caja del año 1 |
| `founder-marketing` | Posicionamiento, canales y campaña de 30 días |
| `founder-brand` | Nombre, voz, promesa y brief visual |
| `founder-ops` | Proveedores, turnos, rutinas, herramientas y permisos |
| `founder-launch` | Plan de lanzamiento con prueba real primero y cuenta regresiva |
| `founder-plan` | Compila todo en un plan de negocio con veredicto |

### Fundador (Emotix) - plugin aparte
De [emotixco/claude-skills-founder](https://github.com/emotixco/claude-skills-founder). Va como su propio plugin, `founder@mis-skills` en `plugins/founder/`, porque todas sus skills leen `shared/conventions.md` en la raíz. Se llaman como `/founder:<skill>`. Guardan su salida en `founder/` del proyecto, igual que las `founder-*` de Jake, pero con nombres de archivo distintos, así que conviven sin pisarse. Cada set lee solo sus propios archivos; para usar el trabajo del otro, nómbralo en el pedido (ver «Cómo combinarlas»).

| Skill | Para qué |
|---|---|
| `validate-idea` | Valida una idea antes de construir |
| `competitor-matrix` | Matriz de competidores con precios y fuentes |
| `pricing-strategy` | Estrategia de precios y niveles |
| `persona-gen` | Perfiles de cliente |
| `product-brief` | Brief de producto |
| `mvp-scope` | Alcance del MVP |
| `user-interviews` | Guion y síntesis de entrevistas |
| `go-to-market` | Plan de lanzamiento al mercado |
| `landing-page` | Texto de la landing page |
| `email-sequence` | Secuencia de correos |
| `metrics-dashboard` | Métricas a seguir |
| `pitch-deck` | Pitch deck |
| `fundraise-prep` | Preparación de la ronda |

### LinkedIn (Serge Bulaev) - plugin aparte
De [sergebulaev/linkedin-skills](https://github.com/sergebulaev/linkedin-skills). Va como su propio plugin, `linkedin-skills@mis-skills` en `plugins/linkedin-skills/`, porque sus skills comparten `references/`, `lib/` y `scripts/` en la raíz. Se llaman como `/linkedin-skills:<skill>`. Publicar o leer LinkedIn necesita una clave de [Publora](https://publora.com) o su conector; el análisis de interacciones, una de [Apify](https://apify.com) (ver `plugins/linkedin-skills/.env.example`).

| Skill | Para qué |
|---|---|
| `linkedin-post-writer` | Escribe un post desde cero con una de 20 fórmulas de gancho |
| `linkedin-comment-drafter` | Comenta o comparte un post a partir de su URL |
| `linkedin-reply-handler` | Responde un comentario o barre un hilo completo |
| `linkedin-humanizer` | Quita las marcas de texto de IA y audita antes de publicar |
| `linkedin-hook-extractor` | Saca la fórmula de gancho de un post viral |
| `linkedin-profile-optimizer` | Audita y reescribe un perfil completo |
| `linkedin-content-planner` | Plan de contenido de 7 días |
| `linkedin-repurposer` | Convierte un tweet, video o blog en post nativo |
| `linkedin-interviewer` | Te entrevista y arma un banco de historias para tus posts |
| `linkedin-employee-advocacy` | Programa de advocacy para un equipo |
| `linkedin-thread-monitor` | Sigue qué comentarios tuyos recibieron respuesta del autor |
| `linkedin-engager-analytics` | Segmenta a quienes dieron like o comentaron un post |

## Licencias de terceros
Cada skill importada conserva su `LICENSE` original en su carpeta.

- MIT: find-skills, Taste Skill, gbro-collage-broll, claude-animation, lemo-opuscar, las skills de Alex Chen (`agency`, `shark`, `court`, `launch`, `linkedin-roast`, `night-crew`), las `founder-*`, `linkedin-skills` y el plugin `founder` de Emotix
- Apache 2.0: HyperFrames y `media-use`
- **PolyForm Noncommercial 1.0.0: `onetake`. Solo uso no comercial.**
- **Sin licencia: `content-principles`.** El repo original no tiene archivo de licencia, así que los derechos son del autor. Se incluye sin cambios para uso personal, como sugiere su README; ver `SOURCE.md` en su carpeta. Si el autor lo pide, hay que quitarla.

Para ahorrar espacio se quitaron los GIF/MP4 de demostración de los README de `onetake` y `gbro-collage-broll` (las imágenes de esos README apuntan a archivos que no están aquí). Lo mismo con la imagen principal del README de `linkedin-skills`; de ese repo tampoco se copiaron la copia para Codex, sus tests, sus evals ni sus archivos de desarrollo (`CLAUDE.md`, `AGENTS.md`, `.github/`). Del plugin `founder` de Emotix no se copiaron `commands/` (avisos de la v1 obsoleta), `evals/`, `examples/` ni `.github/`; su README todavía enlaza a esas carpetas.
