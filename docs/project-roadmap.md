# Six project blueprints

**Status: planned concepts — no implementation is included for these six ideas.**

These plans explore CSE, AI, embedded control, and defensive security. Stacks are proposals, not claims of current expertise. Each project should finish with runnable source, setup instructions, an architecture diagram, meaningful checks, screenshots or a demo, and documented limitations.

## 1. Hassan AI — Personal Agent

**Goal:** A Bangla/English assistant that answers questions from personal notes and proposes useful task actions.

**Distinctive idea:** Show a preview and an action history so users can see what the agent intends to do and what it actually did.

**First version:** bilingual text chat; import text or Markdown notes; retrieve relevant passages with citations; draft task plans; save approved tasks; retain a local action log and explain unsupported answers.

**Proposed stack:** Python, FastAPI, SQLite, a simple web UI, and a replaceable model adapter. Mock model responses for tests; real model access requires a separately configured service or local model.

**Architecture:** browser → assistant API → note retrieval / task tools → local database. The model proposes tool inputs; the application validates them and requests review for writes.

**Milestones:** notes and tasks without AI → retrieval with citations → bilingual chat → action previews and permission checks → recorded demo.

**Completion checks:** answer fixed questions from sample notes; flag unsupported questions; cancel a proposed task without writing; save an approved task once; demonstrate that note text cannot grant tool permissions.

**Portfolio evidence:** sample notes, an evaluation sheet, action-flow diagram, and bilingual walkthrough.

## 2. GestureDrive — Gesture-Controlled Vehicle

**Goal:** Control a small, low-speed robot car through deliberate hand gestures.

**Distinctive idea:** Display confidence and command latency, and stop automatically when tracking or communication is lost.

**First version:** webcam recognition for stop, forward, left, and right; stable gestures across several frames; live gesture and command display; explicit arm/disarm; physical stop control; a microcontroller timeout that stops motors. Start in a simulator.

**Proposed stack:** Python, OpenCV, a hand-landmark library, an ESP32 or Arduino-compatible controller, motor driver, and robot chassis.

**Architecture:** webcam → gesture classifier → command validator → serial/radio link → microcontroller watchdog → motor driver.

**Milestones:** gesture samples → on-screen simulator → timeout and stop checks → hardware link → controlled low-speed course demo.

**Completion checks:** ambiguous gestures do not start motion; disarmed mode ignores movement commands; lost camera input or link stops the robot within the configured timeout; record latency and recognition errors.

**Portfolio evidence:** wiring diagram, bill of materials, gesture mapping, simulator recording, and hardware demo. This is a hobby robot concept, not a road-vehicle control system.

## 3. ShieldLab — Web Security and WAF Environment

**Goal:** Make web application firewall decisions understandable in a reproducible local lab.

**Distinctive idea:** Compare lab traffic before and after filtering, explain triggered rules, and document false positives.

**First version:** containerized sample app behind a WAF proxy; repeatable benign requests and labelled security fixtures; dashboard for rule ID, action, timestamp, and redacted context; detection-only and blocking modes; a documented false-positive tuning exercise.

**Proposed stack:** Docker Compose, Nginx, ModSecurity with OWASP Core Rule Set, a Python sample app, and a lightweight report UI. Confirm supported component versions during implementation.

**Architecture:** local test client → WAF proxy → sample app; audit logs → parser → dashboard. Keep the sample app bound to the lab environment.

**Milestones:** repeatable baseline → detection-only rules → normalized events → blocking comparison → one documented tuning change.

**Completion checks:** legitimate fixtures stay usable; selected malicious fixtures produce expected lab events; reports explain decisions; logs omit secrets; a fresh setup reproduces results. Report false positives and missed cases.

**Portfolio evidence:** lab diagram, labelled fixtures, before/after report, and reproducible walkthrough. Passing fixtures does not establish protection against every attack.

## 4. SOC Lens — Investigation Dashboard

**Goal:** Turn educational security events into a timeline that helps a learner investigate suspicious activity.

**Distinctive idea:** Connect alerts to their underlying evidence and an analyst explanation.

**First version:** import synthetic SSH and web-access logs; normalize timestamps; preserve source-line references; group repeated authentication failures; filter by time, host, and event type; add analyst notes; export Markdown incident reports.

**Proposed stack:** Python, SQLite, Streamlit, and reusable parsing logic from the existing security log analyzer.

**Architecture:** offline sample logs → parsers → normalized events → detection rules → timeline and report.

**Milestones:** event schema → sample import → grouped alerts → timeline → evidence links and export.

**Completion checks:** known samples produce expected counts; malformed lines are reported; timezone handling is consistent; threshold changes update alerts; exported reports retain evidence references.

**Portfolio evidence:** synthetic incident story, screenshots, sample report, rule tests, and parsing limitations. Start with offline data before live log collection.

## 5. StudyForge — CSE Learning Companion

**Goal:** Help a student organize notes, practise concepts, and revisit topics over time.

**Distinctive idea:** Attach generated questions to source passages so users can check their basis.

**First version:** import Markdown notes by course/topic; create editable flashcards and questions from selected passages; link questions to notes; schedule reviews; record self-reported confidence; export notes, cards, and progress.

**Proposed stack:** Python, FastAPI, SQLite, browser UI, and optional model adapter. Manual card creation remains available without AI access.

**Architecture:** notes → passage selection → question draft → user review → card store → review scheduler.

**Milestones:** notes and manual cards → review queue → source-linked drafts → edit/reject flow → import/export round trip.

**Completion checks:** rejected drafts stay out of the queue; deleting notes handles linked cards visibly; dates match the documented scheduling rule; exports can be reimported; generated answers remain editable.

**Portfolio evidence:** original sample course, review-flow diagram, source-linked questions, and user walkthrough. Generated study material may contain errors.

## 6. Integrity Watch — File Change Monitor

**Goal:** Identify added, modified, and removed files using a saved hash baseline.

**Distinctive idea:** Explain differences and keep baseline updates separate from scans so changes are not silently accepted.

**First version:** SHA-256 baseline with relative paths; compare additions, deletions, and changes; configurable exclusions; unreadable-file reporting; JSON and Markdown exports; explicit baseline replacement command.

**Proposed stack:** Python standard library, CLI, and JSON storage; a desktop view can follow later.

**Architecture:** chosen folder → bounded traversal → streaming hashes → baseline comparison → report. Define symlink handling and avoid following links outside the chosen folder.

**Milestones:** baseline creation → comparison → errors and exclusions → exports → deliberate change demonstration.

**Completion checks:** detect changed contents even at the same file size; distinguish additions and deletions; report unreadable files; scans leave the baseline unchanged; document baseline tampering as a limitation.

**Portfolio evidence:** reproducible sample folder, before/after reports, edge-case checks, and an explanation of hashing. A hash change alone is not a malware diagnosis.

## Suggested build order

1. **Integrity Watch:** a bounded Python project with clear checks.
2. **SOC Lens:** extend the existing log-analysis work.
3. **ShieldLab:** connect detection results to a local security environment.
4. **StudyForge:** practise a complete web app and data model.
5. **Hassan AI:** add retrieval and reviewable tool actions on that foundation.
6. **GestureDrive:** progress from simulator to embedded hardware.

This sequence is a proposal. Choose based on available hardware, time, and learning goals.
