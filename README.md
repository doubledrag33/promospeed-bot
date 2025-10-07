# Gropt (GROcery OPTimized)

Gropt è una piattaforma end-to-end per pianificare la spesa ottimizzata su più negozi.
Il monorepo contiene backend FastAPI, frontend Next.js, database PostgreSQL, test
Pytest/Playwright e infrastruttura Docker Compose pronta per ambienti di sviluppo e produzione.

## Table of Contents
- [Architettura](#architettura)
- [Prerequisiti](#prerequisiti)
- [Setup rapido](#setup-rapido)
- [Backend](#backend)
- [Frontend](#frontend)
- [Database & Seed](#database--seed)
- [Testing](#testing)
- [Qualità & CI](#qualità--ci)
- [Struttura directory](#struttura-directory)
- [FAQ](#faq)
- [Note privacy e legali](#note-privacy-e-legali)

## Architettura
- **Backend**: FastAPI + SQLAlchemy + Alembic + Pydantic. Autenticazione JWT con refresh
  token e password hashing Argon2.
- **Database**: PostgreSQL 15 con migrazioni Alembic e seed demo.
- **Frontend**: Next.js 14 (App Router) + Tailwind CSS + Zustand per lo stato condiviso +
  React Hook Form + Zod.
- **Tests**: Pytest (unit/integration) e Playwright per e2e.
- **Infra**: Docker Compose con servizi `api`, `db`, `web`, `nginx` e supporto `.env`.
- **Lint/Format**: Ruff + Black per Python, ESLint + Prettier per TypeScript.

## Prerequisiti
- Docker >= 24 e Docker Compose Plugin >= 2.
- Node.js >= 18 (solo per sviluppo frontend locale senza Docker).
- Python >= 3.11 (solo per esecuzione backend locale senza Docker).

## Setup rapido
1. Copia le variabili di ambiente e personalizza secondo necessità:
   ```bash
   cp .env.example .env
   ```
2. Avvia l'intero stack:
   ```bash
   docker compose up --build
   ```
3. In una nuova shell, esegui le migrazioni e carica i dati demo:
   ```bash
   docker compose exec api alembic upgrade head
   docker compose exec api psql postgresql://postgres:postgres@db:5432/gropt -f /app/db/seed.sql
   ```
4. L'applicazione è disponibile su <http://localhost:8080> (servita tramite NGINX).

### Accessi demo
| Ruolo | Email | Password |
|-------|-------|----------|
| Admin | admin@gropt.local | Admin123! |
| Merchant | merchant@gropt.local | Merchant123! |
| Utente | user@gropt.local | User123! |

## Backend
- Avvio locale (senza Docker):
  ```bash
  python -m venv .venv
  source .venv/bin/activate
  pip install -r backend/requirements.txt
  uvicorn backend.app.main:app --reload
  ```
- Configurazione via variabili d'ambiente: vedere `.env.example` per i dettagli.
- Endpoints principali disponibili su `/docs` (Swagger UI) e `/redoc`.

## Frontend
- Avvio locale (senza Docker):
  ```bash
  cd frontend
  pnpm install
  pnpm dev
  ```
- App Router con PWA (manifest e service worker) e Tailwind configurato.

## Database & Seed
- Migrazioni con Alembic nella cartella `backend/alembic`.
- Seed demo in `db/seed.sql` con 5 negozi di Ravenna, ~250 prodotti e prezzi/offerte.

## Testing
- Pytest (backend): `docker compose exec api pytest`
- Playwright (frontend): `docker compose exec web pnpm test:e2e`
- Coverage minimo backend: 70% (verificato con `pytest --cov`).

## Qualità & CI
- Lint Python: `docker compose exec api ruff check .`
- Format Python: `docker compose exec api black .`
- Lint frontend: `docker compose exec web pnpm lint`
- Prettier check: `docker compose exec web pnpm format:check`
- Workflow GitHub Actions (`.github/workflows/ci.yml`) esegue lint, test e build Docker.

## Struttura directory
```
gropt/
  backend/
  db/
  frontend/
  infra/
  tests/
```
Dettagli nel file tree reale.

## FAQ
**È possibile usare un provider OSRM esterno?**
Sì, impostare `OSRM_BASE_URL` per usare un endpoint personalizzato; in assenza viene
utilizzato un calcolo Haversine.

**Come funziona il rate limiting?**
Un semplice limitatore in-memory (Starlette `LimiterMiddleware`) limita registrazioni/login
per IP a 5 richieste/minuto.

## Note privacy e legali
- Il consenso esplicito per geolocalizzazione e caricamento scontrini è richiesto durante
  l'onboarding; i dati sono salvati come flag booleani.
- Le immagini scontrini vengono pseudonimizzate e salvate su storage configurabile; nella
  demo restano placeholder.
- Disclosure prezzi: "I prezzi online possono differire dai prezzi in negozio; mostriamo
  fonte e data rilevazione." visibile nel footer frontend.
- Il README contiene indicazioni per DPIA futura.

