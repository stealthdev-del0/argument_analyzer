# 🧠 Argument Structure Analyzer

Ein Machine Learning NLP-Projekt zur **strukturellen Analyse von Argumenten** in beliebigen Texten. Identifiziert Thesen, unterstützende Argumente, Gegenargumente, emotionale Sprache und logische Schwächen.

## 🎯 Features (MVP)

### ✅ Implementiert
- **Satzsegmentierung & Tokenisierung** (spaCy)
- **Claim Detection**: Erkennt Hauptthesen via Keyword-Heuristiken
- **Argument Classification**: Klassifiziert CLAIM / SUPPORT / COUNTER / NEUTRAL
- **Sentiment Analysis**: Positive/Negative/Neutral mit Emotionalitäts-Score
- **Logical Weakness Detection**: Heuristische Erkennung von Ad-Hominems, Verallgemeinerungen, etc.
- **ASCII-Visualisierung**: Argument-Struktur als Baum
- **Terminal-Output**: Schöne farbige Ausgaben

### 🔄 Level 2 (geplant)
- Embeddings (Word2Vec / GloVe)
- Argument Clustering (K-Means)
- Graph-Visualisierung (networkx → Graphviz)
- Confidence Scores pro Relation

### 🚀 Level 3 (geplant)
- Fine-tuned BERT für Claim Detection
- Argument-Relation Classification
- Zero-Shot Classification
- Web-App (Streamlit)

---

## 📦 Installation

### Requirements
```bash
python 3.8+
```

### Setup
```bash
# 1. Clone / Navigate
cd argument_analyzer

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download spaCy models
python -m spacy download en_core_web_sm
# oder für Deutsch:
# python -m spacy download de_core_news_sm
```

**Dependencies:**
- `spacy` - NLP Pipeline (Tokenization, POS-Tags, Dependency Parsing)
- `nltk` - Natural Language Toolkit
- `transformers` - Für zukünftige Upgrades
- `networkx` - Graph-Modellierung

---

## 🚀 Quickstart

### 1. Demo mit Standard-Text
```bash
python main.py
```

### 2. Interaktiver Modus
```bash
python main.py -i
# Dann Text eingeben...
```

### 3. Datei analysieren
```bash
python main.py -f essay.txt
```

### 4. Direkt Text übergeben
```bash
python main.py "Climate change is important because..."
```

---

## 🏗️ Architektur

```
argument_analyzer/
│
├── preprocessing.py          # Satzsegmentierung, Tokenisierung, POS-Tags
├── claim_detection.py        # Identifies Hauptthesen via Keywords
├── argument_classification.py # Klassifiziert Argumente + Stärke
├── emotion_analysis.py       # Sentiment & Emotionalität
├── structure_builder.py      # Baut Argument-Graph / Baum
├── visualizer.py             # Terminal-Visualisierung
└── main.py                   # Entry Point & CLI
```

### Datenfluss

```
Text Input
    ↓
[preprocessing] → Sentences + Tokens
    ↓
[claim_detection] → ClaimResults
    ↓
[emotion_analysis] → EmotionResults
    ↓
[argument_classification] → ArgumentClassification
    ↓
[structure_builder] → ArgumentTree
    ↓
[visualizer] → Terminal Output 🎨
```

---

## 📊 Beispiel-Output

```
🟢 CLAIM (confidence: 0.90)
   Text: We must act now because the evidence is overwhelming.
   Markers: ['therefore', 'must']
   Strength: [████████░░] 85%

🔵 SUPPORT (confidence: 0.80)
   Text: Research shows that temperatures are rising.
   Markers: ['because', 'evidence']
   Strength: [███████░░░] 75%

🟣 COUNTER (confidence: 0.85)
   Text: However, some people disagree.
   Markers: ['however']
   Strength: [██████░░░░] 65%

ARGUMENT STRUCTURE:
🟢 CLAIM
 ├── 🔵 SUPPORT
 ├── 🔵 SUPPORT
 └── 🟣 COUNTER

LOGICAL WEAKNESSES:
❌ "Some people argue that..."
   ⚠️ Argument basiert stark auf Emotion statt Logik
```

---

## 🔍 Module im Detail

### `preprocessing.py`
- **TextPreprocessor**: Lädt spaCy-Modelle und verarbeitet Text
- **Sentence**: Dataclass für Sätze mit Tokens
- **Token**: Dataclass für einzelne Tokens mit POS/Dependencies

```python
processor = TextPreprocessor()
sentences = processor.process_text("Your text here")
for sent in sentences:
    tokens = sent.tokens  # Liste von Token-Objekten
    verbs = processor.extract_verbs(sent)
```

### `claim_detection.py`
- **ClaimDetector**: Erkennt Argumenttypen via Keyword-Matching
- **ClaimResult**: Enthält Text, Type, Confidence, gefundene Markers

```python
detector = ClaimDetector()
results = detector.detect_claims(sentences)
# Ergebnis: CLAIM, SUPPORT, COUNTER oder NEUTRAL
```

### `emotion_analysis.py`
- **EmotionAnalyzer**: Sentiment-Analyse + Emotionalität
- **EmotionResult**: Sentiment (-1 bis 1) + Emotionality Score

