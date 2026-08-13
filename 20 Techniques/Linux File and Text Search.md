---
type: technique
domain:
  - linux
techniques: []
status: practiced
confidence: 2
source:
  - tryhackme
---

# Linux File and Text Search

## Цель

Быстро находить filesystem entries или text внутри files, не просматривая большой объём данных вручную.

## Когда применяется

Когда известны filename/path criteria либо искомый pattern внутри известного файла.

## Что требуется на входе

Понимание того, ищется ли filename/path или content, доступ к [[Linux Shell]] и разрешённой filesystem area.

## Основные методы

### Найти entry по имени

**Goal:** найти file или directory с заданным именем от текущего location.

**Action:**

```bash
find . -name "NAME"
```

**Evidence:** matching filesystem paths.

**Interpretation:** `find` обходит hierarchy от указанной starting point (`.`) и `-name` задаёт filename criterion.

**Next step:** проверить найденный path и уточнить search criteria при лишних либо отсутствующих результатах.

Lesson example:

```bash
find -name passwords.txt
```

### Найти text внутри файла

**Goal:** найти строки известного файла, соответствующие pattern.

**Action:**

```bash
grep "PATTERN" FILE
```

**Evidence:** matching lines.

**Interpretation:** `grep` ищет content/patterns; он решает другую задачу, чем filesystem search через `find`.

**Next step:** inspect matching lines и при необходимости уточнить pattern.

Lesson example, не реальный credential:

```bash
grep "password123" passwords.txt
```

## Инструменты

Отдельные Tool-сущности не выделялись: commands сохранены внутри техники.

## Типовой workflow

```text
What am I looking for?
  ↓
Filename or path? → find
  ↓
Text inside a known file? → grep
  ↓
Inspect evidence
  ↓
Refine search
```

## Что может пойти не так

- `find` и `grep` смешиваются, хотя первый ищет filesystem entries, а второй — matching content.
- Search начинается не от той directory.
- Lesson example ошибочно принимается за реальный secret или пользовательский result.

## Labs

- [[THM - Linux Fundamentals (Pt1)]] — interactive search task completed; exact result, log content и flag не сохранены.

## Проверка себя

- Когда выбирать `find`, а когда `grep`?
- Что означает `.` в reusable `find` pattern?
- Как отличить lesson example от practical evidence?
