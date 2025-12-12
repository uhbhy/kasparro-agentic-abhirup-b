# src/agents/qa_agent.py

# --- LangChain import (modern) ---
from langchain.chat_models import ChatOpenAI as OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from typing import Dict, List
from blocks.transform_blocks import generate_summary
import os
from config import OPENAI_API_KEY, DEFAULT_TEMPERATURE

class QAAgent:
    """
    Responsibility: create 15+ categorized user questions and generate answers for each.
    Uses LLM calls (LangChain). Does not hardcode the answers — uses model-driven generation.
    """

    def __init__(self):
        # Initialize ChatOpenAI from LangChain v1.x
        if OPENAI_API_KEY:
            self.llm = OpenAI(openai_api_key=OPENAI_API_KEY, temperature=DEFAULT_TEMPERATURE)
        else:
            # if no key present, fallback to default constructor (useful for local testing)
            self.llm = OpenAI(temperature=DEFAULT_TEMPERATURE)

        self.q_prompt = PromptTemplate(
            input_variables=["summary", "num"],
            template=(
                "You are an assistant that generates user-facing FAQs for a cosmetic product.\n"
                "Product summary:\n{summary}\n\n"
                "Generate {num} categorized questions across categories: Informational, Safety, Usage, Purchase, Comparison.\n"
                "Return JSON array of objects with 'category' and 'question' fields.\n"
                "Do not answer here — just generate questions."
            )
        )
        self.a_prompt = PromptTemplate(
            input_variables=["question", "product_summary"],
            template=(
                "You are an assistant that writes a short, accurate answer (1-2 sentences) to the question:\n\nQuestion: {question}\n\n"
                "Product summary:\n{product_summary}\n\n"
                "Answer concisely and factually using only the product information provided. If the question cannot be answered from the product data, say 'Not enough product data to answer.'"
            )
        )

    def generate_questions(self, product: Dict, num:int=15) -> List[Dict]:
        summary = generate_summary(product)
        chain = LLMChain(llm=self.llm, prompt=self.q_prompt)
        resp = chain.run({"summary": summary, "num": num})
        # we expect JSON-like; attempt to parse safely
        import json, re
        # try to extract json array using regex
        match = re.search(r'(\[.*\])', resp, re.S)
        if match:
            arr = match.group(1)
            try:
                qs = json.loads(arr)
                return qs
            except Exception:
                pass
        # fallback: naive split
        lines = [l.strip("- ").strip() for l in resp.splitlines() if l.strip()]
        qs = []
        for i,l in enumerate(lines):
            qs.append({"category":"Informational","question":l})
        return qs

    def answer_question(self, question: str, product: Dict) -> str:
        chain = LLMChain(llm=self.llm, prompt=self.a_prompt)
        return chain.run({"question": question, "product_summary": generate_summary(product)})
