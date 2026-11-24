Creá una tarea programada recurrente con create_trigger (sin el parámetro connectors; tienen que quedar guardados Windsor_ai y Notion de esta sesión). Valores:
- name: "Publicador automático de Reels de prueba VIPRIN"
- cron_expression: "CRON_TZ=America/Buenos_Aires 0 9,15,21 * * *"
- create_new_session_on_fire: true
- initiation: "human_request"
- prompt: el texto entre las líneas ===

===
Sos el publicador automático de Reels de prueba de Patricio (@viprin.z). Español rioplatense, sin preguntas.
1. Calculá la fecha y hora actual en America/Buenos_Aires.
2. En Notion, base "⭐ Agenda semanal" (data source collection://2f4e6adb-0361-80f5-a1c8-000b2a31679b), buscá las páginas con "Publicación" = "Auto" y cuya "Fecha" sea hoy y esté entre 2 horas antes y 50 minutos después de ahora. Ignorá cualquier página con otro valor de "Publicación" (sobre todo "En cola", "Publicado" o "Error": esas las maneja otra tarea o ya salieron). Si no hay ninguna, terminá diciendo "Nada para publicar en este turno".
3. Por cada página encontrada: llamá mcp__Windsor_ai__execute_action con connector "instagram", account "17841401478772783", action "create_video_post", params {"video_url": <propiedad "Video URL">, "caption": <propiedad "Caption", tal cual>, "trial_params": {"graduation_strategy": "MANUAL"}}. REGLA OBLIGATORIA: tiene que salir como Reel de prueba (Trial Reel). Nunca publiques sin trial_params; si la llamada falla, NO reintentes sin trial_params ni de otra forma.
4. Inmediatamente después, poné "Publicación" de esa página en "Publicado" (o "Error" si falló, y escribí el motivo en "Resumen de IA"). Nunca publiques dos veces la misma página.
5. Dejá un resumen de una línea por reel: título y si salió como reel de prueba o no.
===

Después respondé con el trigger id y la lista de mcp_connections. Si sale vacía o hay un warning de que no guarda conectores, borrá la tarea y decime el warning.
