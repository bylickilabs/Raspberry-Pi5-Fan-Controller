import os, glob, subprocess, shutil, tkinter as tk
from tkinter import ttk, messagebox
import signal, webbrowser
from collections import deque

OVERLAY_WIDTH = 670
OVERLAY_HEIGHT = 670
MIN_WIDTH = 630
MIN_HEIGHT = 630

DEFAULT_INTERVAL_SEC = 1.0
MIN_INTERVAL_SEC = 0.2
MAX_INTERVAL_SEC = 10.0

CHART_MAX_POINTS = 300
CHART_PADDING_PX = 8

GITHUB_URL = "https://github.com/bylickilabs"

LANG = {
    "de": {
        "title": "Raspberry Pi - Lüftersteuerung",
        "paths": "Erkannte Pfade",
        "lbl_pwm1": "hwmon pwm1:",
        "lbl_pwm1_en": "pwm1_enable:",
        "lbl_fan1_input": "fan1_input:",
        "lbl_cooling": "cooling_device:",

        "control": "Steuerung",
        "mode": "Modus:",
        "interval": "Intervall (s):",
        "apply_once": "Einmal anwenden",
        "start": "Start",
        "stop": "Stopp",

        "metrics": "Messwerte",
        "pwm_val": "PWM-Wert:",
        "cd_val": "Cooling-State:",
        "rpm_val": "Drehzahl (RPM):",
        "temp_now": "Temperatur:",
        "degc": "degC",
        "cpu_freq": "CPU-Takt:",
        "mhz": "MHz",
        "ram_usage": "RAM genutzt/gesamt:",

        "chart_title": "Echtzeit-Temperaturkurve",

        "info_title": "Info",
        "btn_info": "Info",
        "btn_github": "GitHub",
        "btn_lang": "EN",
        "info_btn_close": "Schliessen",
        "info_text":
            "Fan Controller (BYLICKILABS)\n\n"
            "Funktionen:\n"
            "- Modi: Auto, 25%, 50%, 100%\n"
            "- RPM-Anzeige (falls verfuegbar)\n"
            "- CPU-Temperatur live + Echtzeitkurve\n"
            "- CPU-Taktfrequenz (MHz)\n"
            "- RAM genutzt/gesamt\n"
            "- Einstellbares Intervall (Watchdog/Neu-Anwendung)\n"
            "- Schreibt in /sys (Root erforderlich)\n\n"
            "Hinweise:\n"
            "- Manche Treiber unterstuetzen 'Auto' (pwm1_enable=2) nicht.\n"
            "- Ohne fan1_input keine RPM-Anzeige.\n"
            "- Ohne sudo nur Lesen, keine Steuerung.",

        "status_idle": "Status: Inaktiv",
        "status_run": "Status: Aktiv",
        "status_applied": "Status: Angewendet '{mode}'",
        "status_partial": "Status: Angewendet '{mode}' (teilweise/fehlgeschlagen)",

        "warn_perm_title": "Berechtigung",
        "warn_perm_text": "Bitte mit sudo starten, um den Luefter zu steuern.\nRPM kann ggf. ohne sudo lesbar sein.",
        "no_ctrl": "Keine Steuerung moeglich (sudo erforderlich).",
        "err_no_paths": "Warnung: Weder hwmon noch cooling_device gefunden."
    },
    "en": {
        "title": "Raspberry Pi - Fan Controller",
        "paths": "Detected Paths",
        "lbl_pwm1": "hwmon pwm1:",
        "lbl_pwm1_en": "pwm1_enable:",
        "lbl_fan1_input": "fan1_input:",
        "lbl_cooling": "cooling_device:",

        "control": "Control",
        "mode": "Mode:",
        "interval": "Interval (s):",
        "apply_once": "Apply Once",
        "start": "Start",
        "stop": "Stop",

        "metrics": "Metrics",
        "pwm_val": "PWM value:",
        "cd_val": "Cooling state:",
        "rpm_val": "Fan RPM:",
        "temp_now": "Temperature:",
        "degc": "degC",
        "cpu_freq": "CPU freq:",
        "mhz": "MHz",
        "ram_usage": "RAM used/total:",

        "chart_title": "Real-time Temperature Curve",

        "info_title": "Info",
        "btn_info": "Info",
        "btn_github": "GitHub",
        "btn_lang": "DE",
        "info_btn_close": "Close",
        "info_text":
            "Fan Controller (BYLICKILABS)\n\n"
            "Features:\n"
            "- Modes: Auto, 25%, 50%, 100%\n"
            "- RPM readout (if available)\n"
            "- Live CPU temperature + real-time curve\n"
            "- CPU frequency (MHz)\n"
            "- RAM used/total\n"
            "- Adjustable interval (watchdog/re-apply)\n"
            "- Writes to /sys (root required)\n\n"
            "Notes:\n"
            "- Some drivers do not support 'Auto' (pwm1_enable=2).\n"
            "- Without fan1_input no RPM display.\n"
            "- Without sudo read-only; no control.",

        "status_idle": "Status: Idle",
        "status_run": "Status: Running",
        "status_applied": "Status: Applied '{mode}'",
        "status_partial": "Status: Applied '{mode}' (partial/failed)",

        "warn_perm_title": "Permission",
        "warn_perm_text": "Please run with sudo to control the fan.\nRPM may be readable without sudo.",
        "no_ctrl": "No control possible (sudo required).",
        "err_no_paths": "Warning: Neither hwmon nor cooling_device found."
    }
}

