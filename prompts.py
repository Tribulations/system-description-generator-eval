import textwrap

def get_task_introduction_prompt(metric_name):
    metric_name = metric_name.lower()

    task_introduction_old = textwrap.dedent(f"""
    You will be given a concise high-level description of an existing software system. 
    This description is intended for developers who will maintain, extend, or contribute new code to the system. 
    Your task is to evaluate the {metric_name.upper()} of this description without comparing it to any reference text. 
    Assign a score for {metric_name} on a scale of 1 to 5, where 1 is the lowest and 5 is the highest based on the Evaluation Criteria.
    Please carefully read and understand these instructions, keeping them available for reference throughout your evaluation.
    """)

    task_introduction = textwrap.dedent(f"""
    You will be given a high-level description of an existing software system. 
    This description is intended for developers who will maintain, extend, or contribute new code to the system, but it is only meant as an INITIAL OVERVIEW, not a detailed technical specification.

    A good high-level description should:
    - Explain the system's primary purpose and functionality
    - Identify major components and their general responsibilities 
    - Mention key technologies and dependencies
    - Provide enough context for a developer to begin exploring the codebase

    A high-level description should NOT be expected to include:
    - Method-level details or class hierarchies
    - Implementation specifics
    - Detailed API references
    - Low-level technical intricacies

    Your task is to CRITICALLY evaluate the {metric_name.upper()} of this description based on its effectiveness as a high-level overview. Assign a score for {metric_name} on a scale of 1 to 5, where most descriptions should fall in the 2-3 range.

    Please carefully read and understand these instructions, keeping them available for reference throughout your evaluation.
    """)
    
    return task_introduction

correctness_evaluation_criteria = """
Correctness (1-5) - Evaluate the technical accuracy and logical consistency of the description.

1: Contains major technical errors or contradictions that would make maintenance work impossible
2: Has several technical inaccuracies or inconsistencies that would significantly hinder understanding the system
3: Generally correct but with some minor technical issues or ambiguities
4: Technically sound with very minor issues that wouldn't affect maintenance or extension work
5: Completely correct from a technical standpoint with no errors or inconsistencies
"""

relevance_evaluation_criteria = """
Relevance (1-5) - How well the description focuses on information that is useful for the developer who will maintain, extend, or contribute new code to the system. 
A high score means the information is practical, actionable, and at an appropriate level of detail.

1: Contains mostly irrelevant information or is at an inappropriate level of detail
2: Has significant amounts of irrelevant information or critically mismatches the developer's needs
3: Mostly relevant but contains some unnecessary information or lacks some detail
4: Highly relevant with minimal extraneous information
5: Perfectly tailored to the developer's implementation needs
"""

usefulness_evaluation_criteria = """
Usefulness (1-5) - How valuable the description would be to a developer working on the system.

1: Provides little to no actionable information for a developer
2: Contains some useful information but misses critical aspects needed for maintenance
3: Moderately useful but lacks detail in important areas
4: Very useful with most information a developer would need to understand the system
5: Exceptionally useful, providing comprehensive understanding that would enable confident code changes
"""

#### New prompts below for testing purposes

correctness_grading_schema = """
Correctness (1-5) How well the generated description aligns with the actual behavior and structure of the system.

1: Major inaccuracies, misleading or factually incorrect information about system components, behavior, or interactions
2: Frequent inaccuracies or misunderstandings of key architectural elements, with some information being correct but overall misleading
3: Mostly correct, with some minor errors or omissions, captures the main architectural elements but lacks important details
4: Generally correct and accurate, minor details may be missing or slightly imprecise, but the main structure and behavior are well described
5: Fully correct. Aligns with the system's behavior, structure, and architecture. Contains no factual errors
"""

relevance_grading_schema = """
Relevance (1-5) - How well the generated description address the key components of the system, avoiding irrelevant details.

1: Entirely irrelevant to the system, it does not relate to the system at all
2: Mostly irrelevant, only minor parts relate to the high-level view of the system, but the majority does not
3: Partially relevant, describes some correct architectural elements but includes unnecessary or unrelated information
4: Mostly relevant. Nearly all content relates to the system, with only slight deviations
5: Fully relevant. All information directly relates to the described system and its architecture
"""

usefulness_grading_schema = """
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
