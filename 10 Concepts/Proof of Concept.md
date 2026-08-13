---
type: concept
domain:
  - general
techniques:
  - "[[Security Information Research]]"
status: learned
confidence: 2
source:
  - tryhackme
---

# Proof of Concept

## Что это

Proof of Concept (PoC) — минимальная демонстрация того, что vulnerability, technique или technical claim можно воспроизвести.

## Зачем это нужно

PoC может дать дополнительный research context для [[CVE]], но сам требует проверки в рамках [[Security Information Research]].

## Как это работает

Публичный repository может содержать incomplete, incorrect, intentionally misleading или malicious code. Наличие PoC не подтверждает его корректность, безопасность или применимость к конкретной системе.

## Связано с

- [[CVE]]
- [[CVSS]]
- [[Security Information Research]]
- [[GitHub]]

## Что важно запомнить

- Public PoC не равен trustworthy code.
- Public PoC не равен safe to execute.
- Перед любым использованием нужно отдельно исследовать source, provenance и behaviour в разрешённой среде.
