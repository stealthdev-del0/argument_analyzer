"""
Claim Detection Module: Erkennung von Hauptthesen und Argumente-Markern
"""

from typing import List, Dict, Tuple
from dataclasses import dataclass
import re
from preprocessing import Sentence


@dataclass
class ClaimResult:
    """Ergebnis der Claim-Erkennung"""
    sentence_text: str
    confidence: float  # 0.0 - 1.0
    markers: List[str]  # Gefundene Marker
    claim_type: str  # "CLAIM", "SUPPORT", "COUNTER", "NEUTRAL"


class ClaimDetector:
    """Erkennt Thesen und argumentative Strukturen mittels Heuristiken"""
    
    # MVP: Einfache Keyword-Heuristiken
    CLAIM_MARKERS = {
        "therefore": 0.9,
        "thus": 0.9,
        "hence": 0.9,
        "so": 0.7,
        "conclude": 0.95,
        "conclusion": 0.95,
        "in conclusion": 0.95,
        "it is clear that": 0.9,
        "this shows that": 0.85,
        "this demonstrates": 0.85,
        "this proves": 0.9,
        "it follows that": 0.85,
    }
    
    SUPPORT_MARKERS = {
        "because": 0.85,
        "since": 0.8,
        "as": 0.6,  # Niedriger Score wegen Ambiguität
        "due to": 0.85,
        "caused by": 0.85,
        "for example": 0.75,
        "for instance": 0.75,
        "such as": 0.75,
        "like": 0.6,
        "in fact": 0.7,
        "indeed": 0.7,
        "furthermore": 0.75,
        "moreover": 0.75,
        "additionally": 0.75,
        "also": 0.65,
        "this supports": 0.9,
        "this proves": 0.85,
        "this shows": 0.85,
        "evidence": 0.8,
        "research shows": 0.85,
        "studies show": 0.85,
    }
    
    COUNTER_MARKERS = {
        "however": 0.8,
        "but": 0.85,
        "yet": 0.85,
        "although": 0.85,
        "though": 0.8,
        "despite": 0.85,
        "in spite of": 0.85,
        "on the other hand": 0.9,
        "conversely": 0.9,
        "by contrast": 0.9,
        "instead": 0.85,
        "rather": 0.75,
        "some people argue": 0.85,
        "others claim": 0.85,
        "critics say": 0.9,
        "opponents argue": 0.9,
        "this contradicts": 0.9,
        "disagree": 0.85,
        "counter-argument": 0.95,
    }
    
    MODAL_VERBS = {
        "should": 0.8,
        "must": 0.8,
        "ought": 0.8,
        "may": 0.6,
        "might": 0.6,
        "could": 0.6,
        "would": 0.6,
        "need to": 0.75,
        "have to": 0.7,
    }
    
    BELIEF_MARKERS = {
        "i believe": 0.85,
        "i think": 0.8,
        "in my opinion": 0.9,
        "my view": 0.9,
        "i argue": 0.9,
        "it seems": 0.7,
        "it appears": 0.7,
        "arguably": 0.85,
        "certainly": 0.75,
        "clearly": 0.75,
        "obviously": 0.75,
    }
    
    def __init__(self):
        """Initialisiert Detector"""
        self.all_markers = {
            "CLAIM": {**self.CLAIM_MARKERS, **self.MODAL_VERBS, **self.BELIEF_MARKERS},
            "SUPPORT": self.SUPPORT_MARKERS,
            "COUNTER": self.COUNTER_MARKERS,
        }
    
    def detect_claims(self, sentences: List[Sentence]) -> List[ClaimResult]:
        """
        Analysiert Sätze auf argumentative Struktur
        Args:
            sentences: Liste von Sentence-Objekten
        Returns:
            Liste von ClaimResult-Objekten
        """
        results = []
        for sent in sentences:
            result = self._analyze_sentence(sent)
            results.append(result)
        return results
    
    def _analyze_sentence(self, sentence: Sentence) -> ClaimResult:
        """
        Analysiert einzelnen Satz
        Args:
            sentence: Satz-Objekt
        Returns:
            ClaimResult
        """
        text_lower = sentence.text.lower()
        
        # Sammle Marker und Confidence-Scores pro Typ
        type_scores = {
            "CLAIM": [],
            "SUPPORT": [],
            "COUNTER": [],
            "NEUTRAL": [0.0]  # Default Neutral
        }
        
        found_markers = {
            "CLAIM": [],
            "SUPPORT": [],
            "COUNTER": [],
        }
        
        # Suche nach Markern
        for claim_type, markers in self.all_markers.items():
            for marker, confidence in markers.items():
                if marker in text_lower:
                    type_scores[claim_type].append(confidence)
                    found_markers[claim_type].append(marker)
        
        # Berechne beste Klassifikation
        claim_type = "NEUTRAL"
        confidence = 0.0
        markers = []
        
        for ctype, scores in type_scores.items():
            if scores:
                avg_score = sum(scores) / len(scores)
                if avg_score > confidence:
                    confidence = avg_score
                    claim_type = ctype
                    markers = found_markers[ctype]
        
        return ClaimResult(
            sentence_text=sentence.text,
            confidence=confidence,
            markers=markers,
            claim_type=claim_type
        )
    
    def get_main_claims(self, results: List[ClaimResult], threshold: float = 0.6) -> List[ClaimResult]:
        """
        Filtert nur Hauptclaims (hohe Confidence)
        Args:
            results: ClaimResult-Liste
            threshold: Minimum Confidence
        Returns:
            Gefilterte Liste
        """
        return [r for r in results if r.claim_type == "CLAIM" and r.confidence >= threshold]
    
    def get_argument_tree(self, results: List[ClaimResult]) -> Dict:
        """
        Vereinfachte Struktur der Argumente
        Args:
            results: ClaimResult-Liste
        Returns:
            Dictionary mit Struktur
        """
        claims = [r for r in results if r.claim_type == "CLAIM"]
        supports = [r for r in results if r.claim_type == "SUPPORT"]
        counters = [r for r in results if r.claim_type == "COUNTER"]
        
        return {
            "claims": [{"text": c.sentence_text, "confidence": c.confidence} for c in claims],
            "supports": [{"text": s.sentence_text, "confidence": s.confidence} for s in supports],
            "counters": [{"text": c.sentence_text, "confidence": c.confidence} for c in counters],
            "neutral": len([r for r in results if r.claim_type == "NEUTRAL"])
        }


