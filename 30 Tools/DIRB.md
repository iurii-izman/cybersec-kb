---
type: tool
domain:
  - web
techniques:
  - "[[Content Discovery]]"
status: practiced
confidence: 2
source:
  - tryhackme
---

# DIRB

## Что это

DIRB — CLI-инструмент для dictionary-based Web Content Discovery, который проверяет кандидаты из [[Wordlists]] по заданному base URL.

## Для чего нужен

Ищет существующие или скрытые directories, files, paths и endpoints в рамках [[Content Discovery]].

## Когда использовать

Когда `http://TARGET/` доступен, активная проверка разрешена, а passive discovery не дал полной картины.

## Связанные техники

- [[Content Discovery]]
- [[Web Enumeration]]

## Базовый синтаксис

```bash
dirb http://TARGET/ [wordlist]
```

## Основные команды

### Выполнить базовый поиск путей

**Goal:** найти неочевидные ресурсы учебного web-приложения.

**Action:**

```bash
dirb http://TARGET/
```

**Evidence:** строки с candidate URL, [[HTTP Status Codes|status code]] и размером response.

**Interpretation:** отличающийся status или размер делает путь кандидатом, но не подтверждает его назначение или безопасность.

**Next step:** вручную запросить полезный path, проверить headers/body и сопоставить с baseline отсутствующего пути.

### Использовать выбранную wordlist

**Goal:** сузить поиск под контекст приложения.

**Action:**

```bash
dirb http://TARGET/ /path/to/wordlist.txt
```

**Evidence:** результаты только для кандидатов из выбранного файла.

**Interpretation:** отсутствие находок говорит лишь о текущем списке и настройках, а не об отсутствии скрытого контента.

**Next step:** проверить корректность URL и baseline; расширять список только при обоснованной гипотезе.

### Найти скрытые страницы FakeBank

**Goal:** найти скрытые страницы учебного приложения FakeBank, отсутствующие в обычной навигации.

**Action:**

```bash
dirb http://fakebank.thm
```

**Evidence:**

- `http://fakebank.thm/images`
- `http://fakebank.thm/bank-transfer`

**Interpretation:** web-приложение может содержать доступные пути, не представленные ссылками в UI, и [[Content Discovery]] позволяет обнаруживать такие ресурсы. `/bank-transfer` представляет больший интерес для дальнейшего анализа как функциональный endpoint приложения, но само обнаружение endpoint ещё не является доказательством vulnerability.

**Next step:** открыть найденный endpoint и исследовать его назначение и поведение в рамках учебной лаборатории.

## Важные параметры

| Параметр | Назначение |
|---|---|
| `-X .ext` | Проверять заданные расширения, если это оправдано технологией |
| `-r` | Отключить recursive search и ограничить текущий проход |

## Как читать результат

Сравнивать status code, URL и размер. Redirect требует проверки `Location`; `403` может указывать на существующий закрытый ресурс; одинаковые `200` для случайных путей могут быть custom 404.

## Важные моменты

- Сначала установить baseline для несуществующего пути.
- Подбирать [[Wordlists]] по цели.
- Контролировать нагрузку и scope.
- DIRB — content discovery/scanning tool, а не vulnerability scanner; найденный endpoint является объектом дальнейшего исследования.
- В уроке использовалась терминология `dirbuster`, при этом фактически выполнялась команда `dirb`; в этой базе практический evidence относится к DIRB.

## Типичные ошибки

- Считать каждую строку подтверждённой находкой.
- Игнорировать trailing slash, redirects и custom error pages.
- Начинать с чрезмерно большого списка.

## Альтернативы

- [[DirBuster]] — GUI-инструмент для той же основной техники.

## Где использовал

- [[THM - Offensive Security Intro]] — Task 3, поиск скрытых страниц FakeBank.
- [[THM - Content Discovery Example]] — example / seed, без реального сканирования.

## Что запомнить

- DIRB реализует технику, но не заменяет интерпретацию HTTP.
- Нулевой результат ограничен выбранной wordlist и настройками.

## Проверка себя

- Что является входом DIRB?
- Как отличить candidate от подтверждённого ресурса?
- Зачем нужен not-found baseline?
- Какая техника стоит за инструментом?
