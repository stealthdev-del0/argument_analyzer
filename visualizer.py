"""
Visualizer Module: Visualisiert Analyse-Ergebnisse im Terminal
"""

from typing import List, Dict
from argument_classification import ArgumentClassification
from structure_builder import StructureBuilder, ArgumentNode
from emotion_analysis import EmotionResult


class TerminalVisualizer:
    """Erstellt hübsche Terminal-Ausgaben der Analyse-Ergebnisse"""
    
    def __init__(self):
        """Initialisiert Visualizer"""
        self.width = 70
    
    def print_header(self, title: str):
        """Druckt schönen Header"""
        print("\n" + "=" * self.width)
        print(f"🧠 {title}")
        print("=" * self.width)
    
    def print_argument_analysis(self, classifications: List[ArgumentClassification]):
        """
        Druckt detaillierte Argument-Analyse
        Args:
            classifications: Klassifikations-Liste
        """
        self.print_header("ARGUMENT ANALYSIS")
        
        for i, cls in enumerate(classifications, 1):
            self._print_argument(i, cls)
    
    def _print_argument(self, num: int, cls: ArgumentClassification):
        """Druckt einzelnes Argument"""
        icon = self._get_argument_icon(cls.argument_type)
        
        print(f"\n[{num}] {icon} {cls.argument_type}")
        print(f"    Text: {cls.sentence_text}")
        
        # Confidence Bar
        confidence_bar = self._draw_bar(cls.confidence)
        print(f"    Confidence: {confidence_bar} {cls.confidence:.0%}")
        
        # Strength
        strength_bar = self._draw_bar(cls.strength)
        print(f"    Strength:   {strength_bar} {cls.strength:.0%}")
        
        # Emotionality
        emotion_bar = self._draw_bar(cls.emotionality)
        emotion_icon = "😊" if cls.sentiment == "positive" else "😠" if cls.sentiment == "negative" else "😐"
        print(f"    Emotion:    {emotion_bar} {cls.emotionality:.0%} {emotion_icon} {cls.sentiment}")
        
        # Keywords
        if cls.keywords:
            keywords_str = ", ".join(cls.keywords[:5])
            print(f"    Keywords:   {keywords_str}")
    
    def print_argument_summary(self, summary: Dict):
        """
        Druckt Zusammenfassung der Argument-Typen
        Args:
            summary: Dictionary mit Summary-Statistiken
        """
        self.print_header("ARGUMENT SUMMARY")
        
        for arg_type in ["CLAIM", "SUPPORT", "COUNTER", "NEUTRAL"]:
            if arg_type in summary:
                stats = summary[arg_type]
                count = stats["count"]
                avg_strength = stats["avg_strength"]
                
                icon = self._get_argument_icon(arg_type)
                bar = self._draw_bar(avg_strength)
                
                print(f"\n{icon} {arg_type}")
                print(f"    Count:       {count}")
                print(f"    Avg Strength: {bar} {avg_strength:.0%}")
                
                if stats["examples"]:
                    print(f"    Examples:")
                    for example in stats["examples"]:
                        print(f"      • {example}")
    
    def print_structure(self, builder: StructureBuilder):
        """
        Druckt Argument-Struktur (ASCII-Baum)
        Args:
            builder: StructureBuilder-Instanz
        """
        self.print_header("ARGUMENT STRUCTURE")
        
        tree_visualization = builder.visualize_ascii()
        print(tree_visualization)
        
        # Statistiken
        print("\n" + "-" * self.width)
        stats = builder.get_tree_stats()
        print(f"📊 Total Nodes: {stats['total_nodes']} | Depth: {stats['max_depth']}")
        print(f"   Claims: {stats['total_claims']} | Supports: {stats['total_supports']} | Counters: {stats['total_counters']}")
        print(f"   Avg Strength: {stats['avg_strength']:.2f}")
    
    def print_strongest_arguments(self, classifications: List[ArgumentClassification], top_n: int = 3):
        """
        Druckt stärkste Argumente
        Args:
            classifications: Klassifikations-Liste
            top_n: Wie viele zeigen
        """
        self.print_header(f"TOP {top_n} STRONGEST ARGUMENTS")
        
        sorted_args = sorted(classifications, key=lambda c: c.strength, reverse=True)[:top_n]
        
        for i, cls in enumerate(sorted_args, 1):
            icon = self._get_argument_icon(cls.argument_type)
            bar = self._draw_bar(cls.strength)
            
            print(f"\n#{i} {icon} {cls.argument_type} - Strength: {bar} {cls.strength:.0%}")
            print(f"    {cls.sentence_text}")
    
    def print_emotional_analysis(self, emotion_results: List[EmotionResult], summary: Dict):
        """
        Druckt emotionale Analyse
        Args:
            emotion_results: Emotions-Liste
            summary: Emotionals-Summary
        """
        self.print_header("EMOTIONAL ANALYSIS")
        
        # Overall Summary
        print(f"\n📊 Overall Sentiment:")
        print(f"    Positive: {summary['positive']} sentences")
        print(f"    Negative: {summary['negative']} sentences")
        print(f"    Neutral:  {summary['neutral']} sentences")
        
        sentiment_score = summary['avg_sentiment']
        sentiment_bar = self._draw_bar((sentiment_score + 1) / 2)  # Normalisiert zu 0-1
        print(f"    Avg Score: {sentiment_bar} {sentiment_score:+.2f}")
        
        print(f"\n😤 Average Emotionality: {summary['avg_emotionality']:.2f}")
        emotionality_bar = self._draw_bar(summary['avg_emotionality'])
        print(f"    {emotionality_bar}")
        
        # Sehr emotionale Sätze
        emotional_sentences = [r for r in emotion_results if r.emotionality > 0.6]
        if emotional_sentences:
            print(f"\n🔥 Highly Emotional Sentences ({len(emotional_sentences)}):")
            for r in emotional_sentences[:3]:
                print(f"    • {r.sentence_text}")
    
    def print_logical_weaknesses(self, classifications: List[ArgumentClassification], detector_func):
        """
        Druckt logische Schwächen
        Args:
            classifications: Klassifikations-Liste
            detector_func: Funktion(classification) -> List[str]
        """
        self.print_header("LOGICAL WEAKNESSES & FALLACIES")
        
        found_weaknesses = {}
        for cls in classifications:
            weaknesses = detector_func(cls)
            if any("⚠️" in w or "🔴" in w for w in weaknesses):
                found_weaknesses[cls.sentence_text] = weaknesses
        
        if found_weaknesses:
            for text, weaknesses in list(found_weaknesses.items())[:5]:
                print(f"\n❌ {text}")
                for weakness in weaknesses:
                    print(f"    {weakness}")
        else:
            print("\n✅ No major logical weaknesses detected!")
    
    def print_full_analysis(self, classifications: List[ArgumentClassification], 
                           builder: StructureBuilder, emotion_results: List[EmotionResult],
                           summary_dict: Dict, emotion_summary: Dict, detector_func):
        """
        Druckt komplette Analyse (All-in-One)
        Args:
            classifications: Klassifikationen
            builder: StructureBuilder
            emotion_results: Emotions-Ergebnisse
            summary_dict: Argument-Summary
            emotion_summary: Emotions-Summary
            detector_func: Weakness-Detector-Funktion
        """
        print("\n" + "🔬" * 35)
        print("🧠 ARGUMENT STRUCTURE ANALYZER - FULL ANALYSIS 🧠")
        print("🔬" * 35)
        
        self.print_argument_analysis(classifications)
        self.print_argument_summary(summary_dict)
        self.print_structure(builder)
        self.print_emotional_analysis(emotion_results, emotion_summary)
        self.print_logical_weaknesses(classifications, detector_func)
        self.print_strongest_arguments(classifications, top_n=3)
        
        self.print_footer()
    
    def print_footer(self):
        """Druckt schönen Footer"""
        print("\n" + "=" * self.width)
        print("✨ Analysis complete! Use this structure to understand argument flow.")
        print("=" * self.width + "\n")
    
    @staticmethod
    def _get_argument_icon(arg_type: str) -> str:
        """Gibt Icon für Argument-Typ"""
        icons = {
            "CLAIM": "🟢",
            "SUPPORT": "🔵",
            "COUNTER": "🟣",
            "NEUTRAL": "⚪"
        }
        return icons.get(arg_type, "⚪")
    
    @staticmethod
    def _draw_bar(value: float, width: int = 20) -> str:
        """
        Zeichnet einfach Fortschritts-Bar
        Args:
            value: Wert 0.0 - 1.0
            width: Breite in Zeichen
        Returns:
            Bar-String
        """
        filled = int(value * width)
        empty = width - filled
        return "[" + "█" * filled + "░" * empty + "]"


if __name__ == "__main__":
    from preprocessing import TextPreprocessor
    from argument_classification import ArgumentClassifier
    
    # Quick test
    processor = TextPreprocessor()
    classifier = ArgumentClassifier()
    builder = StructureBuilder()
    visualizer = TerminalVisualizer()
    
    sample_text = """
    Climate change is definitely a serious problem. We absolutely must act now!
    The evidence overwhelmingly shows it. However, some people disagree.
    Therefore, governments should implement stronger policies.
    """
    
    sentences = processor.process_text(sample_text)
    classifications = classifier.classify_arguments(sentences)
    builder.build_structure(classifications)
    
    visualizer.print_argument_summary(classifier.get_argument_summary(classifications))
