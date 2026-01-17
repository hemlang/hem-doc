# Bem-vindo ao Hemlock

> "Uma pequena linguagem insegura para escrever coisas inseguras com segurança."

**Hemlock** é uma linguagem de scripting para sistemas que combina o poder do C com a ergonomia moderna de scripting. Ela oferece gerenciamento manual de memória, controle explícito e concorrência assíncrona estruturada integrada.

## O que é Hemlock?

Hemlock é projetada para programadores que desejam:

- **Controle explícito** sobre memória e execução
- **Sintaxe similar ao C** com conveniências modernas
- **Sem comportamento oculto** ou mágica
- **Async paralelo verdadeiro** com concorrência baseada em pthread

Hemlock NÃO é uma linguagem com segurança de memória e coleta de lixo. Em vez disso, ela fornece as ferramentas para ser seguro (`buffer`, anotações de tipo, verificação de limites) sem forçá-lo a usá-las (`ptr`, memória manual, operações inseguras).

## Exemplo Rápido

```hemlock
// Olá, Hemlock!
fn greet(name: string): string {
    return `Olá, ${name}!`;
}

let message = greet("Mundo");
print(message);

// Gerenciamento manual de memória
let buf = buffer(64);
buf[0] = 72;  // 'H'
buf[1] = 105; // 'i'
print(buf);
free(buf);
```

## Recursos em Resumo

| Recurso | Descrição |
|---------|-----------|
| **Sistema de Tipos** | i8-i64, u8-u64, f32/f64, bool, string, rune, ptr, buffer, array, object |
| **Memória** | Gerenciamento manual com `alloc()`, `buffer()`, `free()` |
| **Async** | `async`/`await` integrado com paralelismo pthread verdadeiro |
| **FFI** | Chame funções C diretamente de bibliotecas compartilhadas |
| **Biblioteca Padrão** | 40 módulos incluindo crypto, http, sqlite, json e mais |

## Primeiros Passos

Pronto para começar? Veja como iniciar:

1. **[Instalação](#getting-started-installation)** - Baixe e configure o Hemlock
2. **[Início Rápido](#getting-started-quick-start)** - Escreva seu primeiro programa em minutos
3. **[Tutorial](#getting-started-tutorial)** - Aprenda Hemlock passo a passo

## Seções da Documentação

- **Primeiros Passos** - Instalação, guia de início rápido e tutoriais
- **Guia da Linguagem** - Aprofunde-se em sintaxe, tipos, funções e mais
- **Tópicos Avançados** - Programação async, FFI, sinais e operações atômicas
- **Referência da API** - Referência completa de funções integradas e biblioteca padrão
- **Design e Filosofia** - Entenda por que Hemlock é do jeito que é

## Gerenciador de Pacotes

Hemlock vem com **hpm**, um gerenciador de pacotes para gerenciar dependências:

```bash
hpm init meu-projeto
hpm add algum-pacote
hpm run
```

Consulte as seções da documentação do hpm para mais detalhes.

---

Use a navegação à esquerda para explorar a documentação, ou use a barra de pesquisa para encontrar tópicos específicos.
