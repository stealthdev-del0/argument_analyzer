"""
Preprocessing Module: Satzsegmentierung, Tokenisierung, POS-Tags
"""

try:
    import spacy
    SPACY_AVAILABLE = True
except (ImportError, Exception):
    SPACY_AVAILABLE = False

from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Token:
    """Datenstruktur für Token mit Metadaten"""
    text: str
    pos: str  # POS-Tag
    lemma: str  # Lemma
    dep: str  # Dependency relation
    

@dataclass
class Sentence:
    """Datenstruktur für Satz mit Tokens"""
    text: str
    tokens: List[Token]
    doc_id: int  # Satz-Index im Dokument


class TextPreprocessor:
    """Verarbeitet Rohtexte für Analyse"""
    
    def __init__(self, model: str = "en_core_web_sm"):
        """
        Initialisiert TextPreprocessor (mit Fallback)
        Args:
            model: spaCy-Modellname
        """
        self.nlp = None
        self.use_fallback = True
        
        if SPACY_AVAILABLE:
            try:
                self.nlp = spacy.load(model)
                self.use_fallback = False
            except Exception as e:
                print(f"⚠️  spaCy nicht verfügbar: {e}")
                print(f"   Nutze Fallback-Tokenizer")
        else:
            print(f"⚠️  spaCy ist nicht installiert")
            print(f"   Nutze Fallback-Tokenizer (Regex-basiert)")
    
    def process_text(self, text: str) -> List[Sentence]:
        """
        Verarbeitet Text in Sätze und Tokens
        Args:
            text: Eingabe-Text
        Returns:
            Liste von Sentence-Objekten
        """
        if self.nlp:
            return self._process_with_spacy(text)
        else:
            return self._process_with_fallback(text)
    
    def _process_with_spacy(self, text: str) -> List[Sentence]:
        """Nutzt spaCy für Verarbeitung"""
        doc = self.nlp(text)
        sentences = []
        
        for sent_idx, sent in enumerate(doc.sents):
            tokens = []
            for token in sent:
                tobj = Token(
                    text=token.text,
                    pos=token.pos_,
                    lemma=token.lemma_,
                    dep=token.dep_
                )
                tokens.append(tobj)
            
            sentence = Sentence(
                text=sent.text,
                tokens=tokens,
                doc_id=sent_idx
            )
            sentences.append(sentence)
        
        return sentences
    
    def _process_with_fallback(self, text: str) -> List[Sentence]:
        """Fallback-Tokenizer (einfache Regex-basierte Sätze)"""
        import re
        
        # Einfache Satz-Segmentierung
        sentence_pattern = r'[^.!?]*[.!?]'
        sent_texts = re.findall(sentence_pattern, text)
        
        sentences = []
        for sent_idx, sent_text in enumerate(sent_texts):
            sent_text = sent_text.strip()
            if not sent_text:
                continue
            
            # Einfache Tokenisierung
            word_pattern = r'\w+'
            word_tokens = re.findall(word_pattern, sent_text.lower())
            
            tokens = []
            for word in word_tokens:
                tobj = Token(
                    text=word,
                    pos="UNKNOWN",  # Fallback: keine POS-Info
                    lemma=word,
                    dep="UNKNOWN"
                )
                tokens.append(tobj)
            
            sentence = Sentence(
                text=sent_text,
                tokens=tokens,
                doc_id=sent_idx
            )
            sentences.append(sentence)
        
        return sentences
    
    def get_dependency_tree(self, sentence: Sentence) -> Dict:
        """
        Extrahiert Dependency-Parse-Baum eines Satzes
        Args:
            sentence: Satz-Objekt
        Returns:
            Dictionary mit Struktur
        """
        tree = {}
        for token in sentence.tokens:
            tree[token.text] = {
                "pos": token.pos,
                "dep": token.dep,
                "lemma": token.lemma
            }
        return tree
    
    def extract_verbs(self, sentence: Sentence) -> List[str]:
        """
        Extrahiert Verben aus einem Satz
        Args:
            sentence: Satz-Objekt
        Returns:
            Liste von Verben (Lemmas)
        """
        return [token.lemma for token in sentence.tokens if token.pos in ["VERB", "AUX"]]
    
    def extract_entities(self, text: str) -> List[Tuple[str, str]]:
        """
        Extrahiert Named Entities
        Args:
            text: Eingabe-Text
        Returns:
            Liste von (Entity, Label) Tupel
        """
        if not self.nlp:
            return []  # Fallback: keine Entities
        
        doc = self.nlp(text)
        return [(ent.text, ent.label_) for ent in doc.ents]
    
    def get_sentence_stats(self, sentence: Sentence) -> Dict:
        """
        Gibt Statistiken über einen Satz
        Args:
            sentence: Satz-Objekt
        Returns:
            Dictionary mit Stats
        """
        return {
            "text": sentence.text,
            "token_count": len(sentence.tokens),
            "pos_tags": [t.pos for t in sentence.tokens],
            "verbs": self.extract_verbs(sentence),
            "avg_token_length": sum(len(t.text) for t in sentence.tokens) / len(sentence.tokens) if sentence.tokens else 0
        }


if __name__ == "__main__":
    # Teste Preprocessing
    processor = TextPreprocessor()
    
    sample_text = """
    Climate change is a serious problem. We must act now because the evidence is overwhelming.
    Some people disagree, but they ignore the data. Therefore, governments should implement stronger policies.
    """
    
    sentences = processor.process_text(sample_text)
    
    print("=" * 60)
    print("PREPROCESSING RESULTS")
    print("=" * 60)
    
    for sent in sentences:
        print(f"\n📄 Satz {sent.doc_id}: {sent.text}")
        stats = processor.get_sentence_stats(sent)
        print(f"   Tokens: {stats['token_count']} | Verben: {stats['verbs']}")
        print(f"   POS-Tags: {stats['pos_tags'][:5]}...")
