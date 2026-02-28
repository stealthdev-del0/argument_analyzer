# 🚀 Quick Start - Lokal auf dem Laptop

Die einfachste Weise, die App auf deinem Laptop zu starten.

---

## ⚡ 30 Sekunden Setup

### macOS/Linux
```bash
cd /Users/Salomo/Desktop/Programmier_Projekt/argument_analyzer
./start.sh
```

Fertig! Öffne [http://localhost:8501](http://localhost:8501) im Browser.

### Windows
```bash
cd C:\Users\...\Programmier_Projekt\argument_analyzer
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Fertig! Öffne [http://localhost:8501](http://localhost:8501) im Browser.

---

## 🎮 So nutzt du die App

### 1️⃣ Text eingeben
- **Option A:** Kopiere einen Text direkt rein
- **Option B:** Wähle ein Beispiel ("Climate Change", "AI Ethics", etc.)

### 2️⃣ Analyse starten
- Klick auf **🚀 Analyze**
- Warte ~1-2 Sekunden

### 3️⃣ Ergebnisse ansehen
Wähle einen Tab:
- **📋 Arguments** - Detaillierte Klassifikation
- **🌳 Structure** - Baum der Argumente
- **😊 Emotions** - Sentiment-Analyse
- **🔴 Weaknesses** - Logische Fehler
- **📈 Details** - JSON-Export

---

## 🆘 Troubleshooting

### "Command not found: streamlit"
```bash
# Aktiviere Virtual Environment
source .venv/bin/activate
# oder auf Windows
.venv\Scripts\activate
```

### "Port 8501 already in use"
```bash
# Nutze einen anderen Port
streamlit run app.py --server.port=8502
```

### "ModuleNotFoundError: No module named 'streamlit'"
```bash
# Installiere Dependencies neu
pip install -r requirements.txt
```

### App startet nicht
```bash
# Überprüfe Python Version
python --version
# Sollte 3.8+ sein

# Versuche direkt zu starten
python -m streamlit run app.py
```

---

## 📚 Weitere Optionen

### CLI (nur Text, kein Web-Interface)
```bash
source .venv/bin/activate
python main.py
```

### Unit Tests laufen
```bash
source .venv/bin/activate
python test_units.py
# Output: ✅ 11 tests passed
```

### Mit Docker (wenn installiert)
```bash
docker-compose up
# → http://localhost:8501
```

---

## 📝 Das ist alles!

**Zur Erinnerung:**
- `./start.sh` zum Starten (macOS/Linux)
- Öffne [http://localhost:8501](http://localhost:8501)
- Drücke **Ctrl+C** zum Stoppen

---

**Viel Spaß! 🎉**
