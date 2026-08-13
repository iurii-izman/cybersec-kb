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

# CVE

## Что это

CVE — Common Vulnerabilities and Exposures, общепринятый identifier для публично раскрытой vulnerability.

## Зачем это нужно

Формат `CVE-YEAR-NUMBER` позволяет однозначно ссылаться на запись при [[Security Information Research]] и сопоставлять сведения из разных sources.

## Как это работает

CVE ID идентифицирует vulnerability record. Связанные источники могут отдельно описывать affected products, severity и доступные references.

## Связано с

- [[CVSS]]
- [[Proof of Concept]]
- [[Security Information Research]]

## Что важно запомнить

- CVE ID не является severity score.
- CVE ID не является exploit.
- Наличие CVE не доказывает, что конкретный target уязвим.
- `CVE-2026-1337` из [[THM - Search Skills]] — fictional TryHackMe training identifier, а не заявленная реальная публичная CVE.
