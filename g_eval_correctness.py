from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from g_eval_prompts import correctness_evaluation_criteria, get_task_introduction_prompt
from sdg_eval import sdg_llm_json_input, generated_description

sdg_task_template = """
Given the following knowledge graph in JSON format representing Java software system at a high level:
{}
**Task:**
Provide a **concise and structured high-level summary** of the system’s behavior and structure.
Your response must include:
1. **System Purpose:** Clearly state the system's primary function.
2. **Key Components & Responsibilities:** Briefly describe the major components and their roles.
3. **Core Technologies & Dependencies:** Explicitly confirm the technologies used and dependencies.
**Response Guidelines:**
- Keep the summary **brief yet informative**.
- Use **direct and factual statements** instead of speculation.
- Ensure the response is structured and easy to understand.
- **Avoid** using uncertain language like "might", "could", "may", etc.
- Do not return your response as JSON."""


task_template_and_kg_data = sdg_task_template.format(sdg_llm_json_input)

model = "gpt-4o"
metric = "Correctness"

evaluation_instructions = "{}{}"
evaluation_instructions = evaluation_instructions.format(get_task_introduction_prompt(metric), correctness_evaluation_criteria)

evaluation_steps = [
    "Read the high-level description carefully and identify any technical concepts or components mentioned in the description.",
    "Evaluate the description for any technical errors or logical inconsistencies in the explanation of these concepts and components.",
    "Assign a correctness score based on the number and severity of technical inaccuracies found, following the given scale from 1 to 5.",
    "Ensure that the assigned score aligns with the evaluation criteria, considering whether the inaccuracies would hinder maintenance or extension work."
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
