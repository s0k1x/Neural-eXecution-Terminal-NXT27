# Neural eXecution Terminal · NXT27

Demo visual con estética de terminal hacker: intro de manos + chispa, ventana
emergente, lluvia matrix, logo **NXT27** con glitch, montañas ASCII en
movimiento y un navegador de módulos con navegación por teclado.

> **Aviso:** es una **demo visual**. Los módulos son cáscaras no funcionales
> ("DEMO · SIN FUNCIONALIDAD"): no ejecutan ni generan nada.

---

## 1. Abrir rápido (navegador)

Descarga `index.html` y haz doble clic. No necesita internet ni instalación.

## 2. Un solo comando (Termux / Linux)

Descarga, instala lo necesario, arranca un servidor local y abre el navegador:

```bash
curl -fsSL https://raw.githubusercontent.com/s0k1x/Neural-eXecution-Terminal-NXT27/main/nxt27.sh | bash
```

Se sirve en `http://localhost:8027`. Para detener: `Ctrl+C`.
Si no tienes `curl` en Termux: `pkg install -y curl` y repite.

## 3. App de escritorio (Windows .exe)

El `.exe` abre la terminal en su propia ventana (motor Edge WebView2 de Windows).

- **Descarga:** pestaña **Actions** → último run de `build-exe` → sección
  **Artifacts** → `NXT27-exe` (contiene `NXT27.exe` + `NXT27-publisher.cer`).
- También se adjunta a la **Release** si se publica un tag `v*`.

### Firma digital

`NXT27.exe` está firmado (Authenticode SHA-256, autofirmado). Al ser
autofirmado, SmartScreen puede avisar la primera vez
("Más información → Ejecutar de todas formas"). Para que Windows confíe en la
firma, instala `NXT27-publisher.cer` en *Entidades de certificación raíz de
confianza*. Una firma sin avisos requiere un certificado de code-signing de
una CA (de pago).

---

## Controles

| Acción            | Tecla                 |
|-------------------|-----------------------|
| Explorar tarjetas | ↑ ↓ ← →               |
| Abrir módulo      | Enter (o tocar)       |
| Cambiar categoría | Tab                   |
| Acceso directo    | 1–9                   |
| Volver            | Esc                   |
| Saltar intro      | botón **SKIP INTRO**  |

## Estructura

| Archivo                         | Qué es                                    |
|---------------------------------|-------------------------------------------|
| `index.html`                    | La demo (autónoma, sin dependencias)      |
| `nxt27.sh`                      | Instalador/lanzador de un comando         |
| `app.py`                        | Envoltorio de escritorio (pywebview)      |
| `.github/workflows/build-exe.yml` | Compila y firma `NXT27.exe` en Windows  |
