import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          dark: "#0F172A",
        },
        accent: {
          DEFAULT: "#2563EB",
          light: "#DBEAFE",
        },
        surface: "#F8FAFC",
        card: "#FFFFFF",
        "text-primary": "#0F172A",
        "text-secondary": "#64748B",
        border: "#E2E8F0",
        success: "#22C55E",
        danger: "#EF4444",
      },
    },
  },
  plugins: [],
};

export default config;
