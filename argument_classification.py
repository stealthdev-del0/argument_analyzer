"""
Argument Classification Module: Klassifiziert Sätze nach Argumenttyp
"""

from typing import List, Dict
from dataclasses import dataclass
from claim_detection import ClaimDetector, ClaimResult
from emotion_analysis import EmotionAnalyzer, EmotionResult


@dataclass
class ArgumentClassification:
    """Vollständige Klassifikation eines Arguments"""
    sentence_text: str
    argument_type: str  # "CLAIM", "SUPPORT", "COUNTER", "NEUTRAL"
    confidence: float
    sentiment: str
    emotionality: float
    keywords: List[str]
    strength: float  # 0.0 - 1.0: Wie stark ist das Argument


class ArgumentClassifier:
    """Kombiniert verschiedene Analysen zur Argument-Klassifikation"""
    
    def __init__(self):
        """Initialisiert Classifier mit Submodulen"""
        self.claim_detector = ClaimDetector()
        self.emotion_analyzer = EmotionAnalyzer()
    
    def classify_arguments(self, sentences: List) -> List[ArgumentClassification]:
        """
        Klassifiziert alle Sätze nach Argumenttyp und Qualität
        Args:
            sentences: Liste von Sentence-Objekten
        Returns:
            Liste von ArgumentClassification-Objekten
        """
        # Nutze vorhandene Detektoren
        claim_results = self.claim_detector.detect_claims(sentences)
        emotion_results = self.emotion_analyzer.analyze_emotions(sentences)
        
        classifications = []
        for claim_result, emotion_result in zip(claim_results, emotion_results):
            classification = self._combine_analyses(claim_result, emotion_result)
            classifications.append(classification)
        
        return classifications
    
    def _combine_analyses(self, claim_result: ClaimResult, emotion_result: EmotionResult) -> ArgumentClassification:
        """
        Kombiniert Claim- und Emotionsanalyse
        Args:
            claim_result: Claim-Erkennungsergebnis
            emotion_result: Emotionsanalyse-Ergebnis
        Returns:
            Kombinierte Klassifikation
        """
        # Berechne Argument-Stärke basierend auf verschiedenen Faktoren
        strength = self._calculate_argument_strength(claim_result, emotion_result)
        
        return ArgumentClassification(
            sentence_text=claim_result.sentence_text,
            argument_type=claim_result.claim_type,
            confidence=claim_result.confidence,
            sentiment=emotion_result.sentiment,
            emotionality=emotion_result.emotionality,
            keywords=claim_result.markers + emotion_result.emotion_keywords,
            strength=strength
        )
    
    def _calculate_argument_strength(self, claim_result: ClaimResult, emotion_result: EmotionResult) -> float:
        """
        Berechnet Stärke eines Arguments (0-1)
        
        Stärkere Argumente haben:
        - Höhere Claim-Confidence
        - Moderates Sentiment (nicht zu emotional)
        - Logische Marker statt emotionale
        
        Args:
            claim_result: Claim-Result
            emotion_result: EmotionResult
        Returns:
            Strength Score 0.0 - 1.0
        """
        # Claim-Confidence ist wichtig
        confidence_factor = claim_result.confidence
        
        # Emotionalität sollte moderat sein (zu viel = schwächer)
        # Aber neutraler Score ist verdächtig
        emotionality_penalty = abs(emotion_result.emotionality - 0.3)
        emotionality_factor = max(0.5, 1.0 - emotionality_penalty)
        
        # Sentiment negativer Gegenargumente ist normal
        if claim_result.claim_type == "COUNTER":
            sentiment_neutral_bonus = 0.2 if emotion_result.sentiment == "negative" else -0.1
        else:
            sentiment_neutral_bonus = 0.2 if emotion_result.sentiment in ["positive", "neutral"] else -0.1
        
        # Kombiniere Faktoren
        strength = (
            confidence_factor * 0.5 +
            emotionality_factor * 0.3 +
            (0.5 + sentiment_neutral_bonus) * 0.2
        )
        
        return min(1.0, max(0.0, strength))
    
    def get_argument_summary(self, classifications: List[ArgumentClassification]) -> Dict:
        """
        Gibt Zusammenfassung aller Argumente
        Args:
            classifications: Liste von ArgumentClassification
        Returns:
            Dictionary mit Statistiken
        """
        types = {"CLAIM": [], "SUPPORT": [], "COUNTER": [], "NEUTRAL": []}
        
        for cls in classifications:
            types[cls.argument_type].append(cls)
        
        summary = {}
        for arg_type, items in types.items():
            summary[arg_type] = {
                "count": len(items),
                "avg_strength": sum(c.strength for c in items) / len(items) if items else 0.0,
                "avg_emotionality": sum(c.emotionality for c in items) / len(items) if items else 0.0,
                "examples": [c.sentence_text[:60] + "..." for c in items[:2]]  # Erste 2 Beispiele
            }
        
        return summary
    
    def get_strongest_arguments(self, classifications: List[ArgumentClassification], arg_type: str = None, top_n: int = 3) -> List[ArgumentClassification]:
        """
        Gibt stärkste Argumente zurück
        Args:
            classifications: Liste von ArgumentClassification
            arg_type: Nur diesen Typ (z.B. "CLAIM"), None = alle
            top_n: Wie viele zurückgeben
        Returns:
            Sortierte Liste nach Strength
        """
        if arg_type:
            filtered = [c for c in classifications if c.argument_type == arg_type]
        else:
            filtered = classifications
        
        return sorted(filtered, key=lambda c: c.strength, reverse=True)[:top_n]
    
    def detect_logical_weaknesses(self, classification: ArgumentClassification) -> List[str]:
        """
        Heuristische Erkennung logischer Schwächen
        Args:
            classification: ArgumentClassification-Objekt
        Returns:
            Liste von erkannten Schwächen
        """
        weaknesses = []
        text_lower = classification.sentence_text.lower()
        
        # Zu emotional → logisches Argument schwächer
        if classification.emotionality > 0.7:
            weaknesses.append("⚠️ Argument basiert stark auf Emotion statt Logik")
        
        # Viele Superlative deuten auf Übertreibung hin
        superlatives = ["absolutely", "definitely", "certainly", "obviously", "clearly"]
        superlative_count = sum(1 for s in superlatives if s in text_lower)
        if superlative_count >= 2:
            weaknesses.append("⚠️ Übertriebene Sicherheit (Superlative)")
        
        # Ad-Hominem Angriffe
        ad_hominem_words = ["stupid", "idiot", "fool", "moron", "ignorant"]
        if any(word in text_lower for word in ad_hominem_words):
            weaknesses.append("🔴 Ad-Hominem-Angriff erkannt (Angriff auf Person, nicht Argument)")
        
        # Verallgemeinerungen
        generalization_words = ["all", "never", "always", "everybody", "nobody"]
        if any(word in text_lower for word in generalization_words):
            weaknesses.append("⚠️ Mögliche unbegründete Verallgemeinerung")
        
        # Zirkelschluss-Muster
        if "is" in text_lower and text_lower.count("is") > 2:
            weaknesses.append("⚠️ Möglicher Zirkelschluss (zu viele 'ist' Aussagen)")
        
        # Fehlendes Belege
        if classification.argument_type == "SUPPORT" and "believe" in text_lower:
            weaknesses.append("⚠️ Glaubenssaussage statt Beweis")
        
        return weaknesses if weaknesses else ["✅ Keine offensichtlichen Schwächen erkannt"]


