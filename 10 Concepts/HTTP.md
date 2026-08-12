---
type: concept
domain:
  - web
  - network
techniques:
  - "[[Web Enumeration]]"
  - "[[Content Discovery]]"
status: learned
confidence: 2
source:
  - documentation
---

# HTTP

## Что это

HTTP — протокол обмена сообщениями между клиентом и сервером по модели request/response. В security-практике важны метод, путь, headers, body и ответ сервера.

## Зачем это нужно

Понимание HTTP позволяет отличать поведение приложения от поведения сети, осмысленно исследовать endpoints и читать результаты web-инструментов.

## Как это работает

Клиент отправляет запрос с методом и ресурсом, например `GET /path/`. Сервер отвечает status code, headers и при необходимости body. Значение кода раскрывается в [[HTTP Status Codes]].

## Пример

```http
GET /path/ HTTP/1.1
Host: TARGET
```

Ответ `200`, `301`, `403` или `404` — evidence, который нужно интерпретировать в контексте приложения, а не как готовый вывод.

## Связано с

- [[HTTP Status Codes]]
- [[Web Enumeration]]
- [[Content Discovery]]

## Что важно запомнить

- Request и response нужно рассматривать вместе.
- Один status code не доказывает наличие или отсутствие уязвимости.
- Paths, headers и методы могут менять поведение сервера.

## Проверка себя

- Из каких частей состоит HTTP-запрос?
- Что сообщает response status?
- Почему одинаковый path может отвечать по-разному?
