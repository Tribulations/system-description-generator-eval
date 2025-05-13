from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from prompts import sdg_task_template, get_task_introduction_prompt, usefulness_grading_schema
from dotenv import load_dotenv

load_dotenv()

# File containing the data sent to the LLM from the SDG-tool
json_path = "evaluation/g-eval/paimon/paimon.json"

# File containing the generated description to evaluate
gd_path = "evaluation//g-eval/paimon/desc.md"

# Read files and assign to variables
with open(json_path, "r") as file:
    sdg_llm_json_input = file.read()

with open(gd_path, "r") as file:
    generated_description = file.read()

# G-Eval needs the full prompt sent to the LLM from the SDG-tool as input
task_template_and_kg_data = sdg_task_template.format(sdg_llm_json_input)

model = "gpt-4o"
metric = "Usefulness"

evaluation_instructions = "{}{}"
evaluation_instructions = evaluation_instructions.format(get_task_introduction_prompt(metric), usefulness_grading_schema)

evaluation_steps = [
    "Examine the actual output critically, identifying specific areas where it fails to provide actionable insights or relies on generic descriptions rather than precise technical explanations.",
    "Identify missing technical details that would be essential for a developer to understand the system architecture - be specific about what information should have been included but wasn't.",
    "Assess whether the description provides concrete examples or merely abstract generalizations. Concrete examples should be weighted more heavily.",
    "Check if the description clearly explains component relationships and dependencies or if these connections are vague or implied.",
    "Evaluate whether technical terminology is used precisely and accurately or if terms are used in a way that suggests limited understanding.",
    "Compare what was provided in the input data against what appears in the output to identify missing or misrepresented information.",
    "Assign a usefulness score, defaulting to a lower score (3-4) unless the description demonstrates exceptional clarity and completeness."
]

g_eval = GEval(
    name=metric,
    criteria=evaluation_instructions,
    evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.INPUT],
    model=model,
    verbose_mode=False,
    evaluation_steps=evaluation_steps
)

test_case = LLMTestCase(
    input=task_template_and_kg_data,
    actual_output=generated_description,
)

g_eval.measure(test_case)

# Print the results
print(f"Score: {g_eval.score}")
print(f"Reason: {g_eval.reason}")
