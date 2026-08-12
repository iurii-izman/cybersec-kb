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
type: concept
domain:
  - general
techniques: []
status: new
confidence: 1
source:
  - other
```

| Property | Семантика | Default в шаблоне |
|---|---|---|
| `type` | Тип сущности | Тип выбранного шаблона |
| `domain` | Один или несколько расширяемых domains | список с `general` |
| `techniques` | Wikilinks на применимые или использованные Techniques; `[]`, если связей пока нет | `[]` |
| `status` | Стадия освоения | `new` |
| `confidence` | Субъективная уверенность от 1 до 5 | `1` |
| `source` | Один или несколько источников знания | список с `other` |

Для самой Technique поле `techniques` обычно остаётся пустым. У Concept оно показывает применимые техники, у Tool — поддерживаемые техники, у Lab — реально использованные техники. Каждый элемент — quoted wikilink на существующую заметку в `20 Techniques`. У реальной Tool-заметки должна быть хотя бы одна Technique.

Допустимые `type`: `concept`, `technique`, `tool`, `lab`, `cheatsheet`.

`status` отражает подтверждённую стадию:

- `new` — заметка создана, личное понимание ещё не подтверждено;
- `learned` — могу объяснить основу своими словами;
- `practiced` — самостоятельно применил в разрешённой Lab;
- `confident` — могу выбрать и применить без постоянной подсказки.

`confidence` — отдельная субъективная уверенность от 1 до 5: `1` почти не помню, `2` понимаю с подсказкой, `3` могу повторить, `4` применяю самостоятельно, `5` могу уверенно объяснить и выбрать. `status` повышается по evidence, а `confidence` не обязана расти синхронно.

Стартовые domains: `web`, `network`, `linux`, `windows`, `active-directory`, `cloud`, `osint`, `cryptography`, `malware`, `defensive-security`, `general`. `general` — временный fallback; удалить его после выбора более точного domain.

Стартовые sources: `tryhackme`, `hackthebox`, `portswigger`, `book`, `course`, `documentation`, `personal-lab`, `other`. `other` — временный fallback; заменить его, если точный source известен. Перед расширением domain/source искать существующее значение; новые tokens записывать в lowercase kebab-case.

Для реальной THM Lab заменить `other` на `tryhackme`; для другой платформы выбрать её фактический source.

Перед использованием шаблона заполнить или удалить текстовые подсказки. `{{title}}` поддерживается встроенным Obsidian Templates и берёт имя файла заметки. Если Technique пока нет, оставлять всю запись `techniques: []`, а не пустой YAML list item.

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
