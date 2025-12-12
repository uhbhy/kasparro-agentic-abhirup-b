from typing import Dict, Any
import json

def load_template_defs(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

class TemplateEngine:
    def __init__(self, template_defs: Dict[str, Any]):
        self.template_defs = template_defs

    def render(self, template_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        if template_name not in self.template_defs:
            raise ValueError(f"Unknown template: {template_name}")
        fields = self.template_defs[template_name]["fields"]
        output = {}
        for f in fields:
            output[f] = context.get(f)
        # simple validation rules
        rules = self.template_defs[template_name].get("rules", {})
        if rules.get("questions_min"):
            qs = output.get("questions") or []
            if len(qs) < rules["questions_min"]:
                raise ValueError(f"Template {template_name} requires at least {rules['questions_min']} questions")
        return output
