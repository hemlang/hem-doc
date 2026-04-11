# Formatage du code

Hemlock inclut un formateur de code integre pour imposer un style coherent.

## Utilisation

```bash
hemlock format <FILE>         # Formater un fichier sur place
hemlock format --check <FILE> # Verifier si le fichier est formate (exit 1 sinon)
```

## Regles de style

Le formateur impose ces conventions :

| Regle | Valeur |
|-------|--------|
| Indentation | Tabulations |
| Style d'accolades | K&R (accolade ouvrante sur la meme ligne) |
| Largeur maximale de ligne | 100 caracteres |
| Virgules finales | Oui, dans les contextes multilignes |
| Lignes vides consecutives max | 1 |

## Coupure de ligne automatique

Le formateur coupe automatiquement les longues lignes :

- **Parametres de fonction** - Les longues listes de parametres sont decoupees avec un parametre par ligne
- **Expressions binaires** - Les longues chaines logiques/comparaisons sont coupees aux operateurs
- **Instructions d'import** - Les longues listes d'imports sont decoupees avec chaque element sur sa propre ligne
- **Chaines de methodes** - Les longues chaines sont coupees avant les points

## Exemple

Avant :
```hemlock
fn create_user(name: string, email: string, age: i32, active: bool, role: string) { return { name: name, email: email, age: age, active: active, role: role }; }
```

Apres :
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

## Integration CI

Utilisez `--check` dans les pipelines CI pour imposer le formatage :

```bash
hemlock format --check src/main.hml || echo "File not formatted"
```
