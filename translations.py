# translation support for UI strings

LANGUAGE_NAMES = {
    "en": "English",
    "de": "Deutsch",
}

# keys used throughout the app
LANGUAGES = {
    "en": {
        "config_header": "⚙️ Configuration",
        "select_input_method": "Select Input Method:",
        "input_help": "Choose how to input text for analysis",
        "free_text": "📝 Free Text",
        "example_cases": "📂 Example Cases",
        "min_confidence": "Minimum Confidence Threshold:",
        "min_confidence_help": "Filter arguments by minimum confidence",
        "about_header": "📊 About",
        "about_text": "Argument Structure Analyzer analyzes text for:\n- 🟢 Main claims\n- 🔵 Supporting arguments\n- 🟣 Counter arguments\n- 😊 Sentiment & emotionality\n- 🔴 Logical weaknesses",
        "page_title": "🧠 Argument Structure Analyzer",
        "subtitle": "*Analyze argumentative structures in any text*",
        "input_header": "📍 Input Text",
        "text_placeholder": "Enter or paste your text:",
        "text_area_placeholder": "Enter your text here... (essay, comment, debate, etc.)",
        "example_loaded": "ℹ️ Loaded example: **{case}**",
        "stats_header": "📊 Stats",
        "chars_label": "Characters",
        "words_label": "Words",
        "est_sentences": "Est. Sentences",
        "analyze_button": "🚀 Analyze",
        "analyzing_spinner": "⏳ Analyzing text...",
        "classified_args_header": "Classified Arguments",
        "argument_tree_header": "Argument Tree Structure",
        "structure_stats_header": "Structure Statistics",
        "sentiment_header": "Sentiment & Emotional Analysis",
        "weaknesses_header": "Detected Logical Weaknesses & Fallacies",
        "breakdown_header": "Detailed Breakdown",
        "visualizations_header": "📊 Comprehensive Visualizations",
        "analysis_complete": "✅ Analysis complete!",
        "warning_no_text": "⚠️ Please enter some text to analyze",
        "results_header": "📊 Analysis Results",
        "error_analysis": "❌ Error during analysis: {error}",
    },
    "de": {
        "config_header": "⚙️ Konfiguration",
        "select_input_method": "Eingabemethode wählen:",
        "input_help": "Wählen Sie, wie der Text eingegeben wird",
        "free_text": "📝 Freier Text",
        "example_cases": "📂 Beispieltexte",
        "min_confidence": "Minimale Vertrauensschwelle:",
        "min_confidence_help": "Argumente nach Mindestvertrauen filtern",
        "about_header": "📊 Über",
        "about_text": "Der Argumentstruktur-Analysator untersucht Text auf:\n- 🟢 Hauptthesen\n- 🔵 unterstützende Argumente\n- 🟣 Gegenargumente\n- 😊 Stimmung & Emotionalität\n- 🔴 Logische Schwächen",
        "page_title": "🧠 Argumentstruktur-Analysator",
        "subtitle": "*Untersuche argumentative Strukturen in beliebigem Text*",
        "input_header": "📍 Texteingabe",
        "text_placeholder": "Geben Sie Ihren Text ein oder fügen Sie ihn ein:",
        "text_area_placeholder": "Geben Sie hier Ihren Text ein... (Essay, Kommentar, Debatte etc.)",
        "example_loaded": "ℹ️ Beispiel geladen: **{case}**",
        "stats_header": "📊 Statistik",
        "chars_label": "Zeichen",
        "words_label": "Wörter",
        "est_sentences": "Geschätzte Sätze",
        "analyze_button": "🚀 Analysieren",
        "analyzing_spinner": "⏳ Text wird analysiert...",
        "classified_args_header": "Klassifizierte Argumente",
        "argument_tree_header": "Argumentbaum-Struktur",
        "structure_stats_header": "Strukturstatistiken",
        "sentiment_header": "Stimmungs- & Emotionsanalyse",
        "weaknesses_header": "Erkannte logische Schwächen & Tr Trugschlüsse",
        "breakdown_header": "Detaillierte Aufschlüsselung",
        "visualizations_header": "📊 Umfassende Visualisierungen",
        "analysis_complete": "✅ Analyse abgeschlossen!",
        "warning_no_text": "⚠️ Bitte geben Sie einen Text zur Analyse ein",
        "results_header": "📊 Analyseergebnisse",
        "error_analysis": "❌ Fehler bei der Analyse: {error}",
    },
}


def t(lang: str, key: str, **kwargs) -> str:
    """Return translated string for given language and key.

    Falls der Schlüssel nicht existiert, wird der Schlüssel selbst
    zurückgegeben (nützlich während der Entwicklung).
    """
    template = LANGUAGES.get(lang, LANGUAGES["en"]).get(key, key)
    try:
        return template.format(**kwargs)
    except Exception:
        return template
