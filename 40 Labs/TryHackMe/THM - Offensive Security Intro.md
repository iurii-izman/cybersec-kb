---
type: lab
domain:
  - web
techniques:
  - "[[Content Discovery]]"
status: practiced
confidence: 2
source:
  - tryhackme
---

# THM - Offensive Security Intro

## Цель лаборатории

TryHackMe, путь `Cyber Security 101 → Start Your Cyber Security Journey → Offensive Security Intro`. Room `Offensive Security Intro` завершён на 100%; подтверждённый практический блок — Task 3 `Find Hidden Pages`, поиск скрытых страниц учебного приложения FakeBank.

## Что было новым

### Techniques

- [[Content Discovery]]

### Tools

- [[DIRB]]

## Практика

### Task 3 — Find Hidden Pages

**Goal:** найти скрытые страницы FakeBank.

**Action:**

```bash
dirb http://fakebank.thm
```

**Evidence:**

- `http://fakebank.thm/images`
- `http://fakebank.thm/bank-transfer`

**Interpretation:**

1. Не все существующие web resources обязаны быть представлены в обычной навигации.
2. [[Content Discovery]] позволяет находить такие пути.
3. Найденный функциональный endpoint `/bank-transfer` может стать следующим объектом исследования.
4. Обнаружение URL само по себе не является доказательством vulnerability.

**Next step:** открыть `/bank-transfer` и исследовать его назначение и поведение в рамках учебной лаборатории.

## Ошибки и сложности

В материале использовалась терминология `dirbuster`, однако фактически выполнялась команда `dirb`. Для KB этот evidence классифицирован как практика DIRB, чтобы не смешивать два отдельных инструмента.

## Что понял после практики

- Tool и Technique — разные уровни знания: [[DIRB]] реализует [[Content Discovery]].
- Скрытый путь может отсутствовать в UI, но оставаться доступным напрямую.
- Результаты discovery требуют интерпретации.
- Найденный endpoint — начало следующего шага, а не автоматически vulnerability.

## Что повторить

- [[DIRB]]
- [[Content Discovery]]
- [[Wordlists]]
- [[Web Enumeration]] как более широкий контекст, а не подтверждённая этой Lab практика полного workflow.

## Итог

Практика подтвердила цепочку Lab → [[DIRB]] → [[Content Discovery]] без автоматического повышения более широкой техники [[Web Enumeration]].
