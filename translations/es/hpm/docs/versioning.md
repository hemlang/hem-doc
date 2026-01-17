# Versionado

Guia completa de versionado semantico en hpm.

## Versionado Semantico

hpm usa [Versionado Semantico 2.0.0](https://semver.org/) (semver) para versiones de paquetes.

### Formato de Version

```
MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]
```

**Ejemplos:**
```
1.0.0           # Version de lanzamiento
2.1.3           # Version de lanzamiento
1.0.0-alpha     # Pre-lanzamiento
1.0.0-beta.1    # Pre-lanzamiento con numero
1.0.0-rc.1      # Candidato a lanzamiento
1.0.0+20231201  # Con metadatos de compilacion
1.0.0-beta+exp  # Pre-lanzamiento con metadatos de compilacion
```

### Componentes de Version

| Componente | Descripcion | Ejemplo |
|------------|-------------|---------|
| MAJOR | Cambios incompatibles | `1.0.0` → `2.0.0` |
| MINOR | Nuevas caracteristicas (compatibles hacia atras) | `1.0.0` → `1.1.0` |
| PATCH | Correcciones de errores (compatibles hacia atras) | `1.0.0` → `1.0.1` |
| PRERELEASE | Identificador de pre-lanzamiento | `1.0.0-alpha` |
| BUILD | Metadatos de compilacion (ignorado en comparacion) | `1.0.0+build123` |

### Cuando Incrementar

| Tipo de Cambio | Incrementar | Ejemplo |
|----------------|-------------|---------|
| Cambio de API incompatible | MAJOR | Eliminar una funcion |
| Renombrar funcion publica | MAJOR | `parse()` → `decode()` |
| Cambiar firma de funcion | MAJOR | Agregar parametro requerido |
| Agregar nueva funcion | MINOR | Agregar `validate()` |
| Agregar parametro opcional | MINOR | Nuevo argumento opcional `options` |
| Correccion de error | PATCH | Arreglar puntero nulo |
| Mejora de rendimiento | PATCH | Algoritmo mas rapido |
| Refactorizacion interna | PATCH | Sin cambio de API |

## Restricciones de Version

### Sintaxis de Restricciones

| Sintaxis | Significado | Resuelve a |
|----------|-------------|------------|
| `1.2.3` | Version exacta | Solo 1.2.3 |
| `^1.2.3` | Caret (compatible) | ≥1.2.3 y <2.0.0 |
| `~1.2.3` | Tilde (actualizaciones de parche) | ≥1.2.3 y <1.3.0 |
| `>=1.0.0` | Al menos | 1.0.0 o superior |
| `>1.0.0` | Mayor que | Superior a 1.0.0 |
| `<2.0.0` | Menor que | Inferior a 2.0.0 |
| `<=2.0.0` | Como maximo | 2.0.0 o inferior |
| `>=1.0.0 <2.0.0` | Rango | Entre 1.0.0 y 2.0.0 |
| `*` | Cualquiera | Cualquier version |

### Rangos Caret (^)

El caret (`^`) permite cambios que no modifican el digito mas a la izquierda que no es cero:

```
^1.2.3  →  >=1.2.3 <2.0.0   # Permite 1.x.x
^0.2.3  →  >=0.2.3 <0.3.0   # Permite 0.2.x
^0.0.3  →  >=0.0.3 <0.0.4   # Solo permite 0.0.3
```

**Usar cuando:** Quieres actualizaciones compatibles dentro de una version mayor.

**Restriccion mas comun** - recomendada para la mayoria de dependencias.

### Rangos Tilde (~)

El tilde (`~`) solo permite cambios a nivel de parche:

```
~1.2.3  →  >=1.2.3 <1.3.0   # Permite 1.2.x
~1.2    →  >=1.2.0 <1.3.0   # Permite 1.2.x
~1      →  >=1.0.0 <2.0.0   # Permite 1.x.x
```

**Usar cuando:** Solo quieres correcciones de errores, sin nuevas caracteristicas.

### Rangos de Comparacion

Combina operadores de comparacion para control preciso:

```json
{
  "dependencies": {
    "owner/pkg": ">=1.0.0 <2.0.0",
    "owner/other": ">1.5.0 <=2.1.0"
  }
}
```

### Cualquier Version (*)

Coincide con cualquier version:

```json
{
  "dependencies": {
    "owner/pkg": "*"
  }
}
```

**Advertencia:** No recomendado para produccion. Siempre obtendra la ultima version.

## Versiones de Pre-lanzamiento

### Identificadores de Pre-lanzamiento

Los pre-lanzamientos tienen menor precedencia que los lanzamientos:

```
1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-beta < 1.0.0-rc.1 < 1.0.0
```

### Etiquetas Comunes de Pre-lanzamiento

| Etiqueta | Significado | Etapa |
|----------|-------------|-------|
| `alpha` | Desarrollo temprano | Muy inestable |
| `beta` | Caracteristicas completas | Pruebas |
| `rc` | Candidato a lanzamiento | Pruebas finales |
| `dev` | Snapshot de desarrollo | Inestable |

### Pre-lanzamiento en Restricciones

Las restricciones no coinciden con pre-lanzamientos por defecto:

```
^1.0.0    # NO coincide con 1.1.0-beta
>=1.0.0   # NO coincide con 2.0.0-alpha
```

Para incluir pre-lanzamientos, referencialos explicitamente:

```
>=1.0.0-alpha <2.0.0   # Incluye todos los pre-lanzamientos 1.x
```

## Comparacion de Versiones

### Reglas de Comparacion

1. Comparar MAJOR, MINOR, PATCH numericamente
2. Lanzamiento > pre-lanzamiento con la misma version
3. Pre-lanzamientos comparados alfanumericamente
4. Metadatos de compilacion ignorados

### Ejemplos

```
1.0.0 < 1.0.1 < 1.1.0 < 2.0.0

1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-beta < 1.0.0

1.0.0 = 1.0.0+build123  # Metadatos de compilacion ignorados
```

### Ordenamiento

Las versiones se ordenan de forma ascendente:

```
1.0.0
1.0.1
1.1.0
1.1.1
2.0.0-alpha
2.0.0-beta
2.0.0
```

## Resolucion de Versiones

### Algoritmo de Resolucion

Cuando multiples paquetes requieren la misma dependencia:

1. Recopilar todas las restricciones
2. Encontrar la interseccion de todos los rangos
3. Seleccionar la version mas alta en la interseccion
4. Error si ninguna version satisface todas

### Ejemplo de Resolucion

```
package-a requires hemlang/json@^1.0.0  (>=1.0.0 <2.0.0)
package-b requires hemlang/json@~1.2.0  (>=1.2.0 <1.3.0)

Interseccion: >=1.2.0 <1.3.0
Disponibles: [1.0.0, 1.1.0, 1.2.0, 1.2.1, 1.2.5, 1.3.0]
Resuelto: 1.2.5 (mas alta en la interseccion)
```

### Deteccion de Conflictos

El conflicto ocurre cuando ninguna version satisface todas las restricciones:

```
package-a requires hemlang/json@^1.0.0  (>=1.0.0 <2.0.0)
package-b requires hemlang/json@^2.0.0  (>=2.0.0 <3.0.0)

Interseccion: (vacia)
Resultado: CONFLICTO - ninguna version satisface ambas
```

## Mejores Practicas

### Para Consumidores de Paquetes

1. **Usar rangos caret** para la mayoria de dependencias:
   ```json
   "hemlang/json": "^1.2.0"
   ```

2. **Usar rangos tilde** para dependencias criticas:
   ```json
   "critical/lib": "~1.2.0"
   ```

3. **Fijar versiones** solo cuando sea necesario:
   ```json
   "unstable/pkg": "1.2.3"
   ```

4. **Incluir tu archivo de bloqueo** para compilaciones reproducibles

5. **Actualizar regularmente** para obtener correcciones de seguridad:
   ```bash
   hpm update
   hpm outdated
   ```

### Para Autores de Paquetes

1. **Comenzar en 0.1.0** para desarrollo inicial:
   - La API puede cambiar frecuentemente
   - Los usuarios esperan inestabilidad

2. **Ir a 1.0.0** cuando la API sea estable:
   - Compromiso publico de estabilidad
   - Cambios incompatibles requieren incremento mayor

3. **Seguir semver estrictamente**:
   - Cambio incompatible = MAJOR
   - Nueva caracteristica = MINOR
   - Correccion de error = PATCH

4. **Usar pre-lanzamientos** para pruebas:
   ```bash
   git tag v2.0.0-beta.1
   git push --tags
   ```

5. **Documentar cambios incompatibles** en CHANGELOG

## Publicar Versiones

### Crear Lanzamientos

```bash
# Actualizar version en package.json
# Editar package.json: "version": "1.1.0"

# Confirmar cambio de version
git add package.json
git commit -m "Bump version to 1.1.0"

# Crear y enviar etiqueta
git tag v1.1.0
git push origin main --tags
```

### Formato de Etiqueta

Las etiquetas **deben** comenzar con `v`:

```
v1.0.0      ✓ Correcto
v1.0.0-beta ✓ Correcto
1.0.0       ✗ No sera reconocido
```

### Flujo de Trabajo de Lanzamiento

```bash
# 1. Asegurar que las pruebas pasen
hpm test

# 2. Actualizar version en package.json
# 3. Actualizar CHANGELOG.md
# 4. Confirmar cambios
git add -A
git commit -m "Release v1.2.0"

# 5. Crear etiqueta
git tag v1.2.0

# 6. Enviar todo
git push origin main --tags
```

## Verificar Versiones

### Listar Versiones Instaladas

```bash
hpm list
```

### Verificar Actualizaciones

```bash
hpm outdated
```

Salida:
```
Package         Current  Wanted  Latest
hemlang/json    1.0.0    1.0.5   1.2.0
hemlang/sprout  2.0.0    2.0.3   2.1.0
```

- **Current**: Version instalada
- **Wanted**: Mas alta que coincide con la restriccion
- **Latest**: Ultima disponible

### Actualizar Paquetes

```bash
# Actualizar todos
hpm update

# Actualizar paquete especifico
hpm update hemlang/json
```

## Ver Tambien

- [Creacion de Paquetes](creating-packages.md) - Guia de publicacion
- [Especificacion de Paquetes](package-spec.md) - Formato de package.json
- [Comandos](commands.md) - Referencia de CLI
