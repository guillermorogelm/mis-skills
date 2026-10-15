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
| `linkedin-roast` | Cinco perfiles critican tu LinkedIn y luego lo reescriben (titular, Acerca de, experiencia) | [linkedin-roast-skill](https://github.com/alexyc9381/linkedin-roast-skill) |

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
De [emotixco/claude-skills-founder](https://github.com/emotixco/claude-skills-founder). Va como su propio plugin, `founder@mis-skills` en `plugins/founder/`, porque todas sus skills leen `shared/conventions.md` en la raíz. Se llaman como `/founder:<skill>`. Guardan su salida en `founder/` del proyecto, igual que las `founder-*` de Jake, pero con nombres de archivo distintos, así que conviven y se pueden leer entre sí.

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

Para ahorrar espacio se quitaron los GIF/MP4 de demostración de los README de `onetake` y `gbro-collage-broll` (las imágenes de esos README apuntan a archivos que no están aquí). Lo mismo con la imagen principal del README de `linkedin-skills`; de ese repo tampoco se copiaron la copia para Codex, sus tests, sus evals ni sus archivos de desarrollo (`CLAUDE.md`, `AGENTS.md`, `.github/`). Del plugin `founder` de Emotix no se copiaron `commands/` (avisos de la v1 obsoleta), `evals/`, `examples/` ni `.github/`; su README todavía enlaza a esas carpetas.
