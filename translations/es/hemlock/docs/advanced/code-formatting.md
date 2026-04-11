# Formateo de Codigo

Hemlock incluye un formateador de codigo integrado para imponer un estilo consistente.

## Uso

```bash
hemlock format <FILE>         # Formatear un archivo en su lugar
hemlock format --check <FILE> # Verificar si el archivo esta formateado (sale con 1 si no)
```

## Reglas de Estilo

El formateador impone estas convenciones:

| Regla | Valor |
|-------|-------|
| Indentacion | Tabulaciones |
| Estilo de llaves | K&R (llave de apertura en la misma linea) |
| Ancho maximo de linea | 100 caracteres |
| Comas finales | Si, en contextos multilinea |
| Lineas en blanco consecutivas maximas | 1 |

## Corte Automatico de Lineas

El formateador corta automaticamente las lineas largas:

- **Parametros de funcion** - Las listas de parametros largas se cortan con un parametro por linea
- **Expresiones binarias** - Las cadenas largas de operadores logicos/comparacion se cortan en los operadores
- **Sentencias import** - Las listas de importacion largas se cortan con cada elemento en su propia linea
- **Cadenas de metodos** - Las cadenas largas se cortan antes de los puntos

## Ejemplo

Antes:
```hemlock
fn create_user(name: string, email: string, age: i32, active: bool, role: string) { return { name: name, email: email, age: age, active: active, role: role }; }
```

Despues:
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

## Integracion CI

Use `--check` en pipelines de CI para imponer el formateo:

```bash
hemlock format --check src/main.hml || echo "File not formatted"
```