if __name__ == "__main__":
    from preprocessing import TextPreprocessor
    
    # Test mit Sample-Text
    processor = TextPreprocessor()
    detector = ClaimDetector()
    
    sample_text = """
    Climate change is a serious problem. We must act now because the evidence is overwhelming.
    However, some people disagree with this conclusion. In my opinion, they ignore the data.
    Therefore, governments should implement stronger policies. This shows that action is necessary.
    """
    
    sentences = processor.process_text(sample_text)
    results = detector.detect_claims(sentences)
    
    print("=" * 60)
    print("CLAIM DETECTION RESULTS")
    print("=" * 60)
    
    for result in results:
        icon = "🟢" if result.claim_type == "CLAIM" else \
               "🔵" if result.claim_type == "SUPPORT" else \
               "🟣" if result.claim_type == "COUNTER" else "⚪"
        
        print(f"\n{icon} {result.claim_type} (confidence: {result.confidence:.2f})")
        print(f"   Text: {result.sentence_text}")
        print(f"   Markers: {result.markers}")
    
    print("\n" + "=" * 60)
    tree = detector.get_argument_tree(results)
    print("ARGUMENT STRUCTURE:")
    print(f"Claims: {len(tree['claims'])}")
    print(f"Supports: {len(tree['supports'])}")
    print(f"Counters: {len(tree['counters'])}")
