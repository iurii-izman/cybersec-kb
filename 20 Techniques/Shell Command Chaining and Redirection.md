---
type: technique
domain:
  - linux
techniques: []
status: learned
confidence: 2
source:
  - tryhackme
---

# Shell Command Chaining and Redirection

## Цель

Управлять последовательностью выполнения shell commands и направлением их standard output.

## Когда применяется

Когда следующая command должна зависеть от успеха предыдущей, command нужно запустить asynchronously или output нужно записать в file.

## Что требуется на входе

Commands, ожидаемая зависимость между ними и понимание того, можно ли создавать либо изменять destination file.

## Основные методы

### Запустить asynchronously

```bash
COMMAND &
```

`&` запускает command asynchronously/background и позволяет shell продолжить работу без ожидания обычного foreground completion. Это само по себе не гарантирует, что process переживёт logout или завершение session.

### Продолжить только после успеха

```bash
COMMAND1 && COMMAND2
```

`COMMAND2` запускается только если `COMMAND1` завершилась успешно, то есть вернула successful exit status.

### Перезаписать output

```bash
COMMAND > FILE
```

`>` перенаправляет standard output; destination обычно создаётся либо существующий file truncates перед записью.

### Добавить output

```bash
COMMAND >> FILE
```

`>>` перенаправляет standard output в append mode и создаёт destination, если его ещё нет.

Lesson example:

```bash
echo hey > welcome
cat welcome
```

Этот пример подтверждает содержание lesson, но не является сохранённым user-level result.

## Инструменты

Отдельные Tool-сущности для operators и commands не выделялись.

## Типовой workflow

```text
Desired execution/output behavior
  ↓
Choose &, &&, >, or >>
  ↓
Run in an authorized environment
  ↓
Inspect process state, exit status, or destination content
  ↓
Decide whether the behavior matched intent
```

## Что может пойти не так

- `>` уничтожает прежнее содержимое destination из-за truncation.
- `&&` ошибочно воспринимается как безусловная последовательность.
- Background execution ошибочно считается гарантией persistence после logout.

## Labs

- [[THM - Linux Fundamentals (Pt1)]] — operators и lesson example изучены; отдельный practical result не сохранён.

## Проверка себя

- Чем `>` отличается от `>>`?
- При каком условии правая часть `&&` выполняется?
- Чего `&` не гарантирует?
