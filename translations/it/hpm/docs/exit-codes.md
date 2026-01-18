# Codici di Uscita

Riferimento per i codici di uscita di hpm e i loro significati.

## Tabella dei Codici di Uscita

| Codice | Nome | Descrizione |
|--------|------|-------------|
| 0 | SUCCESS | Comando completato con successo |
| 1 | CONFLICT | Conflitto di versione delle dipendenze |
| 2 | NOT_FOUND | Pacchetto non trovato |
| 3 | VERSION_NOT_FOUND | Versione richiesta non trovata |
| 4 | NETWORK | Errore di rete |
| 5 | INVALID_MANIFEST | package.json non valido |
| 6 | INTEGRITY | Verifica integrita fallita |
| 7 | RATE_LIMIT | Limite di frequenza API GitHub superato |
| 8 | CIRCULAR | Dipendenza circolare rilevata |

## Descrizioni Dettagliate

### Codice di Uscita 0: SUCCESS

Il comando e stato completato con successo.

```bash
$ hpm install
Installati 5 pacchetti
$ echo $?
0
```

### Codice di Uscita 1: CONFLICT

Due o piu pacchetti richiedono versioni incompatibili di una dipendenza.

**Esempio:**
```
Errore: Conflitto di dipendenze per hemlang/json

  pacchetto-a richiede hemlang/json@^1.0.0 (>=1.0.0 <2.0.0)
  pacchetto-b richiede hemlang/json@^2.0.0 (>=2.0.0 <3.0.0)

Nessuna versione soddisfa tutti i vincoli.
```

**Soluzioni:**
1. Controlla quali pacchetti hanno il conflitto:
   ```bash
   hpm why hemlang/json
   ```
2. Aggiorna il pacchetto in conflitto:
   ```bash
   hpm update pacchetto-a
   ```
3. Rilassa i vincoli di versione in package.json
4. Rimuovi uno dei pacchetti in conflitto

### Codice di Uscita 2: NOT_FOUND

Il pacchetto specificato non esiste su GitHub.

**Esempio:**
```
Errore: Pacchetto non trovato: hemlang/inesistente

Il repository hemlang/inesistente non esiste su GitHub.
```

**Soluzioni:**
1. Verifica l'ortografia del nome del pacchetto
2. Controlla se il repository esiste: `https://github.com/proprietario/repo`
3. Verifica di avere accesso (per repo privati, imposta GITHUB_TOKEN)

### Codice di Uscita 3: VERSION_NOT_FOUND

Nessuna versione corrisponde al vincolo specificato.

**Esempio:**
```
Errore: Nessuna versione di hemlang/json corrisponde al vincolo ^5.0.0

Versioni disponibili: 1.0.0, 1.1.0, 1.2.0, 2.0.0
```

**Soluzioni:**
1. Controlla le versioni disponibili su GitHub releases/tags
2. Usa un vincolo di versione valido
3. I tag di versione devono iniziare con 'v' (es. `v1.0.0`)

### Codice di Uscita 4: NETWORK

Si e verificato un errore relativo alla rete.

**Esempio:**
```
Errore: Errore di rete: impossibile connettersi a api.github.com

Per favore controlla la tua connessione internet e riprova.
```

**Soluzioni:**
1. Controlla la connessione internet
2. Controlla se GitHub e accessibile
3. Verifica le impostazioni proxy se sei dietro un firewall
4. Usa `--offline` se i pacchetti sono in cache:
   ```bash
   hpm install --offline
   ```
5. Aspetta e riprova (hpm riprova automaticamente)

### Codice di Uscita 5: INVALID_MANIFEST

Il file package.json e invalido o malformato.

**Esempio:**
```
Errore: package.json non valido

  - Campo obbligatorio mancante: name
  - Formato versione non valido: "1.0"
```

**Soluzioni:**
1. Controlla la sintassi JSON (usa un validatore JSON)
2. Assicurati che i campi obbligatori esistano (`name`, `version`)
3. Verifica i formati dei campi:
   - name: formato `proprietario/repo`
   - version: formato semver `X.Y.Z`
