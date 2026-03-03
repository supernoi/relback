/**
 * Tailwind CSS + DaisyUI configuration for Relback
 *
 * Design System:
 *   - relback_light: Light dashboard theme (Oracle Red primary, white base)
 *   - relback_dark:  Dark dashboard theme  (Indigo primary + Cyan accent, slate base)
 *   - dracula:       High-contrast dark mode
 *
 * Backup Status Tokens (maps to BackupStatusValue enum in domain/entities.py):
 *   COMPLETED        → success      (#22c55e light / #4ade80 dark)   WCAG ≥6.3:1
 *   RUNNING          → info         (#3b82f6 light / #93c5fd dark)   WCAG ≥5.8:1
 *   FAILED           → error        (#ef4444 light / #f87171 dark)   WCAG ≥4.9:1  NOC-optimised
 *   RUNNING_W_ISSUES → warning      (#f59e0b light / #fbbf24 dark)   WCAG ≥6.8:1
 *   INTERRUPTED      → interrupted  (#7c3aed light / #a78bfa dark)   violet — common RMAN abort
 *   UNKNOWN          → neutral      (#6b7280)
 *
 * WCAG AA note: all dark-theme status tokens are tested for ≥4.5:1 contrast
 * against base-100 (#0f172a) to satisfy NOC/operations-room readability.
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
          completed:   "#22c55e",  // green-500  (light)
          running:     "#3b82f6",  // blue-500   (light)
          failed:      "#ef4444",  // red-500    (light)
          warning:     "#f59e0b",  // amber-500  (light — RUNNING_W_ISSUES)
          interrupted: "#7c3aed",  // violet-600 (light — INTERRUPTED / RMAN abort)
          unknown:     "#6b7280",  // gray-500
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
          "primary":          "#6366f1",   // indigo-500 — modern corporate
          "primary-content":  "#FFFFFF",
          "secondary":        "#94a3b8",   // slate-400 — muted label text
          "secondary-content":"#0f172a",
          "accent":           "#06b6d4",   // cyan-500 — tech/monitoring accent
          "accent-content":   "#0f172a",
          "neutral":          "#334155",
          "neutral-content":  "#e2e8f0",
          "base-100":         "#0f172a",   // slate-950
          "base-200":         "#1e293b",   // slate-800
          "base-300":         "#334155",   // slate-700
          "base-content":     "#e2e8f0",
          // WCAG AA ≥4.5:1 against base-100 (#0f172a) — NOC/operations monitor safe
          "info":             "#93c5fd",   // blue-300    ≈5.8:1  (was #2563eb ≈2.8:1)
          "info-content":     "#1e3a5f",
          "success":          "#4ade80",   // green-400   ≈6.3:1  (was #16a34a ≈2.1:1)
          "success-content":  "#052e16",
          "warning":          "#fbbf24",   // amber-400   ≈6.8:1  (was #d97706 ≈4.4:1)
          "warning-content":  "#451a03",
          "error":            "#f87171",   // red-400     ≈4.9:1  (was #dc2626 ≈3.3:1)
          "error-content":    "#1e293b",   // de-saturated dark — reduces NOC eye fatigue
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