if __name__ == "__main__":
    from preprocessing import TextPreprocessor
    
    # Test
    processor = TextPreprocessor()
    classifier = ArgumentClassifier()
    
    sample_text = """
    Climate change is absolutely the most serious problem! 
    We must act now because the evidence overwhelmingly shows it.
    However, some stupid people disagree with this.
    Therefore, governments should implement stronger policies.
    """
    
    sentences = processor.process_text(sample_text)
    classifications = classifier.classify_arguments(sentences)
    
    print("=" * 60)
    print("ARGUMENT CLASSIFICATION")
    print("=" * 60)
    
    for cls in classifications:
        icon = "🟢" if cls.argument_type == "CLAIM" else \
               "🔵" if cls.argument_type == "SUPPORT" else \
               "🟣" if cls.argument_type == "COUNTER" else "⚪"
        
        print(f"\n{icon} {cls.argument_type} | Strength: {cls.strength:.2f} | Confidence: {cls.confidence:.2f}")
        print(f"   Text: {cls.sentence_text}")
        print(f"   Sentiment: {cls.sentiment} | Emotionality: {cls.emotionality:.2f}")
        
        # Zeige Schwächen
        weaknesses = classifier.detect_logical_weaknesses(cls)
        for weakness in weaknesses:
            print(f"   {weakness}")
    
    print("\n" + "=" * 60)
    print("SUMMARY:")
    summary = classifier.get_argument_summary(classifications)
    for arg_type, stats in summary.items():
        print(f"\n{arg_type}: {stats['count']} Arguments (avg strength: {stats['avg_strength']:.2f})")
