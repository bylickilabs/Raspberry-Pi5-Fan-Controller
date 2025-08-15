# Usage Guide

> This guide explains how to use the **Raspberry Pi Fan Controller (Tkinter)** application.

### 1) Starting the application
Run without root for read-only monitoring:
```bash
python3 fan.py
```
Run with root for full fan control:
```bash
sudo python3 fan.py
```

---

### 2) Interface Overview
- **Mode:** Select between Auto / 25% / 50% / 100% fan speed
- **Interval (s):** Set the refresh and apply interval in seconds (accepts comma or dot decimals, e.g., `1.0` or `1,0`)
- **Apply Once:** Applies the selected mode once
- **Start:** Starts the watchdog — applies mode periodically and refreshes metrics
- **Stop:** Stops the watchdog
- **Metrics:**
  - **PWM value:** Current fan PWM duty cycle
  - **Cooling state:** Thermal cooling device state
  - **Fan RPM:** Fan rotation speed (if available)
  - **Temperature:** CPU temperature
  - **CPU freq:** Current CPU frequency in MHz
  - **RAM used/total:** Memory usage
- **Graph:** Real-time CPU temperature curve
- **Buttons:**
  - **DE/EN:** Switches the entire interface language
  - **Info:** Opens an information window with detailed app description
  - **GitHub:** Opens the project repository or profile in the browser

---

### 3) Workflow Example
1. Start app with root to control fan:
   ```bash
   sudo python3 fan.py
   ```
2. Set **Interval** to `1.0`
3. Select **Mode** `Auto` or a fixed percentage
4. Click **Start**
5. Observe metrics and graph updating in real time

---

### 4) Tips
- For constant high fan speed, set mode to **100%** and interval to `2.0`
- If RPM is `--`, your hardware may not support RPM feedback
- Resize the window — layout adapts, scroll is available if needed

<br>

---

<br>

> Dieser Leitfaden erklärt die Nutzung der **Raspberry Pi Fan Controller (Tkinter)** Anwendung.

---

### 1) Starten der Anwendung
Ohne Root für reines Monitoring:
```bash
python3 fan.py
```
Mit Root für volle Lüftersteuerung:
```bash
sudo python3 fan.py
```

---

### 2) Benutzeroberfläche
- **Modus:** Auswahl zwischen Auto / 25% / 50% / 100% Lüftergeschwindigkeit
- **Intervall (s):** Aktualisierungs- und Apply-Intervall in Sekunden (Akzeptiert Komma oder Punkt, z. B. `1.0` oder `1,0`)
- **Einmal anwenden:** Wendet den ausgewählten Modus einmalig an
- **Start:** Startet den Watchdog — wendet den Modus periodisch an und aktualisiert Metriken
- **Stopp:** Stoppt den Watchdog
- **Messwerte:**
  - **PWM-Wert:** Aktueller PWM-Duty-Cycle des Lüfters
  - **Cooling-State:** Thermal Cooling Device Status
  - **Drehzahl (RPM):** Lüfterdrehzahl (falls verfügbar)
  - **Temperatur:** CPU-Temperatur
  - **CPU-Takt:** Aktuelle CPU-Frequenz in MHz
  - **RAM genutzt/gesamt:** Speichernutzung
- **Diagramm:** Echtzeit-CPU-Temperaturkurve
- **Buttons:**
  - **DE/EN:** Schaltet die gesamte Oberfläche um
  - **Info:** Öffnet ein Infofenster mit Details zur App
  - **GitHub:** Öffnet das Projekt-Repo oder Profil im Browser

---

### 3) Beispiel-Workflow
1. App mit Root starten:
   ```bash
   sudo python3 fan.py
   ```
2. **Intervall** auf `1.0` setzen
3. **Modus** `Auto` oder festen Prozentsatz wählen
4. **Start** klicken
5. Metriken und Diagramm in Echtzeit beobachten

---

### 4) Tipps
- Für konstant hohe Lüftergeschwindigkeit: Modus **100%** und Intervall `2.0`
- Wenn RPM `--` ist, unterstützt deine Hardware evtl. kein RPM-Feedback
- Fenstergröße ändern — Layout passt sich an, Scrollen möglich
