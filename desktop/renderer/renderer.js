"use strict";
/* NXT27 desktop — xterm UI over a real mini-shell (child_process). */

const term = new window.Terminal({
  fontFamily: '"JetBrains Mono", ui-monospace, Menlo, Consolas, monospace',
  fontSize: 14, cursorBlink: true, allowProposedApi: true,
  theme: {
    background: "#050308", foreground: "#d9d2ea", cursor: "#c084fc", cursorAccent: "#050308",
    selectionBackground: "#3b2a55",
    black: "#1a1324", brightBlack: "#564d6e", red: "#f87171", brightRed: "#fca5a5",
    green: "#4ade80", brightGreen: "#86efac", yellow: "#e3b341", brightYellow: "#fbbf24",
    blue: "#60a5fa", brightBlue: "#93c5fd", magenta: "#a855f7", brightMagenta: "#c084fc",
    cyan: "#22d3ee", brightCyan: "#67e8f9", white: "#d9d2ea", brightWhite: "#ffffff",
  },
});
const fit = new window.FitAddon.FitAddon();
term.loadAddon(fit);
try { term.loadAddon(new window.WebLinksAddon.WebLinksAddon()); } catch (_) {}
term.open(document.getElementById("term"));
function doFit(){ try { fit.fit(); } catch(_){} }
requestAnimationFrame(doFit); window.addEventListener("resize", doFit);

const C = { v: "\x1b[95m", d: "\x1b[90m", r: "\x1b[0m", g: "\x1b[92m", y: "\x1b[93m" };
let line = "", history = [], hi = -1, busy = false;

function banner(){
  term.writeln(C.v + "  ███╗   ██╗██╗  ██╗████████╗██████╗ ███████╗" + C.r);
  term.writeln(C.v + "  ██╔██╗ ██║ ╚███╔╝    ██║    █████╔╝    ██╔╝ " + C.r);
  term.writeln(C.v + "  ██║ ╚████║██╔╝ ██╗   ██║   ███████╗   ██║  " + C.r);
  term.writeln(C.d + "  Neural eXecution Terminal · escritorio · comandos reales" + C.r);
  term.writeln(C.d + "  escribe: git --version · python -V · npm -v · dir/ls · help" + C.r);
}
async function prompt(){
  const c = await window.nxt.cwd();
  term.write("\r\n" + C.v + "nxt" + C.d + " " + c + C.r + "> ");
}
function redraw(){ // redraw current line after history nav
  term.write("\x1b[2K\r");
  window.nxt.cwd().then(c => term.write(C.v + "nxt" + C.d + " " + c + C.r + "> " + line));
}

term.onData(async (d) => {
  if (busy) return;
  for (const ch of d) {
    const code = ch.charCodeAt(0);
    if (ch === "\r") {
      term.write("\r\n");
      const cmd = line.trim(); line = ""; hi = -1;
      if (cmd) {
        history.push(cmd);
        if (/^help$/i.test(cmd)) { term.writeln(C.g + "Ejecuta cualquier comando de tu sistema (git, python, npm, dir...). 'clear' limpia." + C.r); await prompt(); continue; }
        busy = true;
        const res = await window.nxt.run(cmd);
        busy = false;
        if (res.clear) term.clear();
        else if (res.out) term.write(res.out.replace(/\r?\n/g, "\r\n"));
      }
      await prompt();
    } else if (code === 127) { // backspace
      if (line.length) { line = line.slice(0, -1); term.write("\b \b"); }
    } else if (code === 27) { // escape seq (arrows)
      // handled below via full sequence check
    } else if (code >= 32) {
      line += ch; term.write(ch);
    }
  }
  // arrow history (sequences arrive as \x1b[A / \x1b[B)
  if (d === "\x1b[A") { if (history.length && hi < history.length - 1) { hi++; line = history[history.length - 1 - hi] || ""; redraw(); } }
  else if (d === "\x1b[B") { if (hi > 0) { hi--; line = history[history.length - 1 - hi] || ""; } else { hi = -1; line = ""; } redraw(); }
});

// tools bar + setup
let missing = [];
window.nxt.checkTools().then((t) => {
  const order = ["git", "python", "node", "npm"];
  document.getElementById("tools").innerHTML = order.map(k => `<span class="tool ${t[k] ? "ok" : "no"}">${t[k] ? "✓" : "✕"} ${k}</span>`).join(" ");
  missing = order.filter(k => !t[k] && k !== "npm");
  const btn = document.getElementById("setup");
  if (missing.length && window.nxt.platform === "win32") {
    btn.style.display = "inline-flex";
    btn.textContent = "⚙ Instalar " + missing.join(", ");
  }
}).catch(() => {});
document.getElementById("setup").addEventListener("click", async () => {
  const btn = document.getElementById("setup"); btn.style.display = "none";
  term.writeln("\r\n" + C.v + "◆ instalando dependencias (winget)… puede tardar unos minutos" + C.r);
  busy = true; const res = await window.nxt.setup(missing); busy = false;
  if (res.out) term.write(res.out.replace(/\r?\n/g, "\r\n"));
  await prompt();
});

banner();
prompt();
term.focus();
