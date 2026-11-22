"use strict";
const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("nxt", {
  run: (line) => ipcRenderer.invoke("run", line),
  cwd: () => ipcRenderer.invoke("cwd"),
  checkTools: () => ipcRenderer.invoke("tools:check"),
  setup: (missing) => ipcRenderer.invoke("tools:setup", missing),
  platform: process.platform,
});
