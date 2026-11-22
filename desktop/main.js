"use strict";
const { app, BrowserWindow, ipcMain } = require("electron");
const path = require("path");
const os = require("os");
const fs = require("fs");
const cp = require("child_process");

const isWin = process.platform === "win32";
const SHELL = isWin ? "powershell.exe" : "/bin/bash";

let win = null;
let cwd = os.homedir();

function createWindow() {
  win = new BrowserWindow({
    width: 1040, height: 700, minWidth: 560, minHeight: 360,
    backgroundColor: "#050308",
    title: "NXT27 · Neural eXecution Terminal",
    autoHideMenuBar: true,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });
  win.loadFile(path.join(__dirname, "renderer", "index.html"));
}

ipcMain.handle("cwd", () => cwd);

// Mini-shell: runs each command for real in the user's shell, keeps cwd.
ipcMain.handle("run", (_e, raw) => {
  const line = String(raw || "").trim();
  if (!line) return { out: "", cwd };
  if (/^(cls|clear)$/i.test(line)) return { clear: true, cwd };
  const m = line.match(/^cd\s+(.+)$/i);
  if (m) {
    let t = m[1].trim().replace(/^["']|["']$/g, "").replace(/^~/, os.homedir());
    const np = path.resolve(cwd, t);
    try { if (fs.statSync(np).isDirectory()) { cwd = np; return { out: "", cwd }; } return { out: "cd: no es carpeta: " + t + "\n", cwd }; }
    catch { return { out: "cd: no existe: " + t + "\n", cwd }; }
  }
  return new Promise((res) => {
    cp.exec(line, { cwd, shell: SHELL, timeout: 180000, maxBuffer: 16 * 1024 * 1024, windowsHide: true },
      (err, stdout, stderr) => {
        let out = (stdout || "") + (stderr || "");
        if (err && !out) out = String(err.message) + "\n";
        res({ out, cwd });
      });
  });
});

ipcMain.handle("tools:check", () => {
  const which = isWin ? "where " : "command -v ";
  const has = (c) => { try { cp.execSync(which + c, { stdio: "ignore" }); return true; } catch (_) { return false; } };
  return { git: has("git"), python: has(isWin ? "python" : "python3"), node: has("node"), npm: has("npm") };
});

ipcMain.handle("tools:setup", async (_e, missing) => {
  if (!isWin) return { out: "La instalacion automatica (winget) solo esta disponible en Windows.\n" };
  const ids = { git: "Git.Git", python: "Python.Python.3.12", node: "OpenJS.NodeJS" };
  let out = "";
  for (const m of (missing || [])) {
    if (!ids[m]) continue;
    out += "\n== instalando " + m + " ==\n";
    out += await new Promise((res) => {
      cp.exec(`winget install --id ${ids[m]} -e --accept-package-agreements --accept-source-agreements`,
        { timeout: 600000, maxBuffer: 16 * 1024 * 1024, windowsHide: true },
        (err, so, se) => res((so || "") + (se || "") + (err && !so ? String(err.message) + "\n" : "")));
    });
  }
  out += "\n== listo · cierra y reabre la terminal para usar los nuevos comandos ==\n";
  return { out };
});

app.whenReady().then(createWindow);
app.on("activate", () => { if (BrowserWindow.getAllWindows().length === 0) createWindow(); });
app.on("window-all-closed", () => app.quit());
