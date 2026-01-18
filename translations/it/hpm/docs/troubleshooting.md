# Risoluzione dei Problemi

Soluzioni ai problemi comuni di hpm.

## Problemi di Installazione

### "hemlock: comando non trovato"

**Causa:** Hemlock non e installato o non e nel PATH.

**Soluzione:**

```bash
# Controlla se hemlock esiste
which hemlock

# Se non trovato, installa prima Hemlock
# Visita: https://github.com/hemlang/hemlock

# Dopo l'installazione, verifica
hemlock --version
```

### "hpm: comando non trovato"

**Causa:** hpm non e installato o non e nel PATH.

**Soluzione:**

```bash
# Controlla dove e installato hpm
ls -la /usr/local/bin/hpm
ls -la ~/.local/bin/hpm

# Se usi una posizione personalizzata, aggiungi al PATH
export PATH="$HOME/.local/bin:$PATH"

# Aggiungi a ~/.bashrc o ~/.zshrc per renderlo permanente
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Reinstalla se necessario
cd /percorso/a/hpm
sudo make install
```

### "Permesso negato" durante l'installazione

**Causa:** Nessun permesso di scrittura nella directory di installazione.

**Soluzione:**

```bash
# Opzione 1: Usa sudo per installazione a livello di sistema
sudo make install

# Opzione 2: Installa nella directory utente (senza sudo)
make install PREFIX=$HOME/.local
```

## Problemi di Dipendenze

### "Pacchetto non trovato" (codice di uscita 2)

**Causa:** Il pacchetto non esiste su GitHub.

**Soluzione:**

```bash
# Verifica che il pacchetto esista
# Controlla: https://github.com/proprietario/repo

# Verifica l'ortografia
hpm install hemlang/sprout  # Corretto
hpm install hemlan/sprout   # Proprietario sbagliato
hpm install hemlang/spout   # Repo sbagliato

# Controlla errori di battitura in package.json
cat package.json | grep -A 5 dependencies
```

### "Versione non trovata" (codice di uscita 3)

**Causa:** Nessuna release corrisponde al vincolo di versione.

**Soluzione:**

```bash
# Elenca le versioni disponibili (controlla release/tag su GitHub)
# I tag devono iniziare con 'v' (es. v1.0.0)

# Usa un vincolo di versione valido
hpm install proprietario/repo@^1.0.0

# Prova l'ultima versione
hpm install proprietario/repo

# Controlla i tag disponibili su GitHub
# https://github.com/proprietario/repo/tags
```

### "Conflitto di dipendenze" (codice di uscita 1)

**Causa:** Due pacchetti richiedono versioni incompatibili di una dipendenza.

**Soluzione:**

```bash
# Vedi il conflitto
hpm install --verbose

# Controlla cosa richiede la dipendenza
hpm why pacchetto/in-conflitto

# Soluzioni:
# 1. Aggiorna il pacchetto in conflitto
hpm update pacchetto/problema

# 2. Cambia i vincoli di versione in package.json
# Modifica per permettere versioni compatibili

# 3. Rimuovi uno dei pacchetti in conflitto
hpm uninstall un/pacchetto
```

### "Dipendenza circolare" (codice di uscita 8)

**Causa:** Il pacchetto A dipende da B, che dipende da A.

**Soluzione:**

```bash
# Identifica il ciclo
hpm install --verbose

# Questo e solitamente un bug nei pacchetti
# Contatta i manutentori dei pacchetti

# Workaround: evita uno dei pacchetti
```

## Problemi di Rete

### "Errore di rete" (codice di uscita 4)

**Causa:** Impossibile connettersi all'API GitHub.

**Soluzione:**

```bash
# Controlla la connessione internet
ping github.com

# Controlla se l'API GitHub e accessibile
curl -I https://api.github.com

# Riprova (hpm riprova automaticamente)
hpm install

# Usa la modalita offline se i pacchetti sono in cache
hpm install --offline

# Controlla le impostazioni proxy se sei dietro un firewall
export HTTPS_PROXY=http://proxy:8080
hpm install
```

### "Limite di frequenza GitHub superato" (codice di uscita 7)

**Causa:** Troppe richieste API senza autenticazione.

**Soluzione:**

```bash
# Opzione 1: Autenticati con token GitHub (consigliato)
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
hpm install

# Crea token: GitHub -> Impostazioni -> Impostazioni sviluppatore -> Token di accesso personali

# Opzione 2: Salva il token nel file di configurazione
mkdir -p ~/.hpm
echo '{"github_token": "ghp_xxxxxxxxxxxx"}' > ~/.hpm/config.json

# Opzione 3: Aspetta il reset del limite di frequenza (si resetta ogni ora)

# Opzione 4: Usa la modalita offline
hpm install --offline
```

### Timeout della connessione

**Causa:** Rete lenta o problemi API GitHub.

**Soluzione:**

```bash
# hpm riprova automaticamente con backoff esponenziale

# Controlla se GitHub ha problemi
# Visita: https://www.githubstatus.com

# Riprova piu tardi
hpm install

# Usa i pacchetti in cache
hpm install --offline
```

## Problemi di Package.json

### "package.json non valido" (codice di uscita 5)

**Causa:** Malformato o campi obbligatori mancanti.

**Soluzione:**