4. Rigenera:
   ```bash
   rm package.json
   hpm init
   ```

### Codice di Uscita 6: INTEGRITY

La verifica dell'integrita del pacchetto e fallita.

**Esempio:**
```
Errore: Verifica integrita fallita per hemlang/json@1.0.0

Atteso: sha256-abc123...
Attuale: sha256-def456...

Il pacchetto scaricato potrebbe essere corrotto.
```

**Soluzioni:**
1. Pulisci la cache e reinstalla:
   ```bash
   hpm cache clean
   hpm install
   ```
2. Controlla problemi di rete (download parziali)
3. Verifica che il pacchetto non sia stato manomesso

### Codice di Uscita 7: RATE_LIMIT

Il limite di frequenza dell'API GitHub e stato superato.

**Esempio:**
```
Errore: Limite di frequenza API GitHub superato

Limite di frequenza non autenticato: 60 richieste/ora
Utilizzo attuale: 60/60

Il limite di frequenza si resetta alle: 2024-01-15 10:30:00 UTC
```

**Soluzioni:**
1. **Autenticati con GitHub** (consigliato):
   ```bash
   export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
   hpm install
   ```
2. Aspetta che il limite di frequenza si resetti (si resetta ogni ora)
3. Usa la modalita offline se i pacchetti sono in cache:
   ```bash
   hpm install --offline
   ```

### Codice di Uscita 8: CIRCULAR

Rilevata dipendenza circolare nel grafo delle dipendenze.

**Esempio:**
```
Errore: Dipendenza circolare rilevata

  pacchetto-a@1.0.0
  └── pacchetto-b@1.0.0
      └── pacchetto-a@1.0.0  (circolare!)

Impossibile risolvere l'albero delle dipendenze.
```

**Soluzioni:**
1. Questo e solitamente un bug nei pacchetti stessi
2. Contatta i manutentori dei pacchetti
3. Evita di usare uno dei pacchetti circolari

## Uso dei Codici di Uscita negli Script

### Bash

```bash
#!/bin/bash

hpm install
codice_uscita=$?

case $codice_uscita in
  0)
    echo "Installazione riuscita"
    ;;
  1)
    echo "Conflitto di dipendenze - controlla i vincoli di versione"
    exit 1
    ;;
  2)
    echo "Pacchetto non trovato - controlla il nome del pacchetto"
    exit 1
    ;;
  4)
    echo "Errore di rete - controlla la connessione"
    exit 1
    ;;
  7)
    echo "Limite di frequenza - imposta GITHUB_TOKEN"
    exit 1
    ;;
  *)
    echo "Errore sconosciuto: $codice_uscita"
    exit 1
    ;;
esac
```

### CI/CD

```yaml
# GitHub Actions
- name: Installa dipendenze
  run: |
    hpm install
    if [ $? -eq 7 ]; then
      echo "::error::Limite di frequenza GitHub superato. Aggiungi GITHUB_TOKEN."
      exit 1
    fi
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Make

```makefile
install:
	@hpm install || (echo "Installazione fallita con codice $$?"; exit 1)

test: install
	@hpm test
```

## Risoluzione dei Problemi per Codice di Uscita

### Riferimento Rapido

| Codice | Prima Cosa da Controllare |
|--------|---------------------------|
| 1 | Esegui `hpm why <pacchetto>` per vedere il conflitto |
| 2 | Verifica il nome del pacchetto su GitHub |
| 3 | Controlla i tag versione disponibili su GitHub |
| 4 | Controlla la connessione internet |
| 5 | Valida la sintassi di package.json |
| 6 | Esegui `hpm cache clean && hpm install` |
| 7 | Imposta la variabile d'ambiente `GITHUB_TOKEN` |
| 8 | Contatta i manutentori dei pacchetti |

## Vedi Anche

- [Risoluzione dei Problemi](troubleshooting.md) - Soluzioni dettagliate
- [Comandi](commands.md) - Riferimento comandi
- [Configurazione](configuration.md) - Configurazione del token GitHub
