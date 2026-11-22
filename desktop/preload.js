"use strict";
const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("nxt", {
  onData: (cb) => ipcRenderer.on("pty:data", (_e, d) => cb(d)),
  input: (d) => ipcRenderer.send("pty:input", d),
  resize: (cols, rows) => ipcRenderer.send("pty:resize", { cols, rows }),
  checkTools: () => ipcRenderer.invoke("tools:check"),
  setup: (missing) => ipcRenderer.send("tools:setup", missing),
  platform: process.platform,
});
