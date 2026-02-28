# 🏗️ Architecture Guide - Argument Structure Analyzer

## System Design Overview

Das **Argument Structure Analyzer** Projekt folgt einer modularen **NLP-Pipeline-Architektur** mit klarer Separation of Concerns. Jedes Modul hat eine spezifische Aufgabe und ist unabhängig testbar.

---

## 📊 Dataflow Diagram

```
Input Text (beliebiger Text)
    ↓
[TextPreprocessor]  ──→  Sentences + Tokens
    ↓
[ClaimDetector]     ──→  ClaimResult (Type, Confidence)
    ↓                      ↓
[EmotionAnalyzer]   ──→  EmotionResult (Sentiment, Score)
    ↓
[ArgumentClassifier] ──→ ArgumentClassification (vollständig klassifiziert)
    ↓
[StructureBuilder]   ──→ ArgumentNodes (Baum-Struktur)
    ↓
[TerminalVisualizer] ──→ 📊 Terminal Output
```

---

## 🔍 Module Details

### 1. **preprocessing.py** - Satzsegmentierung & Tokenisierung
**Zweck:** Text in Sätze und Tokens zerlegen

**Datenstrukturen:**
```python
@dataclass
class Token:
    text: str          # "climate"
    pos: str           # "NOUN"
    lemma: str         # "climate"
    dep: str           # "nsubj" (dependency)

@dataclass
class Sentence:
    text: str          # "Climate change is real."
    tokens: List[Token]
    doc_id: int        # Satz-Index
```

**Funktionen:**
- `process_text(text)` → `List[Sentence]`
- `extract_verbs(sentence)` → `List[str]` (Lemmatisierung)
- `extract_entities(text)` → `List[Tuple[str, str]]` (Named Entities)

**Fallback-Tokenizer:** Wenn spaCy nicht verfügbar, nutzt Regex-basierte Segmentierung

---

### 2. **claim_detection.py** - Thesis & Argument Type Detection
**Zweck:** Klassifizieren von Sätzen nach Argumenttyp

**Datenstruktur:**
```python
@dataclass
class ClaimResult:
    sentence_text: str
    confidence: float  # 0.0 - 1.0
    markers: List[str] # ["therefore", "should"]
    claim_type: str    # "CLAIM", "SUPPORT", "COUNTER", "NEUTRAL"
```

**Heuristiken (MVP):**
- **CLAIM:** "therefore", "thus", "conclude", "should", "must"  
  Confidence: ~0.9
- **SUPPORT:** "because", "since", "evidence", "research shows"  
  Confidence: ~0.85
- **COUNTER:** "however", "but", "although", "critics say"  
  Confidence: ~0.85
- **NEUTRAL:** Keine Marker gefunden
  Confidence: 0.0

**Algorithmus:**
```
1. Konvertiere Satz zu Lowercase
2. Suche nach Markern pro Type
3. Berechne durchschnittliche Confidence pro Type
4. Wähle Type mit höchster Confidence
```

---

### 3. **emotion_analysis.py** - Sentiment & Emotionality Detection
**Zweck:** Emotionale Sprache & Sentiment analysieren

**Datenstruktur:**
```python
@dataclass
class EmotionResult:
    sentence_text: str
    sentiment: str         # "positive", "negative", "neutral"
    sentiment_score: float # -1.0 bis +1.0
    emotionality: float    # 0.0 bis 1.0 (wie emotional)
    emotion_keywords: List[str]
```

**Sentiment-Berechnung:**
```
sentiment_score = (positive_words - negative_words) / (positive_words + negative_words)

Wenn sentiment_score > 0.1  → "positive"
Wenn sentiment_score < -0.1 → "negative"
Sonst                       → "neutral"
```

**Emotionality** = Min(1.0, (positive_count + negative_count) / 5.0)

**Emotionale Marker:**
- Positive: "good", "great", "excellent", "love", "benefit"
- Negative: "bad", "terrible", "hate", "wrong", "stupid"
- Intensifier: "very" (+1.2x), "extremely" (+1.3x), "absolutely" (+1.3x)
- CAPS_LOCK: Großbuchstaben → +0.3 Score
- Ausrufezeichen: ! → +0.2 Score pro !

---

### 4. **argument_classification.py** - Kombinierte Klassifikation
**Zweck:** Claims + Emotions zusammenbringen + Argument-Stärke berechnen

