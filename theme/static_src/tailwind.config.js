/**
 * Tailwind CSS + DaisyUI configuration for Relback
 *
 * Design System:
 *   - relback_light: Light dashboard theme (Oracle Red primary, white base)
 *   - relback_dark:  Dark dashboard theme  (Oracle Red primary, slate base)
 *   - dracula:       High-contrast dark mode
 *
 * Backup Status Tokens (maps to BackupStatusValue enum in domain/entities.py):
 *   COMPLETED        → success  (#22c55e)
 *   RUNNING          → info     (#3b82f6)
 *   FAILED           → error    (#ef4444)
 *   RUNNING_W_ISSUES → warning  (#f59e0b)
 *   UNKNOWN          → neutral  (#6b7280)
 */
const plugin = require("tailwindcss/plugin");

module.exports = {
  content: [
    // Django templates — all apps
    "../../**/templates/**/*.html",
    "../../**/templatetags/**/*.py",
    // Static JS that might reference Tailwind classes
    "../../static/js/**/*.js",
  ],

  // Dark mode driven by DaisyUI data-theme; keep 'class' for manual overrides
  darkMode: ["class", '[data-theme="relback_dark"]'],

  theme: {
    extend: {
      // Oracle brand colors available as tw utilities (e.g. text-oracle-red)
      colors: {
        oracle: {
          red:   "#C74634",
          blue:  "#0052CC",
          navy:  "#1A1A2E",
          gray:  "#6B7280",
        },
        backup: {
          completed: "#22c55e",  // green-500
          running:   "#3b82f6",  // blue-500
          failed:    "#ef4444",  // red-500
          warning:   "#f59e0b",  // amber-500
          unknown:   "#6b7280",  // gray-500
        },
      },
      fontFamily: {
        sans: ["Roboto", "ui-sans-serif", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "ui-monospace", "monospace"],
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
          "primary":          "#C74634",   // Oracle Red
          "primary-content":  "#FFFFFF",
          "secondary":        "#1A1A2E",   // Deep Navy
          "secondary-content":"#FFFFFF",
          "accent":           "#0052CC",   // Oracle Blue
          "accent-content":   "#FFFFFF",
          "neutral":          "#1e293b",
          "neutral-content":  "#e2e8f0",
          "base-100":         "#f8fafc",
          "base-200":         "#f1f5f9",
          "base-300":         "#e2e8f0",
          "base-content":     "#1e293b",
          "info":             "#3b82f6",
          "info-content":     "#FFFFFF",
          "success":          "#22c55e",
          "success-content":  "#FFFFFF",
          "warning":          "#f59e0b",
          "warning-content":  "#1e293b",
          "error":            "#ef4444",
          "error-content":    "#FFFFFF",
        },
        relback_dark: {
          "primary":          "#C74634",   // Oracle Red
          "primary-content":  "#FFFFFF",
          "secondary":        "#e2e8f0",
          "secondary-content":"#1e293b",
          "accent":           "#60a5fa",   // blue-400
          "accent-content":   "#0f172a",
          "neutral":          "#334155",
          "neutral-content":  "#e2e8f0",
          "base-100":         "#0f172a",   // slate-950
          "base-200":         "#1e293b",   // slate-800
          "base-300":         "#334155",   // slate-700
          "base-content":     "#e2e8f0",
          "info":             "#2563eb",
          "info-content":     "#FFFFFF",
          "success":          "#16a34a",
          "success-content":  "#FFFFFF",
          "warning":          "#d97706",
          "warning-content":  "#FFFFFF",
          "error":            "#dc2626",
          "error-content":    "#FFFFFF",
        },
      },
      "dracula",
    ],
    defaultTheme: "relback_dark",
    darkTheme: "relback_dark",
    base: true,
    styled: true,
    utils: true,
    logs: false,
  },
};
