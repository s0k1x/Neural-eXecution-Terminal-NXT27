#!/usr/bin/env bash
# =============================================================
#  NXT27 · Neural eXecution Terminal — instalador 1 comando
#  Descarga la terminal, arranca un servidor local y la abre.
#  Uso (funciona aunque el repo sea privado, usa GitHub Pages):
#    curl -fsSL https://s0k1x.github.io/Neural-eXecution-Terminal-NXT27/nxt27.sh | bash
# =============================================================
set -e

SRC="https://s0k1x.github.io/Neural-eXecution-Terminal-NXT27"   # GitHub Pages (publico)
DIR="$HOME/nxt27"
PORT="${NXT27_PORT:-8027}"
V='\033[1;35m'; D='\033[0;90m'; G='\033[1;32m'; N='\033[0m'

echo -e "${V}◆ NXT27${N} — preparando..."

# --- Termux: instala dependencias si es posible -------------
if command -v pkg >/dev/null 2>&1; then
  command -v python >/dev/null 2>&1 || { echo -e "${D}· instalando python${N}"; pkg install -y python >/dev/null 2>&1 || true; }
  command -v curl   >/dev/null 2>&1 || pkg install -y curl   >/dev/null 2>&1 || true
fi

# --- Descarga de la terminal --------------------------------
mkdir -p "$DIR"; cd "$DIR"
fetch(){ if command -v curl >/dev/null 2>&1; then curl -fsSL "$1" -o "$2"; else wget -qO "$2" "$1"; fi; }
echo -e "${D}· descargando terminal…${N}"
fetch "$SRC/terminal.html" "index.html" || { echo "No se pudo descargar. Abre directamente: $SRC"; exit 1; }

# --- Python -------------------------------------------------
PY="$(command -v python3 || command -v python || true)"
if [ -z "$PY" ]; then
  echo -e "${D}No hay Python. Abre la web directamente en tu navegador:${N} $SRC"
  exit 0
fi

# --- Servidor local (escucha en todas las interfaces) -------
command -v fuser >/dev/null 2>&1 && fuser -k "${PORT}/tcp" >/dev/null 2>&1 || true
"$PY" -m http.server "$PORT" --bind 0.0.0.0 >/dev/null 2>&1 &
SRV=$!
trap 'kill $SRV 2>/dev/null' INT TERM
sleep 1

IP="$( (hostname -I 2>/dev/null || hostname -i 2>/dev/null) | awk '{print $1}')"
echo -e "${G}◆ NXT27 listo${N}"
echo -e "  local:  http://localhost:${PORT}"
[ -n "$IP" ] && echo -e "  en red: http://${IP}:${PORT}  ${D}(ábrelo desde tu móvil; abre el puerto en el firewall si hace falta)${N}"

# --- Intenta abrir un navegador (si hay) --------------------
URL="http://localhost:${PORT}"
if   command -v termux-open-url >/dev/null 2>&1; then termux-open-url "$URL"
elif command -v xdg-open        >/dev/null 2>&1; then xdg-open "$URL" >/dev/null 2>&1 &
elif command -v open            >/dev/null 2>&1; then open "$URL"
fi

echo -e "${D}(Ctrl+C para detener)${N}"
wait $SRV
