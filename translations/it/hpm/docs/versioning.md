# Versionamento

Guida completa al versionamento semantico in hpm.

## Versionamento Semantico

hpm usa il [Versionamento Semantico 2.0.0](https://semver.org/) (semver) per le versioni dei pacchetti.

### Formato della Versione

```
MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]
```

**Esempi:**
```
1.0.0           # Versione di release
2.1.3           # Versione di release
1.0.0-alpha     # Pre-release
1.0.0-beta.1    # Pre-release con numero
1.0.0-rc.1      # Release candidate
1.0.0+20231201  # Con metadati di build
1.0.0-beta+exp  # Pre-release con metadati di build
```

### Componenti della Versione

| Componente | Descrizione | Esempio |
|------------|-------------|---------|
| MAJOR | Modifiche incompatibili | `1.0.0` -> `2.0.0` |
| MINOR | Nuove funzionalita (retrocompatibili) | `1.0.0` -> `1.1.0` |
| PATCH | Correzioni bug (retrocompatibili) | `1.0.0` -> `1.0.1` |
| PRERELEASE | Identificatore pre-release | `1.0.0-alpha` |
| BUILD | Metadati di build (ignorati nel confronto) | `1.0.0+build123` |

### Quando Incrementare

| Tipo di Modifica | Incremento | Esempio |
|------------------|------------|---------|
| Modifica API incompatibile | MAJOR | Rimuovere una funzione |
| Rinominare funzione pubblica | MAJOR | `parse()` -> `decode()` |
| Cambiare firma funzione | MAJOR | Aggiungere parametro obbligatorio |
| Aggiungere nuova funzione | MINOR | Aggiungere `validate()` |
| Aggiungere parametro opzionale | MINOR | Nuovo argomento `options` opzionale |
| Correzione bug | PATCH | Correggere puntatore nullo |
| Miglioramento prestazioni | PATCH | Algoritmo piu veloce |
| Refactoring interno | PATCH | Nessun cambio API |

## Vincoli di Versione

### Sintassi dei Vincoli

| Sintassi | Significato | Si risolve in |
|----------|-------------|---------------|
| `1.2.3` | Versione esatta | Solo 1.2.3 |
| `^1.2.3` | Caret (compatibile) | >=1.2.3 e <2.0.0 |
| `~1.2.3` | Tilde (aggiornamenti patch) | >=1.2.3 e <1.3.0 |
| `>=1.0.0` | Almeno | 1.0.0 o superiore |
| `>1.0.0` | Maggiore di | Superiore a 1.0.0 |
| `<2.0.0` | Minore di | Inferiore a 2.0.0 |
| `<=2.0.0` | Al massimo | 2.0.0 o inferiore |
| `>=1.0.0 <2.0.0` | Range | Tra 1.0.0 e 2.0.0 |
| `*` | Qualsiasi | Qualsiasi versione |

### Range Caret (^)

Il caret (`^`) permette modifiche che non alterano la cifra non-zero piu a sinistra:

```
^1.2.3  ->  >=1.2.3 <2.0.0   # Permette 1.x.x
^0.2.3  ->  >=0.2.3 <0.3.0   # Permette 0.2.x
^0.0.3  ->  >=0.0.3 <0.0.4   # Permette solo 0.0.3
```

**Usa quando:** Vuoi aggiornamenti compatibili entro una versione major.

**Vincolo piu comune** - consigliato per la maggior parte delle dipendenze.

### Range Tilde (~)

Il tilde (`~`) permette solo modifiche a livello patch:

```
~1.2.3  ->  >=1.2.3 <1.3.0   # Permette 1.2.x
~1.2    ->  >=1.2.0 <1.3.0   # Permette 1.2.x
~1      ->  >=1.0.0 <2.0.0   # Permette 1.x.x
```

**Usa quando:** Vuoi solo correzioni bug, nessuna nuova funzionalita.

### Range di Confronto

Combina operatori di confronto per un controllo preciso:

```json
{
  "dependencies": {
    "proprietario/pkg": ">=1.0.0 <2.0.0",
    "proprietario/altro": ">1.5.0 <=2.1.0"
  }
}
```

### Qualsiasi Versione (*)

Corrisponde a qualsiasi versione:

```json
{
  "dependencies": {
    "proprietario/pkg": "*"
  }
}
```

**Attenzione:** Non consigliato per produzione. Prendera sempre l'ultima versione.

## Versioni Pre-release

### Identificatori Pre-release

Le pre-release hanno precedenza inferiore rispetto alle release:

```
1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-beta < 1.0.0-rc.1 < 1.0.0
```

### Tag Pre-release Comuni

| Tag | Significato | Fase |
|-----|-------------|------|
| `alpha` | Sviluppo iniziale | Molto instabile |
| `beta` | Funzionalita complete | Test |
| `rc` | Release candidate | Test finali |
| `dev` | Snapshot di sviluppo | Instabile |

### Pre-release nei Vincoli

I vincoli non corrispondono alle pre-release per default:

```
^1.0.0    # NON corrisponde a 1.1.0-beta
>=1.0.0   # NON corrisponde a 2.0.0-alpha
```

Per includere le pre-release, referenziale esplicitamente:

```
>=1.0.0-alpha <2.0.0   # Include tutte le pre-release 1.x
```

## Confronto delle Versioni

### Regole di Confronto

1. Confronta MAJOR, MINOR, PATCH numericamente
2. Release > pre-release con stessa versione
3. Pre-release confrontate alfanumericamente
4. Metadati di build ignorati

### Esempi

```
1.0.0 < 1.0.1 < 1.1.0 < 2.0.0

1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-beta < 1.0.0

1.0.0 = 1.0.0+build123  # Metadati di build ignorati
```

### Ordinamento

Le versioni si ordinano in modo ascendente:

```
1.0.0
1.0.1
1.1.0
1.1.1
2.0.0-alpha
2.0.0-beta
2.0.0
```

## Risoluzione delle Versioni

### Algoritmo di Risoluzione

Quando piu pacchetti richiedono la stessa dipendenza:

1. Raccogli tutti i vincoli
2. Trova l'intersezione di tutti i range
3. Seleziona la versione piu alta nell'intersezione
4. Errore se nessuna versione soddisfa tutti

### Esempio di Risoluzione

```
pacchetto-a richiede hemlang/json@^1.0.0  (>=1.0.0 <2.0.0)
pacchetto-b richiede hemlang/json@~1.2.0  (>=1.2.0 <1.3.0)

Intersezione: >=1.2.0 <1.3.0
Disponibili: [1.0.0, 1.1.0, 1.2.0, 1.2.1, 1.2.5, 1.3.0]
Risolto: 1.2.5 (piu alta nell'intersezione)
```

### Rilevamento Conflitti

Il conflitto si verifica quando nessuna versione soddisfa tutti i vincoli:

```
pacchetto-a richiede hemlang/json@^1.0.0  (>=1.0.0 <2.0.0)
pacchetto-b richiede hemlang/json@^2.0.0  (>=2.0.0 <3.0.0)

Intersezione: (vuota)
Risultato: CONFLITTO - nessuna versione soddisfa entrambi
```

## Best Practice

### Per i Consumatori di Pacchetti

1. **Usa range caret** per la maggior parte delle dipendenze:
   ```json
   "hemlang/json": "^1.2.0"
   ```

2. **Usa range tilde** per dipendenze critiche:
   ```json
   "critico/lib": "~1.2.0"
   ```

3. **Fissa le versioni** solo quando necessario:
   ```json
   "instabile/pkg": "1.2.3"
   ```

4. **Committa il tuo file di lock** per build riproducibili

5. **Aggiorna regolarmente** per ottenere correzioni di sicurezza:
   ```bash
   hpm update
   hpm outdated
   ```

### Per gli Autori di Pacchetti

1. **Inizia da 0.1.0** per lo sviluppo iniziale:
   - L'API puo cambiare frequentemente
   - Gli utenti si aspettano instabilita

2. **Vai a 1.0.0** quando l'API e stabile:
   - Impegno pubblico alla stabilita
   - Le modifiche incompatibili richiedono bump major

3. **Segui rigorosamente semver**:
   - Modifica incompatibile = MAJOR
   - Nuova funzionalita = MINOR
   - Correzione bug = PATCH

4. **Usa pre-release** per i test:
   ```bash
   git tag v2.0.0-beta.1
   git push --tags
   ```

5. **Documenta le modifiche incompatibili** nel CHANGELOG

## Pubblicazione delle Versioni

### Creazione delle Release

```bash
# Aggiorna la versione in package.json
# Modifica package.json: "version": "1.1.0"

# Committa la modifica della versione
git add package.json
git commit -m "Bump versione a 1.1.0"

# Crea e pusha il tag
git tag v1.1.0
git push origin main --tags
```

### Formato del Tag

I tag **devono** iniziare con `v`:

```
v1.0.0      Corretto
v1.0.0-beta Corretto
1.0.0       Non verra riconosciuto
```

### Flusso di Lavoro per la Release

```bash
# 1. Assicurati che i test passino
hpm test

# 2. Aggiorna la versione in package.json
# 3. Aggiorna CHANGELOG.md
# 4. Committa le modifiche
git add -A
git commit -m "Release v1.2.0"

# 5. Crea il tag
git tag v1.2.0

# 6. Pusha tutto
git push origin main --tags
```

## Verifica delle Versioni

### Elenca le Versioni Installate

```bash
hpm list
```

### Controlla gli Aggiornamenti

```bash
hpm outdated
```

Output:
```
Pacchetto       Corrente Desiderata Ultima
hemlang/json    1.0.0    1.0.5      1.2.0
hemlang/sprout  2.0.0    2.0.3      2.1.0
```

- **Corrente**: Versione installata
- **Desiderata**: Piu alta che corrisponde al vincolo
- **Ultima**: Ultima disponibile

### Aggiorna i Pacchetti

```bash
# Aggiorna tutti
hpm update

# Aggiorna pacchetto specifico
hpm update hemlang/json
```

## Vedi Anche

- [Creazione di Pacchetti](creating-packages.md) - Guida alla pubblicazione
- [Specifiche dei Pacchetti](package-spec.md) - Formato package.json
- [Comandi](commands.md) - Riferimento CLI
