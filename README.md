# Neural eXecution Terminal · NXT27

Terminal **web funcional** con estética hacker: escribes comandos reales y se
ejecutan en tu navegador — con **pipes**, **redirección**, sistema de archivos
persistente, autocompletado, autosugerencias tipo Fish, temas, editor de texto
y un montón de comandos (incluidos clásicos divertidos como `cowsay`, `figlet`,
`lolcat`, `cmatrix`, `fortune`, `neofetch`).

Todo funciona **offline**, sin servidores. Prueba en vivo:
**https://s0k1x.github.io/Neural-eXecution-Terminal-NXT27/**

---

## Probarla

- **Navegador:** descarga `index.html` y doble clic. Nada que instalar.
- **Un comando (Termux/Linux):**
  ```bash
  curl -fsSL https://raw.githubusercontent.com/s0k1x/Neural-eXecution-Terminal-NXT27/main/nxt27.sh | bash
  ```
  Sirve en `http://localhost:8027`. (`pkg install -y curl` si falta en Termux.)
- **Windows `.exe`:** pestaña **Actions** → run de `build-exe` → **Artifacts** →
  `NXT27-exe` (`NXT27.exe` firmado + `NXT27-publisher.cer`). También se adjunta a
  la **Release** al publicar un tag `v*`.

---

## Comandos

- **Shell:** `help` `man` `clear` `exit` `history` `alias` `export` `env` `which` `type` `echo` `printf` `repeat` `sleep`
- **Archivos:** `ls` `cd` `pwd` `cat` `tac` `head` `tail` `tree` `find` `grep` `wc` `stat` `du` `mkdir` `rmdir` `touch` `rm` `mv` `cp` `edit`/`nano`
- **Texto:** `rev` `upper` `lower` `sort` `uniq` `nl` `tr` `base64` `rot13` `hash` `uuid` `urlencode` `urldecode` `json` `morse` `password` `seq` `cal`
- **Sistema:** `neofetch` `whoami` `uname` `hostname` `uptime` `date` `free` `df` `ps` `top` `battery` `theme`
- **Seguridad (pentest/CTF):** `hash` `hashid` `hex/unhex` `bin` `caesar` `atbash` `vigenere` `xor` `jwt` `cidr` `strength` `entropy` `portref/ports` `wifi` `nmap` `whois` `dig` `scan` `crack` `defang` `ua` (recon de red = SIMULADO/educativo)
- **IA / agente:** `ask` (chat + visión), `agent on` + `ai <petición>` (el agente ejecuta comandos de la terminal por ti), `ultra` (modo NXT ULTRA con contraseña y animación)
- **Red (simulado):** `ping` `traceroute` `ifconfig` `speedtest`
- **Dev:** `git` (init/add/commit/log/branch/checkout/diff sobre el FS virtual)
- **Nube (Supabase):** `wall` (muro global) · `save`/`load` (guardar en la nube con código) · `paste`/`getpaste` · `rank` · `stats`
- **Visual:** `dashboard` `chart` `plot` `gauge` `progress` `button` `card` `table` `palette` `color` `icon` `icons` `clock`
- **Diversión:** `figlet` `banner` `cowsay` `cowthink` `lolcat` `fortune` `matrix` `sl` `hack` `8ball` `dice` `coin` `roll` `rps` `guess` `joke` `yes`

Al abrir la terminal verás una **secuencia de arranque animada** y, la primera vez, un **asistente** para elegir color, nombre y efectos (reábrelo con `setup`). Los comandos visuales **generan cosas dentro de la terminal** (gráficos, botones clicables, tarjetas, medidores). La **nube** usa un backend propio en Supabase (muro compartido, guardado en la nube, pastebin, ranking).

**Potencia:**
```sh
figlet NXT27 | lolcat          # ASCII gigante en arcoíris
fortune | cowsay               # cita aleatoria en una vaca
echo hola | upper | rev        # pipes encadenados
seq 100 | tail -5              # tubería con utilidades
echo "nota" > diario.txt       # redirección a archivo (persiste)
theme matrix                   # cambia el tema de color
```

**Atajos:** `↑`/`↓` historial · `→` acepta la sugerencia fantasma · `Tab`
autocompleta · `Ctrl+L` limpia · `Ctrl+C` cancela · `Ctrl+U` borra la línea.
En el editor: `Ctrl+S` guarda, `Esc` sale. Funciona en móvil (toca y escribe).

El estado (archivos, historial, tema, alias) se guarda en tu navegador.

---

## Estructura

| Archivo | Qué es |
|---|---|
| `index.html` | La terminal (autónoma, sin dependencias) |
| `site/` + `.github/workflows/pages.yml` | Landing web + deploy a GitHub Pages |
| `nxt27.sh` | Instalador/lanzador de un comando |
| `app.py` + `.github/workflows/build-exe.yml` | App de escritorio `.exe` (firmada) |
