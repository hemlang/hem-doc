# Formatacao de Codigo

Hemlock inclui um formatador de codigo integrado para garantir estilo consistente.

## Uso

```bash
hemlock format <FILE>         # Formata um arquivo no local
hemlock format --check <FILE> # Verifica se o arquivo esta formatado (exit 1 se nao)
```

## Regras de Estilo

O formatador aplica estas convencoes:

| Regra | Valor |
|-------|-------|
| Indentacao | Tabs |
| Estilo de chaves | K&R (chave de abertura na mesma linha) |
| Largura maxima de linha | 100 caracteres |
| Virgulas finais | Sim, em contextos multilinha |
| Maximo de linhas em branco consecutivas | 1 |

## Quebra Automatica de Linha

O formatador quebra automaticamente linhas longas:

- **Parametros de funcao** - Listas longas de parametros quebram com um parametro por linha
- **Expressoes binarias** - Cadeias longas de logica/comparacao quebram nos operadores
- **Instrucoes de import** - Listas longas de import quebram com cada item em sua propria linha
- **Cadeias de metodos** - Cadeias longas quebram antes dos pontos

## Exemplo

Antes:
```hemlock
fn create_user(name: string, email: string, age: i32, active: bool, role: string) { return { name: name, email: email, age: age, active: active, role: role }; }
```

Depois:
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

## Integracao com CI

Use `--check` em pipelines de CI para garantir formatacao:

```bash
hemlock format --check src/main.hml || echo "File not formatted"
```
