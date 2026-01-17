# Versionierung

Vollständige Anleitung zur semantischen Versionierung in hpm.

## Semantische Versionierung

hpm verwendet [Semantic Versioning 2.0.0](https://semver.org/) (semver) für Paketversionen.

### Versionsformat

```
MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]
```

**Beispiele:**
```
1.0.0           # Release-Version
2.1.3           # Release-Version
1.0.0-alpha     # Pre-Release
1.0.0-beta.1    # Pre-Release mit Nummer
1.0.0-rc.1      # Release Candidate
1.0.0+20231201  # Mit Build-Metadaten
1.0.0-beta+exp  # Pre-Release mit Build-Metadaten
```

### Versionskomponenten

| Komponente | Beschreibung | Beispiel |
|------------|--------------|----------|
| MAJOR | Breaking Changes | `1.0.0` → `2.0.0` |
| MINOR | Neue Features (abwärtskompatibel) | `1.0.0` → `1.1.0` |
| PATCH | Bugfixes (abwärtskompatibel) | `1.0.0` → `1.0.1` |
| PRERELEASE | Pre-Release-Identifikator | `1.0.0-alpha` |
| BUILD | Build-Metadaten (bei Vergleich ignoriert) | `1.0.0+build123` |

### Wann erhöhen

| Änderungstyp | Erhöhen | Beispiel |
|--------------|---------|----------|
| Breaking API-Änderung | MAJOR | Funktion entfernen |
| Öffentliche Funktion umbenennen | MAJOR | `parse()` → `decode()` |
| Funktionssignatur ändern | MAJOR | Erforderlichen Parameter hinzufügen |
| Neue Funktion hinzufügen | MINOR | `validate()` hinzufügen |
| Optionalen Parameter hinzufügen | MINOR | Neues optionales `options`-Arg |
| Bugfix | PATCH | Null-Pointer beheben |
| Leistungsverbesserung | PATCH | Schnellerer Algorithmus |
| Internes Refactoring | PATCH | Keine API-Änderung |

## Versionseinschränkungen

### Einschränkungssyntax

| Syntax | Bedeutung | Löst auf zu |
|--------|-----------|-------------|
| `1.2.3` | Exakte Version | Nur 1.2.3 |
| `^1.2.3` | Caret (kompatibel) | ≥1.2.3 und <2.0.0 |
| `~1.2.3` | Tilde (Patch-Updates) | ≥1.2.3 und <1.3.0 |
| `>=1.0.0` | Mindestens | 1.0.0 oder höher |
| `>1.0.0` | Größer als | Höher als 1.0.0 |
| `<2.0.0` | Kleiner als | Niedriger als 2.0.0 |
| `<=2.0.0` | Höchstens | 2.0.0 oder niedriger |
| `>=1.0.0 <2.0.0` | Bereich | Zwischen 1.0.0 und 2.0.0 |
| `*` | Beliebig | Beliebige Version |

### Caret-Bereiche (^)

Das Caret (`^`) erlaubt Änderungen, die die linkeste Nicht-Null-Ziffer nicht modifizieren:

```
^1.2.3  →  >=1.2.3 <2.0.0   # Erlaubt 1.x.x
^0.2.3  →  >=0.2.3 <0.3.0   # Erlaubt 0.2.x
^0.0.3  →  >=0.0.3 <0.0.4   # Erlaubt nur 0.0.3
```

**Verwenden wenn:** Sie kompatible Updates innerhalb einer Major-Version wollen.

**Häufigste Einschränkung** - für die meisten Abhängigkeiten empfohlen.

### Tilde-Bereiche (~)

Die Tilde (`~`) erlaubt nur Patch-Level-Änderungen:

```
~1.2.3  →  >=1.2.3 <1.3.0   # Erlaubt 1.2.x
~1.2    →  >=1.2.0 <1.3.0   # Erlaubt 1.2.x
~1      →  >=1.0.0 <2.0.0   # Erlaubt 1.x.x
```

**Verwenden wenn:** Sie nur Bugfixes wollen, keine neuen Features.

### Vergleichsbereiche

Vergleichsoperatoren für präzise Kontrolle kombinieren:

```json
{
  "dependencies": {
    "owner/pkg": ">=1.0.0 <2.0.0",
    "owner/other": ">1.5.0 <=2.1.0"
  }
}
```

### Beliebige Version (*)

Entspricht jeder Version:

```json
{
  "dependencies": {
    "owner/pkg": "*"
  }
}
```

**Warnung:** Nicht für Produktion empfohlen. Wird immer die neueste Version holen.

## Pre-Release-Versionen

### Pre-Release-Identifikatoren

Pre-Releases haben niedrigere Priorität als Releases:

```
1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-beta < 1.0.0-rc.1 < 1.0.0
```

### Häufige Pre-Release-Tags

| Tag | Bedeutung | Stadium |
|-----|-----------|---------|
| `alpha` | Frühe Entwicklung | Sehr instabil |
| `beta` | Feature-vollständig | Testen |
| `rc` | Release Candidate | Finales Testen |
| `dev` | Entwicklungs-Snapshot | Instabil |

### Pre-Release in Einschränkungen

Einschränkungen entsprechen standardmäßig keinen Pre-Releases:

```
^1.0.0    # Entspricht NICHT 1.1.0-beta
>=1.0.0   # Entspricht NICHT 2.0.0-alpha
```

Um Pre-Releases einzuschließen, explizit referenzieren:

```
>=1.0.0-alpha <2.0.0   # Schließt alle 1.x Pre-Releases ein
```

## Versionsvergleich

### Vergleichsregeln

1. MAJOR, MINOR, PATCH numerisch vergleichen
2. Release > Pre-Release mit gleicher Version
3. Pre-Releases alphanumerisch vergleichen
4. Build-Metadaten werden ignoriert

### Beispiele

```
1.0.0 < 1.0.1 < 1.1.0 < 2.0.0

1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-beta < 1.0.0

1.0.0 = 1.0.0+build123  # Build-Metadaten ignoriert
```

### Sortierung

Versionen werden aufsteigend sortiert:

```
1.0.0
1.0.1
1.1.0
1.1.1
2.0.0-alpha
2.0.0-beta
2.0.0
```

## Versionsauflösung

### Auflösungsalgorithmus

Wenn mehrere Pakete dieselbe Abhängigkeit benötigen:

1. Alle Einschränkungen sammeln
2. Schnittmenge aller Bereiche finden
3. Höchste Version in der Schnittmenge wählen
4. Fehler, wenn keine Version alle erfüllt

### Beispiel-Auflösung

```
package-a erfordert hemlang/json@^1.0.0  (>=1.0.0 <2.0.0)
package-b erfordert hemlang/json@~1.2.0  (>=1.2.0 <1.3.0)

Schnittmenge: >=1.2.0 <1.3.0
Verfügbar: [1.0.0, 1.1.0, 1.2.0, 1.2.1, 1.2.5, 1.3.0]
Aufgelöst: 1.2.5 (höchste in Schnittmenge)
```

### Konflikterkennung

Konflikt tritt auf, wenn keine Version alle Einschränkungen erfüllt:

```
package-a erfordert hemlang/json@^1.0.0  (>=1.0.0 <2.0.0)
package-b erfordert hemlang/json@^2.0.0  (>=2.0.0 <3.0.0)

Schnittmenge: (leer)
Ergebnis: KONFLIKT - keine Version erfüllt beide
```

## Best Practices

### Für Paket-Konsumenten

1. **Caret-Bereiche verwenden** für die meisten Abhängigkeiten:
   ```json
   "hemlang/json": "^1.2.0"
   ```

2. **Tilde-Bereiche verwenden** für kritische Abhängigkeiten:
   ```json
   "critical/lib": "~1.2.0"
   ```

3. **Versionen nur bei Bedarf pinnen**:
   ```json
   "unstable/pkg": "1.2.3"
   ```

4. **Lock-Datei committen** für reproduzierbare Builds

5. **Regelmäßig aktualisieren** um Sicherheitsfixes zu erhalten:
   ```bash
   hpm update
   hpm outdated
   ```

### Für Paket-Autoren

1. **Bei 0.1.0 starten** für die anfängliche Entwicklung:
   - API kann sich häufig ändern
   - Benutzer erwarten Instabilität

2. **Zu 1.0.0 wechseln**, wenn API stabil ist:
   - Öffentliche Verpflichtung zur Stabilität
   - Breaking Changes erfordern Major-Bump

3. **Semver strikt folgen**:
   - Breaking Change = MAJOR
   - Neues Feature = MINOR
   - Bugfix = PATCH

4. **Pre-Releases für Tests verwenden**:
   ```bash
   git tag v2.0.0-beta.1
   git push --tags
   ```

5. **Breaking Changes dokumentieren** im CHANGELOG

## Versionen veröffentlichen

### Releases erstellen

```bash
# Version in package.json aktualisieren
# package.json bearbeiten: "version": "1.1.0"

# Versionsänderung committen
git add package.json
git commit -m "Bump version to 1.1.0"

# Tag erstellen und pushen
git tag v1.1.0
git push origin main --tags
```

### Tag-Format

Tags **müssen** mit `v` beginnen:

```
v1.0.0      ✓ Richtig
v1.0.0-beta ✓ Richtig
1.0.0       ✗ Wird nicht erkannt
```

### Release-Workflow

```bash
# 1. Sicherstellen, dass Tests bestehen
hpm test

# 2. Version in package.json aktualisieren
# 3. CHANGELOG.md aktualisieren
# 4. Änderungen committen
git add -A
git commit -m "Release v1.2.0"

# 5. Tag erstellen
git tag v1.2.0

# 6. Alles pushen
git push origin main --tags
```

## Versionen prüfen

### Installierte Versionen auflisten

```bash
hpm list
```

### Nach Updates suchen

```bash
hpm outdated
```

Ausgabe:
```
Package         Current  Wanted  Latest
hemlang/json    1.0.0    1.0.5   1.2.0
hemlang/sprout  2.0.0    2.0.3   2.1.0
```

- **Current**: Installierte Version
- **Wanted**: Höchste, die Einschränkung entspricht
- **Latest**: Neueste verfügbar

### Pakete aktualisieren

```bash
# Alle aktualisieren
hpm update

# Bestimmtes Paket aktualisieren
hpm update hemlang/json
```

## Siehe auch

- [Pakete erstellen](creating-packages.md) - Veröffentlichungsanleitung
- [Paketspezifikation](package-spec.md) - package.json-Format
- [Befehle](commands.md) - CLI-Referenz
