from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from prompts import sdg_task_template, get_task_introduction_prompt, usefulness_evaluation_criteria, usefulness_evaluation_steps
from dotenv import load_dotenv

load_dotenv()

# File containing the data sent to the LLM from the SDG-tool
json_path = "evaluation/g-eval/javaparser/javaparser.json"

# File containing the generated description to evaluate
gd_path = "evaluation//g-eval/javaparser/desc.md"

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
evaluation_instructions = evaluation_instructions.format(get_task_introduction_prompt(metric), usefulness_evaluation_criteria)

evaluation_steps = usefulness_evaluation_steps

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
