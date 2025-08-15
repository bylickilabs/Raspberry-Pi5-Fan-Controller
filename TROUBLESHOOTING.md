# Troubleshooting Guide

> This guide lists common issues when using the **Raspberry Pi Fan Controller (Tkinter)** and how to solve them.

---

### 1) GitHub button does not open browser
**Cause:** The app is running as `root` without correct desktop session environment variables.  
**Solution:**  
- Run the app as your normal user (if possible).  
- If root is required, set environment variables in your systemd service:
  ```ini
  Environment=DISPLAY=:0
  Environment=XAUTHORITY=/home/<USER>/.Xauthority
  Environment=XDG_RUNTIME_DIR=/run/user/1000
  Environment=DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus
  ```

---

### 2) No RPM value (`--` shown)
**Cause:** `fan1_input` is not available in sysfs.  
**Solution:** RPM reading depends on driver/board; some Pi fan hats do not expose RPM.

---

### 3) Warning: Neither hwmon nor cooling_device found
**Cause:** Sysfs paths differ or no compatible fan control is detected.  
**Solution:**  
- Check with:
  ```bash
  find /sys -name pwm1 2>/dev/null
  find /sys -name cooling_device\* 2>/dev/null
  ```
- Adjust discovery paths in the code if needed.

---

### 4) No control, only read-only values
**Cause:** Running without root or missing write permissions to `/sys`.  
**Solution:** Start with `sudo` or delegate permissions via udev.

---

### 5) Graph not updating
**Cause:** Start button not clicked, or interval too long.  
**Solution:** Set interval to `1.0` and click **Start**.

<br>

---

<br>

> Dieser Leitfaden listet häufige Probleme bei der Nutzung des **Raspberry Pi Fan Controller (Tkinter)** auf und wie man sie behebt.

---

### 1) GitHub-Button öffnet keinen Browser
**Ursache:** App läuft als `root` ohne korrekte Desktop-Session-Umgebungsvariablen.  
**Lösung:**  
- App als normaler User starten (wenn möglich).  
- Falls Root nötig ist, Environment-Variablen in der systemd-Unit setzen:
  ```ini
  Environment=DISPLAY=:0
  Environment=XAUTHORITY=/home/<USER>/.Xauthority
  Environment=XDG_RUNTIME_DIR=/run/user/1000
  Environment=DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus
  ```

---

### 2) Keine RPM-Anzeige (`--`)
**Ursache:** `fan1_input` ist im sysfs nicht vorhanden.  
**Lösung:** RPM-Auslesen hängt vom Treiber/Board ab; einige Pi-Lüfter-HATs liefern keinen RPM-Wert.

---

### 3) Warnung: Weder hwmon noch cooling_device gefunden
**Ursache:** Sysfs-Pfade abweichend oder keine kompatible Lüftersteuerung erkannt.  
**Lösung:**  
- Prüfen mit:
  ```bash
  find /sys -name pwm1 2>/dev/null
  find /sys -name cooling_device\* 2>/dev/null
  ```
- Discovery-Pfade im Code anpassen, falls nötig.

---

### 4) Keine Steuerung, nur Read-Only-Werte
**Ursache:** Start ohne Root oder fehlende Schreibrechte für `/sys`.  
**Lösung:** Mit `sudo` starten oder Berechtigungen per udev vergeben.

---

### 5) Diagramm aktualisiert sich nicht
**Ursache:** Start-Button nicht geklickt oder Intervall zu lang.  
**Lösung:** Intervall auf `1.0` setzen und **Start** klicken.
