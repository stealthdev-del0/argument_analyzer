"""
Structure Builder Module: Baut Argument-Graph und Struktur
"""

from typing import List, Dict, Optional
from dataclasses import dataclass, field
from argument_classification import ArgumentClassification


@dataclass
class ArgumentNode:
    """Knoten in der Argument-Struktur"""
    id: int
    text: str
    arg_type: str  # CLAIM, SUPPORT, COUNTER, NEUTRAL
    strength: float
    emotionality: float
    children: List['ArgumentNode'] = field(default_factory=list)
    parent: Optional['ArgumentNode'] = None
    
    def add_child(self, child: 'ArgumentNode'):
        """Fügt Child-Node hinzu"""
        self.children.append(child)
        child.parent = self
    
    def __str__(self) -> str:
        """String-Repräsentation"""
        return f"[{self.arg_type}] {self.text[:50]}..."


class StructureBuilder:
    """Baut Argument-Struktur und Graph aus Klassifizierungen"""
    
    def __init__(self):
        """Initialisiert Builder"""
        self.nodes: List[ArgumentNode] = []
        self.root_claims: List[ArgumentNode] = []
    
    def build_structure(self, classifications: List[ArgumentClassification]) -> List[ArgumentNode]:
        """
        Baut Argument-Struktur aus Klassifizierungen
        
        Struktur:
        CLAIM
         ├── SUPPORT
         ├── SUPPORT
         └── COUNTER
              └── REBUTTAL (implizit)
        
        Args:
            classifications: Liste von ArgumentClassification
        Returns:
            Liste von Root-Knoten (Claims)
        """
        # Erstelle Nodes
        nodes = []
        for idx, cls in enumerate(classifications):
            node = ArgumentNode(
                id=idx,
                text=cls.sentence_text,
                arg_type=cls.argument_type,
                strength=cls.strength,
                emotionality=cls.emotionality
            )
            nodes.append(node)
        
        # Identifiziere Hauptclaims
        claims = [n for n in nodes if n.arg_type == "CLAIM"]
        supports = [n for n in nodes if n.arg_type == "SUPPORT"]
        counters = [n for n in nodes if n.arg_type == "COUNTER"]
        
        # Wenn keine expliziten Claims, nutze stärksten Support als Claim
        if not claims and supports:
            strongest = max(supports, key=lambda n: n.strength)
            claims = [strongest]
        
        # Baue einfache Struktur: Claims bekommen Supports und Counters
        # (MVP: Naive nearest-neighbor Zuordnung)
        for claim in claims:
            # Assign Supports zum nächstgelegenen Claim
            for support in supports:
                # Einfache Heuristik: Positionen im Original-Text
                if support.id > claim.id:
                    claim.add_child(support)
            
            # Assign Counters zum nächstgelegenen Claim
            for counter in counters:
                if counter.id > claim.id:
                    claim.add_child(counter)
        
        self.nodes = nodes
        self.root_claims = claims
        
        return claims
    
    def get_argument_tree_dict(self, root: ArgumentNode, depth: int = 0) -> Dict:
        """
        Konvertiert Argument-Node zu Dictionary (für Visualisierung)
        Args:
            root: Root-Node
            depth: Aktuelle Tiefe (für Rekursion)
        Returns:
            Dictionary-Repräsentation
        """
        return {
            "id": root.id,
            "type": root.arg_type,
            "text": root.text,
            "strength": root.strength,
            "emotionality": root.emotionality,
            "children": [
                self.get_argument_tree_dict(child, depth + 1)
                for child in root.children
            ]
        }
    
    def get_tree_stats(self) -> Dict:
        """
        Gibt Statistiken über die Argument-Struktur
        Returns:
            Dictionary mit Stats
        """
        total_nodes = len(self.nodes)
        total_claims = sum(1 for n in self.nodes if n.arg_type == "CLAIM")
        total_supports = sum(1 for n in self.nodes if n.arg_type == "SUPPORT")
        total_counters = sum(1 for n in self.nodes if n.arg_type == "COUNTER")
        
        # Durchschnittliche Stärke
        avg_strength = sum(n.strength for n in self.nodes) / total_nodes if total_nodes > 0 else 0
        
        # Tiefe des tiefesten Baums
        max_depth = 0
        for claim in self.root_claims:
            depth = self._calculate_depth(claim)
            max_depth = max(max_depth, depth)
        
        return {
            "total_nodes": total_nodes,
            "total_claims": total_claims,
            "total_supports": total_supports,
            "total_counters": total_counters,
            "avg_strength": avg_strength,
            "max_depth": max_depth,
            "num_root_claims": len(self.root_claims)
        }
    
    def _calculate_depth(self, node: ArgumentNode) -> int:
        """Berechnet Tiefe eines Knoten-Subtrags"""
        if not node.children:
            return 1
        return 1 + max(self._calculate_depth(child) for child in node.children)
    
    def get_strongest_path(self) -> List[ArgumentNode]:
        """
        Gibt den Pfad von stärksten Argumenten zurück
        Returns:
            Liste von Nodes vom Root zum tiefsten starken Argument
        """
        if not self.root_claims:
            return []
        
        # Stärkster Root-Claim
        strongest_root = max(self.root_claims, key=lambda n: n.strength)
        path = [strongest_root]
        
        # Folge dem stärksten Kind
        current = strongest_root
        while current.children:
            strongest_child = max(current.children, key=lambda n: n.strength)
            path.append(strongest_child)
            current = strongest_child
        
        return path
    
    def get_counterargument_pairs(self) -> List[tuple]:
        """
        Findet Claim-Counter-Paare
        Returns:
            Liste von (Claim, Counter) Tupel
        """
        pairs = []
        for claim in self.root_claims:
            for child in claim.children:
                if child.arg_type == "COUNTER":
                    pairs.append((claim, child))
        return pairs
    
    def visualize_ascii(self) -> str:
        """
        Erstellt ASCII-Visualisierung der Struktur
        Returns:
            String mit ASCII-Baum
        """
        output = []
        for claim in self.root_claims:
            output.append(self._build_ascii_tree(claim))
        return "\n".join(output)
    
    def _build_ascii_tree(self, node: ArgumentNode, prefix: str = "", is_last: bool = True) -> str:
        """
        Rekursiv ASCII-Baum bauen
        Args:
            node: Node
            prefix: Präfix für Indentation
            is_last: Ist das letzte Sibling?
        Returns:
            ASCII-String
        """
        icon = "🟢" if node.arg_type == "CLAIM" else \
               "🔵" if node.arg_type == "SUPPORT" else \
               "🟣" if node.arg_type == "COUNTER" else "⚪"
        
        connector = "└── " if is_last else "├── "
        text = node.text[:60] + "..." if len(node.text) > 60 else node.text
        current_line = f"{prefix}{connector}{icon} [{node.arg_type}] {text}"
        
        lines = [current_line]
        
        extension = "    " if is_last else "│   "
        for i, child in enumerate(node.children):
            is_last_child = (i == len(node.children) - 1)
            child_tree = self._build_ascii_tree(child, prefix + extension, is_last_child)
            lines.append(child_tree)
        
        return "\n".join(lines)


if __name__ == "__main__":
    from preprocessing import TextPreprocessor
    from argument_classification import ArgumentClassifier
    
    # Test
    processor = TextPreprocessor()
    classifier = ArgumentClassifier()
    builder = StructureBuilder()
    
    sample_text = """
    Climate change is a serious problem. We must act now because the evidence is overwhelming.
    Research shows that temperatures are rising. However, some people disagree.
    Therefore, governments should implement stronger policies.
    """
    
    sentences = processor.process_text(sample_text)
    classifications = classifier.classify_arguments(sentences)
    
    # Baue Struktur
    root_nodes = builder.build_structure(classifications)
    
    print("=" * 60)
    print("ARGUMENT STRUCTURE")
    print("=" * 60)
    print(builder.visualize_ascii())
    
    print("\n" + "=" * 60)
    print("STRUCTURE STATISTICS:")
    stats = builder.get_tree_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n" + "=" * 60)
    print("STRONGEST ARGUMENT PATH:")
    path = builder.get_strongest_path()
    for i, node in enumerate(path):
        indent = "  " * i
        print(f"{indent}→ {node.arg_type}: {node.text[:50]}... (strength: {node.strength:.2f})")
