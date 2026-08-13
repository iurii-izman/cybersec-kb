---
type: lab
domain:
  - linux
techniques:
  - "[[Linux Filesystem Navigation]]"
  - "[[Linux File and Text Search]]"
  - "[[Shell Command Chaining and Redirection]]"
status: practiced
confidence: 2
source:
  - tryhackme
---

# THM - Linux Fundamentals (Pt1)

## Цель лаборатории

TryHackMe, путь `Cyber Security 101 → Start Your Cyber Security Journey → Linux Fundamentals (Pt1)`. Room завершён на 100%. Цель — освоить базовое взаимодействие с Linux terminal: определить user context, вывести text, ориентироваться в filesystem, читать и искать данные и познакомиться с shell operators/redirection.

## Что было новым

### Concepts

- [[Linux Shell]]
- [[Man Pages]] — related/review knowledge, а не новый evidence этой Room.

### Techniques

- [[Linux Filesystem Navigation]]
- [[Linux File and Text Search]]
- [[Shell Command Chaining and Redirection]]

### Tools

Отдельные Tool-сущности в этой Room не выделялись; commands сохранены внутри Techniques.

## Практика

### User context и basic output

**Goal:** понять basic terminal interaction и current user context.

**Action — lesson commands:**

```bash
whoami
echo "hello world"
```

**Evidence:** Room completed 100%; конкретный username и command output не предоставлены.

**Interpretation:** shell принимает command и возвращает output; user context влияет на разрешённые действия.

**Next step:** перед permission-sensitive действиями проверять user context и интерпретировать фактический output.

### Navigation

**Goal:** ориентироваться в filesystem без GUI.

**Action — commands covered:** `pwd`, `ls`, `cd`, `cat`.

**Evidence:** interactive room/task completed; exact path, listing, filename и output не сохранены.

**Interpretation:** current working directory задаёт context для relative paths; directory inspection и navigation помогают понять location и доступные files.

**Next step:** применять commands в следующих Linux labs без постоянной подсказки.

### File и text search

**Goal:** найти нужный file или text без ручного просмотра большого объёма данных.

**Action — commands covered:** `find`, `grep`.

Lesson context упоминал `~/access.log` и flag внутри; flag не сохраняется.

**Evidence:** interactive search task completed; exact find result, grep query/output, access log content и flag не предоставлены.

**Interpretation:** сначала нужно определить, ищется filename/path или content, затем выбрать `find` либо `grep`.

**Next step:** повторить commands на собственных или THM files и сохранить конкретный несекретный result при следующей практике.

### Shell operators

**Goal:** понять базовое управление execution и standard output.

**Action — learning evidence:** lesson covered `&`, `&&`, `>` и `>>`.

Lesson example:

```bash
echo hey > welcome
cat welcome
```

**Evidence:** operators и пример показаны в lesson; отдельный user-level command result не сохранён.

**Interpretation:** operators позволяют запускать command asynchronously, условно продолжать после success и перенаправлять output с заменой либо append.

**Next step:** выполнить собственный безопасный redirection workflow в следующей Lab и записать фактический результат.

## Ошибки и сложности

Конкретные mistakes пользователя не предоставлены. Lesson-specific file colors не перенесены как универсальное правило Linux.

## Что понял после практики

- Linux security work часто начинается с terminal interaction.
- `pwd`, `ls` и `cd` дают orientation и context.
- `cat` позволяет быстро inspect небольшой text file.
- `find` ищет filesystem entries, а `grep` — content/patterns.
- Shell operators позволяют связывать execution и перенаправлять output.
- Command output является evidence и требует interpretation, а не простого копирования.
- Current user context важен, поскольку определяет доступные действия.

## Что повторить

- [[Linux Shell]]
- [[Linux Filesystem Navigation]]
- [[Linux File and Text Search]]
- [[Shell Command Chaining and Redirection]]
- [[Man Pages]]

## Итог

Room дала первую bounded practice навигации и поиска в интерактивной Linux environment. Operators сохранены как learned material, поскольку отдельный user-level result для них не предоставлен.
