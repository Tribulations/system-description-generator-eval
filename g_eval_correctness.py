from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from prompts import sdg_task_template, correctness_evaluation_criteria, get_task_introduction_prompt, correctness_grading_schema
from sdg_eval.sdg_eval import sdg_llm_json_input as df, generated_description as d

# File containing the data sent to the LLM from the SDG-tool
json_path = "evaluation/javaparser/javaparser.json"

# File containing the generated description to evaluate
gd_path = "evaluation/javaparser/javaparser_gd2.md"

# Read files and assign to variables
with open(json_path, "r") as file:
    sdg_llm_json_input = file.read()

with open(gd_path, "r") as file:
    generated_description = file.read()

# G-Eval needs the full prompt sent to the LLM from the SDG-tool as input
task_template_and_kg_data = sdg_task_template.format(sdg_llm_json_input)

model = "gpt-4o"
metric = "Correctness"

evaluation_instructions = "{}{}"
evaluation_instructions = evaluation_instructions.format(get_task_introduction_prompt(metric), correctness_grading_schema)

evaluation_steps2 = [
    "Read the high-level description carefully and identify any technical concepts or components mentioned in the description.",
    "Evaluate the description for any technical errors or logical inconsistencies in the explanation of these concepts and components.",
    "Assign a correctness score based on the number and severity of technical inaccuracies found, following the given scale from 1 to 5.",
    "Ensure that the assigned score aligns with the evaluation criteria, considering whether the inaccuracies would hinder maintenance or extension work."
]

evaluation_steps = [
    "Critically examine the system description against the provided knowledge graph data, identifying any factual errors or misrepresentations about components, relationships, or system behavior.",
    "Check for logical inconsistencies or contradictions within the description itself that would indicate a misunderstanding of the system architecture.",
    "Evaluate whether the technical terms and concepts used in the description are applied accurately and appropriately for the described system.",
    "Identify any statements that make unfounded assumptions beyond what's supported by the input data or that inappropriately extrapolate system functionality.",
    "Compare the system components and relationships mentioned in the input data against those described in the output to identify missing or incorrectly characterized elements.",
    "Assess whether the description captures the correct system purpose and primary functions according to the input data.",
    "Assign a correctness score, defaulting to a lower score (2-3) unless the description demonstrates exceptional accuracy and fidelity to the provided system information."
]

print(task_template_and_kg_data)

g_eval = GEval(
    name=metric,
    criteria=evaluation_instructions,
    evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.INPUT],
    model=model,
    verbose_mode=True,
    evaluation_steps=evaluation_steps
)

test_case = LLMTestCase(
    input=task_template_and_kg_data,
    actual_output=generated_description,
)

g_eval.measure(test_case)
