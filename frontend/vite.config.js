import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0",
    port: 5173,
    // Running Vite in Docker with the source bind-mounted from the host: poll
    // for changes so file events aren't missed across the mount boundary.
    watch: { usePolling: true, interval: 200 },
  },
});
