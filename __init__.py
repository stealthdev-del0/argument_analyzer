"""
Argument Structure Analyzer - Main Package

Ein NLP-System zur Analyse von Argumentstrukturen in Texten.

USAGE:
    from argument_analyzer import main
    results = main("Your text here")

MODULES:
    preprocessing - Text-Verarbeitung
    claim_detection - Thesis-Erkennung
    emotion_analysis - Sentiment-Analyse
    argument_classification - Argument-Klassifikation
    structure_builder - Baum-Konstruktion
    visualizer - Terminal-Visualisierung
"""

__version__ = "1.0.0-MVP"
__author__ = "NLP Analyzer"

from preprocessing import TextPreprocessor
from claim_detection import ClaimDetector
from emotion_analysis import EmotionAnalyzer
from argument_classification import ArgumentClassifier
from structure_builder import StructureBuilder
from visualizer import TerminalVisualizer

__all__ = [
    "TextPreprocessor",
    "ClaimDetector",
    "EmotionAnalyzer",
    "ArgumentClassifier",
    "StructureBuilder",
    "TerminalVisualizer",
]