```bash
# Valida la sintassi JSON
cat package.json | python -m json.tool

# Controlla i campi obbligatori
cat package.json

# Campi obbligatori:
# - "name": formato proprietario/repo
# - "version": formato X.Y.Z

# Rigenera se necessario
rm package.json
hpm init
```

### Errore formato "name"

**Causa:** Nome pacchetto non nel formato `proprietario/repo`.

**Soluzione:**

```json
// Sbagliato
{
  "name": "mio-pacchetto"
}

// Corretto
{
  "name": "tuonome/mio-pacchetto"
}
```

### Errore formato "version"

**Causa:** Versione non nel formato semver.

**Soluzione:**

```json
// Sbagliato
{
  "version": "1.0"
}

// Corretto
{
  "version": "1.0.0"
}
```

## Problemi del File di Lock

### File di lock non sincronizzato

**Causa:** package.json modificato senza eseguire install.

**Soluzione:**

```bash
# Rigenera il file di lock
rm package-lock.json
hpm install
```

### File di lock corrotto

**Causa:** JSON non valido o modifiche manuali.

**Soluzione:**

```bash
# Controlla validita JSON
cat package-lock.json | python -m json.tool

# Rigenera
rm package-lock.json
hpm install
```

## Problemi di hem_modules

### I pacchetti non si installano

**Causa:** Vari possibili problemi.

**Soluzione:**

```bash
# Pulisci e reinstalla
rm -rf hem_modules
hpm install

# Controlla output verboso
hpm install --verbose
```

### L'import non funziona

**Causa:** Pacchetto non installato correttamente o percorso import sbagliato.

**Soluzione:**

```bash
# Verifica che il pacchetto sia installato
ls hem_modules/proprietario/repo/

# Controlla il campo main di package.json
cat hem_modules/proprietario/repo/package.json

# Formato import corretto
import { x } from "proprietario/repo";          # Usa la voce main
import { y } from "proprietario/repo/sottopercorso";  # Import sottopercorso
```

### Errore "Modulo non trovato"

**Causa:** Il percorso import non si risolve a un file.

**Soluzione:**

```bash
# Controlla il percorso import
ls hem_modules/proprietario/repo/src/

# Controlla index.hml
ls hem_modules/proprietario/repo/src/index.hml

# Verifica il campo main in package.json
cat hem_modules/proprietario/repo/package.json | grep main
```

## Problemi di Cache

### La cache occupa troppo spazio

**Soluzione:**

```bash
# Visualizza dimensione cache
hpm cache list

# Pulisci cache
hpm cache clean
```

### Permessi cache

**Soluzione:**

```bash
# Correggi permessi
chmod -R u+rw ~/.hpm/cache

# Oppure rimuovi e reinstalla
rm -rf ~/.hpm/cache
hpm install
```

### Usa cache sbagliata

**Soluzione:**

```bash
# Controlla posizione cache
echo $HPM_CACHE_DIR
ls ~/.hpm/cache

# Pulisci variabile d'ambiente se non corretta
unset HPM_CACHE_DIR
```

## Problemi di Script

### "Script non trovato"

**Causa:** Il nome dello script non esiste in package.json.

**Soluzione:**

```bash
# Elenca script disponibili
cat package.json | grep -A 20 scripts

# Controlla l'ortografia
hpm run test    # Corretto
hpm run tests   # Sbagliato se lo script si chiama "test"
```

### Lo script fallisce

**Causa:** Errore nel comando dello script.

**Soluzione:**

```bash
# Esegui il comando direttamente per vedere l'errore
hemlock test/run.hml

# Controlla la definizione dello script
cat package.json | grep test
```

## Debug

### Abilita output verboso

```bash
hpm install --verbose
```

### Controlla versione hpm

```bash
hpm --version
```

### Controlla versione hemlock

```bash
hemlock --version
```

### Dry run

Anteprima senza apportare modifiche:

```bash
hpm install --dry-run
```

### Ripartire da zero

Ricomincia da capo:

```bash
rm -rf hem_modules package-lock.json
hpm install
```

## Ottenere Aiuto

### Aiuto comandi

```bash
hpm --help
hpm install --help
```

### Segnalare problemi

Se incontri un bug:

1. Controlla i problemi esistenti: https://github.com/hemlang/hpm/issues
2. Crea un nuovo problema con:
   - Versione hpm (`hpm --version`)
   - Versione Hemlock (`hemlock --version`)
   - Sistema operativo
   - Passi per riprodurre
   - Messaggio di errore (usa `--verbose`)

## Riferimento Codici di Uscita

| Codice | Significato | Soluzione Comune |
|--------|-------------|------------------|
| 0 | Successo | - |
| 1 | Conflitto di dipendenze | Aggiorna o cambia i vincoli |
| 2 | Pacchetto non trovato | Controlla ortografia, verifica che il repo esista |
| 3 | Versione non trovata | Controlla versioni disponibili su GitHub |
| 4 | Errore di rete | Controlla connessione, riprova |
| 5 | package.json non valido | Correggi sintassi JSON e campi obbligatori |
| 6 | Verifica integrita fallita | Pulisci cache, reinstalla |
| 7 | Limite frequenza GitHub | Aggiungi GITHUB_TOKEN |
| 8 | Dipendenza circolare | Contatta i manutentori dei pacchetti |

## Vedi Anche

- [Installazione](installation.md) - Guida all'installazione
- [Configurazione](configuration.md) - Opzioni di configurazione
- [Comandi](commands.md) - Riferimento comandi
