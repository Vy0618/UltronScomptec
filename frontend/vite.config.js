import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig(({ mode }) => ({
  plugins: [react()],
  // Caminhos relativos permitem carregar os arquivos locais no Electron.
  base: mode === "electron" ? "./" : "/",
  server: {
    port: 5173,
    strictPort: true,
    host: "0.0.0.0",
    allowedHosts: true,
    proxy: { "/api": "http://127.0.0.1:8000" },
  },
}));
