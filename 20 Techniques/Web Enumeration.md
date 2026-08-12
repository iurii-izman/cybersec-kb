---
type: technique
domain:
  - web
  - network
techniques: []
status: learned
confidence: 2
source:
  - tryhackme
---

# Web Enumeration

## Цель

Собрать подтверждённые сведения о доступной web-поверхности в разрешённой среде: сервисах, технологиях, ресурсах и поведении приложения.

## Когда применяется

После получения разрешённой цели и определения scope, до углублённой проверки отдельных компонентов.

## Что требуется на входе

- Разрешённый `TARGET` и границы тестирования.
- Сетевой доступ и понимание [[HTTP]].

## Основные методы

- Определение доступных HTTP-сервисов и портов с помощью [[Nmap]].
- Ручная проверка requests, responses и [[HTTP Status Codes]].
- Поиск связанных ресурсов через [[Content Discovery]].

## Инструменты

- [[Nmap]]
- [[DIRB]]
- [[DirBuster]]

## Типовой workflow

```text
Authorized target
  ↓
Find reachable web service
  ↓
Inspect HTTP behavior
  ↓
Discover content
  ↓
Interpret and verify findings
```

## Что может пойти не так

- Scope или протокол определены неверно.
- Redirects и virtual hosting искажают первичную картину.
- Одинаковые custom error pages создают ложные находки.
- Слишком агрессивные настройки создают лишнюю нагрузку.

## Labs

- [[THM - Content Discovery Example]] — example / seed

## Проверка себя

- Какова цель web enumeration?
- Какие evidence подтверждают наличие web-сервиса?
- Когда переходить к content discovery?
- Как отличить сигнал от custom error page?
