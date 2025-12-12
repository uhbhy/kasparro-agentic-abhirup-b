# src/agents/content_agent.py

# --- LangChain import (modern) ---
from langchain.chat_models import ChatOpenAI as OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from templates.templates import load_template_defs, TemplateEngine
from blocks.transform_blocks import generate_summary, generate_benefits_block, extract_usage_block, extract_safety_block
from typing import Dict
from config import OPENAI_API_KEY, DEFAULT_TEMPERATURE

class ContentAgent:
    """
    Responsibility: produce product_page JSON using template engine and blocks.
    """

    def __init__(self, template_defs_path: str):
        self.template_defs = load_template_defs(template_defs_path)
        self.engine = TemplateEngine(self.template_defs)

        # Initialize ChatOpenAI
        if OPENAI_API_KEY:
            self.llm = OpenAI(openai_api_key=OPENAI_API_KEY, temperature=DEFAULT_TEMPERATURE)
        else:
            self.llm = OpenAI(temperature=DEFAULT_TEMPERATURE)

        self.explain_prompt = PromptTemplate(
            input_variables=["block", "product_summary"],
            template=(
                "Write a concise explanatory sentence for this block:\n\n{block}\n\n"
                "Use the product summary: {product_summary}\n\n"
                "One sentence only."
            )
        )

    def create_product_page(self, product: Dict) -> Dict:
        summary = generate_summary(product)
        benefits_block = generate_benefits_block(product)
        usage_block = extract_usage_block(product)
        safety_block = extract_safety_block(product)

        # optionally call LLM to generate a nicer summary sentence
        chain = LLMChain(llm=self.llm, prompt=self.explain_prompt)
        nice_summary = chain.run({"block": "product one-line summary", "product_summary": summary})

        context = {
            "title": product["product_name"],
            "summary": nice_summary.strip(),
            "ingredients": product["key_ingredients"],
            "benefits_block": benefits_block,
            "usage": usage_block,
            "safety": safety_block,
            "price": f"₹{product['price_inr']}"
        }
        return self.engine.render("product_page", context)
