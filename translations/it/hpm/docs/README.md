# Documentazione di hpm

Benvenuti nella documentazione di hpm (Hemlock Package Manager). hpm è il gestore di pacchetti ufficiale del linguaggio di programmazione [Hemlock](https://github.com/hemlang/hemlock).

## Panoramica

hpm utilizza GitHub come registro dei pacchetti, dove i pacchetti sono identificati dal percorso del loro repository GitHub (ad es. `hemlang/sprout`). Questo significa:

- **Nessun registro centrale** - i pacchetti risiedono nei repository GitHub
- **Tag di versione** - le release sono tag Git (ad es. `v1.0.0`)
- **Pubblicare è semplicemente git** - esegui il push di un tag per pubblicare una nuova versione

## Documentazione

### Per iniziare

- [Installazione](installation.md) - Come installare hpm
- [Avvio rapido](quick-start.md) - Diventa operativo in 5 minuti
- [Configurazione del progetto](project-setup.md) - Configurare un nuovo progetto Hemlock

### Guida utente

- [Riferimento comandi](commands.md) - Riferimento completo di tutti i comandi hpm
- [Configurazione](configuration.md) - File di configurazione e variabili d'ambiente
- [Risoluzione dei problemi](troubleshooting.md) - Problemi comuni e soluzioni

### Sviluppo di pacchetti

- [Creazione di pacchetti](creating-packages.md) - Come creare e pubblicare pacchetti
- [Specifica del pacchetto](package-spec.md) - Il formato package.json
- [Versionamento](versioning.md) - Versionamento semantico e vincoli di versione

### Riferimento

- [Architettura](architecture.md) - Architettura interna e progettazione
- [Codici di uscita](exit-codes.md) - Riferimento dei codici di uscita CLI

## Riferimento rapido

### Comandi di base

```bash
hpm init                              # Creare un nuovo package.json
hpm install                           # Installare tutte le dipendenze
hpm install owner/repo                # Aggiungere e installare un pacchetto
hpm install owner/repo@^1.0.0        # Installare con vincolo di versione
hpm uninstall owner/repo              # Rimuovere un pacchetto
hpm update                            # Aggiornare tutti i pacchetti
hpm list                              # Mostrare i pacchetti installati
hpm run <script>                      # Eseguire uno script del pacchetto
```

### Identificazione dei pacchetti

I pacchetti utilizzano il formato GitHub `owner/repo`:

```
hemlang/sprout          # Framework web
hemlang/json            # Utilità JSON
alice/http-client       # Libreria client HTTP
```

### Vincoli di versione

| Sintassi | Significato |
|----------|-------------|
| `1.0.0` | Versione esatta |
| `^1.2.3` | Compatibile (>=1.2.3 <2.0.0) |
| `~1.2.3` | Aggiornamenti patch (>=1.2.3 <1.3.0) |
| `>=1.0.0` | Almeno 1.0.0 |
| `*` | Qualsiasi versione |

## Ottenere aiuto

- Usa `hpm --help` per la guida da riga di comando
- Usa `hpm <command> --help` per la guida specifica di un comando
- Segnala problemi su [github.com/hemlang/hpm/issues](https://github.com/hemlang/hpm/issues)

## Licenza

hpm è rilasciato sotto la licenza MIT.
