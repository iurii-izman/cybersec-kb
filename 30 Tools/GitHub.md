---
type: tool
domain:
  - osint
techniques:
  - "[[Security Information Research]]"
status: practiced
confidence: 2
source:
  - tryhackme
---

# GitHub

## Что это

В контексте этой KB GitHub — source для исследования code repositories, README/documentation, technical analysis, scanner code, PoC repositories и CVE references.

## Для чего нужен

Помогает находить и проверять repository context в рамках [[Security Information Research]], не подменяя оценку provenance, correctness и safety найденного кода.

## Когда использовать

Когда research question связан с implementation, repository documentation, public analysis или возможным [[Proof of Concept]].

## Связанные техники

- [[Security Information Research]]

## Подтверждённая практика

**Goal:** найти информацию о training vulnerability в repository.

**Action:** review repository → read README → identify relevant script.

**Evidence:** для `CVE-2026-1337`, явно fictional TryHackMe training identifier, подтверждённый ответ — `exploit.py`.

**Interpretation:** README и source tree помогли связать описание с relevant script. Это не подтверждает реальную публичную [[CVE]], корректность кода или его безопасность.

**Next step:** перед работой с реальным third-party PoC отдельно изучить source, provenance и behaviour; неизвестный код не выполнять только потому, что он найден на GitHub.

## Важные моменты

- Repository existence не равен correctness.
- Stars не равны safety.
- Public PoC не равен trustworthy code.
- Здесь нет инструкций по запуску `exploit.py` или описания его поведения.

## Где использовал

- [[THM - Search Skills]] — Task 6, подтверждённый repository/README research.

## Что запомнить

- Читать README и source, но проверять утверждения независимо.
- Оценивать provenance до доверия к repository.