```python
analyzer = EmotionAnalyzer()
emotions = analyzer.analyze_emotions(sentences)
# Sentiment: positive/negative/neutral
# Emotionality: 0.0 - 1.0 (wie emotional)
```

### `argument_classification.py`
- **ArgumentClassifier**: Kombiniert Claims, Emotions, und Stärke-Berechnung
- **ArgumentClassification**: Vollständige Klassifikation mit Kraft-Score

```python
classifier = ArgumentClassifier()
classifications = classifier.classify_arguments(sentences)
# Jeder Satz hat: Type, Strength (0-1), Sentiment, Emotionality
```

### `structure_builder.py`
- **StructureBuilder**: Baut Argument-Baum aus Klassifizierungen
- **ArgumentNode**: Knoten im Baum mit Kindern und Parents

```python
builder = StructureBuilder()
root_claims = builder.build_structure(classifications)
tree = builder.visualize_ascii()  # ASCII-Visualisierung
```

### `visualizer.py`
- **TerminalVisualizer**: Schöne Terminal-Ausgaben mit Bars, Icons, etc.

```python
visualizer = TerminalVisualizer()
visualizer.print_full_analysis(...)
```

---

## 🧪 Testing

Jedes Modul hat einen `if __name__ == "__main__"` Block zum Testen:

```bash
python preprocessing.py
python claim_detection.py
python emotion_analysis.py
python argument_classification.py
python structure_builder.py
python visualizer.py
```

---

## 🤖 Heuristiken (MVP-Level)

### Claim Detection
- **Keywords**: "therefore", "should", "must", "I believe", "This shows that"
- **Modal Verbs**: "should", "must", "ought"
- **Confidence**: Basierend auf Anzahl und Gewicht der Marker

### Support Detection
- **Keywords**: "because", "since", "for example", "furthermore", "evidence"
- **Kombination**: Häufig nach Claims im Text

### Counter Detection
- **Keywords**: "however", "but", "although", "on the other hand", "critics say"
- **Sentiment**: Oft negativ gegenüber vorheriger These

### Logical Weaknesses
- ❌ **Ad-Hominem**: "stupid", "idiot", "fool" → Angriff auf Person statt Argument
- ⚠️ **Overgeneralization**: "all", "never", "always" → Zu absolute Aussagen
- ⚠️ **Over-emotional**: Emotionality > 0.7 → Basiert mehr auf Gefühl als Logik
- ⚠️ **Superlatives**: Mehrere "absolutely", "definitely" → Übertriebene Sicherheit

---

## 📈 Level-Progression

### 🟢 MVP (2-4 Tage) ✅
- Keyword-Heuristiken
- Einfache Sentiment-Analyse
- ASCII-Terminal-Output
- ~200 Zeilen pro Modul

### 🟡 Level 2 (1-2 Wochen)
- Sentence Embeddings (Word2Vec / GloVe)
- Cosine Similarity für Argument-Relations
- Clustering von ähnlichen Argumenten
- Graph-Visualisierung mit networkx

### 🔴 Level 3 (2-4 Wochen)
- Fine-tuned BERT / RoBERTa
- Argument-Relation Classification
- Confidence Scores pro Relation
- Web-App (Streamlit / Flask)

---

## 🎓 Was du lernst

✅ **NLP-Pipeline-Architektur**
- Text → Tokens → Features → Classification

✅ **Feature Engineering**
- Heuristische Marker-Erkennung
- Sentiment-Scoring
- Emotionality-Metriken

✅ **Klassifikation & Modellierung**
- Multi-Label Classification
- Confidence Scoring
- Graph-Strukturen

✅ **Code-Qualität**
- Saubere Modularisierung
- Dataclasses für Strukturen
- Wiederverwendbare Komponenten
- Gute Dokumentation

---

## 🔮 Zukünftige Ideen

- [ ] Support für mehrere Sprachen (Deutsch, Französisch, etc.)
- [ ] PDF/Web-Scraping Integration
- [ ] Real-time Zusammenfassung während Eingabe
- [ ] Interactive Web-Interface
- [ ] Argument-Fact-Checking Integration
- [ ] Training auf annotiertem Datensatz
- [ ] Zero-Shot Klassifikation

---

## 📝 Lizenz

MIT - Frei verwendbar für Lern- und Forschungszwecke.

---

## 🙋 FAQ

**Q: Warum Keyword-Heuristiken statt ML-Modelle?**
A: MVP ist schneller zu bauen, verständlich, und arbeitet ohne Training. Level 2/3 bringt dann ML!

**Q: Funktioniert das mit anderen Sprachen?**
A: Ja! Du brauchst nur `python -m spacy download de_core_news_sm` für Deutsch. Keywords müssen aber angepasst werden.

**Q: Wie kann ich neue Keywords hinzufügen?**
A: In `claim_detection.py` und `emotion_analysis.py` einfach in die MARKER-Dicts neue Einträge hinzufügen.

**Q: Kann ich es auf große Dokumente trainieren?**
A: MVP arbeitet Satz-für-Satz. Für Level 2 kannst du dann Batching und Caching hinzufügen.

---

**Happy analyzing! 🚀**
# argument_analyzer
