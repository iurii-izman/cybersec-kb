---
type: concept
domain:
  - linux
techniques:
  - "[[Linux Filesystem Navigation]]"
  - "[[Linux File and Text Search]]"
  - "[[Shell Command Chaining and Redirection]]"
status: learned
confidence: 2
source:
  - tryhackme
---

# Linux Shell

## Что это

Shell — command-line interpreter, через который пользователь запускает команды и получает их output. Terminal предоставляет interface/session, внутри которой может работать shell; это не строго одно и то же.

## Зачем это нужно

Многие задачи Linux и security начинаются с terminal interaction. Для осмысленной работы важно различать command, переданные ему arguments, полученный output, текущий user context и working directory.

## Как это работает

Shell разбирает command и arguments, запускает нужную программу или builtin и показывает либо перенаправляет её output. Текущий user context влияет на разрешённые действия, а working directory — на разрешение relative paths.

## Пример

```bash
whoami
echo "hello world"
```

`whoami` показывает effective username текущего процесса и тем самым текущий user context. `echo` выводит переданные arguments в standard output.

## Связано с

- [[Linux Filesystem Navigation]]
- [[Linux File and Text Search]]
- [[Shell Command Chaining and Redirection]]
- [[Man Pages]]

## Что важно запомнить

- Command и его arguments задают действие, output даёт evidence о результате.
- User context определяет доступные действия.
- Working directory задаёт контекст для relative paths.

## Проверка себя

- Чем shell отличается от terminal?
- Что показывают `whoami` и `pwd`?
- Почему command output нужно интерпретировать?
