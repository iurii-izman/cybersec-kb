---
type: lab
domain:
  - web
techniques:
  - "[[Web Enumeration]]"
  - "[[Content Discovery]]"
status: new
confidence: 1
source:
  - other
---

# THM - Content Discovery Example

> [!IMPORTANT]
> **Example / seed only.** Это демонстрация структуры Lab, а не запись о реально пройденной TryHackMe Room. Ниже нет результатов реального сканирования.

## Цель лаборатории

Показать, как связать concepts, techniques и tools и как документировать практический шаг без выдуманных результатов.

## Что было новым

### Concepts

- [[HTTP]]
- [[HTTP Status Codes]]
- [[Wordlists]]

### Techniques

- [[Web Enumeration]]
- [[Content Discovery]]

### Tools

- [[Nmap]]
- [[DIRB]]
- [[DirBuster]]

## Практика

### Шаг 1 — подтвердить web-сервис

**Goal:** определить, доступен ли web-сервис на выданном учебном `TARGET`.

**Action:**

```bash
nmap -sV -p PORT TARGET
```

**Evidence:** в реальной Lab сюда записывается фактическое состояние порта и признаки сервиса. Для seed результата нет.

**Interpretation:** продолжать web enumeration можно только после подтверждения web-сервиса; предполагаемую версию нужно проверять отдельно.

**Next step:** сформировать корректный base URL или остановиться и проверить target/scope.

### Шаг 2 — установить baseline отсутствующего пути

**Goal:** понять, как приложение отвечает на заведомо случайный path.

**Action:** отправить безопасный запрос к `http://TARGET/path-that-should-not-exist` в рамках лаборатории.

**Evidence:** в реальной Lab сохранить status code, response size и важные headers без credentials или tokens. Для seed значения не придуманы.

**Interpretation:** этот response станет baseline для отделения candidates от custom error pages.

**Next step:** выбрать небольшую релевантную [[Wordlists|wordlist]] и выполнить контролируемый поиск.

### Шаг 3 — выполнить content discovery

**Goal:** найти candidate resources, отсутствующие в обычной навигации.

**Action:**

```bash
dirb http://TARGET/ /path/to/wordlist.txt
```

**Evidence:** в реальной Lab сюда переносятся только наблюдаемые candidate URLs, [[HTTP Status Codes|status codes]] и размеры. В seed находки отсутствуют.

**Interpretation:** candidate требует сравнения с baseline и ручной проверки; один код ответа не подтверждает назначение ресурса.

**Next step:** проверить релевантные candidates по одному и связать подтверждённый вывод с [[Content Discovery]].

## Ошибки и сложности

- Placeholder: записать, как custom error page, redirect или неверная wordlist повлияли на результат.
- Не копировать walkthrough; сохранять собственное наблюдение и решение.

## Что понял после практики

- Seed показывает ожидаемый формат. Личный вывод появится только после реальной практики.

## Что повторить

- [[HTTP Status Codes]]
- Выбор [[Wordlists|wordlist]] под контекст.
- Различие между evidence и interpretation.

## Итог

Демонстрационная цепочка навигации: Lab → [[DIRB]] / [[DirBuster]] → [[Content Discovery]] → [[HTTP Status Codes]]. После реальной комнаты этот seed не следует выдавать за личный опыт; нужно создать или заполнить фактическую Lab-заметку.
