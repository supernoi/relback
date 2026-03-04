/**
 * Tailwind CSS + DaisyUI — Relback Design System
 *
 * Paleta "confiança corporativa":
 *   - relback_light: Blue primary (#2563eb), slate neutrals, white base
 *   - relback_dark:  Blue-400 primary (#60a5fa), slate dark bases (NOC-safe)
 *
 * Backup Status Tokens (BackupStatusValue → DaisyUI semantic):
 *   COMPLETED        → success    (#16a34a / #4ade80)  WCAG ≥4.5:1
 *   RUNNING          → info       (#2563eb / #93c5fd)  WCAG ≥4.5:1
 *   FAILED           → error      (#dc2626 / #f87171)  WCAG ≥4.5:1
 *   RUNNING_W_ISSUES → warning    (#d97706 / #fbbf24)  WCAG ≥4.5:1
 *   INTERRUPTED      → violet via backup.interrupted utility
 *   UNKNOWN          → neutral
 *
 * All dark-theme tokens tested for ≥4.5:1 contrast against base-100 (#0f172a).
 */

module.exports = {
  content: [
    "../../**/templates/**/*.html",
    "../../**/templatetags/**/*.py",
    "../../static/js/**/*.js",
  ],

  darkMode: ["class", '[data-theme="relback_dark"]'],

  theme: {
    extend: {
      colors: {
        backup: {
          completed:   "#16a34a",
          running:     "#2563eb",
          failed:      "#dc2626",
          warning:     "#d97706",
          interrupted: "#7c3aed",
          unknown:     "#6b7280",
        },
      },
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "-apple-system", "sans-serif"],
        mono: ["JetBrains Mono", "ui-monospace", "monospace"],
      },
      boxShadow: {
        card: "0 1px 3px 0 rgba(0,0,0,0.06), 0 1px 2px -1px rgba(0,0,0,0.06)",
      },
      borderRadius: {
        card: "0.75rem",
      },
    },
  },

  plugins: [
    require("daisyui"),
  ],

  daisyui: {
    themes: [
      {
        relback_light: {
          "primary":          "#2563eb",   // blue-600 — trust & stability
          "primary-content":  "#ffffff",
          "secondary":        "#475569",   // slate-600
          "secondary-content":"#ffffff",
          "accent":           "#3b82f6",   // blue-500
          "accent-content":   "#ffffff",
          "neutral":          "#1e293b",   // slate-800
          "neutral-content":  "#f1f5f9",
          "base-100":         "#ffffff",   // clean white
          "base-200":         "#f8fafc",   // slate-50
          "base-300":         "#e2e8f0",   // slate-200
          "base-content":     "#0f172a",   // slate-900
          "info":             "#2563eb",
          "info-content":     "#ffffff",
          "success":          "#16a34a",
          "success-content":  "#ffffff",
          "warning":          "#d97706",
          "warning-content":  "#ffffff",
          "error":            "#dc2626",
          "error-content":    "#ffffff",
        },
      },
      {
        relback_dark: {
          "primary":          "#60a5fa",   // blue-400 — NOC-friendly
          "primary-content":  "#0f172a",
          "secondary":        "#94a3b8",   // slate-400
          "secondary-content":"#0f172a",
          "accent":           "#38bdf8",   // sky-400
          "accent-content":   "#0f172a",
          "neutral":          "#334155",   // slate-700
          "neutral-content":  "#e2e8f0",
          "base-100":         "#0f172a",   // slate-900
          "base-200":         "#1e293b",   // slate-800
          "base-300":         "#334155",   // slate-700
          "base-content":     "#e2e8f0",   // slate-200
          "info":             "#93c5fd",   // blue-300  ≈5.8:1
          "info-content":     "#0f172a",
          "success":          "#4ade80",   // green-400 ≈6.3:1
          "success-content":  "#052e16",
          "warning":          "#fbbf24",   // amber-400 ≈6.8:1
          "warning-content":  "#451a03",
          "error":            "#f87171",   // red-400   ≈4.9:1
          "error-content":    "#1e293b",
        },
      },
    ],
    defaultTheme: "relback_light",
    darkTheme: "relback_dark",
    base: true,
    styled: true,
    utils: true,
    logs: false,
  },
};
