# CyberSec KB v0.1 — First Field Test Audit

## Scope

Аудит проверяет фактическую пригодность минимальной модели `Concept → Technique → Tool ← Lab` после трёх реальных TryHackMe Labs. Это read/analyze/report review: knowledge notes, Properties, templates, validator и архитектура не изменялись.

Проверены полностью `AGENTS.md`, `README.md`, `Home.md`, `docs/Conventions.md`, исходное ТЗ, четыре templates, все 24 knowledge notes и Git history трёх field-evidence commits.

## Current State

- Baseline HEAD до аудита: `078393f327ed1524f50414499fdc9b449aabe6ab` (`Add THM Linux Fundamentals Pt1 field evidence`).
- Ветка `main` совпадала с `origin/main`; `git pull --ff-only origin main` не получил новых изменений.
- Knowledge notes: 24 — 8 Concepts, 6 Techniques, 6 Tools, 4 Labs. Cheatsheets отсутствуют.
- Templates: 4.
- Mastery distribution: `new / confidence 1` — 7; `learned / confidence 2` — 7; `practiced / confidence 2` — 10. Других комбинаций нет.
- Growth: 10 → 19 → 24 knowledge notes. Рост связан с самостоятельными reusable entities, а не с копированием структуры Room.
- Baseline checks: 53 unit tests PASS; validator PASS (`24 knowledge notes and 4 required templates`); compile PASS; `git diff --check` PASS.

## Real Labs Reviewed

### REAL FIELD EVIDENCE

1. `THM - Offensive Security Intro` — конкретная практика DIRB: команда и найденные FakeBank paths `/images` и `/bank-transfer` сохранены как evidence.
2. `THM - Search Skills` — общая техника research подтверждена MAN lookup и GitHub repository research; Shodan и VirusTotal честно оставлены на уровне lesson/simulation learning.
3. `THM - Linux Fundamentals (Pt1)` — Room completed 100%; интерактивная навигация и search отражены как bounded practice, а operators — как learned material без выдуманных user-level outputs.

### SEED / EXAMPLE

`THM - Content Discovery Example` — демонстрационный seed. Он явно помечен как example, имеет `status: new`, `confidence: 1`, `source: other`, не содержит результатов сканирования и не учитывается как реальная практика.

## Knowledge Graph Summary

Фактические основные ветки:

```text
THM - Offensive Security Intro
  → DIRB
  → Content Discovery
      → HTTP / HTTP Status Codes / Wordlists
      → DIRB / DirBuster
      → Web Enumeration (broader context, not practiced by this Lab)
```

```text
THM - Search Skills
  → Security Information Research
      → CVE / CVSS / Proof of Concept / Man Pages
      → Shodan / VirusTotal / GitHub
```

```text
THM - Linux Fundamentals (Pt1)
  → Linux Shell
  → Linux Filesystem Navigation
  → Linux File and Text Search
  → Shell Command Chaining and Redirection
  → Man Pages (related/review only, not new evidence from this Room)
```

Status/confidence effects соответствуют evidence: DIRB, GitHub, Man Pages и четыре реально применённые Techniques получили `practiced / 2`; Shodan, VirusTotal, CVE, CVSS, Proof of Concept, Linux Shell и shell operators остались `learned / 2`; seed-only entities остались `new / 1`.

## What Works

- Technique остаётся центром: Tools объясняют задачу и ссылаются на Technique, а Labs не превращают инструменты в taxonomy.
- Course independence выдержана: reusable knowledge вынесено в Concepts, Techniques и Tools; Room-specific completion, FakeBank evidence и границы сохранённых результатов остаются в Labs.
- Evidence discipline не допускает mastery inflation: completion не превращает lesson examples в personal results, упоминание Tool не становится `practiced`.
- Команды Linux сохранены внутри задач с Goal/Action/Evidence/Interpretation/Next Step. Отдельные Tool notes для `ls`, `cd`, `grep`, `find` не понадобились.
- Manual `Home.md` при 24 notes остаётся короткой полной картой всех Concepts, Techniques, Tools и Labs.
- Validator и ручная read-only проверка подтверждают целостность графа.

