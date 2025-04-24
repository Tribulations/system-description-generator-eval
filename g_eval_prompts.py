import textwrap

def get_task_introduction_prompt(metric_name):
    metric_name = metric_name.lower()
    
    task_introduction = textwrap.dedent(f"""
    You will be given a high-level description of an existing software system. 
    This description is intended for developers who will maintain, extend, or contribute new code to the system. 
    Your task is to evaluate the {metric_name.upper()} of this description without comparing it to any reference text. 
    Assign a score for {metric_name} on a scale of 1 to 5, where 1 is the lowest and 5 is the highest based on the Evaluation Criteria.
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
