import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { resolve } from "path";
import { fileURLToPath } from "url";

const __dirname = fileURLToPath(new URL(".", import.meta.url));

export default defineConfig(({}) => {
  return {
    plugins: [react()],
    server: {
      port: 4000,
      host: "0.0.0.0",
      watch: {
        usePolling: true,
      },
    },
    // build: {
    //   lib: {
    //     entry: resolve(__dirname, "src/widget-entry.jsx"),
    //     name: "ChatWidget",
    //     fileName: "chat-widget",
    //     formats: ["umd"],
    //   },
    //   rollupOptions: {
    //     external: ["react", "react-dom"],
    //     output: {
    //       globals: {
    //         react: "React",
    //         "react-dom": "ReactDOM",
    //       },
    //     },
    //   },
    //   outDir: "dist",
    //   emptyOutDir: true,
    // },
  };
});
