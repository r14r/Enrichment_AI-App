/// <reference types="vitest" />

import { defineConfig } from "vite";

export default defineConfig({
  test: {
    globals: true,
    setupFiles: ["./vitest.setup.ts"],
    include: ["src/test/unit/**/*.test.ts"],
    projects: [
      "<rootDir>/language-server/vitest.config.mts",
      "<rootDir>",
      "<rootDir>/webview-ui/vite.config.mts",
    ],
    testTimeout: 15_000,
    environment: "node",
    coverage: {
      enabled: true,
      provider: "v8",
      reporter: ["text", "html", "clover", "json-summary"],
      include: [
        "src/**/*.{js,jsx,ts,tsx}",
        "webview-ui/src/**/*.{js,jsx,ts,tsx}",
        "language-server/src/**/*.{js,jsx,ts,tsx}",
        "!src/**/*.test.{js,jsx,ts,tsx}",
        "!src/test/**/*.*",
      ],
      exclude: [
        "*.d.ts",
        "*.test.ts",
        "**/index.ts",
        "**/types.ts",
      ],
    },
  },
});