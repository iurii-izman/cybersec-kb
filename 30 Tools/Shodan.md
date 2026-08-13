---
type: tool
domain:
  - network
  - osint
techniques:
  - "[[Security Information Research]]"
status: learned
confidence: 2
source:
  - tryhackme
---

# Shodan

## Что это

Shodan — поисковый сервис для Internet-exposed devices/services и информации, которую они публично представляют.

## Для чего нужен

Помогает исследовать network equipment, публично доступные services, banners, ports, organisations/ASN context и hostnames в рамках [[Security Information Research]].

## Когда использовать

Когда research question относится к публично наблюдаемой Internet infrastructure и результаты нужно сузить по известным признакам.

## Связанные техники

- [[Security Information Research]]

## Базовый синтаксис

В уроке показан поисковый запрос с filters. Это lesson examples, а не реальные targets или результаты пользователя:

```text
apache 2.4.1
country:IE
port:22
org:AS7224
hostname:fakebank.thm
```

## Важные параметры

| Filter | Назначение |
|---|---|
| `country` | Ограничить результаты страной |
| `port` | Искать наблюдаемый service port |
| `org` | Ограничить организацией или ASN context |
| `hostname` | Ограничить hostname |

## Как читать результат

Filters уменьшают search scope и помогают отвечать на конкретный research question. Найденная запись остаётся публичным наблюдением сервиса и требует проверки контекста; она не доказывает vulnerability.

## Важные моменты

- Примеры выше взяты из lesson и не являются evidence самостоятельного Internet scanning.
- Эта заметка фиксирует learned evidence без сохранённого конкретного пользовательского результата.

## Где изучил

- [[THM - Search Skills]] — Task 2, lesson/simulation learning evidence.

## Что запомнить

- Начинать с research question.
- Использовать filters для уменьшения шума.
- Не путать публичный service banner с подтверждённой vulnerability.
