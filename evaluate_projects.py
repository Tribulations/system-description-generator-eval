import os
import csv
from datetime import datetime
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from prompts import (
    sdg_task_template, 
    get_task_introduction_prompt, 
    correctness_evaluation_criteria,
    relevance_evaluation_criteria,
    usefulness_evaluation_criteria,
    correctness_evaluation_steps,
    relevance_evaluation_steps,
    usefulness_evaluation_steps
)
from dotenv import load_dotenv

load_dotenv()

def evaluate_project(project_name, model="gpt-4o", verbose=False):
    """
    Evaluate a project using all three metrics (correctness, relevance, usefulness)
    and return the results.
    
    Args:
        project_name (str): Name of the project to evaluate
        model (str): The LLM model to use for evaluation
        verbose (bool): Whether to print detailed output
        
    Returns:
        dict: Dictionary containing scores and reasons for each metric
    """
    print(f"\n=== Evaluating project: {project_name} ===\n")
    
    # Define file paths to the JSON and description files
    json_path = f"evaluation/g-eval/{project_name}/{project_name}.json"
    desc_path = f"evaluation/g-eval/{project_name}/desc.md"
    
    # Check if files exist
    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at {json_path}")
        return None
    
    if not os.path.exists(desc_path):
        print(f"Error: Description file not found at {desc_path}")
        return None
    
    # Read description and JSON files
    try:
        with open(json_path, "r") as file:
            sdg_llm_json_input = file.read()
        
        with open(desc_path, "r") as file:
            generated_description = file.read()
    except Exception as e:
        print(f"Error reading files: {e}")
        return None
    
    # Prepare task prompt and knowledge graph data
    task_template_and_kg_data = sdg_task_template.format(sdg_llm_json_input)
    
    # Create test case
    test_case = LLMTestCase(
        input=task_template_and_kg_data,
        actual_output=generated_description,
    )
    
    # The evaluation criteria for each metric
    metric_evaluation_criteria = {
        "Correctness": correctness_evaluation_criteria,
        "Relevance": relevance_evaluation_criteria,
        "Usefulness": usefulness_evaluation_criteria
    }
    
    # Dictionary to store results for each metric
    results = {}
    
    # Run each metric
    for metric_name, evaluation_criteria in metric_evaluation_criteria.items():
        print(f"\n--- Running {metric_name} evaluation ---")
        
        # Prepare evaluation instructions
        evaluation_instructions = "{}{}"
        evaluation_instructions = evaluation_instructions.format(
            get_task_introduction_prompt(metric_name), 
            evaluation_criteria
        )
        
        g_eval = GEval(
            name=metric_name,
            criteria=evaluation_instructions,
            evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.INPUT],
            model=model,
            verbose_mode=verbose,
            evaluation_steps=get_evaluation_steps(metric_name)
        )
        
        # Run the measurement
        g_eval.measure(test_case)
        
        # Store results
        results[metric_name.lower()] = {
            'score': g_eval.score,
            'reason': g_eval.reason
        }
        
        # Print results
        print(f"Score: {g_eval.score}")
        if verbose:
            print(f"Reason: {g_eval.reason}")
    
    return results

def save_results_to_csv(results_dict, csv_path=None):
    """
    Save evaluation results to a CSV file.
    
    Args:
        results_dict (dict): Dictionary mapping project names to their evaluation results e.g., 
        {project_name: {metric_name: {score: 0.8, reason: "Reason for correctness"}}}
        
        csv_path (str, optional): Path to save the CSV file. If None, a new file is created.
        
    Returns:
        str: Path to the CSV file
    """
    # Create a new CSV file if path not provided
    if csv_path is None:
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = f"evaluation/g-eval/data_{current_datetime}.csv"
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    
    # Write results to CSV
    with open(csv_path, 'w', newline='') as csvfile:
        fieldnames = ['name', 'correctness', 'relevance', 'usefulness']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header
        writer.writeheader()
        
        # Write data for each project
        for project_name, metrics in results_dict.items():
            row = {'name': project_name}
            
            # Add scores for each metric
            for metric_name in ['correctness', 'relevance', 'usefulness']:
                if metric_name in metrics:
                    row[metric_name] = metrics[metric_name]['score']
                else:
                    row[metric_name] = 'N/A'  # Handle missing metrics
            
            writer.writerow(row)
    
    print(f"Results saved to: {csv_path}")
    return csv_path

def create_results_file(project_name, results):
    """
    Create a Markdown file with the results for a project.
    
    Args:
        project_name (str): Name of the project
        results (dict): Dictionary containing the results for each metric
    """
    # Create the results directory if it doesn't exist
    results_dir = f"evaluation/g-eval/{project_name}"
    os.makedirs(results_dir, exist_ok=True)
    
    # Get current date and time for the filename
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Path to the results file with datetime suffix
    results_file = f"{results_dir}/{project_name}_results_{current_datetime}.md"
    
    # Write results to file
    with open(results_file, "w") as file:
        # Add timestamp at the top of the file
        file.write(f"# Evaluation Results for {project_name}\n")
        file.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for metric, data in results.items():
            file.write(f"## {metric.capitalize()}\n")
            file.write(f"Score: {data['score']}\n\n")
            file.write(f"Reason: {data['reason']}\n\n")
    
    print(f"The projects results have been saved to: {results_file}")

def read_projects_file(file_path="projects_to_evaluate.md"):
    """
    Create the list of projects to evaluate from the projects_to_evaluate.md file.
    
    Args:
        file_path (str): Path to the projects file
        
    Returns:
        list: List of project names
    """
    projects = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Strip whitespace and skip empty lines
                project = line.strip().lower()
                if project:
                    projects.append(project)
        print(f"Read {len(projects)} projects from {file_path}")
    except FileNotFoundError:
        print(f"Warning: Projects file {file_path} not found. No projects to evaluate.")
    
    return projects

def main():
    # Read projects from the projects_to_evaluate.md file
    projects = read_projects_file()
    
    if not projects:
        print("No projects to evaluate. Please add projects to projects_to_evaluate.md file.")
        return
    
    print(f"Projects to evaluate: {', '.join(projects)}")
    
    # Dictionary to store all results
    all_results = {}
    
    # Run evaluation for each project
    for project_name in projects:
        results = evaluate_project(project_name)
        
        if results:
            # Store results
            all_results[project_name] = results
            
            create_results_file(project_name, results)
    
    # Save all results to CSV
    if all_results:
        save_results_to_csv(all_results)

def get_evaluation_steps(metric_name):
    if metric_name == "Correctness":
        return correctness_evaluation_steps
    elif metric_name == "Relevance":
        return relevance_evaluation_steps
    elif metric_name == "Usefulness":
        return usefulness_evaluation_steps

if __name__ == "__main__":
    main()
