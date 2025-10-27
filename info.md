
---

## Inizio nuovo progetto, guidami nella creazione passo passo

### Obiettivo generale

Voglio creare un **CRM (Customer Relationship Management)** per gestire in modo centralizzato tutti i miei clienti, sia **B2C (Business to Consumer)** che **B2B (Business to Business)**.
Il sistema dovrà permettere di **gestire anagrafiche**, **monitorare attività**, **inviare comunicazioni personalizzate**, **visualizzare statistiche** e **automatizzare alcune operazioni di marketing**.

### Funzionalità principali

#### Gestione anagrafiche clienti

* Creazione, modifica ed eliminazione dei clienti.
* Possibilità di **cambiare tipologia cliente** (da B2C a B2B e viceversa).
* Campi principali:

  * Nome / Ragione sociale
  * Email / Telefono
  * Indirizzo
  * Tipo cliente (B2C / B2B)
  * Partita IVA o Codice fiscale (opzionale)
  * Data di registrazione
  * Note interne / tag personalizzati
* Possibilità di allegare file o documenti (es. contratti, preventivi, ecc.)

#### Comunicazioni integrate

* Invio di **email personalizzate** ai clienti (es. tramite SMTP o API esterna come SendGrid).
* Invio di **messaggi WhatsApp** (tramite API ufficiale WhatsApp Business o Twilio).
* Gestione dei **template di messaggi** per campagne automatiche.

#### Analisi e statistiche

* Dashboard con grafici per:

  * Numero di clienti attivi per mese.
  * Distribuzione B2B/B2C.
  * Tasso di conversione.
  * Totale comunicazioni inviate.
* Possibilità di **esportare dati** in formato `.csv`, `.xlsx` o `.pdf`.

#### Ricerca e filtri avanzati

* Ricerca clienti per nome, email, tag o tipo.
* Filtri per data, stato o categoria.
* Ordinamento dinamico (es. per data o nome).

#### Sicurezza e configurazione

* Gestione di **utenti amministratori** con autenticazione JWT.
* Utilizzo di file `.env` per variabili sensibili (es. connessione DB, chiavi API, ecc.).
* Configurazione **CORS** per lo sviluppo locale e produzione.

### Stack tecnologico

#### Backend

* **Framework:** FastAPI
* **Database:** MongoDB (connessione asincrona)
* **ORM/Driver:** Motor o Beanie
* **Autenticazione:** JWT + OAuth2
* **CORS Middleware:** incluso
* **Gestione .env:** python-dotenv
* **Invio email:** aiosmtplib o FastAPI-Mail
* **Invio WhatsApp:** integrazione con API Twilio o Meta Graph API

#### Frontend

* **Framework:** Nuxt 3
* **Libreria CSS:** TailwindCSS
* **Componenti UI:** Flowbite + componenti personalizzati
* **Libreria grafici:** Chart.js o ApexCharts
* **Rich text editor:** TipTap o Quill
* **Gestione stato:** Pinia

### Struttura del progetto

```
crm/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── core/
│   │   └── utils/
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── app/
│   ├── public/
│   ├── nuxt.config.ts
│   └── ...
└── README.md
```

### Connessione MongoDB

Il database sarà ospitato su:

```
mongodb+srv://testUser:bD91w6E9qvhx6z8a@cluster0.fve8hpt.mongodb.net/
```

Questa connessione sarà gestita tramite variabile d’ambiente nel file `.env`:

```
MONGO_URI=mongodb+srv://testUser:bD91w6E9qvhx6z8a@cluster0.fve8hpt.mongodb.net/
```

### File `.env` esempio

```
MONGO_URI="mongodb+srv://testUser:***@cluster0.mongodb.net/"
EMAIL_HOST="smtp.gmail.com"
EMAIL_PORT=587
EMAIL_USER="noreply@mycrm.com"
EMAIL_PASS="password"
JWT_SECRET="supersegreto"
ALLOWED_ORIGINS="http://localhost:3000"
```

### File `requirements.txt`

```
fastapi
uvicorn
pydantic
motor
python-dotenv
fastapi-mail
aiosmtplib
python-multipart
pandas
openpyxl
matplotlib
beanie
requests
twilio
passlib[bcrypt]
pyjwt
```

### Suggerimenti per rendere il progetto unico

* Integrare **notifiche push via browser** per eventi come nuovi clienti o promemoria.
* Aggiungere una sezione **agenda** per appuntamenti o scadenze.
* Implementare un **modulo AI** per suggerire azioni (es. follow-up automatici).
* Creare una **modalità dark/light** per migliorare l’esperienza utente.
* Supportare **multilingua** (es. ITA/ENG).
