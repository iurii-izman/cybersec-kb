# AGENTS.md

Постоянные правила для любой автоматизированной работы с этим Vault.

## Architecture

Использовать только сущности Concept, Technique, Tool, Lab и, при накопленной практике, Cheatsheet. Не добавлять новый тип без явного утверждения пользователя. Центр структуры — Technique, а не Tool.

## No duplication

Перед созданием заметки искать существующую сущность по имени и смыслу. Если она уже существует, дополнять её и связывать wikilink. Одна идея должна иметь одно основное место хранения.

## Course independence

TryHackMe, Hack The Box и PortSwigger — источники практики, но не taxonomy Vault. Постоянные знания выносить в Concept, Technique и Tool.

## Commands require context

Не добавлять бессмысленные списки команд. Практический материал оформлять как Goal → Action → Evidence → Interpretation → Next Step. Объяснять ожидаемый сигнал, его смысл и дальнейшее решение.

## Preserve human knowledge

Не удалять пользовательские observations, mistakes, conclusions и interpretations без явной причины. При реорганизации сохранять исходный смысл и ссылки.

## Minimal architecture

Не добавлять плагины, frameworks, dependencies, новые Properties или типы сущностей без реальной необходимости. Vault должен оставаться обычной переносимой Markdown-директорией.

## Properties and naming

Соблюдать `docs/Conventions.md`. Использовать базовые поля `type`, `domain`, `techniques`, `status`, `confidence`, `source`. Не создавать случайные префиксы, UUID, ненужные даты и альтернативные имена сущности.

## Safety

Практические security-примеры допустимы только для labs, CTF, owned systems и explicitly authorized environments. Использовать placeholders `TARGET`, `http://TARGET/` и `/path/`; не заменять их реальными внешними targets. Не сохранять credentials, tokens и другие secrets.

## Validation

После структурных изменений запускать `python scripts/validate_kb.py`. Validator read-only; не изменять заметки автоматически для сокрытия ошибок.
