# AGENTS.md

Постоянные правила для любой автоматизированной работы с этим Vault.

## Preserve architecture

Использовать только сущности Concept, Technique, Tool, Lab и, при накопленной практике, Cheatsheet. Не добавлять новый тип без явного утверждения пользователя. Центр структуры — Technique, а не Tool.

## Search before create

Перед созданием заметки искать существующую сущность по имени и смыслу. Если она уже существует, дополнять её и связывать wikilink. Одна идея должна иметь одно основное место хранения.

## Technique-first

Каждый Tool связывать с задачей или Technique. Не каталогизировать knowledge graph только вокруг инструментов и команд.

## Course independence

TryHackMe, Hack The Box и PortSwigger — источники практики, но не taxonomy Vault. Постоянные знания выносить в Concept, Technique и Tool.

## Commands require context

Не добавлять бессмысленные списки команд. Практический материал оформлять как Goal → Action → Evidence → Interpretation → Next Step. Объяснять ожидаемый сигнал, его смысл и дальнейшее решение.

## Preserve human knowledge

Не переписывать и не удалять пользовательские mistakes, observations, interpretations, conclusions, `what confused me` и decision reasoning без явной необходимости. При реорганизации сохранять исходный смысл и ссылки.

## No encyclopedic inflation

Не превращать заметки в копии документации, walkthrough или `--help`. Сохранять только материал, который помогает понять, применить, интерпретировать или повторить знание.

## Minimal architecture

Не добавлять плагины, frameworks, dependencies, новые Properties или типы сущностей без реальной необходимости. Vault должен оставаться обычной переносимой Markdown-директорией.

## No autonomous v0.2

Без явного запроса пользователя не добавлять Dataview, Anki, MITRE/OWASP mappings, AI ingestion, automation, dashboards, Procedures/Playbooks или новые сущности.

## Properties and naming

Соблюдать `docs/Conventions.md`. Использовать базовые поля `type`, `domain`, `techniques`, `status`, `confidence`, `source`. Не создавать случайные префиксы, UUID, ненужные даты и альтернативные имена сущности.

## Safety

Практические security-примеры допустимы только для labs, CTF, owned systems и explicitly authorized environments. Использовать placeholders `TARGET`, `http://TARGET/` и `/path/`; не заменять их реальными внешними targets. Не сохранять credentials, tokens и другие secrets.

## Validate before commit

Перед завершением изменений запускать `python -m unittest discover` и `python scripts/validate_kb.py`, затем просматривать `git diff` и `git diff --check`. Validator read-only; не изменять заметки автоматически для сокрытия ошибок.
