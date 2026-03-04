# Design Tokens — Relback

Referência dos tokens de design usados na interface (Tailwind + DaisyUI). Consulte também `theme/static_src/tailwind.config.js`.

---

## 1. Temas

| Tema | Uso | Primary | Base-100 | Base-content |
|------|-----|---------|----------|--------------|
| **relback_light** | Default, uso geral | #2563eb (blue-600) | #ffffff | #0f172a |
| **relback_dark** | NOC / operações 24x7 | #60a5fa (blue-400) | #0f172a | #e2e8f0 |

- **defaultTheme:** `relback_light`
- Troca via botão no navbar ou `localStorage['relback-theme']`.

---

## 2. Tokens de cor (DaisyUI)

### 2.1 Semânticos principais

| Token | Light (hex) | Dark (hex) | Uso |
|-------|-------------|------------|-----|
| primary | #2563eb | #60a5fa | Links, botões principais, ícone da marca, CTAs |
| primary-content | #ffffff | #0f172a | Texto sobre fundo primary |
| secondary | #475569 | #94a3b8 | Botões secundários, labels discretos |
| accent | #3b82f6 | #38bdf8 | Hover em links, badges “info” |
| base-100 / base-200 / base-300 | (ver config) | — | Fundos de página, cards, bordas/divisores |
| base-content | #0f172a | #e2e8f0 | Texto principal |

### 2.2 Status (backup e feedback)

| Token | Light | Dark | Uso |
|-------|--------|------|-----|
| success | #16a34a | #4ade80 | Backup OK, confirmações |
| info | #2563eb | #93c5fd | Em execução, informação neutra |
| warning | #d97706 | #fbbf24 | Atenção, RUNNING_W_ISSUES |
| error | #dc2626 | #f87171 | Falha, erros, ações destrutivas |
| neutral | — | — | Estado desconhecido, placeholder |

Tons de dark foram escolhidos para **contraste ≥4.5:1** sobre `base-100` (WCAG AA).

### 2.3 Tokens de backup (utilitários)

Em `tailwind.config.js` → `theme.extend.colors.backup`:

- `backup.completed`, `backup.running`, `backup.failed`, `backup.warning`, `backup.interrupted`, `backup.unknown`

Uso: quando precisar da cor fora do componente badge (ex.: ícone ou borda). Preferir classes DaisyUI `badge-success`, `badge-error`, etc.

---

## 3. Tipografia

- **Sans:** Inter (Google Fonts), fallback system-ui.
- **Mono:** JetBrains Mono (código, logs).
- Escala: usar classes Tailwind (`text-sm`, `text-base`, `text-lg`, `text-xl`, etc.). Título de página: `page-title` ou `text-xl font-bold`.

---

## 4. Espaçamento e superfícies

- **Cards:** `card-section` ou `bg-base-200 border border-base-300 rounded-xl shadow-sm`.
- **Sombras:** `shadow-sm` padrão; `shadow-lg` para modais/dropdowns.
- **Border radius:** `rounded-lg` (0.5rem), `rounded-xl` (0.75rem). Tokens `rounded-card` no config.

---

## 5. Padrões de uso (quando usar o quê)

### 5.1 Primary vs secondary

| Situação | Usar |
|----------|------|
| Ação principal da tela (ex.: “Salvar”, “Adicionar cliente”) | `btn btn-primary` |
| Ação secundária (ex.: “Cancelar”, “Voltar”) | `btn btn-ghost` ou `btn btn-outline` |
| Link de destaque (ex.: “Sign up”) | `link link-primary` |
| Texto ou rótulo que não é CTA | `text-base-content` ou `text-base-content/70`; evitar primary |
| Ícone da marca / logo | `text-primary` ou ícone em container `bg-primary` |

**Regra:** Primary = uma ação principal por contexto. O resto em outline/ghost ou neutro.

### 5.2 Badge vs alert

| Componente | Quando usar | Exemplo |
|------------|-------------|---------|
| **Badge** (`badge badge-success`, etc.) | Status **inline** (tabela, card, linha de texto) | Status do backup: “Completed”, “Failed” |
| **Alert** (`alert alert-warning`, etc.) | Mensagem **em bloco** para o usuário (erro, aviso, sucesso após ação) | “Credenciais inválidas”, “Backup concluído com sucesso” |

- Badge: informação de estado, pouco texto.
- Alert: feedback de ação ou aviso que exige atenção; pode ter título + corpo + ação.

### 5.3 Botões destrutivos

- Ex.: “Excluir”, “Remover”. Usar `btn btn-error` e, em modais, combinar com `btn btn-ghost` ou `btn btn-outline` para “Cancelar”.

---

## 6. Acessibilidade

- **Contraste:** Tokens de texto e status foram definidos para WCAG AA (≥4.5:1) sobre o fundo correspondente. Tema escuro validado sobre `base-100` #0f172a.
- **Foco:** Focus visível global em `theme/static_src/src/styles.css` (`*:focus-visible` com outline primary).
- **Movimento:** Animação e scroll suave respeitam `prefers-reduced-motion: reduce` (ver estilos globais).

Para auditoria formal, usar axe DevTools ou Contrast Checker nos fluxos críticos.

---

*Documento em `docs/` conforme convenção do projeto. Fonte dos valores: `theme/static_src/tailwind.config.js`.*
