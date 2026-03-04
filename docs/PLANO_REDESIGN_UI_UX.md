# Plano de Redesign UI/UX — Relback

> **Status: IMPLEMENTADO** — todas as 4 fases concluídas. 84 testes passando. Zero classes legado restantes.

Análise da interface atual e plano para uma interface **limpa, corporativa e confiável**, com técnicas modernas de UI/UX.

---

## 1. Análise do estado atual

### 1.1 Problemas identificados

| Problema | Causa atual | Impacto |
|----------|-------------|---------|
| **Paleta Oracle (vermelho #C74634)** | Tema `relback_light` e CSS legado com Oracle Red como primary | Transmite “marca Oracle” em vez de “confiança/operação”; cansa em uso prolongado (NOC). |
| **Gradientes pesados** | `oracle-modern-theme.css`: múltiplos gradientes (slate, ocean, accent) em headers, cards, navbar | Poluição visual; difícil hierarquia; aspecto “datar” em vez de clean. |
| **Mistura de sistemas** | Tailwind/DaisyUI + CSS custom (md-card, oracle-info-gradient, etc.) | Inconsistência; conflitos de especificidade; manutenção difícil. |
| **Excesso de cor** | Muitos tokens (pine, teal, ocean, sky, sienna) em um só tema | Interface barulhenta; usuário não sabe onde olhar. |
| **Falta de hierarquia clara** | Títulos, cards e ações com peso visual similar | Pouca orientação; não fica óbvio o fluxo principal (ex.: Reports vs CRUD). |

### 1.2 O que manter

- **DaisyUI + Tailwind** como base (componentes, grid, utilitários).
- **Material Icons** (ou migração futura para ícones mais neutros).
- **Drawer responsivo** (sidebar em lg, overlay em mobile).
- **Tokens de status de backup** (success, warning, error, info) — apenas refinar contraste e saturação.

---

## 2. Princípios do redesign

### 2.1 Clean / Corporativo

- **Menos é mais:** uma cor primária, neutros para fundo e texto, um acento para ações críticas.
- **Espaço em branco:** padding e margin generosos; cards e seções bem separados.
- **Tipografia clara:** uma família sans-serif (ex.: Inter ou system-ui), pesos bem definidos (regular, medium, semibold) e escala consistente (ex.: 0.875 → 1 → 1.125 → 1.25 → 1.5 rem).
- **Bordas e sombras sutis:** bordas 1px neutras; sombras leves para elevação (ex.: 0 1px 3px rgba(0,0,0,0.08)).

### 2.2 Confiança (Trust)

- **Azul como primário:** azul está associado a confiança, estabilidade e tecnologia (ex.: #2563eb, #1d4ed8 ou tons slate-blue).
- **Evitar vermelho como cor principal:** reservar para erros e alertas críticos.
- **Neutros estáveis:** cinzas frios (slate) em vez de amarelados; fundos #f8fafc (light) e #0f172a / #1e293b (dark).
- **Contraste acessível:** WCAG AA (≥4.5:1 para texto normal); status e badges sempre legíveis.

### 2.3 Intuitividade

- **Hierarquia visual clara:** título da página > seções > cards > conteúdo; CTAs principais em destaque (primary), secundários em outline ou ghost.
- **Padrões reconhecíveis:** listas em tabela ou card list; formulários com labels acima ou floating; confirmações destrutivas em modal com botão danger.
- **Feedback imediato:** loading states, toasts ou alerts após ações; estados hover/focus visíveis.
- **Navegação previsível:** sidebar com itens estáveis; breadcrumb quando fizer sentido; mesma estrutura em todas as telas.

### 2.4 Técnicas modernas recomendadas

- **Design system mínimo:** tokens de cor, espaçamento (4/8px grid) e tipografia em um único lugar (Tailwind + DaisyUI theme).
- **Modo escuro opcional:** paleta paralela com mesma estrutura (primary, base-100, base-content) para NOC/operações.
- **Componentes reutilizáveis:** botões, inputs, cards e tabelas só com classes Tailwind/DaisyUI; eliminar CSS custom por componente.
- **Mobile-first e touch-friendly:** alvos ≥44px; drawer em mobile; tabelas scroll horizontal ou cards em small.
- **Acessibilidade:** foco visível, aria-labels onde necessário, contraste verificado.

---

## 3. Proposta de paleta (confiança + corporativo)

### 3.1 Tema claro (default sugerido)

| Token | Uso | Cor proposta | Hex |
|-------|-----|--------------|-----|
| **primary** | Links, botões principais, ícone brand | Azul confiável | #2563eb (blue-600) |
| **primary-content** | Texto sobre primary | Branco | #ffffff |
| **secondary** | Botões secundários, labels | Slate médio | #475569 |
| **base-100** | Fundo da página | Cinza muito claro | #f8fafc |
| **base-200** | Fundo de cards/sidebar | #f1f5f9 |
| **base-300** | Bordas, divisores | #e2e8f0 |
| **base-content** | Texto principal | #0f172a |
| **accent** | Links hover, badges “info” | Azul mais claro | #3b82f6 |
| **success / warning / error** | Status de backup | Verde/âmbar/vermelho suaves, WCAG AA | #16a34a, #d97706, #dc2626 |

### 3.2 Tema escuro (NOC / 24x7)

| Token | Uso | Cor proposta | Hex |
|-------|-----|--------------|-----|
| **primary** | Ações principais | Azul claro | #60a5fa (blue-400) |
| **base-100** | Fundo | Slate escuro | #0f172a |
| **base-200** | Cards, sidebar | #1e293b |
| **base-300** | Bordas | #334155 |
| **base-content** | Texto | #e2e8f0 |
| **success / info / warning / error** | Status | Tons que mantêm ≥4.5:1 sobre base-100 | (manter ou ajustar levemente) |

### 3.3 Remoção progressiva

- **Oracle Red como primary:** remover do tema claro; usar apenas em alertas ou remover.
- **Gradientes em headers/cards:** substituir por fundo sólido (base-200) + borda ou sombra leve.
- **oracle-modern-theme.css:** migrar o estritamente necessário (ex.: Material Icons) para Tailwind/theme; deprecar classes .md-card, .oracle-*-gradient, etc.

---

## 4. Plano de implementação

### Fase 1 — Design system (tema e tokens)

1. **Atualizar `theme/static_src/tailwind.config.js`:**
   - Novo tema `relback_clean_light`: primary azul (#2563eb), neutros slate, sem Oracle Red.
   - Ajustar `relback_dark` para mesma lógica (primary azul claro, bases slate).
   - Manter tokens de status de backup (success, warning, error, info) com contraste verificado.
2. **Definir `defaultTheme`** como `relback_clean_light` (ou renomear `relback_light` para essa paleta).
3. **Documentar** tokens em `docs/` (uma página “Design tokens”).

**Sensor:** Página inicial e Reports renderizam com nova paleta; sem gradientes em cards/header.

---

### Fase 2 — Limpeza de CSS legado

1. **Inventariar** uso de classes em `coreRelback/templates/`: `md-card`, `oracle-*-gradient`, `table-header-content`, etc.
2. **Substituir** por componentes DaisyUI/Tailwind:
   - Cards: `card card-bordered bg-base-200 shadow-sm`
   - Headers de tabela: `bg-base-300 text-base-content font-medium`
   - Botões: `btn btn-primary`, `btn btn-ghost`, etc.
3. **Remover ou encerrar** blocos em `oracle-modern-theme.css` que não forem mais usados (ou mover para um arquivo “legacy” e não carregar por padrão).

**Sensor:** Nenhuma classe `oracle-*-gradient` ou `md-card` em uso; testes visuais e de acessibilidade (contraste) passando.

---

### Fase 3 — Componentes e layout

1. **Sidebar e navbar:** fundo sólido (base-200), texto base-content; ícone/brand com primary.
2. **Tabelas:** cabeçalho discreto (base-300), linhas zebra opcional (base-200/base-100), bordas sutis.
3. **Formulários:** labels acima ou floating; inputs com `input input-bordered w-full`; agrupamento em `form-control`.
4. **Modais:** header com título e botão fechar; footer com ações alinhadas à direita (Cancel outline, Confirm primary).
5. **Empty states e alerts:** ícone + texto + CTA; cores apenas para success/warning/error.

**Sensor:** Todas as telas (Dashboard, Clients, Hosts, DBs, Policies, Reports) seguem o mesmo padrão visual; breadcrumb e navegação consistentes.

---

### Fase 4 — Refino e acessibilidade

1. **Revisar contraste** (WCAG AA) em todos os textos e botões (Ferramentas: axe DevTools, Contrast Checker).
2. **Focus visible:** `focus:ring-2 focus:ring-primary focus:ring-offset-2` em interativos.
3. **Reduzir movimento** (opcional): `prefers-reduced-motion` para animações mínimas.
4. **Documentar** padrões de uso (quando usar primary vs secondary, quando usar badge vs alert) em `docs/`.

**Sensor:** Zero violações críticas em auditoria de acessibilidade; documentação de componentes atualizada.

---

## 5. Resumo executivo

| Objetivo | Ação principal |
|----------|----------------|
| **Limpo** | Um sistema de cores (tokens), sem gradientes desnecessários, componentes DaisyUI/Tailwind only. |
| **Corporativo** | Azul como primary, neutros slate, tipografia e espaçamento consistentes. |
| **Confiável** | Paleta que transmite estabilidade; vermelho apenas para erro; contraste WCAG AA. |
| **Intuitivo** | Hierarquia clara, padrões reconhecíveis, feedback imediato, navegação previsível. |

A implementação pode ser feita em **4 fases** (tema → remoção CSS legado → componentes/layout → acessibilidade), com sensores em cada fase para não regredir.

---

*Documento em `docs/` conforme convenção do projeto. Atualizar conforme decisões de design e implementação.*
