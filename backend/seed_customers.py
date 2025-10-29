#!/usr/bin/env python3
"""
Seed clienti via API FastAPI.

Prerequisiti:
  pip install requests

Opzionale (per dati più realistici):
  pip install faker
Se faker non è installato, lo script genera comunque dati plausibili.

Configura le variabili in CONFIG qui sotto.
"""

import os
import random
import string
import time
from typing import Optional

import requests

# ========= CONFIG =========
BASE_URL = os.getenv("SEED_BASE_URL", "http://localhost:8000")  # es. http://localhost:8000
LOGIN_ENDPOINT = os.getenv("SEED_LOGIN_ENDPOINT", "/customers")  # se non usi login, lascia pure
LOGIN_EMAIL = os.getenv("SEED_LOGIN_EMAIL", "admin@example.com")  # se usi login con email/password
LOGIN_PASSWORD = os.getenv("SEED_LOGIN_PASSWORD", "Password!123")
EXTERNAL_BEARER = os.getenv("SEED_BEARER", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QGV4YW1wbGUxLmNvbSIsImV4cCI6MTc2MTMxMjA3OX0.8c7THuxwQpUFBcEO-I3YldEMpqCaG5V-jReo7jR7F6Q")  # se già hai un token: esporta SEED_BEARER="eyJhbGciOi..."

CUSTOMERS_ENDPOINT = "/customers"
TOTAL = int(os.getenv("SEED_TOTAL", "100"))  # Quanti clienti creare
B2B_RATIO = float(os.getenv("SEED_B2B_RATIO", "0.6"))  # 60% B2B, 40% B2C
REQUESTS_TIMEOUT = 15
# ==========================

# Prova ad usare Faker se presente
try:
    from faker import Faker
    faker = Faker("it_IT")
except Exception:
    faker = None


def rand_digits(n: int) -> str:
    return "".join(random.choice(string.digits) for _ in range(n))


def fake_company() -> str:
    if faker:
        return faker.company()
    return random.choice(
        ["Acme", "Globex", "Initech", "Umbrella", "Stark", "Wayne", "Wonka", "Cyberdyne"]
    ) + " " + random.choice(["S.r.l.", "S.p.A.", "S.a.s.", "S.c.a.r.l."])


def fake_email(name_hint: Optional[str] = None) -> str:
    if faker:
        return faker.unique.email()
    user = name_hint or "".join(random.choice(string.ascii_lowercase) for _ in range(8))
    domain = random.choice(["example.com", "mail.it", "azienda.it", "demo.org"])
    return f"{user}@{domain}"


def fake_phone() -> str:
    if faker:
        return faker.phone_number()
    return "+39 " + rand_digits(3) + " " + rand_digits(6)


def fake_address() -> str:
    if faker:
        return faker.address().replace("\n", ", ")
    return f"Via {random.choice(['Roma','Milano','Garibaldi','Dante','Manzoni'])} {random.randint(1,120)}, {random.choice(['Milano','Roma','Firenze','Bologna','Torino'])}"


def fake_vat() -> str:
    # formato semplice: prefisso IT + 11-13 cifre (non validiamo checksum)
    return "IT" + rand_digits(random.choice([11, 13]))


def fake_cf(first: str, last: str) -> str:
    # CF realistico è complesso; qui un placeholder maiuscolo di 16 char
    base = (last[:3] + first[:3]).upper().ljust(6, "X")
    rest = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    return (base + rest)[:16]


def get_token_or_none() -> Optional[str]:
    """Restituisce un Bearer token. Se SEED_BEARER è valorizzato lo usa.
    Altrimenti tenta il login a LOGIN_ENDPOINT con email/password."""
    if EXTERNAL_BEARER:
        return EXTERNAL_BEARER

    # prova login, adattando al tuo backend:
    # molti backend FastAPI usano /auth/login con JSON {email,password} oppure form.
    url = BASE_URL.rstrip("/") + LOGIN_ENDPOINT
    try:
        # 1) tentativo JSON {email,password}
        r = requests.post(
            url,
            json={"email": LOGIN_EMAIL, "password": LOGIN_PASSWORD},
            timeout=REQUESTS_TIMEOUT,
        )
        if r.ok:
            data = r.json()
            token = data.get("access_token") or data.get("token") or data.get("accessToken")
            if token:
                return token

        # 2) tentativo form OAuth2 password flow
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
        print(f"[login] warning: {e}")

    print("[login] nessun token ottenuto (userò richieste senza Authorization)")
    return None


def make_payload_b2b() -> dict:
    company = fake_company()
    email = fake_email(company.split()[0].lower())
    return {
        "kind": "B2B",
        "company_name": company,
        "vat_number": fake_vat(),
        "email": email,
        "phone": fake_phone(),
        "address": fake_address(),
        "notes": random.choice(["Cliente pilota", "Priority", "—", ""]),
    }


def make_payload_b2c() -> dict:
    if faker:
        first = faker.first_name()
        last = faker.last_name()
    else:
        first = random.choice(["Mario", "Luigi", "Anna", "Sara", "Marco", "Giulia"])
        last  = random.choice(["Rossi", "Bianchi", "Verdi", "Ferrari", "Russo", "Conti"])
    email = fake_email((first + "." + last).lower())
    return {
        "kind": "B2C",
        "first_name": first,
        "last_name": last,
        "codice_fiscale": fake_cf(first, last),
        "email": email,
        "phone": fake_phone(),
        "address": fake_address(),
        "notes": random.choice(["Lead fiera", "Newsletter", "—", ""]),
    }


def strip_empty(d: dict) -> dict:
    return {k: v for k, v in d.items() if v not in ("", None)}


def create_customer(session: requests.Session, token: Optional[str], payload: dict) -> requests.Response:
    url = BASE_URL.rstrip("/") + CUSTOMERS_ENDPOINT
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return session.post(url, json=payload, headers=headers, timeout=REQUESTS_TIMEOUT)


def main():
    print(f"Seed avviato su {BASE_URL} -> {CUSTOMERS_ENDPOINT} (tot: {TOTAL})")
    token = get_token_or_none()
    created, conflicts, errors = 0, 0, 0

    with requests.Session() as s:
        for i in range(1, TOTAL + 1):
            is_b2b = random.random() < B2B_RATIO
            payload = make_payload_b2b() if is_b2b else make_payload_b2c()
            payload = strip_empty(payload)

            try:
                resp = create_customer(s, token, payload)
            except Exception as e:
                errors += 1
                print(f"[{i}] ERRORE rete: {e}")
                time.sleep(0.1)
                continue

            if resp.status_code in (200, 201):
                created += 1
                if i % 10 == 0 or i == TOTAL:
                    print(f"[{i}] creati finora: {created} (409: {conflicts}, err: {errors})")
                continue

            if resp.status_code == 409:
                # duplicato indice unico (P.IVA / CF) -> rigenera e riprova 1 volta
                conflicts += 1
                alt = make_payload_b2b() if is_b2b else make_payload_b2c()
                alt = strip_empty(alt)
                r2 = create_customer(s, token, alt)
                if r2.status_code in (200, 201):
                    created += 1
                    print(f"[{i}] 409 risolto rigenerando.")
                else:
                    errors += 1
                    print(f"[{i}] 409 persiste: {r2.status_code} -> {r2.text[:200]}")
                continue

            errors += 1
            print(f"[{i}] FAIL {resp.status_code}: {resp.text[:200]}")

    print("==== RISULTATO ====")
    print(f"Creati:   {created}")
    print(f"Duplicati:{conflicts}")
    print(f"Errori:   {errors}")


if __name__ == "__main__":
    main()
