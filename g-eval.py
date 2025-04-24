from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from g_eval_prompts import correctness_evaluation_criteria, relevance_evaluation_criteria, usefulness_evaluation_criteria, get_task_introduction_prompt
from sdg_eval import sdg_llm_json_input, generated_description

prompt_template = """
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

sdg_llm_prompt = prompt_template.format(sdg_llm_json_input)

model = "gpt-4o"
metric = "Relevance"

evaluation_instructions = "{}{}"
evaluation_instructions = evaluation_instructions.format(get_task_introduction_prompt(metric), relevance_evaluation_criteria)

g_eval = GEval(
    name=metric,
    criteria=evaluation_instructions.format(get_task_introduction_prompt(metric), relevance_evaluation_criteria),
    evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.INPUT],
    model=model,
    verbose_mode=True
)

test_case = LLMTestCase(
    input=sdg_llm_prompt,
    actual_output=generated_description,
)

g_eval.measure(test_case)
