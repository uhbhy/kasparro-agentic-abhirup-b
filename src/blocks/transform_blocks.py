from typing import Dict, List

def generate_summary(product: Dict) -> str:
    parts = [
        f"{product['product_name']} ({product['concentration']})",
        f"Formulated for {', '.join(product['skin_type'])} skin types.",
        f"Key ingredients include {', '.join(product['key_ingredients'])}.",
        f"Main benefits: {', '.join(product['benefits'])}."
    ]
    return " ".join(parts)

def generate_benefits_block(product: Dict) -> List[Dict]:
    return [{"title": b, "explanation": f"{b} — achieved via {', '.join(product['key_ingredients'])}."} for b in product["benefits"]]

def extract_usage_block(product: Dict) -> Dict:
    return {"how_to_use": product.get("how_to_use"), "frequency": "Once daily (morning)"} 

def extract_safety_block(product: Dict) -> Dict:
    return {"side_effects": product.get("side_effects"), "precaution": "Patch test before use."}
