---
type: technique
domain:
  - osint
techniques: []
status: practiced
confidence: 2
source:
  - tryhackme
---

# Security Information Research

## Цель

Находить, проверять и сопоставлять security- и technical information с помощью специализированных поисковых сервисов, vulnerability references, официальной документации и code repositories.

## Когда применяется

- При исследовании Internet-exposed services и публично доступного контекста.
- При проверке reputation файла, URL или domain.
- При поиске известных vulnerabilities, официального syntax или связанного repository/PoC.
- Когда вывод нужно подтвердить несколькими независимыми источниками.

## Что требуется на входе

Конкретный research question и подходящий indicator: service, product/version, file, URL, domain, hash, vulnerability identifier или command name.

## Основные методы

- Сузить Internet-service search фильтрами в [[Shodan]].
- Получить агрегированные security signals через [[VirusTotal]].
- Разделить identifier, severity context и demonstration через [[CVE]], [[CVSS]] и [[Proof of Concept]].
- Сверить syntax и documented behaviour с [[Man Pages]] или другой официальной документацией.
- Исследовать README, source и provenance repository через [[GitHub]].
- Сопоставить выводы разных источников и отделить observation от interpretation.

## Инструменты

- [[Shodan]]
- [[VirusTotal]]
- [[GitHub]]

## Типовой workflow

```text
Research question
  ↓
Choose the most relevant source
  ↓
Collect evidence
  ↓
Cross-check provenance and context
  ↓
Record a bounded conclusion
```

## Что может пойти не так

- Один источник принимается за абсолютную истину.
- Vulnerability reference ошибочно считается доказательством уязвимости конкретной системы.
- Публичный repository или PoC считается корректным и безопасным без проверки.
- Поиск начинается с инструмента, а не с вопроса, и создаёт нерелевантный шум.

## Labs

- [[THM - Search Skills]] — MAN lookup и repository research дали подтверждённую практику.

## Проверка себя

- Какой вопрос я пытаюсь закрыть?
- Какой источник лучше всего отвечает именно на него?
- Что является evidence, а что моей interpretation?
- Чем можно независимо проверить вывод?
