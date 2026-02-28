"""
Emotion Analysis Module: Sentiment-Analyse und emotionale Sprache-Erkennung
"""

from typing import List, Dict
from dataclasses import dataclass
import re


@dataclass
class EmotionResult:
    """Ergebnis der Emotions-Analyse"""
    sentence_text: str
    sentiment: str  # "positive", "negative", "neutral"
    sentiment_score: float  # -1.0 bis +1.0
    emotionality: float  # 0.0 bis 1.0 (wie emotional ist die Sprache)
    emotion_keywords: List[str]


class EmotionAnalyzer:
    """Analysiert emotionale Sprache und Sentiment"""
    
    # Positive Wörter mit Gewicht
    POSITIVE_WORDS = {
        "good": 0.7, "great": 0.9, "excellent": 0.95, "wonderful": 0.9,
        "amazing": 0.95, "fantastic": 0.95, "beautiful": 0.8, "love": 0.85,
        "brilliant": 0.9, "perfect": 0.9, "wonderful": 0.9, "awesome": 0.9,
        "positive": 0.8, "benefit": 0.75, "success": 0.8, "help": 0.7,
        "support": 0.75, "agree": 0.6, "right": 0.6, "true": 0.65,
        "best": 0.85, "better": 0.75, "improve": 0.8
    }
    
    # Negative Wörter mit Gewicht
    NEGATIVE_WORDS = {
        "bad": 0.7, "terrible": 0.95, "awful": 0.95, "horrible": 0.95,
        "hate": 0.95, "dislike": 0.8, "wrong": 0.75, "evil": 0.95,
        "stupid": 0.9, "idiots": 0.95, "idiotic": 0.95, "ridiculous": 0.85,
        "absurd": 0.85, "nonsense": 0.85, "lies": 0.9, "failure": 0.8,
        "problem": 0.6, "issue": 0.5, "danger": 0.75, "dangerous": 0.85,
        "threat": 0.8, "destroy": 0.85, "crisis": 0.8, "disaster": 0.9,
        "blame": 0.7, "fault": 0.7, "worst": 0.9, "worse": 0.8,
        "negative": 0.7, "disagree": 0.6, "false": 0.75, "incorrect": 0.7
    }
    
    # Emotionale Intensivierungswörter (Exclamation, Großbuchstaben, etc.)
    INTENSITY_MARKERS = {
        "very": 1.2,
        "extremely": 1.3,
        "incredibly": 1.3,
        "absolutely": 1.3,
        "definitely": 1.2,
        "obviously": 1.1,
        "clearly": 1.1,
        "utterly": 1.3,
        "completely": 1.2,
        "totally": 1.2,
        "really": 1.15,
        "so": 1.15,
    }
    
    def __init__(self):
        """Initialisiert Analyzer"""
        self.all_words = {**self.POSITIVE_WORDS, **self.NEGATIVE_WORDS}
    
    def analyze_emotions(self, sentences: List) -> List[EmotionResult]:
        """
        Analysiert emotionale Inhalte in Sätzen
        Args:
            sentences: Liste von Sentence-Objekten
        Returns:
            Liste von EmotionResult-Objekten
        """
        results = []
        for sent in sentences:
            result = self._analyze_sentence(sent.text)
            results.append(result)
        return results
    
    def _analyze_sentence(self, text: str) -> EmotionResult:
        """
        Analysiert einzelnen Satz
        Args:
            text: Satz-Text
        Returns:
            EmotionResult
        """
        text_lower = text.lower()
        
        # Zähle positive und negative Wörter
        positive_score = 0.0
        negative_score = 0.0
        emotion_keywords = []
        intensity_multiplier = 1.0
        
        # Suche nach Intensitätswörtern
        for intensity_word, multiplier in self.INTENSITY_MARKERS.items():
            if intensity_word in text_lower:
                intensity_multiplier = max(intensity_multiplier, multiplier)
        
        # Zähle emotionale Wörter
        for word, weight in self.POSITIVE_WORDS.items():
            if word in text_lower:
                positive_score += weight * intensity_multiplier
                emotion_keywords.append(word)
        
        for word, weight in self.NEGATIVE_WORDS.items():
            if word in text_lower:
                negative_score += weight * intensity_multiplier
                emotion_keywords.append(word)
        
        # Extrapunkte für Großbuchstaben (SCREAMING)
        uppercase_ratio = sum(1 for c in text if c.isupper()) / len(text) if text else 0
        if uppercase_ratio > 0.3:  # Mehr als 30% Großbuchstaben
            emotion_keywords.append("CAPS_LOCK")
            positive_score += 0.3 * intensity_multiplier
            negative_score += 0.3 * intensity_multiplier
        
        # Extrapunkte für Ausrufezeichen
        exclamation_count = text.count("!")
        if exclamation_count > 0:
            emotion_keywords.append(f"!x{exclamation_count}")
            positive_score += 0.2 * exclamation_count
            negative_score += 0.15 * exclamation_count
        
        # Berechne Sentiment
        total_positive = positive_score
        total_negative = negative_score
        
        if total_positive + total_negative == 0:
            sentiment_score = 0.0
            sentiment = "neutral"
        else:
            sentiment_score = (total_positive - total_negative) / (total_positive + total_negative)
        
        if sentiment_score > 0.1:
            sentiment = "positive"
        elif sentiment_score < -0.1:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        # Emotionalität = wie emotional ist die Ausdrucksweise
        emotionality = min(1.0, (total_positive + total_negative) / 5.0)
        
        return EmotionResult(
            sentence_text=text,
            sentiment=sentiment,
            sentiment_score=sentiment_score,
            emotionality=emotionality,
            emotion_keywords=list(set(emotion_keywords))  # Duplikate entfernen
        )
    
    def get_emotional_sentences(self, results: List[EmotionResult], threshold: float = 0.5) -> List[EmotionResult]:
        """
        Filtert stark emotionale Sätze
        Args:
            results: EmotionResult-Liste
            threshold: Minimum Emotionality
        Returns:
            Gefilterte Liste
        """
        return [r for r in results if r.emotionality >= threshold]
    
    def get_sentiment_summary(self, results: List[EmotionResult]) -> Dict:
        """
        Gibt Zusammenfassung des Sentiments
        Args:
            results: EmotionResult-Liste
        Returns:
            Dictionary mit Statistiken
        """
        if not results:
            return {"positive": 0, "negative": 0, "neutral": 0, "avg_sentiment": 0.0}
        
        positive_count = sum(1 for r in results if r.sentiment == "positive")
        negative_count = sum(1 for r in results if r.sentiment == "negative")
        neutral_count = sum(1 for r in results if r.sentiment == "neutral")
        avg_sentiment = sum(r.sentiment_score for r in results) / len(results)
        avg_emotionality = sum(r.emotionality for r in results) / len(results)
        
        return {
            "positive": positive_count,
            "negative": negative_count,
            "neutral": neutral_count,
            "avg_sentiment": avg_sentiment,
            "avg_emotionality": avg_emotionality,
            "total_sentences": len(results)
        }


if __name__ == "__main__":
    from preprocessing import TextPreprocessor
    
    # Test mit Sample-Text
    processor = TextPreprocessor()
    analyzer = EmotionAnalyzer()
    
    sample_text = """
    Climate change is a terrible and disastrous problem! We absolutely must act NOW.
    Some stupid people disagree, but they are completely wrong. 
    This is actually a really positive step for our future.
    """
    
    sentences = processor.process_text(sample_text)
    results = analyzer.analyze_emotions(sentences)
    
    print("=" * 60)
    print("EMOTION ANALYSIS RESULTS")
    print("=" * 60)
    
    for result in results:
        emotion_icon = "😊" if result.sentiment == "positive" else \
                      "😠" if result.sentiment == "negative" else "😐"
        
        print(f"\n{emotion_icon} {result.sentiment.upper()} (score: {result.sentiment_score:+.2f})")
        print(f"   Emotionality: {result.emotionality:.2f} | Keywords: {result.emotion_keywords}")
        print(f"   Text: {result.sentence_text}")
    
    print("\n" + "=" * 60)
    summary = analyzer.get_sentiment_summary(results)
    print("SENTIMENT SUMMARY:")
    for key, value in summary.items():
        print(f"  {key}: {value}")