## Observed Pain Signals

| Signal | Observed? | Evidence | Severity |
|---|---|---|---|
| Classification ambiguity | YES | `Man Pages` находится на границе Concept и information resource; `Security Information Research` охватывает несколько классов sources | LOW |
| Duplication | YES | Bounded practice evidence частично повторяется между Lab и Tool, особенно FakeBank paths в DIRB и `exploit.py` в GitHub | LOW |
| Processing cost | YES | Search Skills потребовал 9 новых knowledge notes, Linux Fundamentals — 5; это breadth-heavy capture, но все entities reusable и validator friction не наблюдался | LOW |
| Navigation friction | NO | Home индексирует все 24 notes; Lab ↔ permanent knowledge и Technique ↔ Tool routes работают; orphans отсутствуют | NONE |
| Forgotten knowledge | NO | Нет фактического evidence, что каталогизированное знание уже забыто | NONE |
| Repeated workflows | NO | Ни один одинаковый многошаговый workflow не повторён в нескольких реальных Labs | NONE |

Ни один observed signal пока не демонстрирует architectural pain.

## Taxonomy Audit

### Concept vs Technique

| Entity | Result | Reasoning |
|---|---|---|
| Man Pages | AMBIGUOUS | Это существующая documentation system/resource (`что это`), поэтому Concept защищаем; одновременно использование man pages является методом research. Текущая note не формулирует отдельную задачу, поэтому MISCLASSIFIED не доказано. |
| Linux Shell | CLEAR | Описывает существующий interpreter/context и механизм command execution; задачи вынесены в Linux Techniques. |
| Security Information Research | CLEAR | Формулирует цель: найти, проверить и сопоставить информацию; sources и services являются средствами. |
| Linux Filesystem Navigation | CLEAR | Формулирует операционную задачу ориентации и перехода по filesystem. |
| Linux File and Text Search | CLEAR | Формулирует задачу поиска entries или content и выбор метода по искомому объекту. |
| Shell Command Chaining and Redirection | CLEAR | Формулирует задачу управления execution dependency и output routing; operators являются методами. |

Ни одна entity не получила доказанную оценку MISCLASSIFIED.

### Technique vs Tool

Разделение выдерживается:

- `Content Discovery` задаёт цель и интерпретацию; DIRB и DirBuster — два разных средства её выполнения.
- `Security Information Research` начинается с research question; Shodan, VirusTotal и GitHub дают разные виды evidence.
- Linux Techniques хранят базовые commands непосредственно внутри осмысленного workflow.

Решение **не создавать Tool notes для `ls`, `cd`, `pwd`, `cat`, `find`, `grep`, `echo` и shell operators было правильным**. Текущий материал краток, связан с конкретными задачами и быстро сравнивает decision points (`find` vs `grep`, `>` vs `>>`). Отдельные Tool notes добавили бы navigation hops и metadata decisions без самостоятельного knowledge payoff.

## Granularity and Duplication

### Granularity

| Entity | Result | Reasoning |
|---|---|---|
| CVE | GOOD GRANULARITY | Независимо объясняет identifier и предотвращает смешение с score/exploit. |
| CVSS | GOOD GRANULARITY | Независимо объясняет severity context и отделяет его от identification. |
| Proof of Concept | GOOD GRANULARITY | Имеет самостоятельную ценность для provenance/safety reasoning вне Room. |
| Man Pages | GOOD GRANULARITY | Reusable для многих commands и хранит подтверждённый documentation lookup. |
| Linux Shell | GOOD GRANULARITY | Даёт общий context для нескольких Linux Techniques без копирования основы. |
| Security Information Research | POSSIBLY TOO BROAD | Объединяет infrastructure search, artifact reputation, vulnerability research, documentation и repositories. Пока их связывает один стабильный question-first/cross-check workflow и только одна реальная Lab, поэтому splitting не оправдан. |
| Shell Command Chaining and Redirection | GOOD GRANULARITY | Operators образуют связную задачу управления execution/output и имеют общие risks. |

