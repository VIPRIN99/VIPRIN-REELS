# VIPRIN — Centro de trabajo (Claude Code)

Repo de Patricio (artista, DJ y productor, Buenos Aires). Acá se guardan los videos de los Reels y desde acá Claude gestiona la publicación.
Datos privados (carrera, precios, métricas, audiencia, pauta): leelos con Claude Docs en "VIPRIN — Contexto privado" → https://claude.ai/artifact/492hNWyjiQ8wbmj4TfmDn6 . Si existe `CLAUDE.local.md` (en .gitignore), tiene lo mismo.

## Cómo hablarle
- Español rioplatense, directo, analítico y corto (mínimos tokens). No llamarlo "rey".
- Hacé el trabajo sin pedir permiso para lo que ya está definido acá. Preguntá solo si algo es irreversible o ambiguo.
- La edición de los Reels la hace Claude, no él: él graba y pasa clips crudos. No le devuelvas la edición.

## Marcas
- **VIPRIN** (IG @viprin.z, TikTok, YouTube, Spotify, taplink.cc/viprin). Objetivo: oyentes. Tres ramas: artista · DJ open format · productor de remixes.
- **Puzzle** (@puzzle.av, "Puzzle Audiovisual"). Servicios de producción y visuales (videolyrics, visualizers, instrumentales, mix y master). Objetivo: ventas.
- Géneros: reggaetón (old school), trap, techengue, UK garage. Herramientas: Premiere, After Effects, Photoshop, FL Studio, Blender, Rekordbox, Serato, ElevenLabs.

## Conectores (claude.ai)
- **Windsor.ai**: Instagram VIPRIN (cuenta `17841401478772783`), TikTok VIPRIN, Meta Ads. Para métricas (`get_data`) y para publicar (`execute_action`).
- **Notion**: base "⭐ Agenda semanal". La agenda va **solo** ahí. Nunca crear eventos en Google o Notion Calendar porque se duplican.
- **Claude Docs**: estrategia en "VIPRIN — Diagnóstico y estrategia de crecimiento" → https://claude.ai/artifact/V67Ao7z2cRXWoLUQsecB9F
- **Scheduled tasks** (Claude Code Remote: `list_triggers`, `create_trigger`): cada Reel de prueba es una tarea programada de una sola vez.
- Gmail.
Si un conector no aparece, pedile que lo active en claude.ai → Configuración → Conectores.

## Pipeline de Reels
1. **Video**: `videos/AAAA-MM-DD_HHMM_slug.mp4` (hora de Argentina). Material de anuncios en `ads/`.
2. **Push a `main`**: la URL pública es `https://raw.githubusercontent.com/VIPRIN99/VIPRIN-REELS/main/videos/<archivo>`. No borres ni renombres videos que tengan una tarea pendiente, porque se rompe la publicación.
3. **Tarea programada** (`create_trigger`, `run_once_at` en America/Buenos_Aires). Nombre: `Reel de prueba DD/MM HH:MM — <título>`. Prompt modelo:
   > Publicá un REEL DE PRUEBA en el Instagram de Patricio (@viprin.z) usando el conector Windsor.ai. REGLA OBLIGATORIA: tiene que salir como Reel de prueba (Trial Reel). Nunca publiques sin trial_params; si la llamada falla, NO reintentes sin trial_params ni de otra forma: reportá el error.
   > Paso 1: llamá mcp__Windsor_ai__execute_action con connector "instagram", account "17841401478772783", action "create_video_post", params {"video_url": "<URL raw>", "caption": "<caption>", "trial_params": {"graduation_strategy": "MANUAL"}}. Verificá que trial_params esté incluido antes de llamar.
   > Paso 2: en Notion, buscá en la base "Agenda semanal" la página "<título>" y poné "Publicación" en "Publicado" (o "Error" con el motivo si falló).
   > Paso 3: dejá un resumen de una línea: si se publicó como reel de prueba o no.
4. **Notion**: crear la página en "⭐ Agenda semanal" con el título exacto y "Publicación" en "Programado".
5. **Orden**: cada Reel nuevo va al próximo turno libre, en orden cronológico, rellenando huecos.

### "¿Ya están los Reels de prueba?"
Cruzá estas tres fuentes y respondé con una tabla (fecha · hora · título · estado):
- `list_triggers`: tareas pendientes (`next_run_at`) y última ejecución (`last_run.status`).
- `videos/`: que cada tarea tenga su `.mp4` en `main`.
- Notion "Agenda semanal": estado de "Publicación". Si hace falta, confirmá con Windsor que el Reel salió.
Marcá huecos (días sin los 3 turnos), tareas fallidas y videos sin tarea.

## Reglas de contenido (resumen del doc de estrategia)
- El DJ es el motor de la cuenta. La canción entra como "caballo de Troya": un clásico conocido en transición a su tema, o un remix o flip de un tema famoso.
- Instagram: 3 Reels por día como máximo (2 públicos y 1 de prueba). TikTok: 1-2 por día, reexportado con otro texto y otro primer frame.
- Horarios: los programados hoy son 9:00, 15:00 y 21:00. El doc recomienda 13:00 (DJ), 19:00 (productor o personaje) y 22:30 (prueba de artista). Confirmá con él antes de cambiarlos.
- Cada prueba testea una sola variable (hook, primer frame o caption). Una prueba con más de 300 vistas en 24 h y skip menor al 50% va al feed. Las pruebas estancadas se reeditan, no se borran.
- Hook: el primer frame es acción en curso, nunca intro ni logo. Texto en los primeros 0,5 s, máximo 7 palabras. El momento fuerte va primero. Artista 7-15 s, DJ 10-20 s. Final en loop.
- Caption: la frase de la canción o del tema conocido + 3-4 hashtags específicos. Sin #fyp, #viral ni #musica.
- Estética "dark purple": fondo negro con degradé violeta oscuro, nada de violeta claro ni estilo dibujito. Texto blanco con borde violeta. Animaciones con golpes, whooshes y SFX.
- Voz en off con IA: masculina, acento neutro (ElevenLabs).
- El contenido de personaje (él hablando, clips de stream) es lo que mejor funciona en TikTok y acompaña cada lanzamiento.
- Una canción por semana. Último: "SENSUAL". Actual: "No quiero la ambigüedad". Próxima: "Inimaginable" (UK garage, 130 BPM).
- La revisión semanal corre los domingos como tarea programada y escribe en el doc de estrategia.
