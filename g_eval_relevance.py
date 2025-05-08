from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from prompts import sdg_task_template, relevance_evaluation_criteria, get_task_introduction_prompt, relevance_grading_schema
from sdg_eval.sdg_eval import sdg_llm_json_input, generated_description

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
metric = "Relevance"

evaluation_instructions = "{}{}"
evaluation_instructions = evaluation_instructions.format(get_task_introduction_prompt(metric), relevance_grading_schema)

evaluation_steps2 = [
    "Evaluate the relevance of the input description by determining how well it addresses the needs of a developer tasked with maintaining, extending, or adding new code to the system.",
    "Assess whether the description contains practical and actionable information that is directly applicable to a developer's tasks and responsibilities within the system.",
    "Determine if the description maintains an appropriate level of detail, avoiding unnecessary information or critical gaps that could hinder a developer's understanding or implementation efforts.",
    "Assign a relevance score from 1 to 5 based on how closely the description aligns with the specified criteria, considering its practicality, actionability, and detail appropriateness for development tasks."
]

evaluation_steps = [
    "Critically analyze whether the description focuses on truly essential system components or dilutes its value with tangential information that would not help a developer understand the system's core functionality.",
    "Identify specific instances where the description introduces irrelevant technical details, unnecessary background information, or unfocused explanations that detract from understanding the system architecture.",
    "Assess whether the description maintains appropriate focus on the system's most important architectural elements or if it gives undue attention to minor or peripheral aspects.",
    "Check if the description provides information at a consistent and appropriate level of abstraction, or if it mixes high-level concepts with unnecessarily low-level details.",
    "Evaluate whether the description prioritizes information based on what would be most valuable to a developer approaching the system for the first time.",
    "Compare what was provided in the input data against what appears in the output to identify irrelevant information that doesn't correspond to the system described in the input.",
    "Assign a relevance score, defaulting to a lower score (2-3) unless the description demonstrates exceptional focus and appropriate selection of information."
]

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
