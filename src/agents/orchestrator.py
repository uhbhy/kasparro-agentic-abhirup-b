from typing import Dict
from agents.parser_agent import ParserAgent
from agents.qa_agent import QAAgent
from agents.content_agent import ContentAgent
from agents.compare_agent import CompareAgent
import json
import os

class Orchestrator:
    """
    Responsibility: orchestrator agent -> coordinates worker agents.
    Implements a clear DAG: parse -> qa generation -> content -> compare -> write outputs.
    """

    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        self.parser = ParserAgent()
        self.qa = QAAgent()
        self.content = ContentAgent(os.path.join(base_dir, "src", "templates", "template_defs.json"))
        self.compare = CompareAgent(os.path.join(base_dir, "src", "templates", "template_defs.json"))

    def run_pipeline(self, input_path: str, outputs_dir: str):
        product = self.parser.parse_from_file(input_path)

        # QA agent: generate questions and answers (model-driven)
        questions = self.qa.generate_questions(product, num=15)
        # answer them
        qas = []
        for q in questions:
            ans = self.qa.answer_question(q["question"], product)
            qas.append({"category": q.get("category","Uncategorized"), "question": q["question"], "answer": ans.strip()})

        faq_output = {"title": f"FAQ - {product['product_name']}", "questions": qas}

        # Content page
        product_page = self.content.create_product_page(product)

        # Comparison page
        comparison_page = self.compare.create_comparison(product)

        # write outputs as JSON
        os.makedirs(outputs_dir, exist_ok=True)
        with open(os.path.join(outputs_dir, "faq.json"), "w", encoding="utf-8") as f:
            json.dump(faq_output, f, ensure_ascii=False, indent=2)
        with open(os.path.join(outputs_dir, "product_page.json"), "w", encoding="utf-8") as f:
            json.dump(product_page, f, ensure_ascii=False, indent=2)
        with open(os.path.join(outputs_dir, "comparison_page.json"), "w", encoding="utf-8") as f:
            json.dump(comparison_page, f, ensure_ascii=False, indent=2)

        return {
            "faq": faq_output,
            "product_page": product_page,
            "comparison_page": comparison_page
        }
