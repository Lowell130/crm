#!/usr/bin/env python3
"""
Seed fatture via API FastAPI (compatibile col tuo backend).

Prerequisiti:
  pip install requests

Opzionale (per descrizioni più realistiche):
  pip install faker

Configura le variabili in CONFIG o via env (prefisso SEED_*):

  SEED_BASE_URL           default: http://localhost:8000
  SEED_BEARER             default: "" (se presente, viene usato direttamente)
  SEED_LOGIN_ENDPOINT     default: /auth/login
  SEED_LOGIN_EMAIL        default: admin@example.com
  SEED_LOGIN_PASSWORD     default: Password!123

  SEED_TOTAL              quante fatture creare (default: 100)
  SEED_DAYS_BACK          orizzonte temporale per issue_date (default: 120)
  SEED_MAX_DUE_DAYS       max giorni dopo issue_date per la scadenza (default: 30)

  SEED_PCT_DRAFT          % fatture draft (default: 0.20 -> 20%)
  SEED_PCT_CANCELLED      % fatture cancelled (default: 0.05 -> 5%)
  (il resto diventa issued)

  SEED_PCT_PAID_ON_ISSUED % di issued pagate (default: 0.70 -> 70%)

  SEED_MIN_ITEMS          default: 1
  SEED_MAX_ITEMS          default: 4
  SEED_MIN_QTY            default: 1
  SEED_MAX_QTY            default: 8
  SEED_MIN_PRICE          default: 20
  SEED_MAX_PRICE          default: 450
  SEED_VAT_CHOICES        default: 0,10,22  (lista separata da virgole)

Note:
- Il backend calcola subtotal/vat_total/total: qui inviamo items/issue_date/due_date/status/paid/paid_at.
- paid/paid_at sono usati solo se status='issued'. Le draft/cancelled non sono pagate.
"""

import os
import random
import time
from typing import Optional, List
from datetime import date, timedelta

import requests

