import subprocess
import os
from app.llm_utils import call_llm
from fuzzywuzzy import process 
from pathlib import Path

DATA_DIR = "data"

# def execute_task1(task: str):
#     """Parses and executes the given task description."""
#     if "install uv" in task and "run datagen.py" in task:
#         return run_datagen()
#     elif "count Wednesdays" in task:
#         return count_weekdays("Wednesday", "data/dates.txt", "data/dates-wednesdays.txt")
#     elif "extract email sender" in task:
#         return extract_email_sender()
#     elif "credit card number" in task:
#         return extract_credit_card()
#     else:
#         return "Task not recognized."

# def run_datagen():
#     """Runs the external datagen.py script"""
#     cmd = ["python3", "data/datagen.py"]
#     result = subprocess.run(cmd, capture_output=True, text=True)
#     return result.stdout if result.returncode == 0 else result.stderr

# def count_weekdays(weekday, input_file, output_file):
#     """Counts occurrences of a weekday in a file."""
#     with open(input_file, "r") as f:
#         dates = f.readlines()
#     count = sum(1 for date in dates if weekday in date)
#     with open(output_file, "w") as f:
#         f.write(str(count))
#     return f"Wrote count {count} to {output_file}"

# def extract_email_sender():
#     """Extracts email sender using LLM."""
#     with open("data/email.txt", "r") as f:
#         email_content = f.read()
#     prompt = f"Extract the sender email from the following email:\n{email_content}"
#     sender_email = call_llm(prompt)
#     with open("data/email-sender.txt", "w") as f:
#         f.write(sender_email)
#     return "Extracted sender email."

# def extract_credit_card():
#     """Extracts credit card number using LLM."""
#     from PIL import Image
#     img = Image.open("data/credit-card.png")
#     prompt = "Extract the credit card number from this image."
#     card_number = call_llm(prompt, image=img)
#     with open("data/credit-card.txt", "w") as f:
#         f.write(card_number.replace(" ", ""))
#     return "Extracted credit card number."


# def run_datagen():
#     """Runs the external datagen.py script."""
#     cmd = ["python3", "data/datagen.py"]
#     result = subprocess.run(cmd, capture_output=True, text=True)
#     return result.stdout if result.returncode == 0 else result.stderr

# def count_weekdays(weekday, input_file, output_file):
#     """Counts occurrences of a weekday in a file."""
#     input_path = Path(input_file)
#     output_path = Path(output_file)

#     if not input_path.exists():
#         return f"Error: {input_file} not found."

#     with input_path.open("r") as f:
#         dates = f.readlines()
#     count = sum(1 for date in dates if weekday in date)

#     with output_path.open("w") as f:
#         f.write(str(count))

#     return f"Wrote count {count} to {output_file}"

# def extract_email_sender():
#     """Extracts email sender using LLM."""
#     email_path = Path(DATA_DIR) / "email.txt"
#     output_path = Path(DATA_DIR) / "email-sender.txt"

#     if not email_path.exists():
#         return "Error: email.txt not found."

#     with email_path.open("r") as f:
#         email_content = f.read()

#     prompt = f"Extract the sender email from the following email:\n{email_content}"
#     sender_email = call_llm(prompt)

#     with output_path.open("w") as f:
#         f.write(sender_email)

#     return "Extracted sender email."

# def extract_credit_card():
#     """Extracts credit card number using LLM."""
#     from PIL import Image
#     image_path = Path(DATA_DIR) / "credit-card.png"
#     output_path = Path(DATA_DIR) / "credit-card.txt"

#     if not image_path.exists():
#         return "Error: credit-card.png not found."

#     img = Image.open(image_path)
#     prompt = "Extract the credit card number from this image."
#     card_number = call_llm(prompt, image=img)

#     with output_path.open("w") as f:
#         f.write(card_number.replace(" ", ""))

#     return "Extracted credit card number."

# def format_markdown(file_path, prettier_version="3.4.2"):
#     """Formats a Markdown file using Prettier."""
#     cmd = ["npx", f"prettier@{prettier_version}", "--write", file_path]
#     result = subprocess.run(cmd, capture_output=True, text=True)

#     return f"Formatted {file_path}" if result.returncode == 0 else result.stderr

# TASK_HANDLERS = {
#     "install uv": run_datagen,
#     "count weekdays": lambda: count_weekdays("Wednesday", "data/dates.txt", "data/dates-wednesdays.txt"),
#     "extract email sender": extract_email_sender,
#     "credit card number": extract_credit_card,
#     "format markdown": lambda: format_markdown("data/format.md"),
# }

# def execute_task(task: str):
#     """Finds the best-matching task and executes it."""
    
#     # Normalize task input (convert to lowercase)
#     task_lower = task.lower()
    
#     # Get the best matching predefined task using fuzzy matching
#     best_match, score = process.extractOne(task_lower, TASK_HANDLERS.keys())
    
#     # Execute if confidence score is high enough (e.g., above 70)
#     if score >= 70:
#         return TASK_HANDLERS[best_match]()
    
#     # If no match found, fallback to LLM classification
#     prompt = f"Classify the following task into one of these: {list(TASK_HANDLERS.keys())}.\nTask: {task}"
#     classified_task = call_llm(prompt).lower()
    
#     if classified_task in TASK_HANDLERS:
#         return TASK_HANDLERS[classified_task]()
    
#     return f"Task not recognized: {task}"

def read_file(path):
    """Reads the contents of a file."""
    with open(path, "r") as f:
        return f.read()

def execute_task(task: str):
    """Passes task to LLM and executes the suggested command."""
    
    # Generate a structured response from LLM
    prompt = f"""
    You are an AI agent. Given the user task below, generate a structured response.
    1. Identify the task type (e.g., "run script", "format file", "extract data").
    2. Extract any relevant details (file names, versions, options).
    3. Output a valid shell command or Python function call to execute the task.

    Task: {task}
    Response format:
    {{
      "task_type": "format file",
      "command": "npx prettier@3.4.2 --write data/format.md"
    }}
    """
    
    response = call_llm(prompt)

    try:
        task_data = eval(response)  # Convert string to dictionary safely
        command = task_data.get("command")
        
        if command:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return {"status": "success", "output": result.stdout or result.stderr}
        else:
            return {"status": "error", "message": "No command generated by LLM"}
    
    except Exception as e:
        return {"status": "error", "message": f"Invalid LLM response: {response}, Error: {str(e)}"}
