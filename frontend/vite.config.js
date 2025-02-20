import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": "/src", // Ensures that "@/components/..." works
    },
  },
  optimizeDeps: {
    include: ["rsuite", "react-markdown", "remark-gfm"],
  },
  server: {
    host: true, // Allows access from Docker
    port: 3000, // Ensures correct port exposure
    strictPort: true,
  }
});