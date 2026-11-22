"use strict";
/* NXT27 desktop terminal — xterm.js frontend over a real system shell. */

const term = new window.Terminal({
  fontFamily: '"JetBrains Mono", ui-monospace, Menlo, Consolas, monospace',
  fontSize: 14,
  cursorBlink: true,
  allowProposedApi: true,
  theme: {
    background: "#050308",
    foreground: "#d9d2ea",
    cursor: "#c084fc",
    cursorAccent: "#050308",
    selectionBackground: "#3b2a55",
    black: "#1a1324", brightBlack: "#564d6e",
    red: "#f87171", brightRed: "#fca5a5",
    green: "#4ade80", brightGreen: "#86efac",
    yellow: "#e3b341", brightYellow: "#fbbf24",
    blue: "#60a5fa", brightBlue: "#93c5fd",
    magenta: "#a855f7", brightMagenta: "#c084fc",
    cyan: "#22d3ee", brightCyan: "#67e8f9",
    white: "#d9d2ea", brightWhite: "#ffffff",
  },
});

const fit = new window.FitAddon.FitAddon();
term.loadAddon(fit);
try { term.loadAddon(new window.WebLinksAddon.WebLinksAddon()); } catch (_) {}
term.open(document.getElementById("term"));

function doFit() {
  try {
    fit.fit();
    window.nxt.resize(term.cols, term.rows);
  } catch (_) {}
}
requestAnimationFrame(doFit);
window.addEventListener("resize", doFit);

// wire pty <-> terminal
window.nxt.onData((d) => term.write(d));
term.onData((d) => window.nxt.input(d));
term.focus();

// dependency check + setup button
let missing = [];
const toolsEl = document.getElementById("tools");
const setupBtn = document.getElementById("setup");

window.nxt.checkTools().then((t) => {
  const order = ["git", "python", "node", "npm"];
  toolsEl.innerHTML = order
    .map((k) => `<span class="tool ${t[k] ? "ok" : "no"}">${t[k] ? "✓" : "✕"} ${k}</span>`)
    .join(" ");
  missing = order.filter((k) => !t[k] && k !== "npm"); // npm viene con node
  if (missing.length && window.nxt.platform === "win32") {
    setupBtn.style.display = "inline-flex";
    setupBtn.textContent = "⚙ Instalar " + missing.join(", ");
    term.writeln("\x1b[95m◆ NXT27\x1b[0m — faltan: \x1b[91m" + missing.join(", ") +
      "\x1b[0m. Pulsa \x1b[95m⚙ Instalar\x1b[0m arriba para añadirlos.\r");
  }
}).catch(() => {});

setupBtn.addEventListener("click", () => {
  window.nxt.setup(missing);
  setupBtn.style.display = "none";
  term.focus();
});
