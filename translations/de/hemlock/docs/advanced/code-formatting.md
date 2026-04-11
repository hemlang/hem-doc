# Code-Formatierung

Hemlock enthält einen eingebauten Code-Formatierer zur Durchsetzung eines einheitlichen Stils.

## Verwendung

```bash
hemlock format <DATEI>         # Datei direkt formatieren
hemlock format --check <DATEI> # Prüfen ob Datei formatiert ist (Exit 1 wenn nicht)
```

## Stilregeln

Der Formatierer erzwingt diese Konventionen:

| Regel | Wert |
|-------|------|
| Einrückung | Tabs |
| Klammerstil | K&R (öffnende Klammer auf gleicher Zeile) |
| Maximale Zeilenbreite | 100 Zeichen |
| Nachgestellte Kommas | Ja, in mehrzeiligen Kontexten |
| Maximale aufeinanderfolgende Leerzeilen | 1 |

## Automatischer Zeilenumbruch

Der Formatierer bricht automatisch lange Zeilen um:

- **Funktionsparameter** - Lange Parameterlisten werden mit einem Parameter pro Zeile umbrochen
- **Binäre Ausdrücke** - Lange logische/Vergleichsketten werden an Operatoren umbrochen
- **Import-Anweisungen** - Lange Import-Listen werden mit jedem Element auf eigener Zeile umbrochen
- **Methodenketten** - Lange Ketten werden vor Punkten umbrochen

## Beispiel

Vorher:
```hemlock
fn create_user(name: string, email: string, age: i32, active: bool, role: string) { return { name: name, email: email, age: age, active: active, role: role }; }
```

Nachher:
```hemlock
fn create_user(
	name: string,
	email: string,
	age: i32,
	active: bool,
	role: string,
) {
	return {
		name: name,
		email: email,
		age: age,
		active: active,
		role: role,
	};
}
```

## CI-Integration

Verwenden Sie `--check` in CI-Pipelines zur Durchsetzung der Formatierung:

```bash
hemlock format --check src/main.hml || echo "Datei nicht formatiert"
```
