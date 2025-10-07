# Gropt QA Checklist

Questo documento descrive i controlli manuali e automatici consigliati prima di rilasciare una build di Gropt.
Spuntare ogni voce garantisce che le funzionalità principali richieste siano integre.

## 1. Preparazione ambiente
- [ ] Copia delle variabili: `cp .env.example .env` e personalizzazione dei secret.
- [ ] Stack avviato con `docker compose up --build`.
- [ ] Migrazioni applicate: `docker compose exec api alembic upgrade head`.
- [ ] Seed demo caricato: `docker compose exec api psql postgresql://postgres:postgres@db:5432/gropt -f /app/db/seed.sql`.
- [ ] Utenti demo funzionanti (login via frontend e `/api/auth/login`).

## 2. Test automatici
- [ ] Pytest backend: `docker compose exec api pytest`.
- [ ] Coverage backend ≥ 70% (`pytest --cov`).
- [ ] Lint Python: `docker compose exec api ruff check .`.
- [ ] Black diff pulito: `docker compose exec api black --check .`.
- [ ] Lint frontend: `docker compose exec web pnpm lint`.
- [ ] Prettier check: `docker compose exec web pnpm format:check`.
- [ ] Playwright smoke: `docker compose exec web pnpm test:e2e`.

## 3. Funzionalità core utente
- [ ] Registrazione, verifica CAP e login tramite web app.
- [ ] Ricerca prodotto da home e aggiunta al carrello.
- [ ] Gestione carrello: modifica quantità, rimozione item, preferiti (singolo + "Aggiungi tutti").
- [ ] Confronto prezzi mostra fonte (volantino/online/scontrino) e timestamp aggiornamento.
- [ ] Ottimizzazione restituisce piani Economico, Equilibrato e Un solo negozio con totali, # negozi e km stimati.
- [ ] Toggle In negozio / Consegna attivo con Everli deeplink per store `has_everli=true`.
- [ ] Scanner barcode/QR aggiunge prodotto e mostra feedback.

## 4. Prenota & Ritira
- [ ] Attivazione P&R da carrello (solo prodotti confezionati) genera `pickup_code`.
- [ ] Merchant aggiorna stato ordine da dashboard (`/merchant`).
- [ ] Stati gestiti: `sent → preparazione → pronto → ritirato` e gestione annullato.

## 5. Area admin & pricing
- [ ] Admin accede a `/admin` e vede elenco store/prodotti.
- [ ] Upload CSV prezzi/offerte tramite `/api/admin/prices/upload` con validazione corretta.
- [ ] Grafico freschezza prezzi aggiornato.

## 6. Trasparenza & privacy
- [ ] Flag consenso geoloc e caricamento scontrini salvati nel profilo utente.
- [ ] Footer mostra disclosure prezzi.
- [ ] Immagini scontrini pseudonimizzate e inaccessibili pubblicamente.

## 7. Performance & logging
- [ ] Endpoint sensibili rispettano rate limiting (HTTP 429 oltre soglia).
- [ ] Log strutturati JSON presenti per request principali (uvicorn + structlog).
- [ ] Monitoraggio errori front/back abilitato (es. Sentry) o placeholder documentato.

## 8. Regressione rapida
- [ ] Test manuale PWA: installazione da browser desktop e mobile.
- [ ] Responsive design verificato (desktop, tablet, mobile).
- [ ] Nessun errore console nei flussi principali.

Compilare la checklist e allegarla al report QA di release.
