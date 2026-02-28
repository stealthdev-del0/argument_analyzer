"""
Argument Structure Analyzer - Main Entry Point (MVP)

Analysiert Texts auf argumentative Strukturen:
- Identifiziert Hauptthesen
- Erkennt Unterstützungs- und Gegenargumente
- Analysiert emotionale Sprache
- Warnt vor logischen Schwächen
- Visualisiert Argument-Struktur
"""

import sys
from pathlib import Path

from preprocessing import TextPreprocessor
from argument_classification import ArgumentClassifier
from structure_builder import StructureBuilder
from emotion_analysis import EmotionAnalyzer
from visualizer import TerminalVisualizer


def main(text: str = None, verbose: bool = True):
    """
    Hauptfunktion für die Argument-Analyse
    Args:
        text: Zu analysierender Text
        verbose: Detaillierte Ausgabe?
    """
    
    # Wenn kein Text gegeben, nutze Standard-Beispiel
    if text is None:
        text = """
        Artificial Intelligence is one of the most transformative technologies of our time.
        We should invest heavily in AI research because it can solve many problems.
        AI can accelerate drug discovery, improve healthcare, and optimize energy systems.
        
        However, some people worry about job displacement. They argue that automation will 
        hurt workers. But history shows that new technologies create more jobs than they destroy.
        
        Therefore, we need strong regulations to ensure AI safety while allowing innovation.
        The evidence clearly demonstrates that AI will benefit humanity.
        """
    
    print("\n" + "=" * 70)
    print("🧠 ARGUMENT STRUCTURE ANALYZER - MVP")
    print("=" * 70)
    print(f"\n📄 Input Text ({len(text)} characters):\n")
    print(text.strip())
    
    # ============================================
    # 1. PREPROCESSING
    # ============================================
    print("\n\n⚙️  Processing text...")
    processor = TextPreprocessor()
    sentences = processor.process_text(text)
    print(f"   ✓ Found {len(sentences)} sentences")
    
    # ============================================
    # 2. EMOTION ANALYSIS
    # ============================================
    emotion_analyzer = EmotionAnalyzer()
    emotion_results = emotion_analyzer.analyze_emotions(sentences)
    emotion_summary = emotion_analyzer.get_sentiment_summary(emotion_results)
    
    # ============================================
    # 3. ARGUMENT CLASSIFICATION
    # ============================================
    classifier = ArgumentClassifier()
    classifications = classifier.classify_arguments(sentences)
    argument_summary = classifier.get_argument_summary(classifications)
    
    # ============================================
    # 4. STRUCTURE BUILDING
    # ============================================
    builder = StructureBuilder()
    root_claims = builder.build_structure(classifications)
    
    # ============================================
    # 5. VISUALIZATION
    # ============================================
    visualizer = TerminalVisualizer()
    
    # Drucke detaillierte Analyse
    visualizer.print_full_analysis(
        classifications,
        builder,
        emotion_results,
        argument_summary,
        emotion_summary,
        classifier.detect_logical_weaknesses
    )
    
    return {
        "sentences": sentences,
        "classifications": classifications,
        "emotions": emotion_results,
        "builder": builder,
        "summary": argument_summary
    }


def analyze_from_file(filepath: str):
    """
    Analysiert Texte aus einer Datei
    Args:
        filepath: Pfad zur Textdatei
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        
        print(f"\n📂 Reading file: {filepath}")
        return main(text)
    except FileNotFoundError:
        print(f"❌ Error: File not found: {filepath}")
        return None


def interactive_mode():
    """
    Interaktiver Modus: Nutzer kann Text eingeben
    """
    print("\n" + "=" * 70)
    print("🧠 ARGUMENT STRUCTURE ANALYZER - INTERACTIVE MODE")
    print("=" * 70)
    print("\nEnter your text (press Enter twice to finish):\n")
    
    lines = []
    empty_lines = 0
    
    while True:
        try:
            line = input()
            if line == "":
                empty_lines += 1
                if empty_lines >= 2:
                    break
            else:
                empty_lines = 0
                lines.append(line)
        except EOFError:
            break
    
    text = "\n".join(lines)
    
    if text.strip():
        return main(text)
    else:
        print("❌ No text provided!")
        return None


if __name__ == "__main__":
    
    # Argument-Handling für verschiedene Modi
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        
        if arg == "--interactive" or arg == "-i":
            # Interaktiver Modus
            interactive_mode()
        elif arg == "--file" or arg == "-f":
            # Datei-Modus
            if len(sys.argv) > 2:
                filepath = sys.argv[2]
                analyze_from_file(filepath)
            else:
                print("❌ Usage: python main.py --file <filepath>")
        elif arg == "--help" or arg == "-h":
            # Help
            print("""
🧠 Argument Structure Analyzer - Help

USAGE:
  python main.py              # Nutze Standard-Demo-Text
  python main.py -i           # Interaktiver Modus
  python main.py -f <file>    # Analysiere Datei
  python main.py -h           # Diese Hilfe

FEATURES:
  🟢 Claim Detection (Identifiziert Hauptthesen)
  🔵 Support Detection (Unterstützende Argumente)
  🟣 Counter Detection (Gegenargumente)  
  😊 Sentiment Analysis (Emotionale Sprache)
  🔴 Logical Weakness Detection (Heuristische Fehler)
  📊 Argument Structure Visualization (ASCII-Baum)

EXAMPLE:
  python main.py -i
  Python main.py -f essay.txt

DEVELOPMENT LEVELS:
  ✅ Level 1 (MVP): Keyword-Heuristiken, einfache Sentiment-Analyse
  🔄 Level 2: Embeddings + Clustering
  🚀 Level 3: Fine-tuned Transformers
            """)
        else:
            # Text als Argument
            main(text=arg)
    else:
        # Standard: Demo mit Beispiel-Text
        main()
