---
type: tool
domain:
  - defensive-security
  - osint
techniques:
  - "[[Security Information Research]]"
status: learned
confidence: 2
source:
  - tryhackme
---

# VirusTotal

## Что это

VirusTotal — сервис исследования файлов, URLs, domains и file hashes с помощью агрегированных security-engine signals и связанного контекста.

## Для чего нужен

Помогает получить multi-engine consensus/signals, контекст о подозрительных файлах и ссылках и дополнительные threat-intelligence clues для [[Security Information Research]].

## Когда использовать

Когда есть suspicious artifact или indicator и нужен дополнительный источник evidence до формирования вывода.

## Связанные техники

- [[Security Information Research]]

## Объекты исследования

- file
- URL
- domain
- file hash

## Как читать результат

Несколько detections или других signals усиливают evidence, но требуют интерпретации в контексте. Отсутствие signal также не является абсолютной гарантией безопасности.

## Важные моменты

- VirusTotal result не равен абсолютной истине.
- В Room не сохранены конкретный hash, detection ratio, malware family или scan result, поэтому эта заметка их не приписывает пользователю.
- Эта заметка фиксирует learned, а не tool-level practical evidence.

## Где изучил

- [[THM - Search Skills]] — Task 3, lesson/simulation learning evidence.

## Что запомнить

- Рассматривать результат как набор signals.
- Не делать окончательный вывод по одному engine или одному источнику.