Слишком узких доказанных notes нет. Новые entities имеют самостоятельную ценность вне конкретной Room.

### Semantic duplication

| Pair / area | Result | Reasoning |
|---|---|---|
| HTTP vs HTTP Status Codes | overlap but justified | HTTP хранит request/response model; codes — отдельную интерпретацию response signal. |
| DIRB vs DirBuster | overlap but justified | Разные CLI/GUI tools одной Technique; общая логика принадлежит Content Discovery. |
| CVE vs CVSS | no meaningful overlap | Identifier и severity context разделены явно. |
| Linux Shell vs Man Pages | no meaningful overlap | Runtime interaction context и documentation resource решают разные вопросы. |
| Content Discovery vs Web Enumeration | overlap but justified | Content Discovery — вложенный этап более широкой Web Enumeration. |
| Security Information Research vs OSINT concepts | no meaningful overlap | В Vault нет конкурирующей OSINT entity; текущая Technique организует sources вокруг задачи. |

Одно factual evidence частично поддерживается в двух местах: FakeBank results есть в Lab и DIRB, а repository result `exploit.py` — в Lab и GitHub. Это полезно для recall из обоих направлений, но создаёт небольшой maintenance risk. Повторение bounded и пока не расходится. Linux Lab перечисляет covered commands, тогда как Techniques хранят reusable meaning; это summary/detail, а не конкурирующие canonical explanations.

## Navigation Audit

- Из каждой реальной Lab можно сразу выйти к permanent knowledge через разделы Concepts/Techniques/Tools и body links.
- Technique показывает подходящие Tools. В Linux Techniques отсутствие Tool links является осознанным: command knowledge уже встроено в задачу.
- Каждый Tool через Property и body объясняет поддерживаемую Technique; все шесть Tools имеют существующие Technique links.
- Tools с field evidence ссылаются на соответствующие Labs; Techniques также перечисляют реальные Labs.
- `Home.md` содержит все 8 Concepts, 6 Techniques, 6 Tools и 4 Labs, выделяет текущие направления и seed. При 24 notes он не перегружен и **manual Home работает хорошо**.
- Orphan knowledge notes нет. Read-only search не обнаружил unresolved wikilinks в `Home.md` или knowledge notes; accidental duplicate canonical filenames отсутствуют.
- Важных one-way links, мешающих навигации, не найдено. Backlinks дополняют явные двусторонние routes.

Вывод: Home is still useful; Dataview для навигации не нужен.

## Evidence and Mastery Audit

| Real Lab | Assessment | Evidence discipline |
|---|---|---|
| THM - Offensive Security Intro | strong | Полные Goal/Action/Evidence/Interpretation/Next Step, конкретные FakeBank results, endpoint не объявлен vulnerability. |
| THM - Search Skills | strong | Каждая task отделяет lesson evidence от personal result; MAN и GitHub practice bounded; fictional CVE явно маркирован. |
| THM - Linux Fundamentals (Pt1) | acceptable | Структура полная и отсутствие exact outputs честно зафиксировано; navigation/search backed by interactive completion, operators не повышены до practiced. Recall улучшится после будущего concrete result. |

Invented evidence не найдено:

- FakeBank содержит конкретные наблюдённые paths и не делает лишнего vulnerability claim.
- Search Skills не приписывает пользователю Shodan targets/results, VirusTotal scans или реальную `CVE-2026-1337`.
- Linux Fundamentals не выдумывает username, paths, listings, flag, grep output или result redirection.

Room completion не превращено в mastery всех упомянутых Tools: Shodan/VirusTotal остаются `learned`, operators остаются `learned`, Web Enumeration остаётся `new`. Tool mention не равен practiced.

### Status / confidence

