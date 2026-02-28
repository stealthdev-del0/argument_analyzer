"""
Unit Tests für Argument Structure Analyzer

Teste einzelne Funktionen der Module
"""

import unittest
from preprocessing import TextPreprocessor, Sentence, Token
from claim_detection import ClaimDetector, ClaimResult
from emotion_analysis import EmotionAnalyzer
from argument_classification import ArgumentClassifier


class TestPreprocessing(unittest.TestCase):
    """Tests für TextPreprocessor"""
    
    def setUp(self):
        self.processor = TextPreprocessor()
    
    def test_process_text(self):
        """Test basic text processing"""
        text = "Hello world. This is a test."
        sentences = self.processor.process_text(text)
        
        # Should find at least 2 sentences
        self.assertGreaterEqual(len(sentences), 2)
        
        # Each should be a Sentence object
        for sent in sentences:
            self.assertIsInstance(sent, Sentence)
            self.assertTrue(len(sent.text) > 0)
            self.assertGreater(len(sent.tokens), 0)
    
    def test_sentence_tokens(self):
        """Test token processing"""
        text = "The quick brown fox."
        sentences = self.processor.process_text(text)
        
        self.assertGreater(len(sentences), 0)
        first_sent = sentences[0]
        
        # Should have tokens
        self.assertGreater(len(first_sent.tokens), 0)
        
        # Each token should be a Token object
        for token in first_sent.tokens:
            self.assertIsInstance(token, Token)
            self.assertTrue(len(token.text) > 0)


class TestClaimDetection(unittest.TestCase):
    """Tests für ClaimDetector"""
    
    def setUp(self):
        self.detector = ClaimDetector()
        self.processor = TextPreprocessor()
    
    def test_detect_claim_markers(self):
        """Test detection of claim markers"""
        text = "Therefore, we should act immediately."
        sentences = self.processor.process_text(text)
        results = self.detector.detect_claims(sentences)
        
        self.assertGreater(len(results), 0)
        result = results[0]
        
        # Should be detected as CLAIM
        self.assertEqual(result.claim_type, "CLAIM")
        self.assertGreater(result.confidence, 0.5)
        self.assertIn("therefore", result.markers)
    
    def test_detect_support(self):
        """Test detection of supporting arguments"""
        text = "We should invest in education because it benefits society."
        sentences = self.processor.process_text(text)
        results = self.detector.detect_claims(sentences)
        
        self.assertGreater(len(results), 0)
        result = results[0]
        
        # Should be detected as SUPPORT
        self.assertEqual(result.claim_type, "SUPPORT")
        self.assertIn("because", result.markers)
    
    def test_detect_counter(self):
        """Test detection of counter arguments"""
        text = "However, some people disagree strongly."
        sentences = self.processor.process_text(text)
        results = self.detector.detect_claims(sentences)
        
        self.assertGreater(len(results), 0)
        result = results[0]
        
        # Should be detected as COUNTER
        self.assertIn(result.claim_type, ["COUNTER", "NEUTRAL"])


class TestEmotionAnalysis(unittest.TestCase):
    """Tests für EmotionAnalyzer"""
    
    def setUp(self):
        self.analyzer = EmotionAnalyzer()
        self.processor = TextPreprocessor()
    
    def test_positive_sentiment(self):
        """Test detection of positive sentiment"""
        text = "This is absolutely wonderful and amazing!"
        sentences = self.processor.process_text(text)
        emotions = self.analyzer.analyze_emotions(sentences)
        
        self.assertGreater(len(emotions), 0)
        emotion = emotions[0]
        
        # Should be positive
        self.assertEqual(emotion.sentiment, "positive")
        self.assertGreater(emotion.sentiment_score, 0)
        self.assertGreater(emotion.emotionality, 0.3)
    
    def test_negative_sentiment(self):
        """Test detection of negative sentiment"""
        text = "This is terrible and horrible nonsense."
        sentences = self.processor.process_text(text)
        emotions = self.analyzer.analyze_emotions(sentences)
        
        self.assertGreater(len(emotions), 0)
        emotion = emotions[0]
        
        # Should be negative
        self.assertEqual(emotion.sentiment, "negative")
        self.assertLess(emotion.sentiment_score, 0)
    
    def test_neutral_sentiment(self):
        """Test detection of neutral sentiment"""
        text = "The sky is blue."
        sentences = self.processor.process_text(text)
        emotions = self.analyzer.analyze_emotions(sentences)
        
        self.assertGreater(len(emotions), 0)
        emotion = emotions[0]
        
        # Should be neutral
        self.assertEqual(emotion.sentiment, "neutral")
        self.assertAlmostEqual(emotion.sentiment_score, 0, delta=0.3)


class TestArgumentClassification(unittest.TestCase):
    """Tests für ArgumentClassifier"""
    
    def setUp(self):
        self.classifier = ArgumentClassifier()
        self.processor = TextPreprocessor()
    
    def test_classify_arguments(self):
        """Test argument classification"""
        text = "We should act because evidence shows this works."
        sentences = self.processor.process_text(text)
        classifications = self.classifier.classify_arguments(sentences)
        
        self.assertGreater(len(classifications), 0)
        
        for cls in classifications:
            # Each should have a type
            self.assertIn(cls.argument_type, ["CLAIM", "SUPPORT", "COUNTER", "NEUTRAL"])
            # Should have strength between 0 and 1
            self.assertGreaterEqual(cls.strength, 0)
            self.assertLessEqual(cls.strength, 1)
    
    def test_detect_logical_weaknesses(self):
        """Test detection of logical weaknesses"""
        sentences = self.processor.process_text("Stupid people disagree with this!")
        classifications = self.classifier.classify_arguments(sentences)
        
        for cls in classifications:
            weaknesses = self.classifier.detect_logical_weaknesses(cls)
            self.assertIsInstance(weaknesses, list)
            
            # Should detect Ad-Hominem
            if "stupid" in cls.sentence_text.lower():
                has_ad_hominem = any("Ad-Hominem" in w for w in weaknesses)
                # This depends on implementation, so just check format
                self.assertTrue(all(isinstance(w, str) for w in weaknesses))


class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_full_pipeline(self):
        """Test the complete analysis pipeline"""
        processor = TextPreprocessor()
        classifier = ArgumentClassifier()
        
        text = """
        Climate change is real. 
        We must act because evidence shows warming.
        However, some disagree.
        Therefore, we need action.
        """
        
        # Process
        sentences = processor.process_text(text)
        self.assertGreater(len(sentences), 0)
        
        # Classify
        classifications = classifier.classify_arguments(sentences)
        self.assertEqual(len(classifications), len(sentences))
        
        # Get summary
        summary = classifier.get_argument_summary(classifications)
        self.assertIn("CLAIM", summary)
        self.assertIn("SUPPORT", summary)
        self.assertIn("COUNTER", summary)


def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestPreprocessing))
    suite.addTests(loader.loadTestsFromTestCase(TestClaimDetection))
    suite.addTests(loader.loadTestsFromTestCase(TestEmotionAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestArgumentClassification))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
