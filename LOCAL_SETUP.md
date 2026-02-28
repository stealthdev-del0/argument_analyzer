# 💻 Lokales Setup - Argument Structure Analyzer

Alle Schritte zum Starten der App auf deinem Laptop.

---

## 🖥️ macOS (mit start.sh)

### Super einfach (3 Befehle)

```bash
# 1. Terminal öffnen (Cmd+Space → Terminal)

# 2. Kopiere & paste diese 2 Zeilen:
cd /Users/Salomo/Desktop/Programmier_Projekt/argument_analyzer
./start.sh

# 3. Warte bis "Local URL: http://localhost:8501" erscheint

# 4. Öffne http://localhost:8501 im Browser
```

**Das war's!** 🎉

---

## 🪟 Windows (mit start.bat)

### Super einfach (ein Doppelklick)

**Methode 1: Doppelklick**
1. Öffne Datei-Explorer
2. Navigiere zu: `C:\Users\...\Desktop\Programmier_Projekt\argument_analyzer`
3. Doppelklick auf `start.bat`
4. Warte bis "Local URL: http://localhost:8501" erscheint
5. Öffne http://localhost:8501 im Browser

**Methode 2: Command Prompt**
```cmd
cd C:\Users\...\Desktop\Programmier_Projekt\argument_analyzer
start.bat
```

---

## 🐧 Linux

```bash
cd ~/Desktop/Programmier_Projekt/argument_analyzer
chmod +x start.sh
./start.sh
```

---

## 📜 Was macht start.sh/start.bat?

1. ✅ Erstellt Virtual Environment (nur beim 1. Mal)
2. ✅ Aktiviert Virtual Environment
3. ✅ Installiert Dependencies (nur beim 1. Mal, ~30 Sek)
4. ✅ Startet Streamlit App
5. ✅ Öffnet automatisch Browser (optional)

---

## 🎮 Nach dem Start

### Im Browser öffnen
- Wenn nicht automatisch: `http://localhost:8501`
- Oder `localhost:8501` in Adressleiste

### App nutzen
1. Text eingeben oder Beispiel wählen
2. **🚀 Analyze** anklicken
3. Ergebnisse in Tabs ansehen

### App schließen
- Im Terminal/CMD: `Ctrl+C` drücken
- Browser-Fenster einfach schließen

---

## 🆘 Häufige Fehler

### ❌ "python3: command not found"
**Problem:** Python ist nicht installiert

**Lösung:**
```bash
# Überprüfe Python
python --version

# Falls nicht installiert:
# macOS: brew install python3
# Windows: https://www.python.org/downloads/
# Linux: sudo apt-get install python3
```

### ❌ "No such file or directory: ./start.sh"
**Problem:** Du bist nicht im richtigen Verzeichnis

**Lösung:**
```bash
cd /Users/Salomo/Desktop/Programmier_Projekt/argument_analyzer
ls -la start.sh  # Überprüfe ob Datei existiert
./start.sh
```

### ❌ "Permission denied"
**Problem:** Script hat keine Ausführungserlaubnis

**Lösung macOS/Linux:**
```bash
chmod +x start.sh
./start.sh
```

### ❌ "Port 8501 already in use"
**Problem:** Eine andere App nutzt Port 8501

**Lösung A: Anderen Port nutzen**
```bash
streamlit run app.py --server.port=8502
# Dann: http://localhost:8502
```

**Lösung B: Andere App beenden**
```bash
# macOS/Linux
lsof -i :8501
# Finde die PID und beende sie mit:
kill PID
```

### ❌ "ModuleNotFoundError: No module named 'streamlit'"
**Problem:** Dependencies fehlen

**Lösung:**
```bash
source .venv/bin/activate  # macOS/Linux
# oder
.venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

---

## 📚 Alternative: Manuelle Installation

Falls start.sh nicht funktioniert:

```bash
# 1. Virtual Environment erstellen
python3 -m venv .venv

# 2. Aktivieren
source .venv/bin/activate     # macOS/Linux
# oder
.venv\Scripts\activate        # Windows

# 3. Dependencies installieren
pip install -r requirements.txt

# 4. App starten
streamlit run app.py

# 5. Im Browser öffnen
# http://localhost:8501
```

---

## 🖼️ Was du sehen solltest

Nach `./start.sh`:

```
⚠️  To view live updates on the app, open the app in a new tab.

  You can now view your Streamlit app in your browser.

  Network URL: http://10.0.1.234:8501
  External URL: http://YOUR_IP:8501
  
Remember: This is your LOCAL address - you can close the browser and restart anytime.
```

👆 Klick auf einen der Links oder benutz `http://localhost:8501`

---

## 💾 Speichern & Neustarten

**Du schreibst einen Text und möchtest die App neu starten?**

**Wichtig:** Die App speichert nichts! Alles wird neu geladen.

**Lösung:** Kopiere deinen Text einfach vorher.

Für zukünftige Versionen: Wir werden Historien-Speicherung hinzufügen.

---

## ⚡ Tipps & Tricks

### Schneller Start
```bash
# Terminal öffnen
# Cmd+K um History zu clearen
# ↑ Pfeil drücken → vorheriger Befehl
# Enter
```

### Mehrere Instanzen
Du kannst die App mehrfach mit verschiedenen Ports starten:
```bash
streamlit run app.py --server.port=8501 &
streamlit run app.py --server.port=8502 &
# → http://localhost:8501
# → http://localhost:8502
```

### Debugging
```bash
# Aktiviere Debug Mode
streamlit run app.py --logger.level=debug
```

---

## 🎓 Was ist eine Virtual Environment?

**Virtual Environment (venv)** isoliert Python-Packages für dein Projekt.

**Warum?**
- Unterschiedliche Projekte → unterschiedliche Versions
- Verhindert Konflikte
- Best Practice in Python

**Activation tipps:**
- Aktivieren: `source .venv/bin/activate`
- Deaktivieren: `deactivate`
- Erkennbar: `(.venv)` in der Shell anzeige

---

## 📞 Noch fragen?

- Siehe: [QUICK_START.md](QUICK_START.md)
- Siehe: [README.md](README.md)
- Siehe: [ARCHITECTURE.md](ARCHITECTURE.md)

---

**Viel Spaß mit der App! 🚀**

Wenn dir die App gefällt, denk an Git Push & Deployment später! 🎉
