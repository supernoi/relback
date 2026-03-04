# Roadmap — Sugestões de Melhoria (Relback)

Propostas de próximos passos ordenadas por impacto e esforço.

---

## Visão geral

| Área | Prioridade | Esforço | Descrição |
|------|------------|---------|-----------|
| Qualidade / testes | Alta | Médio | E2E, cobertura, testes de API |
| Observabilidade | Alta | Baixo | Health checks, métricas, logging |
| DevEx / local | Alta | Baixo | Oracle Free em container, dev com um comando |
| Segurança | Média | Médio | Rate limit, tokens API, auditoria |
| Performance | Média | Médio | Cache, paginação, N+1 |
| Documentação | Média | Baixo | OpenAPI, runbooks, troubleshooting |
| Infra | Média | Variado | Podman, CI matrix, staging |

---

## 1. Qualidade e testes

| # | Melhoria | Sensor | Esforço |
|---|----------|--------|---------|
| 1.1 | Testes E2E (Playwright/Selenium): login → Dashboard → Reports → CRUD | Pipeline E2E verde | Médio |
| 1.2 | Cobertura mínima (ex.: 80% em coreRelback/) com gate no CI | pytest-cov/coverage no CI | Baixo |
| 1.3 | Testes de API: validar payload e filtros (from_date, to_date) | Testes em api/tests.py | Baixo |
| 1.4 | Testes de integração com Oracle (opcional, skip sem env) | Tag integration-oracle | Médio |

---

## 2. Observabilidade

| # | Melhoria | Sensor | Esforço |
|---|----------|--------|---------|
| 2.1 | Endpoint /health/: HTTP 200 com status DB e catálogo Oracle | curl /health/ retorna JSON | Baixo |
| 2.2 | Métricas Prometheus (opcional) | /metrics expõe Prometheus | Médio |
| 2.3 | Logging estruturado (JSON em prod) | Logs stdout em JSON | Baixo |
| 2.4 | Alerting + runbook “RMAN catalog down” | Doc em ARCHITECTURE/runbook | Baixo |

---

## 3. Segurança

| # | Melhoria | Sensor | Esforço |
|---|----------|--------|---------|
| 3.1 | Rate limiting (API e login) | 429 após N req/min | Baixo |
| 3.2 | Tokens para API (TokenAuth/JWT) | Authorization: Token … retorna 200 | Médio |
| 3.3 | Auditoria (created_by/updated_by em CRUDs) | Registros ou log | Médio |
| 3.4 | Hardening HTTPS em prod (SECURE_*, HSTS) | Ativar com TLS | Baixo |

---

## 4. Performance

| # | Melhoria | Sensor | Esforço |
|---|----------|--------|---------|
| 4.1 | Cache para dashboard/reports (1–5 min) | Tempo de resposta reduzido | Médio |
| 4.2 | Paginação eficiente (cursor/keyset) | Queries com LIMIT e índice | Médio |
| 4.3 | Revisão N+1 (select_related/prefetch_related) | Sem aumento de queries por item | Baixo |

---

## 5. Documentação e API

| # | Melhoria | Sensor | Esforço |
|---|----------|--------|---------|
| 5.1 | OpenAPI/Swagger para API REST | /api/schema/ retorna OpenAPI 3.0 | Baixo |
| 5.2 | Runbook em docs/ | Doc Runbook em docs/ | Baixo |
| 5.3 | Troubleshooting em ARCHITECTURE | Seção erros comuns | Baixo |

---

## 6. Infra

| # | Melhoria | Sensor | Esforço |
|---|----------|--------|---------|
| 6.1 | Suporte Podman (compose + doc) | podman compose up sobe stack | Baixo |
| 6.2 | Oracle Database Free em container | Serviço oracle + doc | Médio |
| 6.3 | CI matrix (Python 3.12/3.13) | Workflow com matrix | Baixo |
| 6.4 | Ambiente de staging (opcional) | Doc ou script | Médio |

---

## Ordem sugerida

1. **Curto prazo:** Health check, OpenAPI, Podman doc, Rate limit.
2. **Médio prazo:** E2E mínimos, cobertura, Token auth, cache reports.
3. **Longo prazo:** Prometheus, runbook completo, staging.

---

*Atualizar conforme fases do ROADMAP_TAILWIND_DAISYUI e novas prioridades.*
