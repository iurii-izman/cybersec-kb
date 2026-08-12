# Соглашения CyberSec Knowledge Base v0.1

## Типы заметок

- **Concept** — что это и почему важно.
- **Technique** — какую задачу решаем.
- **Tool** — чем выполняем технику.
- **Lab** — где и как применили знания.
- **Cheatsheet** — краткий повторяющийся workflow, создаваемый только из накопленной практики.

Приоритет навигации: Technique → Tool. Курс или платформа являются источником практики, но не taxonomy базы.

## Properties

Каждая knowledge-заметка использует только базовые поля:

```yaml
type:
domain:
techniques:
status:
confidence:
source:
```

Допустимые `type`: `concept`, `technique`, `tool`, `lab`, `cheatsheet`.

Допустимые `status`: `new`, `learned`, `practiced`, `confident`.

`confidence` — целое число от 1 до 5. Стартовые domains: `web`, `network`, `linux`, `windows`, `active-directory`, `cloud`, `osint`, `cryptography`, `malware`, `defensive-security`, `general`. Domain остаётся расширяемым списком.

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
