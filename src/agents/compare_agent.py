# src/agents/compare_agent.py

# --- LangChain import (modern) ---
from langchain.chat_models import ChatOpenAI as OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from typing import Dict
from blocks.compare_blocks import compare_ingredients, compare_benefits
from templates.templates import load_template_defs, TemplateEngine
from config import OPENAI_API_KEY, DEFAULT_TEMPERATURE

class CompareAgent:
    """
    Responsibility:
    - Create a fictional Product B (structured)
    - Run comparison logic blocks
    - Produce comparison_page JSON via template engine
    """
    def __init__(self, template_defs_path: str):
        self.template_defs = load_template_defs(template_defs_path)
        self.engine = TemplateEngine(self.template_defs)

        # Initialize ChatOpenAI
        if OPENAI_API_KEY:
            self.llm = OpenAI(openai_api_key=OPENAI_API_KEY, temperature=DEFAULT_TEMPERATURE)
        else:
            self.llm = OpenAI(temperature=DEFAULT_TEMPERATURE)

        self.make_b_prompt = PromptTemplate(
            input_variables=["product_summary"],
            template=(
                "Create a fictional competitor product B based on the product summary below.\n"
                "Return strictly a JSON object with fields: product_name, key_ingredients (array), benefits (array), price_inr (number).\n\n"
                "Product summary:\n{product_summary}\n\n"
                "Constraints: do not invent external facts; keep ingredients plausible and price reasonable (not 0)."
            )
        )

    def synthesize_product_b(self, product: Dict) -> Dict:
        summary = f"{product['product_name']} — {product['concentration']}, ingredients: {', '.join(product['key_ingredients'])}"
        chain = LLMChain(llm=self.llm, prompt=self.make_b_prompt)
        resp = chain.run({"product_summary": summary})
        import re, json
        match = re.search(r'(\{.*\})', resp, re.S)
        if match:
            try:
                return json.loads(match.group(1))
            except Exception:
                pass
        # fallback fictional product
        return {
            "product_name": "RadiantC Booster",
            "key_ingredients": ["Vitamin C", "Niacinamide"],
            "benefits": ["Brightening", "Evens tone"],
            "price_inr": 799
        }

    def create_comparison(self, product_a: Dict) -> Dict:
        product_b = self.synthesize_product_b(product_a)
        ingredient_comp = compare_ingredients(product_a, product_b)
        benefits_comp = compare_benefits(product_a, product_b)
        context = {
            "title": f"Comparison: {product_a['product_name']} vs {product_b['product_name']}",
            "product_a": product_a,
            "product_b": product_b,
            "ingredient_comparison": ingredient_comp,
            "benefits_comparison": benefits_comp,
            "price_comparison": {"a": product_a["price_inr"], "b": product_b["price_inr"]}
        }
        return self.engine.render("comparison_page", context)
