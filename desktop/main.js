"use strict";
const { app, BrowserWindow, ipcMain } = require("electron");
const path = require("path");
const os = require("os");
const cp = require("child_process");
const pty = require("node-pty");

const isWin = process.platform === "win32";
const SHELL = isWin ? "powershell.exe" : (process.env.SHELL || "bash");

let win = null;
let ptyProc = null;

function spawnPty() {
  ptyProc = pty.spawn(SHELL, [], {
    name: "xterm-256color",
    cols: 100,
    rows: 30,
    cwd: os.homedir(),
    env: process.env,
  });
  ptyProc.onData((d) => { if (win && !win.isDestroyed()) win.webContents.send("pty:data", d); });
  ptyProc.onExit(() => { if (win && !win.isDestroyed()) win.webContents.send("pty:data", "\r\n\x1b[90m[sesion finalizada]\x1b[0m\r\n"); });
}

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
  spawnPty();
}

ipcMain.on("pty:input", (_e, d) => { if (ptyProc) ptyProc.write(d); });
ipcMain.on("pty:resize", (_e, s) => { try { ptyProc.resize(s.cols, s.rows); } catch (_) {} });

ipcMain.handle("tools:check", () => {
  const which = isWin ? "where " : "command -v ";
  const has = (c) => { try { cp.execSync(which + c, { stdio: "ignore" }); return true; } catch (_) { return false; } };
  return {
    git: has("git"),
    python: has(isWin ? "python" : "python3"),
    node: has("node"),
    npm: has("npm"),
  };
});

// Auto-install missing tools via winget (Windows), shown live in the terminal.
ipcMain.on("tools:setup", (_e, missing) => {
  if (!ptyProc) return;
  if (!isWin) {
    ptyProc.write('echo "La instalacion automatica (winget) solo esta disponible en Windows."\r');
    return;
  }
  const ids = { git: "Git.Git", python: "Python.Python.3.12", node: "OpenJS.NodeJS" };
  ptyProc.write('Write-Host "== NXT27: instalando dependencias faltantes ==" -ForegroundColor Magenta\r');
  (missing || []).forEach((m) => {
    if (ids[m]) ptyProc.write(`winget install --id ${ids[m]} -e --accept-package-agreements --accept-source-agreements\r`);
  });
  ptyProc.write('Write-Host "== Listo. Cierra y reabre la terminal para usar los nuevos comandos. ==" -ForegroundColor Green\r');
});

app.whenReady().then(createWindow);
app.on("activate", () => { if (BrowserWindow.getAllWindows().length === 0) createWindow(); });
app.on("window-all-closed", () => { if (ptyProc) try { ptyProc.kill(); } catch (_) {} app.quit(); });