`status` и `confidence` концептуально различаются: status фиксирует тип evidence, confidence — субъективную готовность. Фактически модель пока использует только три согласованные пары (`new/1`, `learned/2`, `practiced/2`), поэтому независимость шкал ещё не проявилась в распределении, но полезность уже видна: `practiced/2` честно означает первую практику без уверенного самостоятельного владения.

Противоречивых комбинаций, mastery inflation и notes, для которых невозможно честно выбрать status, не найдено. Текущей шкалы достаточно; новые statuses не нужны.

## Source and Domain Audit

### Source semantics

Распределение: `tryhackme` — 17 notes, `other` — 5, `documentation` — 2.

В текущей реализации `source` означает **происхождение знания note**, а не источник personal mastery evidence. Это соответствует `docs/Conventions.md` и видно по контрасту:

- CVE/CVSS имеют `source: tryhackme`, хотя их mastery остаётся `learned`.
- HTTP/HTTP Status Codes имеют `source: documentation`, но `status: new`.
- DIRB имеет `source: tryhackme` и `status: practiced`; совпадение source и evidence здесь ситуативно, а не новая семантика поля.

Семантического конфликта в данных пока нет. Есть только low-level risk неверного прочтения поля без Conventions; actual practice provenance уже выражено status, Lab links и текстом. Новое Property не оправдано.

### Domains

Используются `web`, `network`, `linux`, `osint`, `defensive-security`, `general`. Три `general` notes — CVE, CVSS и Proof of Concept — действительно cross-domain и хорошо находятся через `Security Information Research`, взаимные links и Home.

`general` сейчас не создаёт search/navigation pain. Более специфичный domain потребовал бы преждевременного taxonomy decision и не улучшил бы текущий маршрут. Fallback полностью приемлем.

## Maintenance Cost

Timing не записан, поэтому оценка основана только на Git proxies.

| Room | Files / decisions | Cost |
|---|---|---|
| Offensive Security Intro | 1 Lab создана; Content Discovery, DIRB и Home обновлены; одна основная mastery chain | LOW |
| Search Skills | 1 Lab + 4 Concepts + 1 Technique + 3 Tools созданы; Home обновлён; несколько раздельных mastery decisions | HIGH for this Room |
| Linux Fundamentals (Pt1) | 1 Lab + 1 Concept + 3 Techniques созданы; Home обновлён; commands сгруппированы без Tool inflation | ACCEPTABLE |

Search Skills был breadth-heavy, но его девять новых knowledge notes не являются walkthrough fragments: каждая покрывает reusable entity. Linux Room добавил пять notes, сохранив commands внутри трёх задач. Общие explanations не приходится копировать во все Labs. Tests/validator проходят без изменений и не показывают validator friction.

Итоговая стоимость процесса — **ACCEPTABLE**. Один дорогой по file count урок является watchpoint, но трёх Labs недостаточно, чтобы признать capture непропорционально тяжёлым или требующим automation.

Growth 10 → 19 → 24 классифицируется как **healthy reusable growth**, а не early note inflation.

## Memory / Recall Fitness

- Если через месяц забыт DIRB: Tool note быстро восстанавливает what/when, syntax, wordlist choice, expected signals, interpretation, common errors и FakeBank practice.
- Если забыта разница `find`/`grep`: одна Technique прямо противопоставляет filesystem entry search и content search, даёт commands, evidence и decision workflow.
- Если забыты Shodan filters: Tool note хранит filters и их назначение, limits interpretation и ссылку на Room. Она честно не содержит concrete practiced result, потому что его не было.

Для всех трёх cases можно восстановить `what`, `when`, `how`, `how to interpret` и `where learned/practiced`. Недостаток конкретного Shodan result и Linux outputs — content evidence gap, уже выраженный в Next Step, а не missing architectural capability.

**CURRENT MODEL SUFFICIENT.** Фактического forgotten-knowledge signal пока нет; Anki trigger отсутствует.

## Repeated Workflow Check

