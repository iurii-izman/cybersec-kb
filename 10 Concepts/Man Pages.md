---
type: concept
domain:
  - linux
techniques:
  - "[[Security Information Research]]"
status: practiced
confidence: 2
source:
  - tryhackme
---

# Man Pages

## Что это

Man pages — локальная справочная документация Unix-like systems для commands, interfaces и documented behaviour.

## Зачем это нужно

Official product/tool documentation обычно следует проверять до случайных third-party tutorials, когда важны точный syntax или поведение.

## Как это работает

Базовый вызов открывает manual page выбранной команды:

```bash
man <command>
```

## Подтверждённая практика

**Goal:** найти в manual page `nc` нужный syntax/example.

**Action:**

```bash
man nc
```

**Evidence:** Room [[THM - Search Skills]] завершён; пользователь нашёл требуемую информацию и ответил на вопрос. Конечная connection command не сохранена и здесь не выдумывается.

**Interpretation:** official documentation дала source of truth для documented syntax и behaviour.

**Next step:** в будущих Labs сначала проверять man page или официальную документацию, когда параметр либо поведение инструмента неясны.

## Связано с

- [[Security Information Research]]

## Что важно запомнить

- Формулировать конкретный вопрос перед чтением документации.
- Отличать documented behaviour от стороннего пересказа.