def is_root():
    return hasattr(os, "geteuid") and os.geteuid() == 0

def s_read(p):
    try:
        with open(p, "r") as f:
            return f.read().strip()
    except Exception:
        return None

def s_write(p, v):
    try:
        with open(p, "w") as f:
            f.write(v)
        return True
    except Exception:
        return False

def open_url_robust(url):
    """
    Oeffnet URL in der aktiven Desktop-Session.
    - Wenn App als root laeuft: versucht SUDO_USER bzw. UID 1000 fuer DBus/Display.
    """
    try:
        if os.environ.get("DISPLAY") and os.environ.get("XDG_RUNTIME_DIR"):
            if shutil.which("xdg-open"):
                subprocess.Popen(["xdg-open", url],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return True
    except Exception:
        pass

    try:
        euid = os.geteuid()
    except Exception:
        euid = None

    if euid == 0:
        sudo_user = os.environ.get("SUDO_USER")
        target_user = None
        target_uid = 1000
        try:
            import pwd
            if sudo_user:
                target_user = sudo_user
                target_uid = pwd.getpwnam(sudo_user).pw_uid
            else:
                target_user = pwd.getpwuid(1000).pw_name
        except Exception:
            target_user = os.environ.get("USER", "pi")

        env = os.environ.copy()
        env["DISPLAY"] = env.get("DISPLAY") or ":0"
        env["XAUTHORITY"] = f"/home/{target_user}/.Xauthority"
        env["XDG_RUNTIME_DIR"] = f"/run/user/{target_uid}"
        env["DBUS_SESSION_BUS_ADDRESS"] = f"unix:path=/run/user/{target_uid}/bus"

        def run_user(cmd):
            if shutil.which("sudo"):
                try:
                    subprocess.Popen(
                        ["sudo", "-u", target_user, "-H", "env",
                         f"DISPLAY={env['DISPLAY']}",
                         f"XAUTHORITY={env['XAUTHORITY']}",
                         f"XDG_RUNTIME_DIR={env['XDG_RUNTIME_DIR']}",
                         f"DBUS_SESSION_BUS_ADDRESS={env['DBUS_SESSION_BUS_ADDRESS']}"] + cmd,
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                    )
                    return True
                except Exception:
                    return False
            return False

        if shutil.which("xdg-open") and run_user(["xdg-open", url]): return True
        if shutil.which("gio") and run_user(["gio", "open", url]): return True
        for exe in ["chromium-browser", "chromium", "firefox"]:
            if shutil.which(exe) and run_user([exe, url]): return True

    try:
        if webbrowser.open(url, new=2):
            return True
    except Exception:
        pass

    if shutil.which("xdg-open"):
        try:
            subprocess.Popen(["xdg-open", url],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except Exception:
            pass

    for cmd in [["gio", "open"], ["chromium-browser"], ["chromium"], ["firefox"]]:
        if shutil.which(cmd[0]):
            try:
                subprocess.Popen(cmd + [url],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return True
            except Exception:
                continue

    try:
        messagebox.showerror("Browser", "Konnte den Browser nicht oeffnen.\nPruefe Desktop-/Autostart-Setup.")
    except Exception:
        pass
    return False

class HwmonPaths:
    def __init__(self, pwm1, pwm1_enable=None, pwm1_max=None, fan1_input=None):
        self.pwm1 = pwm1
        self.pwm1_enable = pwm1_enable
        self.pwm1_max = pwm1_max
        self.fan1_input = fan1_input

def find_hwmon():
    pats = [
        "/sys/class/hwmon/hwmon*/pwm1",
        "/sys/devices/platform/*/hwmon/hwmon*/pwm1",
        "/sys/devices/platform/*/*/hwmon/hwmon*/pwm1",
    ]
    for pat in pats:
        for pwm1 in glob.glob(pat):
            base = os.path.dirname(pwm1)
            en = os.path.join(base, "pwm1_enable")
            mx = os.path.join(base, "pwm1_max")
            fan = os.path.join(base, "fan1_input")
            return HwmonPaths(
                pwm1=pwm1,
                pwm1_enable=en if os.path.exists(en) else None,
                pwm1_max=mx if os.path.exists(mx) else None,
                fan1_input=fan if os.path.exists(fan) else None,
            )
    return None

class CoolingPaths:
    def __init__(self, cur_state, max_state):
        self.cur_state = cur_state
        self.max_state = max_state

def find_cooling_device():
    for cur in glob.glob("/sys/class/thermal/cooling_device*/cur_state"):
        mx = os.path.join(os.path.dirname(cur), "max_state")
        if os.path.exists(mx):
            return CoolingPaths(cur, mx)
    return None

def find_temp_sensor_path():
    for pat in ["/sys/class/thermal/thermal_zone*/temp",
                "/sys/devices/virtual/thermal/thermal_zone*/temp"]:
        for path in sorted(glob.glob(pat)):
            try:
                v = int(open(path, "r").read().strip())
                if 0 < v < 200000:
                    return path
            except Exception:
                pass
    return None

def read_temp_c(sensor):
    try:
        return int(open(sensor, "r").read().strip()) / 1000.0
    except Exception:
        return None

def find_cpu_freq_path():
    cands = [
        "/sys/devices/system/cpu/cpufreq/policy0/scaling_cur_freq",
        "/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq",
    ] + glob.glob("/sys/devices/system/cpu/cpufreq/policy*/scaling_cur_freq")
    for p in cands:
        if os.path.exists(p):
            return p
    return None

def read_cpu_freq_mhz(p):
    try:
        return int(open(p, "r").read().strip()) / 1000.0 if p else None
    except Exception:
        return None

def read_mem_used_total_mb():
    try:
        total = avail = None
        with open("/proc/meminfo", "r") as f:
            for line in f:
                if line.startswith("MemTotal:"):
                    total = int(line.split()[1])
                elif line.startswith("MemAvailable:"):
                    avail = int(line.split()[1])
                if total is not None and avail is not None:
                    break
        if total is None or avail is None:
            return (None, None)
        used = total - avail
        return (used / 1024.0, total / 1024.0)
    except Exception:
        return (None, None)

def fmt_mb(x):
    if x is None:
        return "--"
    return f"{x/1024.0:.1f} GB" if x >= 1024.0 else f"{x:.0f} MB"

def get_pwm_max(hw):
    if hw and hw.pwm1_max:
        try:
            mv = int(s_read(hw.pwm1_max) or "0")
            if mv > 0:
                return mv
        except Exception:
            pass
    return 255

def set_mode_auto(hw, cd):
    ok = False
    if hw and hw.pwm1_enable:
        ok = s_write(hw.pwm1_enable, "2\n") or s_write(hw.pwm1_enable, "2")
    return ok or (cd is not None)

def set_mode_percent(hw, cd, percent):
    ok = False
    if hw:
        if hw.pwm1_enable and os.path.exists(hw.pwm1_enable):
            s_write(hw.pwm1_enable, "1\n")
        pmax = get_pwm_max(hw)
        duty = max(0, min(int(round(pmax * percent / 100.0)), pmax))
        if s_write(hw.pwm1, f"{duty}\n") or s_write(hw.pwm1, f"{duty}"):
            ok = True
    if cd:
        try:
            ms = int(s_read(cd.max_state) or "0")
        except Exception:
            ms = 0
        if ms > 0:
            target = max(0, min(int(round(ms * percent / 100.0)), ms))
            if s_write(cd.cur_state, f"{target}\n") or s_write(cd.cur_state, f"{target}"):
                ok = True
    return ok

def read_rpm(hw):
    try:
        if hw and hw.fan1_input and os.path.exists(hw.fan1_input):
            val = s_read(hw.fan1_input)
            rpm = int(val) if val is not None else None
            return rpm if (rpm and rpm > 0) else None
    except Exception:
        pass
    return None

def read_pwm_value(hw):
    try:
        if hw and os.path.exists(hw.pwm1):
            rb = s_read(hw.pwm1)
            return int(rb) if rb is not None else None
    except Exception:
        pass
    return None

def read_cooling_state(cd):
    try:
        if cd and os.path.exists(cd.cur_state):
            rb = s_read(cd.cur_state)
            return int(rb) if rb is not None else None
    except Exception:
        pass
    return None

MODES = ["Auto", "25%", "50%", "100%"]

class ScrollableFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.vscroll = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner = ttk.Frame(self.canvas)
        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=self.vscroll.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.vscroll.grid(row=0, column=1, sticky="ns")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

class InfoDialog(tk.Toplevel):
    def __init__(self, master, title, text, close_txt):
        super().__init__(master)
        self.title(title)
        self.geometry("560x460")
        self.minsize(500, 380)
        self.transient(master)
        self.grab_set()

        frame = ttk.Frame(self, padding=10)
        frame.pack(fill="both", expand=True)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        txt = tk.Text(frame, wrap="word", height=20)
        vs = ttk.Scrollbar(frame, orient="vertical", command=txt.yview)
        txt.configure(yscrollcommand=vs.set)
        txt.grid(row=0, column=0, sticky="nsew")
        vs.grid(row=0, column=1, sticky="ns")

        try:
            txt.configure(font=("TkFixedFont", 11))
        except Exception:
            pass
        txt.insert("1.0", text)
        txt.configure(state="disabled")

        ttk.Button(frame, text=close_txt, command=self.destroy).grid(row=1, column=0, columnspan=2, pady=(8, 0))

class FanApp:
    def __init__(self, root):
        self.root = root
        try:
            self.root.tk.call("tk", "scaling", 1.15)
        except Exception:
            pass

        self.lang = "de"
        self.running = False
        self.job = None

        self.hw = find_hwmon()
        self.cd = find_cooling_device()
        self.sensor = find_temp_sensor_path()
        self.freq_path = find_cpu_freq_path()

        self.interval = DEFAULT_INTERVAL_SEC
        self.series = deque(maxlen=CHART_MAX_POINTS)
        self.min_seen = None
        self.max_seen = None

        self.style = ttk.Style(root)
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

        self.build_ui()
        self.apply_language()
        self.refresh_all()

        if not is_root():
            messagebox.showwarning(self.t("warn_perm_title"), self.t("warn_perm_text"))
        if not self.hw and not self.cd:
            messagebox.showwarning(self.t("info_title"), self.t("err_no_paths"))

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        signal.signal(signal.SIGINT, signal.SIG_DFL)

    def t(self, key):
        return LANG[self.lang].get(key, key)

    def build_ui(self):
        self.root.title(self.t("title"))
        self.root.geometry(f"{OVERLAY_WIDTH}x{OVERLAY_HEIGHT}")
        self.root.minsize(MIN_WIDTH, MIN_HEIGHT)

        outer = ttk.Frame(self.root, padding=8)
        outer.pack(fill="both", expand=True)
        outer.grid_rowconfigure(0, weight=1)
        outer.grid_columnconfigure(0, weight=1)

        self.scroll = ScrollableFrame(outer)
        self.scroll.grid(row=0, column=0, sticky="nsew")
        container = self.scroll.inner
        container.grid_columnconfigure(0, weight=1)

        bar = ttk.Frame(container, padding=(0, 0, 0, 6))
        bar.grid(row=0, column=0, sticky="ew")
        bar.columnconfigure(0, weight=1)
        ttk.Label(bar, text="").grid(row=0, column=0, sticky="ew")

        self.btn_lang = ttk.Button(bar, width=6, command=self.toggle_lang)
        self.btn_info = ttk.Button(bar, width=8, command=self.show_info)
        self.btn_github = ttk.Button(bar, width=8, command=lambda: open_url_robust(GITHUB_URL))
        self.btn_lang.grid(row=0, column=1, padx=4)
        self.btn_info.grid(row=0, column=2, padx=4)
        self.btn_github.grid(row=0, column=3, padx=4)

        self.lf_paths = ttk.LabelFrame(container, padding=8)
        self.lf_paths.grid(row=1, column=0, sticky="ew")
        self.lf_paths.columnconfigure(1, weight=1)

        self.k_pwm1 = ttk.Label(self.lf_paths); self.v_pwm1 = ttk.Label(self.lf_paths, text=self.hw.pwm1 if self.hw else "-")
        self.k_pwm1.grid(row=0, column=0, sticky="w"); self.v_pwm1.grid(row=0, column=1, sticky="w", padx=6)

        self.k_pwm1e = ttk.Label(self.lf_paths); self.v_pwm1e = ttk.Label(self.lf_paths, text=self.hw.pwm1_enable if (self.hw and self.hw.pwm1_enable) else "-")
        self.k_pwm1e.grid(row=1, column=0, sticky="w"); self.v_pwm1e.grid(row=1, column=1, sticky="w", padx=6)

        self.k_fan1 = ttk.Label(self.lf_paths); self.v_fan1 = ttk.Label(self.lf_paths, text=self.hw.fan1_input if (self.hw and self.hw.fan1_input) else "-")
        self.k_fan1.grid(row=2, column=0, sticky="w"); self.v_fan1.grid(row=2, column=1, sticky="w", padx=6)

        self.k_cool = ttk.Label(self.lf_paths)
        cd_desc = "-" if not self.cd else f"{self.cd.cur_state} (max: {s_read(self.cd.max_state)})"
        self.v_cool = ttk.Label(self.lf_paths, text=cd_desc)
        self.k_cool.grid(row=3, column=0, sticky="w"); self.v_cool.grid(row=3, column=1, sticky="w", padx=6)

        self.lf_ctrl = ttk.LabelFrame(container, padding=8)
        self.lf_ctrl.grid(row=2, column=0, sticky="ew", pady=(6, 0))
        for i in range(6):
            self.lf_ctrl.grid_columnconfigure(i, weight=0)
        self.lf_ctrl.grid_columnconfigure(5, weight=1)

        self.lbl_mode = ttk.Label(self.lf_ctrl)
        self.cb_mode = ttk.Combobox(self.lf_ctrl, values=MODES, state="readonly", width=8)
        self.cb_mode.set("Auto")
        self.lbl_int = ttk.Label(self.lf_ctrl)
        self.var_int = tk.StringVar(value=str(DEFAULT_INTERVAL_SEC))
        self.entry_int = ttk.Entry(self.lf_ctrl, width=6, textvariable=self.var_int)

        self.lbl_mode.grid(row=0, column=0, sticky="w")
        self.cb_mode.grid(row=0, column=1, sticky="w", padx=6)
        self.lbl_int.grid(row=0, column=2, sticky="w", padx=(12, 0))
        self.entry_int.grid(row=0, column=3, sticky="w")

        self.btn_apply = ttk.Button(self.lf_ctrl, command=self.apply_once)
        self.btn_start = ttk.Button(self.lf_ctrl, command=self.start)
        self.btn_stop = ttk.Button(self.lf_ctrl, state="disabled", command=self.stop)
        self.btn_apply.grid(row=1, column=0, sticky="w", pady=(6, 0))
        self.btn_start.grid(row=1, column=1, sticky="w", padx=6, pady=(6, 0))
        self.btn_stop.grid(row=1, column=2, sticky="w", pady=(6, 0))
        self.cb_mode.bind("<<ComboboxSelected>>", self.on_mode_change)

        self.lf_metrics = ttk.LabelFrame(container, padding=8)
        self.lf_metrics.grid(row=3, column=0, sticky="ew", pady=(6, 0))
        for i in range(10):
            self.lf_metrics.grid_columnconfigure(i, weight=1)

        self.k_pwm = ttk.Label(self.lf_metrics); self.v_pwm = ttk.Label(self.lf_metrics, text="--")
        self.k_cd = ttk.Label(self.lf_metrics); self.v_cd = ttk.Label(self.lf_metrics, text="--")
        self.k_rpm = ttk.Label(self.lf_metrics); self.v_rpm = ttk.Label(self.lf_metrics, text="--")
        self.k_temp = ttk.Label(self.lf_metrics); self.v_temp = ttk.Label(self.lf_metrics, text="--"); self.u_temp = ttk.Label(self.lf_metrics)
        self.k_freq = ttk.Label(self.lf_metrics); self.v_freq = ttk.Label(self.lf_metrics, text="--"); self.u_freq = ttk.Label(self.lf_metrics)
        self.k_ram = ttk.Label(self.lf_metrics); self.v_ram = ttk.Label(self.lf_metrics, text="--")

        self.k_pwm.grid(row=0, column=0, sticky="w"); self.v_pwm.grid(row=0, column=1, sticky="w")
        self.k_cd.grid(row=0, column=2, sticky="w"); self.v_cd.grid(row=0, column=3, sticky="w")
        self.k_rpm.grid(row=0, column=4, sticky="w"); self.v_rpm.grid(row=0, column=5, sticky="w")

        self.k_temp.grid(row=1, column=0, sticky="e", pady=(6, 0)); self.v_temp.grid(row=1, column=1, sticky="w", pady=(6, 0)); self.u_temp.grid(row=1, column=2, sticky="w", pady=(6, 0))
        self.k_freq.grid(row=1, column=3, sticky="e", pady=(6, 0)); self.v_freq.grid(row=1, column=4, sticky="w", pady=(6, 0)); self.u_freq.grid(row=1, column=5, sticky="w", pady=(6, 0))
        self.k_ram.grid(row=1, column=6, sticky="e", pady=(6, 0)); self.v_ram.grid(row=1, column=7, sticky="w", pady=(6, 0))

        self.lf_chart = ttk.LabelFrame(container, padding=8)
        self.lf_chart.grid(row=4, column=0, sticky="nsew", pady=(6, 8))
        container.grid_rowconfigure(4, weight=1)
        self.lf_chart.grid_rowconfigure(0, weight=1)
        self.lf_chart.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.lf_chart, height=240, background="#ffffff",
                                highlightthickness=1, highlightbackground="#cccccc")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.bind("<Configure>", lambda e: self.draw_chart())

        self.lbl_status = ttk.Label(container)
        self.lbl_status.grid(row=5, column=0, sticky="w", pady=(0, 6))

    def apply_language(self):
        t = LANG[self.lang]
        self.root.title(t["title"])
        self.btn_info.configure(text=t["btn_info"])
        self.btn_github.configure(text=t["btn_github"])
        self.btn_lang.configure(text=t["btn_lang"])
        self.lf_paths.configure(text=t["paths"])
        self.lf_ctrl.configure(text=t["control"])
        self.lf_metrics.configure(text=t["metrics"])
        self.lf_chart.configure(text=t["chart_title"])
        self.k_pwm1.configure(text=t["lbl_pwm1"])
        self.k_pwm1e.configure(text=t["lbl_pwm1_en"])
        self.k_fan1.configure(text=t["lbl_fan1_input"])
        self.k_cool.configure(text=t["lbl_cooling"])
        self.lbl_mode.configure(text=t["mode"])
        self.lbl_int.configure(text=t["interval"])
        self.btn_apply.configure(text=t["apply_once"])
        self.btn_start.configure(text=t["start"])
        self.btn_stop.configure(text=t["stop"])
        self.k_pwm.configure(text=t["pwm_val"])
        self.k_cd.configure(text=t["cd_val"])
        self.k_rpm.configure(text=t["rpm_val"])
        self.k_temp.configure(text=t["temp_now"])
        self.u_temp.configure(text=t["degc"])
        self.k_freq.configure(text=t["cpu_freq"])
        self.u_freq.configure(text=t["mhz"])
        self.k_ram.configure(text=t["ram_usage"])
        self.lbl_status.configure(text=t["status_run"] if self.running else t["status_idle"])
        self.draw_chart()

    def toggle_lang(self):
        self.lang = "en" if self.lang == "de" else "de"
        self.apply_language()

    def show_info(self):
        t = LANG[self.lang]
        InfoDialog(self.root, t["info_title"], t["info_text"], t["info_btn_close"])

    def parse_interval(self):
        s = self.var_int.get().strip()
        try:
            v = float(s.replace(",", "."))
            if v < MIN_INTERVAL_SEC: v = MIN_INTERVAL_SEC
            if v > MAX_INTERVAL_SEC: v = MAX_INTERVAL_SEC
            self.interval = v
            self.var_int.set(str(v))
        except Exception:
            self.interval = DEFAULT_INTERVAL_SEC
            self.var_int.set(str(DEFAULT_INTERVAL_SEC))

    def on_mode_change(self, _e=None):
        if self.running:
            self.apply_control()

    def apply_control(self):
        ok = True
        if not is_root():
            ok = False
        else:
            mode = self.cb_mode.get()
            if mode == "Auto":
                ok = set_mode_auto(self.hw, self.cd)
            elif mode == "25%":
                ok = set_mode_percent(self.hw, self.cd, 25)
            elif mode == "50%":
                ok = set_mode_percent(self.hw, self.cd, 50)
            elif mode == "100%":
                ok = set_mode_percent(self.hw, self.cd, 100)
            else:
                ok = False

        t = LANG[self.lang]
        self.lbl_status.configure(text=(t["status_applied"].format(mode=self.cb_mode.get())
                                        if ok else t["status_partial"].format(mode=self.cb_mode.get())))
        self.refresh_all()
        return ok

    def refresh_all(self):
        self.v_pwm.configure(text=str(read_pwm_value(self.hw)) if self.hw else "--")
        self.v_cd.configure(text=str(read_cooling_state(self.cd)) if self.cd else "--")
        rpm = read_rpm(self.hw)
        self.v_rpm.configure(text=str(rpm) if rpm is not None else "--")

        temp = read_temp_c(self.sensor) if self.sensor else None
        if temp is not None:
            self.v_temp.configure(text=f"{temp:.1f}")
            self.series.append(temp)
            if self.min_seen is None or temp < self.min_seen: self.min_seen = temp
            if self.max_seen is None or temp > self.max_seen: self.max_seen = temp
        else:
            self.v_temp.configure(text="--")

        mhz = read_cpu_freq_mhz(self.freq_path)
        self.v_freq.configure(text=f"{mhz:.0f}" if mhz is not None else "--")

        used, total = read_mem_used_total_mb()
        self.v_ram.configure(text=(f"{fmt_mb(used)} / {fmt_mb(total)}" if used is not None else "--"))

        self.draw_chart()

    def apply_once(self):
        self.parse_interval()
        self.apply_control()

    def tick(self):
        try:
            self.apply_control()
        except Exception as e:
            self.lbl_status.configure(text=f"Tick error: {e}")
        finally:
            if self.running:
                self.root.after(int(self.interval * 1000), self.tick)

    def start(self):
        self.parse_interval()
        self.running = True
        self.btn_start.configure(state="disabled")
        self.btn_stop.configure(state="normal")
        self.lbl_status.configure(text=self.t("status_run"))
        self.refresh_all()
        self.tick()

    def stop(self):
        self.running = False
        self.btn_start.configure(state="normal")
        self.btn_stop.configure(state="disabled")
        self.lbl_status.configure(text=self.t("status_idle"))

    def on_close(self):
        self.stop()
        self.root.destroy()

    def draw_chart(self):
        c = self.canvas
        w = int(c.winfo_width())
        h = int(c.winfo_height())
        c.delete("all")
        c.create_rectangle(0, 0, w, h, fill="#ffffff", outline="")

        left = CHART_PADDING_PX + 34
        right = w - CHART_PADDING_PX - 4
        top = CHART_PADDING_PX + 4
        bottom = h - CHART_PADDING_PX - 14

        c.create_line(left, bottom, right, bottom, fill="#cccccc")
        c.create_line(left, top, left, bottom, fill="#cccccc")

        n = len(self.series)
        if n == 0:
            return

        tmin = min(self.series)
        tmax = max(self.series)
        span = max(1.0, tmax - tmin)
        pad = span * 0.1
        ymin = (self.min_seen if self.min_seen is not None else tmin) - pad
        ymax = (self.max_seen if self.max_seen is not None else tmax) + pad
        if ymax - ymin < 5.0:
            ymax = ymin + 5.0

        mid = (ymin + ymax) / 2.0
        for val, y in ((ymin, bottom), (mid, (top + bottom) / 2.0), (ymax, top)):
            c.create_text(left - 6, y, text=f"{val:.0f}", anchor="e", fill="#666666")

        def map_xy(i, v):
            x = left + (i / max(1, (n - 1))) * (right - left)
            y = bottom - ((v - ymin) / (ymax - ymin)) * (bottom - top)
            return x, y

        if n == 1:
            x, y = map_xy(0, self.series[0])
            c.create_oval(x - 3, y - 3, x + 3, y + 3, fill="#0077cc", outline="")
        else:
            px, py = map_xy(0, self.series[0])
            for i in range(1, n):
                x, y = map_xy(i, self.series[i])
                c.create_line(px, py, x, y, fill="#0077cc", width=2)
                px, py = x, y
            c.create_oval(px - 3, py - 3, px + 3, py + 3, fill="#0077cc", outline="")

def main():
    root = tk.Tk()
    FanApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
