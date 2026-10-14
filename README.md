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
  "enabledPlugins": { "mis-skills@mis-skills": true }
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

## Licencias de terceros
Cada skill importada conserva su `LICENSE` original en su carpeta.

- MIT: find-skills, Taste Skill, gbro-collage-broll, claude-animation, lemo-opuscar
- Apache 2.0: HyperFrames y `media-use`
- **PolyForm Noncommercial 1.0.0: `onetake`. Solo uso no comercial.**

Para ahorrar espacio se quitaron los GIF/MP4 de demostración de los README de `onetake` y `gbro-collage-broll` (las imágenes de esos README apuntan a archivos que no están aquí).
