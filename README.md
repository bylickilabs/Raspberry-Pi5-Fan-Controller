# Raspberry Pi 5 Fan Controller

|![Logo](/assets/logo.png)|
|---|

---

### 1) Overview
This application controls and visualizes the Fan, CPU and Ram of a Raspberry Pi.  
It provides a **compact GUI** (ideal for overlays), **full DE/EN localization** and **live telemetry**:

- **Modes:** Auto, 25 %, 50 %, 100 %  
- **Live values:** Temperature (with real-time curve), **CPU frequency (MHz)**, **RAM used/total**, **Fan RPM**, **PWM value**, **Cooling state**  
- **Interval control** for periodic enforcement/watchdog  
- **Robust GitHub button** — opens profile even if started as root (session handling)

**Important:** Writing to `/sys` requires root or proper permissions via udev.  
Without root, values are **read-only**; graph/telemetry still works.

---

### 2) Requirements
- Raspberry Pi OS (Desktop), Python 3
- **Tkinter** (usually preinstalled):

```yarn
  sudo apt update
  sudo apt install -y python3 python3-tk xdg-utils
```

- Recommended: up-to-date system and active CPU fan via HAT/board

---

### 3) Installation
1. Save file (e.g., on Desktop):
```yarn
   nano /home/bylickilabs/Desktop/fan.py
```

2. Start:
```yarn
   python3 /home/bylickilabs/Desktop/fan.py
   sudo python3 /home/bylickilabs/Desktop/fan.py
```

---

### 4) Usage
- **Mode:** Auto / 25 % / 50 % / 100 %  
- **Interval (s):** periodic apply (accepts decimal comma, e.g. “1,0”)  
- **Apply Once:** sets mode once  
- **Start/Stop:** starts/stops watchdog (cyclic apply + live refresh)  
- **DE/EN:** toggles **all** texts, labels, labelframes  
- **Info:** large, scrollable box with info  
- **GitHub:** robustly opens browser (even as root if session is correct)

---

### 5) Autostart
#### A) Desktop-Autostart

```yarn
mkdir -p ~/.config/autostart
nano ~/.config/autostart/fan.desktop
```

```yarn
[Desktop Entry]
Type=Application
Name=Fan Controller
Exec=python3 /home/bylickilabs/Desktop/fan.py
Icon=utilities-system-monitor
Terminal=false
```

#### B) systemd

```yarn
sudo nano /etc/systemd/system/fan-gui.service
```

```yarn
[Unit]
Description=Fan Controller GUI
After=graphical.target

[Service]
Type=simple
User=bylickilabs
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/bylickilabs/.Xauthority
Environment=DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus
ExecStart=/usr/bin/python3 /home/bylickilabs/Desktop/fan.py
Restart=on-failure
```

<br>

---

<br>


### 1) Überblick
Diese Anwendung steuert und visualisiert den CPU-Lüfter eines Raspberry Pi.  
Sie bietet eine **kompakte GUI** (ideal für Overlays), **vollständige Sprachauswahl (DE/EN)** und **Live-Telemetrie**:

- **Modi:** Auto, 25 %, 50 %, 100 %  
- **Live-Werte:** Temperatur (mit Echtzeitkurve), **CPU-Frequenz (MHz)**, **RAM genutzt/gesamt**, **Fan RPM**, **PWM-Wert**, **Cooling-State**  
- **Intervallsteuerung** für zyklische Anwendung/Watchdog  
- **GitHub-Button (robust)** — öffnet das Profil auch bei Root-Start (Session-Handling)

**Wichtig:** Schreiben in `/sys` erfordert Root-Rechte oder passende Berechtigungen via udev.  
Ohne Root sind Werte **read-only**; Kurve/Telemetrie laufen trotzdem.

---

### 2) Systemvoraussetzungen
- Raspberry Pi OS (Desktop), Python 3
- **Tkinter** (meist vorinstalliert):  

```yarn
  sudo apt update
  sudo apt install -y python3 python3-tk xdg-utils
```
- Empfohlen: aktuelles System und aktivierter CPU-Lüfter via HAT/Board

---

### 3) Installation
1. Datei ablegen (z. B. auf dem Desktop):

```yarn
   nano /home/bylickilabs/Desktop/fan.py
```

2. Starten:

```yarn
   python3 /home/bylickilabs/Desktop/fan.py
   sudo python3 /home/bylickilabs/Desktop/fan.py
```

---

### 4) Bedienung
- **Modus:** Auto / 25 % / 50 % / 100 %  
- **Intervall (s):** Zyklischer Apply-Timer (Dezimal-Komma wird toleriert, z. B. „1,0“)  
- **Einmal anwenden:** setzt den Modus einmalig  
- **Start/Stopp:** startet/stopt den Watchdog (zyklisches Anwenden + Live-Refresh)  
- **DE/EN:** schaltet **alle** Texte, Labels, Labelframes um  
- **Info:** große, scrollbare Box mit Hinweisen  
- **GitHub:** öffnet robust den Browser (auch bei Root-Start, falls Session korrekt)

---

### 5) Autostart
#### A) Desktop-Autostart

```yarn
mkdir -p ~/.config/autostart
nano ~/.config/autostart/fan.desktop
```

```yarn
[Desktop Entry]
Type=Application
Name=Fan Controller
Exec=python3 /home/bylickilabs/Desktop/fan.py
Icon=utilities-system-monitor
Terminal=false
```

#### B) systemd

```yarn
sudo nano /etc/systemd/system/fan-gui.service
```

```yarn
[Unit]
Description=Fan Controller GUI
After=graphical.target

[Service]
Type=simple
User=bylickilabs
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/bylickilabs/.Xauthority
Environment=DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus
ExecStart=/usr/bin/python3 /home/bylickilabs/Desktop/fan.py
Restart=on-failure
```
