from typing import Dict
import json

class ParserAgent:
    """
    Single responsibility: read raw product JSON and return a cleaned internal model.
    Input: path or dict
    Output: dict with normalized fields (strings, lists)
    """
    def __init__(self):
        pass

    def parse_from_file(self, path: str) -> Dict:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        return self._normalize(raw)

    def _normalize(self, raw: Dict) -> Dict:
        # minimal normalization to ensure predictable types
        model = {}
        model["product_name"] = raw.get("product_name")
        model["concentration"] = raw.get("concentration")
        st = raw.get("skin_type", [])
        if isinstance(st, str):
            st = [s.strip() for s in st.split(",")]
        model["skin_type"] = st
        model["key_ingredients"] = raw.get("key_ingredients", [])
        model["benefits"] = raw.get("benefits", [])
        model["how_to_use"] = raw.get("how_to_use")
        model["side_effects"] = raw.get("side_effects")
        model["price_inr"] = raw.get("price_inr")
        return model
