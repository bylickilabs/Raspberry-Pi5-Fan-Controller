Thank you for your interest in contributing to the **Raspberry Pi Fan Controller (Tkinter)** project! This guide explains how to set up your environment, propose changes, and collaborate effectively.

### 1) Code of Conduct
Participation in this project is governed by our **[Code of Conduct](CODE_OF_CONDUCT.md)**. By contributing, you agree to follow its terms.

### 2) How you can contribute
- Bug fixes (UI glitches, sensor discovery issues, RPM/PWM reads/writes, localization)
- New features (dark mode, autostart tools, root-helper service, charts)
- Documentation improvements (README, troubleshooting, diagrams)
- Performance and robustness (error handling, retry logic, discovery)
- Packaging (systemd unit templates, `.desktop` files, udev rules examples)

Please open an **issue** before starting work on large features to align on scope and design.

### 3) Development setup
**Prerequisites** (Raspberry Pi OS Desktop):

```yarn
sudo apt update
sudo apt install -y python3 python3-tk xdg-utils
```

**Clone & run:**

```yarn
git clone https://github.com/<YOUR_ORG_OR_USER>/<YOUR_REPO>.git
cd <YOUR_REPO>
python3 fan.py           # read-only test
sudo python3 fan.py      # fan control (sysfs writes)
```

### 4) Branching & workflow
- Use feature branches from `main`: `feat/<short-name>`, `fix/<short-name>`, `docs/<short-name>`
- Keep PRs small and focused (one topic per PR)
- Reference related issues: `Fixes #123` / `Closes #123`

### 5) Commit messages (Conventional Commits)
Follow **Conventional Commits** format:
```
<type>(optional scope): <short summary>

[optional body]
[optional footer(s)]
```

**Types:** `feat`, `fix`, `docs`, `refactor`, `perf`, `test`, `build`, `chore`  
**Examples:**
- `feat(gui): add dark mode toggle`
- `fix(sysfs): fallback for pwm1_max absence`
- `docs(readme): add systemd unit example`

### 6) Code style & structure
- **Python 3.9+**, standard library only (no extra deps)
- UI **ASCII-safe** and **fully localized** (DE/EN keys in `LANG`)
- No hard-coded sysfs paths; always implement discovery with fallbacks
- Encapsulate file I/O in helpers (`s_read`, `s_write`)
- Guard root-only writes; read paths must not crash the UI
- Keep the GUI responsive: use `after()` loops, never block the main thread

### 7) Testing & manual checks
- Start without sudo: verify UI, temperature graph, CPU MHz, RAM
- Start with sudo: verify mode switching (Auto/25/50/100), PWM/CD writes
- If available, verify RPM readout; otherwise ensure `--`
- Test different intervals (`,` and `.` as decimal separators)
- Resize window; ensure controls remain visible

### 8) Submitting changes
1. Fork the repository and create your branch.
2. Make changes in small, clear commits.
3. Update docs if behavior or UI changes.
4. Run the app and verify in both non-root and root scenarios.
5. Open a Pull Request with:
   - What & why
   - Screenshots/GIFs for UI changes
   - Testing notes (environment, commands, observed results)
   - Related issue links

### 9) Reporting issues
For **bugs**, include:
- Environment: Pi model, OS version
- Start method (user vs sudo, autostart/systemd)
- Steps to reproduce
- Expected vs actual behavior
- Logs/tracebacks (as text)
- Output of:
  ```bash
  find /sys -name pwm1 2>/dev/null
  find /sys -name cooling_device\* 2>/dev/null
  ```

For **feature requests**, explain the user story and expected UX.

### 10) Security
Do not post secrets or sensitive paths. If you discover a security issue, contact the maintainer privately.

### 11) License
By contributing, you agree that your contributions will be licensed under the project's license.
[LICENSE](LICENSE)

<br>

---

<br>

Danke für dein Interesse, zum **Raspberry Pi Fan Controller (Tkinter)** beizutragen! Diese Anleitung erklärt Setup, Workflow und Qualitätsstandards.

