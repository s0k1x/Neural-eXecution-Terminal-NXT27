#!/usr/bin/env bash
# =============================================================
#  NXT27 · Neural eXecution Terminal — instalador 1 comando
#  Descarga, arranca un servidor local y abre el navegador.
#  Uso:
#    curl -fsSL https://raw.githubusercontent.com/s0k1x/Neural-eXecution-Terminal-NXT27/main/nxt27.sh | bash
# =============================================================
set -e

REPO_RAW="https://raw.githubusercontent.com/s0k1x/Neural-eXecution-Terminal-NXT27/main"
DIR="$HOME/nxt27"
PORT="${NXT27_PORT:-8027}"
V='\033[1;35m'; D='\033[0;90m'; N='\033[0m'

echo -e "${V}◆ NXT27${N} — preparando..."

# --- Termux: instala dependencias automáticamente -----------
if command -v pkg >/dev/null 2>&1; then
  command -v python >/dev/null 2>&1 || { echo -e "${D}· instalando python${N}"; pkg install -y python >/dev/null 2>&1; }
  command -v curl   >/dev/null 2>&1 || pkg install -y curl   >/dev/null 2>&1 || true
fi

# --- Descarga del archivo -----------------------------------
mkdir -p "$DIR"; cd "$DIR"
fetch(){ if command -v curl >/dev/null 2>&1; then curl -fsSL "$1" -o "$2"; else wget -qO "$2" "$1"; fi; }
echo -e "${D}· descargando index.html${N}"
fetch "$REPO_RAW/index.html" "index.html"

# --- Python -------------------------------------------------
PY="$(command -v python3 || command -v python || true)"
if [ -z "$PY" ]; then
  echo "No se encontró Python. Instálalo (Termux: pkg install python) y reintenta."
  exit 1
fi

# --- Servidor local -----------------------------------------
# libera el puerto si quedó algo abierto
if command -v fuser >/dev/null 2>&1; then fuser -k "${PORT}/tcp" >/dev/null 2>&1 || true; fi
"$PY" -m http.server "$PORT" --bind 127.0.0.1 >/dev/null 2>&1 &
SRV=$!
trap 'kill $SRV 2>/dev/null' INT TERM
sleep 1

URL="http://localhost:${PORT}"
echo -e "${V}◆ NXT27 listo${N} → ${URL}"

# --- Abre el navegador --------------------------------------
if   command -v termux-open-url >/dev/null 2>&1; then termux-open-url "$URL"
elif command -v xdg-open        >/dev/null 2>&1; then xdg-open "$URL" >/dev/null 2>&1 &
elif command -v open            >/dev/null 2>&1; then open "$URL"
else echo -e "${D}Abre manualmente esta URL en tu navegador:${N} $URL"
fi

echo -e "${D}(Ctrl+C para detener el servidor)${N}"
wait $SRV
