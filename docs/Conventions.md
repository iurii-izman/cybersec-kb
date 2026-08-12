# Соглашения CyberSec Knowledge Base v0.1

## Типы заметок

- **Concept** — что это и почему важно.
- **Technique** — какую задачу решаем.
- **Tool** — чем выполняем технику.
- **Lab** — где и как применили знания.
- **Cheatsheet** — краткий повторяющийся workflow, создаваемый только из накопленной практики.

Приоритет навигации: Technique → Tool. Курс или платформа являются источником практики, но не taxonomy базы.

## Properties

Каждая knowledge-заметка использует одни и те же базовые поля:

```yaml
type:
domain:
techniques:
status:
confidence:
source:
```

| Property | Семантика | Default в шаблоне |
|---|---|---|
| `type` | Тип сущности | Тип выбранного шаблона |
| `domain` | Один или несколько расширяемых domains | `[general]` |
| `techniques` | Wikilinks на применимые или использованные Techniques; `[]`, если связей пока нет | `[]` или явный placeholder |
| `status` | Стадия освоения | `new` |
| `confidence` | Субъективная уверенность от 1 до 5 | `1` |
| `source` | Один или несколько источников знания | `[other]`, для THM Lab — `[tryhackme]` |

Для самой Technique поле `techniques` обычно остаётся пустым. У Concept оно показывает применимые техники, у Tool — поддерживаемые техники, у Lab — реально использованные техники.

Допустимые `type`: `concept`, `technique`, `tool`, `lab`, `cheatsheet`.

Допустимые `status`: `new`, `learned`, `practiced`, `confident`.

`confidence` — целое число от 1 до 5. Стартовые domains: `web`, `network`, `linux`, `windows`, `active-directory`, `cloud`, `osint`, `cryptography`, `malware`, `defensive-security`, `general`. Domain остаётся расширяемым списком.

`status` отражает путь `new` → `learned` → `practiced` → `confident`, но повышается только при наличии собственного понимания или практики. Стартовые sources: `tryhackme`, `hackthebox`, `portswigger`, `book`, `course`, `documentation`, `personal-lab`, `other`; список можно расширять осмысленно.

Перед использованием шаблона заменить или удалить все placeholders. `{{title}}` поддерживается встроенным Obsidian Templates и берёт имя файла заметки.

## Имена файлов

- Tools: `Nmap.md`, `DIRB.md`, `DirBuster.md`, `Burp Suite.md`.
- Techniques: `Content Discovery.md`, `Port Scanning.md`.
- Concepts: `HTTP.md`, `HTTP Status Codes.md`, `Wordlists.md`.
- Labs: `THM - Intro to Offensive Security.md`.

Не использовать случайные префиксы, UUID, ненужные даты и альтернативные имена одной сущности. Перед созданием файла искать совпадение по имени и смыслу.

## Практические команды

Команда хранится только вместе с контекстом:

```text
Goal → Action → Evidence → Interpretation → Next Step
```

Примеры предназначены только для labs, CTF, собственных систем и явно разрешённых сред. Использовать учебные placeholders `TARGET`, `http://TARGET/` и `/path/`, а не реальные внешние цели.
