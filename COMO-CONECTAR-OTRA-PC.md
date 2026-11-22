# Cómo conectar otra PC (o arreglar esta)

Objetivo: que Claude en la nube use tu carpeta de trabajo vía Remote Control, sin perder contexto.

## 1. Carpeta única
- Usá **`C:\Claude Workspace`**. No la pongas en OneDrive, Documentos sincronizados ni dentro de una carpeta oculta (las que empiezan con punto, ni `AppData`).
- Si ya la tenés en `Documentos` u `OneDrive\Documentos`, movela a `C:\Claude Workspace`.

## 2. Actualizar Claude
1. Abrí la app de escritorio de Claude → menú (☰ o tu nombre) → **Buscar actualizaciones**. Instalá si hay.
2. Cerrala del todo: clic derecho en el ícono de Claude en la bandeja (al lado del reloj) → **Salir**.
3. Volvé a abrirla.
4. Si usás Claude Code en terminal, en PowerShell:
   ```
   claude update
   claude --version
   ```

## 3. Remote Control
1. App de Claude → **Configuración → Claude Code → Remote Control**.
2. Activá Remote Control.
3. Dejá **una sola carpeta**: `C:\Claude Workspace`. Borrá las demás entradas (ej. "C--Claude-Workspace" duplicada).
4. Dejá la app abierta (puede quedar minimizada en la bandeja).

## 4. Plan B (si la nube no la ve)
En PowerShell:
```
cd "C:\Claude Workspace"
claude remote-control
```
Dejá esa ventana abierta. La sesión aparece en la app de Claude y en el celular.

## 5. Contexto de VIPRIN
En PowerShell (necesita Git instalado: https://git-scm.com):
```
cd "C:\Claude Workspace"
git clone https://github.com/VIPRIN99/VIPRIN-REELS.git
```
- `VIPRIN-REELS\CLAUDE.md` tiene marcas, pipeline de Reels, conectores y reglas de contenido.
- Datos privados: Claude Doc "VIPRIN — Contexto privado". Estrategia: "VIPRIN — Diagnóstico y estrategia de crecimiento". Los links están en el CLAUDE.md.
- Si querés una copia local de lo privado, va en `CLAUDE.local.md` (no se sube a GitHub). Nunca pongas precios ni métricas en otro archivo del repo.