**Datenstruktur:**
```python
@dataclass
class ArgumentClassification:
    sentence_text: str
    argument_type: str     # "CLAIM", "SUPPORT", "COUNTER", "NEUTRAL"
    confidence: float      # Aus ClaimDetector
    sentiment: str         # Aus EmotionAnalyzer
    emotionality: float    # Aus EmotionAnalyzer
    keywords: List[str]    # Marker + Emotion Keywords
    strength: float        # 0.0 - 1.0 (kombiniert)
```

**Strength-Berechnung:**
```
strength = 
    0.5 * confidence +           # Claim-Confidence ist wichtig
    0.3 * emotionality_factor +  # Moderate Emotionalität besser
    0.2 * sentiment_factor       # Sentiment-Konsistenz
```

**Logical Weakness Detection:**
- ❌ Ad-Hominem: "stupid", "idiot", "fool"
- ⚠️ Overgeneralization: "all", "never", "always", "everybody"
- ⚠️ Over-emotional: emotionality > 0.7
- ⚠️ Superlatives: zu viele "absolutely", "definitely"
- ⚠️ Circular reasoning: zu viele "is" Aussagen

---

### 5. **structure_builder.py** - Argument-Graph Konstruktion
**Zweck:** Baut Baum-Struktur aus klassifizierten Argumenten

**Datenstruktur:**
```python
@dataclass
class ArgumentNode:
    id: int
    text: str
    arg_type: str       # "CLAIM", "SUPPORT", "COUNTER", "NEUTRAL"
    strength: float
    emotionality: float
    children: List['ArgumentNode']
    parent: Optional['ArgumentNode']
```

**Struktur-Regeln (MVP):**
1. Identifiziere alle **CLAIM**-Nodes als Roots
2. **SUPPORT** & **COUNTER** Nodes werden als Children assigned
3. Zuordnung nach Position im Original-Text (naive)

**Beispiel:**
```
🟢 CLAIM (Root)
 ├── 🔵 SUPPORT
 ├── 🔵 SUPPORT
 └── 🟣 COUNTER
      └── (impliziter Rebuttal)
```

**Methoden:**
- `build_structure()` → `List[ArgumentNode]` (Root Claims)
- `get_argument_tree_dict()` → Dictionary (für Visualisierung)
- `get_tree_stats()` → Statistiken (depth, count, avg_strength)
- `visualize_ascii()` → ASCII-Baum-String
- `get_strongest_path()` → Linear Path der stärksten Argumente

---

### 6. **visualizer.py** - Terminal-Ausgaben
**Zweck:** Schöne, lesbare Terminal-Visualisierung

**Output-Komponenten:**

1. **Argument Analysis** - Detaillierte Auflistung mit:
   - Argument Type (Icon: 🟢🔵🟣⚪)
   - Confidence Bar
   - Strength Bar
   - Emotionality Bar + Sentiment Icon
   - Keywords

2. **Argument Summary** - Grouped Statistics:
   - Count pro Type
   - Avg Strength
   - Beispiele

3. **Structure Visualization** - ASCII-Baum:
   ```
   └── 🟢 [CLAIM] Main thesis...
       ├── 🔵 [SUPPORT] Supporting argument...
       └── 🟣 [COUNTER] Counter argument...
   ```

4. **Emotional Analysis** - Sentiment Übersicht:
   - Positive/Negative/Neutral Count
   - Avg Sentiment Score
   - Avg Emotionality

5. **Logical Weaknesses** - Erkannte Fallacies

6. **Strongest Arguments** - Top 3 nach Strength

---

### 7. **main.py** - Entry Point & CLI
**Zweck:** Benutzerinteraktion & Pipeline-Orchestrierung

**Funktions-Modi:**
```bash
python main.py                    # Demo mit Beispiel-Text
python main.py -i                 # Interaktiv
python main.py -f essay.txt       # Datei-Modus
python main.py -h                 # Help
python main.py "Custom text"      # Direkt Text
```

**Workflow:**
1. Parse Eingabe (CLI Argumente oder interaktiv)
2. Rufe `main(text)` auf
3. Orchestriere alle Module:
   - TextPreprocessor
   - ClaimDetector
   - EmotionAnalyzer
   - ArgumentClassifier
   - StructureBuilder
4. Nutze TerminalVisualizer für Output
5. Return Ergebnisse als Dictionary

---

## 🔄 Component Interaction

