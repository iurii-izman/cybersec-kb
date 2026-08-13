---
type: technique
domain:
  - web
techniques: []
status: practiced
confidence: 2
source:
  - tryhackme
---

# Content Discovery

## Цель

Найти ресурсы web-приложения, которые не видны через обычную навигацию: directories, files, backup-файлы, panels и endpoints.

## Когда применяется

В рамках [[Web Enumeration]], когда web-сервис уже подтверждён, scope известен и нужно расширить карту приложения.

## Что требуется на входе

- Разрешённый base URL, например `http://TARGET/`.
- Ожидаемое поведение [[HTTP]] для существующего и отсутствующего пути.
- Подходящие [[Wordlists]] для активного поиска.

## Основные методы

### Passive

- Изучить ссылки, HTML, JavaScript, `robots.txt`, `sitemap.xml` и доступную документацию.

### Active

- Dictionary-based discovery.
- Fuzzing имён и расширений.
- Контролируемый recursive discovery после подтверждения полезного пути.

## Инструменты

- [[DIRB]]
- [[DirBuster]]

## Типовой workflow

```text
Authorized base URL + relevant wordlist
  ↓
Establish not-found baseline
  ↓
Run controlled discovery
  ↓
Compare status, size and redirects
  ↓
Manually verify useful candidates
```

## Интерпретация результата

- `200` требует проверки содержимого.
- `301`/`302` требует проверки destination.
- `403` может подтверждать существование закрытого ресурса.
- `404` и похожий body обычно снижают приоритет кандидата.

Подробнее: [[HTTP Status Codes]].

## Что может пойти не так

- Custom 404 возвращает `200` для любого пути.
- Нерелевантная wordlist даёт много шума.
- Высокая скорость создаёт нагрузку или rate limiting.
- Redirect loop принимается за найденный контент.

## Labs

- [[THM - Offensive Security Intro]] — скрытые страницы FakeBank найдены с помощью [[DIRB]].
- [[THM - Content Discovery Example]] — example / seed

## Проверка себя

- Что именно можно искать?
- Чем passive discovery отличается от active?
- Какие признаки нужно сравнивать кроме status code?
- Как вручную подтвердить найденный path?
