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

# Linux Filesystem Navigation

## Цель

Ориентироваться в Linux filesystem через CLI: определить текущее location, увидеть доступные entries, перейти в нужную directory и проверить небольшой text file.

## Когда применяется

Когда нужно понять filesystem context перед чтением, поиском или изменением данных в разрешённой среде.

## Что требуется на входе

Доступ к [[Linux Shell]] и известная либо исследуемая directory.

## Основные методы

### Узнать текущую директорию

**Goal:** определить текущую working directory.

**Action:**

```bash
pwd
```

**Evidence:** path текущей working directory.

**Interpretation:** relative paths будут разрешаться относительно этого location.

**Next step:** проверить содержимое или перейти в нужную directory.

### Посмотреть содержимое

**Goal:** увидеть entries в текущей directory.

**Action:**

```bash
ls
```

**Evidence:** directory entries, показанные командой.

**Interpretation:** результат даёт кандидатов для дальнейшей навигации или inspection. Цвета зависят от environment/theme и не являются универсальным доказательством типа файла.

**Next step:** выбрать relevant entry и перейти к нему либо проверить его содержимое.

### Перейти в директорию

**Goal:** изменить working directory.

**Action:**

```bash
cd DIRECTORY
```

**Evidence:** успешное изменение shell context; новый location можно подтвердить через `pwd`.

**Interpretation:** последующие relative paths разрешаются уже от новой working directory.

**Next step:** подтвердить location и посмотреть его entries.

### Прочитать небольшой текстовый файл

**Goal:** быстро проверить содержимое небольшого text file.

**Action:**

```bash
cat FILE
```

**Evidence:** file contents, записанные в standard output.

**Interpretation:** `cat` фактически concatenates file contents и пишет их в stdout; это удобно для небольших файлов, но не обязательно оптимально для огромных logs.

**Next step:** интерпретировать содержимое или перейти к [[Linux File and Text Search]].

## Инструменты

Отдельные Tool-сущности не выделялись: базовые commands сохранены в контексте техники.

## Типовой workflow

```text
Where am I? → pwd
  ↓
What is here? → ls
  ↓
Move somewhere → cd DIRECTORY
  ↓
Inspect a small file → cat FILE
```

## Что может пойти не так

- Relative path интерпретируется не из той working directory.
- Environment-specific colors принимаются за универсальное правило.
- `cat` используется для неудобно большого файла.

## Labs

- [[THM - Linux Fundamentals (Pt1)]] — interactive room completed 100%; exact paths and output не сохранены.

## Проверка себя

- Какая команда подтверждает current location?
- Почему перед relative path важно знать working directory?
- Когда `cat` подходит для inspection?
