from typing import Dict, List

def compare_ingredients(a: Dict, b: Dict) -> List[Dict]:
    a_set = set(a.get("key_ingredients", []))
    b_set = set(b.get("key_ingredients", []))
    return [
        {"ingredient": i, "in_a": i in a_set, "in_b": i in b_set}
        for i in sorted(list(a_set.union(b_set)))
    ]

def compare_benefits(a: Dict, b: Dict) -> List[Dict]:
    a_set = set(a.get("benefits", []))
    b_set = set(b.get("benefits", []))
    return [{"benefit": i, "in_a": i in a_set, "in_b": i in b_set} for i in sorted(list(a_set.union(b_set)))]