### 1) Verhaltenskodex
Die Teilnahme unterliegt unserem **[Code of Conduct](CODE_OF_CONDUCT.md)**. Mit deinem Beitrag erklärst du dich mit diesen Regeln einverstanden.

### 2) Wobei du helfen kannst
- Bugfixes (UI, Sensor-Erkennung, RPM/PWM-Lesen/Schreiben, Übersetzung)
- Features (Dark Mode, Autostart-Tools, Root-Helper-Service, Charts)
- Dokumentation (README, Troubleshooting, Diagramme)
- Performance & Robustheit (Error Handling, Retry-Logik, Discovery)
- Packaging (systemd-Units, `.desktop`, udev-Regeln)

Bitte vor größeren Features ein **Issue** eröffnen, um Scope/Design abzustimmen.

### 3) Entwicklungsumgebung
**Voraussetzungen** (Raspberry Pi OS Desktop):
```bash
sudo apt update
sudo apt install -y python3 python3-tk xdg-utils
```
**Klonen & starten:**
```bash
git clone https://github.com/<YOUR_ORG_OR_USER>/<YOUR_REPO>.git
cd <YOUR_REPO>
python3 fan.py           # nur Lesen (Test)
sudo python3 fan.py      # volle Steuerung (Schreibzugriff auf sysfs)
```

### 4) Branching & Workflow
- Feature-Branches von `main`: `feat/<kurz>`, `fix/<kurz>`, `docs/<kurz>`
- PRs klein und fokussiert halten – ein Thema pro PR
- Verweise auf Issues: `Fixes #123` / `Closes #123`

### 5) Commit-Messages (Conventional Commits)
Nutze **Conventional Commits**:
```
<type>(optional scope): <kurze zusammenfassung>

[optional body]
[optional footer(s)]
```
**Types:** `feat`, `fix`, `docs`, `refactor`, `perf`, `test`, `build`, `chore`  
**Beispiele:**
- `feat(gui): dark mode toggler`
- `fix(sysfs): fehlertoleranz falls pwm1_max fehlt`
- `docs(readme): systemd user unit ergänzt`

### 6) Codestil & Struktur
- **Python 3.9+**, nur Standardbibliothek
- UI **ASCII-sicher** und **vollständig übersetzt** (DE/EN in `LANG`)
- Keine hartkodierten sysfs-Pfade; Discovery mit Fallbacks
- Datei-I/O in Helfer kapseln (`s_read`, `s_write`)
- Root-Schreibzugriffe kapseln; Lesevorgänge dürfen die UI nicht blockieren
- GUI responsiv halten: `after()`-Loop, keine Blockierungen

### 7) Tests & Checks
- Ohne sudo starten: UI, Temperaturkurve, CPU MHz, RAM prüfen
- Mit sudo starten: Moduswechsel prüfen, PWM/CD-Writes testen
- RPM-Anzeige prüfen; falls nicht vorhanden `--` ohne Crash
- Intervalle testen (`,` und `.` als Dezimaltrennzeichen)
- Fenstergröße ändern; sicherstellen, dass Controls sichtbar bleiben

### 8) Änderungen einreichen
1. Repo forken, Branch erstellen.
2. Kleine, klare Commits schreiben.
3. Doku anpassen, wenn Verhalten/UI sich ändert.
4. App testen (ohne/mit sudo).
5. Pull Request mit Beschreibung, Screenshots und Tests öffnen.

### 9) Issues melden
Für **Bugs**:
- Umgebung: Pi-Modell, OS-Version
- Startmodus (User vs sudo, Autostart/systemd)
- Repro-Schritte
- Erwartetes vs. tatsächliches Verhalten
- Logs/Tracebacks (als Text)
- Ausgabe von:
  ```bash
  find /sys -name pwm1 2>/dev/null
  find /sys -name cooling_device\* 2>/dev/null
  ```

Für **Feature-Requests**: Nutzerstory + gewünschtes UX beschreiben.

### 10) Sicherheit
Keine sensiblen Daten posten. Sicherheitsfunde privat an den Maintainer melden.

### 11) Lizenz
Mit deinem Beitrag stimmst du zu, dass er unter der Projektlizenz veröffentlicht wird.
[LICENSE](LICENSE)
