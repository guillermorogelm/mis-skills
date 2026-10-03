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
