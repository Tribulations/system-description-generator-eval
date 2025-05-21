import textwrap

def get_task_introduction_prompt(metric_name):
    metric_name = metric_name.lower()

    task_introduction = textwrap.dedent(f"""
    You will be given a concise high-level description of an existing software system. 
    This description is intended for developers who will maintain, extend, or contribute new code to the system. 
    Your task is to evaluate the {metric_name.upper()} of this description without comparing it to any reference text. 
    Assign a score for {metric_name} on a scale of 1 to 5, where 1 is the lowest and 5 is the highest based on the Evaluation Criteria.
    Please carefully read and understand these instructions, keeping them available for reference throughout your evaluation.
    """)
    
    return task_introduction

correctness_evaluation_criteria = """
Correctness (1-5) How well the generated description aligns with the actual behavior and structure of the system.

1: Major inaccuracies, misleading or factually incorrect information about system components, behavior, or interactions
2: Frequent inaccuracies or misunderstandings of key architectural elements, with some information being correct but overall misleading
3: Mostly correct, with some minor errors or omissions, captures the main architectural elements but lacks important details
4: Generally correct and accurate, minor details may be missing or slightly imprecise, but the main structure and behavior are well described
5: Fully correct. Aligns with the system's behavior, structure, and architecture. Contains no factual errors
"""

relevance_evaluation_criteria = """
Relevance (1-5) - How well the generated description address the key components of the system, avoiding irrelevant details.

1: Entirely irrelevant to the system, it does not relate to the system at all
2: Mostly irrelevant, only minor parts relate to the high-level view of the system, but the majority does not
3: Partially relevant, describes some correct architectural elements but includes unnecessary or unrelated information
4: Mostly relevant. Nearly all content relates to the system, with only slight deviations
5: Fully relevant. All information directly relates to the described system and its architecture
"""

usefulness_evaluation_criteria = """
Usefulness (1-5) - How helpful the generated description would be to a developer trying to understand the system at a high-level.

1: Does not provide any actionable or insightful information for understanding the system
2: Provides little useful information. Most important, helpful information, are missing or unclear. Low support for comprehension
3: Provides a generally helpful overview for understanding the system. Includes some useful insights but could be clearer or more focused in certain parts
4: Provides clear and mostly useful insights into the system's architecture. Supports understanding with only minor gaps
5: Very useful. Offers actionable insights that significantly support understanding of the system's architecture
"""

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

correctness_evaluation_steps = [
    "Critically examine the system description against the provided knowledge graph data, identifying any factual errors or misrepresentations about components, relationships, or system behavior.",
    "Check for logical inconsistencies or contradictions within the description itself that would indicate a misunderstanding of the system architecture.",
    "Evaluate whether the technical terms and concepts used in the description are applied accurately and appropriately for the described system.",
    "Identify any statements that make unfounded assumptions beyond what's supported by the input data or that inappropriately extrapolate system functionality.",
    "Compare the system components and relationships mentioned in the input data against those described in the output to identify missing or incorrectly characterized elements.",
    "Assess whether the description captures the correct system purpose and primary functions according to the input data.",
    "Assign a correctness score, defaulting to a lower score (2-3) unless the description demonstrates exceptional accuracy and fidelity to the provided system information."
]

relevance_evaluation_steps = [
    "Critically analyze whether the description focuses on truly essential system components or dilutes its value with tangential information that would not help a developer understand the system's core functionality.",
    "Identify specific instances where the description introduces irrelevant technical details, unnecessary background information, or unfocused explanations that detract from understanding the system architecture.",
    "Assess whether the description maintains appropriate focus on the system's most important architectural elements or if it gives undue attention to minor or peripheral aspects.",
    "Check if the description provides information at a consistent and appropriate level of abstraction, or if it mixes high-level concepts with unnecessarily low-level details.",
    "Evaluate whether the description prioritizes information based on what would be most valuable to a developer approaching the system for the first time.",
    "Compare what was provided in the input data against what appears in the output to identify irrelevant information that doesn't correspond to the system described in the input.",
    "Assign a relevance score, defaulting to a lower score (2-3) unless the description demonstrates exceptional focus and appropriate selection of information."
]

usefulness_evaluation_steps = [
    "Examine the actual output critically, identifying specific areas where it fails to provide actionable insights or relies on generic descriptions rather than precise technical explanations.",
    "Identify missing technical details that would be essential for a developer to understand the system architecture - be specific about what information should have been included but wasn't.",
    "Assess whether the description provides concrete examples or merely abstract generalizations. Concrete examples should be weighted more heavily.",
    "Check if the description clearly explains component relationships and dependencies or if these connections are vague or implied.",
    "Evaluate whether technical terminology is used precisely and accurately or if terms are used in a way that suggests limited understanding.",
    "Compare what was provided in the input data against what appears in the output to identify missing or misrepresented information.",
    "Assign a usefulness score, defaulting to a lower score (3-4) unless the description demonstrates exceptional clarity and completeness."
]
