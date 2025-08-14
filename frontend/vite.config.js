import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig(({ mode }) => {
  // load env for both import.meta.env (client) and process.env (config-time)
  const env = loadEnv(mode, process.cwd(), "");
  const proxyTarget = env.VITE_DEV_PROXY_TARGET || "";

  return {
    base: '/Emergent-Labs-VA/',
    plugins: [react()],
    envPrefix: ["VITE_", "REACT_APP_"],
    server: {
      host: true,
      port: 3000,
      allowedHosts: ["call-manager-3.preview.emergentagent.com"],
      proxy: proxyTarget
        ? {
            "/api/": {
              target: proxyTarget,
              changeOrigin: true,
              // keep path movis to preserve ingress-style prefix
              rewrite: (path) => path,
            },
          }
        : undefined,
    },
    preview: {
      host: true,
      port: 3000,
    },
  };
});