```
main.py
  │
  ├─→ preprocessing.TextPreprocessor()
  │     │ process_text(text)
  │     └─ Sentences[] 
  │
  ├─→ claim_detection.ClaimDetector()
  │     │ detect_claims(sentences)
  │     └─ ClaimResult[]
  │
  ├─→ emotion_analysis.EmotionAnalyzer()
  │     │ analyze_emotions(sentences)
  │     └─ EmotionResult[]
  │
  ├─→ argument_classification.ArgumentClassifier()
  │     │ classify_arguments(sentences)
  │     │ get_argument_summary()
  │     │ detect_logical_weaknesses()
  │     └─ ArgumentClassification[]
  │
  ├─→ structure_builder.StructureBuilder()
  │     │ build_structure(classifications)
  │     │ get_tree_stats()
  │     │ visualize_ascii()
  │     └─ ArgumentNode[]
  │
  └─→ visualizer.TerminalVisualizer()
        └─ print_full_analysis()
```

---

## 🧪 Testing Strategy

**Unit Tests** (`test_units.py`):
- `TestPreprocessing`: Text → Sentences
- `TestClaimDetection`: Marker Detection
- `TestEmotionAnalysis`: Sentiment/Emotionality
- `TestArgumentClassification`: Strength Calculation
- `TestIntegration`: Full Pipeline

**Test Cases** (`test_cases.py`):
- climate_change
- ai_ethics
- education
- gun_control
- social_media

---

## 📈 Performance Characteristics

| Component | Complexity | Speed |
|-----------|-----------|-------|
| Preprocessing | O(n) | < 10ms |
| Claim Detection | O(n*m) | < 50ms |
| Emotion Analysis | O(n*k) | < 30ms |
| Classification | O(n) | < 10ms |
| Structure Building | O(n²) | < 30ms |
| Visualization | O(n) | < 20ms |
| **Total** | **O(n²)** | **~150ms** |

(n = # sentences, m = # markers, k = # emotion words)

---

## 🎯 Design Patterns

1. **Dataclass Pattern** - Verwendung für strukturierte Datentypen
2. **Pipeline Pattern** - Module verarbeiten Input → Output sequentiell
3. **Strategy Pattern** - Fallback-Tokenizer wenn spaCy nicht verfügbar
4. **Decorator Pattern** - ASCII-Codes für Terminal-Icons (🟢🔵🟣)

---

## 🔮 Future Architecture (Level 2+)

### Level 2 - Embeddings & Clustering
```
Arguments
    ↓
[Vectorizer: Word2Vec/GloVe]
    ↓
Embeddings (768-dim)
    ↓
[Clusterer: K-Means]
    ↓
Argument Clusters
    ↓
[GraphViz Renderer]
    ↓
💻 Interactive Graph Visualization
```

### Level 3 - Transformer-basiert
```
Text
    ↓
[BERT Tokenizer]
    ↓
[Fine-tuned BERT Encoder]
    ↓
[Claim Classification Head]
[Relation Classification Head]
    ↓
Confidence Scores + Relations
```

---

## 📝 Design Considerations

### Warum Keyword-Heuristiken? 
- ✅ Fast (kein ML-Training)
- ✅ Interpretierbar (welche Marker gefunden?)
- ✅ Erweiterbar (einfach Keywords hinzufügen)
- ⚠️ Aber: Begrenzte Genauigkeit ohne ML

### Warum Fallback-Tokenizer?
- ✅ Funktioniert ohne externe Dependencies
- ✅ Robuster gegen Python/Library-Inkompatibilität
- ⚠️ Aber: Weniger Features (keine POS-Tags ohne spaCy)

### Warum Satz-basierte Analyse?
- ✅ Klare Einheiten für Klassifikation
- ✅ Einfach zu visualisieren
- ⚠️ Aber: Kann multi-sentence Arguments verpassen

---

## 🛠️ Extension Points

Wo du leicht neue Features hinzufügen kannst:

1. **Claim Detection**: Neue Keywords in `CLAIM_MARKERS` dict
2. **Emotion Analysis**: Neue Wörter in `POSITIVE_WORDS` / `NEGATIVE_WORDS`
3. **Logical Weakness**: Neue Pattern in `detect_logical_weaknesses()`
4. **Output Format**: Neuer Visualizer (z.B. JSON, HTML)
5. **Language Support**: Deutsche Keywords hinzufügen

---

**System-Komplexität:** ⭐⭐⭐ (Mittel)  
**Erweiterbarkeit:** ⭐⭐⭐⭐ (Hoch)  
**Production-Readiness:** ⭐⭐ (MVP-Quality)