- Web Enumeration → Content Discovery: Content Discovery реально практиковался только в Offensive Security Intro; seed не считается repetition.
- Security Information Research: один набор related tasks внутри одной реальной Room, не повторение workflow в нескольких Labs.
- Linux navigation/search: один Linux Room; navigation и search являются соседними задачами, но последовательность ещё не повторена в другой Lab.

Критерий повторения одной последовательности в нескольких реальных Labs не выполнен.

**NO CHEATSHEET TRIGGER YET.** Procedures и Playbooks также не оправданы.

## Seed Assessment

**KEEP FOR NOW.**

Seed всё ещё полезен как reference implementation: он демонстрирует not-found baseline, отсутствие invented evidence и полный Goal → Action → Evidence → Interpretation → Next Step до появления реального result. Он ясно отделён от field evidence и не повышает mastery.

Его уникальная ценность уменьшается по мере появления качественных реальных Labs. RETIRE LATER можно обсуждать только когда реальные Labs полностью заменят его onboarding/reference role или он начнёт создавать navigation confusion; сейчас этого нет.

## v0.2 Trigger Check

| Trigger | Verdict | Evidence |
|---|---|---|
| Dataview | NOT TRIGGERED | Manual Home полностью покрывает 24 notes; orphans/ghost links/navigation friction отсутствуют. |
| Anki / review | NOT TRIGGERED | Нет evidence, что хорошо каталогизированное знание демонстративно забывается. |
| Procedures / Playbooks | NOT TRIGGERED | Одинаковый multi-step workflow не повторён в нескольких реальных Labs. |
| AI ingestion | NOT TRIGGERED | Search Skills был breadth-heavy, но нет recorded burden, repeated stable capture pattern или quality failure. |
| MITRE / OWASP mapping | NOT TRIGGERED | Ни одна Lab или navigation task не требует professional-framework mapping. |

## Recommendations

### NOW

Continue using v0.1 unchanged through Labs 4–5. В следующих Labs продолжать сохранять concrete non-sensitive outputs там, где они доступны, не повышая lesson-only evidence до `practiced`.

### LATER IF TRIGGERED

- Если `Security Information Research` накопит разные повторяющиеся workflows, повторно оценить его granularity; не split по одному широкому уроку.
- Если bounded evidence начнёт расходиться между Lab и Tool, определить одно canonical detail location и оставить в другом месте краткую ссылку.
- Если manual Home начнёт создавать фактическую navigation friction, сначала упростить ручную карту; tooling рассматривать только после подтверждённой боли.
- Если одна последовательность повторится в нескольких реальных Labs, оценить короткий Cheatsheet; Procedure/Playbook обсуждать только если Technique notes перестанут отражать workflow.
- Если появится фактическое забывание хорошо оформленных notes, отдельно оценить review mechanism.

### DO NOT DO YET

Не добавлять Dataview, Anki, Procedures/Playbooks, AI ingestion, dashboards, MITRE/OWASP mappings, новые Properties, entity types, domains или source tokens. Не split/merge/rename notes и не удалять seed на основании этого аудита.

## Deferred Ideas

Зафиксированы как watchpoints, не backlog:

- Concept/resource boundary у `Man Pages`.
- Breadth `Security Information Research` после одного курса.
- Bounded duplication конкретного practice evidence между Lab и Tool.
- Будущая onboarding value seed после накопления дополнительных реальных Labs.

Ни одна идея не требует implementation plan сейчас.

## Final Verdict

**V0_1_HEALTHY_WITH_MINOR_ISSUES**

Минимальная модель работает на трёх разных типах практики: web discovery, information research и Linux fundamentals. Она сохраняет course-independent knowledge, удерживает Technique в центре, различает learned/practiced evidence, обеспечивает ручную навигацию и не вынуждает создавать Tool notes для каждой команды.

Minor issues — пограничная классификация Man Pages, потенциальная широта одной research Technique и небольшое повторение bounded evidence — локальны, не вызывают observable user pain и не оправдывают architecture change. Основное действие: продолжить Field Test без изменения v0.1.
