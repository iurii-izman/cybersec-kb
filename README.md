# CyberSec Knowledge Base v0.1

Локальный Obsidian-compatible Markdown Vault для ежедневного обучения cybersecurity. Он хранит знания независимо от конкретного курса, остаётся читаемым без Obsidian и версионируется Git.

## Архитектура

- **Concept** — что существует и почему важно.
- **Technique** — какую задачу нужно решить.
- **Tool** — чем и как выполнить технику.
- **Lab** — где знание применялось и как интерпретировался результат.

Главный принцип: **Technique > Tool**. Платформы вроде TryHackMe, HTB и PortSwigger дают практику, но не задают структуру базы.

## Структура

```text
00 Inbox/           сырые заметки для последующей обработки
10 Concepts/        понятия
20 Techniques/      задачи и техники
30 Tools/           инструменты
40 Labs/TryHackMe/  практический опыт
50 Cheatsheets/     зрелые короткие workflow
90 Templates/       шаблоны Obsidian
docs/               компактные соглашения
scripts/            read-only проверка Vault
Home.md             ручная стартовая карта
```

## Daily / Room workflow

```text
Start THM Room
  ↓
Capture raw notes in 00 Inbox
  ↓
Finish a meaningful section
  ↓
Create or update the Lab
  ↓
Extract reusable knowledge
  ↓
Update existing Concepts / Techniques / Tools
  ↓
Create only genuinely new entities
  ↓
Link notes → validate → review diff → commit
```

После TryHackMe фиксировать не пересказ комнаты, а новое знание, ход практики, ошибки и выводы. Практические шаги оформлять как Goal → Action → Evidence → Interpretation → Next Step. Использовать команды только в собственных, учебных или явно разрешённых средах.

`00 Inbox` — временный capture, а не архив. Во время урока сырые заметки допустимы; после законченного смыслового блока reusable knowledge переносится в Concepts, Techniques и Tools, а практический контекст остаётся в Lab. Не нужно очищать Inbox после каждого действия, но его следует периодически разбирать.

Перед созданием постоянной заметки найти существующую сущность по имени и смыслу. Если её нет, скопировать подходящий файл из `90 Templates`, заменить placeholders и добавить осмысленные `[[wikilinks]]`.

## Первый Field Test

Ближайшие 3–5 реальных TryHackMe Labs используются для проверки текущей архитектуры. До их завершения не добавлять новые architectural layers без наблюдаемой проблемы. Отмечать простыми наблюдениями: ambiguity классификации, дублирование, затраты времени, неудобство навигации, забываемые знания и повторяющиеся workflows. Это не метрики и не повод заранее переходить к v0.2.

## Открытие в Obsidian

Выберите **Open folder as vault** и укажите `C:\Dev\cybersec-kb`. Включите core plugin **Templates**, затем задайте `90 Templates` как **Template folder location**. Специальная `.obsidian`-конфигурация не требуется.

## Проверка

Нужен только Python 3; внешних пакетов нет:

```powershell
python -m unittest discover
python scripts/validate_kb.py
```

Unit tests проверяют позитивный fixture, основные ошибки и read-only поведение. Validator только читает файлы и возвращает ненулевой exit code при ошибке. Его упрощённая проверка YAML намеренно не заменяет полный YAML parser.

После успешной проверки просмотреть и сохранить понятный блок работы:

```powershell
git status --short
git diff
git add --all
git diff --cached
git commit -m "Add THM room notes"
```

Подробные Properties и naming rules: [docs/Conventions.md](docs/Conventions.md).

## Границы v0.1

В эту версию сознательно не входят Dataview, Anki, MITRE/OWASP automation, AI ingestion, dashboards, базы данных и собственное приложение. Рассматривать v0.2 стоит только когда ручная навигация перестанет справляться, появится устойчивая потребность в повторении или сформируются повторяющиеся playbooks.
