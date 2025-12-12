# kasparro-agentic-abhirup-basu

Agentic content generation system for Kasparro Applied AI assignment.

## How to run

1. Create and activate a virtualenv:
python -m venv venv
source venv/bin/activate # mac/linux
.\venv\Scripts\activate # windows

markdown
Copy code

2. Install:
pip install -r requirements.txt

vbnet
Copy code

3. Set your OpenAI key:
export OPENAI_API_KEY="sk-..."

markdown
Copy code

4. Run:
python src/main.py

pgsql
Copy code

Outputs will be written to `/outputs/faq.json`, `/outputs/product_page.json`, `/outputs/comparison_page.json`.

Design goals: LangChain-based agents, no global state, template engine, JSON structured output.
