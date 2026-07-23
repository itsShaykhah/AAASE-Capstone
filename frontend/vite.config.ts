import path from "node:path";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// Path alias (@/...) mirrors tsconfig.app.json's "paths" entry so imports
// stay short and stable if files move between folders.
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 5173,
  },
});
