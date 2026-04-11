# Formattazione del Codice

Hemlock include un formattatore di codice integrato per imporre uno stile coerente.

## Utilizzo

```bash
hemlock format <FILE>         # Formatta un file in loco
hemlock format --check <FILE> # Verifica se il file è formattato (esce con 1 se non lo è)
```

## Regole di Stile

Il formattatore impone queste convenzioni:

| Regola | Valore |
|--------|--------|
| Indentazione | Tab |
| Stile parentesi graffe | K&R (parentesi graffa aperta sulla stessa riga) |
| Larghezza massima riga | 100 caratteri |
| Virgole finali | Sì, nei contesti multiriga |
| Righe vuote consecutive massime | 1 |

## Interruzione Automatica delle Righe

Il formattatore interrompe automaticamente le righe lunghe:

- **Parametri delle funzioni** - Le liste di parametri lunghe si interrompono con un parametro per riga
- **Espressioni binarie** - Le catene logiche/di confronto lunghe si interrompono agli operatori
- **Istruzioni import** - Le liste di import lunghe si interrompono con ogni elemento sulla propria riga
- **Catene di metodi** - Le catene lunghe si interrompono prima dei punti

## Esempio

Prima:
```hemlock
fn create_user(name: string, email: string, age: i32, active: bool, role: string) { return { name: name, email: email, age: age, active: active, role: role }; }
```

Dopo:
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

## Integrazione CI

Usa `--check` nelle pipeline CI per imporre la formattazione:

```bash
hemlock format --check src/main.hml || echo "File non formattato"
```
