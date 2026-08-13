---
type: lab
domain:
  - osint
techniques:
  - "[[Security Information Research]]"
status: practiced
confidence: 2
source:
  - tryhackme
---

# THM - Search Skills

## Цель лаборатории

TryHackMe, путь `Cyber Security 101 → Start Your Cyber Security Journey → Search Skills`. Room завершён на 100% и обучал эффективному поиску и проверке cybersecurity information через специализированные сервисы, vulnerability references, official documentation и code repositories.

## Что было новым

### Concepts

- [[CVE]]
- [[CVSS]]
- [[Proof of Concept]]
- [[Man Pages]]

### Techniques

- [[Security Information Research]]

### Tools

- [[Shodan]] — lesson/simulation learning evidence без сохранённого конкретного результата.
- [[VirusTotal]] — lesson/simulation learning evidence без сохранённого конкретного результата.
- [[GitHub]] — confirmed practical repository research.

## Практика

### Task 2 — Shodan (TryScanMe)

**Goal:** понять, как специализированный Internet search service сужает результаты по security-relevant infrastructure information.

**Lesson evidence:** search term example `apache 2.4.1`; filters `country`, `port`, `org`, `hostname`; lesson examples `country:IE`, `port:22`, `org:AS7224`, `hostname:fakebank.thm`. Это примеры урока, а не targets или результаты пользователя.

**Interpretation:** filters уменьшают search scope и помогают отвечать на конкретный research question.

**Next step:** при реальной разрешённой практике сохранить конкретный question, query и интерпретируемый result до повышения [[Shodan]] до `practiced`.

### Task 3 — VirusTotal (TryDetectMe)

**Goal:** понять, как исследовать suspicious artifact или indicator через aggregation of security-engine signals.

**Lesson evidence:** scope включал file, URL, domain и hash; конкретный пользовательский scan result не сохранён.

**Interpretation:** несколько detections/signals дают evidence, но результат [[VirusTotal]] не является абсолютной истиной.

**Next step:** при будущей практике отделять indicator, observed signals и собственный вывод, не публикуя чувствительные данные.

### Task 4 — Vulnerability Databases

**Goal:** различить роль vulnerability identifier, severity context и demonstration.

**Evidence:** lesson связал [[CVE]], [[CVSS]] и [[Proof of Concept]] как разные элементы research.

**Interpretation:** CVE identifies, CVSS helps describe severity, PoC may demonstrate reproducibility. Ни один из этих sources сам по себе не доказывает применимость vulnerability к конкретной системе.

**Next step:** cross-check affected context и authoritative references до практического вывода.

### Task 5 — Technical Documentation (MAN)

**Goal:** найти в manual pages для `nc` пример, относящийся к запрошенному соединению.

**Action:**

```bash
man nc
```

**Evidence:** пользователь нашёл требуемую информацию и смог ответить на вопрос; точная конечная command line не была предоставлена и не записана.

**Interpretation:** [[Man Pages|official tool documentation]] является предпочтительным source of truth для syntax и documented behaviour.

**Next step:** сначала проверять official documentation/man page, когда параметр или поведение инструмента неясны.

### Task 6 — GitHub

**Goal:** найти информацию о training vulnerability в repository.

**Action:** review repository → read README → identify relevant script.

**Evidence:** `CVE-2026-1337` — fictional TryHackMe training identifier; подтверждённый ответ — `exploit.py`.

**Interpretation:** repository/README может дать полезный research context и PoC references, но найденный код нельзя автоматически считать корректным или безопасным.

**Next step:** для реального third-party PoC сначала изучить source, provenance и behaviour; не выполнять неизвестный код только потому, что он найден на [[GitHub]].

## Ошибки и сложности

Конкретные ошибки пользователя не предоставлены. Важно не переносить lesson examples в KB как личные tool results.

## Что понял после практики

- Правильный security research начинается с вопроса, а не с инструмента.
- Специализированные сервисы дают разные виды evidence.
- Official documentation обычно надёжнее случайного third-party tutorial.
- CVE, CVSS и PoC решают разные задачи.
- Repository/PoC нужно оценивать критически.
- Один источник не должен автоматически считаться абсолютной истиной.

## Что повторить

- [[Security Information Research]]
- [[Shodan]]
- [[VirusTotal]]
- [[CVE]]
- [[CVSS]]
- [[Proof of Concept]]
- [[Man Pages]]
- [[GitHub]]

## Итог

Room дал практику общей техники через MAN lookup и GitHub repository research, сохранив Shodan и VirusTotal на уровне learned evidence без выдуманных результатов.