# ========= CONFIG =========
BASE_URL = os.getenv("SEED_BASE_URL", "http://localhost:8000")  # es. http://localhost:8000
LOGIN_ENDPOINT = os.getenv("SEED_LOGIN_ENDPOINT", "/customers")  # se non usi login, lascia pure
LOGIN_EMAIL = os.getenv("SEED_LOGIN_EMAIL", "admin@example.com")  # se usi login con email/password
LOGIN_PASSWORD = os.getenv("SEED_LOGIN_PASSWORD", "Password!123")
EXTERNAL_BEARER = os.getenv("SEED_BEARER", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsImlhdCI6MTc2MjI0NTUwNiwiZXhwIjoxNzYyMjQ5MTA2fQ.9yK95cXXcShvgyz5VfDqclxcKXMnxu8JuizuaG3-_Os").strip()

CUSTOMERS_ENDPOINT  = "/customers"
INVOICES_ENDPOINT   = "/invoices"

TOTAL               = int(os.getenv("SEED_TOTAL", "100"))
DAYS_BACK           = int(os.getenv("SEED_DAYS_BACK", "120"))
MAX_DUE_DAYS        = int(os.getenv("SEED_MAX_DUE_DAYS", "30"))

PCT_DRAFT           = float(os.getenv("SEED_PCT_DRAFT", "0.20"))
PCT_CANCELLED       = float(os.getenv("SEED_PCT_CANCELLED", "0.05"))
PCT_PAID_ON_ISSUED  = float(os.getenv("SEED_PCT_PAID_ON_ISSUED", "0.70"))

MIN_ITEMS           = int(os.getenv("SEED_MIN_ITEMS", "1"))
MAX_ITEMS           = int(os.getenv("SEED_MAX_ITEMS", "4"))
MIN_QTY             = int(os.getenv("SEED_MIN_QTY", "1"))
MAX_QTY             = int(os.getenv("SEED_MAX_QTY", "8"))
MIN_PRICE           = float(os.getenv("SEED_MIN_PRICE", "20"))
MAX_PRICE           = float(os.getenv("SEED_MAX_PRICE", "450"))
VAT_CHOICES         = [int(x) for x in os.getenv("SEED_VAT_CHOICES", "0,10,22").split(",") if x.strip()]

REQUESTS_TIMEOUT    = 20
PAGE_SIZE           = 100
# ==========================

# Prova ad usare Faker per descrizioni più carine
try:
    from faker import Faker
    faker = Faker("it_IT")
except Exception:
    faker = None

# ----------------- UTILS -----------------
def rand_issue_date() -> date:
    """Data emissione negli ultimi N giorni (incluso oggi)."""
    delta = random.randint(0, DAYS_BACK)
    return date.today() - timedelta(days=delta)

def rand_due_date(issue: date) -> date:
    """Scadenza fra 0 e MAX_DUE_DAYS dopo issue_date (può coincidere)."""
    return issue + timedelta(days=random.randint(0, MAX_DUE_DAYS))

def rand_paid_at(issue: date) -> date:
    """paid_at tra issue_date e oggi (inclusi)."""
    if issue >= date.today():
        return issue
    span = (date.today() - issue).days
    return issue + timedelta(days=random.randint(0, span))

def choose_status() -> str:
    """Sceglie draft/cancelled/issued secondo le percentuali configurate."""
    r = random.random()
    if r < PCT_DRAFT:
        return "draft"
    if r < PCT_DRAFT + PCT_CANCELLED:
        return "cancelled"
    return "issued"

def item_description() -> str:
    if faker:
        return faker.catch_phrase()
    pool = [
        "Consulenza", "Sviluppo feature", "Assistenza", "Installazione",
        "Analisi tecnica", "Integrazione", "Supporto remoto", "Formazione"
    ]
    return random.choice(pool)

def make_items() -> List[dict]:
    n = random.randint(MIN_ITEMS, MAX_ITEMS)
    items = []
    for _ in range(n):
        qty  = random.randint(MIN_QTY, MAX_QTY)
        unit = round(random.uniform(MIN_PRICE, MAX_PRICE), 2)
        vat  = random.choice(VAT_CHOICES) if VAT_CHOICES else 22
        items.append({
            "description": item_description(),
            "quantity": qty,
            "unit_price": unit,
            "vat_rate": vat
        })
    return items

def make_notes() -> Optional[str]:
    if random.random() < 0.35:
        if faker:
            return faker.sentence(nb_words=8)
        return random.choice([
            "Pagamento a 30 gg. f.m.",
            "Grazie per la collaborazione.",
            "Rif. ordine interno #A-192",
            "—"
        ])
    return None

def auth_headers(token: Optional[str]) -> dict:
    h = {"Accept": "application/json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h

# ----------------- API HELPERS -----------------
def get_token_or_none() -> Optional[str]:
    """Se c'è SEED_BEARER lo usa; altrimenti tenta il login al tuo /auth/login."""
    if EXTERNAL_BEARER:
        return EXTERNAL_BEARER

    url = BASE_URL.rstrip("/") + LOGIN_ENDPOINT
    try:
        r = requests.post(url, json={"email": LOGIN_EMAIL, "password": LOGIN_PASSWORD}, timeout=REQUESTS_TIMEOUT)
        if r.ok:
            data = r.json()
            token = data.get("access_token") or data.get("token") or data.get("accessToken")
            if token:
                return token
    except Exception as e:
        print(f"[login] warning (json): {e}")

    # eventuale fallback form-encoded
    try:
        r = requests.post(
            url,
            data={"username": LOGIN_EMAIL, "password": LOGIN_PASSWORD},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=REQUESTS_TIMEOUT,
        )
        if r.ok:
            data = r.json()
            token = data.get("access_token") or data.get("token") or data.get("accessToken")
            if token:
                return token
    except Exception as e:
        print(f"[login] warning (form): {e}")

    print("[login] nessun token ottenuto (procedo comunque: il tuo backend permette GET /customers?)")
    return None

def fetch_all_customers(session: requests.Session, token: Optional[str]) -> List[dict]:
    """Scarica tutti i clienti (pagina per pagina) e restituisce dict con id/kind/snapshot utile."""
    url = BASE_URL.rstrip("/") + CUSTOMERS_ENDPOINT
    out = []
    skip = 0

    while True:
        try:
            r = session.get(
                url,
                params={"skip": skip, "limit": PAGE_SIZE},
                headers=auth_headers(token),
                timeout=REQUESTS_TIMEOUT
            )
        except Exception as e:
            print(f"[customers] errore rete: {e}")
            break

        if not r.ok:
            print(f"[customers] FAIL {r.status_code}: {r.text[:200]}")
            break

        batch = r.json() or []
        if not batch:
            break

        # normalizza id
        for c in batch:
            cid = c.get("_id") or c.get("id") or c.get("_id_str")
            if cid:
                c["_id"] = cid
                out.append(c)

        if len(batch) < PAGE_SIZE:
            break

        skip += PAGE_SIZE

    return out

def post_invoice(session: requests.Session, token: Optional[str], payload: dict) -> requests.Response:
    url = BASE_URL.rstrip("/") + INVOICES_ENDPOINT
    return session.post(url, json=payload, headers=auth_headers(token), timeout=REQUESTS_TIMEOUT)

# ----------------- MAIN SEED -----------------
def build_invoice_payload(customer: dict) -> dict:
    """
    Costruisce un payload coerente con il tuo models.InvoiceCreate:
      - customer_id (stringa)
      - issue_date / due_date (YYYY-MM-DD)
      - items (almeno 1)
      - status in {draft, issued, cancelled}
      - paid/paid_at solo per issued (secondo PCT_PAID_ON_ISSUED)
      - number NON inviato (così il backend lo genera se serve)
    """
    cid = customer.get("_id")
    if not cid:
        raise ValueError("customer senza _id valido")

    issue = rand_issue_date()
    due   = rand_due_date(issue)
    status = choose_status()
    items  = make_items()
    notes  = make_notes()

    payload = {
        "customer_id": cid,
        "issue_date": issue.isoformat(),
        "due_date": due.isoformat(),
        "notes": notes,
        "items": items,
        "status": status,
    }

    if status == "issued":
        is_paid = random.random() < PCT_PAID_ON_ISSUED
        payload["paid"] = bool(is_paid)
        payload["paid_at"] = rand_paid_at(issue).isoformat() if is_paid else None
    else:
        payload["paid"] = False
        payload["paid_at"] = None

    return payload

def main():
    print(f"Seed fatture su {BASE_URL} -> {INVOICES_ENDPOINT} (tot: {TOTAL})")
    token = get_token_or_none()

    with requests.Session() as s:
        customers = fetch_all_customers(s, token)
        if not customers:
            print("Nessun cliente trovato: crea prima dei clienti e riprova.")
            return

        print(f"Trovati {len(customers)} clienti. Inizio creazione fatture…")

        created, errors = 0, 0
        for i in range(1, TOTAL + 1):
            cust = random.choice(customers)
            payload = build_invoice_payload(cust)

            try:
                resp = post_invoice(s, token, payload)
            except Exception as e:
                errors += 1
                print(f"[{i}] ERRORE rete: {e}")
                time.sleep(0.1)
                continue

            if resp.status_code in (200, 201):
                created += 1
                if i % 10 == 0 or i == TOTAL:
                    print(f"[{i}] creati finora: {created} (err: {errors})")
                continue

            errors += 1
            snippet = resp.text[:300].replace("\n", " ")
            print(f"[{i}] FAIL {resp.status_code}: {snippet}")

    print("==== RISULTATO ====")
    print(f"Creati: {created}")
    print(f"Errori: {errors}")

if __name__ == "__main__":
    main()
