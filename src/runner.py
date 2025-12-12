from agents.orchestrator import Orchestrator
import os
BASE = os.path.dirname(os.path.dirname(__file__))

def main():
    input_path = os.path.join(BASE, "src", "data", "input_product.json")
    outputs_dir = os.path.join(BASE, "outputs")
    orch = Orchestrator(BASE)
    results = orch.run_pipeline(input_path, outputs_dir)
    print("Pipeline finished. Outputs written to", outputs_dir)

if __name__ == "__main__":
    main()
